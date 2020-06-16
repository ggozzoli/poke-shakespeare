import logging

from injector import inject
from redis import StrictRedis, RedisError

from core.exceptions import RepositoryError
from core.repositories import RedisRepository

logger = logging.getLogger(f'{__name__}')


class RedisRepositoryImpl(RedisRepository):

    @inject
    def __init__(self, redis_client: StrictRedis):
        self._redis = redis_client

    def get_key(self, name: str):
        logger.debug(f'Get key from redis (name: {name}).')
        try:
            return self._redis.get(name=name)
        except RedisError:
            raise RepositoryError

    def save(self, name: str, value):
        logger.debug(f'Save key to redis (name: {name}, value: {value}).')
        try:
            return self._redis.set(name=name, value=value)
        except RedisError:
            raise RepositoryError
