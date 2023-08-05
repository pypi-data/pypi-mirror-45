#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zeroPy import proto


"""
    Create proto structure
"""


def create_proto(type, *args):
    _proto = None
    if len(args) != 1:
        return _proto

    if type == proto.CMD_NUMS['GetBalance']:
        _proto = proto.GetBalance()
    elif type == proto.CMD_NUMS['GetLastHash']:
        _proto = proto.GetLastHash()
    elif type == proto.CMD_NUMS['GetCounters']:
        _proto = proto.GetCounters()
    elif type == proto.CMD_NUMS['GetBlockSize']:
        hash, wtf = args[0]
        _proto = proto.GetBlockSize(hash)
    elif type == proto.CMD_NUMS['GetBlocks']:
        offset, limit = args[0]
        _proto = proto.GetBlocks(offset, limit)
    elif type == proto.CMD_NUMS['GetTransaction']:
        block_hash, t_hash = args[0]
        _proto = proto.GetTransaction(block_hash,t_hash)
    elif type == proto.CMD_NUMS['GetTransactions']:
        b_hash, wtf, offset, limit = args[0]
        _proto = proto.GetTransactions(b_hash, offset, limit)
    elif type == proto.CMD_NUMS['GetTransactionsByKey']:
        offset, limit = args[0]
        _proto = proto.GetTransactionsByKey(offset, limit)
    elif type == proto.CMD_NUMS['GetFee']:
        amount, wft = args[0]
        _proto = proto.GetFee(amount)
    elif type == proto.CMD_NUMS['CommitTransaction']:
        t, wtf = args[0]
        _proto = proto.SendTransaction(t)
    elif type == proto.CMD_NUMS['GetInfo']:
        key, wft = args[0]
        _proto = proto.GetInfo(key)
    elif type == proto.CMD_NUMS['CommitTransactionArray']:
        tr_list, wtf = args[0]
        _proto = proto.SendTransactionArray(tr_list)
    elif type == proto.CMD_NUMS['SendBuffer']:
        __buffer, wtf = args[0]
        _proto = proto.SendBuffer(__buffer)
    elif type == proto.CMD_NUMS['GetBuffer']:
        __buffer, wtf = args[0]
        _proto = proto.GetBuffer(__buffer)
    elif type == proto.CMD_NUMS['GetBufferPart']:
        __bufferPart, wtf = args[0]
        _proto = proto.GetBufferPart(__bufferPart)
    return _proto

"""
    create answer 
"""


def create_struct(type):
    _s = None
    _s = proto.BlockHash()
    if type == proto.CMD_NUMS['GetFee']:
        _s = proto.Balance()
    if type == proto.CMD_NUMS['GetBalance']:
        _s = proto.Balance()
    elif type == proto.CMD_NUMS['GetInfo']:
        _s = proto.PublicKey()
    elif type == proto.CMD_NUMS['GetCounters']:
        _s = proto.Counters()
    # elif type == proto.CMD_NUMS('GetBuffer'):
    #     _s = proto.Buffer()

    return _s


class ProtoMananger(object):
    def __init__(self):
        pass

    def form_cmd(self, _type):
        if _type is not proto.CMD_NUMS['GetBuffer'] or _type is not proto.CMD_NUMS['GetBufferPart']:
            cmd = _type + 1

        if _type == proto.CMD_NUMS['CommitTransaction']:
            cmd += 1
            if(_type == proto.CMD_NUMS['SendBuffer']):
                cmd = 19
        return cmd

    def recv_proto(self, _type):
        result = None
        if _type == 'Transaction':
            result = proto.Transaction()
        elif _type == 'BlockHash':
            result = proto.BlockHash()
        elif _type == 'BlockSize':
            result = proto.BlockSize()
        elif _type == 'Termblock':
            result = proto.TerminatingBlock()
        return result
