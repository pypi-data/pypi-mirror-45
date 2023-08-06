# -*- coding: utf-8 -*-
import sys
import logging


# define formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# define handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)


# define logger
logger = logging.getLogger('flask-keycloak')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
