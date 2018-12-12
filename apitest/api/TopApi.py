import json
import os
import sys

sys.path.append('../')

import conftest
from api.TopAssert import mycheck
from api.Unit import get_init
from api.websocketlib import WsLib

log = conftest.get_my_logger(os.path.basename(__file__))


class TopApi(WsLib):

    def __init__(self):
        self.ws_url, self.zone_shard = get_init()
        log.info('ws_url --> %s' % self.ws_url)
        super(TopApi, self).__init__(self.ws_url)

    def get_notify(self, timeout=15):
        notify = self.get(timeout)
        log.info('get notify: %s' % notify)
        return notify

    @mycheck
    def create_account(self, top_account, top_signature, stamp, content=''):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'account_create',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': content,
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def login(self, top_account, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'login',
            'account': top_account,
            'signature': top_signature,
            'timestamp': stamp,
            'content': ''
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def get_balance(self, top_account, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'account_balance',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': ''
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def get_last_hash(self, top_account, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'last_digest',
            'account': top_account,
            'signature': top_signature,
            'timestamp': stamp,
            'content': ''
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def get_account_info(self, top_account, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'account_info',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': ''
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def transfer(self, top_account, top_destination, top_amount, top_last_digest, top_digest, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'transfer',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': {
                'destination': top_destination,
                'last_digest': top_last_digest,
                'digest': top_digest,
                'amount': top_amount,
                'comment': ''
            }
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def get_account_history(self, top_account, count=0, page=1):
        data = {'action': 'account_history',
                'account': top_account,
                'count': count,
                'per_page': page
                }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = json.loads(self.get())
        return rsp

    def get_tps(self):
        pass

    @mycheck
    def create_property(self, top_account, key, prop_type, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'create_prop',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': {
                'name': key,
                'type': prop_type
            }
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def set_property(self, top_account, cmd, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'set_prop',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': cmd
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def get_property(self, top_account, content, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'get_prop',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': content
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    # @mycheck
    # def get_all_property(self, top_account):
    #     data = {'action': 'query_all_property', 'account': top_account}
    #     d_json = json.dumps(data)
    #     self.send(d_json)
    #     rsp = json.loads(self.get())
    #     return rsp

    def get_online(self):
        pass

    @mycheck
    def notify(self, top_account, cmd, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'send_notification',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': cmd
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def subscribe(self, top_account, cmd, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'subscribe_notification',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': cmd
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def unsubscribe(self, top_account, cmd, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'unsubscribe_notification',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': cmd
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def set_alias(self, top_account, cmd, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'set_alias',
            'account': top_account,
            'timestamp': stamp,
            'signature': top_signature,
            'content': cmd
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def publish_contract(self, top_account, script, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'publish_contract',
            'timestamp': stamp,
            'account': top_account,
            'signature': top_signature,
            'content': script
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp

    @mycheck
    def exec_contract(self, top_account, exec_params, top_signature, stamp):
        data = {
            'msg_id': self.get_id(),
            'type': 'request',
            'action': 'exec_contract',
            'timestamp': stamp,
            'account': top_account,
            'signature': top_signature,
            'content': exec_params
        }
        d_json = json.dumps(data)
        self.send(d_json)
        rsp = self.get()
        rsp = json.loads(rsp) if rsp else None
        return rsp