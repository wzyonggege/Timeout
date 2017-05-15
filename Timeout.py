# coding=utf-8
from threading import Thread

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TimeoutException(Exception):
    pass

ThreadStop = Thread._Thread__stop   # 获取私有函数

def timeout(second):
    def decorator(function):
        def decorator2(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self, _error= None, ):
                    Thread.__init__(self)
                    self._error = _error

                def run(self):
                    try:
                        self.result = function(*args, **kwargs)
                    except Exception, e:
                        self._error = e

                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)

            t = TimeLimited()
            t.start()
            t.join(second)

            if isinstance(t._error, TimeoutException):
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t.isAlive():
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t._error is None:
                return t.result

        return decorator2
    return decorator


@timeout(5)
# 限定下面的slowfunc函数如果在5s内不返回就强制抛TimeoutError Exception结束
def slowfunc(sleep_time):
    a = 1
    import time
    time.sleep(sleep_time)
    return a


if __name__ == '__main__':
    print slowfunc(5.0)
