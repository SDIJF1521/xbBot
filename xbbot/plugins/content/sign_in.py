import datetime
import random
from xbbot.plugins.basics_library import *
from jinja2 import Environment, FileSystemLoader
import os
import Path

path = os.path.dirname(os.path.abspath(__file__).replace("\\", "/"))


class SignIn(BaseClass):
    config_json = Gai(GaiJson()).execute()
    function_name = '签到功能'

    def execute(self, data: dict):
        score = random.randint(3, 30)
        tobay = datetime.date.today()
        user_list = []
        for i in DataExecute(Gai(GaiYml()).execute().内容设置['数据存储设置']).data_read_execute(
                form_name=self.config_json.表单[self.function_name + '表单']['表单名称'], field='user'):
            user_list.append(i[0])
        if not data['user'] + '|' + data['group'] in user_list:
            DataExecute(Gai(GaiYml()).execute().内容设置['数据存储设置']).data_deposit_execute(
                form_name=self.config_json.表单[self.function_name + '表单']['表单名称'],
                user=data['user'] + '|' + data['group'], 积分=score, 日期=str(tobay), 天数=1)
            file_loader = FileSystemLoader(f'./template/')
            env = Environment(loader=file_loader)
            template = env.get_template(f'NXD.html')
            template_data = [data['membership_information']['nickname'], 1, score, score]
            # 准备要渲染的数据
            context = dict(zip(['name', 'time', 'integral_1', 'integral_2'], template_data))
            # 渲染模板
            output = template.render(context)
            # 将渲染结果保存到文件
            with open('./template/output.html', 'w+', encoding='utf-8') as file:
                file.write(output)
            os.system('python JT.py')
            return f'[CQ:image,file={Path.path}/签到.png]'
        else:
            if not DataExecute(Gai(GaiYml()).execute().内容设置['数据存储设置']).data_read_execute(
                    form_name=self.config_json.表单[self.function_name + '表单']['表单名称'], field='日期')[0][
                       0] == str(tobay):
                DataExecute(Gai(GaiYml()).execute().内容设置['数据存储设置']).data_deposit_execute(
                    form_name=self.config_json.表单[self.function_name + '表单']['表单名称'],
                    user=data['user'] + '|' + data['group'], 积分=score, 日期=str(tobay), 天数=1, )
                file_loader = FileSystemLoader(f'./template/')
                env = Environment(loader=file_loader)
                # 加载模板
                template = env.get_template(f'NXD.html')
                sign_in_data = DataExecute(Gai(GaiYml()).execute().内容设置['数据存储设置']).data_read_execute('pd',
                                                                                                               f'user = {data["user"]}"|"{data["group"]}')[0]
                template_data = [data['membership_information']['nickname'], sign_in_data[3], sign_in_data[1], score]
                # 准备要渲染的数据
                context = dict(zip(('name', 'time', 'integral_1', 'integral_2'), template_data))
                # 渲染模板
                output = template.render(context)
                # 将渲染结果保存到文件
                with open('./template/output.html', 'w', encoding='utf-8') as file:
                    file.write(output)
                os.system('python JT.py')
                return f'[CQ:image,file={Path.path}/签到.png]'
            else:
                return f'[CQ:at,qq={data["user"]}]今天已经签到过了'
