import os
import json
import pymysql
import sqlite3
import importlib.util
from confing import confing_data
from abc import ABC, abstractmethod
from confing.creation_config import *


def import_classes_from_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)
                import_classes_from_file(file_path)


def import_classes_from_file(file_path):
    # 提取模块名称
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # 动态加载模块
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 将模块中的所有类导入到当前全局命名空间中
    for name, cls in module.__dict__.items():
        if isinstance(cls, type):
            globals()[name] = cls


# 指定 plug 文件夹路径
folder_path = "./confing/plug"  # 假设 plug 文件夹与 main.py 在同一目录

# 导入 plug 文件夹中的所有类
import_classes_from_folder(folder_path)


# 定义生成数据类策略接口
class DataCreation(ABC):
    def __init__(self):
        self.config = confing_data.Gai(confing_data.GaiJson()).execute()

    @abstractmethod
    def creation(self):
        pass


# sqlite生成策略
class SqliteCreation(DataCreation):

    def creation(self):
        sql = 'CREATE TABLE {} ({})'
        conn = sqlite3.connect(f'./xbbot/data/{self.config.数据库名称}.db')
        cursor = conn.cursor()
        try:
            for table_name, table_info in self.config.表单.items():
                columns = ', '.join(
                    f"{field} {dtype}"
                    for field, dtype in zip(table_info['字段'], table_info['类型'])
                )
                cursor.execute(sql.format(table_info['表单名称'], columns))
            conn.commit()
        finally:
            cursor.close()
            conn.close()


# mysql生成策略
class MysqlCreation(DataCreation):

    def creation(self):
        conn = pymysql.connect(
            host=self.config.数据库主机,
            user=self.config.数据库账号,
            password=self.config.数据库密码
        )
        cursor = conn.cursor()
        try:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.config.数据库名称}')
            conn.commit()
        finally:
            cursor.close()
            conn.close()

        conn = pymysql.connect(
            host=self.config.数据库主机,
            user=self.config.数据库账号,
            password=self.config.数据库密码,
            database=self.config.数据库名称
        )
        cursor = conn.cursor()
        sql = 'CREATE TABLE {} ({})'
        try:
            for table_name, table_info in self.config.表单.items():
                columns = ', '.join(
                    f"{field} {dtype}"
                    for field, dtype in zip(table_info['字段'], table_info['类型'])
                )
                cursor.execute(sql.format(table_info['表单名称'], columns))
            conn.commit()
        finally:
            cursor.close()
            conn.close()


# json生成策略
class JsonCreation(DataCreation):

    def creation(self):
        data = {}
        for table_name, table_info in self.config.表单.items():
            content = {field: [] for field in table_info['字段']}
            data[table_info['表单名称']] = content

        with open(f'./xbbot/data/{self.config.文件名称}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


# 上下文类
class ExecuteCreation:
    def __init__(self, plan: DataCreation | CreateConfigParent):
        self.plan = plan

    def execute(self):
        self.plan.creation()
