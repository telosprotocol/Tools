# coding=utf-8
import base64
import sys
import os
import time
from decimal import Decimal

sys.path.append('../')
from api.LibApi import top_receive_transfer, get_signature
from multiprocessing import Process, Manager
from api.Util import tps_to_file, progressbar, get_test_data_from_file
from api.TopApi import TopApi
import conftest


def tps_transfer_in(receivers, node_index, pid):
    top = TopApi(node_index)
    log = conftest.get_logger(os.path.basename(__file__), pid)

    while True:

        for q in xrange(len(receivers)):
            receiver = receivers[q]
            balance_rsp = top.account_balance(receiver['account'])
            balance_rsp_dict = balance_rsp.json()
            if balance_rsp_dict['Result'] != 1:
                log.error('pre_genesis_balance result not 1:' + str(receiver['account']))
                # 后续需要统计失败
                continue
            balance = balance_rsp_dict['balance']
            receiver['balance'] = int(balance)

            post = int(balance) - receiver['balance']
            tps_list[1] += post

            # 如果账号余额增量不等于上一次接收交易的成功数，则更新hash
            if post < receiver['count']:
                # update receiver last hash
                rsp = top.get_account_last_hash(receiver['account'])
                if rsp.json()['Result'] != 1:
                    log.error('can\'t get last hash :' + str(receiver['account']))
                    # 后续需要统计失败
                    continue
                sender_last_hash = base64.b64decode(rsp.json()['last_digest'])
                receiver['last_hash'] = sender_last_hash
            elif post > receiver['count']:
                log.error('post > count!!! account: %s' % receiver['account'])
                receiver[q] = receiver_pool.pop()
                continue

            # reset count
            receiver['count'] = 0

            # check pending
            rsp_pending = top.get_account_pending(receiver['account'])
            if rsp_pending.json()['Result'] != 1:
                log.error('rsp_pending result not 1:' + str(receiver['account']))
                # 后续需要统计失败
                continue

            for ts in rsp_pending.json()['count']:
                pending_hash_base64 = rsp_pending.json()['blocks'][ts]['block']
                receiver_pending_hash = base64.b64decode(pending_hash_base64)

                receiver_current_hash = top_receive_transfer(receiver['account'], receiver_pending_hash,
                                                             receiver['last_hash'])
                log.info(receiver_current_hash)
                receiver_current_signature = get_signature(receiver['private_key'], receiver_current_hash)

                rsp = top.confirm_receive_transfer(receiver['account'], base64.b64encode(receiver_pending_hash),
                                                   base64.b64encode(receiver['last_hash']),
                                                   base64.b64encode(receiver_current_hash),
                                                   base64.b64encode(receiver_current_signature))
                tps_list[0] += 1
                if rsp.json()['Result'] != 1:
                    log.error('top_transfer_in fail:' + str(receiver['account']))
                    # 后续需要统计失败
                    break
                else:
                    receiver['last_hash'] = receiver_current_hash

                receiver['count'] += 1


def printer():
    pre_hits = 0

    current_date = time.strftime('%Y-%m-%d-%H-%M_%S', time.localtime(time.time()))
    tps_file = conftest.result_dir + 'tps_in_' + current_date + '.txt'

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
                        '%s all: %s | p: %s | f: %s | tps: %s '
                        % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), str(post_hits), str(pas),
                           str(post_hits - pas), str(incr)))
        pre_hits = post_hits


def per_receivers(count):
    p_s = []
    for u in xrange(count):
        p_s.append(receiver_pool.pop())
    return p_s


if __name__ == '__main__':

    process_count = int(sys.argv[1])
    task_count = int(sys.argv[2])
    node_receive = int(sys.argv[3])

    pl = []

    mgr = Manager()
    receiver_pool = mgr.list()
    tps_list = mgr.list()

    tps_list.append(0)

    tps_list.append(0)

    receiver_pool.extend(get_test_data_from_file('receiver_account.txt'))

    for i in xrange(process_count):
        per_r = per_receivers(task_count)
        p = Process(target=tps_transfer_in, args=(per_r, node_receive, i))
        p.start()
        pl.append(p)

    p = Process(target=printer, args=())
    p.start()
    pl.append(p)

    [p.join() for p in pl]