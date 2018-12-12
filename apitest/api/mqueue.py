import Queue
import threading


class MQueue:

    def __init__(self):
        self.__mq = Queue.Queue()
        self.__lock = threading.Lock()
        self.__cond = threading.Condition(self.__lock)

    def put(self, obj):
        if self.__cond.acquire():
            self.__mq.put(obj)
            self.__cond.notify()
            self.__cond.release()

    def get(self, timeout=15):
        if self.__cond.acquire():
            if self.__mq.empty():
                self.__cond.wait(timeout)
            if self.__mq.empty():
                self.__cond.notify()
                self.__cond.release()
                raise Exception('timeout!')
            item = self.__mq.get()
            self.__cond.notify()
            self.__cond.release()
            return item
        raise Exception('mq lock!')

    def get_all(self, timeout=15):
        tmp = []
        if self.__cond.acquire():
            if self.__mq.empty():
                self.__cond.wait(timeout)
            if self.__mq.empty():
                self.__cond.notify()
                self.__cond.release()
                return None
            for i in xrange(self.__mq.qsize()):
                tmp.append(self.__mq.get())
            self.__cond.notify()
            self.__cond.release()
            return tmp
        return None

    def clear(self):
        if self.__cond.acquire():
            self.__mq.queue.clear()
            self.__cond.notify()
            self.__cond.release()


if __name__ == '__main__':
    q = MQueue()
    # q.put('123')
    print q.get()