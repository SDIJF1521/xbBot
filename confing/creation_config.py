class CreateConfigParent(type):
    """
    :param:注意必须实现 create方法用于生成配置文件和creation方法应用配置文件，data_container_name属性必须存在用于判断数据容器
    """
    data_name_list = []
    data_config_class = []

    def __new__(cls, name, bases, dic):

        if 'data_container_name' not in dic and not callable(dic.get('data_container_name')):
            raise TypeError('必须有data_container_name属性用于判断数据容器')

        if not callable(dic.get('create')):
            raise TypeError('数据配置类类必须实现create方法用于生成配置文件')

        if not callable(dic.get('creation')):
            raise TypeError('数据配置类类必须实现creation方法用于应用配置文件')
        data_class = super().__new__(cls, name, bases, dic)
        cls.data_name_list.append(dic['data_container_name'])
        cls.data_config_class.append(data_class())
        return data_class

    @classmethod
    def get_class_dic(cls):
        return dict(zip(cls.data_name_list, cls.data_config_class))
