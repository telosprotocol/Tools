import logging.config
import os
import logging

project_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = project_dir + '/config/'
log_dir = project_dir + '/log/'
report_dir = project_dir + '/report/'
result_dir = project_dir + '/result/'
send_data_dir = project_dir + '/testdata'

config_log_file = config_dir + 'logging.ini'
logging.config.fileConfig(config_log_file)


def get_my_logger(logger_name):
    logger = logging.getLogger(logger_name)
    return logger


def get_logger(name, pid):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    log_out_file = log_dir + '/log_' + str(pid) + '.log'
    handler = logging.FileHandler(log_out_file)
    handler.setLevel(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
