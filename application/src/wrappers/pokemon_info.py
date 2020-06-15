import logging

import requests
from werkzeug.exceptions import NotFound

from core.exceptions import ServiceError
from core.wrappers import PokemonInfoWrapper

logger = logging.getLogger(f'{__name__}')


class PokemonInfoWrapperImpl(PokemonInfoWrapper):

    def __init__(self):
        self._url = 'https://pokeapi.co/api/v2/pokemon-species/{pokemonName}'

    def get_description(self, pokemon_name: str) -> str:
        logger.debug(f'Get pokemon description (pokemon_name: {pokemon_name}).')

        url = self._url.format(pokemonName=pokemon_name)
        r = requests.get(url=url)
        if r.status_code == 200:
            description = self._extract_description(response=r.json())
            return description
        elif r.status_code == 404:
            raise NotFound(description='Pokemon not found.')
        else:
            raise ServiceError

    @staticmethod
    def _extract_description(response: dict) -> str:
        descriptions = response.get('flavor_text_entries')
        for description in descriptions:
            if description.get('language').get('name') == 'en':
                return description.get('flavor_text')
