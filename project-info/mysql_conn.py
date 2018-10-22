import pymysql


class MySQLConn:
    def __init__(self):
        self.cursor, self._con = self._con()

    def _con(self):
        db = pymysql.connect("192.168.0.151", "pycf", "1qaz@WSXabc", "py_maintain")
        cursor = db.cursor()
        return cursor, db

    def _close(self):
        self._con.close()
