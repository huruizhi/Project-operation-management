import pymysql


class MySQLConn:
    def __init__(self):
        self.cursor, self._conn = self._con()

    def _con(self):
        db = pymysql.connect("192.168.0.151", "pycf", "1qaz@WSXabc", "py_maintain")
        cursor = db.cursor()
        return cursor, db

    def close(self):
        self._conn.close()
