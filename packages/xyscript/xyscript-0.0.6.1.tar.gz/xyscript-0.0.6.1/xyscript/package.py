#-*- encoding:utf-8 -*-

class Package:
    def auto_package(self, project_address, branch_name, platform):
        print("自动打包")
        print("项目：",project_address," 分支为：",branch_name," 发布平台为：",platform)