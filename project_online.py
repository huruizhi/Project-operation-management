#!/usr/bin/env python
# -*- coding:utf-8 -*-
#时间：2018-10-27
#作者：Presley
#k8s上线脚本
import subprocess
from datetime import datetime
from config_file_auto.config.settings import *
from config_file_auto.config.ssh_tools import *

#开始上线
def on_line(project_name,online_module_group):
    online_host = "192.168.30.42"
    online_port = "22"
    online_user = "root"
    online_passwd = "123456"

    local_docker_host = "192.168.30.42"
    local_docker_port = "22"
    local_docker_user = "root"
    local_docker_passwd = "123456"
    # 上线到阿里云的时间tag
    up_to_ali_tag = datetime.now().strftime('%Y-%m-%d.%H-%M-%S')

    print("上线模块为{online_module_group}".format(online_module_group=online_module_group))

    #上线准备：开始打本地docker 镜像tag
    ssh_local = SshClient(local_docker_host, local_docker_port, local_docker_user, local_docker_passwd)
    for on_line_module in online_module_group:
        print("\n\n\033[1;32;47m--------------------模块{0}开始上线准备--------------------\n\033[0m".format(on_line_module))
        #打阿里云版本tag
        cmd_shell_relase_tag = "/usr/bin/docker tag harbor.pycf.com/{project_name}/{module_name}:pro registry.cn-qingdao.aliyuncs.com/pystandard/{project_name}-{module_name}:latest && echo \"\t打tag成功\n\"".format(project_name = project_name,module_name = on_line_module)
        #sout, serr = runCmd(cmd_shell)
        #打备份版本tag
        cmd_shell_back_tag = "/usr/bin/docker tag harbor.pycf.com/{project_name}/{module_name}:pro registry.cn-qingdao.aliyuncs.com/pystandard/{project_name}-{module_name}:{data_now} && echo \"\t打tag成功\n\"".format(project_name=project_name, module_name=on_line_module,data_now = up_to_ali_tag)
        #将上线镜像上传到阿里云
        cmd_shell_up_aliyun_tag = "/usr/bin/docker push registry.cn-qingdao.aliyuncs.com/pystandard/{project_name}-{module_name}:latest && echo \"\n\t上传成功\n\"".format(project_name = project_name,module_name = on_line_module)
        #将备份镜像上传到阿里云
        cmd_shell_up_aliyun_backtag = "/usr/bin/docker push registry.cn-qingdao.aliyuncs.com/pystandard/{project_name}-{module_name}:{data_now} && echo \"\n\t上传成功\n\"".format(project_name=project_name, module_name=on_line_module,data_now = up_to_ali_tag)
        print("\033[1;36;47m打阿里云版本tag\n\033[0m")
        stdout, stderr = ssh_local.exec_cmd(cmd_shell_relase_tag)
        print(stdout.read().decode("utf-8"))
        print(stderr.read().decode("utf-8"))

        print("\033[1;36;47m打备份版本tag\n\033[0m")
        stdout, stderr = ssh_local.exec_cmd(cmd_shell_back_tag)
        print(stdout.read().decode("utf-8"))
        print(stderr.read().decode("utf-8"))

        print("\033[1;36;47m将上线镜像上传到阿里云\n\033[0m")
        stdout, stderr = ssh_local.exec_cmd(cmd_shell_up_aliyun_tag)
        print(stdout.read().decode("utf-8"))
        print(stderr.read().decode("utf-8"))

        print("\033[1;36;47m将备份镜像上传到阿里云\n\033[0m")
        stdout, stderr = ssh_local.exec_cmd(cmd_shell_up_aliyun_backtag)
        print(stdout.read().decode("utf-8"))
        print(stderr.read().decode("utf-8"))

    ssh_local.close_connect()

    #开始上线
    ssh_aliyun = SshClient(online_host, online_port, online_user, online_passwd)
    for online_module in online_module_group:
        print("--------------------模块{module_name}开始上线--------------------".format(module_name = online_module))
        print("开始停止模块{module_name}服务".format(module_name = online_module))
        stdout,stderr = ssh_aliyun.exec_cmd("/usr/local/bin/docker-compose -f /application/docker_hub/java/{project_name}/docker-compose-pro.yml stop {project_name}_{module_name}_pro".format(project_name = project_name,module_name = online_module))
        print(stdout.read().decode("utf-8"))
        print(stderr.read().decode("utf-8"))

        print("开始删除模块{module_name}服务".format(module_name = online_module))
        stdout, stderr = ssh_aliyun.exec_cmd("/usr/local/bin/docker-compose -f /application/docker_hub/java/{project_name}/docker-compose-pro.yml rm -f {project_name}_{module_name}_pro".format(project_name = project_name,module_name = online_module))
        print(stdout.read().decode("utf-8"))
        print(stderr.read().decode("utf-8"))

        print("开始构建模块{module_name}服务".format(module_name = online_module))
        stdout, stderr = ssh_aliyun.exec_cmd("/usr/local/bin/docker-compose -f /application/docker_hub/java/{project_name}/docker-compose-pro.yml up -d {project_name}_{module_name}_pro".format(project_name = project_name,module_name = online_module))
        print(stdout.read().decode("utf-8"))
        print(stderr.read().decode("utf-8"))
    print("上线完成，请检查上线结果")
    ssh_aliyun.close_connect()

def run():
    # 选择项目
    project_id = input("请输入需要上线的项目id: ")
    project_info = get_settings_info(project_id)
    project_name = project_info['project_name']
    stages = project_info['stages']
    modules = project_info['modules']

    module_list = []
    module_list.append(project_info["register"][0])
    for module in modules:
        module[0] = module[0].lower()
        module_list.append(module[0])
    print("项目名称为:{project_name}\n"
          "模块信息为:".format(project_name=project_info["project_name"]))

    # 将项目中的模块以id的形式添加到字典中方便根据模块id获取模块名字
    i = 1
    module_dict = {}
    for module in module_list:
        i = str(i)
        print("{module_id}:{module_name}".format(module_id=i, module_name=module))
        module_dict[i] = module
        i = int(i)
        i += 1


    select_module_id_group = input("请输入需要上线模块id(若有多个模块上线请以逗号隔开输入，如 1，2，3，若所有模块需要上线请输入all)\n:")

    # 将选择的模块添加到列表中
    online_module_group = []
    if select_module_id_group == "all":
        for k, v in module_dict.items():
            online_module_group.append(v)
    else:
        select_module_id_group = select_module_id_group.split(",")
        for module_id in select_module_id_group:
            online_module_group.append(module_dict[module_id])
    on_line(project_name, online_module_group)

if __name__ == "__main__":
    run()

