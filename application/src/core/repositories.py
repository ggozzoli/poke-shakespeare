from abc import ABC, abstractmethod


class RedisRepository(ABC):

    @abstractmethod
    def get_key(self, name: str):
        pass

    @abstractmethod
    def save(self, name: str, value):
        pass
