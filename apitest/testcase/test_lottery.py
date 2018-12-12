# coding=utf-8
import json
import time
import sys
sys.path.append('../')

from api.LibApi import *
from api.TopApi import TopApi
import pytest

from api.TopAssert import MyAssert
from api.Unit import fix_node_account, get_lottery_contract, init_lottery, buy_lottery, draw_lottery, get_prop_tmp

log = conftest.get_my_logger(os.path.basename(__file__))


@pytest.mark.usefixtures("laborer")
class TestLottery(object):
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

    @pytest.mark.lottery_smoke
    def test_lottery_smoke(self):
        log.info('create master')
        stamp = int(time.time())
        key_master, account_master, hash_master_1, sign_master = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_master)

        log.info('login master')
        self.top_1.login(account_master)

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_1 = int(rsp['content'])

        log.info('create contract user')
        stamp = int(time.time())
        con_create = {'type': 'smart_contract'}
        key_smart, account_smart, hash_smart, sign_smart = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_smart, content=con_create)

        log.info('publish contract')
        probability = 1
        lottery_amount = 10000
        script = get_lottery_contract(account_master, hash_master_1, account_smart, lottery_amount, probability)
        self.top_1.publish_contract(account_smart, script)

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_1 = int(rsp['content'])

        MyAssert.equal(lottery_amount, smart_balance_1, 'check smart balance')

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_2 = int(rsp['content'])

        MyAssert.equal(master_balance_1 - smart_balance_1, master_balance_2, 'check master balance')

        log.info('init lottery')
        init_param = init_lottery(account_smart)
        self.top_1.exec_contract(account_smart, init_param)

        log.info('get master hash')
        rsp = self.top_1.get_last_hash(account_master)
        hash_master_2 = rsp['content']

        log.info('master buy lottery')
        buy_amount_1 = 1000
        buy_param = buy_lottery(account_master, hash_master_2, buy_amount_1, account_smart)
        self.top_1.exec_contract(account_master, buy_param)

        log.info('draw lottery')
        draw_param = draw_lottery(account_smart)
        self.top_1.exec_contract(account_smart, draw_param)

        log.info('notify win')

        notify = json.loads(self.top_1.get_notify())
        con_notify = json.loads(notify['content'])
        win_amount = int(con_notify['amount'])
        MyAssert.equal('transfer', notify['action'], 'check notify action')
        MyAssert.equal(account_master, notify['account'], 'check notify account')
        MyAssert.equal(account_smart, con_notify['sender'], 'check notify smart account')

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_3 = int(rsp['content'])

        MyAssert.equal(master_balance_2 + win_amount - buy_amount_1, master_balance_3, 'check master balance')

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_2 = int(rsp['content'])

        MyAssert.equal(0, smart_balance_2, 'check smart balance')

        log.info('get master hash')
        rsp = self.top_1.get_last_hash(account_master)
        hash_master_3 = rsp['content']

        log.info('master buy lottery 2')
        buy_amount_1 = 1000
        buy_param = buy_lottery(account_master, hash_master_3, buy_amount_1, account_smart)
        self.top_1.exec_contract(account_master, buy_param, res=0)

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_4 = int(rsp['content'])

        MyAssert.equal(master_balance_3, master_balance_4, 'check master balance')

    @pytest.mark.lottery_flow
    def test_lottery_flow(self):
        log.info('create master')
        stamp = int(time.time())
        key_master, account_master, hash_master_1, sign_master = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_master)

        log.info('login master')
        self.top_1.login(account_master)

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_1 = int(rsp['content'])

        log.info('create contract user')
        stamp = int(time.time())
        con_create = {'type': 'smart_contract'}
        key_smart, account_smart, hash_smart, sign_smart = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_smart, content=con_create)

        log.info('publish contract')
        probability = 1
        lottery_amount = 10000
        script = get_lottery_contract(account_master, hash_master_1, account_smart, lottery_amount, probability)
        self.top_1.publish_contract(account_smart, script)

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_1 = int(rsp['content'])

        MyAssert.equal(lottery_amount, smart_balance_1, 'check smart balance')

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_2 = int(rsp['content'])

        MyAssert.equal(master_balance_1 - smart_balance_1, master_balance_2, 'check master balance')

        log.info('init lottery 1')
        init_param = init_lottery(account_smart)
        self.top_1.exec_contract(account_smart, init_param)

        log.info('draw lottery 1')
        draw_param = draw_lottery(account_smart)
        self.top_1.exec_contract(account_smart, draw_param)

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_2 = int(rsp['content'])

        MyAssert.equal(smart_balance_1, smart_balance_2, 'check smart balance')

        log.info('init lottery 2')
        init_param = init_lottery(account_smart)
        self.top_1.exec_contract(account_smart, init_param)

        log.info('create actor 1')
        stamp = int(time.time())
        key_actor_1, account_actor_1, hash_actor_1, sign_actor_1 = fix_node_account(self.top_2.zone_shard, stamp)
        self.top_2.create_account(account_actor_1)

        log.info('login actor 1')
        self.top_2.login(account_actor_1)

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_1 = int(rsp['content'])

        log.info('actor 1 buy lottery')
        buy_amount_2 = 1000
        buy_param = buy_lottery(account_actor_1, hash_actor_1, buy_amount_2, account_smart)
        self.top_2.exec_contract(account_actor_1, buy_param)

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_2 = int(rsp['content'])

        MyAssert.equal(actor_1_balance_1 - buy_amount_2, actor_1_balance_2, 'check actor 1 balance')

        log.info('draw lottery 2')
        draw_param = draw_lottery(account_smart)
        self.top_1.exec_contract(account_smart, draw_param)

        log.info('notify win')

        notify = json.loads(self.top_2.get_notify())
        con_notify = json.loads(notify['content'])
        win_amount = int(con_notify['amount'])
        MyAssert.equal('transfer', notify['action'], 'check notify action')
        MyAssert.equal(account_actor_1, notify['account'], 'check notify account')
        MyAssert.equal(account_smart, con_notify['sender'], 'check notify smart account')

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_3 = int(rsp['content'])

        MyAssert.equal(actor_1_balance_2 + win_amount, actor_1_balance_3, 'check actor 1 balance')

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_3 = int(rsp['content'])
        MyAssert.equal(0, smart_balance_3, 'check smart balance')

    @pytest.mark.lottery_multi_actor
    def test_lottery_multi_actor(self):
        log.info('create master')
        stamp = int(time.time())
        key_master, account_master, hash_master_1, sign_master = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_master)

        log.info('login master')
        self.top_1.login(account_master)

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_1 = int(rsp['content'])

        log.info('create actor 1')
        stamp = int(time.time())
        key_actor_1, account_actor_1, hash_actor_1, sign_actor_1 = fix_node_account(self.top_2.zone_shard, stamp)
        self.top_2.create_account(account_actor_1)

        log.info('login actor 1')
        self.top_2.login(account_actor_1)

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_1 = int(rsp['content'])

        log.info('create actor 2')
        stamp = int(time.time())
        key_actor_2, account_actor_2, hash_actor_2, sign_actor_2 = fix_node_account(self.top_3.zone_shard, stamp)
        self.top_3.create_account(account_actor_2)

        log.info('login actor 2')
        self.top_3.login(account_actor_2)

        log.info('check actor 2 balance')
        rsp = self.top_3.get_balance(account_actor_2)
        actor_2_balance_1 = int(rsp['content'])

        log.info('create contract user')
        stamp = int(time.time())
        con_create = {'type': 'smart_contract'}
        key_smart, account_smart, hash_smart, sign_smart = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_smart, content=con_create)

        log.info('publish contract')
        probability = 3
        lottery_amount = 10000
        script = get_lottery_contract(account_master, hash_master_1, account_smart, lottery_amount, probability)
        self.top_1.publish_contract(account_smart, script)

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_1 = int(rsp['content'])

        MyAssert.equal(lottery_amount, smart_balance_1, 'check smart balance')

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_2 = int(rsp['content'])

        MyAssert.equal(master_balance_1 - smart_balance_1, master_balance_2, 'check master balance')

        log.info('init lottery')
        init_param = init_lottery(account_smart)
        self.top_1.exec_contract(account_smart, init_param)

        log.info('get win number')
        get_prop = get_prop_tmp(account_smart, 'win_number')
        rsp = self.top_1.get_property(account_smart, get_prop)
        win_number = int(rsp['content'])
        log.info('win_number: %d' % win_number)

        log.info('get master hash')
        rsp = self.top_1.get_last_hash(account_master)
        hash_master_2 = rsp['content']

        log.info('master buy lottery')
        buy_amount_1 = 1000
        buy_param = buy_lottery(account_master, hash_master_2, buy_amount_1, account_smart)
        self.top_1.exec_contract(account_master, buy_param)

        log.info('get master number')
        get_prop = get_prop_tmp(account_smart, 'sell_record')
        rsp = self.top_1.get_property(account_smart, get_prop)
        master_hold_number = int(json.loads(rsp['content'])[account_master])
        log.info('master_hold_number: %d' % master_hold_number)

        log.info('check master balance')
        rsp = self.top_1.get_balance(account_master)
        master_balance_3 = int(rsp['content'])

        MyAssert.equal(master_balance_2 - buy_amount_1, master_balance_3, 'check master balance')

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_2 = int(rsp['content'])

        MyAssert.equal(smart_balance_1 + buy_amount_1,
                       smart_balance_2, 'check smart balance')

        log.info('actor 1 buy lottery')
        buy_param = buy_lottery(account_actor_1, hash_actor_1, buy_amount_1, account_smart)
        self.top_2.exec_contract(account_actor_1, buy_param)

        log.info('get actor 1 number')
        get_prop = get_prop_tmp(account_smart, 'sell_record')
        rsp = self.top_2.get_property(account_smart, get_prop)
        actor_1_hold_number = int(json.loads(rsp['content'])[account_actor_1])
        log.info('actor_1_hold_number: %d' % actor_1_hold_number)

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_2 = int(rsp['content'])

        MyAssert.equal(actor_1_balance_1 - buy_amount_1, actor_1_balance_2, 'check actor 1 balance')

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_2 = int(rsp['content'])

        MyAssert.equal(smart_balance_1 + buy_amount_1 + buy_amount_1,
                       smart_balance_2, 'check smart balance')

        log.info('actor 2 buy lottery')
        buy_param = buy_lottery(account_actor_2, hash_actor_2, buy_amount_1, account_smart)
        self.top_3.exec_contract(account_actor_2, buy_param)

        log.info('get actor 2 number')
        get_prop = get_prop_tmp(account_smart, 'sell_record')
        rsp = self.top_3.get_property(account_smart, get_prop)
        actor_2_hold_number = int(json.loads(rsp['content'])[account_actor_2])
        log.info('actor_2_hold_number: %d' % actor_2_hold_number)

        log.info('check actor 2 balance')
        rsp = self.top_3.get_balance(account_actor_2)
        actor_2_balance_2 = int(rsp['content'])

        MyAssert.equal(actor_2_balance_1 - buy_amount_1, actor_2_balance_2, 'check actor 2 balance')

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_2 = int(rsp['content'])

        MyAssert.equal(smart_balance_1 + buy_amount_1 + buy_amount_1 + buy_amount_1,
                       smart_balance_2, 'check smart balance')

        log.info('draw lottery')
        draw_param = draw_lottery(account_smart)
        self.top_1.exec_contract(account_smart, draw_param)

        log.info('master check result')
        master_is_win = (master_hold_number == win_number)
        if master_is_win:
            master_notify = json.loads(self.top_1.get_notify())
            log.info('master is win')
            con_notify = json.loads(master_notify['content'])
            master_win_amount = int(con_notify['amount'])
            MyAssert.equal('transfer', master_notify['action'], 'check notify action')
            MyAssert.equal(account_master, master_notify['account'], 'check notify account')
            MyAssert.equal(account_smart, con_notify['sender'], 'check notify smart account')

            log.info('check master balance')
            rsp = self.top_1.get_balance(account_master)
            master_balance_4 = int(rsp['content'])
            MyAssert.equal(master_balance_3 + master_win_amount, master_balance_4, 'check master balance')
        else:
            log.info('master not win')
            log.info('check master balance')
            rsp = self.top_1.get_balance(account_master)
            master_balance_4 = int(rsp['content'])
            MyAssert.equal(master_balance_3, master_balance_4, 'check master balance')

        log.info('actor 1 check result')
        actor_1_is_win = (actor_1_hold_number == win_number)
        if actor_1_is_win:
            actor_1_notify = json.loads(self.top_2.get_notify())
            log.info('actor 1 is win')
            con_notify = json.loads(actor_1_notify['content'])
            actor_1_win_amount = int(con_notify['amount'])
            MyAssert.equal('transfer', actor_1_notify['action'], 'check notify action')
            MyAssert.equal(account_actor_1, actor_1_notify['account'], 'check notify account')
            MyAssert.equal(account_smart, con_notify['sender'], 'check notify smart account')

            log.info('check actor 1 balance')
            rsp = self.top_2.get_balance(account_actor_1)
            actor_1_balance_3 = int(rsp['content'])
            MyAssert.equal(actor_1_balance_2 + actor_1_win_amount, actor_1_balance_3, 'check actor 1 balance')
        else:
            log.info('actor 1 not win')
            log.info('check actor 1 balance')
            rsp = self.top_2.get_balance(account_actor_1)
            actor_1_balance_3 = int(rsp['content'])
            MyAssert.equal(actor_1_balance_2, actor_1_balance_3, 'check actor 1 balance')

        log.info('actor 2 check result')
        actor_2_is_win = (actor_2_hold_number == win_number)
        if actor_2_is_win:
            actor_2_notify = json.loads(self.top_3.get_notify())
            log.info('actor 2 is win')
            con_notify = json.loads(actor_2_notify['content'])
            actor_2_win_amount = int(con_notify['amount'])
            MyAssert.equal('transfer', actor_2_notify['action'], 'check notify action')
            MyAssert.equal(account_actor_2, actor_2_notify['account'], 'check notify account')
            MyAssert.equal(account_smart, con_notify['sender'], 'check notify smart account')

            log.info('check actor 2 balance')
            rsp = self.top_3.get_balance(account_actor_2)
            actor_2_balance_3 = int(rsp['content'])
            MyAssert.equal(actor_2_balance_2 + actor_2_win_amount, actor_2_balance_3, 'check actor 2 balance')
        else:
            log.info('actor 2 not win')
            log.info('check actor 2 balance')
            rsp = self.top_3.get_balance(account_actor_2)
            actor_2_balance_3 = int(rsp['content'])
            MyAssert.equal(actor_2_balance_2, actor_2_balance_3, 'check actor 2 balance')

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance_3 = int(rsp['content'])

        if not (master_is_win or actor_1_is_win or actor_2_is_win):
            log.info('nobody win')
            MyAssert.equal(smart_balance_2, smart_balance_3, 'check smart balance')
        else:
            log.info('someone win')
            MyAssert.equal(0, smart_balance_3, 'check smart balance')