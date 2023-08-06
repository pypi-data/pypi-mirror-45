import copy
import hashlib
import json
import os
import re
import shutil
import time

import jsonpath
import prettytable
import requests
import yaml
import operator
import pymongo


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


# environment config info
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = YmlReader(os.path.join(ROOT_DIR, 'gofers.yml')).data
gofers = dict(
    env=config.get('env'),
    http=config.get('http'),
    mongodb=config.get('mongodb')
)
# global path
CASE_DIR = os.path.join(ROOT_DIR, 'case', gofers['env']['project'])
SCRIPT_DIR = os.path.join(ROOT_DIR, 'script', gofers['env']['project'])
REPORT_DIR = os.path.join(ROOT_DIR, 'report')
# define vars for batch runner
REPORT_TIME_FORMATTER = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
REPORT_ALLURE_PATH = r'%s\allure-results\%s' % (
    REPORT_DIR, REPORT_TIME_FORMATTER)
CMD_EXEC_PYTEST_ALLURE = r'pytest --alluredir %s' % REPORT_ALLURE_PATH
CMD_EXEC_PYTEST_ALLURE_GENERATE = r'allure generate --clean %s' % REPORT_ALLURE_PATH
# flag
PARAMETER_FLAG = '${'
FLAG_CASE = 'AT_'
FLAG_FIXTURE = 'conftest'
# specials vars
VALUE_JSON_SPECIALS = ['\"', '[', ']', '\'', ' ', '\\', '//']
VALUE_ATTR_SPECIALS = ['$', '\"', '[', ']', '\'', ' ', '\\', '//', '{', '}']
TIMER = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# Allure parameter define
# case level
_LEVEL = {
    '增加': 'Blocker',
    '删除': 'Normal',
    '修改': 'Critical',
    '编辑': 'Critical',
    '配置': 'Critical',
    '查询': 'Normal',
    '异常': 'Minor',
    '正常': 'Normal'
}


class MongoDB(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        env = gofers.get('env')
        mongodb = gofers.get('mongodb')
        project_name = env['project']
        mongo_host = mongodb['host']
        mongo_port = mongodb['port']
        db_name = mongodb['dbname']
        self.mongo_client = pymongo.MongoClient(
            host=mongo_host, port=int(mongo_port))
        db = self.mongo_client[db_name]
        self.collection = db[project_name]
        self.version = {'_id': 'VERSION: ' + str(TIMER)}
        self.version_id = copy.deepcopy(self.version)
        # create version if no version or begin start exec scripts.
        if not self.collection.find_one(filter=self.version):
            self.collection.insert_one(self.version)

    def repository(self):
        return self.collection.find_one(self.version)

    def insert(self, responses):
        self.version.update(responses)
        if isinstance(self.version, dict):
            self.collection.update_one(filter=self.version_id, update={
                                       '$set': self.version})

    def save_step(self, name, step, response):
        if name in self.repository():
            responses = self.repository()[name]
            if step in responses:
                del responses[step]
            responses.update({step: response})
            _responses = {name:  responses}
            self.collection.update_one(
                filter=self.version_id, update={'$set': _responses})
        else:
            responses = {name: {step: response}}
            self.collection.update_one(
                filter=self.version_id, update={'$set': responses})

    def get_step(self, name, step):
        return self.repository()[name][step]


class Pool:

    @staticmethod
    def save_step(name, step, response):
        MongoDB().save_step(name, step, response)

    @staticmethod
    def get_step(name, step):
        return MongoDB().get_step(name, step)

    @staticmethod
    def update(name, parameters):
        params = copy.deepcopy(parameters)
        if isinstance(params, list):
            for index, value in enumerate(params):
                params[index] = Pool._handler(name=name, parameters=value)
            params = str(params).replace('\'', '')
        elif isinstance(params, dict):
            for key, value in params.items():
                params[key] = Pool._handler(name=name, parameters=value)
        return params

    @staticmethod
    def _handler(name, parameters):
        if isinstance(parameters, str) and PARAMETER_FLAG in parameters:
            attr = Pool._attr(parameters)
            val = Pool._value(name, attr)
            parameters = parameters.replace(attr, val).replace('\'', '')
        elif isinstance(parameters, list):
            parameters = str(parameters)
        return parameters

    @staticmethod
    def _attr(parameter):
        if ':' in parameter:
            for p in parameter.split(':'):
                if ',' in p:
                    p = Pool._remove(p).split(',')[0]
                if PARAMETER_FLAG in p:
                    return p
        else:
            parameter = Pool._remove(parameter)
        return parameter

    @staticmethod
    def _value(name, attr):
        #: ${date_setup}.proposalId
        steps = attr.split('.')
        # step
        fixture_step = Pool._clear(content=steps[0][2:-1])
        # attribute
        fixture_attr = Pool._clear(content=steps[-1])
        response = MongoDB().get_step(name, fixture_step)
        return Pool._get_value(fixture_attr, response)

    @staticmethod
    def _get_value(key, responses):
        if isinstance(responses, dict):
            return jsonpath.jsonpath(responses, '$..%s' % key)[0]
        elif isinstance(responses, (list, tuple)):
            for index, _data in enumerate(responses):
                Pool._get_value(key, _data)

    # @staticmethod
    # def _get_value(key, responses):
    #     if isinstance(responses, dict):
    #         for k, v in responses.items():
    #             if isinstance(v, (str, int, bool)) and operator.eq(k, key):
    #                 return v
    #             else:
    #                 Pool._get_value(key, v)
    #     elif isinstance(responses, (list, tuple)):
    #         for index, _data in enumerate(responses):
    #             Pool._get_value(key, _data)

    @staticmethod
    def _remove(content):
        for special in VALUE_JSON_SPECIALS:
            if isinstance(content, str):
                content = content.replace(special, '')
        return content

    @staticmethod
    def _clear(content):
        for special in VALUE_ATTR_SPECIALS:
            if isinstance(content, str):
                content = content.replace(special, '')
        return content


class ABS:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        env = gofers['env']
        http = gofers['http']
        self.base_url = 'http://%s:%s/%s' % (
            env['server'],
            env['port'],
            env['project']
        )
        self.method = None
        self.headers = http['default headers']
        self.params = {}
        self.data = {}
        self.files = {}
        self.timeout = 120
        self.client = self.m(env)

    def __str__(self):
        return self.base_url

    def _headers(self, request):
        headers = copy.deepcopy(self.headers)
        if 'headers' in request:
            headers.update(request['headers'])
        return headers

    # TODO: developer whc about ADPassword
    def m(self, env):
        login = env['login']
        user = env['user']
        password = env['password'].encode('utf-8')
        md5_password = hashlib.new('md5', password).hexdigest()
        login_usr_info = dict(
            userName=user,
            password=md5_password,
            ADPassword=password
        )
        try:
            m = requests.session()
            m.request(method='post', url=self.base_url +
                      login, data=login_usr_info)
            return m if m else None
        except Exception:
            raise ConnectionRefusedError(
                'url: %s\n user info: %s' % (self.base_url, login_usr_info))

    def http(self, step, parameters):
        #: parameters
        name = parameters['name']
        parameters = parameters['data'][step]
        request = parameters['request']
        validator = parameters['validator']
        #: request
        method = request['method']
        url = self.base_url + request['url']
        data = request['data'] if method == 'post' else None
        _params = request['data'] if method == 'get' else None
        headers = self._headers(request=request)
        files = request['files'] if 'files' in request else None
        data = Pool.update(name=name, parameters=data) if data else None
        response = self.client.request(method=method, url=url, params=_params, data=data, headers=headers,
                                       files=files, timeout=self.timeout).json()
        Pool.save_step(name=name, step=step, response=response)
        Verifier.check(verify_points=validator, response=response)
        return response

    def send(self, name, step, parameters):
        #: parameters
        request = parameters['request']
        validator = parameters['validator']
        #: request
        method = request['method']
        url = self.base_url + request['url']
        data = request['data'] if method == 'post' else None
        _params = request['data'] if method == 'get' else None
        headers = self._headers(request=request)
        files = request['files'] if 'files' in request else None
        data = Pool.update(name=name, parameters=data) if data else None
        response = self.client.request(method=method, url=url, params=_params, data=data, headers=headers,
                                       files=files, timeout=self.timeout).json()
        Pool.save_step(name=name, step=step, response=response)
        Verifier.check(validator, response=response)
        return response


ABS = ABS()


class Verifier:
    @staticmethod
    def result_table():
        table = prettytable.PrettyTable()
        table.field_names = ['参数名', '期望值', '实际值', '结果']
        table.header_style = 'title'
        table.align['参数名'] = 'l'
        table.padding_width = 2
        print('\n')
        return table

    # print result of case_pro by table style
    # add green and red result
    """
        +----------------------+------------------------+------------------------+--------+
        |  参数名              |         期望值         |         实际值         |  结果  |
        +----------------------+------------------------+------------------------+--------+
        |  total               |           10           |           10           |  True  |
        |  isLogin             |          True          |          True          |  True  |
        |  page                |           1            |           1            |  True  |
        |  isSuccess           |          True          |          True          |  True  |
        |  records             |           1            |           1            |  True  |
        |  isException         |         False          |         False          |  True  |
        |  projectId           |      201952828999      |      201952828999      |  True  |
        |  projectName         |  AT_微粒贷测试项目005  |  AT_微粒贷测试项目005  |  True  |
        |  setUpDate           |  2018-11-09 00:00:00   |  2018-11-09 00:00:00   |  True  |
        |  legalMaturityDate   |  2021-12-21 00:00:00   |  2021-12-21 00:00:00   |  True  |
        |  issueSize           |       100000000        |       100000000        |  True  |
        |  outstandingBalance  |       100000000        |       100000000        |  True  |
        |  payedPeriod         |   2018年2期（总0期）   |   2018年2期（总0期）   |  True  |
        |  followManager       |          heli          |          heli          |  True  |
        |  projectManager      |          何莉          |          何莉          |  True  |
        |  projectType         |        AST_PCL         |        AST_PCL         |  True  |
        |  projectStatus       |        PJS_ISF         |        PJS_ISF         |  True  |
        |  procStatus          |          None          |          None          |  True  |
        |  nodeName            |         存续期         |         存续期         |  True  |
        |  moduleId            |        PROJM01         |        PROJM01         |  True  |
        |  moduleName          |        项目全景        |        项目全景        |  True  |
        |  issueMarket         |        IMK_SHE         |        IMK_SHE         |  True  |
        |  operaterOrg         |          None          |          None          |  True  |
        |  projectManageType   |       PMT_TRENDS       |       PMT_TRENDS       |  True  |
        +----------------------+------------------------+------------------------+--------+
    """
    @staticmethod
    def check(verify_points, response):
        table = Verifier.result_table()
        result_tb = Verifier.cmp(expect=verify_points,
                                 actul=response, table=table)
        result_rt = result_tb.get_string(fields=['结果'])
        table.clear_rows()
        if 'False' in result_rt:
            raise ValueError('期望参数: {}, 实际响应: {}'.format(
                verify_points, response))

    @staticmethod
    def cmp(expect, actul, table):
        """
            compare expect HTTP response and actul response parameters.
        """
        global ke, result
        try:
            json.dumps(expect, ensure_ascii=False)
            json.dumps(actul, ensure_ascii=False)
        except Exception:
            raise AttributeError('接口响应参数或期望参数类型设置异常！')
        if isinstance(expect, dict):
            for ke, va in expect.items():
                if ke in actul.keys():
                    if operator.eq(ke, 'rows'):
                        expect[ke], actul[ke] = Verifier.rows_setup(
                            expect=expect[ke], actul=actul[ke])
                        Verifier.cmp(va, actul[ke], table)
                    else:
                        Verifier.cmp(expect[ke], actul[ke], table)
                else:
                    raise KeyError(
                        '接口响应Response:{} \n 未包含期望参数: {}'.format(actul, ke))
        elif isinstance(expect, list):
            if len(expect) != len(actul):
                raise AssertionError("List len: '{}' != '{}'"
                                     .format(len(expect), len(actul)))
            for src_list, dst_list in zip(sorted(expect), sorted(actul)):
                Verifier.cmp(src_list, dst_list, table)
        else:
            result = operator.eq(str(expect), str(actul))
            table.add_row([ke, expect, actul, result])
        return table

    @staticmethod
    def rows_setup(expect, actul):
        global md
        expect = str(expect).replace('\\n        ', '')
        expect = expect.replace('\\n    ', '')
        expect = expect.replace('\\n\\t', '')
        actul = str(actul).replace('\\n        ', '')
        actul = actul.replace('\\n    ', '')
        d = re.findall(r'\d+', actul)
        for i in d:
            if str(i).startswith('20190'):
                md = actul.replace(i, '***')
        return md, expect


class Api:
    def __init__(self, script):
        # base info
        self.yml = get_yml_by_script(script)
        self.description = YmlReader(yaml_file=self.yml)
        self.data = dict(
            name=self.description.name,
            data=self.description.data
        ) or FileExistsError('Un support test description file: %s' % self.yml)

    # Gofers要求测试用例描述文件严格的命名规范：
    # AT_模块内用例编号_功能模块名称_模块下分支功能_测试用例级别_测试步骤
    # Feature: 标注主要功能模块
    # Story: 标注Features功能模块下的分支功能
    # Severity: 标注测试用例的重要级别
    # Blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
    # Critical级别：临界缺陷（ 功能点缺失）
    # Normal级别：普通缺陷（数值计算错误）
    # Minor级别：次要缺陷（界面错误与UI需求不符）
    # Trivial级别：轻微缺陷（必输项无提示，或者提示不规范）
    # Step: 标注测试用例的重要步骤
    @property
    def conventions(self):
        try:
            project = gofers['env']['project']
            elements = os.path.basename(self.yml)[:-4].split('_')[2:]
            feature, story, severity = elements[:3]
            step = ''.join(elements[3:])

            api = list(self.description.data.keys())[0]
            preconditions = self.description.data[api]['preconditions'] or None
            if preconditions:
                preconditions = ', '.join(preconditions)
            else:
                preconditions = ''
            if severity:
                severity = _LEVEL[severity]
            return project, feature, story, severity, api, preconditions, step, self.description.name
        except IndexError:
            raise FileExistsError(
                'Un support case Naming conventions: %s' % self.yml)

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=2)

    @staticmethod
    def send(step, parameters):
        return ABS.http(step=step, parameters=parameters)

    @staticmethod
    def parameters(script):
        return Api(script).data


class Fixture:
    def __init__(self, script):
        # base info
        script = str(script).replace('script', 'case')
        self.yml = script.replace('.py', '.yml')
        self.description = YmlReader(yaml_file=self.yml)
        self.name = self.description.name
        self.data = self.description.data or FileExistsError(
            'Un support test description file: %s' % self.yml)
        self.names = list(self.data.keys())

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=2)

    @staticmethod
    def send(step, request, parameters):
        parameter_table = parameters[step]
        parameter_setup = parameter_table['setup'] if 'setup' in parameter_table else None
        parameter_teardown = parameter_table['teardown'] if 'teardown' in parameter_table else None
        if parameter_setup:
            ABS.send(name=request.fspath.purebasename,
                     step=step + '_' + 'setup',
                     parameters=parameter_setup)

        def fin():
            if parameter_teardown:
                ABS.send(name=request.fspath.purebasename,
                         step=step + '_' + 'teardown',
                         parameters=parameter_teardown)

        request.addfinalizer(fin)

    @staticmethod
    def parameters(script):
        return Fixture(script).data


class Repository:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, path=None):
        self.repository = []
        if not path:
            self.root_path = CASE_DIR

    @property
    def yml(self):
        for root, dirs, files in os.walk(top=self.root_path, topdown=False):
            for file in files:
                yml = os.path.join(root, file)
                if os.path.isfile(yml):
                    self.repository.append(yml)
        return self.repository


PROFILE_CASE = """#!/usr/local/python3.6.8
# -*- coding: utf-8 -*-
# desc: Automatically generated scripts by Gofers, Do not support maintenance

import pytest
import allure
from gofers.factory import Api


@pytest.mark.{PROJECT}
@allure.feature('{FLAG_FEATURE}')
@allure.story('{FLAG_STORY}')
@allure.severity('{FLAG_SEVERITY}')
def {TEST_STEP}({PRECONDITIONS}):
    parameters_table = Api.parameters(__file__)
    with allure.step('{FLAG_STEP}'):
        Api.send(step='{TEST_STEP}', parameters=parameters_table)


if __name__ == '__main__':
    pytest.main(['-s', '{SCRIPT_NAME}.py'])

"""
PROFILE_FIXTURE_HEADER = """# # -*- coding: utf-8 -*-
import pytest
import allure
from gofers.factory import Fixture

parameters_table = Fixture.parameters(__file__)
"""
PROFILE_FIXTURE_BODY = """

@pytest.fixture()
@allure.step('{FIXTURE_NAME}')
def {FIXTURE_NAME}(request):
    Fixture.send(step='{FIXTURE_NAME}', request=request, parameters=parameters_table)
"""


def get_script_by_yml(yml):
    script = str(yml).replace('case', 'script')
    script = script.replace('.yml', '.py')
    return script


def get_yml_by_script(script):
    case = str(script).replace('script', 'case')
    yml = case.replace('.py', '.yml')
    return yml


class Generator:

    @staticmethod
    def is_case(yml):
        if FLAG_CASE in yml:
            return True

    @staticmethod
    def is_fixture(yml):
        if FLAG_FIXTURE in yml:
            return True

    @staticmethod
    def case_info(yml):
        return Api(script=get_script_by_yml(yml)).conventions

    @staticmethod
    def fixture_info(yml):
        return Fixture(script=get_script_by_yml(yml)).names

    @staticmethod
    def _script_content(yml):
        project, feature, story, severity, api, preconditions, step, name = Generator.case_info(
            yml)
        script = PROFILE_CASE.format(PROJECT=project,
                                     FLAG_FEATURE=feature,
                                     FLAG_STORY=story,
                                     FLAG_SEVERITY=severity,
                                     TEST_STEP=api,
                                     PRECONDITIONS=preconditions,
                                     FLAG_STEP=step,
                                     SCRIPT_NAME=name)
        return script

    @staticmethod
    def _fixture_content(yml):
        _fixtures = ''
        names = Generator.fixture_info(yml)
        for name in names:
            _fixtures += PROFILE_FIXTURE_BODY.format(FIXTURE_NAME=name)
        return PROFILE_FIXTURE_HEADER + _fixtures

    @staticmethod
    def generate(yml):
        global contents
        name = get_script_by_yml(yml)
        if os.path.exists(name):
            os.remove(name)
        dirs = os.path.dirname(name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(name, 'ab') as s:
            if Generator.is_case(yml):
                contents = Generator._script_content(yml)
            elif Generator.is_fixture(yml):
                contents = Generator._fixture_content(yml)
            if contents:
                s.write(contents.encode('utf-8'))

    @staticmethod
    def scripts():
        Generator.clear()
        yml_list = Repository().yml
        for yml in yml_list:
            Generator.generate(yml)

    @staticmethod
    def clear(path=SCRIPT_DIR):
        if os.path.exists(path):
            shutil.rmtree(path)


if __name__ == '__main__':
    pass
