import os
import re
import json
from collections import namedtuple
from . import util
from .runner import ABS


class CaseNamingConventionsError(Exception):
    """Gofers要求测试用例描述文件严格的命名规范：
        conventions:
            AT_模块内用例编号_功能模块名称_模块下分支功能_测试用例级别_测试步骤描述
        description:
            Feature: 标注主要功能模块
            Story: 标注Features功能模块下的分支功能
            Severity: 标注测试用例的重要级别
            Blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
            Critical级别：临界缺陷（ 功能点缺失）
            Normal级别：普通缺陷（数值计算错误）
            Minor级别：次要缺陷（界面错误与UI需求不符）
            Trivial级别：轻微缺陷（必输项无提示，或者提示不规范）
            Step: 标注测试用例的重要步骤
    for example:
        AT_015_方案设计_分档设计_增加_次级档_固定摊还_算头不算尾_A365_固定_兑付日
    """


class CaseSeverityError(Exception):
    pass


class CaseFileNotFoundError(Exception):
    pass


class CaseDescriptionError(Exception):
    pass


class EnvironmentInfoError(Exception):
    pass


class Api:
    """
    AT_015_方案设计_分档设计_增加_次级档_固定摊还_算头不算尾_A365_固定_兑付日.yml:
        test_security:
            desc: 增加-优先档-过手支付-算头不算尾-A365-固定
            preconditions:
                - project
                - date
                - imputation
                - transfer
                - redemption
                - credit
            request:
                url: /abswebapp/plandesign/backedsecurity/saveorupdate.do
                method: post
                data: xxx
            validator:
                isException: False
                isSuccess: True

        verify:
            desc: 验证-优先档-过手支付-算头不算尾-A365-固定
            request:
                url: /abswebapp/plandesign/backedsecurity/saveorupdate.do
                method: post
                data: xxx
            validator:
                isException: False
                isSuccess: True
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    # description content define: test_* and verify
    _LEN = 2

    # support zh_CN and en_US
    MODULE = re.compile(r'^AT_[\u4E00-\u9FA5A-Za-z0-9_]+\.yml$', re.IGNORECASE)
    DESCRIPTION = ['desc', 'request', 'validator']
    FORMAT = ['url', 'method', 'data']

    def __init__(self, path=None):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
        self._testCaseFile = path
        self.name = None
        self.params = None
        self.STRUCTURE = namedtuple('structure', [
            'project', 'test', 'preconditions', 'step', 'feature', 'story',
            'severity', 'name'
        ])

    @property
    def data(self):
        description = util.YmlReader(yaml_file=self._testCaseFile).data
        if isinstance(description, dict) and len(description) <= self._LEN:
            for key, value in description.items():
                for ele in self.DESCRIPTION:
                    if ele not in value:
                        raise CaseDescriptionError(self._testCaseFile)
            return description
        raise CaseDescriptionError(self._testCaseFile)

    def __bool__(self):
        # naming conventions check
        """
            project,
            feature,
            story,
            severity,
            api,
            preconditions,
            step,
            self.description.name
        """
        name = os.path.basename(self._testCaseFile)

        name_slice = slice(None, -4, None)
        feature_story_slice = slice(2, 4, None)
        step_slice = slice(4, None, None)

        if re.match(pattern=self.MODULE, string=name):
            try:
                name = name[name_slice].split('_')
                self.casename = os.path.basename(
                    self._testCaseFile).split('.')[0]
                self.STRUCTURE.feature, self.STRUCTURE.story = name[
                    feature_story_slice]
                self.STRUCTURE.severity = self._LEVEL.get(name[4])
                self.STRUCTURE.step = '-'.join(name[step_slice])
                self.STRUCTURE.test = list(self.data.keys())[0]
                self.STRUCTURE.name = self.casename
                preconditions = self.data[
                    self.STRUCTURE.test]['preconditions'] or None
                if preconditions:
                    self.STRUCTURE.preconditions = ', '.join(preconditions)
                self.params = {self.STRUCTURE.name: self.data}
            except IndexError:
                raise CaseNamingConventionsError(self._testCaseFile)
            except KeyError:
                raise CaseSeverityError(self._testCaseFile)
        return True if self.params else False

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=2)

    @staticmethod
    def send(step, parameters):
        return ABS.http(step=step, parameters=parameters)

    @staticmethod
    def parameters(script):
        return Api(script).data
    # @staticmethod
    # def run(name, parameters):
    #     m = AbsHttpClient()
    #     if not name:
    #         name = list(dict(parameters).keys())[0]
    #         parameters = parameters[name]
    #     if not step:
    #         parameters = parameters['verification']
    #     elif 'setup' in step:
    #         parameters = parameters[step]['setup']
    #     elif 'teardown' in step:
    #         parameters = parameters[step]['teardown']
    #     #: data
    #     request = parameters['request']
    #     validator = parameters['validator']
    #     #: request
    #     method = request['method']
    #     url = m.base_url + request['url']
    #     data = request['data'] if method == 'post' else None
    #     _params = request['data'] if method == 'get' else None
    #     headers = m._headers(request=request)
    #     files = request['files'] if 'files' in request else None
    #     #: parameters
    #     data = Pool.update(name=name, parameters=data)
    #     response = m.client.request(method=method,
    #                                 url=url,
    #                                 params=_params,
    #                                 data=data,
    #                                 headers=headers,
    #                                 files=files,
    #                                 timeout=m.timeout).json()
    #     Pool.save_step(name=name, step=step, response=response)
    #     return Verifier.check(validator, response=response)
