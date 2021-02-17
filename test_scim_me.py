#!/usr/bin/env python3

# A proof of concept test script for the OCLC IDM api for the OAuth
# explicit authorization code flow.
#
# OCLC OAuth
# https://www.oclc.org/developer/develop/authentication.en.html
# https://www.oclc.org/developer/develop/authentication/oauth.en.html
# https://www.oclc.org/developer/develop/authentication/oauth/explicit-authorization-code.en.html
#
# OCLC WMS IDM
# https://www.oclc.org/developer/develop/web-services/worldshare-identity-management-api.en.html
# https://developer.api.oclc.org/idm
# https://platform.worldcat.org/api-explorer/apis/SCIM/Me/Read
#
# before calling this script direct yourself to
# https://oauth.oclc.org/auth/{registryID}?client_id={}&response_type=code&scope=SCIM:read_self
# in a web browser with
# with institution_id set to the integer institution id and
# client_id being the public part of the IDM API key identifier (not the secret)
# (you'll need an IDM key supporting SCIM:read_self scope and the explicit
# grant workflow for tokens first)
#
# login to your institutions WMS installation as yourself
#
# After login, you'll be redirected to the redirect URI associated with the
# key and there will be an auth_code as a paramater in the URL redirected to.
# collect that auth_code as input when prompted after running this script
#
# If you don't have a redirect URL set up, add one or use redirect_uri paramater
# in # your visit to https://oauth.oclc.org/auth/{registryID}
#
# this script will prompt for the client_id, secret and numeric institution
# registration id
#
# invoke with --token followed by a valid, unexpired access token and
# you'll be just asked for the institution id, demonstrating the tokens
# are reusable during their lifetime

from collections import OrderedDict
from sys import argv

from requests import HTTPError

from oclcwskeyhmacsig.util import (
    post_empty_body_and_recieve_json_from_oclc_url, make_url_and_auth_header,
    get_json_from_oclc_url)

# this URL found in some of the docs doesn't work
#TOKEN_REQUEST_URL = 'https://oauth.oclc.org/token'

TOKEN_REQUEST_URL = 'https://authn.sd00.worldcat.org/oauth2/accessToken'

def request_access_token_with_auth_code(
        authorization_code,
        institution,
        client_key,
        secret):

    url, auth_header = make_url_and_auth_header(
        client_key, secret,
        TOKEN_REQUEST_URL,
        list(sorted(OrderedDict(
            authenticatingInstitutionId=institution,
            code=authorization_code,
            contextInstitutionId=institution,
            grant_type='authorization_code',
            ).items())),
        method='POST',
    )

    try :
        return post_empty_body_and_recieve_json_from_oclc_url(
                url, auth_header
            )
    except HTTPError as e:
        print( repr(e) )
        print( e.args )
        raise e

def get_slash_Me_with_access_token(access_token, institution):
    try:
        me_response = get_json_from_oclc_url(
            'https://%s.share.worldcat.org/idaas/scim/v2/Me' % institution,
            'Bearer ' + access_token,
            json_accept=False,
        )
    except HTTPError as e:
        print( repr(e) )
        print( e.args )
        raise e
    else:
        return me_response

def main():
    institution = str(int(input("institution id> ").strip()))

    # too lazy to use an argparse library when this simple
    if len(argv) == 3 and argv[1] == "--token":
        access_token = argv[2]
    else:
        authorization_code = input("auth code> ").strip()
        client_key = input("client_id> ").strip()
        secret = input("secret> ").strip()
        json_response = request_access_token_with_auth_code(
            authorization_code,
            institution,
            client_key,
            secret)

        if 'access_token' in json_response:
            access_token = json_response['access_token']
            print("access token " + access_token)
        else:
            print('no access token in response to request for token')
            exit(1)

    print( get_slash_Me_with_access_token(access_token, institution) )

if __name__ == "__main__":
    main()
