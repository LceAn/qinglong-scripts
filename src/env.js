/**
 * 环境变量配置
 * 用法：const env = require('./env');
 */

const env = {
  // 必填
  COOKIE: process.env.JUEJIN_COOKIE || '',
  
  // 通知配置（可选）
  EMAIL_USER: process.env.JUEJIN_EMAIL_USER || '',
  EMAIL_PASS: process.env.JUEJIN_EMAIL_PASS || '',
  EMAIL_TO: process.env.JUEJIN_EMAIL_TO || '',
  
  DINGDING_WEBHOOK: process.env.JUEJIN_DINGDING_WEBHOOK || '',
  WEIXIN_WEBHOOK: process.env.JUEJIN_WEIXIN_WEBHOOK || '',
  FEISHU_WEBHOOK: process.env.JUEJIN_FEISHU_WEBHOOK || '',
  PUSHPLUS_TOKEN: process.env.JUEJIN_PUSHPLUS_TOKEN || '',
  SERVERPUSHKEY: process.env.JUEJIN_SERVERPUSHKEY || '',
  BARK_WEBHOOK: process.env.JUEJIN_BARK_WEBHOOK || '',
  
  // 其他配置
  RETRY_TIMES: parseInt(process.env.JUEJIN_RETRY_TIMES) || 3,
  RETRY_DELAY: parseInt(process.env.JUEJIN_RETRY_DELAY) || 1000,
};

module.exports = env;
