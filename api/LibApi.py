import os
from ctypes import *
import sys
sys.path.append('../')
import conftest

log = conftest.get_my_logger(os.path.basename(__file__))

PRIVATE_LEN = 32
HASH_LEN = 32
SIGNATURE_LEN = 65
ACCOUNT_LEN = 35
PROPERTY_KEY_LEN = 50
AMOUNT_LEN = 50


def so_obj():
    so = cdll.LoadLibrary
    lib = so(conftest.project_dir + '/lib/libxrpcclient.so')
    return lib


def get_private_key():
    lib = so_obj()

    # get private key
    p_arr = c_char * PRIVATE_LEN
    p_arg = p_arr()
    lib.xrpc_client_pri_key_make(p_arg)
    private_key_list = []
    for i in range(0, len(p_arg)):
        private_key_list.append(p_arg[i])
        # print(p_arg[i])
    # log.debug('-' * 5 + 'private_key' + '-' * 5)
    private_key = ''.join(private_key_list)
    # log.debug(private_key)
    # log.debug(private_key.encode('hex'))
    # print(len(private_key_list))
    return private_key


def get_account(private_key):
    lib = so_obj()

    # get private key
    p_arr = c_char * PRIVATE_LEN
    p_arg = p_arr()
    for i in range(0, len(private_key)):
        p_arg[i] = private_key[i]

    # get top account
    account_arr = c_char * ACCOUNT_LEN
    account_arg = account_arr()
    lib.xrpc_client_account_address_get(p_arg, account_arg)
    account_list = []
    for i in range(0, len(account_arg)):
        account_list.append(account_arg[i])
        # print(account_arg[i])
    # log.debug('-' * 5 + 'top_account' + '-' * 5)
    top_account = ''.join(account_list)
    # log.debug(top_account)
    # print(len(top_account))
    return top_account.strip()


def get_account_hash(top_account):
    lib = so_obj()

    account_arr = c_char * ACCOUNT_LEN
    account_arg = account_arr()
    for i in range(0, len(top_account)):
        account_arg[i] = top_account[i]

    # get hash
    h_arr = c_char * HASH_LEN
    h_arg = h_arr()
    lib.xprc_client_create_accout_hash_calc(account_arg, h_arg)
    account_hash_list = []
    for i in range(0, len(h_arg)):
        account_hash_list.append(h_arg[i])
        # print(h_arg[i])
    # log.debug('-' * 5 + 'hash' + '-' * 5)
    account_hash = ''.join(account_hash_list)
    # log.debug(account_hash)
    # log.debug(account_hash.encode('hex'))
    # print(len(account_hash))
    return account_hash


# void xrpc_client_hash_to_signature(uint8_t private_key[32], uint8_t hash[32], uint8_t signature[65]);
def get_signature(private_key, top_hash):
    lib = so_obj()

    # get private key
    p_arr = c_char * PRIVATE_LEN
    p_arg = p_arr()
    for i in range(0, len(private_key)):
        p_arg[i] = private_key[i]

    # get hash
    h_arr = c_char * HASH_LEN
    h_arg = h_arr()
    for i in range(0, len(top_hash)):
        h_arg[i] = top_hash[i]

    # get signature
    signature_arr = c_char * SIGNATURE_LEN
    signature_arg = signature_arr()
    lib.xrpc_client_hash_to_signature(p_arg, h_arg, signature_arg)
    signature_list = []
    for i in range(0, len(signature_arg)):
        signature_list.append(signature_arg[i])
        # print(signature_arg[i])
    # log.debug('-' * 5 + 'signature' + '-' * 5)
    top_signature = ''.join(signature_list)
    # log.debug(top_signature)
    # log.debug(top_signature.encode('hex'))
    # print(len(top_signature))
    return top_signature


def top_transfer(sender_account, receiver_account, top_amount, last_hash, property_key='$$'):
    """
    get sender transfer current hash value
    :param sender_account:
    :param receiver_account:
    :param top_amount:
    :param last_hash:
    :param property_key:
    :return:
    """

    lib = so_obj()

    # get sender account
    sender_account_arr = c_char * ACCOUNT_LEN
    sender_account_arg = sender_account_arr()
    for i in range(0, len(sender_account)):
        sender_account_arg[i] = sender_account[i]

    # get receiver account
    receiver_account_arr = c_char * ACCOUNT_LEN
    receiver_account_arg = receiver_account_arr()
    # print receiver_account
    for i in range(0, len(receiver_account)):
        # print len(receiver_account)
        # print receiver_account[i]
        receiver_account_arg[i] = receiver_account[i]

    # get amount
    top_amount_arr = c_char * AMOUNT_LEN
    top_amount_arg = top_amount_arr()
    for i in range(0, len(top_amount)):
        top_amount_arg[i] = top_amount[i]

    # get lash hash
    last_hash_arr = c_char * HASH_LEN
    last_hash_arg = last_hash_arr()
    # log.debug('to_transfer hash:')
    # log.debug(last_hash)
    for i in range(0, len(last_hash)):
        last_hash_arg[i] = last_hash[i]

    # get property_key
    property_key_arr = c_char * PROPERTY_KEY_LEN
    property_key_arg = property_key_arr()
    for i in range(0, len(property_key)):
        property_key_arg[i] = property_key[i]

    # get current transfer hash
    current_hash_arr = c_char * HASH_LEN
    current_hash_arg = current_hash_arr()
    lib.xprc_client_transaction_hash_calc(sender_account_arg, receiver_account_arg,
                                          property_key_arg, top_amount_arg, last_hash_arg,
                                          current_hash_arg)
    current_hash_list = []
    for i in range(0, len(current_hash_arg)):
        current_hash_list.append(current_hash_arg[i])
        # print(current_hash_arg[i])
    # log.debug('-' * 5 + 'current_transfer_hash' + '-' * 5)
    top_current_transfer_hash = ''.join(current_hash_list)
    # log.debug(top_current_transfer_hash)
    # log.debug(top_current_transfer_hash.encode('hex'))
    # print(len(top_current_transfer_hash))
    return top_current_transfer_hash


def top_receive_transfer(receiver_account, pending_return_hash, last_hash):
    """
    get receive confirm transfer current hash value
    :param receiver_account:
    :param pending_return_hash:
    :param last_hash: receive first transfer, last_hash = account_hash
    :return:
    """
    lib = so_obj()

    # get receiver account
    receiver_account_arr = c_char * ACCOUNT_LEN
    receiver_account_arg = receiver_account_arr()
    for i in range(0, len(receiver_account)):
        receiver_account_arg[i] = receiver_account[i]

    # get pending_return_hash
    top_pending_return_hash_arr = c_char * HASH_LEN
    top_pending_return_hash_arg = top_pending_return_hash_arr()
    for i in range(0, len(pending_return_hash)):
        top_pending_return_hash_arg[i] = pending_return_hash[i]

    # get lash hash
    last_hash_arr = c_char * HASH_LEN
    last_hash_arg = last_hash_arr()
    for i in range(0, len(last_hash)):
        last_hash_arg[i] = last_hash[i]

    # get current transfer hash
    current_hash_arr = c_char * HASH_LEN
    current_hash_arg = current_hash_arr()
    lib.xprc_client_transfer_in_hash_calc(receiver_account_arg, top_pending_return_hash_arg,
                                          last_hash_arg, current_hash_arg)
    current_hash_list = []
    for i in range(0, len(current_hash_arg)):
        current_hash_list.append(current_hash_arg[i])
        # print(current_hash_arg[i])
    # log.debug('-' * 5 + 'current_confirm_receive_transfer_hash' + '-' * 5)
    top_current_transfer_hash = ''.join(current_hash_list)
    # log.debug(top_current_transfer_hash)
    # log.debug(top_current_transfer_hash.encode('hex'))
    # print(len(top_current_transfer_hash))
    return top_current_transfer_hash
