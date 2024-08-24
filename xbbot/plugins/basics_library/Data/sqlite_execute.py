import sqlite3
from confing.confing_data import *
from xbbot.plugins.basics_library.Data.data_class_port import *


class SqlIte(metaclass=MyData):
    data_name = 'sqlite'

    def __init__(self):
        self.json = Gai(GaiJson()).execute()

    def execute(self, expression: str, *data):
        print(expression % data)
        conn = sqlite3.connect(f'./xbbot/data/{self.json.数据库名称}.db')
        cursor = conn.cursor()
        cursor.execute(expression % data)
        return_data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return return_data
