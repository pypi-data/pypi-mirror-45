from __future__ import print_function
import os
import sys
import signal
import re
import stat
import shutil
import shlex
import logging
import subprocess
from threading import Timer

PY = sys.version_info[0]

"""
This module provide some useful functions.
"""


def run_command(cmd, cwd=None, shell=True, stdout=False, timeout=30):
    """Run command with a timeout timer.

    Arguments:
        cmd -- {str or list} command string or list, like subprocess
        cwd -- {str} process work directory.
        stdout -- {bool} return stdout, default: False.
        timeout -- {int} timeout seconds, default: 30(s)

    Returns:
        Tuple -- (returncode, output)
    """
    output = ""
    returncode, timer, error_message = None, None, None

    logging.debug(cmd)

    if shell:
        # python documentation:
        # On Windows, The shell argument (which defaults to False) specifies whether to use the shell as the program to execute.
        # If shell is True, it is recommended to pass args as a string rather than as a sequence.
        if isinstance(cmd, list):
            cmd = " ".join(cmd)
    else:
        # Windows platform, convert cmd to list to will lead out the slash issue.
        if os.name == 'nt':
            if not isinstance(cmd, list):
                cmd = shlex.split(cmd)

    kwargs = {
        "stdout": subprocess.PIPE if stdout else None,
        "stderr": subprocess.STDOUT,
        "cwd": cwd,
        "shell": shell
    }

    if PY > 2:
        kwargs['encoding'] = 'utf8'

    try:
        process = subprocess.Popen(cmd, **kwargs)

        #start timer
        timer = Timer(timeout, _timeout_trigger, args=(process,))
        timer.start()

        output, error = process.communicate()
        returncode = process.returncode

        if returncode != 0:
            error_message = 'Error: {0}\n  exit code:  {1}\n'.format(cmd, process.pid)
            if output:
                error_message + '  console output: %s'%(output)
            logging.debug(error_message)

    except OSError as emsg:
        logging.exception(emsg)

    finally:
        if timer:
            timer.cancel()

    return returncode, output



def _timeout_trigger(pro):
    """Timeout will kill the group processes.

    [Timeout will kill the group processes]

    Arguments:
        pro {Popen object} -- process
    """

    if os.name == "nt":
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pro.pid))
    else:
        pro.kill()

    logging.info("--- process operation timeout---")



def check_occupation(keyword):
    '''
    This function only worked for windows.
    keyword: the particial name of the file.
    Use handle.exe to dump the process infomation, and
    return a dictonary that the key is pid, value is a
    list.

    handle.exe
        Handle is a utility that displays information about
        open handles for any process in the system. You can
        use it to see the programs that have a file open, or
        to see the object types and names of all the handles
        of a program.
    '''

    if os.name != 'nt':
        return None

    occupations = dict()
    exclude_apps = ["explorer.exe", "STAFProc.exe", "Git.exe"]

    handle_pipe = os.popen("{0}/bin/handle.exe -u {1} -nobanner -accepteula" \
    .format(os.path.dirname(__file__), keyword), "r")

    content = handle_pipe.readlines()
    if "No matching handles found" in content[0]:
        return occupations

    #merge process
    for line in content:
        try:
            process_name = line.split()[0]
            if process_name not in exclude_apps:
                pid = re.findall(r'pid: \d+', line)[0].replace("pid: ", "")
                occupations[pid] = (process_name, line)
        except Exception as e:
            pass

    return occupations



def remove_occupation(path):
    """
    Query file if is open by another process and kill the process.
    It only works on windows.

    Args:
        path: the path of directory or file.

    Retruns:
        bool: True/False
    """
    if os.name != "nt":
        return True

    logging.debug("Query unclosed hanlder by path: '%s'", path)

    occupations = check_occupation(os.path.normpath(path))
    for (key, value) in occupations.items():
        print("CLOSE HANDLER PID: %s Name: %s"%(key, value[0]))
        if os.system("taskkill /PID %s /F"%key) != 0:
            print("Failed to kill process (pid: %s) name: %s", key, value[0])

    return True



def rmtree(path):
    """Remove directory tree. If failed , it will check the access and force
    to close unclosed handler, then try remove agagin.
    """
    try:
        shutil.rmtree(path)
    except Exception:
        # Is the error an access error ?
        if not os.access(path, os.W_OK):

            os.chmod(path, stat.S_IWUSR)

        # Readonly on windows
        if os.name == "nt":
            subprocess.check_call(('attrib -R ' + path + '\\* /S').split())

        remove_occupation(path)
        shutil.rmtree(path)




def onerrorHandler(func, path, exc_info):
    """Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)


def copydir(root_src_dir, root_dst_dir):
    """Copy directory to dst dir."""
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = os.path.normpath(src_dir.replace(root_src_dir, root_dst_dir, 1))
        print("copying %s"%dst_dir)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.normpath(os.path.join(src_dir, file_))
            dst_file = os.path.normpath(os.path.join(dst_dir, file_))
            if os.path.exists(dst_file):
                os.chmod(dst_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) # 0777
                os.remove(dst_file)
            shutil.copy(src_file, dst_file)


def change_folder_security_win(path):
    """
    Change folder security.
    Add full control for current login user.

    param path: the folder path.
    return bool, command exited code == 0, or not.


    https://stackoverflow.com/questions/2928738/how-to-grant-permission-to-users-for-a-directory-using-command-line-in-windows

    According do MS documentation:

    F = Full Control
    CI = Container Inherit - This flag indicates that subordinate containers will inherit this ACE.
    OI = Object Inherit - This flag indicates that subordinate files will inherit the ACE.
    /T = Apply recursively to existing files and sub-folders. (OI and CI only apply to new files and
    sub-folders). Credit: comment by @AlexSpence.
    For complete documentation, you may run "icacls" with no arguments or see the Microsoft documentation.

    """
    assert os.name == "nt"
    login_username = os.environ.get("USERNAME")
    path = os.path.normpath(path)
    return os.system('''icacls {0} /grant {1}:(OI)(CI)F /T'''.format(path, login_username))==0


