import json
import logging
import os
from logging import config

from flask import Flask, jsonify
from flask_injector import FlaskInjector
from flask_restful import Api
from injector import Injector, Module, singleton, provider
from redis import StrictRedis
from waitress import serve
from werkzeug.exceptions import NotFound, TooManyRequests

from api.resources.pokemon_description import PokemonDescriptionResource
from core.repositories import RedisRepository
from core.services import DescriptionService
from core.wrappers import PokemonInfoWrapper, ShakespeareTranslationWrapper
from repositories.redis import RedisRepositoryImpl
from services.description_service import DescriptionServiceImpl
from wrappers.pokemon_info import PokemonInfoWrapperImpl
from wrappers.shakespeare_translation import ShakespeareTranslationWrapperImpl

with open(os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf'), 'rb') as logging_config_file:
    config.dictConfig(json.loads(logging_config_file.read()))

logger = logging.getLogger(f'{__name__}')


class Application(Flask):

    def __init__(self, injector=None):
        super().__init__(__name__)

        self._api = ApplicationApi(self)
        self._api.add_resource(PokemonDescriptionResource, '/pokemon/<string:pokemon_name>', endpoint='pokemon_desc')

        if not injector:
            injector = Injector(modules=[ApplicationModule()])
        FlaskInjector(app=self, injector=injector)


class ApplicationApi(Api):

    def __init__(self, application):
        super().__init__(app=application)


class ApplicationModule(Module):

    def __init__(self):
        logger.info('Configure application injection module.')

    def configure(self, binder):
        binder.bind(interface=DescriptionService, to=DescriptionServiceImpl, scope=singleton)
        binder.bind(interface=PokemonInfoWrapper, to=PokemonInfoWrapperImpl, scope=singleton)
        binder.bind(interface=ShakespeareTranslationWrapper, to=ShakespeareTranslationWrapperImpl, scope=singleton)
        binder.bind(interface=RedisRepository, to=RedisRepositoryImpl, scope=singleton)

    @provider
    @singleton
    def provide_redis_client(self) -> StrictRedis:
        return StrictRedis(host='redis', port=6379, charset='utf-8', decode_responses=True)


app = Application()


@app.errorhandler(NotFound)
def handle_exception(e):
    return jsonify({"error": e.description}), e.code


@app.errorhandler(TooManyRequests)
def handle_exception(e):
    return jsonify({"error": e.description}), e.code


if __name__ == '__main__':
    logger.info('Application is running.')
    serve(app, host='0.0.0.0', port=5000)
