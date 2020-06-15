from unittest import TestCase

from injector import Module, Injector, singleton
from requests_mock import Mocker
from werkzeug.exceptions import NotFound

from core.exceptions import ServiceError
from core.wrappers import PokemonInfoWrapper
from wrappers.pokemon_info import PokemonInfoWrapperImpl


class TestCaseModule(Module):

    def __init__(self, ):
        pass

    def configure(self, binder):
        super().configure(binder)
        binder.bind(interface=PokemonInfoWrapper, to=PokemonInfoWrapperImpl, scope=singleton)


class PokemonInfoWrapperTestCase(TestCase):

    def setUp(self):
        module = TestCaseModule()
        injector = Injector(modules=[module])
        self._pokemon_info_wrapper: PokemonInfoWrapper = injector.get(PokemonInfoWrapper)
        self._url = 'https://pokeapi.co/api/v2/pokemon-species/{pokemonName}'
        self._json = {'flavor_text_entries': [{'flavor_text': 'pokemon_description', 'language': {'name': 'en'}}]}

    def test_get_description_successful(self):
        pokemon_name = 'pokemon_name'
        with Mocker() as m:
            url = self._url.format(pokemonName=pokemon_name)
            m.get(url=url, json=self._json)
            result = self._pokemon_info_wrapper.get_description(pokemon_name=pokemon_name)
            self.assertEqual('pokemon_description', result)

    def test_get_description_not_found(self):
        with Mocker() as m:
            url = self._url.format(pokemonName='pokemon_name')
            m.get(url=url, status_code=404)
            with self.assertRaises(NotFound):
                self._pokemon_info_wrapper.get_description(pokemon_name='pokemon_name')

    def test_get_description_service_error(self):
        with Mocker() as m:
            url = self._url.format(pokemonName='pokemon_name')
            m.get(url=url, status_code=500)
            with self.assertRaises(ServiceError):
                self._pokemon_info_wrapper.get_description(pokemon_name='pokemon_name')
