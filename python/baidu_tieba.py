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

@cron 0 9 * * *

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
                        "fid": str(item.get("id", "")),
                        "old_level": int(item.get("user_level", 0)),
                        "old_exp": int(item.get("user_exp", 0)),
                    })
            
            if str(res.get("has_more")) != "1":
                break
            
            page_no += 1
            time.sleep(random.uniform(0.5, 1.0))
        
        print(f"共获取到 {len(forums)} 个关注的贴吧")
        return forums



    def get_tbs(self) -> str:
        """获取 TBS 令牌"""
        res = self.request(self.TBS_URL, "get")
        return res.get("tbs", "")

    def final_report(self, total: int, stats: dict):
        """生成最终报告"""
        report = [
            "\n" + "="*30,
            " 贴吧签到运行报告",
            "="*30,
            f"📊 任务总数：{total}",
            f"✅ 成功签到：{stats['success']}",
            f"⏭️ 今日已签：{stats['exist']}",
            f"❌ 签到失败：{stats['error']}",
            f"⬆️ 升级吧数：{len(stats['upgraded'])}"
        ]
        
        if stats["upgraded"]:
            report.append("\n📈 升级名单:")
            for item in stats["upgraded"]:
                report.append(f"- {item}")
        
        report.append("="*30)
        report_text = "\n".join(report)
        print(report_text)
        
        # 发送通知
        try:
            send("贴吧签到报告", report_text)
            print("\n✅ 通知已发送")
        except Exception as e:
            print(f"\n❌ 通知推送异常：{e}")

    def run(self):
        """执行签到任务（批量增强版）"""
        print("--- 百度贴吧自动签到 (推送增强版) ---")
        
        # 获取 TBS
        tbs_res = self.request(self.TBS_URL, method="get")
        tbs = tbs_res.get("tbs") if tbs_res.get("is_login") == 1 else None
        
        if not tbs:
            print("【错误】获取 TBS 失败，登录失效")
            return
        
        # 获取贴吧列表并去重
        raw_forums = self.get_favorite()
        forums = []
        seen_fids = set()
        
        for f in raw_forums:
            if f['fid'] not in seen_fids:
                seen_fids.add(f['fid'])
                forums.append(f)
        
        total = len(forums)
        print(f"列表同步完成：共发现 {total} 个贴吧。")
        
        if total == 0:
            return
        
        # 批量签到
        stats = {
            "success": 0,
            "exist": 0,
            "error": 0,
            "upgraded": [],
        }
        
        pointer = 0
        while pointer < total:
            batch_size = random.randint(5, 10)
            batch = forums[pointer : pointer + batch_size]
            
            for idx, f in enumerate(batch):
                curr_idx = pointer + idx + 1
                time.sleep(random.uniform(0.2, 0.5))
                
                raw_data = {
                    "BDUSS": self.bduss,
                    "fid": f['fid'],
                    "kw": f['name'],
                    "tbs": tbs,
                    "timestamp": str(int(time.time())),
                }
                raw_data.update(self.SIGN_DATA)
                data = self.encode_data(raw_data)
                res = self.request(self.SIGN_URL, "post", data)
                
                code = str(res.get("error_code", ""))
                log_prefix = f"[{curr_idx}/{total}] {f['name']}吧："
                
                if code in ["0", "160002"]:
                    if code == "0":
                        stats["success"] += 1
                    else:
                        stats["exist"] += 1
                    
                    u_info = res.get("user_info", {})
                    new_level = int(u_info.get("user_level", f['old_level']))
                    new_exp = int(u_info.get("user_exp", f['old_exp']))
                    gain_exp = new_exp - f['old_exp'] if new_exp > f['old_exp'] else 0
                    
                    status = "成功" if code == "0" else "已签"
                    exp_tip = f" (Exp+{gain_exp})" if gain_exp > 0 else ""
                    
                    if new_level > f['old_level']:
                        stats["upgraded"].append(f"{f['name']}吧 (Lv.{f['old_level']} -> Lv.{new_level})")
                        print(f"{log_prefix}{status}{exp_tip} ✨ 升级了！")
                    else:
                        print(f"{log_prefix}{status}{exp_tip}")
                else:
                    stats["error"] += 1
                    print(f"{log_prefix}失败 ({res.get('error_msg', '未知错误')})")
            
            pointer += batch_size
            
            if pointer < total:
                wait = random.uniform(6, 12)
                print(f"\n--- 完成一组，随机休眠 {wait:.1f}s ---\n")
                time.sleep(wait)
        
        # 生成最终报告
        self.final_report(total, stats)
        



def main():
    """主函数"""
    try:
        tieba = Tieba()
        tieba.run()
    except ValueError as e:
        error_msg = f"配置错误：{e}"
        print(error_msg)
        send("百度贴吧签到 - 配置错误", error_msg)
    except Exception as e:
        error_msg = f"执行异常：{e}"
        print(error_msg)
        send("百度贴吧签到 - 执行异常", error_msg)


if __name__ == "__main__":
    Tieba().run()
