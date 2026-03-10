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

在青龙面板中执行：

```bash
ql repo https://github.com/LceAn/qinglong-scripts.git
```

### 2️⃣ 配置环境变量

在青龙面板 → 环境变量 中添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `BAIDU_COOKIE` | `BDUSS=xxx; BAIDUID=xxx;` | 百度 Cookie |

### 3️⃣ 添加定时任务

在青龙面板 → 定时任务 中添加新任务：

- **命令：** `python <脚本名>.py`
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
> 暂无，敬请期待...

### Shell 脚本

| 脚本 | 功能 | 推荐指数 | 最后更新 | 状态 | 定时建议 |
|------|------|----------|----------|------|----------|
> 暂无，敬请期待...

---

## ⚙️ 环境变量

### Google Voice 系列

```bash
# 必填
GV_SENDER_EMAIL=your_email@gmail.com
GV_SENDER_PASSWORD=your_app_password
GV_RECEIVER_EMAIL=xxxxxxxx@txt.voice.google.com

# 可选
GV_USE_YAN_YAN=true
GV_YAN_YAN_API=https://v1.hitokoto.cn/
```

**获取方法：**

1. **Gmail 应用专用密码：**
   - 登录 Google 账户 → 安全设置
   - 启用两步验证
   - 生成应用专用密码
   - 复制密码并保存

2. **Google Voice 接收邮箱：**
   - 访问 [Google Voice](https://voice.google.com/)
   - 进入设置 → 账号
   - 找到短信转发邮箱（格式：`xxxxxxxx@txt.voice.google.com`）

3. **配置到青龙：**
   - 青龙面板 → 环境变量
   - 添加上述环境变量

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
# Google Voice 保号短信 - 每 15 天发送一次
0 0 */15 * * *
python google_voice_auto_sms.py

# 百度贴吧签到 - 每天早上 9 点
0 9 * * *
python baidu_tieba.py

# 百度网盘签到 - 每天早上 8 点
0 8 * * *
python baidu_wangpan.py
```

### Cron 表达式参考

| 表达式 | 说明 |
|--------|------|
| `0 9 * * *` | 每天 9:00 |
| `0 8,20 * * *` | 每天 8:00 和 20:00 |
| `*/5 * * * *` | 每 5 分钟 |
| `0 0 * * 0` | 每周日 0:00 |

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
- ...

然后在脚本中读取对应的变量即可。

---

## 📝 更新日志

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

---

<p align="center">
  <b>如果对你有帮助，请给个 ⭐ Star 吧！</b>
</p>
