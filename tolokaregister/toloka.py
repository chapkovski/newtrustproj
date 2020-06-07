# some consntants (like host urls) go here.
REAL_HOST = 'https://toloka.yandex.ru'
SANDBOX_HOST = 'https://sandbox.toloka.yandex.ru'
DEFAULT_ACCEPT_MSG = 'Thank you!'
# naive but let's do it:

# we obtain api from settings, there they are obtained from env
from django.conf import settings
from django.template.loader import render_to_string
import json
import requests
from enum import Enum


class CodeStatus(Enum):
    ACCESS_DENIED = 'ACCESS_DENIED'


class objdict(dict):
    """updated dict object to access and set dict properties as obj propperties. Taken from
    here: https://goodcode.io/articles/python-dict-object/"""

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class TolokaClient:
    def __init__(self, sandbox):
        self.sandbox = sandbox
        if sandbox:
            self.host = SANDBOX_HOST
            self.api_key = settings.SANDBOX_TOLOKA_API
        else:
            self.host = REAL_HOST
            self.api_key = settings.TOLOKA_API
        print('APIKEY', self.api_key)

    def get_authorization_header(self):
        """Yes, that's the weird way toloka sets authorization header."""
        return dict(Authorization=f'OAuth {self.api_key}')

    def get_headers(self):
        """getting authorization header, and open the possibility to inject other headers later."""
        headers = {
            'Content-Type': 'application/json'
        }
        headers.update(self.get_authorization_header())
        return headers

    def get_assignment_url(self, assignment_id):
        """Im not sure we need separate url methods, but if later on toloka changes the urls, it will be easier to
        replace just these methods.
        """
        return f"{self.host}/api/v1/assignments/{assignment_id}"

    def get_bonus_url(self):
        """Im not sure we need separate url methods, but if later on toloka changes the urls, it will be easier to
        replace just these methods.
        """
        return f"{self.host}/api/v1/user-bonuses"

    def get_error_msg(self, resp):
        return dict(error=True,
                    error_status=resp.status_code,
                    error_raw=resp.json())

    def request_to_toloka(self, url, method, payload, ):
        headers = self.get_headers()
        if isinstance(payload, dict):
            payload = json.dumps(payload)

        response = requests.request(method, url, headers=headers, data=payload)
        print('HEADERs', headers)
        print('URL', url)
        print("STATUS CODE", response.status_code)
        print("RAW RESP", response.json())
        if 200 <= response.status_code <= 300:
            return response.json()
        else:
            return self.get_error_msg(response)

    def get_assignment_info(self, assignment_id):
        """Using assginment id returns a toloka response object"""
        url = self.get_assignment_url(assignment_id)
        method = 'GET'
        payload = None
        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)

    def accept_assignment(self, assignment_id):
        """given assignment id, accept assignment. The method DOES NOT CHECK whether the assignment is in acceptable status.
        for instance it is not in ACTIVE mode. It just stupidly sends accept post. All checking should be done by
        a calling function/instance. Returns toloka response object"""
        url = self.get_assignment_url(assignment_id)
        method = 'PATCH'
        # we can think about customizing acceptance message later, it's not important
        payload = dict(status='ACCEPTED',
                       public_comment=DEFAULT_ACCEPT_MSG)
        # todo: error handnling
        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)

    def pay_bonus(self, user_id, bonus, title, message):
        """pay bonus in usd. Does not check for anything (nor for existance of user, nor size of bonus, nor amount of
        money available on balance, -just existence of the three params, Returns toloka response object"""
        bonus_params = dict(user_id=user_id, amount=str(bonus), title=title, message=message)
        payload = render_to_string('tolokaregister/bonus.json', bonus_params)
        url = self.get_bonus_url()
        method = 'POST'
        # todo: error handnling
        r = self.request_to_toloka(url, method, payload)
        return TolokaResponse(**r)


class TolokaResponse(objdict):
    """just an objdict. open for some customization"""
    pass
