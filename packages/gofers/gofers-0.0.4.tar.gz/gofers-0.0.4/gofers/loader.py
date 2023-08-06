import os
import shutil
from .case import Api
from .fixture import Fixture
from .util import ConfigHandler, PathHandler
from .suite import Repository


PROFILE_CASE = """#!/usr/local/python3.7.3
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
    Fixture.send(step='{FIXTURE_NAME}', request, parameters_table)
"""


class Generator:
    @staticmethod
    def _script_content(case, yml):
        project = ConfigHandler(path=yml).cfg['env']['project']
        feature = case.STRUCTURE.feature
        story = case.STRUCTURE.story
        severity = case.STRUCTURE.severity
        test = case.STRUCTURE.test
        preconditions = case.STRUCTURE.preconditions
        step = case.STRUCTURE.step
        name = case.STRUCTURE.name

        script = PROFILE_CASE.format(PROJECT=project,
                                     FLAG_FEATURE=feature,
                                     FLAG_STORY=story,
                                     FLAG_SEVERITY=severity,
                                     TEST_STEP=test,
                                     PRECONDITIONS=preconditions,
                                     FLAG_STEP=step,
                                     SCRIPT_NAME=name)
        return script

    @staticmethod
    def _fixture_content(fixture, yml):
        _fixtures = ''
        names = fixture.names
        for name in names:
            _fixtures += PROFILE_FIXTURE_BODY.format(FIXTURE_NAME=name)
        return PROFILE_FIXTURE_HEADER + _fixtures

    @staticmethod
    def generate(yml):
        name = PathHandler.get_script_by_yml(yml)
        if os.path.exists(name):
            os.remove(name)
        dirs = os.path.dirname(name)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(name, 'ab') as s:
            case = Api(path=yml)
            fixture = Fixture(path=yml)
            if case:
                contents = Generator._script_content(case, yml)
                s.write(contents.encode('utf-8'))
            elif fixture:
                contents = Generator._fixture_content(fixture, yml)
                s.write(contents.encode('utf-8'))

    @staticmethod
    def scripts(path):
        if 'case' in path:
            path = PathHandler.get_scriptp_by_ymlp(path)
        Generator.clear(path)
        yml_list = Repository(path).yml
        for yml in yml_list:
            Generator.generate(yml)

    @staticmethod
    def clear(path):
        if 'script' in path:
            if os.path.exists(path):
                shutil.rmtree(path)
