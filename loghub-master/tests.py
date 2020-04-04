import loghub
import unittest
import json
import datetime
from redis import StrictRedis


class LoghubTestCase(unittest.TestCase):
    def setUp(self):
        loghub.app.testing = True
        self.app = loghub.app.test_client()

        self.redis = StrictRedis(host='localhost', port=6379, db=0)

    def tearDown(self):
        pass

    def test_no_logs(self):
        rv = self.app.get('/logs')
        assert (b'' in rv.data)

    # def test_get_log(self):
    #     self.add_log('test')
    #     rv = self.app.get('/logs/test')
    #     assert b'1.0' in rv.data
    #     assert str(datetime.datetime(day=1, month=1, year=1, hour=1, minute=1, second=1)).encode('utf-8') in rv.data
    #     self.remove_logs()

    def test_del_log(self):
        self.add_log('test1')
        self.add_log('test2')
        self.app.delete('/logs/test1')
        assert self.redis.exists('test1') is False
        assert self.redis.exists('test2') is True
        self.remove_logs()

    def test_create_log(self):
        self.redis.delete('log_id')
        self.redis.delete('log')
        rv = self.app.post('/logs')
        log = self.redis.hgetall('log')
        assert log is not None
        assert log['id'.encode('utf-8')].decode('utf-8') is json.loads(rv.data.decode('utf-8'))['id']

    def add_log(self, log_id):
        self.redis.lpush(log_id, json.dumps(
            {'datetime': json.dumps(str(datetime.datetime(day=1, month=1, year=1, hour=1, minute=1, second=1))),
             'data': 1.0}))

    def remove_logs(self):
        self.redis.flushall()


if __name__ == '__main__':
    unittest.main()
