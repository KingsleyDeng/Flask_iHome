# coding=utf-8
import ssl

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
    """自己封装的用于发送短信的辅助类"""
    # 用来保存对象的类属性
    instance = None

    def __new__(cls):
        # 判断ccp类有没有已经创建好的对象，如果没有创建一个对象并保存
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls.instance = obj
        return cls.instance
        # 如果有 则 将保存的对象直接返回

    def send_template_sms(self, to, datas, temp_id):
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        for k, v in result.items():
            if k == 'templateSMS':
                for k, s in v.items():
                    print('%s:%s' % (k, s))
            else:
                print('%s:%s' % (k, v))


if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms("13037136525", ["1234", "5"], 1)
