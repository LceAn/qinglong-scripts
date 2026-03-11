# 🐉 青龙脚本仓库

> 📦 个人编写的青龙面板定时任务脚本集合

[![GitHub license](https://img.shields.io/github/license/LceAn/qinglong-scripts)](https://github.com/LceAn/qinglong-scripts/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/LceAn/qinglong-scripts)](https://github.com/LceAn/qinglong-scripts/issues)
[![GitHub stars](https://img.shields.io/github/stars/LceAn/qinglong-scripts)](https://github.com/LceAn/qinglong-scripts/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/LceAn/qinglong-scripts)](https://github.com/LceAn/qinglong-scripts/commits/main)

---

## 📖 目录

- [快速开始](#-快速开始)
- [脚本列表](#-脚本列表)
- [环境变量](#-环境变量)
- [定时任务配置](#-定时任务配置)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)

---

## 🚀 快速开始

### 1️⃣ 拉取仓库

**推荐方式（排除依赖目录）：**

```bash
ql repo https://github.com/LceAn/qinglong-scripts.git "js/|python/" "" "lib/"
```

**参数说明：**
- 第 1 个参数：仓库地址
- 第 2 个参数：白名单（只扫描 `js/` 和 `python/` 目录）
- 第 3 个参数：留空
- 第 4 个参数：黑名单（`lib/` 目录不创建任务）

**或者基础拉取：**

```bash
ql repo https://github.com/LceAn/qinglong-scripts.git
```

### 2️⃣ 配置环境变量

在青龙面板 → 环境变量中添加对应脚本所需的环境变量。

### 3️⃣ 添加定时任务

在青龙面板 → 定时任务 中添加新任务：

- **命令：** `<语言> <脚本路径>`
- **定时规则：** 参考下方的 [定时任务配置](#-定时任务配置)

---

## 📜 脚本列表

### Python 脚本

| 脚本 | 功能 | 推荐指数 | 最后更新 | 状态 | 定时建议 |
|------|------|----------|----------|------|----------|
| [google_voice_auto_sms.py](python/google_voice_auto_sms.py) | Google Voice 自动保号短信 | ⭐⭐⭐⭐⭐ | 2026-03-10 | ✅ 可用 | 每 15 天 0:00 |
| [baidu_tieba.py](python/baidu_tieba.py) | 百度贴吧自动签到 | ⭐⭐⭐⭐⭐ | 2026-03-03 | ✅ 可用 | 每天 9:00 |
| [baidu_wangpan.py](python/baidu_wangpan.py) | 百度网盘签到 + 每日一题 | ⭐⭐⭐⭐⭐ | 2026-03-03 | ✅ 可用 | 每天 8:00 |

### JavaScript 脚本

| 脚本 | 功能 | 推荐指数 | 最后更新 | 状态 | 定时建议 |
|------|------|----------|----------|------|----------|
| [juejin_v3.js](js/juejin_v3.js) | 掘金签到 + 抽奖 + 沾喜气 | ⭐⭐⭐⭐⭐ | 2026-03-11 | ✅ 可用 | 每天 9:51 |
| [juejin_v2.js](js/juejin_v2.js) | 掘金签到（旧版） | ⭐⭐⭐⭐ | 2026-03-11 | ✅ 可用 | 每天 9:51 |

### Shell 脚本

| 脚本 | 功能 | 推荐指数 | 最后更新 | 状态 | 定时建议 |
|------|------|----------|----------|------|----------|
> 暂无，敬请期待...

---

## ⚙️ 环境变量

### 掘金系列

```bash
# 必填
JUEJIN_COOKIE=你的掘金 Cookie

# 通知（可选）
JUEJIN_DINGDING_WEBHOOK=钉钉机器人 Webhook
JUEJIN_WEIXIN_WEBHOOK=企业微信机器人 Webhook
JUEJIN_EMAIL_USER=发件人邮箱
JUEJIN_EMAIL_PASS=邮箱密码/授权码
JUEJIN_EMAIL_TO=收件人邮箱
```

**Cookie 获取方法：**

1. 浏览器访问 [掘金](https://juejin.cn/) 并登录
2. 按 `F12` 打开开发者工具 → Network
3. 复制任意请求的 `Cookie` 字段全部内容
4. 在青龙面板中添加环境变量 `JUEJIN_COOKIE`

---

### Google Voice 系列

```bash
# 必填
GV_SENDER_EMAIL=your_email@gmail.com
GV_SENDER_PASSWORD=xxxxxxxxxxxxxxxx  # 16 位应用专用密码（不是登录密码！）
GV_RECEIVER_EMAIL=xxxxxxxx@txt.voice.google.com

# 可选
GV_USE_YAN_YAN=true
GV_YAN_YAN_API=https://v1.hitokoto.cn/
```

**⚠️ 重要：必须使用应用专用密码！**

Gmail 不允许使用登录密码进行 SMTP 认证，必须使用**应用专用密码（App Password）**。

**获取应用专用密码步骤：**

1. **开启两步验证**
   - 访问：https://myaccount.google.com/security
   - 找到 **两步验证** 并开启
   - 按提示完成手机验证

2. **生成应用专用密码**
   - 访问：https://myaccount.google.com/apppasswords
   - 选择应用：**邮件**
   - 选择设备：**其他（自定义名称）**
   - 输入名称：`QingLong` 或任意
   - 点击 **生成**
   - 复制生成的 **16 位密码**（格式：`xxxx xxxx xxxx xxxx`）

3. **配置到青龙**
   - 青龙面板 → 环境变量
   - 添加 `GV_SENDER_PASSWORD` = 16 位密码（去掉空格）

**Google Voice 接收邮箱获取：**
- 访问 [Google Voice](https://voice.google.com/)
- 进入设置 → 账号
- 找到短信转发邮箱（格式：`xxxxxxxx@txt.voice.google.com`）

---

### 百度系列（共用）

```bash
BAIDU_COOKIE=BDUSS=xxx; BAIDUID=xxx; ...
```

**获取方法：**

1. 浏览器访问 [tieba.baidu.com](https://tieba.baidu.com) 或 [pan.baidu.com](https://pan.baidu.com)
2. 登录百度账号
3. 按 `F12` 打开开发者工具
4. 找到 `Cookie` 并复制全部内容
5. 在青龙面板中添加环境变量 `BAIDU_COOKIE`

---

## 📅 定时任务配置

### 推荐配置

```bash
# 掘金签到 - 每天早上 9:51
51 9 * * *
js/juejin_v3.js

# Google Voice 保号短信 - 每 15 天发送一次（0:00）
0 0 */15 * * *
python google_voice_auto_sms.py

# 百度贴吧签到 - 每天早上 9 点
0 9 * * *
python baidu_tieba.py

# 百度网盘签到 + 每日一题 - 每天早上 8 点
0 8 * * *
python baidu_wangpan.py
```

**提示：** 脚本中已内置 `@cron` 定时规则，青龙拉取后会自动应用。

### Cron 表达式参考

| 表达式 | 说明 |
|--------|------|
| `0 9 * * *` | 每天 9:00 |
| `0 8,20 * * *` | 每天 8:00 和 20:00 |
| `*/5 * * * *` | 每 5 分钟 |
| `0 0 * * 0` | 每周日 0:00 |
| `51 9 * * *` | 每天 9:51 |

---

## ❓ 常见问题

### Q: 如何获取 Cookie？

**A:** 参考上方 [环境变量](#-环境变量) 部分的详细说明。

### Q: 脚本运行失败怎么办？

**A:** 
1. 检查环境变量是否正确配置
2. 检查 Cookie 是否过期（重新获取）
3. 查看运行日志，确认错误信息

### Q: 如何更新脚本？

**A:** 
```bash
# 在青龙面板中重新拉取仓库
ql repo https://github.com/LceAn/qinglong-scripts.git
```

### Q: 可以多个账号一起用吗？

**A:** 
可以！在青龙面板中添加多个环境变量，使用不同的变量名：
- `BAIDU_COOKIE_1`
- `BAIDU_COOKIE_2`
- `JUEJIN_COOKIE_1`
- `JUEJIN_COOKIE_2`
- ...

然后在脚本中读取对应的变量即可。

### Q: JavaScript 脚本需要安装依赖吗？

**A:** 
不需要！所有 JS 脚本均使用 Node.js 原生模块实现，开箱即用。

---

## 📝 更新日志

### v3.3 - 2026-03-11
- ✨ 新增 掘金签到脚本 v3.0（纯原生实现，无需依赖）
- ✨ 新增 掘金签到脚本 v2.0（优化版）
- ✨ 新增 公共通知模块（邮件/钉钉/企业微信）
- 📖 新增 JavaScript 脚本分类说明

### v3.2 - 2026-03-10
- ✨ 新增 Google Voice 自动保号短信脚本
- ✨ 每日一言功能集成（hitokoto.cn）
- 📖 新增 Google Voice 环境变量说明
- 📖 更新定时任务配置示例

### v3.1 - 2026-03-03
- 📖 README 优化 - 脚本列表新增"最后更新"和"状态"列

### v3.0 - 2026-03-03
- ✨ 百度网盘脚本 v2.0 - 新增每日一题自动答题
- 🐛 百度贴吧脚本 v2.0 - 优化通知报告格式
- 📖 README 重构 - 更友好、更美观

### v2.0 - 2026-03-03
- ✨ 百度贴吧脚本 v2.0 - 批量签到、等级检测、经验显示
- 📖 新增环境变量说明和定时任务配置

### v1.0 - 2026-03-03
- ✨ 初始版本 - 百度贴吧自动签到脚本
- 🎉 仓库创建

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 发现 Bug？ → [提交 Issue](https://github.com/LceAn/qinglong-scripts/issues)
- 有新脚本？ → [提交 PR](https://github.com/LceAn/qinglong-scripts/pulls)

---

## 📄 许可证

MIT License © 2026 [LceAn](https://github.com/LceAn)

---

## 🔗 相关链接

- [青龙面板 GitHub](https://github.com/whyour/qinglong)
- [青龙面板文档](https://docs.qinglong.pro/)
- [百度贴吧](https://tieba.baidu.com)
- [百度网盘](https://pan.baidu.com)
- [稀土掘金](https://juejin.cn/)
- [Google Voice](https://voice.google.com/)

---

<p align="center">
  <b>如果对你有帮助，请给个 ⭐ Star 吧！</b>
</p>
