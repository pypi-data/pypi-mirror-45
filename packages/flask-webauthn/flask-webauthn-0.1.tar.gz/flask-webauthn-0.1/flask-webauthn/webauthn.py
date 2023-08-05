# -*- coding: utf-8 -*-

from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from flask import session

import webauthn

from .config import (
    WEBAUTHN_REGISTER_DISPLAY_NAME_FIELD,
    WEBAUTHN_REGISTER_UKEY_FIELD,
    WEBAUTHN_REGISTER_USERNAME_FIELD,
    WEBAUTHN_CHALLENGE_FIELD,
    WEBAUTHN_RELYING_PARTY_NAME,
    WEBAUTHN_RELYING_PARTY_ID)
from .util import generate_challenge


class WebAuthnManager(object):
    pass
