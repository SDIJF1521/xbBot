import pymysql
from confing.confing_data import *
from xbbot.plugins.basics_library.Data.data_class_port import *


class Mysql(metaclass=MyData):
    data_name = 'mysql'

    def __init__(self):
        self.json = Gai(GaiJson()).execute()

    def execute(self, expression: str, *data):
        conn = pymysql.connect(host=self.json.数据库主机,
                               user=self.json.数据库账号,
                               password=self.json.数据库密码,
                               database=self.json.数据库名称
                               )
        cursor = conn.cursor()
        # print(expression)
        if data:
            cursor.execute(expression, data)
        else:
            cursor.execute(expression)
        return_data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return return_data
