import os
import conftest

log = conftest.get_my_logger(os.path.basename(__file__))


class AssertException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        log.error(self.value)
        return repr(self.value)


class MyAssert(object):

    @staticmethod
    def equal(ex, ac, extras=''):
        if isinstance(ex, basestring):
            if str(ac).encode('utf-8') == ex.encode('utf-8'):
                return
            else:
                raise AssertException('fail, except: ' + ex.encode('utf-8')
                                      + ', actual: ' + str(ac).encode('utf-8') + '. ' + extras)
        elif isinstance(ex, int):
            if int(ac) == ex:
                return
            else:
                raise AssertException('fail, except: ' + str(ex) + ', actual: ' + str(ac) + '. ' + extras)
        elif isinstance(ex, long):
            if long(ac) == ex:
                return
            else:
                raise AssertException('fail, except: ' + str(ex) + ', actual: ' + str(ac) + '. ' + extras)
        elif isinstance(ex, float):
            if float(ac) == ex:
                return
            else:
                raise AssertException('fail, except: ' + str(ex) + ', actual: ' + str(ac) + '. ' + extras)
        else:
            if ex == ac:
                return
            else:
                raise AssertException('fail, value type error.' + extras)

    @staticmethod
    def unequal(ex, ac, extras=''):
        if isinstance(ex, str):
            if str(ac) == ex:
                raise AssertException('fail, except: ' + str(ex) + 'the same as actual: ' + str(ac) + '. ' + extras)
            else:
                return
        elif isinstance(ex, int):
            if int(ac) == ex:
                raise AssertException('fail, except: ' + str(ex) + 'the same as actual: ' + str(ac) + '. ' + extras)
            else:
                return
        elif isinstance(ex, long):
            if long(ac) == ex:
                raise AssertException('fail, except: ' + str(ex) + 'the same as actual: ' + str(ac) + '. ' + extras)
            else:
                return
        elif isinstance(ex, float):
            if float(ac) == ex:
                raise AssertException('fail, except: ' + str(ex) + 'the same as actual: ' + str(ac) + '. ' + extras)
            else:
                return
        else:
            if ex == ac:
                raise AssertException('fail, value type error, but the same' + extras)
            else:
                return

    @staticmethod
    def contain(tree, leaf, extras=''):
        if isinstance(tree, list) or isinstance(tree, dict) or isinstance(tree, tuple) or isinstance(tree, set):
            if leaf in tree:
                return
            else:
                raise AssertException('fail, no contain. ' + extras)
        else:
            if leaf in tree:
                return
            else:
                raise AssertException('fail, value type err, and no contain.' + extras)

    @staticmethod
    def uncontain(tree, leaf, extras=''):
        if isinstance(tree, list) or isinstance(tree, dict) or isinstance(tree, tuple) or isinstance(tree, set):
            if leaf in tree:
                raise AssertException('fail, no contain. ' + extras)
            else:
                return
        else:
            if leaf in tree:
                raise AssertException('fail, value type err, but contain.' + extras)
            else:
                return

    @staticmethod
    def exist(ac, extras=""):
        if ac is not None:
            return
        else:
            raise AssertException('fail, actual is null. ' + extras)

    @staticmethod
    def inexist(ac, extras=""):
        if ac is None:
            raise AssertException('fail, actual is null. ' + extras)
        else:
            return


def mycheck(foo):
    def checker(*args, **kwargs):
        rsp = foo(*args, **kwargs)
        MyAssert.equal(1, rsp.json()['Result'], foo.__name__)
        return rsp
    return checker
