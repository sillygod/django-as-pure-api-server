import hashlib
import hmac
import logging

from urllib.parse import (urljoin, urlencode, urlunparse, parse_qs)

import requests

from django.urls import reverse
from django.conf import settings

logger = logging.getLogger('member.oauth2_client')


def url(scheme='', host='', path='', params='', query='', fragment=''):
    return urlunparse((scheme, host, path, params, query, fragment))


def get_local_host(request):
    scheme = 'http' + ('s' if request.is_secure() else '')
    return url(scheme=scheme, host=request.get_host())


def parse_response(response):
    if 'application/json' in response.headers['Content-Type']:
        return response.json()
    else:
        content = parse_qs(response.text)
        content = dict(
            (x, y[0] if len(y) == 1 else y) for x, y in content.items())

        return content


class Oauth2RequestAuthorizer(requests.auth.AuthBase):
    """authorization header for requests
    """

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer {}'.format(
            self.access_token)
        return request


class OAuth2Client:

    service = None
    client_id = None
    client_secret = None

    auth_url = None
    token_url = None
    user_info_url = None

    scope = None

    def __init__(self,
                 local_host,
                 code=None,
                 client_id=None,
                 client_secret=None,
                 scope=None):
        self.local_host = local_host

        if client_id and client_secret:
            self.client_id = client_id
            self.client_secret = client_secret

        if code:
            access_token = self.get_access_token(code)
            self.authorizer = Oauth2RequestAuthorizer(
                access_token=access_token)
        else:
            self.authorizer = None

        if scope:
            self.scope = scope

    def set_access_token(self, token):
        """you can set access token by this method. Most use cases are
        access_token are by client side. For security, the remain process
        of OAuth should be done by server side.
        """
        self.authorizer = Oauth2RequestAuthorizer(access_token=token)

    def get_access_token(self, code):
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.get_redirect_url(),
            'scope': self.scope
        }

        response = self.post(self.token_url, data=data, authorize=False)
        return response['access_token']

    def get_redirect_url(self):
        kwargs = {'service': self.service}
        path = reverse('api:member:social_login', kwargs=kwargs)

        return urljoin(self.local_host, path)

    def get_login_url(self):
        data = {
            'response_type': 'code',
            'scope': self.scope,
            'redirect_url': self.get_redirect_url,
            'client_id': self.client_id
        }
        query = urlencode(data)
        return urljoin(self.auth_url, url(query=query))

    def get_user_info(self):
        return self.get(self.user_info_url)

    def get_request_params(self, data=None, authorize=True):
        """set custom authorize if authorize is True
        """
        auth = self.authorizer if authorize else None
        return data, auth

    def get(self, address, params=None, authorize=True):
        params, auth = self.get_request_params(params, authorize)
        response = request.get(address, params=params, auth=auth)
        return self.handle_response(response)

    def post(self, address, data=None, authorize=True):
        data, auth = self.get_request_params(data, authorize)
        response = request.post(address, data=data, auth=auth)
        return self.handle_response(response)

    def handle_response(self, response):
        response_content = parse_response(response)

        if response.status_code == requests.codes.ok:
            return response_content
        else:
            logger.error("{}: {}".format(response.status_code, response.text))
            error = self.extract_error_from_response(response_content)
            raise ValueError(error)

    def extract_error_from_response(self, response_content):
        """there is a specific format for every client so we should deal with it
        individually
        """
        raise NotImplementedError()


class FacebookClient(OAuth2Client):

    service = 'FACEBOOK'
    auth_url = 'https://www.facebook.com/dialog/oauth'
    token_url = 'https://graph.facebook.com/oauth/access_token'
    user_info_url = 'https://graph.facebook.com/me?fields=email,name,gender,birthday,locale,verified'

    scope = ','.join(['email', 'public_profile'])

    def __init__(self, *args, **kwargs):
        if not self.client_id and not self.client_secret:
            self.client_id = settings.SOCIAL_AUTH_FACEBOOK_ID
            self.client_secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
        super().__init__(*args, **kwargs)

    def get_request_params(self, data=None, authorize=True):
        data = data or {}
        if authorize:
            data.update({
                'appsecret_proof':
                hmac.new(settings.SOCIAL_AUTH_FACEBOOK_SECRET.encode('utf-8'),
                         msg=self.authorizer.access_token.encode('utf-8'),
                         digestmod=hashlib.sha256).hexdigests()
            })

        return super().get_request_params(data, authorize)

    def get_user_info(self):
        """#NOTE: want to do more process?
        """
        response = super().get_user_info()

        fields = ('email', 'name', 'gender', 'birthday')
        for key in fields:
            value = response.get(key, None)

        return response

    def extract_error_from_response(self, response_content):
        return response_content['error']['message']
