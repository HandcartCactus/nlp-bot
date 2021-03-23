def api_cert_validate(api):
    return not api.VerifyCredentials() is None

def whole_number(i):
    assert i==int(i) and i>0
