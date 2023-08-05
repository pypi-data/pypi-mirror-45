#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zeroPy.client
import unittest
from tests.utils import *


class TestClient(unittest.TestCase):
    key_dir = 'test_keys/keys/'

    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.host = '91'
        self.port = 38100

        self.test_client = rsapi.apiClient()


    def setUp(self):
        self.test_client._handler.connect(host=self.host,
                                          port=self.port)


    def tearDown(self):
        self.test_client._handler.disconnect()


    #@unittest.skip("GetBalance")
    def test_get_balance(self):
        #test_key = load_pub_key(self.key_dir)
        test_key = b'53c0aecece0a3d9e2e69230c977e874c8dda4a2fe1f162af98979e69bc27f859'
        self.test_client.send_info(test_key)

        amount = self.test_client.get_balance()

        self.assertIsNotNone(self.test_client._handler.response)
        if self.test_client._handler.response is not None:
            self.assertTrue(self.test_client._handler.response.check())


    #@unittest.skip("GetCounters")
    def test_get_counters(self):
        test_key = load_pub_key(self.key_dir)
        self.test_client.send_info(test_key)

        counters = self.test_client.get_counters()
        print(counters.blocks)
        print(counters.transactions)

        self.assertIsNotNone(self.test_client._handler.response)
        self.assertTrue(self.test_client._handler.response.check())
        self.assertIsInstance(counters, rsapi.Counters)
        #self.assertEqual(counters.blocks, 4)
        #self.assertEqual(counters.transactions, 1406)

    @unittest.skip("GetLastHash")
    def test_get_last_hash(self):
        last_hash = self.test_client.get_last_hash()



        self.assertIsNotNone(self.test_client._handler.response)
        if self.test_client._handler.response is not None:
            self.assertTrue(self.test_client._handler.response.check())
            self.assertEqual(len(last_hash.hash), 64)
            self.assertEqual(len(last_hash.hash_hex), 128)

    @unittest.skip("GetBlockSize")
    def test_get_block_size(self):
        e_pub_key = (b'12cdadbc73da73cbd9985b2a41ffdb8d')
        self.test_client.send_info(e_pub_key)


        b_hash = b'1bb6058bb2e6f7fb44c60f25b5f963b75e49adb89a90aa15a8e48c0ece6c229ad52' \
                 b'0029bba723960b3f0c81' \
            b'c61bae2378a4ce79d0d722d59b0e5aabfd67cbfea'

        block_size = self.test_client.get_block_size(b_hash)
        print(block_size)

        self.assertIsNotNone(self.test_client._handler.response)
        if self.test_client._handler.response is not None:
            self.assertTrue(self.test_client._handler.response.check())
            self.assertEqual(block_size, 694)


    #@unittest.skip("GetBlocks")
    def test_get_blocks(self):
        offset = 0
        limit = 50

        e_pub_key = (b'12cdadbc73da73cbd9985b2a41ffdb8d')
        self.test_client.send_info(e_pub_key)

        blocks = self.test_client.get_blocks(offset,
                                             limit)


        self.assertIsNotNone(self.test_client._handler.response)
        self.assertTrue(self.test_client._handler.response.check())
        self.assertGreater(len(blocks), 0)
        self.assertEqual(len(blocks), 3)


    #@unittest.skip("GetTransaction")
    def test_get_transaction(self):
        e_pub_key = (b'12cdadbc73da73cbd9985b2a41ffdb8d')
        self.test_client.send_info(e_pub_key)

        b_hash = b'D6B004EFC377D2126E750BE6260FEBA7555D1051488FB7691E3A4A8F1ECA4' \
                 b'27780A935706AB3F5DCA4C46F9F80E0DDABD4D226F40C054BD6A92EDBB9AC1DD92E'

        t_hash = b'044EE5CBA6BACB2466B1A6EF98B59BEA7F7DA977AA615DCD8C43E5035ADCE4B1407D2EAB3' \
                 b'F45133A4F483F1D8A58567AF06EBCACF9C85F4D5FCE61FCD502D106'

        t = self.test_client.get_transaction(b_hash, t_hash)


        self.assertIsNotNone(self.test_client._handler.response)
        self.assertTrue(self.test_client._handler.response.check())
        self.assertEqual(t.amount.integral, 1000)
        self.assertIsInstance(t, rsapi.Transaction)


    @unittest.skip("GetTransactions")
    def test_get_transactions(self):

        b_hash = b'1bb6058bb2e6f7fb44c60f25b5f963b75e49adb89a90aa15a8e48c0ece6c229ad520029bba723960b3f0c81' \
                 b'c61bae2378a4ce79d0d722d59b0e5aabfd67cbfea'
        offset = 0
        limit = 20

        txs = self.test_client.get_transactions(b_hash,
                                                offset,
                                                limit)


        self.assertIsNotNone(self.test_client._handler.response)
        self.assertTrue(self.test_client._handler.response.check())

        self.assertEqual(len(txs), 20)



    #@unittest.skip("transactionsbykey")
    def test_get_transactionsbykey(self):
        offset = 0
        limit = 3

        test_key = load_pub_key(self.key_dir)

        self.test_client.send_info(test_key)
        txs = self.test_client.get_transactionsbykey(offset, limit)

        self.assertIsNotNone(self.test_client._handler.response)
        self.assertTrue(self.test_client._handler.response.check())

        self.assertEqual(len(txs), 3)


    @unittest.skip("get_fee")
    def test_get_fee(self):
        #test_key = load_pub_key(self.key_dir)
        # test_key = (b'c1c02d12cdadbc73da73cbd9985b2a41ffdb8dba9de470eaab453cc3595'
        #            b'eaead')
        # test_key = binascii.unhexlify(test_key)
        temp = rsapi.Amount()
        temp.integral = 1000
        temp.fraction = 0

        #self.test_client.send_info(test_key)
        fee = self.test_client.get_fee(temp)


        self.assertIsNotNone(self.test_client._handler.response)
        self.assertTrue(self.test_client._handler.response.check())
        self.assertEqual(fee.integral, 100)
        self.assertEqual(fee.fraction, 0)


    @unittest.skip("send_info")
    def test_send_info(self):
        test_key = load_pub_key(self.key_dir)
        resp_key = self.test_client.send_info(test_key)
        if not resp_key == None:
            print(binascii.hexlify(resp_key.values[0]))
        self.assertTrue(True)



    @unittest.skip("SendTransation")
    def test_send_transaction(self):
        import racrypt
        from os import path

        lib = racrypt.Crypto()
        lib.load(path.dirname(racrypt.__file__))
        lib.create_keys()

        e_pub_key = binascii.hexlify(lib.public_key)
        e_priv_key = binascii.hexlify(lib.private_key)

        self.test_client.set_keys(e_pub_key, e_priv_key)
        test_key = (b'4b335fb3f5fe4669fa2bc7b384d68c377f4e4c1fec878e82bd09158ddb'
                    b'0c77f2')

        self.test_client.send_info(e_pub_key)

        amount = self.test_client.get_balance()

        target = test_key
        integral = 1
        fraction = 0

        ok = self.test_client.send_transaction(target,
                                               integral,
                                               fraction)

        self.assertIsNotNone(self.test_client._handler.response)


    def test_send_buffer(self):
        _buffer = bytearray(0)
        # TODO temp data in buffer + crc32 sum

        test_path = "pics/axe.png"
        with open(test_path, "rb") as image:
            f = image.read()
            _buffer += f
        ok = self.test_client.sendbuffer(_buffer)

    def test_get_buffer(self):
        _buffer = self.test_client.getbuffer()

        with open("pics/img.png", "wb") as file:
            file.write(_buffer)



    def test_send_transaction_array(self):

        key1, key2 = load_keys(self.key_dir)
        self.test_client.set_keys(key1, key2)

        self.test_client.send_info(key1)



        tr_data = []
        for _ in range(0, 1000):
            data = gen_transaction(40)
            tr_data.append(data)

        ok = self.test_client.send_transaction_array(tr_data)
        self.assertIsNotNone(self.test_client._handler.response)

if __name__ == '__main__':
    unittest.main()
