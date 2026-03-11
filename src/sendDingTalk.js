/**
 * 钉钉机器人通知（原生 https 实现，无需依赖）
 * 用法：await sendDingTalk('通知内容');
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
 * 发送钉钉消息
 * @param {string} content - 消息内容
 * @param {string} title - 标题（可选）
 */
async function sendDingTalk(content, title = '掘金助手通知') {
  const webhook = env.DINGDING_WEBHOOK;
  
  if (!webhook) {
    throw new Error('未配置钉钉机器人 Webhook');
  }
  
  const result = await httpRequest(webhook, {
    msgtype: 'text',
    text: {
      content: `${title}\n${content}`,
    },
  });
  
  if (result.errcode !== 0) {
    throw new Error(`钉钉发送失败：${result.errmsg || '未知错误'}`);
  }
  
  console.log('钉钉通知发送完成');
}

module.exports = sendDingTalk;
