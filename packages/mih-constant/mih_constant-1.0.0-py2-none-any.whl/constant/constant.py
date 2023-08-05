# encoding: utf-8

class METACONSTANT(type):
    def __getattr__(cls, key):
        return cls[key]

    def __setattr__(cls, key, value):
        raise TypeError("constant variable %s can't be reassigned!" % key)


class CONSTANT(object):
    __metaclass__ = METACONSTANT

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        raise TypeError("constant variable %s can't be reassigned!" % name)
