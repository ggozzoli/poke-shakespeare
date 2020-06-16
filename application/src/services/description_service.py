import logging

from injector import inject
from requests import RequestException

from core.exceptions import ServiceError, RepositoryError
from core.repositories import RedisRepository
from core.services import DescriptionService
from core.wrappers import PokemonInfoWrapper, ShakespeareTranslationWrapper

logger = logging.getLogger(f'{__name__}')


class DescriptionServiceImpl(DescriptionService):

    @inject
    def __init__(
            self,
            pokemon_info_wrapper: PokemonInfoWrapper,
            shakespeare_translation_wrapper: ShakespeareTranslationWrapper,
            redis_repository: RedisRepository
    ):
        self._pokemon_info_wrapper = pokemon_info_wrapper
        self._shakespeare_translation_wrapper = shakespeare_translation_wrapper
        self._redis_repository = redis_repository

    def get_shakespeare_description(self, pokemon_name: str) -> str:
        logger.debug(f'Get pokemon shakespeare description (pokemon_name: {pokemon_name}).')

        try:
            value = self._redis_repository.get_key(name=pokemon_name)
            if value:
                return value
        except RepositoryError:
            pass

        try:
            description = self._pokemon_info_wrapper.get_description(pokemon_name=pokemon_name)
            shakespeare_description = self._shakespeare_translation_wrapper.translate(text=description)

            try:
                self._redis_repository.save(name=pokemon_name, value=shakespeare_description)
            except RepositoryError:
                pass

            return shakespeare_description
        except RequestException:
            raise ServiceError
