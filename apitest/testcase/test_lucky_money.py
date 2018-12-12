# coding=utf-8
import json
import time
import sys
sys.path.append('../')

from api.LibApi import *
from api.TopApi import TopApi
import pytest

from api.TopAssert import MyAssert
from api.Unit import fix_node_account, get_lucky_tmp, get_qiang_tmp, get_lucky_money_contract, \
    get_lucky_money_out_contract

log = conftest.get_my_logger(os.path.basename(__file__))


@pytest.mark.usefixtures("laborer")
class TestLuckyMoney(object):
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

    @pytest.mark.lucky_money_smoke
    def test_lucky_money_smoke(self):
        log.info('create group user')
        stamp = int(time.time())
        key_group, account_group, hash_group, sign_group = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_group)

        log.info('create contract user')
        stamp = int(time.time())
        con_create = {'type': 'smart_contract'}
        key_smart, account_smart, hash_smart, sign_smart = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_smart, content=con_create)

        log.info('publish contract')
        script = get_lucky_money_contract()
        self.top_1.publish_contract(account_smart, script)

        log.info('create sender user')
        stamp = int(time.time())
        key_sender, account_sender, hash_sender, sign_sender = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_sender)

        log.info('login sender user')
        self.top_1.login(account_sender)

        log.info('sender sub group')
        self.top_1.subscribe(account_sender, account_group)

        log.info('check sender balance')
        rsp = self.top_1.get_balance(account_sender)
        balance_1 = int(rsp['content'])

        log.info('sender user send luck money')
        lucky_amount = 1000
        con_sender_money = get_lucky_tmp(account_sender, hash_sender, account_smart, lucky_amount)
        self.top_1.exec_contract(account_sender, con_sender_money)

        log.info('check sender balance')
        rsp = self.top_1.get_balance(account_sender)
        balance_2 = int(rsp['content'])
        MyAssert.equal(balance_1, balance_2 + lucky_amount, 'assert sender balance')

        log.info('notify new lucky money to group')
        msg = "new lucky money"
        set_dict = {
            "receiver": account_group,
            "message": msg
        }
        self.top_1.notify(account_sender, set_dict)

        log.info('receiver new lucky money notify')
        notify = json.loads(self.top_1.get_notify())
        con_notify = json.loads(notify['content'])
        MyAssert.equal(msg, con_notify['notification'], 'check notification')
        MyAssert.equal(account_sender, con_notify['sender'], 'check msg sender')

        log.info('sender loot luck money')
        exec_loot_money = get_qiang_tmp(account_smart)
        self.top_1.exec_contract(account_sender, exec_loot_money)

        log.info('notify reach money')
        notify = json.loads(self.top_1.get_notify())
        con_notify = json.loads(notify['content'])
        loot_lucky_amount = int(con_notify['amount'])
        MyAssert.equal('transfer', notify['action'], 'check notify action')
        MyAssert.equal(account_sender, notify['account'], 'check notify account')
        MyAssert.equal(account_smart, con_notify['sender'], 'check notify smart account')

        log.info('check sender balance')
        rsp = self.top_1.get_balance(account_sender)
        balance_3 = int(rsp['content'])

        MyAssert.equal(loot_lucky_amount, balance_3 - balance_2, 'assert sender money')

        log.info('sender loot luck money again')
        exec_loot_money = get_qiang_tmp(account_smart)
        self.top_1.exec_contract(account_sender, exec_loot_money, res=0)

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance = int(rsp['content'])

        MyAssert.equal(lucky_amount - loot_lucky_amount, smart_balance, 'assert smart balance')

    @pytest.mark.lucky_money_flow
    def test_lucky_money_flow(self):
        log.info('create group user')
        stamp = int(time.time())
        key_group, account_group, hash_group, sign_group = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_group)

        log.info('create contract user')
        stamp = int(time.time())
        con_create = {'type': 'smart_contract'}
        key_smart, account_smart, hash_smart, sign_smart = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_smart, content=con_create)

        log.info('publish contract')
        script = get_lucky_money_contract()
        self.top_1.publish_contract(account_smart, script)

        log.info('create sender user')
        stamp = int(time.time())
        key_sender, account_sender, hash_sender, sign_sender = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_sender)

        log.info('login sender user')
        self.top_1.login(account_sender)

        log.info('sender sub group')
        self.top_1.subscribe(account_sender, account_group)

        log.info('check sender balance')
        rsp = self.top_1.get_balance(account_sender)
        sender_balance_1 = int(rsp['content'])

        log.info('create actor user 1')
        stamp = int(time.time())
        key_actor_1, account_actor_1, hash_actor_1, sign_actor_1 = fix_node_account(self.top_2.zone_shard, stamp)
        self.top_2.create_account(account_actor_1)

        log.info('login actor user 1')
        self.top_2.login(account_actor_1)

        log.info('actor 1 sub group')
        self.top_2.subscribe(account_actor_1, account_group)

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_1 = int(rsp['content'])

        log.info('create actor user 2')
        stamp = int(time.time())
        key_actor_2, account_actor_2, hash_actor_2, sign_actor_2 = fix_node_account(self.top_3.zone_shard, stamp)
        self.top_3.create_account(account_actor_2)

        log.info('login actor user 2')
        self.top_3.login(account_actor_2)

        log.info('actor 2 sub group')
        self.top_3.subscribe(account_actor_2, account_group)

        log.info('check actor 2 balance')
        rsp = self.top_3.get_balance(account_actor_2)
        actor_2_balance_1 = int(rsp['content'])

        log.info('sender user send luck money')
        lucky_amount = 1000
        con_sender_money = get_lucky_tmp(account_sender, hash_sender, account_smart, lucky_amount)
        self.top_1.exec_contract(account_sender, con_sender_money)

        log.info('check sender balance')
        rsp = self.top_1.get_balance(account_sender)
        sender_balance_2 = int(rsp['content'])
        MyAssert.equal(sender_balance_1, sender_balance_2 + lucky_amount, 'assert sender balance')

        log.info('notify new lucky money to group')
        msg = "new lucky money"
        set_dict = {
            "receiver": account_group,
            "message": msg
        }
        self.top_1.notify(account_sender, set_dict)

        log.info('sender receive new lucky money notify')
        sender_lucky_notify = json.loads(self.top_1.get_notify())
        sender_con_notify = json.loads(sender_lucky_notify['content'])
        MyAssert.equal(msg, sender_con_notify['notification'], 'check notification')
        MyAssert.equal(account_sender, sender_con_notify['sender'], 'check msg sender')

        log.info('actor 1 receive new lucky money notify')
        actor_1_lucky_notify = json.loads(self.top_2.get_notify())
        actor_1_con_notify = json.loads(actor_1_lucky_notify['content'])
        MyAssert.equal(msg, actor_1_con_notify['notification'], 'check notification')
        MyAssert.equal(account_sender, actor_1_con_notify['sender'], 'check msg sender')

        log.info('actor 2 receive new lucky money notify')
        actor_2_lucky_notify = json.loads(self.top_3.get_notify())
        actor_2_con_notify = json.loads(actor_2_lucky_notify['content'])
        MyAssert.equal(msg, actor_2_con_notify['notification'], 'check notification')
        MyAssert.equal(account_sender, actor_2_con_notify['sender'], 'check msg sender')

        log.info('actor 1 loot luck money')
        exec_loot_money = get_qiang_tmp(account_smart)
        self.top_2.exec_contract(account_actor_1, exec_loot_money)

        log.info('notify reach money')
        actor_1_notify = json.loads(self.top_2.get_notify())
        actor_1_con_notify = json.loads(actor_1_notify['content'])
        actor_1_loot_lucky_amount = int(actor_1_con_notify['amount'])
        MyAssert.equal('transfer', actor_1_notify['action'], 'check 1 notify action')
        MyAssert.equal(account_actor_1, actor_1_notify['account'], 'check 1 notify account')
        MyAssert.equal(account_smart, actor_1_con_notify['sender'], 'check 1 notify smart account')

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_2 = int(rsp['content'])
        MyAssert.equal(actor_1_loot_lucky_amount, actor_1_balance_2 - actor_1_balance_1, 'assert actor 1 money')

        log.info('actor 2 loot luck money')
        exec_loot_money = get_qiang_tmp(account_smart)
        self.top_3.exec_contract(account_actor_2, exec_loot_money)

        log.info('notify reach money')

        actor_2_notify = json.loads(self.top_3.get_notify())
        actor_2_con_notify = json.loads(actor_2_notify['content'])
        actor_2_loot_lucky_amount = int(actor_2_con_notify['amount'])
        MyAssert.equal('transfer', actor_2_notify['action'], 'check 2 notify action')
        MyAssert.equal(account_actor_2, actor_2_notify['account'], 'check 2 notify account')
        MyAssert.equal(account_smart, actor_2_con_notify['sender'], 'check 2 notify smart account')

        log.info('check actor 2 balance')
        rsp = self.top_3.get_balance(account_actor_2)
        actor_2_balance_2 = int(rsp['content'])

        MyAssert.equal(actor_2_loot_lucky_amount, actor_2_balance_2 - actor_2_balance_1, 'assert actor 2 money')

        log.info('actor 1 loot luck money again')
        exec_loot_money = get_qiang_tmp(account_smart)
        self.top_2.exec_contract(account_actor_1, exec_loot_money, res=0)

        log.info('check smart balance')
        rsp = self.top_1.get_balance(account_smart)
        smart_balance = int(rsp['content'])

        MyAssert.equal(lucky_amount - actor_1_loot_lucky_amount - actor_2_loot_lucky_amount,
                       smart_balance, 'assert smart balance')

    @pytest.mark.lucky_money_out
    def test_lucky_money_out(self):
        log.info('create contract user')
        stamp = int(time.time())
        con_create = {'type': 'smart_contract'}
        key_smart, account_smart, hash_smart, sign_smart = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_smart, content=con_create)

        log.info('publish contract')
        script = get_lucky_money_out_contract()
        self.top_1.publish_contract(account_smart, script)

        log.info('create sender user')
        stamp = int(time.time())
        key_sender, account_sender, hash_sender, sign_sender = fix_node_account(self.top_1.zone_shard, stamp)
        self.top_1.create_account(account_sender)

        log.info('login sender user')
        self.top_1.login(account_sender)

        log.info('check sender balance')
        rsp = self.top_1.get_balance(account_sender)
        sender_balance_1 = int(rsp['content'])

        log.info('sender user send lucky money')
        lucky_amount = 1000
        con_sender_money = get_lucky_tmp(account_sender, hash_sender, account_smart, lucky_amount)
        self.top_1.exec_contract(account_sender, con_sender_money)

        log.info('check sender balance')
        rsp = self.top_1.get_balance(account_sender)
        sender_balance_2 = int(rsp['content'])

        MyAssert.equal(sender_balance_1, sender_balance_2 + lucky_amount, 'assert sender balance')

        log.info('create actor user 1')
        stamp = int(time.time())
        key_actor_1, account_actor_1, hash_actor_1, sign_actor_1 = fix_node_account(self.top_2.zone_shard, stamp)
        self.top_2.create_account(account_actor_1)

        log.info('login actor user 1')
        self.top_2.login(account_actor_1)

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_1 = int(rsp['content'])

        log.info('actor 1 loot luck money')
        exec_loot_money = get_qiang_tmp(account_smart)
        self.top_2.exec_contract(account_actor_1, exec_loot_money)

        log.info('notify reach money')
        actor_1_notify = json.loads(self.top_2.get_notify())
        actor_1_con_notify = json.loads(actor_1_notify['content'])
        actor_1_loot_lucky_amount = int(actor_1_con_notify['amount'])
        MyAssert.equal(lucky_amount, actor_1_loot_lucky_amount, 'check actor 1 loot money')
        MyAssert.equal('transfer', actor_1_notify['action'], 'check 1 notify action')
        MyAssert.equal(account_actor_1, actor_1_notify['account'], 'check 1 notify account')
        MyAssert.equal(account_smart, actor_1_con_notify['sender'], 'check 1 notify smart account')

        log.info('check actor 1 balance')
        rsp = self.top_2.get_balance(account_actor_1)
        actor_1_balance_2 = int(rsp['content'])

        MyAssert.equal(actor_1_loot_lucky_amount, actor_1_balance_2 - actor_1_balance_1, 'assert actor 1 money')

        log.info('sender loot luck money')
        exec_loot_money = get_qiang_tmp(account_smart)
        rsp = self.top_1.exec_contract(account_sender, exec_loot_money, res=0)
        MyAssert.equal(0, rsp['result'], 'assert result')
