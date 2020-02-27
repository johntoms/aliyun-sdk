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
修改于 2019-09-16（by ruijie.qiao） 添加API STS请求验证功能
请求参数案例1（默认AK传空值为STS Token验证方式，RoleName为空的默认值为ZhuyunFullReadOnlyAccess）:
        'AccessKeyId': None,
        'AccessKeySecret': None,
        'RoleName': None,
请求参数案例2（AK值不为空的时候，为普通的AK验证方式，这时候如果RoleName为非空，STS Token验证方式也不生效）:
        'AccessKeyId': XXXXXXXXXXXXXX,
        'AccessKeySecret': XXXXXXXXXXXXXX,
        'RoleName': None,
请求参数案例3（默认AK传空值为STS Token验证方式，RoleName不为空，RoleName为设置的值）:
        'AccessKeyId': None,
        'AccessKeySecret': None,
        'RoleName': XXXXXXXXXXXXXX,
==========================================================================================
"""

ROLE_URL = "http://100.100.100.200/latest/meta-data/ram/security-credentials/"
PRODUCT_API_CONFIG_MAP = {
    'ecs': {
        'domain': 'ecs.aliyuncs.com',
        'version': '2014-05-26',
        'port': 443,
        'protocol': 'https'
    },
    'rds': {
        'domain': 'rds.aliyuncs.com',
        'version': '2014-08-15',
        'port': 443,
        'protocol': 'https'
    },
    'drds': {
        'domain': 'drds.aliyuncs.com',
        'version': '2015-04-13',
        'port': 443,
        'protocol': 'https'
    },
    'slb': {
        'domain': 'slb.aliyuncs.com',
        'version': '2014-05-15',
        'port': 443,
        'protocol': 'https'
    },
    'ess': {
        'domain': 'ess.aliyuncs.com',
        'version': '2014-08-28',
        'port': 443,
        'protocol': 'https'
    },
    'mts': {
        'domain': 'mts.aliyuncs.com',
        'version': '2014-06-18',
        'port': 443,
        'protocol': 'https'
    },
    'yundun': {
        'domain': 'yundun.aliyuncs.com',
        'version': '2014-09-24',
        'port': 443,
        'protocol': 'https'
    },
    'cdn': {
        'domain': 'cdn.aliyuncs.com',
        'version': '2018-05-10',
        'port': 443,
        'protocol': 'https'
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
        'port': 443,
        'protocol': 'https'
    },
    'dysms': {
        'domain': 'dysmsapi.aliyuncs.com',
        'version': '2017-05-25',
        'port': 443,
        'protocol': 'https'
    },
    'dyvms': {
        'domain': 'dyvmsapi.aliyuncs.com',
        'version': '2017-05-25',
        'port': 443,
        'protocol': 'https'
    },
    'dybase': {
        'domain': 'dybaseapi.aliyuncs.com',
        'version': '2017-05-25',
        'port': 443,
        'protocol': 'https'
    },
    'redis': {
        'domain': 'r-kvstore.aliyuncs.com',
        'version': '2015-01-01',
        'port': 443,
        'protocol': 'https'
    },
    'mongodb': {
        'domain': 'mongodb.aliyuncs.com',
        'version': '2015-12-01',
        'port': 443,
        'protocol': 'https'
    },
    'dts': {
        'domain': 'dts.aliyuncs.com',
        'version': '2016-08-01',
        'port': 443,
        'protocol': 'https'
    },
    'vpc': {
        'domain': 'vpc.aliyuncs.com',
        'version': '2016-04-28',
        'port': 443,
        'protocol': 'https'
    },
    'cms': {
        'domain': 'metrics.aliyuncs.com',
        'version': '2019-01-01',
        'port': 443,
        'protocol': 'https',
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
    'avds':{
        'domain': 'avds.aliyuncs.com',
        'version': '2017-11-29',
        'port': 443,
        'protocol': 'https',
    },
    'cbn':{
        'domain': 'cbn.aliyuncs.com',
        'version': '2017-09-12',
        'port': 443,
        'protocol': 'https',
    },
    'smartag':{
        'domain': 'smartag.cn-shanghai.aliyuncs.com',
        'version': '2018-03-13',
        'port': 443,
        'protocol': 'https',
    },
}


def percent_encode(string):
    if string is None:
        raise Exception('params is None')
    if not isinstance(string, (str, bytes, int)):
        raise TypeError(str(string) + 'params TypeError')
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

    def __init__(self, access_key_id=None, access_key_secret=None, role_name=None, *args, **kwargs):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        if role_name is None or role_name == "":
            self.role_name = "ZhuyunFullReadOnlyAccess"
        else:
            self.role_name = role_name
        self.security_token = None

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

        if self.access_key_id is None or self.access_key_secret is None or self.access_key_secret == "" or self.access_key_id == "":
            resp_role = requests.get(ROLE_URL + self.role_name)
            if resp_role.status_code == 200:
                parsed_resp = parse_response(resp_role)
                self.access_key_id = parsed_resp.get('AccessKeyId')
                self.access_key_secret = parsed_resp.get('AccessKeySecret')
                self.security_token = parsed_resp.get('SecurityToken')
                api_params['AccessKeyId'] = self.access_key_id

        if self.security_token:
            api_params['SecurityToken'] = self.security_token

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
