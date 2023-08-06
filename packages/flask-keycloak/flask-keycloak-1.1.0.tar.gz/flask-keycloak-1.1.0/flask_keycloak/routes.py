# -*- coding: utf-8 -*-
import os

from flask import redirect, request, session

from .constants import Cookies, Defaults, QueryParams, Sessions, Tokens, URLs
from .log import logger as log
from .utils import keycloak_client, update_tokens, prune_tokens


kc = keycloak_client()


def keycloak_login():
    """ initialize the login flow """
    prune_tokens()
    auth_url, state = kc.authentication_url()
    session[Sessions.state] = state
    session[Sessions.referrer] = request.referrer or URLs.root_url
    log.debug('Redirecting to keycloak login URL')
    return redirect(auth_url)


def keycloak_callback():
    """ callback handler for login flow """
    log.debug('Processing callback from keycloak')
    code = request.args.get(QueryParams.code, Defaults.unknown)
    state = request.args.get(QueryParams.state, Defaults.unknown)

    # validate state
    if state != session.pop(Sessions.state, None):
        log.debug('Invalid state')
        return Response(status=400)

    # retrieve user info
    response = kc.authentication_callback(code)
    update_tokens(response)

    # redirect user back to the referrer
    log.debug('Redirecting back to the referrer')
    referrer = session.pop(Sessions.referrer, URLs.root_url)
    return redirect(referrer)
