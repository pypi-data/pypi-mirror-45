#!/usr/bin/env python

# Copyright (c) 2015-2016 Freescale Semiconductor, Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, this list
#   of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# o Neither the name of Freescale Semiconductor, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#####
# Author: Haley, Date: 2016.9.13
#####
from __future__ import print_function
import os
import re
import io
import time
import glob
import shutil
import platform
import logging
import subprocess
import datetime

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from mcutk import util
from mcutk.exceptions import CodeSyncError, BranchError


bin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin')



def _get_repo_url(path):
    ret, output = util.run_command('git config --get remote.origin.url', cwd=path, stdout=True, shell=True)
    if ret != 0:
        logging.warning('Not a valid git repository.')
        return None

    return output.replace('\\n', '').strip()




class Repo(object):
    """Class Repo provide an abstract model access for git repositories, it is warpper
    based on git tool. Many useful built in abstactions or shortcut functions make the
    git call is very easy so that you don't need to handle process call by subprocess
    or others.

    Exmaple 1:
        >>> repo = Repo("ssh://exmaple.git")
        >>> repo.is_ready
        >>> repo.Clone("/home/")

    Exmaple 2:
        >>> repo = Repo.frompath("C:/mcu-sdk-2.0")
        >>> print repo.repo_url
        >>> print repo.is_ready
        >>> print repo.get_branch_name()
        >>> print repo.get_latest_commit_message()
        >>> print repo.get_submodules()
        >>> repo.checkout_branch("dev")
        >>> repo.exec_commands(["git status", "git --version"])
    """


    @classmethod
    def frompath(cls, path):
        """Return a repo object from specific path."""

        url = _get_repo_url(path)
        if url:
            return cls(url, path)






    def __init__(self, repo_url, repo_dir=None):
        """Create a repo instance.

        params:
            - repo_url: repo remote address.
            - repo_dir: the directory of repo on your local file system.
        """
        self.repo_dir = repo_dir
        self.repo_url = repo_url
        self.occupations = dict()
        self.repo_name = repo_url.split("/")[-1].replace(".git", "")
        self.repo_domain = repo_url.replace(self.repo_name+".git", "")
        self.need_modify_gitmodules = False


    def __str__(self):
        return "Repo(%s)"%self.repo_url



    def __exec(self, cmd, cwd=None, t=3600, retry=2):
        if cwd == None:
            cwd = self.repo_dir

        for _ in range(retry):
            noerror, output = util.run_command(cmd, cwd=cwd, stdout=True, timeout=t)
            if noerror == 0:
                break
            logging.info("retry again..")
        else:
            raise CodeSyncError("Run command {0} failure".format(cmd))

        return output



    @property
    def is_ready(self):
        if not os.path.exists(str(self.repo_dir)):
            return False

        url_c = _get_repo_url(self.repo_dir)

        if not url_c:
            return False

        if urlparse(self.repo_url).path == urlparse(url_c).path:
            return True
        else:
            logging.error(" Error: " + output + self.repo_url)
            return False




    def exec_commands(self, cmds):
        """Execute a list of commands.

        Arguments:
            cmds {list} -- a list of commands
        """
        for cmd in cmds:
            self.__exec(cmd)




    def checkout_branch(self,
                        branch_name,
                        tag_name=None,
                        submodule_deinit=True,
                        submodule_update=True,
                        shallow_fetch=False):
        """Fetch and checkout to specific branch, and make the branch update to date.

        Execute git commands, and try several times if any steps are failed.
            1. git reset --hard
            2. git clean -fxd
            3. git deinit -f .
            4. git fetch -t origin <branch name>
            5. git checkout <branch name>
            6. git submodule update --init

        Arguments:
            branch_name {str} -- branch name or hash

        Keyword Arguments:
            tag_name {str} -- tag name (default: {None})
            submodule_deinit {bool} -- do submodule deinit (default: {True})
            submodule_update {bool} -- do submodule update (default: {True})
            shallow_fetch {bool} -- do shallow fetch (default: {False})

        Raises:
            BranchError -- When branch is not exists
            CodeSyncError -- When any git operation failed.


        Returns:
            bool -- success or not
        """
        logging.info("start to update repo...")

        if shallow_fetch:
            fetch_command = 'git fetch --depth 10 -t origin %s'%branch_name
        else:
            fetch_command = 'git fetch -t origin %s'%branch_name

        try:
            if submodule_deinit and submodule_update:
                self.__exec('git submodule deinit -f .')

            self.__exec('git reset --hard', retry=1)
            self.__exec('git clean -fxd', retry=1)
        except CodeSyncError:
            if os.name == "nt":
                util.change_folder_security_win(self.repo_dir)
            Repo.remove_index_lock(self.repo_dir)
            util.remove_occupation(self.repo_dir)
            self.__exec('git reset --hard')
            self.__exec('git clean -fxd')


        try:
            self.__exec(fetch_command, retry=4)
        except CodeSyncError:
            raise BranchError("Fetch Branch Error!")

        self.__exec('git checkout %s'%branch_name)
        self.__exec('git merge origin/%s'%branch_name)
        if tag_name:
            self.__exec('git checkout %s'%tag_name)

        if submodule_update:
            return self.update_submodules(self.repo_dir)



    def get_latest_commit_message(self, repo_dir=None):
        """Return the commit message on the head

        Default work directory is the main repo.
        """
        if not repo_dir:
            repo_dir = self.repo_dir
        try:
            return self.__exec("git log -n 1", cwd=repo_dir, t=1)
        except Exception as e:
            return "Failed to get commit message for %s"%repo_dir


    def get_branch_name(self, repo_dir=None):
        """Return branch name.

        Default work directory is the main repo.
        """
        if not repo_dir:
            repo_dir = self.repo_dir
        return self.__exec("git rev-parse --abbrev-ref HEAD", cwd=repo_dir, t=1).replace("\n", "").strip()


    def get_submodules(self, repo_dir=None):
        """Return a dictionary about all submodules.

        Default return the main submodules.
        """
        if not repo_dir:
            repo_dir = self.repo_dir

        gitmodules = os.path.join(repo_dir, ".gitmodules")
        if os.path.exists(gitmodules) is False:
            return None

        mod_parser = configparser.RawConfigParser()
        with open(gitmodules) as f:
            content = f.read().replace("\t", "").decode('utf-8')
            fakefile = io.StringIO(content)

        mod_parser.readfp(fakefile, filename=gitmodules)
        modules = mod_parser.sections()
        modules_dict = dict()

        for modname in modules:
            url = mod_parser.get(modname, "url")
            path = os.path.join(self.repo_dir, mod_parser.get(modname, "path"))
            modules_dict[modname.replace("submodule ", "").replace("\"", "")] = Repo(url, path)

        return modules_dict



    def relace_submodules_url(self, pattern, repl):
        """Replace submodule configuration in .gitmodules.

            Due to Freescale code server is migrated to bitbucket.
            We need update stash to bitbucket!
            Mirror server for mcu-sdk-2.0.
        """
        gitmodules = os.path.join(self.repo_dir, ".gitmodules")

        if os.path.exists(gitmodules) is False:
            return None

        submodule_list = list()
        with open(gitmodules, "r+") as file:
            lines = file.readlines()
            for i in xrange(len(lines)):
                # parse the submodule url
                if lines[i].find("path = ") != -1:
                    path = self.repo_dir + "/" + lines[i].replace("\t", "").replace("\n", "").split(" = ")[1]
                    submodule_list.append(path)

                # update url host
                elif lines[i].find("url = ") != -1:
                    # sub sw-stash to bitbucket
                    lines[i] = re.sub('ssh://git@sw-stash.freescale.net/',
                                      'ssh://git@bitbucket.sw.nxp.com/',
                                      lines[i])
            file.seek(0)
            file.truncate()
            content = "".join(lines)
            file.write(content)

        return submodule_list



    def update_submodules(self, repo_dir):
        """Update submodules
            functions instruction:
                # update submodules
                # 1> get commit message
                # 2> get current branch
                # 3> if need, update gitsubmodules configurations
                # 4> git submodule deinit -f .
                # 5> git submodule update --init
        """
        message = self.get_latest_commit_message(repo_dir)
        branch = self.get_branch_name(repo_dir)
        logging.info("-- SUBMODULE: %s --\ncurrent branch: %s\n%s", repo_dir.replace(self.repo_dir, ""), branch, message)

        submodules_path = self.get_submodules()
        if not submodules_path:
            return


        try:
            self.__exec('git submodule update --init --recursive', cwd=repo_dir, t=100)
        except CodeSyncError:
            # sometimes the command is failed, due to submodule index.lock is exists.
            # delete the index lock
            Repo.remove_index_lock(self.repo_dir)
            self.__exec('git submodule deinit -f .')
            self.__exec('git submodule update --init --recursive', cwd=repo_dir, t=100)


        for p in submodules_path:
            message = self.get_latest_commit_message(p)
            branch = self.get_branch_name(p)
            logging.info("-- SUBMODULE: %s --\ncurrent branch: %s\n%s",
                        repo_dir.replace(p, ""),
                        branch,
                        message)






    def _apply_patch(self, patch):
        """Apply patch file. If failed, will convert format and try again.

        Returns:
            Bool, True or False.

            Git command:
                git apply --ignore-space-change --ignore-whitespace <patch>
        """
        work_dir = os.path.dirname(patch)
        cmd = "git apply --ignore-space-change --ignore-whitespace %s"%os.path.basename(patch)

        try:
            self.__exec(cmd, cwd=work_dir)
        except Exception as e:
            logging.error('apply patch failed, may caused by format reasons, try to converting format....')

            rc = util.run_command(bin_path + '/unix2dos ' + patch)[0]
            if rc != 0:
                logging.error('Failed to convert patch format!')
                return False

            logging.info('Convert format successfully, try to apply patch again...')

            try:
                self.__exec(cmd, cwd=work_dir)
            except Exception as e:
                logging.error('Try to apply patch failed!')
                return False

        logging.info('apply patch successfully')
        return True



    def apply_patch(self, repo_dir, patch):
        """Apply patch for given repo location.

        params:
            repo_dir: repo directory
            patch: the path of patch file. Maybe a zipped file or
            a patch file.

        Returns:
            bool, True or False.
        """
        def __get_dst_path(repo_dir_path, patch_file_name):
            if '_sub' in patch_file_name.lower() or '_usb' in patch_file_name.lower():
                return repo_dir_path+'/middleware/usb/' + patch_file_name
            else:
                return repo_dir_path+'/'+patch_file_name


        if not os.path.exists(patch):
            return False

        apply_ret = True

        # .zip include multi patch files
        if patch.endswith('.zip'):
            patch_dirname = os.path.dirname(patch)
            patch_name = os.path.basename(patch)
            unzip_folder = patch_dirname + '/' + os.path.splitext(patch_name)[0]

            rc = util.run_command(bin_path + '/unzip -o ' + patch + ' -d ' + unzip_folder)[0]

            if rc != 0:
                logging.error('unzip patch file failed')
                return False

            unzip_patch_path = unzip_folder + '/tmp'
            for filename in os.listdir(unzip_patch_path):
                src_patch_path = os.path.join(unzip_patch_path, filename)
                dst_patch_path = __get_dst_path(repo_dir, filename)

                #copy patch to repo_dir
                shutil.copyfile(src_patch_path, dst_patch_path)
                apply_ret = self._apply_patch(dst_patch_path)
                if apply_ret is False:
                    break

        else:
            filename = os.path.basename(patch)
            #single patch will be only applied in mian dir
            dst_patch_path = repo_dir+'/'+filename#__get_dst_path(repo_dir, filename)
            shutil.copyfile(patch, dst_patch_path)
            apply_ret = self._apply_patch(dst_patch_path)

        return apply_ret



    def get_head_hash(self):
        """Return commit hash from head."""
        return self.__exec("git rev-parse HEAD", t=1).replace("\n", "").strip()




    def get_history_abbrev(self, since="1.weeks"):
        """Useful options for git log --pretty=format
            Option	Description of Output
            %H Commit hash
            %h Abbreviated commit hash
            %T Tree hash
            %t Abbreviated tree hash
            %an Author name
            %ae Author e-mail
            %ad Author date (format respects the -date= option)
            %ar Author date, relative
            %cn Committer name
            %ce Committer email
            %cd Committer date
            %cr Committer date, relative
            %s Subject

        Reference:
            https://git-scm.com/book/tr/v2/Git-Basics-Viewing-the-Commit-History
            https://git-scm.com/docs/git-log
        """
        if since.split(".")[1] not in ["days", "weeks"]:
            raise ValueError("argument is not valid format,")

        return util.run_command('git log --pretty=format:"#### %h - %cr - %an: %s" --since={0} --stat'.format(since),
                                cwd=self.repo_dir)[1]



    def get_history(self, since="1.weeks"):
        """Extract commits history details.

            git log -p --since=1.weeks
        """
        if since.split(".")[1] not in ["days", "weeks"]:
            raise ValueError("argument is not valid format,")

        return util.run_command('git log -p --since={0}'.format(since),
                                cwd=self.repo_dir)[1]


    def get_remote_branches(self):
        """Fetch all of branches from remote.

        Returns: A list of branches.
        """
        content = util.run_command("git ls-remote --heads", cwd=self.repo_dir)[1]
        branches = [line.split("heads/")[1].strip() for line in content.split("\n") \
                    if "refs/heads/" in line]

        return branches



    def remote_update(self):
        """git remote update --prune origin
        """
        self.__exec("git remote update --prune origin")





    def generate_history_report(self, outdir, branches=None):
        """Generate commits history report for specific branches.

        Arguments:
            outdir {str} -- path to output direcotry

        Keyword Arguments:
            branches {list} -- list of branches (default: {None})
                               If None, it will fetch and check all of branches.
                               This may will take a long time and use many disks.
        Raises:
            CodeSyncError -- Git command failed.

        """

        print("=====================================")
        print("Repo: {0}\nUrl: {1}".format(self.repo_name, self.repo_url))

        current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        report_folder = os.path.join(outdir, self.repo_name+"_"+current_time)

        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

        if not branches:
            branches = self.get_remote_branches()

        if len(branches) > 200:
            logging.warning("Program will statistic all of branches, %s",
                            "this will take a long time if the repo is too big!")

        print("branches count: ", len(branches))

        for index, branch in enumerate(branches):
            print("> {0:5}  {1}".format(index+1, branch))

            self.checkout_branch(branch, submodule_deinit=False, submodule_update=False, shallow_fetch=False)
            print("> head now on: " + self.get_branch_name(self.repo_dir))

            brief = self.get_history_abbrev()
            full = self.get_history()

            report = ("# {0}: {1} \n\n## SUMMARY: \n{2}\n\n"\
                      "## ALL CHANGES: \n{3}").format(self.repo_name, branch, \
                                                      brief, full)

            report_file = os.path.normpath(report_folder+"/{0}.md".format(branch))
            with open(report_file, "w") as fobj:
                fobj.write(report)

            print("> generated %s"%report_file)




    def clone(self, clone_path, branch_name='master', foldername=None):
        """Clone specific branch to specific directory.

        Arguments:
            clone_path {str} -- directory to clone

        Keyword Arguments:
            branch_name {str} -- branch name (default: {'master'})
            foldername {str} -- folder name (default: {None})

        Returns:
            repo_dir

        Documentation about git clone:
            --depth=<depth>
                Create a shallow clone with a history truncated to the specified number of commits.
                Implies --single-branch unless --no-single-branch is given to fetch the histories
                near the tips of allbranches. If you want to clone submodules shallowly also pass
                --shallow-submodules.


            --branch <name>
            -b <name>
                Instead of pointing the newly created HEAD to the branch pointed to by the cloned
                repository's HEAD, point to <name> branch instead. In a non-bare repository, this
                is the branch that will be checked out. --branch can also take tags and detaches
                the HEAD at that commit in the resulting repository.
        """
        logging.info("prepare to clone repo")
        os.chdir(clone_path)
        clone_cmd = 'git clone --depth 10 -b {0} {1}'.format(branch_name, self.repo_url)

        # clone to specific dest folder
        if foldername:
            clone_cmd += " " + foldername
        else:
            # default folder
            dir_name = self.repo_name

        #clone single branch, instead of all branches
        noerror = util.run_command(clone_cmd)[0]

        if not noerror:
            raise CodeSyncError("Failed to clone repo!")

        self.repo_dir = os.path.join(clone_path, dir_name)
        self.__exec('git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"')
        logging.info('---clone repo successfully---')
        return self.repo_dir



    def autosync(self,
                 repo_parent_dir,
                 branchs="master",
                 patch=None,
                 submodule_deinit=True,
                 submodule_update=True):
        """Automatic sync this repo.

        This function can be used in bellow situations:
            1. We don't know it is ready in local.
            2. We hope to simple the repo update.

        Arguments:
            repo_parent_dir {str} -- the root directory of the repo is located

        Keyword Arguments:
            branch {str} -- branch name (default: {"master"})
            patch {str} -- path to patch file (default: {None})
            submodule_deinit {bool} -- do submodule deinit (default: {True})
            submodule_update {bool} -- do submodule update (default: {True})

        Returns:
            bool.
        """
        #Parser branch name and tag name
        branch_name, tag_name = branchs, None
        if "%" in branchs:
            try:
                name_list = branchs.split('%')
                branch_name = name_list[0]
                tag_name = name_list[1]
            except Exception as e:
                pass

        logging.info("Repo url: %s, Branch: %s, Tag: %s.", self.repo_url, branch_name, tag_name)

        if not os.path.exists(repo_parent_dir):
            os.makedirs(repo_parent_dir)

        # Get repo dir from main repo parent
        if not self.repo_dir:
            self.repo_dir = get_repo_location(repo_parent_dir, self.repo_name, self.repo_url)


        # Clone repo to repo_parent_dir
        if not self.is_ready:
            self.repo_dir = self.clone(repo_parent_dir, branch_name)


        logging.info(self.repo_dir)
        # checkout & update repo
        self.checkout_branch(branch_name,
                             tag_name,
                             submodule_deinit,
                             submodule_update)

        # Apply patch
        if patch:
            if self.apply_patch(self.repo_dir, patch) is False:
                return False

        logging.info("---- Sync successfully %s ----", self.repo_dir)
        return True



    @staticmethod
    def remove_index_lock(repo_dir):
        gitdir = repo_dir+"/.git"
        if os.path.exists(gitdir) is False:
            return

        try:
            for parent, _, filenames in os.walk(gitdir):
                for filename in filenames:
                    if ".lock" in filename:
                        path = os.path.join(parent, filename)
                        os.remove(path)

        except Exception:
            logging.exception("remove git lock failure")




def _repo_is_match(repo_dir, repo_url):
    '''
    check if the specified repo is adentical with the repo_url
    '''
    if os.path.isdir(repo_dir) is False:
        return False
    output = subprocess.check_output('git remote -v', cwd=repo_dir, shell=True)
    return repo_url in output





def get_repo_location(maindir, repo_name, repo_url):
    '''
    Search local repo in maindir,
    Return True: This repo is ready to use.
    Return False: Need Clone.
    '''
    # Search local repo in repo_parent_dir
    dirlist = glob.glob(maindir+"/"+repo_name)
    try:
        path = dirlist[0]
        output = subprocess.check_output('git remote -v', cwd=path, shell=True)
        logging.debug(output)
        return path

    except IndexError as e:
        logging.warning("Not found repo")
        return None

    except subprocess.CalledProcessError:
        logging.warning("Repo is damaged. Trying to delete directory: {0}".format(path))
        util.rmtree(path)
        return None






