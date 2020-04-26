# coding=utf-8
import ssl

from flask import logging

ssl._create_default_https_context = ssl._create_unverified_context  # 全局取消证书验证

from CCPRestSDK import REST


# 主帐号
accountSid = '8a216da8719c20ad0171b15047c20aec'

# 主帐号Token
accountToken = '3f40566481b745b8855364f4825d8b86'

# 应用Id
appId = '8a216da8719c20ad0171b150482b0af3'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

class CCP(object):

    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
        except Exception as e:
            logging.error(e)
            raise e
        # print result
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        success = "<statusCode>000000</statusCode>"
        if success in result:
            return True
        else:
            return False
ccp = CCP.instance()
if __name__ == "__main__":
    ccp = CCP.instance()
    res = ccp.sendTemplateSMS("185xxxxxxxx", ["1234", 5], 1)
    print(res)