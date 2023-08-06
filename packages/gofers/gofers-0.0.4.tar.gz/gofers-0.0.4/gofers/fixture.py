import json
from .util import YmlReader
from .runner import ABS
from .util import PathHandler


class Fixture:
    def __init__(self, path):
        # base info
        self.yml = PathHandler.get_yml_by_script(script=path)
        self.description = YmlReader(yaml_file=self.yml)
        self.name = self.description.name
        self.data = self.description.data or FileExistsError(
            'Un support test description file: %s' % self.yml)
        self.names = list(self.data.keys())

    def __bool__(self):
        return True if 'conftest' in self.yml else False

    def __str__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=2)

    @staticmethod
    def send(step, request, parameters):
        parameter_table = parameters[step]
        parameter_setup = parameter_table[
            'setup'] if 'setup' in parameter_table else None
        parameter_teardown = parameter_table[
            'teardown'] if 'teardown' in parameter_table else None
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
