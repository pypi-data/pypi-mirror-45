from ._compat import urljoin

import requests

from .exception import (
    InvalidAPIKeyException,
    trueverifiAPIError
)

class API:
    URL_BASE = "https://app.truverifi.com"
    URL_API  = urljoin(URL_BASE, "api")

    def __init__(self, api_key):
        self.api_key = api_key

    def _api_request(self, method, base_url, **kwargs):
        headers = kwargs.get("header", { })
        headers.update({
            "Accept": "application/json",
            "X-API-Key": self.api_key,
        })

        kwargs["headers"] = headers
        abs_url           = "%s/%s" % (API.URL_API, base_url)

        response  = requests.request(method, abs_url, **kwargs)
        json_data = response.json()
        if response.ok:
            return json_data
        else:
            if response.status_code == 401:
                raise InvalidAPIKeyException("The provided API Key is invalid.")
            else:
                raise trueverifiAPIError("Error Recieved: %s" % json_data)

    def account(self):
        response = self._api_request("GET", "account")
        return response

    def line(self):
        response = self._api_request("GET", "line")
        return response

    def checkService(self, services, zip = None):
        params   = dict(zip = zip, services = services)
        response = self._api_request("POST", "checkService", data = params)
        return response

    def lineChangeService(self, services, zip = None):
        params   = dict(zip = zip, services = services)
        response = self._api_request("POST", "line/changeService", data = params)
        return response

    def lineExtend(self):
        response = self._api_request("POST", "line/extend")
        return response