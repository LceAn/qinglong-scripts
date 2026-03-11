/**
 * 邮件发送模块
 * 依赖：nodemailer
 * 用法：await sendMail({ from: '掘金', subject: '通知', html: '<h1>内容</h1>' });
 */

const nodemailer = require('nodemailer');
const env = require('./env');

/**
 * 发送邮件
 * @param {Object} options 
 * @param {string} options.from - 发件人名称
 * @param {string} options.subject - 邮件主题
 * @param {string} options.html - HTML 内容
 */
async function sendMail(options) {
  const { from = '掘金助手', subject = '通知', html = '' } = options;
  
  const auth = {
    user: env.EMAIL_USER,
    pass: env.EMAIL_PASS,
  };
  
  if (!auth.user || !auth.pass) {
    throw new Error('未配置邮箱账号和密码');
  }
  
  // 提取域名
  const domain = auth.user.match(/@(.*)/);
  const smtpHost = domain ? `smtp.${domain[1]}` : 'smtp.qq.com';
  
  // 创建 transporter
  const transporter = nodemailer.createTransport({
    host: smtpHost,
    port: 465,
    secure: true,
    auth,
    tls: {
      rejectUnauthorized: false,
    },
  });
  
  // 发送邮件
  await transporter.sendMail({
    from: `"${from}" <${auth.user}>`,
    to: env.EMAIL_TO || auth.user,
    subject: subject,
    html: html,
  });
  
  console.log('邮件发送完成');
}

module.exports = sendMail;
