from requests import request as http_request

class EpcRequests:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def request(method: str, url: str, json=None):
        return http_request(method, url, json=json)