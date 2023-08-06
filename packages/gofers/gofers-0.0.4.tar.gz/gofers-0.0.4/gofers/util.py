import os
import time
import yaml


class YmlReader:
    # get content from yml file
    def __init__(self, yaml_file):
        if os.path.exists(yaml_file):
            self.yaml_file = yaml_file
        else:
            raise FileNotFoundError('Case description file not exits')
        self._data = None

    @property
    def data(self):
        # invoking this func will read yaml file ,
        # otherwise return TData before func invoking
        if not self._data:
            with open(self.yaml_file, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data[0]

    @property
    def name(self):
        return os.path.basename(self.yaml_file).split('.')[0]


class PathHandler:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, dest_path):
        if os.path.exists(dest_path):
            self.path = dest_path
        else:
            raise FileExistsError('Plase check testfile path.')
        self.root_slice = slice(0)

    @property
    def root(self):
        if 'case' in self.path:
            return self.path.split('case')[self.root_slice]
        else:
            raise FileExistsError('Plase check testfile path.')

    @staticmethod
    def get_script_by_yml(yml):
        script = str(yml).replace('case', 'script')
        script = script.replace('.yml', '.py')
        return script

    @staticmethod
    def get_yml_by_script(script):
        case = str(script).replace('script', 'case')
        yml = case.replace('.py', '.yml')
        return yml

    @staticmethod
    def get_ymlp_by_scriptp(scriptp):
        return str(scriptp).replace('script', 'case')

    @staticmethod
    def get_scriptp_by_ymlp(ymlp):
        return str(ymlp).replace('case', 'script')


class ConfigHandler:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, path):
        if os.path.exists(path):
            self.path = path
        else:
            raise FileExistsError('Plase check testfile path.')
        self.root = PathHandler(dest_path=path).root
        self.CASE_DIR = os.path.join(self.root, 'case',
                                     self.cfg['env']['project'])
        self.SCRIPT_DIR = os.path.join(self.root, 'script',
                                       self.cfg['env']['project'])
        self.REPORT_DIR = os.path.join(self.root, 'report')
        # define vars for batch runner
        self.REPORT_TIME_FORMATTER = time.strftime('%Y-%m-%d-%H-%M-%S',
                                                   time.localtime())
        self.REPORT_ALLURE_PATH = r'%s\\allure-results\%s' % (
            self.REPORT_DIR, self.REPORT_TIME_FORMATTER)
        self.CMD_EXEC = r'pytest --alluredir %s' % self.REPORT_ALLURE_PATH
        self.CMD_REPORT = r'allure generate --clean %s' % (
            self.REPORT_ALLURE_PATH)
        # level in case name
        self._LEVEL = dict(增加='Blocker',
                           删除='Normal',
                           修改='Critical',
                           编辑='Critical',
                           配置='Critical',
                           查询='Normal',
                           异常='Minor',
                           正常='Normal')

    # environment config info
    @property
    def cfg(self):
        config = YmlReader(os.path.join(self.root, 'gofers.yml')).data
        return dict(env=config.get('env'),
                    http=config.get('http'),
                    mongodb=config.get('mongodb'))
