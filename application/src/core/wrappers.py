from abc import ABC, abstractmethod


class PokemonInfoWrapper(ABC):

    @abstractmethod
    def get_description(self, pokemon_name: str) -> str:
        pass


class ShakespeareTranslationWrapper(ABC):

    @abstractmethod
    def translate(self, text: str) -> str:
        pass
