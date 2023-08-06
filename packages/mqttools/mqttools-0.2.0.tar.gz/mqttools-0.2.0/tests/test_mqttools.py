import logging
import asyncio
import unittest
import threading
import binascii
import queue
import socket

import mqttools


HOST = 'localhost'
PORT = 0


class Broker(threading.Thread):

    EXPECTED_DATA_INDEX = 0
    EXPECTED_DATA_STREAM = []
    ACTUAL_DATA_STREAM = []

    def __init__(self):
        super().__init__()
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener.bind((HOST, PORT))
        self._listener.listen()
        self._client_closed = queue.Queue()

    @property
    def address(self):
        return self._listener.getsockname()

    def wait_for_client_closed(self):
        self._client_closed.get()

    def run(self):
        while True:
            print('Broker: Listening for client...')
            self.serve_client(self._listener.accept()[0])
            self._client_closed.put(True)

    def serve_client(self, client):
        print('Broker: Serving client...')

        while self.EXPECTED_DATA_INDEX < len(self.EXPECTED_DATA_STREAM):
            _, data = self.EXPECTED_DATA_STREAM[self.EXPECTED_DATA_INDEX]
            self.EXPECTED_DATA_INDEX += 1

            size = len(data)
            data = client.recv(size)
            # print(f'Broker: Received: {data}')
            self.ACTUAL_DATA_STREAM.append(('c2s', data))

            while self.EXPECTED_DATA_INDEX < len(self.EXPECTED_DATA_STREAM):
                direction, data = self.EXPECTED_DATA_STREAM[self.EXPECTED_DATA_INDEX]

                if direction != 's2c':
                    break

                self.EXPECTED_DATA_INDEX += 1
                # print(f'Broker: Sending: {data}')
                client.send(data)
                self.ACTUAL_DATA_STREAM.append(('s2c', data))

        client.close()


class MQTToolsTest(unittest.TestCase):

    def setUp(self):
        Broker.EXPECTED_DATA_INDEX = 0
        Broker.EXPECTED_DATA_STREAM = []
        Broker.ACTUAL_DATA_STREAM = []
        Broker.CLOSE_AFTER_INDEX = -1
        self.broker = Broker()
        self.broker.daemon = True
        self.broker.start()
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.broker.wait_for_client_closed()
        self.assertEqual(Broker.ACTUAL_DATA_STREAM, Broker.EXPECTED_DATA_STREAM)

    def run_until_complete(self, coro):
        return self.loop.run_until_complete(coro)

    def test_start_stop(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            (
                'c2s',
                b'\x10\x0f\x00\x04\x4d\x51\x54\x54\x04\x02\x00\x00\x00\x03\x62'
                b'\x61\x72'
            ),
            # CONNACK
            ('s2c', b'\x20\x02\x00\x00'),
            # DISCONNECT
            ('c2s', b'\xe0\x00')
        ]

        client = mqttools.Client(*self.broker.address, b'bar')
        self.run_until_complete(client.start())
        self.run_until_complete(client.stop())

    def test_subscribe(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            (
                'c2s',
                b'\x10\x0f\x00\x04\x4d\x51\x54\x54\x04\x02\x00\x00\x00\x03\x62'
                b'\x61\x72'
            ),
            # CONNACK
            ('s2c', b'\x20\x02\x00\x00'),
            # SUBSCRIBE
            ('c2s', b'\x82\x09\x00\x01\x00\x04\x2f\x61\x2f\x62\x00'),
            # SUBACK
            ('s2c', b'\x90\x03\x00\x01\x00'),
            # PUBLISH
            (
                's2c',
                b'\x30\x09\x00\x04\x2f\x61\x2f\x62\x61\x70\x61'
            ),
            # DISCONNECT
            ('c2s', b'\xe0\x00')
        ]

        client = mqttools.Client(*self.broker.address, b'bar')
        self.run_until_complete(client.start())
        self.run_until_complete(client.subscribe(b'/a/b', 0))
        topic, message = self.run_until_complete(client.messages.get())
        self.assertEqual(topic, b'/a/b')
        self.assertEqual(message, b'apa')
        self.run_until_complete(client.stop())

    def test_publish_qos_0(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            (
                'c2s',
                b'\x10\x0f\x00\x04\x4d\x51\x54\x54\x04\x02\x00\x00\x00\x03\x62'
                b'\x61\x72'
            ),
            # CONNACK
            ('s2c', b'\x20\x02\x00\x00'),
            # PUBLISH
            (
                'c2s',
                b'\x30\x0e\x00\x09\x2f\x74\x65\x73\x74\x2f\x66\x6f\x6f\x61'
                b'\x70\x61'
            ),
            # DISCONNECT
            ('c2s', b'\xe0\x00')
        ]

        client = mqttools.Client(*self.broker.address, b'bar')
        self.run_until_complete(client.start())
        self.run_until_complete(client.publish(b'/test/foo', b'apa', 0))
        self.run_until_complete(client.stop())


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    unittest.main()
