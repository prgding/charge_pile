import requests
import os
import yaml


def full_available_list():

    if res.json().get('msg') == 'SUCCESS':
        for i in range(12):
            status = res.json().get('data')[i].get('status')
            # 空闲
            if status == 1:
                number = res.json().get('data')[i].get('code')
                available_pile.append(number)
    else:
        print('请求失败')
        send_email('接口请求失败', '接口请求失败')


def file_save():
    with open("new.txt", "w") as f:
        f.write(f'{available_pile}')


def compare():
    with open("new.txt", "r") as f, open("old.txt", "r") as f2:
        new = f.read()
        old = f2.read()
        quantity = len(available_pile)
        if new != old:
            print(f'可用充电桩变化, {old} 到 {new}')
            with open("durationText.txt", "r") as f:
                detail = f.read()
            with open("FinishRecord.txt", "r") as f:
                detail += f.read()
            #send_email(f'可用充电桩数量:{quantity}', f'空闲口:{new}\n\n{detail}')
            with open("old.txt", "w") as f3:
                f3.write(new)


def duration_init():
    duration_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    with open('duration.txt', 'w') as f:
        f.write(str(duration_list)[1:-1])


def duration_plus():
    for i in range(12):
        duration_list[i] = int(duration_list[i]) + 1


def duration_reset():
    from datetime import datetime
    current_time = datetime.strftime(datetime.now(), "%m-%d %H:%M")
    for i in range(12):
        status = res.json().get('data')[i].get('status')
        # 空闲
        if status == 1:
            number = int(res.json().get('data')[i].get('code'))
            if duration_list[number - 1] > 5:
                with open('FinishRecord.txt', 'a') as f:
                    f.write(f'{number} 充电时间:{duration_list[number - 1] // 60}小时{duration_list[number - 1] % 60}分钟 {current_time}\n')
            duration_list[number - 1] = 0


def duration_filesave():
    with open("duration.txt", "w") as f:
        f.write(str(duration_list)[1:-1])


def convert_to_dict():
    duration_dict = {}

    for i in range(12):
        duration = duration_list[i]
        duration_dict[i + 1] = duration

    # 排序
    duration_dict = sorted(duration_dict.items(), key=lambda x: x[1], reverse=True)
    os.system('rm durationText.txt')
    for i in range(12):
        if duration_dict[i][0] < 10:
            # 换成小时
            if duration_dict[i][1] > 60:
                info = f'0{duration_dict[i][0]} 已充：{duration_dict[i][1] // 60}小时{duration_dict[i][1] % 60}分钟'
            else:
                info = f'0{duration_dict[i][0]} 已充：{duration_dict[i][1]}分钟'
        else:
            if duration_dict[i][1] > 60:
                info = f'{duration_dict[i][0]} 已充：{duration_dict[i][1] // 60}小时{duration_dict[i][1] % 60}分钟'
            else:
                info = f'{duration_dict[i][0]} 已充：{duration_dict[i][1]}分钟'
        with open("durationText.txt", "a") as f:
            f.write(info + '\n')


def send_email(mailcontent, detail):
    from smtplib import SMTP_SSL
    from email.mime.text import MIMEText
    from datetime import datetime

    current_time = datetime.strftime(datetime.now(), "%m-%d %H:%M")

    # 邮件内容编写
    sender_show = f'{mailcontent}'  # 一级：大标题
    Subject = f'{current_time} 充电桩监控'  # 二级：时间+主题
    message = f'{detail}'  # 三级：邮件正文
    to_addrs = '1203823603@qq.com, 17538056834@163.com'

    # 赋值
    msg = MIMEText(message, 'plain', _charset="utf-8")
    msg["from"] = sender_show
    msg["Subject"] = Subject

    # 发件人账号
    with open("/etc/pwd.yaml", 'r') as f:
        Password = yaml.load(f, Loader=yaml.FullLoader)
    mail_server = '网易'
    user = Password[f'{mail_server}']['Account']
    password = Password[f'{mail_server}']['Password']

    # 发送
    with SMTP_SSL(host=Password[f'{mail_server}']['Host'], port=465) as smtp:
        smtp.login(user=user, password=password)
        smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())


if __name__ == "__main__":
    url = 'https://prod.jx9n.com/yzc-app-charge/yzc-app/v1/chargingSocket/get/by/charging/id?chargingId=45109&gateWayId=&letter=W'
    headers = {
        'Host': 'prod.jx9n.com',
        'appType': '0',
        'User-Agent': 'yun zhi chong/4.4.8 (iPhone; iOS 16.1; Scale/2.00)',
        'userId': 'c81c38ccdbc24979836652f7dd6dd294',
        'deviceToken': '0',
        'channel': 'yzc-baidu',
        'osInformation': 'iPhone12,1',
        'uuid': 'c81c38ccdbc24979836652f7dd6dd294',
        'latitude': '28.756174',
        'appVersion': '4.4.8',
        'version': '1.0.0',
        'plat': 'iOS',
        'Connection': 'keep-alive',
        'longitude': '115.850906',
        'timestamp': '1667103343000',
        'Accept-Language': 'zh-Hans-US;q=1, en-US;q=0.9',
        'isTest': '1',
        'certType': '1',
        'Accept': '*/*',
        'cityCode': '360112',
        'Accept-Encoding': 'gzip, deflate, br',
        'certification': 'URLEVEW4ylpRptoN28q9feTMsCttZPYvZcQeXg9wtK7w0Hck4UNFBpLy23mKzqiy8Recxta38dNm3Y1YWNJBUoOHKd96sBhyLoco/ap6uYbOTsE+LeSgXFvoyBE+znaK3QgyO6COgD8/LVPCrHByElnT8VdEW05ajDML10Kx2uo='
    }
    res = requests.get(url, headers=headers)

    available_pile = []

    with open("duration.txt", "r") as f:
        duration_list = list(f.read().split(','))

    full_available_list()
    duration_plus()
    duration_reset()
    if duration_list[10] == 0:
        send_email('充电桩监控', '已充满，或被拔掉')
    duration_filesave()
    file_save()
    convert_to_dict()
    compare()
