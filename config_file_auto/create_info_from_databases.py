from project_info.mysql_conn import *

def get_info(project_id):
    setting_info = {
        'harbor_url': 'harbor.pycf.com',
        'project_name': None,
        'stages': ['pro', 'dev'],
        'register': ['register', None, None, None, 'java'],
        'modules': []
    }
    get_module_info_sql = '''select * from py_maintain_module_list_info where project_id = {project_id};'''.format(project_id = project_id)
    get_project_name_sql = '''select * from py_maintain_project_mabiao where project_id = {project_id};'''.format(project_id = project_id)
    cursor = MySQLConn()
    cursor = cursor.cursor

    #获取项目名称并添加到字典
    cursor.execute(get_project_name_sql)
    results = cursor.fetchall()
    project_name = results[0][2]
    setting_info["project_name"] = project_name

    #获取模块信息并添加到字典
    cursor.execute(get_module_info_sql)
    results_modules = cursor.fetchall()
    for row in results_modules:
        port_pro = str(row[6]).split("/")[1]
        port_dev = str(row[6]).split("/")[0]
        svn_url = row[4]
        module_name = str(row[9]).split("/")[1]
        section_name = str(row[9]).split("/")[0]
        if  str(row[9]).split("/")[1] == "register":
            setting_info['register'] = ["register",
                                        "{port_pro}".format(port_pro = port_pro),"{port_dev}",
                                        "{svn_url}".format(svn_url = svn_url),
                                        "java"]
        else:
            module_info = [module_name,port_pro,port_dev,svn_url,section_name]
            setting_info["modules"].append(module_info)
    cursor.close()
    return setting_info
