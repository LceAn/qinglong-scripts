/**
 * 邮件发送模块（原生实现，无需依赖）
 * 用法：await sendMail({ from: '掘金', subject: '通知', html: '<h1>内容</h1>' });
 */

const net = require('net');
const crypto = require('crypto');

const env = require('./env');

/**
 * Base64 编码
 */
function base64Encode(str) {
  return Buffer.from(str).toString('base64');
}

/**
 * 生成随机边界
 */
function generateBoundary() {
  return '----=_Part_' + Math.random().toString(16).slice(2);
}

/**
 * 发送邮件（原生 SMTP 实现）
 */
async function sendMail(options) {
  const { from = '掘金助手', subject = '通知', html = '' } = options;
  
  const user = env.EMAIL_USER;
  const pass = env.EMAIL_PASS;
  const to = env.EMAIL_TO || user;
  
  if (!user || !pass) {
    throw new Error('未配置邮箱账号和密码');
  }
  
  // 提取 SMTP 服务器
  const domain = user.match(/@(.*)/);
  const smtpHost = domain ? `smtp.${domain[1]}` : 'smtp.qq.com';
  const smtpPort = 465; // SSL 端口
  
  return new Promise((resolve, reject) => {
    // 注意：原生 net 不支持 SSL，需要用 tls
    const tls = require('tls');
    
    const socket = tls.connect(smtpPort, smtpHost, {
      rejectUnauthorized: false,
    }, () => {
      let step = 0;
      let authData = '';
      
      const sendCommand = (cmd) => {
        socket.write(cmd + '\r\n');
      };
      
      const onData = (data) => {
        const response = data.toString();
        console.log(`SMTP: ${response.trim()}`);
        
        // 220 服务就绪
        if (step === 0 && response.startsWith('220')) {
          step = 1;
          sendCommand(`EHLO ${smtpHost}`);
        }
        // EHLO 响应
        else if (step === 1 && response.includes('250')) {
          step = 2;
          // 开始 AUTH LOGIN
          sendCommand('AUTH LOGIN');
        }
        // 334 VXNlcm5hbWU6 (Username:)
        else if (step === 2 && response.startsWith('334')) {
          step = 3;
          sendCommand(base64Encode(user));
        }
        // 334 UGFzc3dvcmQ6 (Password:)
        else if (step === 3 && response.startsWith('334')) {
          step = 4;
          sendCommand(base64Encode(pass));
        }
        // 235 Authentication successful
        else if (step === 4 && response.startsWith('235')) {
          step = 5;
          sendCommand(`MAIL FROM: <${user}>`);
        }
        // 250 OK
        else if (step === 5 && response.startsWith('250')) {
          step = 6;
          sendCommand(`RCPT TO: <${to}>`);
        }
        // 250 OK
        else if (step === 6 && response.startsWith('250')) {
          step = 7;
          sendCommand('DATA');
        }
        // 354 Start mail input
        else if (step === 7 && response.startsWith('354')) {
          step = 8;
          
          const boundary = generateBoundary();
          const headers = [
            `From: "${from}" <${user}>`,
            `To: <${to}>`,
            `Subject: ${subject}`,
            'MIME-Version: 1.0',
            `Content-Type: text/html; charset="UTF-8"`,
            'Content-Transfer-Encoding: base64',
            '',
          ].join('\r\n');
          
          const body = Buffer.from(html).toString('base64');
          sendCommand(headers + '\r\n' + body + '\r\n\r\n.');
        }
        // 250 OK (邮件发送成功)
        else if (step === 8 && response.startsWith('250')) {
          console.log('邮件发送成功');
          sendCommand('QUIT');
          socket.end();
          resolve();
        }
        // QUIT 响应
        else if (response.startsWith('221') || response.startsWith('421')) {
          socket.end();
        }
        // 错误处理
        else if (response.startsWith('4') || response.startsWith('5')) {
          socket.end();
          reject(new Error(`SMTP 错误：${response.trim()}`));
        }
      };
      
      socket.on('data', onData);
      socket.on('error', (err) => {
        reject(new Error(`SMTP 连接失败：${err.message}`));
      });
    });
    
    socket.on('error', (err) => {
      reject(new Error(`SMTP 连接失败：${err.message}`));
    });
  });
}

module.exports = sendMail;
