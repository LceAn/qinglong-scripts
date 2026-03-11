#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Voice Auto SMS - 自动保号短信发送脚本
优化版本：添加每日一言功能，替换随机中文乱码
作者：karllee830 (原始作者)
优化：LceAn
版本：v1.1
日期：2026-03-10

@cron 0 0 */15 * * *
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import requests
import json

# ==================== 配置区域 ====================
# 邮箱设置
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your_email@gmail.com"  # 替换为你的 Gmail 邮箱
sender_password = "your_app_password"  # 替换为你的应用专用密码
receiver_email = "xxxxxxxx@txt.voice.google.com"  # 替换为接收者的邮箱地址

# 每日一言 API 设置
# 可选 API:
# 1. https://v1.hitokoto.cn/ - 一言 API
# 2. https://api.uomg.com/api/rand.qinghua - 情话 API
# 3. https://api.uomg.com/api/rand.shici - 诗词 API
YAN_YAN_API = "https://v1.hitokoto.cn/"
USE_YAN_YAN = True  # True: 使用每日一言，False: 使用随机中文

# ==================== 功能函数 ====================

def get_daily_quote():
    """
    获取每日一言
    返回：句子 + 出处
    """
    try:
        response = requests.get(YAN_YAN_API, timeout=5)
        data = json.loads(response.text)
        
        hitokoto = data.get('hitokoto', '')
        from_who = data.get('from_who', '')
        from_where = data.get('from', '')
        
        if from_who and from_where:
            return f"「{hitokoto}」—— {from_who}《{from_where}》"
        elif from_who:
            return f"「{hitokoto}」—— {from_who}"
        else:
            return f"「{hitokoto}」"
    except Exception as e:
        print(f"获取每日一言失败：{e}")
        return generate_random_chinese(32)

def generate_random_chinese(length):
    """
    生成随机中文字符（备用方案）
    """
    return ''.join(chr(random.randint(0x4e00, 0x9fff)) for _ in range(length))

def send_email(subject, body):
    """
    发送邮件
    """
    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = sender_email
    message['To'] = receiver_email
    
    server = None
    try:
        print("正在连接到 SMTP 服务器...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("正在登录...")
        server.login(sender_email, sender_password)
        print("正在发送邮件...")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ 邮件发送成功！")
        return True
    except smtplib.SMTPConnectError as e:
        print(f"❌ 连接 SMTP 服务器失败：{e}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP 认证失败：{e}")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP 错误：{e}")
    except Exception as e:
        print(f"❌ 发生未知错误：{e}")
    finally:
        if server:
            print("正在关闭连接...")
            server.quit()
        else:
            print("未能建立 SMTP 连接")
    return False

# ==================== 主程序 ====================

def main():
    """
    主函数
    """
    print("=" * 50)
    print("🎯 Google Voice 自动保号短信发送")
    print("=" * 50)
    
    # 设置邮件主题
    subject = "Google Voice 保号短信"
    
    # 生成邮件正文
    if USE_YAN_YAN:
        print("📖 正在获取每日一言...")
        daily_quote = get_daily_quote()
        body = f"【Google Voice 自动保号】\n\n此短信为自动保号 Google Voice 所用的自动发送短信。\n\n📝 每日一言：\n{daily_quote}\n\n感谢使用！"
        print(f"✅ 已获取每日一言：{daily_quote[:30]}...")
    else:
        random_chinese = generate_random_chinese(32)
        body = f"【Google Voice 自动保号】\n\n此短信为自动保号 Google Voice 所用的自动发送短信，后方中文为规避风控所用，请勿理会。\n\n{random_chinese}"
        print("✅ 已生成随机中文字符")
    
    print("-" * 50)
    
    # 发送邮件
    success = send_email(subject, body)
    
    print("=" * 50)
    if success:
        print("🎉 任务完成！")
    else:
        print("⚠️  任务失败，请检查配置和网络连接")
    print("=" * 50)

if __name__ == "__main__":
    main()
