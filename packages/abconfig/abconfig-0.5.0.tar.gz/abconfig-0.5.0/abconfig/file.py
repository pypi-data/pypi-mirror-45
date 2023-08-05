import yaml
import json

from os import path as fpath
from abconfig.common import Cached


class BaseFormat:
    @staticmethod
    def reader(file):
        raise NotImplementedError

    @classmethod
    def read(cls, path):
        with open(path, 'r') as file:
            read = cls.reader(file)
            if not isinstance(read, dict):
                raise IOError('Not valid file format')
            return read


class Yaml(BaseFormat):
    @staticmethod
    def reader(file):
        return yaml.load(file, Loader=yaml.FullLoader)


class Json(BaseFormat):
    @staticmethod
    def reader(file):
        return json.load(file)


class File(Cached):
    formats = (Yaml, Json)

    def __init__(self, path):
        self.path = self.isexists(path)

    def isexists(self, path):
        if fpath.exists(path) is False:
            raise FileNotFoundError(f'{path} not found')
        return path

    def __call__(self, data=None):
        errors = list()
        for reader in self.formats:
            try:
                return reader.read(self.path)
            except Exception as e:
                errors.append(f'{reader.__name__} reader: {e}')
                continue
        error_message = '\n'.join(errors)
        raise IOError(f'{self.path} read error:\n{error_message}')
