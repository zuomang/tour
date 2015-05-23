#!/usr/bin/env python
# encoding: utf-8

import parameter
import random
import hashlib
import xml.etree.ElementTree as ET
import urllib2
import threading
import uuid
import json

from urllib import quote
from jsapi_ticket import get_jsapi_ticket
from util import get_timestamp

class PaymentBaseConf(object):
    APPID = parameter.appid
    APPSECRET = parameter.appsecret
    MCHID = parameter.mchid
    KEY = parameter.key

    NOTIFY_URL = "http://www.quxhuan.com/payback"
    CURL_TIMEOUT = 30


class Singleton(object):
    """单例模式"""

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    impl = cls.configure() if hasattr(cls, "configure") else cls
                    instance = super(Singleton, cls).__new__(impl, *args, **kwargs)
                    instance.__init__(*args, **kwargs)
                    cls._instance = instance
        return cls._instance


class UrllibClient(object):
    """使用urlib2发送请求"""

    def get(self, url, second=30):
        return self.postXml(None, url, second)

    def postXml(self, xml, url, second=30):
        """不使用证书"""
        data = urllib2.urlopen(url, xml, timeout=second).read()
        return data


class HttpClient(Singleton):
    @classmethod
    def configure(cls):
        return UrllibClient


class CommonUtilPub(object):
    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def createNoncestr(self, length = 32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            if k != "sign":
                v = quote(paraMap[k]) if urlencode else paraMap[k]
                buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def getSign(self, obj):
        """生成签名"""
        #签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        #签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String, PaymentBaseConf.KEY)
        #签名步骤三：MD5加密
        String = hashlib.md5(String).hexdigest()
        #签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_

    def arrayToXml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.iteritems():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def postXmlCurl(self, xml, url, second = 30):
        return HttpClient().postXml(xml, url, second = second)


class WechatConfigJsAPI(CommonUtilPub):
    respone = None
    url = None
    curl_timeout = None

    def __init__(self):
        self.parameters = {}
        self.result = {}

    def setParameter(self, parameter, parameterValue):
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def getSign(self, obj):
        """生成签名"""
        #签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        print String
        #签名步骤二：在string后加入KEY
        String = hashlib.sha1(String).hexdigest()
        return String

    def createDate(self):
        self.parameters["noncestr"] = self.createNoncestr()
        self.parameters["jsapi_ticket"] = get_jsapi_ticket()
        self.parameters["timestamp"] = get_timestamp()
        self.parameters["url"] = "http://www.quxhuan.com/payment/recharge?showwxpaytitle=1"
        self.parameters["sign"] = self.getSign(self.parameters)

    def getResult(self):
        self.result = {
            'appId': parameter.appid,
            'timestamp': self.parameters['timestamp'],
            'nonceStr': self.parameters['noncestr'],
            'signature': self.parameters['sign'],
            'jsApiList': ['chooseWXPay']
            }
        return self.result


class WechatJsPayment(CommonUtilPub):
    code = None
    openid = None
    parameters = None
    prepay_id = None
    curl_timeout = None

    def __init__(self, timeout = PaymentBaseConf.CURL_TIMEOUT):
        self.curl_timeout = timeout

    def getParameters(self, prepayid):
        jsApiObj = {}
        jsApiObj["appId"] = PaymentBaseConf.APPID
        jsApiObj["timeStamp"] = str(get_timestamp())
        jsApiObj["nonceStr"] = self.createNoncestr()
        jsApiObj["package"] = "prepay_id=" + prepayid
        jsApiObj["signType"] = "MD5"
        jsApiObj["sign"] = self.getSign(jsApiObj)
        self.parameters = jsApiObj

        return self.parameters

class WechatPaymentBase(CommonUtilPub):
    respone = None
    url = None
    curl_timeout = None

    def __init__(self):
        self.parameters = {}
        self.result = {}

    def setParameter(self, parameter, parameterValue):
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        self.parameters["appid"] = PaymentBaseConf.APPID
        self.parameters["mch_id"] = PaymentBaseConf.MCHID
        self.parameters["nonce_str"] = self.createNoncestr
        self.parameters["sign"] = self.getSign(self.parameters)
        return self.arrayToXml(self.parameters)

    def createTradeNo(self):
        uuid_str = str(uuid.uuid1())
        return uuid_str[0:32]

    def postXml(self):
        xml = self.createXml()
        self.respone = self.postXmlCurl(xml, self.url, self.curl_timeout)
        return self.respone

    def getResult(self):
        self.postXml()
        self.result = self.xmlToArray(self.respone)
        return self.result


class UnfiedOrder(WechatPaymentBase):
    """统一支付接口"""

    def __init__(self, timeout = PaymentBaseConf.CURL_TIMEOUT):
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.curl_timeout = timeout
        super(UnfiedOrder, self).__init__()

    def createXml(self):
        self.parameters["appid"] = PaymentBaseConf.APPID
        self.parameters["mch_id"] = PaymentBaseConf.MCHID
        self.parameters["nonce_str"] = self.createNoncestr()
        self.parameters["out_trade_no"] = self.createTradeNo()
        self.parameters["spbill_create_ip"] = "127.0.0.1"
        self.parameters["notify_url"] = PaymentBaseConf.NOTIFY_URL
        self.parameters["trade_type"] = "JSAPI"
        self.parameters["sign"] = self.getSign(self.parameters)
        return self.arrayToXml(self.parameters)

    def getPrepayId(self):
        self.postXml()
        self.result = self.xmlToArray(self.respone)
        prepay_id = self.result["prepay_id"]
        return prepay_id
