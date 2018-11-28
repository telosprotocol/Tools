# -*- coding: utf-8 -*-
import ConfigParser
import os
import time
import sys

# 设置节点url
node_1_url = sys.argv[1]
node_2_url = sys.argv[2]
node_3_url = sys.argv[3]

# 设置节点启动状态，1表示启动，0表示不启动
node_1_alive = sys.argv[4]
node_2_alive = sys.argv[5]
node_3_alive = sys.argv[6]

project_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = project_dir + '/config/'
log_dir = project_dir + '/log/'
report_dir = project_dir + '/report/'

# config log info
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
log_out_file = log_dir + '/log_' + current_date + '.log'
config_log_file = config_dir + 'logging.ini'
args_value = (log_out_file, 'a', 1024 * 1024 * 10, 20,)
cp_logging = ConfigParser.SafeConfigParser()
cp_logging.read(config_log_file)
cp_logging.set('handlers', 'keys', 'consoleHandler,fileHandler')
cp_logging.set('logger_root', 'handlers', 'consoleHandler,fileHandler')
cp_logging.set('handler_fileHandler', 'args', str(args_value))
cp_logging.write(open(config_log_file, 'w'))

# read and write env.ini
cp_env = ConfigParser.SafeConfigParser()
config_env_file = config_dir + 'env.ini'
cp_env.read(config_env_file)
cp_env.set('node_url', 'node_1', node_1_url)
cp_env.set('node_url', 'node_2', node_2_url)
cp_env.set('node_url', 'node_3', node_3_url)
cp_env.set('node_1', 'alive', node_1_alive)
cp_env.set('node_2', 'alive', node_2_alive)
cp_env.set('node_3', 'alive', node_3_alive)
cp_env.write(open(config_env_file, 'w'))

# create report dir
report_dir = project_dir + '/report/'
if not os.path.exists(report_dir):
    os.makedirs(report_dir)

