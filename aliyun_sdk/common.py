# BuiltIn Packages
import base64
import hashlib
import hmac
import time
from urllib.request import quote
import uuid

# Part3   Packages
import requests

# Project Packages
from . import parse_response


"""
==========================================================================================
整理于 2019-04-16
==========================================================================================
"""

PRODUCT_API_CONFIG_MAP = {
    'ecs': {
        'domain': 'ecs.aliyuncs.com',
        'version': '2014-05-26',
        'port': 80,
        'protocol': 'http'
    },
    'rds': {
        'domain': 'rds.aliyuncs.com',
        'version': '2014-08-15',
        'port': 80,
        'protocol': 'http'
    },
    'drds': {
        'domain': 'drds.aliyuncs.com',
        'version': '2015-04-13',
        'port': 80,
        'protocol': 'http'
    },
    'slb': {
        'domain': 'slb.aliyuncs.com',
        'version': '2014-05-15',
        'port': 80,
        'protocol': 'http'
    },
    'ess': {
        'domain': 'ess.aliyuncs.com',
        'version': '2014-08-28',
        'port': 80,
        'protocol': 'http'
    },
    'mts': {
        'domain': 'mts.aliyuncs.com',
        'version': '2014-06-18',
        'port': 80,
        'protocol': 'http'
    },
    'yundun': {
        'domain': 'yundun.aliyuncs.com',
        'version': '2014-09-24',
        'port': 80,
        'protocol': 'http'
    },
    'cdn': {
        'domain': 'cdn.aliyuncs.com',
        'version': '2018-05-10',
        'port': 80,
        'protocol': 'http'
    },
    'ram': {
        'domain': 'ram.aliyuncs.com',
        'version': '2015-05-01',
        'port': 443,
        'protocol': 'https'
    },
    'sts': {
        'domain': 'sts.aliyuncs.com',
        'version': '2015-04-01',
        'port': 80,
        'protocol': 'http'
    },
    'dysms': {
        'domain': 'dysmsapi.aliyuncs.com',
        'version': '2017-05-25',
        'port': 80,
        'protocol': 'http'
    },
    'dyvms': {
        'domain': 'dyvmsapi.aliyuncs.com',
        'version': '2017-05-25',
        'port': 80,
        'protocol': 'http'
    },
    'dybase': {
        'domain': 'dybaseapi.aliyuncs.com',
        'version': '2017-05-25',
        'port': 80,
        'protocol': 'http'
    },
    'redis': {
        'domain': 'r-kvstore.aliyuncs.com',
        'version': '2015-01-01',
        'port': 80,
        'protocol': 'http'
    },
    'mongodb': {
        'domain': 'mongodb.aliyuncs.com',
        'version': '2015-12-01',
        'port': 80,
        'protocol': 'http'
    },
    'dts': {
        'domain': 'dts.aliyuncs.com',
        'version': '2016-08-01',
        'port': 80,
        'protocol': 'http'
    },
    'vpc': {
        'domain': 'vpc.aliyuncs.com',
        'version': '2016-04-28',
        'port': 80,
        'protocol': 'http'
    },
    'cms': {
        'domain': 'metrics.aliyuncs.com',
        'version': '2019-01-01',
        'port': 80,
        'protocol': 'http',
    },
    'waf': {
        'domain': 'wafopenapi.cn-hangzhou.aliyuncs.com',
        'version': '2018-01-17',
        'port': 443,
        'protocol': 'https',
    },
    'domain': {
        'domain': 'domain.aliyuncs.com',
        'version': '2018-01-29',
        'port': 443,
        'protocol': 'https',
    },
    'business': {
        'domain': 'business.aliyuncs.com',
        'version': '2017-12-14',
        'port': 443,
        'protocol': 'https',
    },
    'ddospro': {
        'domain': 'ddospro.cn-hangzhou.aliyuncs.com',
        'version': '2017-07-25',
        'port': 443,
        'protocol': 'https',
    },
    'ddoscoo':{
        'domain': 'ddoscoo.cn-hangzhou.aliyuncs.com',
        'version': '2017-12-28',
        'port': 443,
        'protocol': 'https',
    },
}


def percent_encode(string):
    if string is None:
        raise Exception('AccessKeyId or AccessKeySecret is None')
    if not isinstance(string, (str, bytes, int)):
        raise TypeError('AccessKeyId or AccessKeySecret should be String')
    if isinstance(string, bytes):
        string.decode('utf-8')
    elif isinstance(string, int):
        string = str(string)
    else:
        string.encode('utf-8').decode('utf-8')

    string = quote(string, '')
    string = string.replace('+', '%20')
    string = string.replace('*', '%2A')
    string = string.replace('%7E', '~')

    return string


class AliyunCommon(object):
    '''
    Aliyun common HTTP API
    '''

    def __init__(self, access_key_id=None, access_key_secret=None, *args, **kwargs):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

    def sign(self, params_to_sign):
        canonicalized_query_string = ''

        sorted_params = sorted(params_to_sign.items(), key=lambda kv_pair: kv_pair[0])
        for k, v in sorted_params:
            canonicalized_query_string += percent_encode(k) + '=' + percent_encode(v) + '&'

        canonicalized_query_string = canonicalized_query_string[:-1]

        string_to_sign = 'POST&%2F&' + percent_encode(canonicalized_query_string)

        h = hmac.new(bytes(self.access_key_secret + "&", 'utf-8'), bytes(string_to_sign, 'utf-8'), hashlib.sha1)
        signature = base64.encodebytes(h.digest()).strip()

        return signature

    def verify(self):
        status_code, _ = self.ecs(Action='DescribeRegions')
        return (status_code == 200)

    def call(self, domain, version, port=80, protocol='http', timeout=3, **biz_params):
        api_params = {
            'Format': 'json',
            'Version': version,
            'AccessKeyId': self.access_key_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid4()),
            'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            'partner_id': '1.0',
        }

        api_params.update(biz_params)
        api_params['Signature'] = self.sign(api_params)

        url = '{}://{}:{}/'.format(protocol, domain, port)

        resp = requests.post(url, data=api_params, timeout=timeout)
        parsed_resp = parse_response(resp)

        return resp.status_code, parsed_resp

    def __getattr__(self, product):
        api_config = PRODUCT_API_CONFIG_MAP.get(product)

        if not api_config:
            raise Exception('Unknow Aliyun product API config. Please use `call()` with full API configs.')

        domain = api_config.get('domain')
        version = api_config.get('version')
        port = api_config.get('port')
        protocol = api_config.get('protocol')

        def f(timeout=3, **biz_params):
            return self.call(domain=domain, version=version, port=port, protocol=protocol, timeout=timeout,
                             **biz_params)

        return f