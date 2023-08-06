# -*- coding: utf-8 -*-
from .constants import URLs
from .middlewares import keycloak_authentication
from .routes import keycloak_callback, keycloak_login


class FlaskKeycloak:
    """ Keycloak extension for flask """

    def __init__(self, app, base_url=''):
        """ initialize object """
        self.app = app
        self.base_url = base_url
        self.init_app(app)

    @property
    def login_url(self):
        return self.base_url + URLs.login_url

    @property
    def callback_url(self):
        return self.base_url + URLs.callback_url

    def init_app(self, app):
        """ initialize flask app """

        # register routes
        app.add_url_rule(self.login_url, 'keycloak_login', keycloak_login)
        app.add_url_rule(self.callback_url, 'keycloak_callback', keycloak_callback)

        # register middlewares
        authentication_middleware = keycloak_authentication(self.login_url, self.callback_url)
        app.before_request(authentication_middleware)
