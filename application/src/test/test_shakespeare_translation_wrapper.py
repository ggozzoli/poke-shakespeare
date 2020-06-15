from unittest import TestCase

from injector import Module, Injector, singleton
from requests_mock import Mocker
from werkzeug.exceptions import TooManyRequests

from core.exceptions import ServiceError
from core.wrappers import ShakespeareTranslationWrapper
from wrappers.shakespeare_translation import ShakespeareTranslationWrapperImpl


class TestCaseModule(Module):

    def __init__(self, ):
        pass

    def configure(self, binder):
        super().configure(binder)
        binder.bind(interface=ShakespeareTranslationWrapper, to=ShakespeareTranslationWrapperImpl, scope=singleton)


class ShakespeareTranslationWrapperTestCase(TestCase):

    def setUp(self):
        module = TestCaseModule()
        injector = Injector(modules=[module])
        self._shakespeare_translation_wrapper: \
            ShakespeareTranslationWrapper = injector.get(ShakespeareTranslationWrapper)
        self._url = 'https://api.funtranslations.com/translate/shakespeare'
        self._json = {'contents': {'translated': 'translated_text'}}

    def test_translate_successful(self):
        with Mocker() as m:
            m.post(url=self._url, json=self._json)
            result = self._shakespeare_translation_wrapper.translate(text='text_to_translate')
            self.assertEqual('translated_text', result)

    def test_translate_too_many_requests(self):
        with Mocker() as m:
            m.post(url=self._url, status_code=429)
            with self.assertRaises(TooManyRequests):
                self._shakespeare_translation_wrapper.translate(text='text_to_translate')

    def test_translate_service_error(self):
        with Mocker() as m:
            m.post(url=self._url, status_code=500)
            with self.assertRaises(ServiceError):
                self._shakespeare_translation_wrapper.translate(text='text_to_translate')
