from config_file_auto.config.settings import *
import os

#创建生成docker-compose目录
def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def run(project_id):
    project_info = get_settings_info(project_id)
    project_name = project_info['project_name']
    stages = project_info['stages']
    modules = project_info['modules']
    harbor_url = "registry.cn-qingdao.aliyuncs.com/pystandard"
    register_info = project_info['register']
    docker_compose_info_pro_str_flag = '''version: '3'
services:
'''
    docker_compose_info_dev_str_flag = '''version: '3'
services:
'''

    create_dir("{project_name}/docker_compose_config/".format(project_name = project_name))
    for stage in stages:
        if stage == "dev":
            docker_compose_info_dev_str_flag = docker_compose_info_dev_str_flag + '''  {project_name}_{module_name}_{stage}:
    image: {harbor_url}/{project_name}-{module_name}:latest
    container_name: {project_name}_{module_name}_{stage}
    hostname: {project_name}_{module_name}_{stage}
    restart: always
    ports:
      - {port}:5000
    volumes:
      - /etc/localtime:/etc/localtime
    environment:
      - TZ=Asia/Shanghai
    healthcheck:
      test: ["CMD-SHELL", "ss -tnlp|grep -w 5000|grep -v grep"]
      interval: 5s
      timeout: 2s
      retries: 3
    entrypoint:
      - java
      - -Xms128m
      - -Xmx256m
      - -jar
      - /java8/app.jar
      - --server.port=5000
      - --spring.profiles.active=pro
    networks:
      - {stage}

'''.format(project_name=project_name, module_name=register_info[0], stage=stage, harbor_url=harbor_url,port=register_info[2])
            for module in modules:
                if module[4] == "java":
                    docker_compose_java_info_str = '''  {project_name}_{module_name}_{stage}:
    image: {harbor_url}/{project_name}-{module_name}:latest
    container_name: {project_name}_{module_name}_{stage}
    hostname: {project_name}_{module_name}_{stage}
    restart: always
    ports:
      - {port}:5000
    volumes:
      - /etc/localtime:/etc/localtime
    environment:
      - TZ=Asia/Shanghai
    healthcheck:
      test: ["CMD-SHELL", "ss -tnlp|grep -w 5000|grep -v grep"]
      interval: 5s
      timeout: 2s
      retries: 3
    entrypoint:
      - java
      - -Xms128m
      - -Xmx256m
      - -jar
      - /java8/app.jar
      - --server.port=5000
      - --spring.profiles.active={stage}
    networks:
      - {stage}

'''.format(project_name = project_name,module_name = module[0],stage = stage,harbor_url = harbor_url,port = module[2])
                    docker_compose_info_dev_str_flag = docker_compose_info_dev_str_flag + docker_compose_java_info_str
                if module[4] == "python":
                    module_python_info_str = '''  {project_name}_{module_name}_{stage}:
    image: {harbor_url}/{project_name}-{module_name}:latest
    container_name: {project_name}_{module_name}_{stage}
    hostname: {project_name}_{module_name}_{stage}
    restart: always
    ports:
      - {port}:5000
    volumes:
      - /etc/localtime:/etc/localtime
    environment:
      - TZ=Asia/Shanghai
    healthcheck:
      test: ["CMD-SHELL", "netstat -tnlp|grep -w 5000|grep -v grep"]
      interval: 5s
      timeout: 2s
      retries: 3
    entrypoint:
      - python
      - -u
      - /python3/manage.py
      - runserver
      - 0.0.0.0:5000
    networks:
      - {stage}

'''.format(project_name = project_name,module_name = module[0],stage = stage,harbor_url = harbor_url,port = module[2])
                    docker_compose_info_dev_str_flag = docker_compose_info_dev_str_flag + module_python_info_str
            docker_compose_info_dev_str_flag = docker_compose_info_dev_str_flag + '''networks:
  {stage}:
    external: false
'''.format(stage = stage)
            with open("{project_name}/docker_compose_config/docker-compose-{stage}.yml".format(project_name=project_name,stage=stage), "w") as f:
                f.write(docker_compose_info_dev_str_flag)
        if stage == "pro":
            docker_compose_info_pro_str_flag = docker_compose_info_pro_str_flag + '''  {project_name}_{module_name}_{stage}:
    image: {harbor_url}/{project_name}-{module_name}:latest
    container_name: {project_name}_{module_name}_{stage}
    hostname: {project_name}_{module_name}_{stage}
    restart: always
    ports:
      - {port}:5000
    volumes:
      - /etc/localtime:/etc/localtime
    environment:
      - TZ=Asia/Shanghai
    healthcheck:
      test: ["CMD-SHELL", "ss -tnlp|grep -w 5000|grep -v grep"]
      interval: 5s
      timeout: 2s
      retries: 3
    entrypoint:
      - java
      - -Xms128m
      - -Xmx256m
      - -jar
      - /java8/app.jar
      - --server.port=5000
      - --spring.profiles.active={stage}
    networks:
      - {stage}

'''.format(project_name=project_name, module_name=register_info[0], stage=stage, harbor_url=harbor_url,port=register_info[1])
            for module in modules:
                if module[4] == "java":
                    docker_compose_java_info_str = '''  {project_name}_{module_name}_{stage}:
    image: {harbor_url}/{project_name}-{module_name}:latest
    container_name: {project_name}_{module_name}_{stage}
    hostname: {project_name}_{module_name}_{stage}
    restart: always
    ports:
      - {port}:5000
    volumes:
      - /etc/localtime:/etc/localtime
    environment:
      - TZ=Asia/Shanghai
    healthcheck:
      test: ["CMD-SHELL", "ss -tnlp|grep -w 5000|grep -v grep"]
      interval: 5s
      timeout: 2s
      retries: 3
    entrypoint:
      - java
      - -Xms128m
      - -Xmx256m
      - -jar
      - /java8/app.jar
      - --server.port=5000
      - --spring.profiles.active=pro
    networks:
      - {stage}

'''.format(project_name=project_name, module_name=module[0], stage=stage, harbor_url=harbor_url, port=module[1])
                    docker_compose_info_pro_str_flag = docker_compose_info_pro_str_flag + docker_compose_java_info_str
                if module[4] == "python":
                    module_python_info_str = '''  {project_name}_{module_name}_{stage}:
    image: {harbor_url}/{project_name}-{module_name}:latest
    container_name: {project_name}_{module_name}_{stage}
    hostname: {project_name}_{module_name}_{stage}
    restart: always
    ports:
      - {port}:5000
    volumes:
      - /etc/localtime:/etc/localtime
    environment:
      - TZ=Asia/Shanghai
    healthcheck:
      test: ["CMD-SHELL", "netstat -tnlp|grep -w 5000|grep -v grep"]
      interval: 5s
      timeout: 2s
      retries: 3
    entrypoint:
      - python
      - -u
      - /python3/manage.py
      - runserver
      - 0.0.0.0:5000
    networks:
      - {stage}

'''.format(project_name=project_name, module_name=module[0], stage=stage, harbor_url=harbor_url,port=module[1])
                    docker_compose_info_pro_str_flag = docker_compose_info_pro_str_flag + module_python_info_str
            docker_compose_info_pro_str_flag = docker_compose_info_pro_str_flag +  '''networks:
  {stage}:
    external: false
'''.format(stage = stage)
            with open("{project_name}/docker_compose_config/docker-compose-{stage}.yml".format(project_name=project_name,stage=stage), "w") as f:
                f.write(docker_compose_info_pro_str_flag)

if __name__ == "__main__":
    run(11)







# with open("k8stest-pymom/docker_compose_config/docker-compose-pro.yaml",'w') as f:
#     f.write(s)

