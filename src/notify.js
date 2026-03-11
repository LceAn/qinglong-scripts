/**
 * 统一通知模块（整合所有通知方式）
 * 用法：
 *   const notify = require('./notify');
 *   await notify.send({ title: '标题', content: '内容' });
 */

const sendMail = require('./sendMail');
const sendDingTalk = require('./sendDingTalk');
const sendWxWork = require('./sendWxWork');
const env = require('./env');

class Notify {
  constructor() {
    this.results = [];
  }
  
  /**
   * 发送通知（所有启用的通道）
   * @param {Object} options
   * @param {string} options.title - 标题
   * @param {string} options.content - 内容
   * @param {string} options.html - HTML 内容（用于邮件）
   */
  async send(options) {
    const { title = '掘金助手通知', content = '', html = '' } = options;
    
    const promises = [];
    
    // 邮件通知
    if (env.EMAIL_USER && env.EMAIL_PASS) {
      promises.push(
        this.trySend('邮件', () =>
          sendMail({
            from: '掘金助手',
            subject: title,
            html: html || `<pre>${content}</pre>`,
          })
        )
      );
    }
    
    // 钉钉通知
    if (env.DINGDING_WEBHOOK) {
      promises.push(
        this.trySend('钉钉', () => sendDingTalk(content, title))
      );
    }
    
    // 企业微信通知
    if (env.WEIXIN_WEBHOOK) {
      promises.push(
        this.trySend('企业微信', () => sendWxWork(content))
      );
    }
    
    // 等待所有通知完成
    await Promise.allSettled(promises);
    
    console.log('所有通知发送完成');
  }
  
  /**
   * 尝试发送（捕获错误）
   */
  async trySend(name, fn) {
    try {
      await fn();
      console.log(`[${name}] 发送成功`);
      this.results.push({ name, status: 'success' });
    } catch (error) {
      console.error(`[${name}] 发送失败：${error.message}`);
      this.results.push({ name, status: 'failed', error: error.message });
    }
  }
  
  /**
   * 获取发送结果
   */
  getResults() {
    return this.results;
  }
}

// 导出单例
const notify = new Notify();

module.exports = notify;
module.exports.Notify = Notify;
