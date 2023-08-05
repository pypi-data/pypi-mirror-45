#-*- encoding:utf-8 -*-
import json
import os
import sys
import stat

from git import Repo
from xyscript.xylog import *
from xyscript.cert import Cert
from xyscript.CommonScript import IOSProjectTool

class Package:
    
    def clone_form_address(self,address,local_path):
        print("clone project from: ", address)
        global project_repo
        try:
            # 更改权限
            os.chmod('./', stat.S_IRWXU)
            # 克隆仓库
            project_repo = Repo.clone_from(
                url=address, to_path=local_path, progress=None)
            successlog("clone project success")
        except IOError as error:
            faillog(format(error))
        else:
            print("克隆项目成功")
            return project_repo

    def change_branch(self, branch_name, git=None):
        if git is None:
            repo = Repo(os.getcwd())
            print("start change branch to:",branch_name)
            local_branch_names = []#本地库列表
            remote_branch_names = []#远端库列表
            current_branch = repo.active_branch.name
            # print("current_branch_name:", current_branch)
            for localitem in repo.heads :
                local_branch_names.append(localitem.name)
                # print(localitem.name)
            # print("local_branch_names:", local_branch_names)

            for remoteitem in repo.refs:
                remote_branch_names.append(remoteitem.name)
                # print(remoteitem)
            # print("remote_branch_names:", remote_branch_names)

            if branch_name == current_branch:
                pass
                # print("就是当前分支，不需要切换")
                warningstring = "current branch is already :" + branch_name
                warninglog(warningstring)
            else:
                if branch_name in local_branch_names:
                    # print("本地存在目标分支，切换即可")
                    try:
                        local_target_branch = None
                        if branch_name == "develop":
                            local_target_branch = repo.heads.develop
                        elif branch_name == "Develop" :
                            local_target_branch = repo.heads.Develop
                        elif branch_name == "master" :
                            local_target_branch = repo.heads.master

                        repo.head.reference = local_target_branch
                        successlog("change branch success")
                    except BaseException as error:
                        errstr = "change branch failed:" + str(error)
                        faillog(errstr)
                        sys.exit()
                    
                else:
                    remote_branch_name = 'origin/' + branch_name
                    if remote_branch_name in remote_branch_names:
                        # print("远端存在目标分支同名分支，checkout")
                        try:
                            git = repo.git
                            git.checkout('-b', branch_name, remote_branch_name)
                            # repo.remote().pull()
                            successlog("change branch success")
                        except BaseException as error:
                            errstr = "checkout failed:" + str(error)
                            faillog(errstr)
                    else:
                        errstr = "have no branch named:" + branch_name + "exist,cannot to checkout"
                        # errstr = "\033[1;31m" + "远端不存在名为："+ branch_name + "的分支，无法checkout,请先创建远端仓库分支再checkout" + "\033[0m"
                        print(errstr)

        else:
            print(branch_name)

    def pull_submodule(self):
        """
        pull submodules
        """
        try:
            currentPath = os.getcwd()
            repo = Repo(currentPath)
            initFlag = 0
            file = open("ProjConfig.json")
            moduleConfigList = json.load(file)
            for moduleConfig in moduleConfigList:
                module_path = currentPath + "/" + moduleConfig["module"]
                if not os.listdir(module_path):
                    initFlag = 1
            if initFlag == 1:
                print("submodule init...")
                repo.git.submodule('update', '--init')
                print("submodule init success")
            for moduleConfig in moduleConfigList:
                module_path = currentPath + "/" + moduleConfig["module"]
                sub_repo = Repo(module_path)
                sub_remote = sub_repo.remote()
                sub_repo.git.reset('--hard')
                sub_repo.git.checkout(moduleConfig["branch"])
                sub_remote.pull()
                print(module_path + " " + "\033[1;32m" +
                      moduleConfig["branch"] + "\033[0m" + " pull success")
        except BaseException as error:
            errorstr = "pull submodule failed:" + format(error)
            faillog(errorstr)
    
    def _hava_install_pgy_plugin(self):
        pass
    
    def package(self):
        pass


    def auto_package(self, project_address, branch_name, platform):
        print("自动打包 项目：",project_address," 分支为：",branch_name," 发布平台为：",platform)

        #clone
        self.clone_form_address(project_address,"")
        #切换分支
        self.change_branch(branch_name)
        #拉子模块
        self.pull_submodule()
        #pod indtall
        IOSProjectTool().run_pod_install()
        #fastlane syn
        Cert().run_cert_syn()
        #打包（pgyer插件）
