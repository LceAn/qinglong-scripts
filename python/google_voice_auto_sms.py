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
import os
from email.mime.text import MIMEText
from email.header import Header
import random
import requests
import json

# ==================== 配置区域 ====================
# 从环境变量读取配置
sender_email = os.environ.get('GV_SENDER_EMAIL', '')
sender_password = os.environ.get('GV_SENDER_PASSWORD', '')
receiver_email = os.environ.get('GV_RECEIVER_EMAIL', '')

# SMTP 设置
smtp_server = "smtp.gmail.com"
smtp_port = int(os.environ.get('GV_SMTP_PORT', '587'))  # 587=TLS, 465=SSL

# 每日一言 API 设置
YAN_YAN_API = "https://v1.hitokoto.cn/"
USE_YAN_YAN = os.environ.get('GV_USE_YAN_YAN', 'true').lower() == 'true'
if os.environ.get('GV_YAN_YAN_API'):
    YAN_YAN_API = os.environ.get('GV_YAN_YAN_API')

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
        print(f"📡 SMTP 服务器：{smtp_server}:{smtp_port}")
        print("正在连接到 SMTP 服务器...")
        
        # 根据端口选择连接方式
        if smtp_port == 465:
            # SSL 直连
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            print("✅ 使用 SSL 连接")
        else:
            # TLS 连接
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            print("✅ 使用 TLS 连接")
        
        print(f"正在登录：{sender_email}...")
        print(f"密码长度：{len(sender_password)}位")
        server.login(sender_email, sender_password)
        print("正在发送邮件...")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ 邮件发送成功！")
        return True
    except smtplib.SMTPConnectError as e:
        print(f"❌ 连接 SMTP 服务器失败：{e}")
        print("\n💡 尝试修改端口：")
        print("   - 如使用 587 失败，试试 465（添加环境变量 GV_SMTP_PORT=465）")
        print("   - 如使用 465 失败，试试 587")
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP 认证失败：{e}")
        print("\n💡 可能原因：")
        print("   1. 密码包含空格（应用专用密码格式：xxxx xxxx xxxx xxxx）")
        print("   2. 应用专用密码已失效，需要重新生成")
        print("   3. Google 账户安全设置阻止了登录")
        print("\n✅ 解决方法：")
        print("   1. 检查密码是否去掉了所有空格")
        print("   2. 重新生成应用专用密码：https://myaccount.google.com/apppasswords")
        print("   3. 尝试切换端口（587 ↔ 465）")
        print("   4. 检查 Google 账户安全设置")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP 错误：{e}")
    except Exception as e:
        print(f"❌ 发生未知错误：{e}")
        print(f"   错误类型：{type(e).__name__}")
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
    
    # 检查环境变量配置
    print("\n📋 检查配置...")
    if not sender_email:
        print("❌ 错误：GV_SENDER_EMAIL 未配置！")
        print("   请在青龙面板添加环境变量 GV_SENDER_EMAIL=your_email@gmail.com")
        return False
    if not sender_password:
        print("❌ 错误：GV_SENDER_PASSWORD 未配置！")
        print("   注意：需要使用 Gmail 应用专用密码，不是登录密码！")
        print("   获取方法：https://myaccount.google.com/apppasswords")
        return False
    if not receiver_email:
        print("❌ 错误：GV_RECEIVER_EMAIL 未配置！")
        print("   请在青龙面板添加环境变量 GV_RECEIVER_EMAIL=xxx@txt.voice.google.com")
        return False
    
    print(f"✅ 发件邮箱：{sender_email}")
    print(f"✅ 收件邮箱：{receiver_email}")
    print(f"✅ 应用密码：{'*' * len(sender_password)} ({len(sender_password)}位)")
    print(f"✅ SMTP 端口：{smtp_port}")
    
    # 检查密码格式
    if ' ' in sender_password:
        print(f"\n⚠️  警告：密码中包含空格！应用专用密码应该去掉所有空格")
        print(f"   当前密码：'{sender_password}'")
        print(f"   正确格式：'{''.join(sender_password.split())}'")
    elif len(sender_password) != 16:
        print(f"\n⚠️  警告：应用专用密码应该是 16 位，当前为{len(sender_password)}位")
        print("   如果不是 16 位，可能配置的是登录密码而非应用专用密码！")
        print("   获取应用专用密码：https://myaccount.google.com/apppasswords")
    else:
        print(f"\n✅ 密码格式正确（16 位，无空格）")
    
    print("\n" + "-" * 50)
    
    # 设置邮件主题
    subject = "Google Voice 保号短信"
    
    # 生成邮件正文（短信内容，需要简洁）
    if USE_YAN_YAN:
        print("📖 正在获取每日一言...")
        daily_quote = get_daily_quote()
        # 精简版：只保留核心内容，避免被截断
        body = f"GV 保号\n{daily_quote}"
        print(f"✅ 已获取每日一言：{daily_quote[:30]}...")
        print(f"📱 短信内容：{body}")
    else:
        random_chinese = generate_random_chinese(16)
        body = f"GV 保号 {random_chinese}"
        print("✅ 已生成随机中文字符")
        print(f"📱 短信内容：{body}")
    
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
