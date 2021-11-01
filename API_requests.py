import requests

import config, config_restricted


class APIRequests:
    _API_auth_token = config_restricted.API_TOKEN

    @classmethod
    def get(cls):
        pass

    @classmethod
    def post(cls, url: str, payload):
        headers = {'Authorization': f'Token {cls._API_auth_token}',
                   'Content-Type': 'application/json'}

        request = requests.post(url=url, json=payload, headers=headers)
        request_status = request.status_code
        request.close()
        print(f'Request status: {request_status}')
        return request_status
