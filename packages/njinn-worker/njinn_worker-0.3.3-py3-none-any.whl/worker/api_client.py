import requests
from requests_jwt import JWTAuth


class NjinnAPI():
    """
    Class provides access to the Njinn API by adding the
    base URL and authentication (JWT) to each request.
    """

    def __init__(self, api, token, worker_name):
        """
        Prepare Njinn base URL and token for authentication
        """

        self.auth = JWTAuth(token, header_format=u'JWT %s')
        self.auth.expire(30)
        self.auth.add_field('worker', worker_name)

        self.njinn_api = api

    def get_url(self, path):
        """
        Add the Njinn API base url in front of the path.
        """

        path = path[1:] if path.startswith('/') else path
        url = f"{self.njinn_api}/{path}"
        return url

    def get(self, path, params=None, **kwargs):
        """
        Run GET request to the Njinn API.
        """

        url = self.get_url(path)
        return requests.get(url, params=params, auth=self.auth, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        """
        Run POST request to the Njinn API.
        """

        url = self.get_url(path)
        return requests.post(url, data=data, json=json, auth=self.auth, **kwargs)

    def put(self, path, data=None, **kwargs):
        """
        Run PUT request to the Njinn API.
        """

        url = self.get_url(path)
        return requests.put(url, data=data, auth=self.auth, **kwargs)

    def patch(self, path, data=None, **kwargs):
        """
        Run PATCH request to the Njinn API.
        """

        url = self.get_url(path)
        return requests.patch(url, data=data, auth=self.auth, **kwargs)

    def delete(self, path, **kwargs):
        """
        Run DELETE request to the Njinn API.
        """

        url = self.get_url(path)
        return requests.delete(url, auth=self.auth, **kwargs)
