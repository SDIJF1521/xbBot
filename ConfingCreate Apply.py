import os
from confing import yml,Apply

if os.path.exists('XB_config.yml') and not os.path.exists('data_config.json'):
    Apply().config_json_create()
    print('\033[4;33mdata_config.json文件已生成请进行配置\033[0m')

elif os.path.exists('XB_config.yml') and os.path.exists('data_config.json'):
    Apply().apply_config()
    Apply().Fcreate_essential_document()
    print('\033[4;33m已配置成功,机器人命令修改文件位置在XBbot/xbbot/data/function_command_config.json\033[0m')

else:
    yml.Yaml()
    print('\033[4;33mconfig.yml文件已生成请进行配置\033[0m')