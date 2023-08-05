from typing import Dict

import requests


class JSONResponse:
    def __init__(self, url: str) -> None:
        self.url = url
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        url = f'{self.url.rstrip("/")}{endpoint}'
        response = self.session.request(method, url, json=data)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str = '') -> Dict:
        return self._request('GET', endpoint)

    def post(self, endpoint: str = '', data: Dict = None) -> Dict:
        return self._request('POST', endpoint, data)

    def delete(self, endpoint: str = '') -> Dict:
        return self._request('DELETE', endpoint)
