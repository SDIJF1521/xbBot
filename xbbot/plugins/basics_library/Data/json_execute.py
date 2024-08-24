import json
from confing.confing_data import *
from xbbot.plugins.basics_library.Data.data_class_port import *


class Json(metaclass=MyData):
    data_name = 'json'

    def __init__(self):
        self.json = Gai(GaiJson()).execute()

    def read(self):
        with open(f'./xbbot/data/{self.json.文件名称}.json', 'r', encoding='utf-8') as f:
            print('yes')
            json_data = json.load(f)
            print(dict(json_data))
            return dict(json_data)

    def deposit(self, data: dict):
        with open(f'./xbbot/data/{self.json.文件名称}.json', 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

