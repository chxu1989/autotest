# encoding:utf-8
# python常量类

import sys

class _const:
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            raise self.ConstError("Can't rebind const (%s)" % name)
        if not name.isupper():
            raise self.ConstCaseError("Const variable must be combined with upper letters:'%s'" % name)
        self.__dict__[name] = value


sys.modules[__name__] = _const()
