# tested requests library with
# apt install python3-requests on Ubuntu 16.04
import requests

from .hmacsig import oclc_authorization_header_value

def make_query_string(query_ordered):
    return '&'.join( '%s=%s' % (key, value)
                     for key, value in query_ordered )

def get_json_from_oclc_url(url, authorization_header, json_accept=True):
    headers = {'Authorization': authorization_header}
    if json_accept:
        headers['Accept'] = 'application/json'

    r = requests.get(
        url,
        headers=headers,
    ) # requests.get
    r.raise_for_status()

    return r.json()

def post_empty_body_and_recieve_json_from_oclc_url(
        url, authorization_header,
        user_agent=None):

    headers = {'Authorization': authorization_header,
               'Accept': 'application/json',
    }
    if user_agent != None:
        headers['User-Agent'] = user_agent

    r = requests.post(
        url,
        headers=headers,
        data=b'',
    ) # requests.post
    r.raise_for_status()
    return r.json()

def make_url_and_auth_header(
        apikey, secret,
        urlbase,
        query_ordered,
        method='GET',
        nonce=None,
        timestamp=None,
):
    query_string = make_query_string(sorted(query_ordered))
    oclc_url = "%s?%s" % (urlbase, query_string )
    authorization_header = oclc_authorization_header_value(
        apikey, secret,
        query_ordered,
        method=method,
        timestamp=timestamp,
        nonce=nonce,
    )
    return oclc_url, authorization_header
