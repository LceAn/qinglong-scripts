/**
 * 企业微信机器人通知
 * 用法：await sendWxWork('通知内容');
 */

const axios = require('axios');
const env = require('./env');

/**
 * 发送企业微信消息（支持 Markdown）
 * @param {string} markdown - Markdown 内容
 */
async function sendWxWork(markdown) {
  const webhook = env.WEIXIN_WEBHOOK;
  
  if (!webhook) {
    throw new Error('未配置企业微信机器人 Webhook');
  }
  
  const response = await axios.post(webhook, {
    msgtype: 'markdown',
    markdown: {
      content: markdown,
    },
  });
  
  return response.data;
}

module.exports = sendWxWork;
