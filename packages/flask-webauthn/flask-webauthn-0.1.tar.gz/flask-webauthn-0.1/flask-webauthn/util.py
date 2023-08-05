# -*- coding: utf-8 -*-

import random
import string


def generate_challenge(challenge_len):
    '''Generates a random challenge for use in WebAuthn operations.

    Arguments:
        challenge_len {int} -- The length of the generated challenge.

    Returns:
        str -- The generated challenge.
    '''

    return ''.join([
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for i in range(challenge_len)
    ])
