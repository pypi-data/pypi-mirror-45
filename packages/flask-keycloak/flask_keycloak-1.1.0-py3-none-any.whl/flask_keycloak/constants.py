# -*- coding: utf-8 -*-

class Sessions:
    state = 'state'
    referrer = 'referrer'


class Cookies:
    kc_id_token = 'KC_ID_TOKEN'
    kc_access_token = 'KC_ACCESS_TOKEN'
    kc_refresh_token = 'KC_REFRESH_TOKEN'


class Tokens:
    id_token = 'id_token'
    access_token = 'access_token'
    refresh_token = 'refresh_token'


class URLs:
    root_url = '/'
    login_url = '/kc-login'
    callback_url = '/kc-callback'


class QueryParams:
    code = 'code'
    state = 'state'


class Defaults:
    unknown = 'unknown'
