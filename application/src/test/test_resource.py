from unittest import TestCase
from unittest.mock import Mock

from flask import Response
from injector import Module, Injector, singleton
from werkzeug.exceptions import NotFound, TooManyRequests

from api.app import Application
from core.services import DescriptionService


class TestCaseModule(Module):

    def __init__(self, description_service: DescriptionService):
        self._description_service = description_service

    def configure(self, binder):
        super().configure(binder)
        binder.bind(interface=DescriptionService, to=self._description_service, scope=singleton)


class PokemonDescriptionResourceTestCase(TestCase):

    def setUp(self):
        self._description_service: DescriptionService = Mock(DescriptionService)
        module = TestCaseModule(self._description_service)
        injector = Injector(modules=[module])
        self._client = Application(injector).test_client()

    def test_get_pokemon_description_success(self):
        self._description_service.get_shakespeare_description = Mock(return_value='pokemon_description')
        response: Response = self._client.get(path=f'/pokemon/pokemon_name')
        self.assertEqual(200, response.status_code)

    def test_get_pokemon_description_not_found(self):
        self._description_service.get_shakespeare_description = Mock(side_effect=NotFound)
        response: Response = self._client.get(path=f'/pokemon/pokemon_name')
        self.assertEqual(404, response.status_code)

    def test_get_pokemon_description_too_many_requests(self):
        self._description_service.get_shakespeare_description = Mock(side_effect=TooManyRequests)
        response: Response = self._client.get(path=f'/pokemon/pokemon_name')
        self.assertEqual(429, response.status_code)
