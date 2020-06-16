from unittest import TestCase
from unittest.mock import Mock

from injector import Module, Injector, singleton
from redis import StrictRedis, RedisError

from core.exceptions import RepositoryError
from core.repositories import RedisRepository
from repositories.redis import RedisRepositoryImpl


class TestCaseModule(Module):

    def __init__(self, redis: StrictRedis):
        self._redis = redis

    def configure(self, binder):
        super().configure(binder)
        binder.bind(interface=StrictRedis, to=self._redis, scope=singleton)
        binder.bind(interface=RedisRepository, to=RedisRepositoryImpl, scope=singleton)


class RedisRepositoryTestCase(TestCase):

    def setUp(self):
        self._redis: StrictRedis = Mock(StrictRedis)
        module = TestCaseModule(self._redis)
        injector = Injector(modules=[module])
        self._redis_repository: RedisRepository = injector.get(RedisRepository)

    def test_get_key_successful(self):
        self._redis.get = Mock(return_value='value')
        result = self._redis_repository.get_key(name='name')
        self.assertEqual('value', result)

    def test_get_key_redis_error(self):
        self._redis.get = Mock(side_effect=RedisError)
        with self.assertRaises(RepositoryError):
            self._redis_repository.get_key(name='name')

    def test_save_successful(self):
        self._redis.set = Mock(return_value=None)
        self._redis_repository.save(name='name', value='value')
        self._redis.set.assert_called_once_with(name='name', value='value')

    def test_save_redis_error(self):
        self._redis.set = Mock(side_effect=RedisError)
        with self.assertRaises(RepositoryError):
            self._redis_repository.save(name='name', value='value')
