import requests

from st2common.runners.base_action import Action


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self._email = self.config.get('email')
        self._token = self.config.get('api_token')
        self._brand = self.config.get('brand')
        self._api_root = 'https://{}.reamaze.com/api/v1'.format(self._brand)
        self._headers = {'Accept': 'application/json'}

        if not self._email:
            raise ValueError('Missing "email" config option')
        if not self._brand:
            raise ValueError('Missing "brand" config option')
        if not self._token:
            raise ValueError('Missing "api_token" config option')

    def _api_get(self, endpoint, headers={}, params=None):
        _url = self._api_root + endpoint
        _headers = {**self._headers, **headers}

        r = requests.get(url=_url, auth=(self._email, self._token),
                         params=params, headers=_headers)

        if r.status_code not in [requests.codes.ok]:  # pylint: disable=no-member
            self.logger.error('GET failed. HTTP status: %s, Body: %s.',
                              r.status_code, r.text)

        r.raise_for_status()
        return r.json()

    def _api_post(self, endpoint, headers={}, data=None, json=None):
        _url = self._api_root + endpoint
        _headers = {**self._headers, **headers}

        r = requests.post(url=_url, auth=(self._email, self._token),
                          data=data, headers=_headers, json=json)

        # pylint: disable=no-member
        if r.status_code not in [requests.codes.ok, requests.codes.created]:
            self.logger.error('POST failed. HTTP status: %s, Body: %s.',
                              r.status_code, r.text)

        return r.json()

    def _api_put(self, endpoint, headers={}, data=None, json=None):
        _url = self._api_root + endpoint
        _headers = {**self._headers, **headers}

        r = requests.put(url=_url, auth=(self._email, self._token),
                         data=data, headers=_headers, json=json)

        # pylint: disable=no-member
        if r.status_code not in [requests.codes.ok, requests.codes.accepted]:
            self.logger.error('PUT failed. HTTP status: %s, Body: %s.',
                              r.status_code, r.text)

        r.raise_for_status()
        return r.json()

    def _convert_slug(self, slug_name):
        if not slug_name:
            return None

        return slug_name.lower().replace(' ', '-')

    # Not used in actions but needed for testing
    def run(self, **kwargs):
        raise RuntimeError("run() not implemented")
