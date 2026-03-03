"""
百度贴吧自动签到脚本

功能：
- 自动获取关注的贴吧列表
- 自动签到所有贴吧
- 支持多账号（通过环境变量）
- 发送青龙面板通知

环境变量：
- BAIDU_COOKIE: 百度贴吧 Cookie（必填）
  格式：BDUSS=xxx; BAIDUID=xxx; ...

作者：用户自定义
版本：1.0
日期：2026-03-03
"""

import hashlib
import os
import sys
import random
import time
from typing import Optional
import requests

# ================= 青龙面板通知加载块 =================
# 获取当前脚本所在目录及上一级目录（覆盖青龙 scripts 根目录），加入系统路径
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(cur_path)
sys.path.append(root_path)

try:
    from notify import send
except ImportError:
    # 兜底：如果连外层都没有 notify.py，在日志中打印出来防止报错中断
    def send(title, content):
        print(f"\n--- 未发送的通知 (找不到 notify.py) ---\n标题：{title}\n内容:\n{content}\n--------------------")
# ====================================================


class Tieba:
    def __init__(self):
        self.TBS_URL = "http://tieba.baidu.com/dc/common/tbs"
        self.LIKE_URL = "https://c.tieba.baidu.com/c/f/forum/like"
        self.SIGN_URL = "https://c.tieba.baidu.com/c/c/forum/sign"
        self.SIGN_KEY = "tiebaclient!!!"
        self.HEADERS = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 8) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.181 Mobile Safari/537.36",
        }
        self.SIGN_DATA = {
            "_client_type": "2",
            "_client_version": "9.7.8.0",
            "_phone_imei": "000000000000000",
            "model": "MI+5",
            "net_type": "1",
        }
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        
        # 获取 Cookie
        cookie_raw = os.getenv("BAIDU_COOKIE")
        if not cookie_raw:
            raise ValueError("未找到环境变量 BAIDU_COOKIE")
        
        cookie_dict = {
            k.strip(): v.strip()
            for item in cookie_raw.split(";")
            if "=" in item
            for k, v in [item.split("=", 1)]
        }
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie_dict)
        
        self.bduss = cookie_dict.get("BDUSS")
        if not self.bduss:
            raise ValueError("Cookie 中缺少核心字段 BDUSS")

    def encode_data(self, data: dict) -> dict:
        s = "".join(f"{k}={v}" for k, v in sorted(data.items()))
        sign = hashlib.md5((s + self.SIGN_KEY).encode("utf-8")).hexdigest().upper()
        data.update({"sign": sign})
        return data

    def request(self, url: str, method: str = "post", data: Optional[dict] = None) -> dict:
        try:
            if method.lower() == "get":
                resp = self.session.get(url, timeout=10)
            else:
                resp = self.session.post(url, data=data, timeout=10)
            return resp.json() if resp.status_code == 200 else {}
        except Exception as e:
            print(f"请求异常：{e}")
            return {}

    def get_favorite(self) -> list:
        """获取关注的贴吧列表"""
        forums = []
        page_no = 1
        print("正在同步关注列表，请稍候...")
        
        while True:
            raw_data = {
                "BDUSS": self.bduss,
                "_client_id": "wappc_1534235498291_488",
                "from": "1008621y",
                "page_no": str(page_no),
                "page_size": "200",
                "timestamp": str(int(time.time())),
                "vcode_tag": "11",
            }
            raw_data.update(self.SIGN_DATA)
            data = self.encode_data(raw_data)
            res = self.request(self.LIKE_URL, "post", data)
            
            if not res or "forum_list" not in res:
                break
            
            current_page_items = []
            for forum_type in ["non-gconforum", "gconforum"]:
                if forum_type in res["forum_list"]:
                    items = res["forum_list"][forum_type]
                    if isinstance(items, list):
                        current_page_items.extend(items)
                    elif isinstance(items, dict):
                        current_page_items.append(items)
            
            if not current_page_items:
                break
            
            for item in current_page_items:
                if isinstance(item, dict) and "name" in item:
                    forums.append({
                        "name": item.get("name", ""),
                        "fid": item.get("id", ""),
                    })
            
            page_no += 1
            time.sleep(random.uniform(0.5, 1.5))
        
        print(f"共获取到 {len(forums)} 个关注的贴吧")
        return forums

    def get_tbs(self) -> str:
        """获取 TBS 令牌"""
        res = self.request(self.TBS_URL, "get")
        return res.get("tbs", "")

    def sign(self, forum: dict) -> dict:
        """签到单个贴吧"""
        data = {
            "BDUSS": self.bduss,
            "fid": forum["fid"],
            "tbs": self.get_tbs(),
        }
        data.update(self.SIGN_DATA)
        data = self.encode_data(data)
        return self.request(self.SIGN_URL, "post", data)

    def run(self):
        """执行签到任务"""
        result = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "already": 0,
            "details": [],
        }
        
        try:
            forums = self.get_favorite()
            result["total"] = len(forums)
            
            for i, forum in enumerate(forums, 1):
                print(f"[{i}/{len(forums)}] 正在签到：{forum['name']}")
                res = self.sign(forum)
                
                if res.get("error_code") == "0":
                    result["success"] += 1
                    msg = f"✅ {forum['name']} 签到成功"
                    print(msg)
                    result["details"].append(msg)
                elif res.get("error_code") == "160002":
                    result["already"] += 1
                    msg = f"⚠️ {forum['name']} 已签到"
                    print(msg)
                    result["details"].append(msg)
                else:
                    result["failed"] += 1
                    error_msg = res.get("error_msg", "未知错误")
                    msg = f"❌ {forum['name']} 签到失败：{error_msg}"
                    print(msg)
                    result["details"].append(msg)
                
                # 随机延迟，避免请求过快
                time.sleep(random.uniform(0.5, 2.0))
            
        except Exception as e:
            print(f"执行异常：{e}")
            result["details"].append(f"执行异常：{e}")
        
        return result


def main():
    """主函数"""
    print("=" * 50)
    print("百度贴吧自动签到")
    print("=" * 50)
    
    try:
        tieba = Tieba()
        result = tieba.run()
        
        # 生成通知内容
        summary = (
            f"📊 签到汇总\n"
            f"总计：{result['total']} 个贴吧\n"
            f"✅ 成功：{result['success']} 个\n"
            f"⚠️ 已签：{result['already']} 个\n"
            f"❌ 失败：{result['failed']} 个\n"
        )
        
        details = "\n".join(result["details"][:20])  # 只显示前 20 条详情
        if len(result["details"]) > 20:
            details += f"\n... 还有 {len(result['details']) - 20} 条"
        
        content = f"{summary}\n{details}"
        
        # 发送通知
        send("百度贴吧签到", content)
        
        print("\n" + "=" * 50)
        print(summary)
        print("=" * 50)
        
    except ValueError as e:
        error_msg = f"配置错误：{e}"
        print(error_msg)
        send("百度贴吧签到 - 配置错误", error_msg)
    except Exception as e:
        error_msg = f"执行异常：{e}"
        print(error_msg)
        send("百度贴吧签到 - 执行异常", error_msg)


if __name__ == "__main__":
    main()
