import logging

import requests

from core.wrappers import ShakespeareTranslationWrapper

logger = logging.getLogger(f'{__name__}')


class ShakespeareTranslationWrapperImpl(ShakespeareTranslationWrapper):

    def __init__(self):
        self._url = 'https://api.funtranslations.com/translate/shakespeare'

    def translate(self, text: str) -> str:
        logger.debug(f'Translate text to shakespeare (text: {text}).')

        body = {'text': text}
        r = requests.post(url=self._url, json=body)
        translation = self._extract_translation(response=r.json())
        return translation

    @staticmethod
    def _extract_translation(response: dict) -> str:
        return response.get('contents').get('translated')
