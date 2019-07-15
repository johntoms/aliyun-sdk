#!/usr/bin/env python
# coding=utf-8
"""
__Author__ = 'JohnToms'
__CreateTime__ = '2019/7/15'
"""
# BuiltIn Packages
# Part3   Packages
# Project Packages

from aliyun_sdk import client
ak = {
    "AccessKeyId":"example",
    "AccessKeySecret": "example"
}
aliyun_client = client.AliyunClient(ak)
response = aliyun_client.common('ecs', Action='DescribeRegions')
print(response)
