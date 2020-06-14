import json
import logging
import os
from logging import config

from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api
from injector import Injector, Module

with open(os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf'), 'rb') as logging_config_file:
    config.dictConfig(json.loads(logging_config_file.read()))

logger = logging.getLogger(f'{__name__}')


class Application(Flask):

    def __init__(self, injector=None):
        super().__init__(__name__)

        self._api = ApplicationApi(self)

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
        pass


app = Application()

if __name__ == '__main__':
    app.run(port=5000)
