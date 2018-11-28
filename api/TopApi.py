# coding=utf-8
import base64
import sys
import time

from api.TopAssert import mycheck

sys.path.append('../')

from api.LibApi import *
import os
import conftest
import requests
import ConfigParser

log = conftest.get_my_logger(os.path.basename(__file__))


class TopApi(object):

    def __init__(self, node_index):
        config_file_path = conftest.config_dir + 'env.ini'
        cp = ConfigParser.SafeConfigParser()
        cp.read(config_file_path)
        node_host = cp.get('node_url', 'node_' + str(node_index))
        log.info('node_host --> %s' % node_host)
        self.top_host = node_host

    @mycheck
    def account_create(self, top_account, top_digest, top_signature, count='100000000'):
        """
        create account
        :param top_account:
        :param top_digest:  hash value
        :param top_signature:
        :param count:
        :return:
        """
        url = self.top_host
        payload = {'action': 'account_create', 'account': top_account, 'digest': top_digest,
                   'signature': top_signature, 'amount': count, 'timestamp': time.time()}
        log.debug(str(payload))
        rsp = requests.post(url, json=payload)
        log.debug('api action --> account_create')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def account_balance(self, top_account):
        url = self.top_host
        payload = {'action': 'account_balance', 'account': top_account, 'property_key': '$$'}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> account_balance')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def account_info(self, top_account):
        """
        查询账户信息
        :param top_account:
        :return:
        """
        url = self.top_host
        payload = {
            'action': 'account_info',
            'account': top_account
        }
        rsp = requests.post(url, json=payload)
        log.debug('api action --> account_info')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def account_transfer(self, top_source, top_destination, top_amount, top_last_digest, top_digest, top_signature,
                         property_key='$$'):
        """
        转出交易
        :param top_source:
        :param top_destination:
        :param top_amount:
        :param top_last_digest:
        :param top_digest:
        :param top_signature:
        :param property_key:
        :return:
        """
        url = self.top_host
        payload = {
            'action': 'transfer_out',
            'source': top_source,
            'destination': top_destination,
            'property_key': property_key,
            'amount': top_amount,
            'last_digest': top_last_digest,
            'digest': top_digest,
            'signature': top_signature,
            'timestamp': time.time()}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> transfer_out')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def get_account_pending(self, top_account, count_limit=100):
        """
        get account pending info
        :param top_account:
        :param count_limit:
        :return:
        """
        url = self.top_host
        payload = {'action': 'account_pending',
                   'account': top_account,
                   'count': count_limit}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> account_pending')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def confirm_receive_transfer(self, top_account, pending_return_hash, top_last_digest, top_digest, top_signature):
        """
        接收交易
        :param top_account:
        :param pending_return_hash:
        :param top_last_digest:
        :param top_digest:
        :param top_signature:
        :return:
        """
        url = self.top_host
        payload = {'action': 'transfer_in',
                   'account': top_account,
                   'tx_digest': pending_return_hash,
                   'last_digest': top_last_digest,
                   'digest': top_digest,
                   'signature': top_signature,
                   'timestamp': time.time()}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> transfer_in')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def get_account_history(self, top_account, count_limit=1):
        """
        get account history
        :param top_account:
        :param count_limit:
        :return:
        """
        url = self.top_host
        payload = {'action': 'account_history',
                   'account': top_account,
                   'count': count_limit}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> account_history')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def get_tps(self):
        """
        get tps
        """
        url = self.top_host
        payload = {'action': 'tps'}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> tps')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def set_property(self, top_account, key, value, tx, last, sign):
        """
        设置属性
        :param top_account:
        :param key:
        :param value:
        :param tx:
        :param last:
        :param sign:
        :return:
        """
        url = self.top_host
        payload = {'action': 'set_property',
                   'account': top_account,
                   'property_key': key,
                   'property_value': value,
                   'tx_digest': tx,
                   'last_digest': last,
                   'timestamp': time.time(),
                   'signature': sign}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> set_property')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def query_property(self, top_account, key):
        """
        查询属性
        :param top_account:
        :param key:
        :return:
        """
        url = self.top_host
        payload = {'action': 'query_property',
                   'account': top_account,
                   'property_key': key}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> query_property')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def query_all_property(self, top_account):
        """
        查询全部属性
        :param top_account:
        :return:
        """
        url = self.top_host
        payload = {'action': 'query_property',
                   'account': top_account}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> query_all_property')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    @mycheck
    def get_account_last_hash(self, top_account):
        """
        get account history, changed by aries
        :param top_account:
        :return:
        """
        url = self.top_host
        payload = {'action': 'last_digest',
                   'account': top_account}
        rsp = requests.post(url, json=payload)
        log.debug('api action --> last_digest')
        log.debug('api payload --> %s' % str(payload))
        log.debug('api rsp --> %s' % rsp.text)
        return rsp

    def top_create_account(self, private_key=None):
        if private_key is None:
            my_private_key = get_private_key()
        else:
            my_private_key = private_key.decode('hex')
        log.debug('my_private_key --> %s' % my_private_key.encode('hex'))
        log.debug('my_private_key raw --> %s' % my_private_key)

        my_top_account = get_account(my_private_key)
        my_account_hash = get_account_hash(my_top_account)
        my_account_signature = get_signature(my_private_key, my_account_hash)
        rsp = self.account_create(my_top_account, base64.b64encode(my_account_hash),
                                  base64.b64encode(my_account_signature))
        log.debug(rsp.text)
        rsp_dic = rsp.json()
        account_info = {}
        if rsp_dic['Result'] == 1:
            account_info['account'] = my_top_account
            account_info['account_private_key'] = my_private_key.encode('hex')
            account_info['account_hash'] = my_account_hash.encode('hex')
            account_info['account_signature'] = my_account_signature.encode('hex')
        log.info('account_info --> %s' % str(account_info))
        return account_info

    def top_get_account_balance(self, top_account):
        rsp = self.account_balance(top_account)
        log.debug(rsp.text)
        rsp_dict = rsp.json()
        account_balance = -1
        if rsp_dict['Result'] == 1:
            account_balance = rsp_dict['balance']
        log.info('account_balance --> %s' % str(account_balance))
        return account_balance

    def top_transfer_out(self, sender, receive, amount):
        transfer_amount = str(amount)
        sender_account = sender['account']
        receive_account = receive['account']
        sender_private_key = sender['private_key']
        sender_last_hash = sender['last_hash']
        sender_current_hash = top_transfer(sender_account, receive_account, transfer_amount, sender_last_hash)
        sender_current_signature = get_signature(sender_private_key, sender_current_hash)
        rsp = self.account_transfer(sender_account, receive_account, transfer_amount,
                                    base64.b64encode(sender_last_hash), base64.b64encode(sender_current_hash),
                                    base64.b64encode(sender_current_signature))

        return rsp, sender_current_hash

    def top_transfer_in(self, receiver, pending_hash):
        receiver_private_key = receiver['private_key']
        receiver_account = receiver['account']
        receiver_last_hash = receiver['last_hash']
        receiver_current_hash = top_receive_transfer(receiver_account, pending_hash,
                                                     receiver_last_hash.decode('hex'))
        receiver_current_signature = get_signature(receiver_private_key, receiver_current_hash)

        rsp = self.confirm_receive_transfer(
            receiver_account,
            base64.b64encode(pending_hash), base64.b64encode(receiver_last_hash.decode('hex')),
            base64.b64encode(receiver_current_hash), base64.b64encode(receiver_current_signature)
        )
        return rsp, receiver_current_hash

    def top_account_pending(self, receiver):
        receiver_account = receiver['account']
        pending_rsp = self.get_account_pending(receiver_account)
        log.debug(pending_rsp.text)
        pending_rsp_dict = pending_rsp.json()

        pending_return_hash_base64 = pending_rsp_dict['blocks'][0]['block']
        pending_return_hash = base64.b64decode(pending_return_hash_base64)
        return pending_return_hash

    def create_account(self, private_key=None, time_delay=0.3):
        time.sleep(time_delay)
        account_info = self.top_create_account(private_key=private_key)
        if account_info:
            time.sleep(time_delay)
            account_balance = self.top_get_account_balance(account_info['account'])
            if account_balance > -1:
                return {'private_key': account_info['account_private_key'].decode('hex'),
                        'account': account_info['account'],
                        'last_hash': account_info['account_hash']}
            log.error('create account but balance < 0')
            return {}
        log.error('create account fail')
        return {}

    def finish_transfer_common(self, sender, receiver, amount):
        rsp = self.get_account_last_hash(sender['account'])
        sender_last_hash = base64.b64decode(rsp.json()['last_digest'])
        sender['last_hash'] = sender_last_hash

        receiver_current_hash = self.common_account_transfer(sender, receiver, amount)
        receiver['last_hash'] = receiver_current_hash

        return receiver

    def common_account_transfer(self, sender, receiver, amount, duration=0.1):
        # get pre sender balance
        pre_sender_balance_rsp = self.account_balance(sender['account'])
        pre_sender_balance_rsp_dict = pre_sender_balance_rsp.json()
        if pre_sender_balance_rsp_dict['Result'] != 1:
            log.error('pre_sender_balance_rsp result not 1')
            raise Exception('pre get balance sender--> ' + sender['account'] + ' error!')
        pre_sender_balance = pre_sender_balance_rsp_dict['balance']

        # get pre receiver balance
        pre_receiver_balance_rsp = self.account_balance(receiver['account'])
        pre_receiver_balance_rsp_dict = pre_receiver_balance_rsp.json()
        if pre_receiver_balance_rsp_dict['Result'] != 1:
            log.error('pre_receiver_balance_rsp result not 1')
            raise Exception('pre get balance receiver--> ' + receiver['account'] + ' error!')
        pre_receiver_balance = pre_receiver_balance_rsp_dict['balance']

        # sender transfer to receiver
        rsp, sender_current_hash = self.top_transfer_out(sender, receiver, amount)
        transfer_rsp_dict = rsp.json()
        if transfer_rsp_dict['Result'] != 1:
            log.error(rsp.text)
            raise Exception('transfer action error!')

        # wait making deal
        time.sleep(duration)

        # get post sender balance
        post_sender_balance_rsp = self.account_balance(sender['account'])
        post_sender_balance_rsp_dict = post_sender_balance_rsp.json()
        if post_sender_balance_rsp_dict['Result'] != 1:
            log.error('post_sender_balance_rsp result not 1')
            raise Exception('post get balance sender--> ' + sender['account'] + ' error!')
        post_sender_balance = post_sender_balance_rsp_dict['balance']

        # wait making deal
        time.sleep(duration)

        # get pending
        receiver_pending_hash = None
        for a in xrange(20):
            time.sleep(duration)
            pending_rsp = self.get_account_pending(receiver['account'])
            log.debug(pending_rsp.text)
            pending_rsp_dict = pending_rsp.json()
            if pending_rsp_dict['Result'] != 1:
                continue
            if pending_rsp_dict['blocks'] is not None:
                pending_return_hash_base64 = pending_rsp_dict['blocks'][0]['block']
                receiver_pending_hash = base64.b64decode(pending_return_hash_base64)
                break

        if receiver_pending_hash is None:
            raise Exception('receiver pending hash is None')

        # receiver get transfer
        log.info('log1')
        receiver_transfer_in_rsp, receiver_current_hash = self.top_transfer_in(receiver, receiver_pending_hash)
        log.info('log2')
        if receiver_transfer_in_rsp.json()['Result'] != 1:
            log.error('receiver_transfer_in_rsp result not 1')
            raise Exception('top_transfer_in fail')

        # wait making deal
        time.sleep(duration)

        # get post receiver balance
        log.info('log3')
        for a in xrange(20):
            post_receiver_balance_rsp = self.account_balance(receiver['account'])
            log.info('log4')
            log.debug(post_receiver_balance_rsp.text)
            post_receiver_balance_rsp_dict = post_receiver_balance_rsp.json()
            if post_receiver_balance_rsp_dict['Result'] != 1:
                log.error('post_receiver_balance_rsp result not 1')
                raise Exception('post get balance receiver--> ' + receiver['account'] + ' error!')
            post_receiver_balance = post_receiver_balance_rsp_dict['balance']
            log.info(float(pre_sender_balance))
            log.info(float(post_sender_balance))
            log.info(float(post_receiver_balance))
            log.info(float(pre_receiver_balance))
            if (float(pre_sender_balance) - float(post_sender_balance)) == \
                    (float(post_receiver_balance) - float(pre_receiver_balance)):
                return receiver_current_hash
            time.sleep(duration)
        raise Exception('transfer money variant')


if __name__ == '__main__':
    index = sys.argv[1]
    account = sys.argv[2]
    t = TopApi(index)
    r = t.account_balance(account)
    print r.text