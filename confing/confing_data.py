import os
import json
import yaml
import pandas as pd
from abc import ABC, abstractmethod


# 定义策略接口
class GainData(ABC):
    @abstractmethod
    def gain(self):
        pass


# 读取XB_config.yml配置文件
class GaiYml(GainData):
    def gain(self):
        with open(f'{os.path.abspath(os.curdir)}\\XB_config.yml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return pd.Series(data)


# 读取data_config.json配置文件
class GaiJson(GainData):
    def gain(self):
        with open('./data_config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return pd.Series(data)


class Gai:
    def __init__(self, kind: GainData):
        self.kind = kind

    def execute(self):
        return self.kind.gain()
