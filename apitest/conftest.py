import logging.config
import os
import logging

project_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = project_dir + '/config/'
log_dir = project_dir + '/log/'
lib_dir = project_dir + '/lib/'
report_dir = project_dir + '/report/'
result_dir = project_dir + '/result/'
send_data_dir = project_dir + '/testdata'

config_log_file = config_dir + 'logging.ini'
logging.config.fileConfig(config_log_file)


def get_my_logger(logger_name):
    logger = logging.getLogger(logger_name)
    return logger

