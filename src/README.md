# 青龙脚本依赖模块（纯原生实现）

✅ **无需安装任何依赖！开箱即用！**

## 📁 目录结构

```
qinglong-scripts/
├── js/                          # 主脚本
│   ├── juejin_v2.js            # 掘金签到 v2
│   ├── juejin_v3.js            # 掘金签到 v3（推荐）
│   └── README.md               # 使用说明
├── src/                         # 依赖模块（纯原生）
│   ├── env.js                  # 环境变量配置
│   ├── sendMail.js             # 邮件发送（原生 SMTP）
│   ├── sendDingTalk.js         # 钉钉通知（原生 https）
│   ├── sendWxWork.js           # 企业微信通知（原生 https）
│   ├── dipLucky.js             # 沾喜气功能
│   ├── notify.js               # 统一通知模块
│   └── games/
│       └── autoRun.js          # 自动挖矿游戏
└── README.md                    # 本文件
```

## 🚀 使用方法

### 1. 拉取仓库

在青龙面板执行：

```bash
ql repo https://github.com/LceAn/qinglong-scripts.git "js/juejin" "" "src"
```

### 2. 配置环境变量

在青龙面板添加以下环境变量：

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `JUEJIN_COOKIE` | ✅ | 掘金 Cookie（从浏览器获取） |
| `JUEJIN_DINGDING_WEBHOOK` | ❌ | 钉钉机器人 Webhook |
| `JUEJIN_WEIXIN_WEBHOOK` | ❌ | 企业微信机器人 Webhook |
| `JUEJIN_EMAIL_USER` | ❌ | 发件人邮箱 |
| `JUEJIN_EMAIL_PASS` | ❌ | 邮箱密码（SMTP） |
| `JUEJIN_EMAIL_TO` | ❌ | 收件人邮箱（不填则发给发件人） |

### 3. 添加定时任务

```
51 9 * * * js/juejin_v3.js
```

## 📦 模块说明

所有模块均为**纯原生 JavaScript 实现**，无需安装任何 npm 包！

### env.js - 环境变量

```javascript
const env = require('./src/env');
console.log(env.COOKIE);
```

### sendMail.js - 邮件发送

原生 SMTP 实现（支持 SSL）：

```javascript
const sendMail = require('./src/sendMail');

await sendMail({
  from: '掘金助手',
  subject: '签到通知',
  html: '<h1>签到成功</h1>',
});
```

**支持的邮箱：**
- QQ 邮箱 (`smtp.qq.com`)
- 163 邮箱 (`smtp.163.com`)
- Gmail (`smtp.gmail.com`)
- 其他支持 SMTP 的邮箱

### sendDingTalk.js - 钉钉通知

原生 HTTPS 实现：

```javascript
const sendDingTalk = require('./src/sendDingTalk');

await sendDingTalk('签到成功！', '掘金助手');
```

### sendWxWork.js - 企业微信

原生 HTTPS 实现（支持 Markdown）：

```javascript
const sendWxWork = require('./src/sendWxWork');

await sendWxWork(`## 签到通知
> 结果：成功
> 时间：${new Date().toLocaleString()}`);
```

### dipLucky.js - 沾喜气

```javascript
const dipLucky = require('./src/dipLucky');

const result = await dipLucky();
console.log(result);
```

### notify.js - 统一通知

```javascript
const notify = require('./src/notify');

await notify.send({
  title: '标题',
  content: '文本内容',
  html: '<h1>HTML 内容</h1>',
});
```

## 🔍 获取 Cookie

1. 打开浏览器访问 https://juejin.cn/
2. 登录账号
3. 按 F12 打开开发者工具
4. 进入 Network 标签，刷新页面
5. 找到任意 API 请求（如 `api.juejin.cn`）
6. 复制 Request Headers 中的 `cookie` 字段完整内容
7. 填入青龙的 `JUEJIN_COOKIE` 环境变量

**注意：** Cookie 有效期约 1 个月，需定期更新

## ⚠️ 注意事项

1. **无需安装依赖** - 所有模块均为原生实现
2. **邮箱配置** - 需要开启 SMTP 服务（QQ 邮箱在设置中获取授权码）
3. **Cookie 更新** - Cookie 过期后需手动更新
4. **游戏功能** - 海底掘金游戏官方已下线

## 🐛 常见问题

### Q: 邮件发送失败
A: 检查邮箱 SMTP 是否开启，QQ 邮箱需要使用授权码而非登录密码

### Q: 钉钉/企业微信发送失败
A: 检查 Webhook 地址是否正确，机器人是否启用

### Q: Cookie 无效
A: Cookie 已过期，请重新获取

## 📄 参考项目

- [iDerekLi/juejin-helper](https://github.com/iDerekLi/juejin-helper) - 掘金助手核心库

---

*最后更新：2026-03-11*
