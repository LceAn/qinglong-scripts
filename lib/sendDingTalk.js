/**
 * 钉钉机器人通知（原生 https 实现，无需依赖）
 * 使用青龙标准环境变量：DD_BOT_TOKEN, DD_BOT_SECRET
 * 用法：await sendDingTalk('通知内容');
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');
const crypto = require('crypto');

/**
 * 原生 HTTP POST 请求
 */
function httpRequest(url, data) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const postData = JSON.stringify(data);
    
    const options = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
      },
    };
    
    const req = (parsedUrl.protocol === 'https:' ? https : http).request(options, (res) => {
      let chunks = [];
      
      res.on('data', (chunk) => {
        chunks.push(chunk);
      });
      
      res.on('end', () => {
        const response = Buffer.concat(chunks).toString();
        try {
          resolve(JSON.parse(response));
        } catch (e) {
          resolve({ raw: response });
        }
      });
    });
    
    req.on('error', (e) => {
      reject(new Error(`请求失败：${e.message}`));
    });
    
    req.write(postData);
    req.end();
  });
}

/**
 * 获取钉钉 Webhook（支持青龙标准环境变量）
 */
function getDingTalkWebhook() {
  // 优先使用青龙标准环境变量
  const token = process.env.DD_BOT_TOKEN;
  const secret = process.env.DD_BOT_SECRET;
  
  if (!token) {
    return null;
  }
  
  let webhook = `https://oapi.dingtalk.com/robot/send?access_token=${token}`;
  
  // 如果配置了签名密钥，添加签名
  if (secret) {
    const timestamp = Date.now().toString();
    const stringToSign = `${timestamp}\n${secret}`;
    const sign = crypto
      .createHmac('sha256', secret)
      .update(stringToSign)
      .digest('base64');
    const encodedSign = encodeURIComponent(sign);
    webhook = `${webhook}&timestamp=${timestamp}&sign=${encodedSign}`;
  }
  
  return webhook;
}

/**
 * 发送钉钉消息（支持 Markdown）
 * @param {string} content - 消息内容（支持 Markdown）
 * @param {string} title - 标题（可选）
 */
async function sendDingTalk(content, title = '通知') {
  const webhook = getDingTalkWebhook();
  
  if (!webhook) {
    console.log('ℹ️  未配置 DD_BOT_TOKEN，跳过钉钉通知');
    return;
  }
  
  const result = await httpRequest(webhook, {
    msgtype: 'markdown',
    markdown: {
      title: title,
      text: content,
    },
  });
  
  if (result.errcode !== 0) {
    throw new Error(`钉钉发送失败：${result.errmsg || '未知错误'}`);
  }
  
  console.log('✅ 钉钉通知发送完成');
}

module.exports = sendDingTalk;
