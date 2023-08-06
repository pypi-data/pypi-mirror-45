"""
API for the command-line I{xyscript} tool.
"""
from __future__ import with_statement
import getopt, sys, os

from xyscript.CommonScript import IOSProjectTool, GitLabTool
from xyscript.cert import Cert
from xyscript.package import Package
from xyscript.xylog import *

PROJECT_ADDRESS = None
PROJECT_BRANCH = None
TEST_PLATFORM = None

__all__ = ['pullsubmodule', 'initproject', 'package', "pps", 'syn','main']

def pullsubmodule(*parameters):
    """
    切换分支+拉取子模块代码+pod install
    """

    Package().change_branch("Develop")

    Package().pull_submodule()

    IOSProjectTool().run_pod_install()

def initproject():
    print("从零开始初始化项目")

def package(*parameters):
    global PROJECT_ADDRESS, PROJECT_BRANCH, TEST_PLATFORM
    Package().auto_package(PROJECT_ADDRESS, PROJECT_BRANCH, TEST_PLATFORM)

def pps(*parameters):
    Cert().run_cert_pps()

def syn(*parameters):
    Cert().run_cert_syn()

def _check_fastlane():
    print("检查是否安装fastlane，如果没有则立即安装fastlane和pgyer插件")

def _check_cocoapods():
    print("检查是否安装cocoapods，如果没有则立即安装cocoapods")

def _get_version():
    with open(os.path.dirname(os.path.realpath(__file__))+ "/config.py") as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

def _print_helpdoc():
    print("system doc:")
    print("     [-h] or [--help]  helpdocument for xyscript")
    print("     [-v] or [--version]  version of xyscript")
    print("instructions for use:")
    print("     'xyscript [apiname] [parameters(optional)]' ")
    print("xyscript actions:")
    print("     pullsubmodule       --pull moudle form submoudle"  )
    print("     syn                 --pull latest certs"  )
    # print("     package ")

def run_method(args=None):
    try:
        parameters = args[1:]
        eval(args[0])(parameters)
    except BaseException as error:
        faillog(error)
        _print_helpdoc()
    else:
        pass
        # print("调用方法：", args[0], "成功")
def sys_action(args):
    for parms in args:
        if parms in ("-h", "--help"):
            _print_helpdoc()
            sys.exit()
        elif parms in ("-v", "--version"):
            print(_get_version())
            sys.exit() 

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def main(prog=None,args=None):
    global PROJECT_ADDRESS, PROJECT_BRANCH, TEST_PLATFORM
    #处理系统方法
    sys_action(sys.argv)  

    args = sys.argv[2:]
    shortargs = 'a:p:b:' #短选项模式
    longargs = ['address=', 'platform=', 'branch='], #长选项模式
    try:
        try:
            opts, args = getopt.getopt(args, shortargs, longargs)
        except getopt.GetoptError as error:
            # #调用具体方法,手动异常
            raise Usage(error.msg)
        else:
            # print('args:',args)
            # print('opts:',opts)
            for opt, arg in opts:
                if opt in ("-a", "--address"):
                    PROJECT_ADDRESS = arg
                elif opt in ("-b", "--branch"):
                    PROJECT_BRANCH = arg
                elif opt in ("-p", "--platform"):
                    TEST_PLATFORM = arg
            run_method(sys.argv[1:])
    except Usage:
        # print("参数解析异常")
        _print_helpdoc()
        # run_method(args[1:])
    

if __name__ == "__main__":
    main()
    # GitLabTool().change_branch_g("develop")
    # Cert().run_cert_syn()
    # _get_version()
    # package()