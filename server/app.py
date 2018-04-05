# -*- coding: utf-8 -*-

import os
from flask import Flask
from server.api import api
from server.apiErrors import apiErrors
from flask_cors import CORS
from locatorInitializer import LocatorInitializer

def create_app(settings_overrides=None):
    app = Flask(__name__)
    CORS(app)
    configure_settings(app, settings_overrides)
    configure_error_handlers(app)
    configure_blueprints(app)
    initializeObjects(app)
    return app


def configure_settings(app, settings_override):
    parent = os.path.dirname(__file__)
    data_path = os.path.join(parent, '..', 'data')
    app.config.update({
        'DEBUG': True,
        'TESTING': False,
        'DATA_PATH': data_path
    })
    if settings_override:
        app.config.update(settings_override)


def configure_blueprints(app):
    app.register_blueprint(api)
    api

def configure_error_handlers(app):
    app.register_blueprint(apiErrors)

#not sure about the convention in Flask, this might not be the recommended place to do it
def initializeObjects(app):
    initializer = LocatorInitializer()
    app.Locator = initializer.Initialize(data_path(app,'shops.csv'),data_path(app,'tags.csv'),data_path(app,'taggings.csv'),data_path(app,'products.csv'))

def data_path(app, filename):
    data_path = app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)
