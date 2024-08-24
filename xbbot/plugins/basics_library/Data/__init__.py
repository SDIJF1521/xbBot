import importlib.util
import json
from confing.confing_data import *
from xbbot.plugins.basics_library.Data.data_class_port import *


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
folder_path = "./xbbot/plugins/basics_library/Data"  # 假设 plug 文件夹与 main.py 在同一目录

# 导入 plug 文件夹中的所有类
import_classes_from_folder(folder_path)


class DataProt(ABC):
    data_vessel_select = MyData.get_class()
    config_json = Gai(GaiJson()).execute()
    dic = {'varchar (255)': "%s",
           'int': "%d"}

    @abstractmethod
    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None):
        """

        :param form_name: 表单名称
        :param screening_condition: 筛选条件
        :param field: 字段
        :return:
        """
        pass

    @abstractmethod
    def data_deposit_execute(self, form_name: str, data: dict=None):
        """

        :param form_name: 表单名称
        :param data: 存入数据，字段名称为变量名
        :return:
        """
        pass


# mysql便捷类
class MysqlExecute(DataProt):
    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None):
        # print(field)
        condition = ''
        if screening_condition is not None:
            condition = f'where {screening_condition}'
        if field:
            template = f'SELECT %s FROM {form_name}' + condition
            # print(template)
            return self.data_vessel_select['mysql'].execute(template%field)
        else:
            return self.data_vessel_select['mysql'].execute(f'SELECT * FROM {form_name}')

    def data_deposit_execute(self, form_name: str, data: dict = None):
        """

        :param form_name: 表单名称
        :param data: 存入数据
        :return:
        """
        # 建立字段映射字段
        field_dic = dict(zip([self.config_json.表单[i]['表单名称'] for i in self.config_json.表单],
                             [self.config_json.表单[j]['字段'][0] for j in self.config_json.表单]))
        exist_list = [i[0] for i in
                      self.data_vessel_select['mysql'].execute(f'SELECT {field_dic[form_name]} FROM {form_name}')]
        var = [j for j in self.config_json.表单 if self.config_json.表单[j]["表单名称"] == form_name][0]
        # print(exist_list)
        # 初次存入方法
        if not data[self.config_json.表单[var]["字段"][0]] in exist_list:
            data_transmit = []  # 传递参数列表
            template_data1 = ''  # 表达式参数1
            template_data2 = ''  # 表达式参数
            template = f'insert into {form_name} (%s) values (%s)'  # 定义SQL表达式

            # 补全SQL表达式
            for j in tuple(self.config_json.表单[var]["字段"]):
                template_data1 += f'{j},'
            template_data1 = template_data1[:-1]
            for j in tuple("%s" if i == "int" else "%s" for i in tuple(self.config_json.表单[var]["类型"])):
                template_data2 += f'{j},'
            template_data2 = template_data2[:-1]
            # print(template)
            for i in self.config_json.表单[var]["字段"]:  # 整理传递参数
                data_transmit.append(data[i])
            self.data_vessel_select['mysql'].execute(template % (template_data1, template_data2), *data_transmit)
        # 二次存入方法
        else:
            template = f'update {form_name} set %s where user = "{data[self.config_json.表单[var]["字段"][0]]}"'
            # print(list(data.keys())[:1])
            for i in list(data.keys())[1:]:

                if self.config_json.表单[var]["类型"][self.config_json.表单[var]['字段'].index(i)] == 'int':
                    # print(2,data[i])
                    self.data_vessel_select['mysql'].execute(template % f'{i} = {i}+%s', data[i])
                else:
                    self.data_vessel_select['mysql'].execute(template % f'{i}=%s', data[i])


# sqlite便捷类
class SqlIteExecute(DataProt):
    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None):
        condition = ''
        if screening_condition is not None:
            condition = f'WHERE {screening_condition}'
        if field:
            template = f'SELECT {"%s"} FROM {form_name} ' + condition
            # print(template)
            return self.data_vessel_select['sqlite'].execute(template, field)
        else:
            return self.data_vessel_select['sqlite'].execute(f'SELECT * FROM {form_name}')

    def data_deposit_execute(self, form_name: str, data: dict = None):
        """

        :param form_name: 表单名称
        :param data: 存入数据
        :return:
        """
        # 建立字段映射字段
        field_dic = dict(zip([self.config_json.表单[i]['表单名称'] for i in self.config_json.表单],
                             [self.config_json.表单[j]['字段'][0] for j in self.config_json.表单]))
        exist_list = [i[0] for i in
                      self.data_vessel_select['sqlite'].execute(f'SELECT {field_dic[form_name]} FROM {form_name}')]
        var = [j for j in self.config_json.表单 if self.config_json.表单[j]["表单名称"] == form_name][0]
        # print(exist_list)
        # 初次存入方法
        if not data[self.config_json.表单[var]["字段"][0]] in exist_list:
            data_transmit = []  # 传递参数列表
            template_data1 = ''  # 表达式参数1
            template_data2 = ''  # 表达式参数
            template = f'insert into {form_name} (%s) values (%s)'  # 定义SQL表达式

            # 补全SQL表达式
            for j in tuple(self.config_json.表单[var]["字段"]):
                template_data1 += f'{j},'
            template_data1 = template_data1[:-1]
            for j in tuple("%s" if i == "int" else "'%s'" for i in tuple(self.config_json.表单[var]["类型"])):
                template_data2 += f'{j},'
            template_data2 = template_data2[:-1]
            # print(template%(template_data1, template_data2), *data_transmit)
            for i in self.config_json.表单[var]["字段"]:  # 整理传递参数
                data_transmit.append(data[i])
            self.data_vessel_select['sqlite'].execute(template % (template_data1, template_data2), *data_transmit)
        # 二次存入方法
        else:
            template = f'update {form_name} set %s where user = "{data[self.config_json.表单[var]["字段"][0]]}"'
            # print(list(data.keys())[:1])
            for i in list(data.keys())[1:]:

                if self.config_json.表单[var]["类型"][self.config_json.表单[var]['字段'].index(i)] == 'int':
                    # print(2,data[i])
                    self.data_vessel_select['sqlite'].execute(template % f'{i} = {i}+%s', data[i])
                else:
                    self.data_vessel_select['sqlite'].execute(template % f'{i}=%s', data[i])


# json便携类
class JsonExecute(DataProt):
    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None):
        json_data = self.data_vessel_select['json'].read()

        # 获取指定表单的数据
        form_data = json_data.get(form_name, {})

        # 如果有筛选条件，进行筛选
        if screening_condition:
            key, value = screening_condition.split('==')
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            # 筛选出符合条件的记录索引
            filtered_indices = [i for i, v in enumerate(form_data[key]) if v == value]
        else:
            # 没有筛选条件则选取所有记录
            filtered_indices = range(len(list(form_data.values())[0]))

        # 如果指定了字段，提取该字段的数据，并返回与MySQL一致的格式
        if field:
            result = [(form_data[field][i],) for i in filtered_indices]
        else:
            # 如果没有指定字段，则提取所有字段的数据，并返回与MySQL一致的格式
            result = [tuple(form_data[k][i] for k in form_data) for i in filtered_indices]

        return result

    def data_deposit_execute(self, form_name: str, data: dict = None):
        # 获取 JSON 数据
        var = [j for j in self.config_json.表单 if self.config_json.表单[j]["表单名称"] == form_name][0]
        json_data = self.data_vessel_select['json'].read()  # 直接读取为字典，无需json.loads
        if not data[self.config_json.表单[var]["字段"][0]] in json_data[form_name][
            self.config_json.表单[var]["字段"][0]]:
            for i in list(data.keys()):
                json_data[form_name][i].append(data[i])
            self.data_vessel_select['json'].deposit(json_data)
        else:
            key = json_data[form_name][self.config_json.表单[var]["字段"][0]].index(
                data[self.config_json.表单[var]["字段"][0]])
            print(data.keys()[1:])
            for i in list(data.keys()[1:]):
                json_data[form_name][i][key] = data[i]
            self.data_vessel_select['json'].deposit(json_data)


class DataExecute:
    def __init__(self, name: str):
        self.data_dic: dict = {'mysql': MysqlExecute(),
                               'sqlite': SqlIteExecute(),
                               'json': JsonExecute()}
        self.name = name
        #print(data_class_port.MyData.get_convenient_class())
        self.data_dic.update(data_class_port.MyData.get_convenient_class())

    def data_read_execute(self, form_name: str, screening_condition: str = None, field: str = None):
        """

        :param form_name: 表单名称
        :param screening_condition: 限制表达式
        :param field: 字段
        :return:
        """
        # print(self.name)
        return self.data_dic[self.name].data_read_execute(form_name, screening_condition, field)

    def data_deposit_execute(self, form_name: str, **data):
        """

        :param form_name: 表单名称
        :param data: 存入内容
        :return:
        """
        # print(data)
        self.data_dic[self.name].data_deposit_execute(form_name, data)
