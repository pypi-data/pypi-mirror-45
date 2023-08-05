import requests


class AuthFailedException(Exception):
    pass


class UnknownResponseException(Exception):
    def __init__(self, msg: str, response: requests.Response):
        super().__init__(msg)
        self.response = response
