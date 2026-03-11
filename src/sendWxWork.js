/**
 * 企业微信机器人通知（原生 https 实现，无需依赖）
 * 用法：await sendWxWork('通知内容');
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

const env = require('./env');

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
 * 发送企业微信消息（支持 Markdown）
 * @param {string} markdown - Markdown 内容
 */
async function sendWxWork(markdown) {
  const webhook = env.WEIXIN_WEBHOOK;
  
  if (!webhook) {
    throw new Error('未配置企业微信机器人 Webhook');
  }
  
  const result = await httpRequest(webhook, {
    msgtype: 'markdown',
    markdown: {
      content: markdown,
    },
  });
  
  if (result.errcode !== 0) {
    throw new Error(`企业微信发送失败：${result.errmsg || '未知错误'}`);
  }
  
  console.log('企业微信通知发送完成');
  return result;
}

module.exports = sendWxWork;
