from injector import inject

from core.services import DescriptionService
from core.wrappers import PokemonInfoWrapper, ShakespeareTranslationWrapper


class DescriptionServiceImpl(DescriptionService):

    @inject
    def __init__(
            self,
            pokemon_info_wrapper: PokemonInfoWrapper,
            shakespeare_translation_wrapper: ShakespeareTranslationWrapper
    ):
        self._pokemon_info_wrapper = pokemon_info_wrapper
        self._shakespeare_translation_wrapper = shakespeare_translation_wrapper

    def get_shakespeare_description(self, pokemon_name: str) -> str:
        pass
