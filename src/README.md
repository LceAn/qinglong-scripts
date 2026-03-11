# 青龙脚本依赖模块

本目录包含掘金签到脚本所需的所有依赖模块。

## 📁 目录结构

```
qinglong-scripts/
├── js/                          # 主脚本
│   ├── juejin_v2.js            # 掘金签到 v2
│   ├── juejin_v3.js            # 掘金签到 v3（推荐）
│   └── README.md               # 使用说明
├── src/                         # 依赖模块
│   ├── env.js                  # 环境变量配置
│   ├── sendMail.js             # 邮件发送
│   ├── sendDingTalk.js         # 钉钉通知
│   ├── sendWxWork.js           # 企业微信通知
│   ├── dipLucky.js             # 沾喜气功能
│   ├── notify.js               # 统一通知模块
│   └── games/
│       └── autoRun.js          # 自动挖矿游戏
└── package.json                 # 依赖声明
```

## 🔧 安装依赖

在青龙容器中执行：

```bash
cd /ql/scripts/qinglong-scripts  # 进入脚本目录
pnpm install                      # 安装依赖
```

或手动安装：

```bash
pnpm add axios nodemailer
```

## 📝 环境变量配置

在青龙面板添加以下环境变量：

### 必填

| 变量名 | 说明 |
|--------|------|
| `JUEJIN_COOKIE` | 掘金 Cookie（从浏览器获取） |

### 通知配置（可选）

| 变量名 | 说明 |
|--------|------|
| `JUEJIN_EMAIL_USER` | 发件人邮箱 |
| `JUEJIN_EMAIL_PASS` | 邮箱密码（SMTP） |
| `JUEJIN_EMAIL_TO` | 收件人邮箱（多人用逗号分隔） |
| `JUEJIN_DINGDING_WEBHOOK` | 钉钉机器人 Webhook |
| `JUEJIN_WEIXIN_WEBHOOK` | 企业微信机器人 Webhook |
| `JUEJIN_FEISHU_WEBHOOK` | 飞书机器人 Webhook |
| `JUEJIN_PUSHPLUS_TOKEN` | PushPlus Token（微信推送） |
| `JUEJIN_SERVERPUSHKEY` | Server 酱 Key（微信推送） |
| `JUEJIN_BARK_WEBHOOK` | Bark Webhook（iOS 推送） |

### 其他配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `JUEJIN_RETRY_TIMES` | 重试次数 | `3` |
| `JUEJIN_RETRY_DELAY` | 重试延迟（毫秒） | `1000` |

## 🚀 使用方法

### 方式一：使用主脚本（推荐）

```javascript
// juejin_v3.js 已包含完整逻辑
// 直接在青龙添加定时任务即可
```

定时任务配置：
```
51 9 * * * js/juejin_v3.js
```

### 方式二：自定义脚本

```javascript
const dipLucky = require('./src/dipLucky');
const notify = require('./src/notify');

(async () => {
  // 执行沾喜气
  const result = await dipLucky();
  console.log(result);
  
  // 发送通知
  await notify.send({
    title: '掘金签到通知',
    content: result,
  });
})();
```

## 📦 模块说明

### env.js - 环境变量

```javascript
const env = require('./src/env');
console.log(env.COOKIE); // 获取 Cookie
```

### sendMail.js - 邮件发送

```javascript
const sendMail = require('./src/sendMail');

await sendMail({
  from: '掘金助手',
  subject: '签到通知',
  html: '<h1>签到成功</h1>',
});
```

### sendDingTalk.js - 钉钉通知

```javascript
const sendDingTalk = require('./src/sendDingTalk');

await sendDingTalk('签到成功！', '掘金助手');
```

### sendWxWork.js - 企业微信

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
  html: '<h1>HTML 内容</h1>', // 用于邮件
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

1. **依赖安装**：首次运行前需执行 `pnpm install`
2. **Cookie 更新**：Cookie 过期后需手动更新
3. **通知配置**：至少配置一种通知方式便于排查问题
4. **游戏功能**：海底掘金游戏官方已下线，挖矿模块仅做兼容

## 📄 参考项目

- [iDerekLi/juejin-helper](https://github.com/iDerekLi/juejin-helper) - 掘金助手核心库

## 🐛 常见问题

### Q: 提示 "Cannot find module 'axios'"
A: 未安装依赖，执行 `pnpm install`

### Q: 通知发送失败
A: 检查对应的 Webhook/邮箱配置是否正确

### Q: Cookie 无效
A: Cookie 已过期，请重新获取

---

*最后更新：2026-03-11*
