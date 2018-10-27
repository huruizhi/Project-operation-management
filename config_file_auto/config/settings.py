# from project_info.mysql_conn import *
# def get_settings_info(project_id):
#     setting_info = {
#         'harbor_url': 'harbor.pycf.com',
#         'project_name': None,
#         'stages': ['pro', 'dev'],
#         'register': ['register', None, None, None, 'java'],
#         'modules': []
#     }
#     get_module_info_sql = '''select * from py_maintain_module_list_info where project_id = {project_id};'''.format(project_id = project_id)
#     get_project_name_sql = '''select * from py_maintain_project_mabiao where project_id = {project_id};'''.format(project_id = project_id)
#     cursor = MySQLConn()
#     cursor = cursor.cursor
#
#     #获取项目名称并添加到字典
#     cursor.execute(get_project_name_sql)
#     results = cursor.fetchall()
#     project_name = results[0][2]
#     setting_info["project_name"] = project_name
#
#     #获取模块信息并添加到字典
#     cursor.execute(get_module_info_sql)
#     results_modules = cursor.fetchall()
#     for row in results_modules:
#         port_pro = str(row[6]).split("/")[1]
#         port_dev = str(row[6]).split("/")[0]
#         svn_url = row[4]
#         module_name = str(row[9]).split("/")[1]
#         section_name = str(row[9]).split("/")[0]
#         if  str(row[9]).split("/")[1] == "register":
#             setting_info['register'] = ["register",
#                                         "{port_pro}".format(port_pro = port_pro),
#                                         "{port_dev}".format(port_dev = port_dev),
#                                         "{svn_url}".format(svn_url = svn_url),
#                                         "java"]
#         else:
#             module_info = [module_name,port_pro,port_dev,svn_url,section_name]
#             setting_info["modules"].append(module_info)
#     cursor.close()
#     return setting_info

project_info = {
    'harbor_url': 'harbor.pycf.com',
    'project_name': 'k8stest-pymom',
    'stages': ['pro', 'dev'],
    'register': ['register', 6553, 6503, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-register', 'java'],
    'modules': [['home', 6550, 6500, 'svn://192.168.0.151/pycf/Projects/MOMsystem/pyMomSystem-home-1.0', 'java'],
                ['managerData', 6551, 6501, 'svn://192.168.0.151/pycf/Projects/MOMsystem/pyMomSystem-managerData-1.0', 'java'],
                ['managerSelect', 6552, 6502, 'svn://192.168.0.151/pycf/Projects/MOMsystem/pyMomSystem-managerSelect-1.0', 'java'],
                ['outsourceZuulClient', 6554, 6504, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-zuulClient', 'java'],
                ['manager', 6555, 6505, 'svn://192.168.0.151/pycf/Projects/MOMsystem/pyMomSystem-manager-1.0', 'java'],
                ['outsourceHome', 6556,  6506, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-home', 'java'],
                ['outsourcePosition', 6557, 6507, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-position', 'java'],
                ['outsourceAnalysis', 6558, 6508, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-analysis', 'java'],
                ['outsourceBenchmark', 6559, 6509, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-benchmark', 'java'],
                ['outsourceGroup', 6560, 6510, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-group', 'java'],
                ['outsourceCalculate', 6561, 6511, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-calculate', 'java'],
                ['outsourceBackstageSystem', 6562, 6512, 'svn://192.168.0.151/pycf/Projects/MOMsystem/outsource-tycqls1.0-backstage-system', 'java'],
                ['outsourceManagementSystem', 6563, 6513, 'svn://192.168.0.151/pycf/Projects/MOMsystem/OutsourcingManagementSystem', 'python']]
}

