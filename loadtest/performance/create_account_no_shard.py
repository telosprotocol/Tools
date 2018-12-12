import sys
sys.path.append('../')
from decimal import Decimal
from api.Util import data_to_file, progressbar
from api.TopApi import *


def fix_account(account_type, number, node_index=1):
    top = TopApi(node_index)
    fix_count = 0
    if account_type == 0:
        file_name = 'receiver_account.txt'
    elif account_type == 1:
        file_name = 'sender_account.txt'
    else:
        print 'account_type err'
        exit(-1)

    print 'creating senders account'

    while fix_count < number:
        acc = top.top_create_account()
        if len(acc) > 0:
            sender_context = '%s,%s,%s,' % (str(acc['account']), str(acc['account_private_key']),
                                            str(acc['account_hash']))
            data_to_file(file_name, sender_context)
            fix_count += 1
        time.sleep(0.05)
        progressbar(round(Decimal(fix_count) / Decimal(number), 3))


if __name__ == '__main__':
    a_type = int(sys.argv[1])
    count = int(sys.argv[2])

    if len(sys.argv) < 3:
        print 'argv 1: account type [0: receiver; 1: sender]'
        print 'argv 2: account count'
        exit(-1)

    fix_account(a_type, count)
