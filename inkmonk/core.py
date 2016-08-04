from base64 import b64encode
from hashlib import sha512
import requests
import config
from flask.json import _json as json
import hmac


JSON_MIME_TYPE = 'application/json'


def get_basic_authorization_header(key):
    return "Basic %s" % b64encode(key + ":")


def get_signed_authorization_header(key, secret, message):
    return b64encode("%s:%s" % (
        key, hmac.new(secret, message, sha512).hexdigest()))


def result(response):
    if response.status_code == 200:
        rjson = response.json()
        if rjson['status'] == 'success':
            return rjson['result']
    return None


def getter_request(url, method='GET', params={}, key=config.API_KEY, secret=config.API_SECRET, raw=False):

    sess = requests.Session()
    req = requests.Request(
        'GET', url, params=params, headers={})
    prepped_req = req.prepare()
    prepped_req.headers['Authorization'] = get_signed_authorization_header(
        key, secret, '{0}:{1}'.format('GET', prepped_req.url))
    response = sess.send(prepped_req)
    if raw:
        return response
    else:
        return result(response)


def get(resource, identifier, params={}, version=config.API_VERSION,
        url=config.API_URL, key=config.API_KEY,
        secret=config.API_SECRET, raw=False):
    if key is None:
        key = config.API_KEY
    if secret is None:
        secret = config.API_SECRET
    resource_url = '%s/%s/%s/%s' % (url, version, resource, identifier)
    response = requests.get(
        resource_url,
        headers={
                 'Authorization': get_signed_authorization_header(
                     key, secret,
                     "GET:/{0}/{1}/{2}:{3}".format(
                         version, resource, identifier, JSON_MIME_TYPE))},
        params=params)
    if raw:
        return response
    else:
        return result(response)


def all(resource, params={}, version=config.API_VERSION,
        url=config.API_URL, key=config.API_KEY,
        secret=config.API_SECRET, raw=False):
    if key is None:
        key = config.API_KEY
    if secret is None:
        secret = config.API_SECRET
    resource_url = '{0}/{1}/{2}'.format(url, version, resource)
    sess = requests.Session()
    req = requests.Request(
        'GET', resource_url, params=params, headers={})
    prepped_req = req.prepare()
    prepped_req.headers['Authorization'] = get_signed_authorization_header(
        key, secret, '{0}:{1}'.format('GET', prepped_req.url))
    response = sess.send(prepped_req)
    if raw:
        return response
    else:
        return result(response)

def setter_request(url, method, data, key=config.API_KEY, secret=config.API_SECRET, raw=False):
    requester = getattr(requests, method.lower())
    json_data = json.dumps(data)
    response = requester(
        url, data=json_data,
        headers={
            'Content-Type': JSON_MIME_TYPE,
            'Authorization': get_signed_authorization_header(
                key or config.API_KEY, secret or config.API_SECRET,
                "{0}:{1}:{2}:{3}".format(
                    method, url, JSON_MIME_TYPE, json_data))})
    if raw:
        return response
    else:
        return result(response)




def post(resource, data=None, version=config.API_VERSION,
         url=config.API_URL, key=config.API_KEY,
         secret=config.API_SECRET, raw=False):
    return setter_request(
        url='{0}/{1}/{2}'.format(url, version, resource),
        method='POST', data=data, key=key, secret=secret, raw=raw)


def put(resource, identifier, data=None,
        version=config.API_VERSION,
        url=config.API_URL, key=config.API_KEY,
        secret=config.API_SECRET, raw=False):
    return setter_request(
        url='{0}/{1}/{2}/{3}'.format(url, version, resource, identifier),
        method='PUT', data=data, key=key, secret=secret, raw=raw)


def patch(resource, identifier, data=None,
          version=config.API_VERSION,
          url=config.API_URL, key=config.API_KEY,
          secret=config.API_SECRET, raw=False):
    return setter_request(
        url='{0}/{1}/{2}/{3}'.format(url, version, resource, identifier),
        method='PATCH', data=data, key=key, secret=secret, raw=raw)
