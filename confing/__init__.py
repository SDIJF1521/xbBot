import os
import json
import importlib.util
from confing import yml
from confing import confing_data
from confing import creation_config
from confing import data_confing_file
from confing import apply_json_config

function_name_list = []
function_switch = []


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


# 获取yml功能名称机器功能状态


class Apply:
    def __init__(self):
        folder_path ='./confing/plug'
        import_classes_from_folder(folder_path)
        self.config_data_dict = {'yml': confing_data.GaiYml(),
                                 'json': confing_data.GaiJson()}
        # 定义数据容器配置生成类字典
        self.data_config_file_dict = {'mysql': data_confing_file.MysqlConfig(),
                                      'sqlite': data_confing_file.SqliteConfig(),
                                      'json': data_confing_file.JasonConfig()}
        self.data_config_file_dict.update(creation_config.CreateConfigParent.get_class_dic())
        if os.path.exists('./data_config.json'):
            # 定义数据容器配置应用类字典
            self.apply_json = {'sqlite': apply_json_config.SqliteCreation(),
                               'mysql': apply_json_config.MysqlCreation(),
                               'json': apply_json_config.JsonCreation()}
            self.apply_json.update(creation_config.CreateConfigParent.get_class_dic())

        self.function_command_list = []

    def config_json_create(self):
        print(self.data_config_file_dict)
        data_confing_file.DataConfigFile(self.data_config_file_dict[
                                             confing_data.Gai(self.config_data_dict['yml']).execute().内容设置[
                                                 '数据存储设置']]).execute()

    # 应用配置
    def apply_config(self):
        # 通过config.yml来更改nb框架配置
        with open('.env', 'w+', encoding='utf-8') as env_file:
            env_file.write("ENVIRONMENT=prod\n"
                           "DRIVER=~fastapi")

        with open('.env.dev', 'w+', encoding='utf-8') as dev_file:
            dev_file.write(f"HOST={confing_data.Gai(self.config_data_dict['yml']).execute().基本设置['主机地址']}\n"
                           f"PORT={confing_data.Gai(self.config_data_dict['yml']).execute().基本设置['端口']}\n"
                           f"LOG_LEVEL=DEBUG\n"
                           f"FASTAPI_RELOAD=false")

        with open('.env.prod', 'w+', encoding='utf-8') as prod_file:
            admin = ''
            for i in confing_data.Gai(self.config_data_dict['yml']).execute().基本设置['管理员账号']:
                admin += f'\"{i}"'

            prod_file.write(f"HOST={confing_data.Gai(self.config_data_dict['yml']).execute().基本设置['主机地址']}\n"
                            f"PORT=28081\n"
                            f"SUPERUSERS=[{admin}]  # "
                            f"配置 NoneBot 超级用户\n"
                            f"NICKNAME=[\"{confing_data.Gai(self.config_data_dict['yml']).execute().基本设置['机器人名称']}\"] "
                            f" # 配置机器人的昵称\n"
                            f"COMMAND_START=[\"/\", \"\"]  # 配置命令起始字符\n"
                            f"COMMAND_SEP=[\".\"]  # 配置命令分割字符\n\n\n"
                            "# Custom Configs\n"
                            "CUSTOM_CONFIG1=\"config in env file\"\n"
                            "CUSTOM_CONFIG2=")

        # 应用config.json配置

        if not os.path.isdir('./xbbot/data'):
            os.makedirs('./xbbot/data')
        apply_json_config.ExecuteCreation(self.apply_json[
                                              confing_data.Gai(self.config_data_dict['yml']).execute().内容设置[
                                                  '数据存储设置']]).execute()

    # 生成必要文件
    def Fcreate_essential_document(self):

        Apply().function_list(confing_data.Gai(confing_data.GaiYml()).execute().内容设置['功能设置'])
        for j in range(1, len(function_name_list) + 1):
            self.function_command_list.append([f'function_command{j}'])
        with open('./xbbot/data/function_command_config.json', 'w+', encoding='utf-8') as f:
            json.dump(dict(zip(function_name_list, self.function_command_list)), f, indent=4, ensure_ascii=False)

    # 获取功能名称列表和功能状态
    def function_list(self, data: dict):
        for i in data.items():
            if isinstance(i[1], dict):
                Apply().function_list(i[1])
            else:
                function_name_list.append(i[0])
                function_switch.append(i[1])