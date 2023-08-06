#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import print_function

import json
import os
import sys
import stat
import time
import threading
from pathlib import Path

from git import Repo
import tkinter as tk
from tkinter import filedialog

from xyscript.xylog import *
from xyscript.cert import Cert
from xyscript.CommonScript import IOSProjectTool

SELECT_FILE_COUNT = 0
WORK_SPACE = None


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()
class Package:
    
    def clone_form_address(self,address,local_path):
        folder_name = (address.split("/")[-1]).split(".")[0]
        try:
            #创建目录
            local_path = local_path + "/" + folder_name
            if Path(local_path).exists():
                warninglog(folder_name + "is exists")
            else:
                os.mkdir(local_path)
            # 更改权限
            os.chmod(local_path, stat.S_IRWXU)
            local_path = local_path + "/"
            Repo.clone_from(url=address, to_path=local_path, progress=None)
            successlog("clone project success")
        except BaseException as error:
            faillog(format(error))

    def change_branch(self, branch_name, git=None):
        """
        change_branch
        """
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
                        errstr = "have no branch named:" + branch_name + " exist,cannot to checkout"
                        # errstr = "\033[1;31m" + "远端不存在名为："+ branch_name + "的分支，无法checkout,请先创建远端仓库分支再checkout" + "\033[0m"
                        faillog(errstr)
                        sys.exit()

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
            sys.exit()
    
    def _hava_install_pgy_plugin(self):
        pass
    
    def package(self):
        pass

    def select_directory(self):
        global SELECT_FILE_COUNT
        root = tk.Tk()
        root.withdraw()
        root.update()
        file_path = filedialog.askdirectory(initialdir=os.getcwd(), title="选择项目存储的路径")

        SELECT_FILE_COUNT = SELECT_FILE_COUNT + 1
        if SELECT_FILE_COUNT >=3:
            faillog("you have give up choosing an folder three times!")
            sys.exit()
        if file_path == "":
            warninglog("please choose an folder")
            self.select_directory()
        else:
            root.update()
            # root.mainloop()
            return file_path
    

    def auto_package(self, project_address=None, branch_name=None, platform=None):

        print("自动打包 项目：",project_address," 分支为：",branch_name," 发布平台为：",platform)
        print("please choose an folder")
        
        # #clone
        self.clone_form_address(project_address,self.select_directory())
        # #切换分支
        self.change_branch(branch_name)
        # #拉子模块
        self.pull_submodule()
        # #pod indtall
        IOSProjectTool().run_pod_install()
        # #fastlane syn
        Cert().run_cert_syn()
        # #打包（pgyer插件）

