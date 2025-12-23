#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email.utils import formataddr

import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime

# ================= 配置区域 =================

# 1. 邮件配置 (以QQ邮箱为例)
SMTP_SERVER = 'smtp.qq.com'  # SMTP服务器地址
SMTP_PORT = 465  # SSL端口
SENDER_EMAIL = 'xxx@qq.com'  # 发件人邮箱
PASSWORD = 'xxx'  # 邮箱授权码 (不是QQ密码)
RECEIVER_EMAILS = ['xxx@qq.com', 'xxx@whu.edu.cn']

# 2. 爬虫 API 配置
API_URL = "http://zwhqbsd.whu.edu.cn/ICBS_V2_Server/v3/XINTF/GetReserve"
PARAMS = {
    "MeterID": "xxx"  # 你的 MeterID
}
# 请填入最新的 Headers (尤其是 Cookie, User-Agent 和 Authorization)
HEADERS = {
    "Cookie": "xxx",
    "authorization": "xxx",
    "Host": "zwhqbsd.whu.edu.cn",
    "Referer": "http://zwhqbsd.whu.edu.cn/MobilePayWeb/",
    "User-Agent": "xxx",
    "Accept": "application/json, text/plain, */*",
    "Connection": "keep-alive"
}

# 3. 阈值设置
MIN_BALANCE = 10.0  # 低于多少元发送提醒


# ================= 功能函数 =================

def send_email(current_balance, room_name, update_time):
    """发送邮件函数 (修正版)"""
    subject = f'【警报】宿舍电费余额不足提醒 - {current_balance}元'
    content = f"""
    您好！

    检测到宿舍电费余额已低于预警值。

    ------------------------
    房间名称：{room_name}
    当前余额：{current_balance} 元
    数据时间：{update_time}
    ------------------------

    请尽快充值，以免断电影响生活！

    (本邮件由服务器自动发送)
    """

    message = MIMEText(content, 'plain', 'utf-8')

    # 【修正点1】From 必须包含邮箱地址，formataddr 会自动处理中文编码
    # 生成结果类似：From: =?utf-8?b?...?= <1873404737@qq.com>
    message['From'] = formataddr(["电费管家", SENDER_EMAIL])

    # 【修正点2】To 字段不需要用 Header 编码，直接用字符串拼接即可
    # 否则邮箱地址本身可能会被错误编码，导致发送失败
    message['To'] = ",".join(RECEIVER_EMAILS)

    # Subject 保持原样，中文主题需要 Header 编码
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp_obj = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp_obj.login(SENDER_EMAIL, PASSWORD)
        smtp_obj.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, message.as_string())
        print(f"[{datetime.datetime.now()}] 邮件已发送给 {len(RECEIVER_EMAILS)} 位收件人！")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 邮件发送失败: {e}")


def check_power():
    print(f"[{datetime.datetime.now()}] 开始检查电费...")
    try:
        response = requests.get(API_URL, params=PARAMS, headers=HEADERS, timeout=10)
        response.raise_for_status()
        result = response.json()

        if str(result.get("Code")) in ["0", "200"]:
            data = result.get("Data", {})
            remain_power = float(data.get("remainPower", 0))
            room_name = data.get("U_name", "未知房间")
            read_time = data.get("readTime", "")

            print(f"当前余额: {remain_power} 元")

            if remain_power < MIN_BALANCE:
                print("余额不足，触发邮件发送...")
                send_email(remain_power, room_name, read_time)
            else:
                print("余额充足，无需发送通知。")
        else:
            print(f"API请求成功但返回错误: {result.get('Mess')}")
            # 如果是因为 Token 过期导致的错误，你也可以在这里加个邮件提醒自己去更新 Token

    except Exception as e:
        print(f"[{datetime.datetime.now()}] 脚本运行出错: {e}")


if __name__ == "__main__":
    check_power()
