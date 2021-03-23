def api_cert_validate(api):
    return not api.VerifyCredentials() is None