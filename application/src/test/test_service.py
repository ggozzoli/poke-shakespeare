from unittest import TestCase
from unittest.mock import Mock

from injector import Module, Injector, singleton
from requests import RequestException
from werkzeug.exceptions import NotFound, TooManyRequests

from core.exceptions import ServiceError, RepositoryError
from core.repositories import RedisRepository
from core.services import DescriptionService
from core.wrappers import PokemonInfoWrapper, ShakespeareTranslationWrapper
from services.description_service import DescriptionServiceImpl


class TestCaseModule(Module):

    def __init__(
            self,
            pokemon_info_wrapper: PokemonInfoWrapper,
            shakespeare_translation_wrapper: ShakespeareTranslationWrapper,
            redis_repository: RedisRepository
    ):
        self._pokemon_info_wrapper = pokemon_info_wrapper
        self._shakespeare_translation_wrapper = shakespeare_translation_wrapper
        self._redis_repository = redis_repository

    def configure(self, binder):
        super().configure(binder)
        binder.bind(interface=DescriptionService, to=DescriptionServiceImpl, scope=singleton)
        binder.bind(interface=PokemonInfoWrapper, to=self._pokemon_info_wrapper, scope=singleton)
        binder.bind(interface=ShakespeareTranslationWrapper, to=self._shakespeare_translation_wrapper, scope=singleton)
        binder.bind(interface=RedisRepository, to=self._redis_repository, scope=singleton)


class PokemonDescriptionResourceTestCase(TestCase):

    def setUp(self):
        self._pokemon_info_wrapper: PokemonInfoWrapper = Mock(PokemonInfoWrapper)
        self._shakespeare_translation_wrapper: ShakespeareTranslationWrapper = Mock(ShakespeareTranslationWrapper)
        self._redis_repository: RedisRepository = Mock(RedisRepository)

        module = TestCaseModule(
            self._pokemon_info_wrapper,
            self._shakespeare_translation_wrapper,
            self._redis_repository
        )

        injector = Injector(modules=[module])
        self._description_service: DescriptionService = injector.get(DescriptionService)

    def test_get_shakespeare_description_successful(self):
        self._redis_repository.get_key = Mock(return_value=None)
        self._pokemon_info_wrapper.get_description = Mock(return_value='pokemon_description')
        self._shakespeare_translation_wrapper.translate = Mock(return_value='shakespeare_translation')
        result = self._description_service.get_shakespeare_description(pokemon_name='pokemon_name')
        self.assertEqual('shakespeare_translation', result)

    def test_get_shakespeare_description_cached(self):
        self._redis_repository.get_key = Mock(return_value='cached')
        self._pokemon_info_wrapper.get_description = Mock(return_value='pokemon_description')
        result = self._description_service.get_shakespeare_description(pokemon_name='pokemon_name')
        self.assertEqual('cached', result)

    def test_get_shakespeare_description_not_found(self):
        self._redis_repository.get_key = Mock(return_value=None)
        self._pokemon_info_wrapper.get_description = Mock(side_effect=NotFound)
        with self.assertRaises(NotFound):
            self._description_service.get_shakespeare_description(pokemon_name='pokemon_name')

    def test_get_shakespeare_description_too_many_requests(self):
        self._redis_repository.get_key = Mock(return_value=None)
        self._pokemon_info_wrapper.get_description = Mock(return_value='pokemon_description')
        self._shakespeare_translation_wrapper.translate = Mock(side_effect=TooManyRequests)
        with self.assertRaises(TooManyRequests):
            self._description_service.get_shakespeare_description(pokemon_name='pokemon_name')

    def test_get_shakespeare_description_service_error(self):
        self._redis_repository.get_key = Mock(return_value=None)
        self._pokemon_info_wrapper.get_description = Mock(side_effect=RequestException)
        with self.assertRaises(ServiceError):
            self._description_service.get_shakespeare_description(pokemon_name='pokemon_name')

    def test_get_shakespeare_description_get_key_repository_error(self):
        self._redis_repository.get_key = Mock(side_effect=RepositoryError)
        self._pokemon_info_wrapper.get_description = Mock(return_value='pokemon_description')
        self._shakespeare_translation_wrapper.translate = Mock(return_value='shakespeare_translation')
        result = self._description_service.get_shakespeare_description(pokemon_name='pokemon_name')
        self.assertEqual('shakespeare_translation', result)

    def test_get_shakespeare_description_save_key_repository_error(self):
        self._redis_repository.get_key = Mock(return_value=None)
        self._redis_repository.save = Mock(side_effect=RepositoryError)
        self._pokemon_info_wrapper.get_description = Mock(return_value='pokemon_description')
        self._shakespeare_translation_wrapper.translate = Mock(return_value='shakespeare_translation')
        result = self._description_service.get_shakespeare_description(pokemon_name='pokemon_name')
        self.assertEqual('shakespeare_translation', result)
