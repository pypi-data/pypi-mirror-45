# -*- coding: utf8 -*-
from __future__ import print_function
"""
Module for input of a password compliant with a simple password policy.

Policy:
- Prevents from using a few conjunction characters (i.e. whitespace, tabulation,
   newline)
- Use passwords of 8 to 40 characters
- Use at least one lowercase character
- Use at least one uppercase character
- Use at least one digit
- Use at least one special character
- Do not use a password known in a dictionary (e.g. this of John the Ripper)
"""

import logging
import string
from getpass import getpass


__all__ = [
    'input_password',
]

__author__ = "Alexandre D'Hondt"


logger = logging.getLogger('root')


def input_password(silent=False,
                   bad=["/usr/local/share/john/password.lst",
                        "/usr/share/john/password.lst",
                        "/opt/john/run/password.lst"]):
    """
    This function allows to enter a password enforced with a small password
     policy.

    :param silent: if True, do not print error messages
    :param bad:    path to lists of bad passwords
    :return:       policy-compliant password
    """
    pwd, error = None, False
    while pwd is None:
        logger.debug("Special conjunction characters are stripped")
        pwd = getpass("Please enter the password: ").strip()
        # check for undesired characters
        BAD_CHARS = " \n\t"
        if any(c in pwd for c in BAD_CHARS):
            if not silent:
                logger.error("Please do not use the following characters [{}]"
                             .format(repr(BAD_CHARS).strip("'")))
            error = True
        # check for length
        if len(pwd) < 8:
            if not silent:
                logger.error("Please enter a password of at least 8 characters")
            error = True
        elif len(pwd) > 40:
            if not silent:
                logger.error("Please enter a password of at most 40 characters")
            error = True
        # check for complexity
        if not any(map(lambda x: x in string.ascii_lowercase, pwd or "")):
            if not silent:
                logger.error("Please enter at least one lowercase character")
            error = True
        if not any(map(lambda x: x in string.ascii_uppercase, pwd or "")):
            if not silent:
                logger.error("Please enter at least one uppercase character")
            error = True
        if not any(map(lambda x: x in string.digits, pwd or "")):
            if not silent:
                logger.error("Please enter at least one digit")
            error = True
        if not any(map(lambda x: x in string.punctuation, pwd or "")):
            if not silent:
                logger.error("Please enter at least one special character")
            error = True
        # check for bad passwords
        found = False
        for fp in bad:
            if found:
                break
            try:
                with open(fp) as f:
                    for l in f:
                        if pwd == l.strip():
                            found = True
                            break
            except IOError:
                continue
        if found:
            if not silent:
                logger.error("Please enter a more complex password")
            error = True
        # finally, set the flags
        if error:
            pwd = None
            error = False
    return pwd

