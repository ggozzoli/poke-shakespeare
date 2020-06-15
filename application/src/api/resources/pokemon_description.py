import logging

from flask_restful import Resource
from injector import inject

from core.services import DescriptionService

logger = logging.getLogger(f'{__name__}')


class PokemonDescriptionResource(Resource):

    @inject
    def __init__(self, description_service: DescriptionService):
        self._description_service = description_service

    def get(self, pokemon_name):
        logger.info(f'Get pokemon shakespeare description (pokemon_name: {pokemon_name}).')

        description = self._description_service.get_shakespeare_description(pokemon_name=pokemon_name)

        return {'name': pokemon_name, 'description': description}
