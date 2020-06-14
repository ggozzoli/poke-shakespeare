from abc import ABC, abstractmethod


class DescriptionService(ABC):

    @abstractmethod
    def get_shakespeare_description(self, pokemon_name: str) -> str:
        pass
