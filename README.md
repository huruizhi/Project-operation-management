# Project-operation-management

## 1.概述

自动化的完成项目信息管理，并根据项目信息生成jenkins流程，kubernets\docker-compose配置文件，项目上线脚本等的CI/CD流程的配置以及程序信息。
实现项目的镜像管理。提升项目的流程规范以及提升项目管理效率。
项目主要分为三个部分：
- 管理项目的模块信息，包括模块名称、开发人员、svn地址、模块端口信息等。
- 自动化生成jenkins的项目流程。
- 生成kubernets\docker-compose配置文件，并对配置文件进行分发。

## 2.公司项目环境
公司项目使用java、python与R语言。java使用springCloud框架。
jenkins大致流程如下：
- 使用jenkins拉取源代码。
- java程序需要进行代码构建，将jar包封装进`docker image` ，python程序不需要构建，将源代码封装进`docker image`。
- 将镜像推送到本地docker仓库`harbor`
- 创建、更新`kubernetes deployment`


## 3.数据库模式
数据库沿用 老版本的项目信息管理平台的数据库，其中包含非必要信息。
具体数据库表结构查看[py_maintain.sql]


## 4.名称约定
### 基础变量
```
项目名称: project_name
模块名称: module_name
版本: stage (dev/pro)
harbor地址: harbor_url
注册中心名称: register_module_name
注册中心端口: register_port, port=None
dev端口: dev_port
pro端口: pro_port
```
### 扩展变量
```
docker镜像名称(inner): {{harbor_url}}/{{project_name}}/{{module_name}}
```

### jenkins:
```
jenkins 视图名称: module

```
### kubernetes:
```
deployment名称: {{project_name}}-{{module_name}}-{{stage}}
deployment文件名称: {{deploy_name}}-deployment.yaml
name_space: {{project_name}}-{{stage}}
deploy文件路径: /application/k8s-projects/{{project_name}}/{{stage}}/{{module_name}}/{{deploy_file}}

```

### docker-compose:
```
workdir: /application/docker_hub/java/{{project_name}}
docker_compose_file: {{workdir}}/docker-compose-{{stage}}.yml
docker_compose_module_name: {{project_name}}_{{module_name}}_{{stage}}

```
