# Project Packages
from aliyun_sdk.common import AliyunCommon
from aliyun_sdk.oss import AliyunOSS
from . import retry_for_requests


def get_config(c):
    return {
        'access_key_id': c.get('AccessKeyId'),
        'access_key_secret': c.get('AccessKeySecret'),
        'role_name': c.get('RoleName'),
    }


class AliyunClient(object):
    def __init__(self, config=None):
        self.config = config
        self.common_client = AliyunCommon(**get_config(config))
        self.oss_client = AliyunOSS(**get_config(config))

    def verify(self):
        return self.common_client.verify()

    @retry_for_requests
    def common(self, product, timeout=10, **biz_params):
        return self.common_client.__getattr__(product)(timeout=timeout, **biz_params)

    @retry_for_requests
    def oss(self, method, timeout=10, **biz_params):
        return self.oss_client.__getattr__(method)(timeout=timeout, **biz_params)

