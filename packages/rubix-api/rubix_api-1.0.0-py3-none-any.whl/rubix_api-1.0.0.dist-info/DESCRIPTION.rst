# Rubix API

A proprietary api for external python projects.

## Installation

You can install the Rubix API from [PyPI]():

    pip install rubix_api

The api is tested only on Python 3.6.

## How to use

Rubix API is a toolkit of python modules to help interacting with rubix .NET projects, [Rubix](https://github.com/rubix-labs/Rubix).

### RubixAuth

Introduces custom Oauth2 authentication mechanism, it can be integrated with [requests](https://github.com/kennethreitz/requests) as described
in [new forms of authentication](http://docs.python-requests.org/en/master/user/authentication/#new-forms-of-authentication).

    from rubix_api.auth import RubixAuth

    rubix_auth = RubixAuth(
        "https://hostname/connect/token",
        "client_id",
        "client-secret",
        "grant_type",
        "audience"
    )

    requests.get("https://api/endpoint", auth=rubix_auth)

