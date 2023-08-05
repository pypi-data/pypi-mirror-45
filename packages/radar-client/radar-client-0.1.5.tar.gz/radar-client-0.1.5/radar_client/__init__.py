import requests
from .utils import sign, verify_sig, authorize, InvalidRadarSignature


__all__ = (
    'sign',
    'verify_sig',
    'authorize',
    'InvalidRadarSignature',
    'NetworkError',
    'create_query',
    'radar'
)


class NetworkError(Exception):
    def __init__(self, reason, code, response):
        super().__init__(reason)
        self.message = reason
        self.code = code
        self.response = response


def create_query(name, requires=None, props=None):
    default_requires = requires
    default_props = props

    def init(requires=None, **props):
        return {
            'name': name,
            'requires': requires or default_requires,
            'props': props or default_props
        }

    return init


def radar(url, public_key=None, secret_key=None, header_name='x-radar-signature'):
    signature = None

    if public_key and secret_key:
        signature = sign(public_key, secret_key)

    def request(*queries, headers=None):
        headers = headers or {}

        if signature:
            headers = {**headers, header_name: signature}

        r = requests.post(url, json=queries, headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            raise NetworkError(r.reason, r.status_code, r)

    return request
