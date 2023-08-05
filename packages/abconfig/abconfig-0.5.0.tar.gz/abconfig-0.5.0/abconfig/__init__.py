__version__ = '0.5.0'


from abconfig.common import Dict
from abconfig.file import File
from abconfig.env import Env


class ABConfig(Dict):
    plugins = None
    env = False
    file = None

    def __init__(self, data=None):
        if str(type(self).__name__) == 'ABConfig':
            raise NotImplementedError
        init = Dict(self._attrs() if not data else self._attrs(data))
        super().__init__(init(*self._loaders).get())

    @property
    def _loaders(self):
        result = []
        if self.plugins: result.extend(self.plugins)
        if self.file: result.append(File(self.file))
        if self.env is True: result.append(Env())
        return result

    def _attrs(self, **kwargs):
        result = {str(x): getattr(self, x) for x in type(self).__dict__.keys()
                                        if (x[:2] != '__' and
                                            x[:1] != '_' and
                                            x not in ('plugins','file', 'env'))}
        if kwargs: result.update(kwargs)
        return result
