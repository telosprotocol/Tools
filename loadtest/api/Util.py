import ConfigParser
import os
import sys
import time

import conftest


def tps_to_file(file_path, tps_value):
    # log.debug('tps_file_path --> %s ' % file_path)
    # create tps file
    if not os.path.exists(file_path):
        os.mknod(file_path)
    # write hash to file
    with open(file_path, 'a+') as f:
        f.write(str(tps_value) + '\n')


def progressbar(context):
    sys.stdout.write('\r')
    sys.stdout.write(str(context))
    sys.stdout.flush()


def data_to_file(f_name, context):
    f_dir = conftest.send_data_dir
    f_path = os.path.join(f_dir, f_name)
    if not os.path.exists(f_path):
        os.mknod(f_path)
    with open(f_path, 'a+') as f:
        f.write(str(context) + '\n')


def get_test_data_from_file(f_name):
    f_dir = conftest.send_data_dir
    f_path = os.path.join(f_dir, f_name)
    if not os.path.exists(f_path):
        raise Exception('not such file: ' + str(f_path))
    try:
        f = open(f_path)
        lines = f.readlines()
        f.close()
    except Exception, e:
        print e
        raise Exception('read file error')
    else:
        new_list = []
        for line in lines:
            p = line.split(',')
            new_list.append({
                'account': p[0],
                'private_key': p[1].decode('hex'),
                'last_hash': p[2].decode('hex'),
                'balance': -1,
                'stamp': -1
            })
        return new_list


def get_key(f, n, k):
    config_file_path = conftest.config_dir + f + '.ini'
    cp = ConfigParser.SafeConfigParser()
    cp.read(config_file_path)
    return cp.get(n, k)


def get_acc(n, k):
    return get_key('account', n, k)


def get_env(n, k):
    return get_key('env', n, k)


def get_param():
    nodes = []
    from_to = []
    node_1_alive = get_env('node_1', 'alive')
    node_2_alive = get_env('node_2', 'alive')
    node_3_alive = get_env('node_3', 'alive')
    if node_1_alive == '1':
        nodes.append('1')
    if node_2_alive == '1':
        nodes.append('2')
    if node_3_alive == '1':
        nodes.append('3')
    for i in nodes:
        for j in nodes:
            tp = (i, j)
            from_to.append(tp)
    return from_to


if __name__ == '__main__':
    time.sleep(1)
    progressbar(1)
    time.sleep(1)
    progressbar(2)
    time.sleep(1)
    progressbar(3)
