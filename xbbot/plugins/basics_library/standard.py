from abc import abstractmethod


# 定义功能执行元类
class FunctionSuperclass(type):
    registry = []
    name_list = []

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        cls.name_list.append(attrs.get('function_name', None))
        cls.registry.append(new_class())
        if not 'function_nam' in attrs and callable(attrs.get('function_nam')):
            raise TypeError('function_nam属性必须存在用于判断功能')
        return new_class

    @classmethod
    def get_all_classes(cls):
        return cls.registry

    @classmethod
    def get_all_name(cls):
        return cls.name_list


# 定义功能执行策略基类
class BaseClass(metaclass=FunctionSuperclass):
    function_name: str = None

    @abstractmethod
    def execute(self, data: dict):
        pass


# 策略执行上下文类
class FunctionExecute:
    def __init__(self, name: BaseClass):
        self.name = name
        print(name)

    def execute(self, **data):
        msg = self.name.execute(data)
        return msg
