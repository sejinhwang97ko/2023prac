import pymysql
import pandas as pd

class Database:
    # 생성자 함수
    def __init__(self, _host, _user, _pass, _db, _port):
        self.db = pymysql.connect(
            user = _user,
            password = _pass,
            host = _host, 
            db = _db, #데이터베이스명
            port = _port
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def func_3(self,sql,values=[]):
    # if (sql.find('select') != -1) and (sql.find('select') < 10):
        if (sql.replace('\n', '').strip().startswith('select')):
            self.cursor.execute(sql,values)
            result = self.cursor.fetchall()
            result = pd.DataFrame(result)
        else:
            self.cursor.execute(sql,values)
            self._db.commit()
            result = "Query OK"
        return result