# 青龙脚本仓库

🎯 开箱即用的青龙定时任务脚本，**无需安装任何依赖**！

## 📦 可用脚本

### 掘金签到系列

| 脚本 | 说明 | 推荐 |
|------|------|------|
| `js/juejin_v3.js` | 整合优化版（签到 + 抽奖 + 沾喜气 + 通知） | ✅ |
| `js/juejin_v2.js` | 优化版 | |

## 🚀 快速开始

### 1. 拉取仓库

在青龙面板执行：

```bash
ql repo https://github.com/LceAn/qinglong-scripts.git "js/juejin" "" "src"
```

### 2. 配置环境变量

必填：
```
JUEJIN_COOKIE=你的掘金 Cookie
```

可选（通知）：
```
JUEJIN_DINGDING_WEBHOOK=钉钉 Webhook
JUEJIN_WEIXIN_WEBHOOK=企业微信 Webhook
JUEJIN_EMAIL_USER=邮箱账号
JUEJIN_EMAIL_PASS=邮箱密码/授权码
JUEJIN_EMAIL_TO=收件人邮箱
```

### 3. 添加定时任务

```
51 9 * * * js/juejin_v3.js
```

## 📁 目录结构

```
qinglong-scripts/
├── js/                 # 主脚本目录
│   ├── juejin_v3.js   # 掘金签到（推荐）
│   └── README.md      # 使用说明
├── src/                # 依赖模块（纯原生）
│   ├── env.js         # 环境变量
│   ├── sendMail.js    # 邮件发送
│   ├── sendDingTalk.js # 钉钉通知
│   ├── sendWxWork.js  # 企业微信
│   ├── dipLucky.js    # 沾喜气
│   └── games/
│       └── autoRun.js # 挖矿游戏
└── README.md           # 本文件
```

## ✅ 特点

- **开箱即用** - 无需安装任何 npm 包
- **纯原生实现** - 使用 Node.js 内置模块
- **多通道通知** - 邮件/钉钉/企业微信
- **自动重试** - 网络请求失败自动重试
- **详细日志** - 执行过程清晰可见

## 📖 详细文档

- [依赖模块说明](src/README.md)
- [掘金脚本说明](js/README.md)

## 🔍 获取 Cookie

1. 访问 https://juejin.cn/ 并登录
2. F12 打开开发者工具 → Network
3. 复制任意请求的 `cookie` 字段
4. 填入 `JUEJIN_COOKIE` 环境变量

## 🐛 常见问题

**Q: 需要安装依赖吗？**
A: 不需要！所有模块均为原生实现。

**Q: 邮件发送失败？**
A: QQ 邮箱需使用授权码（非登录密码），在邮箱设置中获取。

**Q: Cookie 多久过期？**
A: 约 1 个月，过期后重新获取即可。

## 📄 参考

- [iDerekLi/juejin-helper](https://github.com/iDerekLi/juejin-helper)

---

*最后更新：2026-03-11*
