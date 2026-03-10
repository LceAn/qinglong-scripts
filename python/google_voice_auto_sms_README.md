# 📮 Google Voice 自动保号短信脚本

> 自动发送保号短信到 Google Voice，支持每日一言功能

---

## 📖 功能特性

- ✅ **自动发送** - 自动发送保号短信到 Google Voice 邮箱
- 📝 **每日一言** - 集成一言 API，每次发送不同的名言警句
- 🔄 **双模式** - 支持每日一言/随机中文两种模式
- 📊 **详细日志** - 完整的发送状态和错误信息
- 🛡️ **错误处理** - 完善的异常捕获和重试机制

---

## 🚀 快速开始

### 1️⃣ 配置环境变量

在青龙面板中添加以下环境变量：

```bash
# Gmail 邮箱配置
export GV_SMTP_SERVER="smtp.gmail.com"
export GV_SMTP_PORT="587"
export GV_SENDER_EMAIL="your_email@gmail.com"
export GV_SENDER_PASSWORD="your_app_password"

# Google Voice 接收邮箱
export GV_RECEIVER_EMAIL="xxxxxxxx@txt.voice.google.com"

# 每日一言配置（可选）
export GV_USE_YAN_YAN="true"
export GV_YAN_YAN_API="https://v1.hitokoto.cn/"
```

### 2️⃣ 添加定时任务

在青龙面板中添加定时任务：

```bash
# 每 15 天发送一次（Google Voice 保号要求）
0 0 */15 * * * python3 /ql/scripts/python/google_voice_auto_sms.py
```

### 3️⃣ 运行脚本

```bash
# 手动运行测试
python3 google_voice_auto_sms.py
```

---

## ⚙️ 配置说明

### 必填配置

| 变量 | 说明 | 示例 |
|------|------|------|
| `GV_SENDER_EMAIL` | 你的 Gmail 邮箱 | `your_email@gmail.com` |
| `GV_SENDER_PASSWORD` | Gmail 应用专用密码 | `abcdefghijklmnop` |
| `GV_RECEIVER_EMAIL` | Google Voice 接收邮箱 | `xxxxxxxx@txt.voice.google.com` |

### 可选配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `GV_SMTP_SERVER` | `smtp.gmail.com` | Gmail SMTP 服务器 |
| `GV_SMTP_PORT` | `587` | SMTP 端口 |
| `GV_USE_YAN_YAN` | `true` | 是否启用每日一言 |
| `GV_YAN_YAN_API` | `https://v1.hitokoto.cn/` | 一言 API 地址 |

---

## 📝 获取 Gmail 应用专用密码

1. 登录你的 Google 账户
2. 访问 [Google 账户安全设置](https://myaccount.google.com/security)
3. 启用 **两步验证**
4. 在 **应用专用密码** 中生成新密码
5. 复制密码并保存到青龙环境变量

---

## 🎯 获取 Google Voice 接收邮箱

1. 访问 [Google Voice](https://voice.google.com/)
2. 进入 **设置** → **账号**
3. 找到 **短信转发** 或 **语音信箱** 相关设置
4. 你的接收邮箱格式为：`xxxxxxxx@txt.voice.google.com`

---

## 🌟 每日一言 API

### 可用 API 列表

| API | 地址 | 说明 |
|-----|------|------|
| 一言 | `https://v1.hitokoto.cn/` | 名人名言、动漫台词等 |
| 情话 | `https://api.uomg.com/api/rand.qinghua` | 土味情话 |
| 诗词 | `https://api.uomg.com/api/rand.shici` | 古诗词 |

### 自定义 API

你可以使用任何返回 JSON 的 API，只需修改 `get_daily_quote()` 函数来解析返回数据。

---

## 📊 日志示例

```
==================================================
🎯 Google Voice 自动保号短信发送
==================================================
📖 正在获取每日一言...
✅ 已获取每日一言：「人生苦短，我用 Python。」—— 某程序员
--------------------------------------------------
正在连接到 SMTP 服务器...
正在登录...
正在发送邮件...
✅ 邮件发送成功！
正在关闭连接...
==================================================
🎉 任务完成！
==================================================
```

---

## ❓ 常见问题

### Q: 发送失败怎么办？

**A:** 检查以下几点：
1. Gmail 邮箱和密码是否正确
2. 是否启用了两步验证并生成了应用专用密码
3. 网络连接是否正常
4. 查看日志中的具体错误信息

### Q: 如何切换为随机中文模式？

**A:** 设置环境变量：
```bash
export GV_USE_YAN_YAN="false"
```

### Q: 多久发送一次合适？

**A:** Google Voice 要求至少每 15 天有一次活动，建议设置为每 10-12 天发送一次。

### Q: 可以自定义短信内容吗？

**A:** 可以，修改脚本中的 `body` 变量即可自定义内容。

---

## 📄 许可证

原始项目：[karllee830/GoogleVoiceAutoSMS](https://github.com/karllee830/GoogleVoiceAutoSMS)  
优化版本由 LceAn 修改并发布

---

## 🔗 相关链接

- [原始项目](https://github.com/karllee830/GoogleVoiceAutoSMS)
- [青龙面板](https://github.com/whyour/qinglong)
- [一言 API](https://hitokoto.cn/)
- [我的青龙脚本仓库](https://github.com/LceAn/qinglong-scripts)

---

<p align="center">
  <b>如果对你有帮助，请给个 ⭐ Star！</b>
</p>
