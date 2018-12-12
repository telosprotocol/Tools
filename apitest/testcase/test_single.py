# coding=utf-8
import base64
import json
import time
import sys
sys.path.append('../')

from api.LibApi import *
from api.TopApi import TopApi
import pytest

from api.TopAssert import MyAssert
from api.Unit import get_acc, fix_node_account

log = conftest.get_my_logger(os.path.basename(__file__))


@pytest.mark.usefixtures("laborer")
class TestSingle(object):
    god_account = {}
    top_1 = TopApi()
    top_2 = TopApi()
    top_3 = TopApi()

    @pytest.fixture(scope='class')
    def laborer(self):
        self.top_1.start()
        self.top_2.start()
        self.top_3.start()
        yield
        self.top_1.close_conn()
        self.top_2.close_conn()
        self.top_3.close_conn()

    def fix_god(self):
        self.god_account['account'] = get_acc('account_god', 'account')
        self.god_account['private_key'] = get_acc('account_god', 'private_key').decode('hex')
        self.god_account['last_hash'] = get_acc('account_god', 'last_hash')
        # signature = str(int(time.time()))

        signature = get_signature(self.god_account['private_key'], self.god_account['last_hash'])
        timestamp = int(time.time())
        rsp = self.top_1.get_last_hash(self.god_account['account'])
        last_hash = str(rsp['content'])
        self.god_account['last_hash'] = last_hash
        return signature

    @pytest.mark.single_info
    def test_account_info(self):
        log.info('create new user')
        balance = 1000000000
        stamp = int(time.time())
        private_key, top_account, account_hash, account_signature = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(top_account)

        log.info('login new user')
        stamp = int(time.time())
        self.top_1.login(top_account)

        stamp = int(time.time())
        rsp = self.top_1.get_balance(top_account)
        MyAssert.equal(balance, rsp['content'], 'check balance')

        stamp = int(time.time())
        rsp = self.top_1.get_last_hash(top_account)
        MyAssert.exist(rsp['content'], 'check hash')

        stamp = int(time.time())
        self.top_1.get_account_info(top_account)

        log.info('set alias')
        stamp = int(time.time())
        alias = 'test_alias'
        self.top_1.set_alias(top_account, alias)

        stamp = int(time.time())
        rsp = self.top_1.get_account_info(top_account)
        MyAssert.equal(alias, json.loads(rsp['content'])['alias'], 'check alias')

    @pytest.mark.single_property
    def test_property(self):
        log.info('create new user')
        balance = 1000000000
        stamp = int(time.time())
        private_key, top_account, account_hash, account_signature = fix_node_account(self.top_1.zone_shard, stamp)

        stamp = int(time.time())
        self.top_1.create_account(top_account)

        log.info('login new user')
        stamp = int(time.time())
        self.top_1.login(top_account)

        log.info('get user balance')
        stamp = int(time.time())
        rsp = self.top_1.get_balance(top_account)
        MyAssert.equal(balance, rsp['content'], 'check balance')

        log.info('create property')
        key = 'test_key'
        prop_type = 'string'
        stamp = int(time.time())
        self.top_1.create_property(top_account, key, prop_type)

        log.info('set property')
        value = 'test_value'
        set_dict = {
            'cmd': 'SET',
            'key': key,
            'value': value
        }
        stamp = int(time.time())
        self.top_1.set_property(top_account, set_dict)

        log.info('get property')
        set_dict = {
            'cmd': 'GET',
            'account': top_account,
            'key': key,
        }
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal(value, rsp['content'], 'check property')

        # list
        log.info('create list type property')
        key = 'test_list_type_key'
        prop_type = 'list'
        stamp = int(time.time())
        self.top_1.create_property(top_account, key, prop_type)

        # left push
        log.info('left push list type property')
        first_value = 'test_left_push_value0'
        set_dict = {
            'cmd': 'LPUSH',
            'key': key,
            'value': first_value
        }
        stamp = int(time.time())
        self.top_1.set_property(top_account, set_dict)

        # right push
        log.info('right push list type property')
        second_value = 'test_right_push_value1'
        set_dict = {
            'cmd': 'RPUSH',
            'key': key,
            'value': second_value
        }
        stamp = int(time.time())
        self.top_1.set_property(top_account, set_dict)

        # length
        log.info('get len of list type property')
        set_dict = {
            'cmd': 'LLEN',
            'key': key,
            'account': top_account
        }
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal(2, rsp['content'], 'check property')

        # assert
        log.info('test exists of list type property')
        set_dict = {
            'cmd': 'LEXISTS',
            'key': key,
            'value': first_value
        }
        index = 0
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal(index, rsp['content'], 'check property')

        # assert
        log.info('test exists of list type property')
        set_dict = {
            'cmd': 'LEXISTS',
            'key': key,
            'value': second_value
        }
        index = 1
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal(index, rsp['content'], 'check property')

        # assert
        log.info('test exists of list type property')
        set_dict = {
            'cmd': 'LEXISTS',
            'key': key,
            'value': 'not_exist_value'
        }
        index = -1
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal(index, rsp['content'], 'check property')

        # get data
        log.info('get list type property by range')
        set_dict = {
            'cmd': 'LRANGE',
            'key': key,
            'start': 0,
            'end': 1
        }
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal([first_value, second_value], rsp['content'], 'check property')

        # remove spec
        # del exist property
        log.info('remove list type property')
        set_dict = {
            'cmd': 'LREM',
            'key': key,
            'value': first_value
        }
        stamp = int(time.time())
        self.top_1.set_property(top_account, set_dict)

        # get property
        log.info('get property by range after lrem exists val')
        set_dict = {
            'cmd': 'LRANGE',
            'key': key,
            'start': 0,
            'end': -1
        }
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal([second_value], rsp['content'], 'check property')

        # del not exist property
        log.info('remove list type property')
        value = 'test_rem_not_exists_value'
        set_dict = {
            'cmd': 'LREM',
            'key': key,
            'value': value
        }
        stamp = int(time.time())
        self.top_1.set_property(top_account, set_dict)

        # get property
        log.info('get property by range after lrem not exists val')
        set_dict = {
            'cmd': 'LRANGE',
            'key': key,
            'start': 0,
            'end': -1
        }
        stamp = int(time.time())
        rsp = self.top_1.get_property(top_account, set_dict)
        MyAssert.equal([second_value], rsp['content'], 'check property')

    @pytest.mark.single_gold_transfer
    def test_single_gold_transfer(self):
        signature = self.fix_god()

        stamp = int(time.time())
        log.info('login god')
        self.top_1.login(self.god_account['account'], base64.b64encode(signature), stamp, god=True)

        log.info('get god balance')
        rsp = self.top_1.get_balance(self.god_account['account'], base64.b64encode(signature), stamp, god=True)
        god_balance_1 = float(rsp['content'])

        log.info('create user')
        stamp = int(time.time())
        balance = 1000000000
        private_key, top_account, account_hash, account_signature = fix_node_account(self.top_2.zone_shard, stamp)

        log.info('user account: %s' % str(top_account))
        self.top_2.create_account(top_account)

        log.info('login new usr')
        stamp = int(time.time())
        self.top_2.login(top_account)

        log.info('get user balance')
        rsp = self.top_2.get_balance(top_account)
        balance_1 = float(rsp['content'])
        MyAssert.equal(balance, balance_1, 'checkout new account balance')

        log.info('transfer from god to user')
        transfer_amount = 1
        stamp = int(time.time())
        god_out_hash = top_transfer(self.god_account['account'], top_account, str(transfer_amount),
                                    self.god_account['last_hash'], stamp)
        god_out_signature = get_signature(self.god_account['private_key'], god_out_hash)

        self.top_1.transfer(self.god_account['account'], top_account, str(transfer_amount),
                            base64.b64encode(self.god_account['last_hash']),
                            base64.b64encode(god_out_hash), base64.b64encode(god_out_signature), stamp, god=True)

        log.info('get god balance')
        rsp = self.top_1.get_balance(self.god_account['account'], base64.b64encode(signature), stamp, god=True)
        god_balance_2 = float(rsp['content'])

        MyAssert.equal(god_balance_2, god_balance_1 - transfer_amount, 'check god balance')

        log.info('wait for transfer in')
        time.sleep(3)

        rsp = self.top_2.get()
        log.info(rsp)
        notify_1 = json.loads(rsp)
        content = json.loads(notify_1['content'])
        MyAssert.equal(1, content['amount'])

    @pytest.mark.single_subscribe
    def test_single_subscribe(self):
        log.info('subscribe')
        # sub
        log.info('create new user1')
        balance = 1000000000
        stamp = int(time.time())
        private_key1, top_account1, account_hash1, account_signature1 = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(top_account1)

        log.info('login new user1')
        stamp = int(time.time())
        self.top_1.login(top_account1)

        log.info('create new user2')
        stamp = int(time.time())
        private_key2, top_account2, account_hash2, account_signature2 = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(top_account2)

        log.info('login new user2')
        stamp = int(time.time())
        self.top_1.login(top_account2)

        self.top_1.subscribe(top_account2, top_account1)

        msg = "test notification hello"
        set_dict = {
            "receiver": top_account2,
            "message": msg
        }
        self.top_1.notify(top_account1, set_dict)

        log.info('wait for notification')
        time.sleep(3)
        rsp = self.top_1.get()
        log.info(rsp)
        notify_1 = json.loads(rsp)
        content = json.loads(notify_1['content'])
        MyAssert.equal(msg, content['notification'], 'check notification')

        self.top_1.unsubscribe(top_account2, top_account1)

    @pytest.mark.single_combo_flow
    def test_combo_flow(self):
        log.info('create new sender user')
        stamp = int(time.time())
        init_balance_s = 1000000000
        private_key_s, top_account_s, account_hash_s, account_signature_s = fix_node_account(self.top_1.zone_shard,
                                                                                             stamp)

        # create_user
        self.top_1.create_account(top_account_s)

        log.info('login new sender')
        self.top_1.login(top_account_s)

        log.info('get user balance')
        rsp = self.top_1.get_balance(top_account_s)
        balance_1_s = float(rsp['content'])
        MyAssert.equal(init_balance_s, balance_1_s, 'checkout new account balance')

        log.info('create property')
        key = 'test_key'
        prop_type = 'string'
        self.top_1.create_property(top_account_s, key, prop_type)

        log.info('set property')
        value = 'test_value'
        set_dict = {
            'cmd': 'SET',
            'key': key,
            'value': value
        }
        self.top_1.set_property(top_account_s, set_dict)

        log.info('get property')
        set_dict = {
            'cmd': 'GET',
            'account': top_account_s,
            'key': key,
        }
        rsp = self.top_1.get_property(top_account_s, set_dict)
        MyAssert.equal(value, rsp['content'], 'check property')

        log.info('create new receiver user')
        stamp = int(time.time())
        init_balance_r = 1000000000
        private_key_r, top_account_r, account_hash_r, account_signature_r = fix_node_account(self.top_2.zone_shard,
                                                                                             stamp)

        self.top_2.create_account(top_account_r)

        log.info('login new receiver')
        self.top_2.login(top_account_r)

        log.info('get user balance')
        rsp = self.top_2.get_balance(top_account_r)
        balance_1_r = float(rsp['content'])
        MyAssert.equal(init_balance_r, balance_1_r, 'checkout new account balance')

        log.info('create property')
        key = 'test_key'
        prop_type = 'string'
        self.top_2.create_property(top_account_r, key, prop_type)

        log.info('set property')
        value = 'test_value'
        set_dict = {
            'cmd': 'SET',
            'value': value,
            'key': key,
        }
        self.top_2.set_property(top_account_r, set_dict)

        log.info('get property')
        set_dict = {
            'cmd': 'GET',
            'account': top_account_r,
            'key': key,
        }
        rsp = self.top_2.get_property(top_account_s, set_dict)
        MyAssert.equal(value, rsp['content'], 'check property')

        log.info('transfer from sender to receiver')
        transfer_amount = 1

        stamp = int(time.time())
        rsp = self.top_1.get_last_hash(top_account_s)
        MyAssert.exist(rsp['content'], 'check hash')
        property_hash_s = rsp['content']
        log.info('property_hash_s: %s' % type(property_hash_s))
        out_hash = top_transfer(top_account_s, top_account_r, str(transfer_amount), str(property_hash_s), stamp)
        out_signature = get_signature(private_key_s, out_hash)
        self.top_1.transfer(top_account_s, top_account_r, str(transfer_amount), base64.b64encode(property_hash_s),
                            base64.b64encode(out_signature))

        log.info('get send balance')
        rsp = self.top_1.get_balance(top_account_s)
        balance_2_s = float(rsp['content'])

        MyAssert.equal(balance_2_s, balance_1_s - transfer_amount, 'check send balance')

        log.info('wait for transfer in')
        time.sleep(3)

        notify_1 = json.loads(self.top_2.get())
        content = json.loads(notify_1['content'])
        MyAssert.equal(1, content['amount'])

        log.info('get receiver balance')
        rsp = self.top_2.get_balance(top_account_r)
        balance_2_r = float(rsp['content'])

        MyAssert.equal(transfer_amount, balance_2_r - balance_1_r, 'check receiver balance')

    @pytest.mark.single_continue_out
    def test_continue_out(self):
        log.info('create nf')
        stamp = int(time.time())
        nf_key, nf_account, nf_hash, nf_signature = fix_node_account(self.top_1.zone_shard, stamp)

        log.info('check nf account: %s' % str(nf_account))
        self.top_1.create_account(nf_account)

        log.info('get nf balance')
        rsp = self.top_1.get_balance(nf_account)
        nf_balance_1 = float(rsp['content'])

        log.info('login nf sender')
        self.top_1.login(nf_account)

        log.info('create mid')
        stamp = int(time.time())
        mid_key, mid_account, mid_hash, mid_signature = fix_node_account(self.top_2.zone_shard, stamp)

        log.info('check mid account: %s' % str(mid_account))
        self.top_2.create_account(mid_account)

        log.info('login mid account')
        self.top_2.login(mid_account)

        log.info('get mid balance')
        rsp = self.top_2.get_balance(mid_account)
        mid_balance_1 = float(rsp['content'])

        log.info('create receiver')
        stamp = int(time.time())
        nt_key, nt_account, nt_hash, nt_signature = fix_node_account(self.top_3.zone_shard, stamp)

        self.top_3.create_account(nt_account)

        log.info('login nt receiver')
        self.top_3.login(nt_account)

        log.info('get nt balance')
        rsp = self.top_3.get_balance(nt_account)
        nt_balance_1 = float(rsp['content'])

        stamp = int(time.time())
        rsp = self.top_1.get_last_hash(nf_account)
        MyAssert.exist(rsp['content'], 'check hash')
        last_hash = rsp['content']

        log.info('transfer from nf to mid')
        transfer_amount_1 = 1
        stamp = int(time.time())
        to_mid_hash = top_transfer(nf_account, mid_account, str(transfer_amount_1), nf_hash, stamp)
        to_mid_signature = get_signature(nf_key, to_mid_hash)
        self.top_1.transfer(nf_account, mid_account, str(transfer_amount_1), str(last_hash),
                            base64.b64encode(to_mid_hash))

        log.info('get nf balance')
        rsp = self.top_1.get_balance(nf_account)
        nf_balance_2 = float(rsp['content'])
        MyAssert.equal(nf_balance_2, nf_balance_1 - transfer_amount_1, 'check nf balance')

        log.info('wait for transfer in')
        time.sleep(3)

        notify_1 = json.loads(self.top_2.get())
        content = json.loads(notify_1['content'])
        MyAssert.equal(1, content['amount'])

        log.info('get mid balance')
        rsp = self.top_2.get_balance(mid_account)
        mid_balance_2 = float(rsp['content'])

        MyAssert.equal(transfer_amount_1, mid_balance_2 - mid_balance_1, 'check mid balance')

        log.info('transfer from mid to nt')
        rsp_hash = self.top_2.get_last_hash(mid_account)
        mid_in_hash = rsp_hash['content']
        transfer_amount_2 = int(mid_balance_2)

        stamp = int(time.time())
        to_nt_hash = top_transfer(mid_account, nt_account, str(transfer_amount_2), str(mid_in_hash), stamp)
        to_nt_signature = get_signature(mid_key, to_nt_hash)
        self.top_2.transfer(mid_account, nt_account, str(transfer_amount_2), str(mid_in_hash),
                            base64.b64encode(to_nt_hash))

        log.info('get mid balance')
        rsp = self.top_2.get_balance(mid_account)
        mid_balance_3 = float(rsp['content'])

        MyAssert.equal(0, mid_balance_3, 'check mid balance')

        log.info('wait for transfer in')
        time.sleep(3)

        notify_1 = json.loads(self.top_3.get())
        content = json.loads(notify_1['content'])
        MyAssert.equal(transfer_amount_2, content['amount'])

        log.info('get nt balance')
        rsp = self.top_3.get_balance(nt_account)
        nt_balance_2 = float(rsp['content'])

        MyAssert.equal(nt_balance_1 + transfer_amount_2, nt_balance_2, 'check nt balance')

