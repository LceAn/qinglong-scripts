# 青龙面板脚本仓库

<p align="center">
  <h3 align="center">🐉 青龙面板定时任务脚本</h3>
  <p align="center">
    个人编写的青龙面板脚本集合
    <br>
    <a href="#scripts">查看脚本</a>
    ·
    <a href="#usage">使用说明</a>
    ·
    <a href="#license">许可证</a>
  </p>
</p>

---

## 📖 关于

本仓库用于存放个人编写的青龙面板（QingLong Panel）定时任务脚本。

**青龙面板** 是一个强大的定时任务管理面板，支持运行 Python、JavaScript、Shell 等多种语言的脚本。

---

## 📁 目录结构

```
qinglong-scripts/
├── README.md              # 本文件
├── python/                # Python 脚本
│   └── example.py
├── js/                    # JavaScript 脚本
│   └── example.js
└── shell/                 # Shell 脚本
    └── example.sh
```

---

## 🚀 快速开始

### 1. 拉取仓库

```bash
# 在青龙面板中拉取本仓库
ql repo https://github.com/LceAn/qinglong-scripts.git
```

### 2. 配置环境变量

根据具体脚本需求，在青龙面板中配置相应的环境变量。

### 3. 添加定时任务

在青龙面板中添加定时任务，设置执行时间和脚本名称。

---

## 📝 脚本列表

### Python 脚本

| 脚本名称 | 功能 | 状态 |
|---------|------|------|
| baidu_tieba.py | 百度贴吧自动签到 | ✅ 可用 |
| baidu_wangpan.py | 百度网盘签到任务 | ✅ 可用 |

### JavaScript 脚本

| 脚本名称 | 功能 | 状态 |
|---------|------|------|
| 待添加 | - | - |

### Shell 脚本

| 脚本名称 | 功能 | 状态 |
|---------|------|------|
| 待添加 | - | - |

---

## ⚙️ 环境变量

### 百度系列

| 变量名 | 说明 | 必填 | 适用脚本 |
|-------|------|------|---------|
| BAIDU_COOKIE | 百度 Cookie（包含 BDUSS 字段） | ✅ 必填 | 贴吧、网盘 |

**Cookie 获取方法：**
1. 打开浏览器访问对应网站（tieba.baidu.com 或 pan.baidu.com）
2. 登录百度账号
3. 按 F12 打开开发者工具
4. 复制 Cookie 全部内容
5. 在青龙面板中添加环境变量 `BAIDU_COOKIE`

**Cookie 获取方法：**
1. 打开浏览器访问 tieba.baidu.com
2. 登录百度账号
3. 按 F12 打开开发者工具
4. 复制 Cookie 全部内容
5. 在青龙面板中添加环境变量 `BAIDU_COOKIE`

---

## 📋 定时任务配置示例

### 百度贴吧签到

```bash
# 每天早上 9 点签到
0 9 * * *

# 每天早上 8 点和晚上 8 点各签到一次
0 8,20 * * *
```

### 百度网盘签到

```bash
# 每天早上 8 点签到
0 8 * * *

# 每天早上 9 点签到
0 9 * * *
```

### 通用 Cron 表达式

```bash
# 每天运行一次
0 0 * * *

# 每小时运行一次
0 * * * *

# 每 5 分钟运行一次
*/5 * * * *
```

---

## ⚠️ 注意事项

1. 本仓库脚本仅供学习交流使用
2. 请遵守相关平台的使用条款
3. 使用脚本产生的风险由使用者自行承担
4. 请合理使用定时任务，避免频繁请求

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [青龙面板 GitHub](https://github.com/whyour/qinglong)
- [青龙面板文档](https://docs.qinglong.pro/)
- [百度贴吧](https://tieba.baidu.com)

## 📝 更新日志

### 2026-03-03 (v2)
- ✅ 新增：百度网盘签到脚本 (baidu_wangpan.py)
- ✅ 更新：百度贴吧脚本 v2.0（批量签到、等级检测）
- ✅ 优化：通知报告格式统一

### 2026-03-03 (v1)
- ✅ 新增：百度贴吧自动签到脚本 (baidu_tieba.py)

---

<p align="center">
  ⭐ 如果对你有帮助，请给个 Star 吧！
</p>
