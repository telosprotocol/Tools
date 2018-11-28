# coding=utf-8
import base64
import sys
import os
import time
from decimal import Decimal

sys.path.append('../')
from multiprocessing import Process, Manager
from api.Util import tps_to_file, progressbar, get_test_data_from_file
from api.TopApi import TopApi
import conftest


def tps_transfer_out(senders, receivers, node_index, pid):
    top = TopApi(node_index)
    log = conftest.get_logger(os.path.basename(__file__), pid)
    test_transfer_amount = 1
    while True:
        # get sender balance
        for q in xrange(len(senders)):
            sender = senders[q]
            balance_rsp = top.account_balance(sender['account'])
            balance_rsp_dict = balance_rsp.json()
            if balance_rsp_dict['Result'] != 1:
                log.error('pre_genesis_balance result not 1:' + str(sender['account']))
                senders[q] = sender_pool.pop()
                # 后续需要统计失败
                log.error('get balance err, account: %s' % (sender['account']))
                continue
            balance = balance_rsp_dict['balance']
            if balance == 0:
                log.error('account power off!')
                senders[q] = sender_pool.pop()
                continue

            nt = time.time()

            if sender['balance'] == float(balance) + 1:
                tps_list[1] += 1
            else:
                log.error('post err, hash: %s, pre :%d post: %d, pt :%d nt :%d' %
                          (sender['last_hash'].encode('hex'), sender['balance'], float(balance), sender['stamp'], nt))
                # update sender last hash
                rsp = top.get_account_last_hash(sender['account'])
                if rsp.json()['Result'] != 1:
                    log.error('can\'t get last hash :' + str(sender['account']))
                    senders[q] = sender_pool.pop()
                    # 后续需要统计失败
                    log.error('get hash err, account: %s' % (sender['account']))
                    continue
                sender_last_hash = base64.b64decode(rsp.json()['last_digest'])
                sender['last_hash'] = sender_last_hash

            sender['balance'] = float(balance)
            sender['stamp'] = nt

            # make deal
            rsp, new_sender = top.top_transfer_out(sender, receivers[q], test_transfer_amount)
            tps_list[0] += 1
            if rsp.json()['Result'] != 1:
                log.error('top_transfer_out fail:' + str(sender['account']))
                senders[q] = sender_pool.pop()
                # 后续需要统计失败
                log.error('transfer err, hash: %s' % (sender['last_hash'].encode('hex')))
                continue


def printer():
    pre_hits = 0

    current_date = time.strftime('%Y-%m-%d-%H-%M_%S', time.localtime(time.time()))
    tps_file = conftest.result_dir + 'tps_out_' + current_date + '.txt'

    if os.path.exists(tps_file):
        os.remove(tps_file)
    while True:
        if len(tps_list) == 0:
            time.sleep(10)
            continue
        if pre_hits == 0:
            pre_hits = tps_list[0]
        time.sleep(60)
        pas = tps_list[1]
        post_hits = tps_list[0]
        incr = round(Decimal(post_hits - pre_hits) / Decimal(60), 2)
        if incr > 0:
            progressbar('all: %s | p: %s | f: %s | tps: %s      '
                        % (str(post_hits), str(pas), str(post_hits - pas), str(incr)))
            tps_to_file(tps_file,
                        '%s all: %s | p: %s | f: %s | tps: %s'
                        % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), str(post_hits), str(pas),
                           str(post_hits - pas), str(incr)))
        pre_hits = post_hits


def per_group(count):
    p_s = []
    p_r = []
    for u in xrange(count):
        p_s.append(sender_pool.pop())
        p_r.append(receiver_pool.pop())
    return p_s, p_r


if __name__ == '__main__':

    process_count = int(sys.argv[1])
    task_count = int(sys.argv[2])
    node_send = int(sys.argv[3])

    pl = []

    mgr = Manager()
    sender_pool = mgr.list()
    receiver_pool = mgr.list()
    tps_list = mgr.list()

    tps_list.append(0)

    tps_list.append(0)

    sender_pool.extend(get_test_data_from_file('sender_account.txt'))

    receiver_pool.extend(get_test_data_from_file('receiver_account.txt'))

    for i in xrange(process_count):
        per_s, per_r = per_group(task_count)
        p = Process(target=tps_transfer_out, args=(per_s, per_r, node_send, i))
        p.start()
        pl.append(p)

    p = Process(target=printer, args=())
    p.start()
    pl.append(p)

    [p.join() for p in pl]

