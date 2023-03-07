import re

headerStr = '''
Host: prod.jx9n.com
appType: 0
User-Agent: yun zhi chong/4.4.8 (iPhone; iOS 16.1; Scale/2.00)
userId: c81c38ccdbc24979836652f7dd6dd294
deviceToken: 0
channel: yzc-baidu
osInformation: iPhone12,1
uuid: c81c38ccdbc24979836652f7dd6dd294
latitude: 28.756174
appVersion: 4.4.8
version: 1.0.0
plat: iOS
Connection: keep-alive
longitude: 115.850906
timestamp: 1667103343000
Accept-Language: zh-Hans-US;q=1, en-US;q=0.9
isTest: 1
certType: 1
Accept: */*
cityCode: 360112
Accept-Encoding: gzip, deflate, br
certification: URLEVEW4ylpRptoN28q9feTMsCttZPYvZcQeXg9wtK7w0Hck4UNFBpLy23mKzqiy8Recxta38dNm3Y1YWNJBUoOHKd96sBhyLoco/ap6uYbOTsE+LeSgXFvoyBE+znaK3QgyO6COgD8/LVPCrHByElnT8VdEW05ajDML10Kx2uo=
'''

ret = ""
for i in headerStr:
    if i == '\n':
        i = "',\n'"
    ret += i

ret = re.sub(": ", "': '", ret)
print(ret[3:-3])
