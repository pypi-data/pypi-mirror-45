from os import environ


class Env:
    def __call__(self, data, prefix=None):
        result = dict()
        update = lambda k, v: result.update({k:v}) if v else None
        for k,v in data.items():
            if isinstance(v, dict):
                update(k, self(v, self._get_prefix(prefix,k)))
            else:
                update(k,self._get_env(prefix,k))
        return result

    def _get_env(self, prefix, name):
        env_name = self._get_prefix(prefix, name)
        return environ.get(env_name.upper(), None)

    def _get_prefix(self, *args):
        clean = lambda x: True if x else False
        return '_'.join(filter(clean, args))
