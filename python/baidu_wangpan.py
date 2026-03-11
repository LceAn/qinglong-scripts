"""
百度网盘自动任务脚本

功能：
- 自动签到获取积分
- 每日一题自动答题
- 获取用户信息（等级、成长值）
- 支持多账号
- 青龙面板通知

环境变量：
- BAIDU_COOKIE: 百度网盘 Cookie（必填）
  格式：BDUSS=xxx; BAIDUID=xxx; ...

@cron 0 8 * * *

作者：用户自定义
版本：2.0
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


def get_daily_question():
    """获取每日一题，返回答案、ID、是否已回答"""
    url = 'https://pan.baidu.com/act/v2/membergrowv2/getdailyquestion?app_id=250528&web=5'
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
        if data.get("errno") == 0 and data.get("data"):
            if data["data"].get("user_info", {}).get("is_answer") == 1:
                return None, None, True
            return str(data["data"].get("answer")), str(data["data"].get("ask_id")), False
    except Exception as e:
        print(f"获取每日一题异常：{e}")
    return None, None, False


def answer_question(answer, ask_id):
    """提交答案并返回结果字符串"""
    url = f'https://pan.baidu.com/act/v2/membergrowv2/answerquestion?app_id=250528&web=5&ask_id={ask_id}&answer={answer}'
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
        if data.get("errno") == 0:
            return f"✅ 答题成功：获得积分 +{data.get('data', {}).get('score', '未知')}"
        elif "exceeded limit" in data.get("show_msg", ""):
            return f"🤔 答题提醒：今日已答题"
        else:
            return f"❌ 答题失败：{data.get('show_msg', '未知错误')}"
    except Exception as e:
        return f"❌ 答题异常：{e}"


def get_user_info():
    """获取用户信息，优先使用 JSON 解析，失败则回退到 Regex"""
    url = 'https://pan.baidu.com/rest/2.0/membership/user?app_id=250528&web=5&method=query'
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        try:
            data = response.json()
            if data.get("errno") == 0 and data.get("user_info"):
                user_info = data["user_info"]
                current_value = user_info.get("current_value", '未知')
                current_level = user_info.get("current_level", '未知')
                return f"👤 用户信息：V{current_level}会员，成长值 {current_value}"
        except json.JSONDecodeError:
            pass
        if response.status_code == 200:
            current_value_match = re.search(r'current_value":(\d+)', response.text)
            current_level_match = re.search(r'current_level":(\d+)', response.text)
            if current_value_match and current_level_match:
                current_value = current_value_match.group(1)
                current_level = current_level_match.group(1)
                return f"👤 用户信息 (兼容模式): V{current_level}会员，成长值 {current_value}"
        return f"❌ 获取用户信息失败：所有模式均未获取到信息。"
    except Exception as e:
        return f"❌ 获取用户信息异常：{e}"


def main():
    """主函数 - 保持简单的顺序执行逻辑"""
    notification_content = []
    
    # 任务 1: 签到
    signin_result = signin()
    print(signin_result)
    notification_content.append(signin_result)
    
    delay(3)
    
    # 任务 2: 每日一题
    answer, ask_id, already_answered = get_daily_question()
    if already_answered:
        answer_result = "🤔 答题提醒：今日已答题"
    elif answer and ask_id:
        answer_result = answer_question(answer, ask_id)
    else:
        answer_result = "🟡 答题跳过：未获取到题目"
    
    print(answer_result)
    notification_content.append(answer_result)
    
    # 任务 3: 获取用户信息
    user_info_result = get_user_info()
    print(user_info_result)
    notification_content.append(user_info_result)
    
    # 最后，整合所有结果并发送通知
    full_content = "\n".join(notification_content)
    send(SCRIPT_TITLE, full_content)


def handler(event, context):
    """青龙面板 Lambda 处理器"""
    main()


if __name__ == "__main__":
    main()
