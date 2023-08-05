from copy import deepcopy


class Dict(dict):
    def __str__(self):
        return type(self).__name__

    def __init__(self, data=None):
        self._data = data if data else dict()

    def get(self, item=None, default=None):
        if not item:
            return self._data
        if not item in self._data:
            return default
        return self._data[item]

    def items(self):
        return self._data.items()

    def __getitem__(self, item):
        return self.get(item)

    def __add__(self, *args):
        return self._add(*args)

    def __iadd__(self, *args):
        return self._add(*args)

    def _add(self, data: dict):
        result = deepcopy(self._data)
        for k,v in self._data.items():
            v2 = data.get(k, None)
            if v2: result.update(
                {k: self._merge(k,v,v2)})
            elif not v2 and isinstance(v, type):
                result.update({k: None})
        return Dict(result)

    def _merge(self, k, source, item):
        istype = False
        eq = lambda x, y: isinstance(x, y)
        if not source or isinstance(source, type):
            eq = lambda x, y: x is y
            istype = True

        converter = (source if isinstance(source, type) else
                     (type(source) if source else lambda x: x))

        eqt = lambda x: eq(source, x)
        error = lambda: self._type_error(k,
            type(converter).__name__ if not istype else converter)

        if eqt(tuple) or eqt(list):
            if eq(item, converter): error()
            return converter(item)
        elif eqt(dict):
            if not isinstance(item, dict): error()
            return (Dict(source) + Dict(item)).get()
        return converter(item)

    def _type_error(self, k, need_type):
        raise TypeError(f'{k} value must be {need_type.__name__}')

    def __call__(self, *args):
        result = deepcopy(self)
        for func in args: result += func(result.get())
        return result


class Cache(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if not args[0] in cls.instances:
            cls.instances[args[0]] = super(Cache, cls).__call__(*args, **kwargs)
        return cls.instances[args[0]]


class Cached(metaclass=Cache):
    """ Created once and stored in the Cache.instances dictionary,
        first positional arg is unique object id to be created
    """