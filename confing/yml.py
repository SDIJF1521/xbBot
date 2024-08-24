import yaml

class Yaml:
    def __init__(self):
        yaml_content = {
            '基本设置':
                {
                    '机器人名称': '小白',
                    '主机地址': '127.0.0.1',
                    '端口': '28081',
                    '管理员账号': [12345678]},
            '内容设置': {
                '数据存储设置': 'sqlite',
                '功能设置': {
                    '命令自定义': True,
                    '签到功能': True,
                    '签词系统': {
                        '存签功能': True,
                        '抽签功能': True
                    },
                }
            }
        }
        with open('XB_config.yml', 'w+', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
