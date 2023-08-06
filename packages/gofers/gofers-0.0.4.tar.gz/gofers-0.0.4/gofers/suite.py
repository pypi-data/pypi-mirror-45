# Minimum folder under a fixed path
import os


class Repository:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, path):
        self.repository = []
        self.root_path = path

    @property
    def yml(self):
        for root, dirs, files in os.walk(top=self.root_path, topdown=False):
            for file in files:
                yml = os.path.join(root, file)
                if os.path.isfile(yml):
                    self.repository.append(yml)
        return self.repository
