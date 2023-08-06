from six import with_metaclass


class EnumBaseMeta(type):

    def __new__(mcs, clsname, bases, classdict):
        mcs = super(EnumBaseMeta, mcs).__new__(mcs, clsname, bases, classdict)
        d = {}
        for base in reversed(mcs.__bases__):
            if hasattr(base, 'NAME_TO_VALUE'):
                d.update(base.NAME_TO_VALUE)

        classdict.pop('MIN_VALUE', None)
        classdict.pop('MAX_VALUE', None)
        d.update((n, v) for n, v in classdict.items() if not n.startswith('__') and not callable(v) and not isinstance(v, (classmethod, staticmethod, dict)))
        type.__setattr__(mcs, 'NAME_TO_VALUE', d)
        type.__setattr__(mcs, 'VALUE_TO_NAME', {v:k for k, v in d.items()})
        if d:
            type.__setattr__(mcs, 'MIN_VALUE', min(d.values()))
            type.__setattr__(mcs, 'MAX_VALUE', max(d.values()))
        return mcs


class EnumBase(with_metaclass(EnumBaseMeta)):
    NAME_TO_VALUE = {}
    VALUE_TO_NAME = {}
    MIN_VALUE = 0
    MAX_VALUE = 0

    @classmethod
    def get_name(cls, value):
        return cls.VALUE_TO_NAME.get(value)

    @classmethod
    def get_value(cls, name):
        return cls.NAME_TO_VALUE.get(name)
