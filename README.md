# 青龙脚本仓库

🎯 青龙定时任务脚本集合 - 开箱即用，无需安装依赖！

## 📦 脚本列表

### 📰 签到脚本

| 名称 | 路径 | 说明 |
|------|------|------|
| 掘金签到 | `js/juejin_v3.js` | 掘金每日签到 + 抽奖 + 沾喜气 |
| 掘金签到 v2 | `js/juejin_v2.js` | 掘金签到（旧版） |

### 🐍 Python 脚本

查看 `python/` 目录获取更多 Python 脚本。

### 📝 Shell 脚本

查看 `shell/` 目录获取更多 Shell 脚本。

## 🚀 快速开始

### 1. 拉取仓库

在青龙面板执行：

```bash
ql repo https://github.com/LceAn/qinglong-scripts.git "js/|python/|shell/" "" ""
```

### 2. 配置环境变量

根据具体脚本需求配置对应的环境变量。

**掘金签到脚本环境变量：**

```bash
# 必填
JUEJIN_COOKIE=你的掘金 Cookie

# 通知（可选）
JUEJIN_DINGDING_WEBHOOK=钉钉 Webhook
JUEJIN_WEIXIN_WEBHOOK=企业微信 Webhook
JUEJIN_EMAIL_USER=邮箱账号
JUEJIN_EMAIL_PASS=邮箱密码/授权码
JUEJIN_EMAIL_TO=收件人邮箱
```

### 3. 添加定时任务

在青龙面板添加定时任务，格式：

```
* * * * * 脚本路径
```

例如掘金签到（每天 9:51 执行）：

```
51 9 * * * js/juejin_v3.js
```

## 📁 目录结构

```
qinglong-scripts/
├── js/                    # JavaScript 脚本
│   ├── juejin_v3.js      # 掘金签到 v3
│   ├── juejin_v2.js      # 掘金签到 v2
│   └── README.md         # JS 脚本说明
├── python/                # Python 脚本
├── shell/                 # Shell 脚本
├── src/                   # 公共依赖模块
│   ├── env.js            # 环境变量配置
│   ├── sendMail.js       # 邮件发送
│   ├── sendDingTalk.js   # 钉钉通知
│   ├── sendWxWork.js     # 企业微信通知
│   └── ...
└── README.md              # 本文件
```

## ✅ 特点

- **开箱即用** - JavaScript 脚本使用 Node.js 原生模块，无需安装依赖
- **多语言支持** - JavaScript / Python / Shell
- **模块化设计** - 公共功能封装在 `src/` 目录
- **易于扩展** - 欢迎提交新的脚本

## 📖 详细文档

- [掘金签到脚本说明](js/README.md)
- [公共模块说明](src/README.md)

## 🤝 贡献

欢迎提交新的脚本或改进现有脚本！

### 提交规范

1. 脚本放在对应语言目录（`js/` / `python/` / `shell/`）
2. 公共功能可放在 `src/` 目录
3. 在脚本开头添加必要注释（功能说明、环境变量、定时任务格式）
4. 更新本 README 添加脚本说明

### 代码风格

- **JavaScript**: 使用 Node.js 原生模块，避免外部依赖
- **Python**: 使用标准库，如需第三方库请说明
- **Shell**: 兼容 bash/sh

## 📮 问题反馈

如有问题或建议，欢迎提交 Issue。

## 📄 许可证

MIT License

---

*最后更新：2026-03-11*
