# -*- coding: utf-8 -*-
from jwt.exceptions import ExpiredSignatureError
from flask import g, redirect, request, session

from .constants import Cookies, Tokens
from .log import logger as log
from .utils import keycloak_client, update_tokens


kc = keycloak_client()


def keycloak_authentication(login_url, callback_url):
    """ decorator to parameterize authenticator """

    def authenticator():
        """ middleware to verify whether the user is authenticated or not """

        # do not perform check for login and callback urls
        if request.path in (login_url, callback_url):
            return

        # authentication check list
        check_list = (
            Cookies.kc_id_token in session,
            Cookies.kc_access_token in session,
            Cookies.kc_refresh_token in session
        )

        # initialize login, if not authenticated yet
        log.debug('Validating checklist')
        if all(check_list) is False:
            log.debug('Checklist failed, redirecting to login URL')
            return redirect(login_url)

        # validate identity token
        try:
            log.debug('Validating ID token')
            id_token = session[Cookies.kc_id_token]
            kc.decode_jwt(id_token)

        # handle invalid identity token
        except ExpiredSignatureError:
            log.debug('ID token expired')

            # validate refresh token
            try:
                log.debug('Validating refresh token')
                refresh_token = session[Cookies.kc_refresh_token]
                kc.decode_jwt(refresh_token)

                # fetch new tokens
                log.debug('Fetching new tokens using refresh token')
                response = kc.refresh_access_token(refresh_token)
                update_tokens(response)

            # handle invalid refresh token
            except ExpiredSignatureError:
                log.debug('Refresh token expired, initiating login')
                return redirect(login_url)

        # set user info in globals
        log.debug('Setting user information to globals g.user')
        id_token = session[Cookies.kc_id_token]
        g.user = kc.decode_jwt(id_token)

    return authenticator
