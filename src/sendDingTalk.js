/**
 * 钉钉机器人通知
 * 用法：await sendDingTalk('通知内容');
 */

const axios = require('axios');
const env = require('./env');

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
  
  await axios.post(webhook, {
    msgtype: 'text',
    text: {
      content: `${title}\n${content}`,
    },
  });
  
  console.log('钉钉通知发送完成');
}

module.exports = sendDingTalk;
