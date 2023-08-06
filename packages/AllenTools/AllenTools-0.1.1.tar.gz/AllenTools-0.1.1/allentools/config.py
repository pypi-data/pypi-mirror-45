import json
import operator
import copy
import sys
import os

def _auto_update(func):
    """
    自动更新装饰器
    """
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if self.auto_update \
                and not operator.eq(self._info_bak, self.info):
            self.update_()
            self._info_bak = copy.deepcopy(self.info)

    return wrapper

class JSONKeeper:
    def __init__(self, json_path, data=None, auto_update=True, section=None, update=False):
        """
        :param json_path: 保存位置
        :param data: 附加信息。如果key已经存在，不会覆盖，如果不存在则添加
        :param auto_update: 修改值后自动更新文件
        :param section: 选择json中的一个section
        :param update: 如果已有内容是否使用data刷新数据
        """
        # self.config_path = self._relative_to_abs(json_path)
        self.config_path = json_path
        self.auto_update = auto_update
        # print(path)
        try:
            with open(self.config_path, 'r') as f:
                self.info = json.load(f)
        except FileNotFoundError:
            print('create {} in {}'.format(self.config_path, os.getcwd()))
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.info = {}
                json.dump(self.info, f, ensure_ascii=False, indent=4)
        if section:
            try:
                self.info = self.info[section]
            except KeyError:
                raise ValueError('section {} is not defined'.format(section))

        self._info_bak = copy.deepcopy(self.info)  # 做深拷贝作为修改快照

        if data:
            if type(data) is list and type(self.info) is not list:
                raise ValueError('can not append a list to json')
            for i in data:
                if not self.info.get(i) \
                        or self.info.get(i) and update:
                    self[i] = data[i]

    @staticmethod
    def _relative_to_abs(path):
        filename = sys._getframe(2).f_code.co_filename # 保护方法，外界调用源栈中索引为2
        file_dir = os.path.split(os.path.abspath(filename))[0]  # 实现相对目录导入
        if path[0] != '/' or '\\':  # 处理同目录文件的情况
            path = os.sep + path.replace('/', '\\')
        path = file_dir + path
        return path

    def update_(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.info, f, indent=4)

    def __str__(self):
        return str(self.info)

    def keys(self):
        return self.info.keys()

    def values(self):
        return self.info.values()

    @_auto_update
    def __setitem__(self, key, value):
        self.info[key] = value

    def __getitem__(self, item):
        return self.info[item]

    def find(self, key, default=None, return_list=True):
        """
        查找一个key的value

        使用这个方法查找数据可以保证在数据结构修改时不存在异常
        :param return_list:
        :param key:
        :param default:
        :return: List
        """
        value = self._find(self.info, key)
        if value is None:
            return default
        return value

    def _find(self, dic: dict, key):
        """
        find递归方法
        :param dic:
        :param key:
        :return:
        """
        value = dic.get(key)
        if not value:
            for d in dic.values():
                if type(d) is dict:
                    return self._find(d, key)
        return value

    def set(self, pos, value):
        """
        在指定位置插入/覆盖value

        pos形如
            layer1.layer2.layer3
        将实现
        this[layer1][layer2][layer3] = value
        """
        pos = pos.split('.')
        if len(pos) == 1:
            self[pos[0]] = value
            return
        temp = value
        for i in range(1, len(pos)):
            temp = {pos[-i]: temp}
        self[pos[0]] = {**(self[pos[0]] or {}), **temp}  # python>3.5 required

    def get(self, key, default=None):
        return self.info.get(key, default)

class Config:
    def to_json(self, indent=None):
        s = {}
        for i in self.__dir__():
            if not hasattr(self.__getattribute__(i), '__call__') and i[0] != '_' and i[-1] != '_':
                s[i] = self.__getattribute__(i)
        return json.dumps(s, indent=indent)

    def get(self, k, default=None):
        if k.upper() in self.__dir__():
            return self.__getattribute__(k.upper())
        return default

    def __setitem__(self, key, value):
        self.__setattr__(key.upper(), value)

    def __getitem__(self, item):
        return self.__getattribute__(item.upper())