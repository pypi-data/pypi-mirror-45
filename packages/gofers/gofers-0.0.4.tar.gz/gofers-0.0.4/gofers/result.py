import copy
import pymongo
import prettytable
import json
import jsonpath
import re
import operator
import time
from .util import ConfigHandler

# flag
PARAMETER_FLAG = '${'
FLAG_CASE = 'AT_'
FLAG_FIXTURE = 'conftest'
# specials vars
VALUE_JSON_SPECIALS = ['\"', '[', ']', '\'', ' ', '\\', '//']
VALUE_ATTR_SPECIALS = ['$', '\"', '[', ']', '\'', ' ', '\\', '//', '{', '}']
TIMER = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class MongoDB(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, path):
        cfg = ConfigHandler(path).cfg
        env = cfg.get('env')
        mongodb = cfg.get('mongodb')
        project_name = env['project']
        mongo_host = mongodb['host']
        mongo_port = mongodb['port']
        db_name = mongodb['dbname']
        self.mongo_client = pymongo.MongoClient(host=mongo_host,
                                                port=int(mongo_port))
        db = self.mongo_client[db_name]
        self.collection = db[project_name]
        self.version = {'_id': 'VERSION: ' + str(cfg.TIMER)}
        self.version_id = copy.deepcopy(self.version)
        # create version if no version or begin start exec scripts.
        if not self.collection.find_one(filter=self.version):
            self.collection.insert_one(self.version)

    def repository(self):
        return self.collection.find_one(self.version)

    def insert(self, responses):
        self.version.update(responses)
        if isinstance(self.version, dict):
            self.collection.update_one(filter=self.version_id,
                                       update={'$set': self.version})

    def save_step(self, name, step, response):
        if name in self.repository():
            responses = self.repository()[name]
            if step in responses:
                del responses[step]
            responses.update({step: response})
            _responses = {name: responses}
            self.collection.update_one(filter=self.version_id,
                                       update={'$set': _responses})
        else:
            responses = {name: {step: response}}
            self.collection.update_one(filter=self.version_id,
                                       update={'$set': responses})

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

    @staticmethod
    def check(verify_points, response):
        table = Verifier.result_table()
        result_tb = Verifier.cmp(expect=verify_points,
                                 actul=response,
                                 table=table)
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
                    raise KeyError('接口响应Response:{} \n 未包含期望参数: {}'.format(
                        actul, ke))
        elif isinstance(expect, list):
            if len(expect) != len(actul):
                raise AssertionError("List len: '{}' != '{}'".format(
                    len(expect), len(actul)))
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
