import os
import json
import confing
import importlib.util
from nonebot import on_regex
from nonebot.adapters import Event
from xbbot.plugins.basics_library import *
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, Message


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
folder_path = "./xbbot/plugins/content"  # 假设 plug 文件夹与 main.py 在同一目录

# 导入 plug 文件夹中的所有类
import_classes_from_folder(folder_path)

# 注册调度事件
Allocation = on_regex('.+', priority=5)
print('yes')

@Allocation.handle()
async def allocation(event: GroupMessageEvent, bot: Bot, event1: Event):
    print(2)
    news = str(event.message)
    function_command = command_read()
    # 生成功能调用字典
    print(FunctionSuperclass.name_list[1::])
    dunction_dict = dict(zip(FunctionSuperclass.name_list[1::], FunctionSuperclass.get_all_classes()[1::]))
    print(dunction_dict)
    for i in function_command.values():
        for j in i:
            print(j)
            if news[:len(j)] == j:
                print(
                    f'命令{j}匹配成功，功能为{list(function_command.keys())[list(function_command.values()).index(i)]}开始检测功能状态')
                confing.Apply().function_list(
                    confing.confing_data.Gai(confing.confing_data.GaiYml()).execute().内容设置['功能设置'])
                if confing.function_switch[confing.function_name_list.index(
                        list(function_command.keys())[list(function_command.values()).index(i)])]:
                    print('功能状态为启用开始执行')
                    print(list(function_command.keys())[list(function_command.values()).index(i)])
                    print(dunction_dict)
                    print(FunctionExecute(
                        dunction_dict[list(function_command.keys())[list(function_command.values()).index(i)]]))
                    msg = FunctionExecute(
                        dunction_dict[list(function_command.keys())[list(function_command.values()).index(i)]]).execute(
                        user=str(event.user_id), group=str(event.group_id),membership_information=await bot.call_api('get_group_member_info', **{'group_id': event.group_id,'user_id': event.user_id}))
                    if isinstance(msg, str):
                        await Allocation.send(Message(msg))
                    elif isinstance(msg, tuple):
                        if 0 < len(msg) < 2:
                            await bot.call_api(msg[0])
                        else:
                            await bot.call_api(msg[0], **msg[1])

