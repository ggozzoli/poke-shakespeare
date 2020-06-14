import logging

from injector import inject
from requests import RequestException

from core.exceptions import ServiceError
from core.services import DescriptionService
from core.wrappers import PokemonInfoWrapper, ShakespeareTranslationWrapper

logger = logging.getLogger(f'{__name__}')


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
        logger.debug(f'Get pokemon shakespeare description (pokemon_name: {pokemon_name}).')

        try:
            description = self._pokemon_info_wrapper.get_description(pokemon_name=pokemon_name)
            shakespeare_description = self._shakespeare_translation_wrapper.translate(text=description)
            return shakespeare_description
        except RequestException:
            raise ServiceError
