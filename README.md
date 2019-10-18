# aliyun_sdk
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
> 因为使用阿里云官方的 sdk 需要调用太多的包，而且写法上比较繁琐，故自己开发了一个比较简单的 sdk。
## 安装方式
```bash
pip install zy-aliyun-python-sdk
```
## 目前支持的产品
> 已适配的阿里云产品及 API 接口详情

## 功能介绍
1. 支持主流的阿里云产品。
2.  加入 `请求超时` 自动重新请求，上限 3 次。

**产品限制：**
- 该接口仅适用于`少次`、`不频繁`、`低速`,其他限制及详细说明，请参考[阿里云官方文档](https://aliyun.com)
- 具体传参请参考官方文档。
- 若需要添加或更新调用的 API 接口信息，请查看`aliyun_sdk/common.py` 文件,修改或添加`PRODUCT_API_CONFIG_MAP`中的字段。

API 接口详情如下：

|产品名称|简称|API 版本|请求地址|端口|协议|添加日期|
|---|---|---|---|---|---|---|
|云服务器|ecs|2014-05-26|ecs.aliyuncs.com|443|https|2019-04-17|
|阿里云关系型数据库|rds|2014-08-15|rds.aliyuncs.com|443|https|2019-04-17|
|分布式关系型数据库|drds|2015-04-13|drds.aliyuncs.com|443|https|2019-04-17|
|负载均衡|slb|2014-05-15|slb.aliyuncs.com|443|https|2019-04-17|
|弹性伸缩|ess|2014-08-28|ess.aliyuncs.com|443|https|2019-04-17|
|媒体处理|mts|2014-06-18|mts.aliyuncs.com|443|https|2019-04-17|
|阿里云云盾|yundun|2014-09-24|yundun.aliyuncs.com|443|https|2019-04-17|
|CDN|cdn|2018-05-10|cdn.aliyuncs.com|443|https|2019-04-17|
|访问控制 RAM|ram|2015-05-01|ram.aliyuncs.com|443|https|2019-04-17|
|安全令牌 STS|sts|2015-04-01|sts.aliyuncs.com|443|https|2019-04-17|
|短信服务|dysms|2017-05-25|dysmsapi.aliyuncs.com|443|https|2019-04-17|
|语音服务|dyvms|2017-05-25|dyvmsapi.aliyuncs.com|443|https|2019-04-17|
|消息接收1|dybase|2017-05-25|dybaseapi.aliyuncs.com|443|https|2019-04-17|
|云数据库Redis版|redis|2015-01-01|r-kvstore.aliyuncs.com|443|https|2019-04-17|
|云数据库 MongoDB 版|mongodb|2015-12-01|mongodb.aliyuncs.com|443|https|2019-04-17|
|数据传输服务DTS|dts|2016-08-01|dts.aliyuncs.com|443|https|2019-04-17|
|VPC|vpc|2016-04-28|vpc.aliyuncs.com|443|https|2019-04-17|
|云监控|cms|2019-01-01|metrics.aliyuncs.com|443|https|2019-07-12|
|Web 应用防火墙|waf|2018-01-17|wafopenapi.cn-hangzhou.aliyuncs.com|443|https|2019-04-17|
|域名|domain|2018-01-29|domain.aliyuncs.com|443|https|2019-04-17|
|交易与账单管理|business|2017-12-14|business.aliyuncs.com|443|https|2019-04-17|
|ddos 防护|ddospro|2017-07-25|ddospro.cn-hangzhou.aliyuncs.com|443|https|2019-04-17|

## example
```python
# 非 oss 产品
from aliyun_sdk import client
ak = {
    "AccessKeyId":"example",
    "AccessKeySecret": "example"
}
aliyun_client = client.AliyunClient(ak)
status_code, response = aliyun_client.common('ecs', Action='DescribeRegions')

# response ==> (status_code, result)
print(status_code, response)

# example result
# (404, {'Recommend': 'https://error-center.aliyun.com/status/search?Keyword=InvalidAccessKeyId.NotFound&source=PopGw', 'Message': 'Specified access key is not found.', 'RequestId': 'AEA6AEB8-6F44-445B-Bd0E-9E5F706B5665', 'HostId': 'ecs.aliyuncs.com', 'Code': 'InvalidAccessKeyId.NotFound'})

# oss 产品
status_code, oss_response = aliyun_client.oss('GET', **{"max-keys": 1000})
print(status_code, oss_response)
status_code, oss_response = aliyun_client.oss('GET', BucketName='cxp-test', Query={'acl': None})
print(status_code, oss_response)
```
