#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zeroPy import socket_manager as h
from zeroPy import proto as p
from zeroPy import signer
from zeroPy import structs as s

class apiClient(object):
    _handler = None
    private_key = None
    public_key = None

    def __init__(self):
        self._handler = h.SocketManager()

    def set_keys(self,
                 pub_key,
                 pr_key):
        self.public_key = pub_key
        self.private_key = pr_key

    def get_counters(self):
        if not self._handler.is_connected():
            return

        r_counters = self._handler.method(
                                    _type=p.CMD_NUMS['GetCounters'],
                                    term_block=True)
        if r_counters is None:
            return

        counters = s.Counters()
        counters.set_vals(r_counters.blocks,
                          r_counters.transactions)
        return counters

    def get_last_hash(self):
        if not self._handler.is_connected():
            return

        r_block_hash = self._handler.method(
                                _type=p.CMD_NUMS['GetLastHash'],
                                term_block=True)

        block = s.Block()
        block.set_hash(r_block_hash.get_hash())
        return block

    def get_block_size(self, block_hash):
        if not self._handler.is_connected():
            return

        block_hash = self._handler.method(block_hash,
                                          'wtf',
                                          _type=p.CMD_NUMS['GetBlockSize'],
                                          term_block=False)
        if block_hash is None:
            return

        block_size = self._handler.recv_into('BlockSize').values[0]

        return block_size

    def get_transactions(self,
                         block_hash,
                         offset,
                         limit):
        if not self._handler.is_connected():
            return

        block_hash = self._handler.method(block_hash,
                                        'wft',
                                        offset,
                                        limit,
                                        _type=p.CMD_NUMS['GetTransactions'],
                                        term_block=False)


        txs_list = []

        hash_size = 64
        txs_list_size = self._handler.response.size - hash_size

        if txs_list_size % hash_size > 0:
            return txs_list
        txs_count = int(txs_list_size / hash_size)
        print(txs_count)
        for i in range(0, txs_count):
            hash = self._handler.recv_into('BlockHash')
            if hash is None:
                return

            hash = hash.get_hash()
            txs_list.append(hash)

        self._handler.recv_term_block()

        return txs_list


    def get_blocks(self,
                   offset,
                   limit):
        if not self._handler.is_connected():
            return


        hash  = self._handler.method(offset,
                             limit,
                             _type=p.CMD_NUMS['GetBlocks'],
                                    term_block=False)




        blocks = []
        block_size = 64
        blocks_count = int(self._handler.response.size / block_size)

        block = s.Block()
        block.set_hash(hash.get_hash())
        blocks.append(block)

        for b in range(0, blocks_count-1):
            block_hash = self._handler.recv_into('BlockHash')
            block = s.Block()
            block.set_hash(block_hash.get_hash())
            blocks.append(block)


        return blocks

    def get_transaction(self,
                        b_hash,
                        t_hash):
        if not self._handler.is_connected():
            return None

        bloch_hash = self._handler.method(b_hash,
                                  t_hash,
                                  _type=p.CMD_NUMS['GetTransaction'],
                                    term_block=False)


        tx = self._handler.recv_into('Transaction')

        t = s.Transaction()
        t.parse(tx.values)

        return t

    def send_info(self,
                  key):
        if not self._handler.is_connected():
            return False

        resp_key = self._handler.method(key,
                                        'wtf',
                                        _type=p.CMD_NUMS['GetInfo'],
                                        term_block=True)
        if resp_key is None:
            return None

        return resp_key

    def get_balance(self):
        if not self._handler.is_connected():
            return

        balance = self._handler.method(
                _type=p.CMD_NUMS['GetBalance'],
                term_block=True)

        if balance is None:
            return None

        amount = s.Amount()
        amount.set_amount(balance.integral,
                          balance.fraction)

        return amount

    def get_transactionsbykey(self,
                              offset,
                              limit):
        if not self._handler.is_connected():
            return

        answer = self._handler.method(offset,
                                      limit,
                                      _type=p.CMD_NUMS['GetTransactionsByKey'],
                                      term_block=False)

        if answer is None:
            return

        txs = []

        tx_size = p.calcsize('=%s' % p.F_TRANSACTION)
        util_size = p.calcsize('=%s' % p.F_HASH)
        txs_buffer_size = self._handler.response.size - util_size

        if txs_buffer_size % tx_size > 0:
            return None

        txs_count = int(txs_buffer_size /
                        tx_size)

        for i in range(0, txs_count):
            tx = self._handler.recv_into('Transaction')
            t = s.Transaction()
            t.parse(tx.values)
            txs.append(t)

        return txs

    def get_fee(self,
                amount):
        if not self._handler.is_connected():
            return False

        fee = self._handler.method(amount,
                                   'wft',
                                   _type=p.CMD_NUMS['GetFee'],
                                    term_block=True)

        _amount = s.Amount()
        _amount.set_amount(fee.integral, fee.fraction)
        return _amount

    def send_transaction(self,
                         target,
                         intg,
                         frac):
        if not self._handler.is_connected():
            return False

        t = signer.transaction(self.private_key,
                               self.public_key,
                               target,
                               intg,
                               frac)


        answer = self._handler.method(t,
                                      'wtf',
                                      _type=p.CMD_NUMS['CommitTransaction'],
                                      term_block=True)

        return True


    def sendbuffer(self,_buffer):
        if not self._handler.is_connected():
            return False



        answer = self._handler.method(_buffer,
                                      'wtf',
                                      _type=p.CMD_NUMS['SendBuffer'],
                                      term_block=True)

        return True


    def getbuffer(self, hash , id_onblock = 0):
        if not self._handler.is_connected():
            return False

        buffer = s.BinaryPart()
        buffer.hash = hash
        buffer.id_onblock = id_onblock
        _buffer = self._handler.method(buffer,
                                      'wtf',
                                      _type=p.CMD_NUMS['GetBuffer'],
                                      term_block=True)

        return _buffer



    #allows get no full buffer, but part of it
    def getBufferHeader(self):
        if not self._handler.is_connected():
            return False


    def send_transaction_array(self, tr_data):
        tr_list = []

        for data in tr_data:
            target, high, low = data
            t = signer.transaction(self.private_key,
                                   self.public_key,
                                   target,
                                   high,
                                   low)
            tr_list.append(t)


        answer = self._handler.method(tr_list,
                                      'wtf',
                                      _type=p.CMD_NUMS['CommitTransactionArray'],
                                      term_block=True)
        return True
