import os
import glob
import logging
import tempfile
from distutils.version import LooseVersion
from xml.etree import cElementTree as ET
from difflib import SequenceMatcher
from mcutk.exceptions import ProjectNotFound, ProjectParserError
from mcutk.apps.projectbase import ProjectBase
from mcutk.apps import eclipse


class Project(eclipse.Project):
    """MCUXpresso SDK and projects parser tool."""

    PROJECT_EXTENSION = '*.xml'


    @classmethod
    def frompath(cls, path):
        """Return a project instance from a given file path or directory.

        If path is a directory, it will search the project file and return an instance.
        Else this will raise mcutk.apps.exceptions.ProjectNotFound.
        """

        if os.path.isfile(path):
            return cls(path)

        if not cls.PROJECT_EXTENSION:
            raise ValueError("Error, %s.PROJECT_EXTENSION is not defined! Please report an bug!"%cls)

        instance = None

        for file in glob.glob(path + "/.project"):
            with open(file) as f:
                content = f.read()
                if '<name>mcux</name>' in content or 'mcuxpresso' in content:
                    instance = cls(file)
                    break

        if instance:
            return instance

        for file in glob.glob(path + "/*" + cls.PROJECT_EXTENSION):
            if 'example.xml' not in file:
                project_file = file
                try:
                    instance = cls(project_file)
                    break
                except ProjectParserError:
                    pass
        else:
            raise ProjectNotFound("Not found %s in specific folder"%cls.PROJECT_EXTENSION)

        return instance


    def __init__(self, prjpath, sdk_root=None, **kwargs):
        """MCUXPressoIDE project constructor.

        Arguments:
            prjpath {str} -- path to <name>.xml

        Keyword Arguments:
            sdk_root {str} -- path to sdk package root, default {None} that will be loaded from xml.
        """
        super(Project, self).__init__(prjpath, **kwargs)
        self._is_package = False
        self._sdk_root = sdk_root
        self._name = ''
        self._targets = None
        self._nature = 'org.eclipse.cdt.core.cnature'

        # eclipse project
        self._is_package = not (prjpath.endswith('.project') or prjpath.endswith('.cproject'))

        if self._is_package:
            self._load_from_sdk_package(prjpath)
            self._properties_init()
        else:
            self._load_from_eclipse_project(prjpath)


    @property
    def sdk_root(self):
        return self._sdk_root



    @sdk_root.setter
    def sdk_root(self, value):
        """Attribute setter for: sdk_root

        Find and check mcuxpresso manifest file,
        If not found, it will raise IOError.
        """
        if not os.path.exists(value):
            raise IOError("Path is not exists.")
        try:
            self._find_latest_manifest(value)
        except ProjectParserError:
            raise IOError("Not found SDK manifest, invalid NXP MCUXPresso SDK.")

        self._sdk_root = value


    @property
    def is_package(self):
        """Package project or standard eclipse project"""
        return self._is_package



    def _load_from_eclipse_project(self, path):
        """Load from Eclipse C/C++ project"""
        self.parse(path)



    def _load_from_sdk_package(self, path):
        """Load from SDK <app>.xml and *_manifest*.xml.
            1. Parse <app>.xml to get manifest.xml,
            2. Get related information from manifest.
        """

        self._targets = self._conf.keys()

        xmlroot = ET.parse(path).getroot()
        example_node = xmlroot.find('./example')
        if example_node is None:
            raise ProjectParserError('Unable to find <example> node.')

        self._example_id = example_node.attrib.get('id')
        self._name = example_node.attrib.get('name')

        try:
            self._nature = example_node.find('projects/project[@nature]').attrib.get('nature')
        except:
            pass

        if not self._example_id:
            raise ProjectParserError('None id in exmaple node! %s'%self.prjpath)


        self._conf = {
            'Debug': self.name + '/Debug/',
            'Release': self.name + '/Release/'
        }

        if self.sdk_root:
            return

        # if sdk_root is not ready
        prjdir_abs = os.path.abspath(self.prjdir).replace('\\', '/')

        def _get_sdk_root(prjdir, node):
            """get sdk_root from an XML element node."""
            if node is None:
                return

            source_path = node.attrib.get('path')
            if not source_path:
                return

            if source_path in prjdir:
                sdk_root = prjdir.replace(source_path, "")
            else:
                match = SequenceMatcher(None, prjdir, source_path).find_longest_match(0, len(prjdir), 0, len(source_path))
                sdk_root = prjdir[:match.a]

            if os.path.exists(sdk_root):
                return sdk_root
            return

        # at fist to find the element with attribute src
        self._sdk_root = _get_sdk_root(prjdir_abs, example_node.find('./source[@type="src"]'))
        if self._sdk_root:
            return

        # if previous is failed, loop all source elements to get sdk_root
        for node in example_node.findall('./source'):
            self._sdk_root = _get_sdk_root(prjdir_abs, node)
            if self._sdk_root:
                return

        # In some situation, example.xml not include the source element.
        # Added a workaround to find mainfest file in it's parent.
        current_dir = prjdir_abs
        while True:
            parent_dir = os.path.dirname(current_dir)
            # system root
            if parent_dir == current_dir:
                break
            try:
                self._find_latest_manifest(parent_dir)
                self._sdk_root = parent_dir
                break
            except ProjectParserError:
                pass
            current_dir = parent_dir

        if self._sdk_root:
            return self._sdk_root

        # Finally raise error, need to manual check by developer!
        raise ValueError('Cannot get sdk root! XML path: %s'% self.prjpath)




    def _properties_init(self):
        """Init build properties variable.

        sdk.location = D:/Users/B46681/Desktop/SDK_2.0_MK64FN1M0xxx12-drop4
            This is the location where your SDK have been downloaded.
            You can use either zip or folder containing the SDK
            Please remember that if you want to create linked resources into your project(i.e. standalone = false) you need to use a folder instead of a zip.
            NOTE: on Windows you have to use "//" or "/".

        example.xml = D:/Users/B46681/Desktop/SDK_2.0_MK64FN1M0xxx12-drop4/boards/frdmk64f/demo_apps/hello_world/mcux/hello_world.xml
            If adding the "example.xml" property, the examples are retrieved from that specific file and shall valid against the used SDK
            NOTE: on Windows you have to use "//" or "/".

        nature = org.eclipse.cdt.core.cnature
            This represents the nature of your project (i.e. C or C++)
            It can be:
                - org.eclipse.cdt.core.cnature for C projects
                - org.eclipse.cdt.core.ccnature for C++ projects
                (Please remember that the example your're going to create shall support the C++ nature)

        standalone = true
            If true, it will copy the files from the SDK, otherwise it will link them.
            Note: linked resources will be only created if the SDK is provided as a folder

        project.build = true
            If true, the project will be compiled, otherwise the project is only created.

        clean.workspace = true
            True, if you want to clear the workspace used, false otherwise

        build.all = false
            If true, all the examples from all the SDK will be created, otherwise you need specify the SDK name

        skip.default = false
            If true, skip the default SDKPackages folder and all its content
            Default is false

        sdk.name = SDK_2.0_MK64FN1M0xxx12
            The SDK name (i.e. the folder/file name without extension)
            NOTE: only used when build.all = false

        board.id = frdmk64f
            The board id as for the manifest definition
            NOTE: only used when build.all = false

        Other Settings:
            verbose = true
                If true, more info will be provided using stdout

            indexer = false
                If true, enable the CDT indexer, false otherwise

            project.build.log = true
                If true, show the CDT build log, false otherwise

            simple.project.name = true

        """
        self._buildproperties = {
            'sdk.location': None,
            'example.xml': None,
            'nature': 'org.eclipse.cdt.core.cnature',
            'standalone': 'true',
            'project.build': 'true',
            'clean.workspace': 'true',
            'build.all': 'false',
            'build.config': 'debug',
            'simple.project.name': 'true',
            'skip.default': 'true',
            'sdk.name': None,
            'board.id': '',
            'verbose': 'false',
            'indexer': 'false',
            'use.io.console': 'false',
            'project.build.log': 'true'
        }


    def gen_properties(self, target, dir=None):
        """Return a file path for properties file.

        Arguments:
            target -- {string} target configuration
            dir -- {string} the location to place the new geneated file, default is system tempfile.

        """
        sdkmanifest = SDKManifest(self._find_latest_manifest(self._sdk_root))
        boardid = self._example_id.split('_')[0]

        logging.info("SDK Manifest Version: %s", sdkmanifest.manifest_version)

        self.setproperties("example.xml", self.prjpath.replace('\\', '/'))
        self.setproperties("sdk.location", self._sdk_root.replace('\\', '/'))
        self.setproperties("nature", self.nature)
        self.setproperties("sdk.name", sdkmanifest.sdk_name)
        self.setproperties("board.id", boardid)
        self.setproperties("build.config", target)


        with tempfile.NamedTemporaryFile(dir=None, delete=False, prefix="mcuxpresso_", mode='w') as f:
            for per_property, value in self._buildproperties.items():
                f.writelines("{0} = {1}\r\n".format(per_property, value))
            properties_file = f.name

        logging.debug('properties file: %s', properties_file)
        return properties_file




    def _find_latest_manifest(self, sdk_root):
        """ Get the max version of manifest file path"""

        manifestfilelist = glob.glob("{0}/*_manifest*.xml".format(sdk_root))
        if not manifestfilelist:
            raise ProjectParserError("cannot found manifest file")

        file_versions = {}
        for per_file in manifestfilelist:
            version_str = per_file.replace('.xml', '').split('_manifest')[-1]
            version =  version_str[1:] if version_str.startswith('_') else version_str
            if version:
                file_versions[version] = per_file

        ver_latest = sorted(file_versions.keys(), key=lambda v: LooseVersion(v))[-1]
        return file_versions[ver_latest].replace("\\",'/')



    def setproperties(self, attrib, value):
        """ Set the value of self._buildproperties"""

        self._buildproperties[attrib] = value




    @property
    def nature(self):
        return self._nature



    @property
    def targets(self):
        """Return all targets name

        Returns:
            list -- a list of targets
        """
        if self._targets:
            return list(self._targets)
        else:
            return ['Debug', 'Release']


    @property
    def name(self):
        """Return the application name

        Returns:
            string --- app name
        """
        return self._name








class SDKManifest(object):
    """NXP MCUXpresso SDK Manifest Parser."""

    def __init__(self, filepath):
        xmlParser = ET.parse(filepath)
        self._xmlroot = xmlParser.getroot()

        self._manifest_version = self._xmlroot.attrib['format_version']
        self._sdk_name = self._xmlroot.attrib["id"]
        self._sdk_version = self._xmlroot.find('./ksdk').attrib['version']

    @property
    def sdk_version(self):
        return self._sdk_version



    @property
    def sdk_name(self):
        return self._sdk_name

    @property
    def manifest_version(self):
        return self._manifest_version

