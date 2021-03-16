The oclcwskeyhmacsig.hmacsig and oclcwskeyhmacsig.util python libraries provided here are useful for OCLC apis which require HMAC signatures. An example is obtaining an access token with an authorization code as per the OAuth apis.

The example script test_scim_me.py tests out the OCLC SCIM /Me API in this manner. Before calling it you'll need an SCIM API key from OCLC and to visit an OAuth login URL and get redirected to a URL that will have an authorization code. You can then run the example script, get an access token and call the /Me API. Read the header of test_scim_me.py for more info.

Code here was developed by staff of the systems team at the University of Winnipeg Library. Free software licensing is pending.
