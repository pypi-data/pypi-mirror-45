try:
    from .base_class import DynamicRobotApiClass
except ImportError:
    from base_class import DynamicRobotApiClass

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from furl import furl
from http.cookies import SimpleCookie
import os
import sys

PY2 = sys.version_info < (3,)
PY3 = sys.version_info > (2,)

def inside_virtualenv():
    return hasattr(sys, 'real_prefix') or hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def from_path(program):
    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path, program)
        if is_exe(exe_file):
            return exe_file

    return None


def from_root(program):
    for root, dirs, files in os.walk("C:\\"):
        if program in files:
            fqfn = os.path.join(root, program)
            if is_exe(fqfn):
                return fqfn
    return None


class SalabsUtils(DynamicRobotApiClass):
    """Random utils to help out in all sorts of testing or implementing test libraries with Robot Framework"""
    def __init__(self):
        pass

    @keyword("Add Basic Authentication To Url")
    def add_authentication(self, url, l, p):
        data = furl(url)
        data.username = l
        data.password = p
        return data.tostr()

    @keyword
    def split_url_to_host_and_path(self, url):
        data = furl(url)
        return {'base': str(data.copy().remove(path=True)), 'path': str(data.path)}

    @keyword
    def cookies_to_dict(self, cookies):
        """
        Converts a cookie string into python dict.
        """
        ret = {}
        cookie = SimpleCookie()
        cookie.load(cookies)
        for key, morsel in cookie.keys():
            ret[key] = morsel.value
        return ret

    @keyword
    def locate_executable(self, binary):
        fpath, fname = os.path.split(binary)
        if fpath and is_exe(binary):
            return binary

        return from_path(binary) or from_root(binary)

    @property
    def log_directory(self):
        try:
            logfile = BuiltIn().get_variable_value("${LOG FILE}")
            if logfile is None:
                return BuiltIn().get_variable_value("${OUTPUTDIR}")
            return os.path.dirname(logfile)
        except RobotNotRunningError:
            return os.getcwdu() if PY2 else os.getcwd()  # pylint: disable=no-member
