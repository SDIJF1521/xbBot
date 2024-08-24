import re


def analysis_news(news: str, command='', symbol='\|', division: bool = True, many_times: bool = True):
    """

    :param news: 文本内容
    :param command: 触发命令
    :param symbol: 可选参数 分离符号不可为空格默认为|
    :param division: 分割可选参数用于执行相关参数的分割，默认为true
    :param many_times:多次分割默认为多次即True
    :return:
    """
    len = re.findall(re.compile(symbol), news)
    if division:
        if many_times:
            if len(len) != 0:
                if len(re.findall(re.compile(symbol), news)) != 0:
                    data = news.replace(' ', '')[len(command):]
                    return re.split(symbol, data)
            else:
                return news.replace(command, '').replace(' ', '')
        else:
            print('OK')
            if symbol in news:
                data = news.replace(' ', '')[len(command):]
                Index = data.index(symbol)
                print(Index)
                return [data[0:Index], data[Index + 1:len(data)]]
            else:
                return None
    else:
        data = (news.replace(' ', '')[len(command):])
        return data
