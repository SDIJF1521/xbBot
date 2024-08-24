import json
from xbbot.plugins.basics_library.standard import *
from xbbot.plugins.basics_library.analysis import *
from xbbot.plugins.basics_library.Data import *


def command_read() -> dict:
    with open('./xbbot/data/function_command_config.json', 'r', encoding='utf-8') as f:
        return json.load(f)
