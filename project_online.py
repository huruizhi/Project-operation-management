#!/usr/bin/env python
# -*- coding:utf-8 -*-
#时间：2018-10-27
#作者：Presley
#k8s上线脚本
from config_file_auto.config.settings import *

project_id = input("请输入需要上线的项目id:")
#project_info = get_settings_info(project_id)
project_name = project_info['project_name']
stages = project_info['stages']
modules = project_info['modules']

module_list = []
module_list.append(project_info["register"][0])
for module in modules:
    module[0] = module[0].lower()
    module_list.append(module[0])


print("项目名称为:{project_name}"
      "模块信息为:".format(project_name = project_info["project_name"]))

i = 1
module_dict = {}
for module in module_list:
    print("{module_id}:{module_name}".format(module_id = i,module_name = module))
    module_dict[i] = module
    i += 1
print(module_dict)

select_module_id = int(input("请输入需要上线模块id:(若有多个模块上线请以逗号隔开输入，如1，2，3，若所有模块需要上线请)"))
print(module_dict[select_module_id])

