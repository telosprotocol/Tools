import os
import time

import websocket
import threading
import sys

sys.path.append('../')
import conftest

from api.mqueue import MQueue

log = conftest.get_my_logger(os.path.basename(__file__))


class WsLib(threading.Thread, MQueue):

    id = 0

    def __init__(self, url):
        MQueue.__init__(self)
        threading.Thread.__init__(self)
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
            # on_data=self.on_data
        )

    def send(self, data):
        log.info('post to ws >>> %s' % str(data))
        self.ws.send(data)

    def run(self):
        self.ws.run_forever()

    def on_message(self, msg):
        self.put(msg)

    def on_error(self, err):
        self.put(err)

    def on_close(self):
        self.put('down')

    # def on_data(self, data, *args):
    #     print 'data'
    #     self.put(data)

    def close_conn(self):
        self.ws.close()

    def get_id(self):
        self.id += 1
        return self.id


if __name__ == '__main__':
    ts1 = WsLib('ws://echo.websocket.org/')
    ts1.start()
    time.sleep(2)
    ts1.send('hello, this is ts1')
    time.sleep(2)
    print ts1.get()
    ts1.close_conn()
    print ts1.is_alive()

