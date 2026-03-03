"""
百度网盘自动任务脚本

功能：
- 自动签到获取积分
- 完成成长值任务
- 支持多账号
- 青龙面板通知

环境变量：
- BAIDU_COOKIE: 百度网盘 Cookie（必填）
  格式：BDUSS=xxx; BAIDUID=xxx; ...

作者：用户自定义
版本：1.0
日期：2026-03-03
"""

import requests
import time
import re
import os
import json

# 脚本标题（用于通知）
SCRIPT_TITLE = "百度网盘任务"

# 尝试导入青龙面板的通知函数
try:
    from notify import send
except ImportError:
    print("未找到 notify.py 模块，无法发送通知。请确保脚本在青龙环境下运行。")
    def send(title, content):
        print(f"\n--- 未发送的通知 ---\n标题：{title}\n内容：{content}\n--------------------")

# 从环境变量中获取 Cookie
COOKIES = os.environ.get('BAIDU_COOKIE', '')
if not COOKIES:
    msg = f"❌ 配置错误：未找到环境变量 BAIDU_COOKIE，请检查！"
    print(msg)
    send(SCRIPT_TITLE, msg)
    exit()

HEADERS = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://pan.baidu.com/wap/svip/growth/task',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': COOKIES
}


# --- 函数定义区 ---

def signin():
    """
    签到函数
    应用了与用户信息函数相同的"JSON 优先，Regex 备用"的兼容逻辑
    """
    url = 'https://pan.baidu.com/rest/2.0/membership/level?app_id=250528&web=5&method=signin'
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # 1. 优先尝试 JSON 解析
        try:
            data = response.json()
            if data.get("errno") == 0:
                return f"✅ 签到成功：获得积分 +{data.get('points', '未知')}"
            
            if "repeat signin" in data.get("error_msg", "") or data.get("errno") == -6:
                return f"🤔 签到提醒：今日已签到"
            
            # 捕获其他有具体信息的 API 错误
            if data.get("error_msg"):
                return f"❌ 签到失败：{data['error_msg']}"
        
        except json.JSONDecodeError:
            # JSON 解析失败，忽略，让后续的 Regex 处理
            pass
        
        # 2. 如果 JSON 解析不成功，回退到 Regex 尝试
        if response.status_code == 200:
            points_match = re.search(r'points":(\d+)', response.text)
            if points_match:
                return f"✅ 签到成功 (兼容模式): 获得积分 +{points_match.group(1)}"
            
            error_match = re.search(r'"error_msg":"(.*?)"', response.text)
            if error_match:
                if "repeat signin" in error_match.group(1):
                    return f"🤔 签到提醒 (兼容模式): 今日已签到"
                else:
                    # 返回正则表达式捕获到的具体错误信息
                    return f"❌ 签到失败 (兼容模式): {error_match.group(1)}"
        
        return f"❌ 签到失败：未知错误，无法从 API 响应中获取有效信息。"
    
    except Exception as e:
        return f"❌ 签到异常：{e}"


def delay(seconds):
    """延时函数"""
    time.sleep(seconds)


def get_user_info():
    """
    获取用户信息
    采用"JSON 优先，Regex 备用"的双重解析策略，确保在各种网络环境下都能获取信息
    """
    url = 'https://pan.baidu.com/rest/2.0/membership/user?app_id=250528&web=5&method=query'
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # 1. 优先尝试 JSON 解析
        try:
            data = response.json()
            if data.get("errno") == 0:
                user_data = data.get('user_info', {})
                return {
                    'level': user_data.get('level', '未知'),
                    'name': user_data.get('name', '未知'),
                    'points': user_data.get('points', '未知')
                }
        except json.JSONDecodeError:
            # JSON 解析失败，忽略，让后续的 Regex 处理
            pass
        
        # 2. 如果 JSON 解析不成功，回退到 Regex 尝试
        if response.status_code == 200:
            level_match = re.search(r'"level":(\d+)', response.text)
            name_match = re.search(r'"name":"(.*?)"', response.text)
            points_match = re.search(r'"points":(\d+)', response.text)
            
            if level_match or name_match or points_match:
                return {
                    'level': level_match.group(1) if level_match else '未知',
                    'name': name_match.group(1) if name_match else '未知',
                    'points': points_match.group(1) if points_match else '未知'
                }
        
        return None
    
    except Exception as e:
        print(f"获取用户信息异常：{e}")
        return None


def main():
    """主函数"""
    print("=" * 50)
    print(SCRIPT_TITLE)
    print("=" * 50)
    
    results = []
    
    # 获取用户信息
    print("\n📱 获取用户信息...")
    user_info = get_user_info()
    if user_info:
        info_text = f"👤 用户：{user_info['name']} | Lv.{user_info['level']} | 积分：{user_info['points']}"
        print(info_text)
        results.append(info_text)
    else:
        print("❌ 获取用户信息失败")
        results.append("❌ 获取用户信息失败")
    
    # 执行签到
    print("\n📅 执行签到...")
    signin_result = signin()
    print(signin_result)
    results.append(f"\n{signin_result}")
    
    # 生成报告
    report = "\n".join([
        "=" * 30,
        " 百度网盘任务报告",
        "=" * 30,
    ] + results + [
        "=" * 30
    ])
    
    print("\n" + report)
    
    # 发送通知
    try:
        send(SCRIPT_TITLE, report)
        print("\n✅ 通知已发送")
    except Exception as e:
        print(f"\n❌ 通知推送异常：{e}")


if __name__ == "__main__":
    main()
