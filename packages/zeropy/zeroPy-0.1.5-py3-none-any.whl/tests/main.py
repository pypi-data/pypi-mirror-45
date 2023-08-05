import zeroPy

if __name__ == '__main__':
    client = zeroPy.apiClient()
    client._handler.connect('10.0.0.61',38100)
    test_key = b'53c0aecece0a3d9e2e69230c977e874c8dda4a2fe1f162af98979e69bc27f859'
    client.send_info(test_key)
    for _ in range(0, 10):
        print('-----------Blocks---------')
        print('blokcs ', client.get_counters().blocks)