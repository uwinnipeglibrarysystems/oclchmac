#!/usr/bin/env python3

import hmac
from hashlib import sha256
from base64 import b64encode
from time import time
from random import SystemRandom # cryptographically strong
from string import hexdigits

sysrandom = SystemRandom()

def oclc_sha256_hmac_sig(
        apikey, secret,
        ordered_query_params,
        timestamp=None, nonce=None,
):
    if timestamp==None:
        timestamp = '%d' % time() # %d string format will do float to int
    if nonce==None:
        nonce = ''.join(sysrandom.choice(hexdigits) for i in range(30))

    prehashedstring = """%s
%s
%s

GET
www.oclc.org
443
/wskey
""" % (apikey, timestamp, nonce)

    query_param_string= '\n'.join( ("%s=%s" % (key, value)
                                    for key, value in ordered_query_params)
    ) # join
    if query_param_string!='':
        query_param_string+="\n"
    prehashedstring+=query_param_string
        
    digest = hmac.new(secret.encode('utf-8'),
                      msg=prehashedstring.encode('utf-8'),
                      digestmod=sha256).digest()
    signature = b64encode(digest).decode()
    return timestamp, nonce, signature

def oclc_authorization_header_value(
                apikey, secret,
        ordered_query_params,
        principalID=None,
        principalIDNS=None,
        timestamp=None, nonce=None,
):
    timestamp, nonce, signature = oclc_sha256_hmac_sig(
        apikey, secret,
        ordered_query_params,
        timestamp=timestamp, nonce=nonce
    )

    principalID_str = (None if principalID==None
                       else 'principalID="%s"' % principalID )
    prinipalIDNS_str = (None if principalIDNS==None
                        else 'principalIDNS="%s"' % principalIDNS )
    
    
    authorization_header = (
        'http://www.worldcat.org/wskey/v2/hmac/v1 '
        'clientId="%s", timestamp="%s", nonce="%s", '
        'signature="%s"'
        ) % (apikey, timestamp, nonce, signature)
    return ', '.join(
        x for x in (authorization_header, principalID_str, prinipalIDNS_str)
        if x != None
    )

if __name__ == "__main__":
    # example from
    # https://www.oclc.org/developer/develop/authentication/hmac-signature.en.html
    apikey = ('jdfRzYZbLc8HZXFByyyLGrUqTOOmkJOAPi4tAN0E'
              '7xI3hgE2xDgwJ7YPtkwM6W3ol5yz0d0JHgE1G2Wa')
    secret = 'UYnwZbmvf3fAXCEa0JryLQ=='

    ordered_query_param = ( ('inst', '128807'), )

    timestamp = '1361408273'
    nonce = '981333313127278655903652665637'
    
    timestamp, nonce, signature = oclc_sha256_hmac_sig(
        apikey,
        secret,
        ordered_query_param,
        timestamp=timestamp, nonce=nonce,
        )

    assert signature=='5O6SRig58wqm6gqEu3oSODVte6Albon9CCvNrZHCoys='

    expected_auth_header = (
        'http://www.worldcat.org/wskey/v2/hmac/v1 '
        'clientId="'
        'jdfRzYZbLc8HZXFByyyLGrUqTOOmkJOAPi4tAN0E'
        '7xI3hgE2xDgwJ7YPtkwM6W3ol5yz0d0JHgE1G2Wa", '
        'timestamp="1361408273", nonce="981333313127278655903652665637", '
        'signature="5O6SRig58wqm6gqEu3oSODVte6Albon9CCvNrZHCoys="'
    )
    assert(
        expected_auth_header
            ==
        oclc_authorization_header_value(
            apikey, secret, ordered_query_param,
            timestamp=timestamp,
            nonce=nonce,
        )
    ) # assert expression
