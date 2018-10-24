from mysql_conn import MySQLConn


class ReadProjectInfo:
    def __init__(self, project_name):
        self.con = MySQLConn()
        self.project_name = project_name

    def get_project_info(self):
        sql_str = """select a.content_path, a.svn_addr, `owner`, port_no, module_type from py_maintain_module_list_info a 
left join py_maintain_project_mabiao b 
on a.project_id =b.project_id 
where b.project_eng_name = 'pymom' """

        self.con.cursor.execute(sql_str)

        data = self.con.cursor.fetchall()

        return data


if __name__ == '__main__':
    info = ReadProjectInfo('pymom')
    info.get_project_info()
