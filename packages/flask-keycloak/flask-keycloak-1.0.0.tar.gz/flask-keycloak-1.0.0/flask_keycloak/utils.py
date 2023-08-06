# -*- coding: utf-8 -*-
import os
from flask import session
from keycloak import KeycloakClient

from .constants import Cookies, Tokens
from .log import logger as log


def keycloak_client():
    log.debug('Initializing keycloak client')
    default = os.path.join(os.getcwd(), 'keycloak.json')
    config_file = os.getenv('KEYCLOAK_CONFIG_FILE', default)
    return KeycloakClient(config_file=config_file)


def update_tokens(response):
    log.debug('Updating tokens')
    session[Cookies.kc_id_token] = response[Tokens.id_token]
    session[Cookies.kc_access_token] = response[Tokens.access_token]
    session[Cookies.kc_refresh_token] = response[Tokens.refresh_token]


def prune_tokens():
    log.debug('Pruning tokens')
    session.pop(Cookies.kc_id_token, None)
    session.pop(Cookies.kc_access_token, None)
    session.pop(Cookies.kc_refresh_token, None)
