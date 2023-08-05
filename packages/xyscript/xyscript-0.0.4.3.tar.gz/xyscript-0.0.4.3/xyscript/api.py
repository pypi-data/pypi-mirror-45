"""
API for the command-line I{xyscript} tool.
"""
from __future__ import with_statement
import getopt, sys
# from CommonScript import IOSProjectTool, GitLabTool
from xyscript.CommonScript import IOSProjectTool, GitLabTool


__all__ = ['pullsubmodule', 'initproject', 'packagetotest', 'pullcerts','main']

def pullsubmodule(*parameters):
    print("start change branch...")
    GitLabTool().change_branch_g("Develop")
    print("\033[1;32m pullsubmodule success \033[0m")

    print("start pull submodules...")
    GitLabTool().pull_submodule()
    print("\033[1;32m pull submodules success \033[0m")

    print("satrt pod install...")
    IOSProjectTool().run_pod_install()
    print("\033[1;32m pod install success \033[0m")

def initproject():
    print("从零开始初始化项目")

def packagetotest(project_name,branch_name,platform):
    print("打测试包")
    print("项目名称：",project_name," 分支为：",branch_name," 发布平台为：",platform)

def pullcerts():
    print("拉取最新证书")

def _check_fastlane():
    print("检查是否安装fastlane，如果没有则立即安装fastlane和pgyer插件")

def _check_cocoapods():
    print("检查是否安装cocoapods，如果没有则立即安装cocoapods")

def _print_helpdoc():
    print("system doc:")
    print("     [-h] or [--help]  helpdocument for xyscript")
    print("instructions for use:")
    print("     'xyscript [apiname] [parameters(optional)]' ")
    print("xyscript api:")
    print("     pullsubmodule       --pull moudle form submoudle"  )

def run_method(args=None):
    try:
        parameters = args[1:]
        eval(args[0])(parameters)
    except BaseException as error:
        print(error)
        _print_helpdoc()
    else:
        pass
        # print("调用方法：", args[0], "成功")

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def main(prog=None,args=None):
    # print(sys.argv)
    args = sys.argv
    shortargs = 'h' #短选项模式
    longargs = ['help'] #长选项模式
    try:
        try:
            opts, args = getopt.getopt(args, shortargs, longargs)
        except getopt.GetoptError as error:
            #调用具体方法,手动异常
            raise Usage(error.msg)
        else:
            # print('args:',args)
            # print('opts:',opts)
            #规定的参数
            for name in args:
                # print(name)
                if name in ("-h", "--help"):
                    _print_helpdoc()
                    sys.exit()
            #没有规定的参数
            run_method(args[1:])
            # for item in args:
            #     处理规定的参数
            #     print(item)
    except Usage:
        run_method(args[1:])
    

if __name__ == "__main__":
    main()
    # GitLabTool().change_branch_g("develop")
   