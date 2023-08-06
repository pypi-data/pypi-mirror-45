import copy
import hashlib
import requests
from .result import Pool, Verifier
from .util import ConfigHandler


def rsuit(testspath):
    pass
    # factory.Generator.scripts()
    # os.chdir(factory.SCRIPT_DIR)
    # os.system(factory.CMD_EXEC_PYTEST_ALLURE)
    # os.chdir(factory.REPORT_DIR)
    # os.system(factory.CMD_ALLURE_GENERATE)


class ABS:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, path):
        gofers = ConfigHandler(path).cfg
        env = gofers['env']
        http = gofers['http']
        self.base_url = 'http://%s:%s/%s' % (env['server'], env['port'],
                                             env['project'])
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
        login_usr_info = dict(userName=user,
                              password=md5_password,
                              ADPassword=password)
        try:
            m = requests.session()
            m.request(method='post',
                      url=self.base_url + login,
                      data=login_usr_info)
            return m if m else None
        except Exception:
            raise ConnectionRefusedError('url: %s\n user info: %s' %
                                         (self.base_url, login_usr_info))

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
        response = self.client.request(method=method,
                                       url=url,
                                       params=_params,
                                       data=data,
                                       headers=headers,
                                       files=files,
                                       timeout=self.timeout).json()
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
        response = self.client.request(method=method,
                                       url=url,
                                       params=_params,
                                       data=data,
                                       headers=headers,
                                       files=files,
                                       timeout=self.timeout).json()
        Pool.save_step(name=name, step=step, response=response)
        Verifier.check(validator, response=response)
        return response


ABS = ABS()
