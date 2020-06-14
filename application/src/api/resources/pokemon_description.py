import logging

from flask_restful import Resource
from injector import inject

logger = logging.getLogger(f'{__name__}')


class PokemonDescriptionResource(Resource):

    @inject
    def __init__(self):
        pass

    def get(self, pokemon_name):
        logger.info(f'Get pokemon description (pokemon_name: {pokemon_name}).')
        return {'name': pokemon_name}
