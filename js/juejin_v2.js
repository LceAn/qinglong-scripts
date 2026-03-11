/**
 * 掘金自动签到脚本 v2.1
 * 功能：签到 + 抽奖 + 挖矿 + 沾喜气 + 多通道通知
 * 作者：G
 * 优化：2026-03-11
 * 
 * @cron 51 9 * * *
 */

const sign_in = require('../lib/signIn');
const draw = require('../lib/draw');
const dipLucky = require('../lib/dipLucky');
const sendMail = require('../lib/sendMail');
const sendDingTalk = require('../lib/sendDingTalk');
const sendWxWork = require('../lib/sendWxWork');
const getPoint = require('../lib/getPoint');
const { autoGame } = require('../lib/games/autoRun');

// 配置项（可通过环境变量覆盖）
const CONFIG = {
  ENABLE_MAIL: process.env.JUEJIN_ENABLE_MAIL !== 'false',
  ENABLE_DINGTALK: process.env.JUEJIN_ENABLE_DINGTALK !== 'false',
  ENABLE_WXWORK: process.env.JUEJIN_ENABLE_WXWORK !== 'false',
  RETRY_TIMES: parseInt(process.env.JUEJIN_RETRY_TIMES) || 3,
  RETRY_DELAY: parseInt(process.env.JUEJIN_RETRY_DELAY) || 1000,
};

// 工具函数：带重试的异步操作
async function retryAsync(fn, name, maxRetries = CONFIG.RETRY_TIMES) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      const isLastTry = i === maxRetries - 1;
      console.log(`${name} 失败 (尝试 ${i + 1}/${maxRetries}): ${error.message}`);
      
      if (!isLastTry) {
        await new Promise(resolve => setTimeout(resolve, CONFIG.RETRY_DELAY));
      } else {
        throw error;
      }
    }
  }
}

// 工具函数：安全执行（捕获错误并返回错误信息）
async function safeExecute(fn, name) {
  try {
    const result = await retryAsync(fn, name);
    return result || `${name}成功`;
  } catch (error) {
    const errorMsg = `${name}失败：${error.message}`;
    console.error(errorMsg);
    return errorMsg;
  }
}

// 工具函数：休眠
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
  console.log('='.repeat(50));
  console.log('🎉 掘金自动签到任务启动');
  console.log('='.repeat(50));
  
  const startTime = Date.now();
  
  // 1. 获取昨日分数
  console.log('\n📊 查询昨日矿石...');
  const yesterday_score = await safeExecute(getPoint, '查询昨日矿石');
  console.log(`昨日矿石：${yesterday_score}`);
  
  await sleep(500); // 避免请求过快
  
  // 2. 签到
  console.log('\n✍️  执行签到...');
  const sign_res = await safeExecute(sign_in, '签到');
  console.log(sign_res);
  
  await sleep(500);
  
  // 3. 抽奖
  console.log('\n🎰 执行抽奖...');
  const draw_res = await safeExecute(draw, '抽奖');
  console.log(draw_res);
  
  await sleep(500);
  
  // 4. 挖矿游戏
  console.log('\n⛏️  执行挖矿...');
  const game_res = await safeExecute(autoGame, '挖矿');
  console.log(game_res);
  
  await sleep(500);
  
  // 5. 获取当前分数
  console.log('\n📊 查询当前矿石...');
  const now_score = await safeExecute(getPoint, '查询当前矿石');
  console.log(`当前矿石：${now_score}`);
  
  await sleep(500);
  
  // 6. 沾喜气
  console.log('\n🧧 执行沾喜气...');
  const dip_res = await safeExecute(dipLucky, '沾喜气');
  console.log(dip_res);
  
  // 计算增长
  const growth = typeof now_score === 'number' && typeof yesterday_score === 'number' 
    ? now_score - yesterday_score 
    : '未知';
  
  // 7. 发送通知（并行执行，互不影响）
  console.log('\n📬 发送通知...');
  
  const notifyData = {
    dip_res,
    now_score,
    growth,
    sign_res,
    draw_res,
    game_res,
  };
  
  // 并行发送所有启用的通知
  const notifyPromises = [];
  
  if (CONFIG.ENABLE_MAIL) {
    notifyPromises.push(sendMailNotification(notifyData));
  }
  
  if (CONFIG.ENABLE_DINGTALK) {
    notifyPromises.push(sendDingTalkNotification(notifyData));
  }
  
  if (CONFIG.ENABLE_WXWORK) {
    notifyPromises.push(sendWxWorkNotification(notifyData));
  }
  
  if (notifyPromises.length > 0) {
    await Promise.allSettled(notifyPromises);
    console.log('通知发送完成');
  } else {
    console.log('所有通知通道已禁用');
  }
  
  // 8. 执行耗时统计
  const duration = ((Date.now() - startTime) / 1000).toFixed(2);
  console.log('\n' + '='.repeat(50));
  console.log(`✅ 任务完成，总耗时：${duration}秒`);
  console.log('='.repeat(50));
})();

// 邮件通知
async function sendMailNotification(data) {
  try {
    const html = `
<h1 style="text-align: center">🎉 掘金自动签到通知</h1>
<table style="margin: 20px auto; border-collapse: collapse;">
  <tr><td style="padding: 8px">🧧 沾喜气结果:</td><td style="padding: 8px">${data.dip_res}</td></tr>
  <tr><td style="padding: 8px">💎 当前矿石:</td><td style="padding: 8px">${data.now_score}</td></tr>
  <tr><td style="padding: 8px">📈 较昨日增长:</td><td style="padding: 8px">${data.growth}</td></tr>
  <tr><td style="padding: 8px">✍️ 签到结果:</td><td style="padding: 8px">${data.sign_res}</td></tr>
  <tr><td style="padding: 8px">🎰 抽奖结果:</td><td style="padding: 8px">${data.draw_res}</td></tr>
  <tr><td style="padding: 8px">⛏️  游戏结果:</td><td style="padding: 8px">${data.game_res}</td></tr>
</table>
<p style="text-align: center; color: #999; font-size: 12px">执行时间：${new Date().toLocaleString('zh-CN')}</p>
`;
    await sendMail({ from: '掘金', subject: '🎉 自动签到通知', html });
    console.log('✅ 邮件通知发送完成');
  } catch (error) {
    console.error('❌ 邮件通知失败:', error.message);
  }
}

// 钉钉通知
async function sendDingTalkNotification(data) {
  try {
    const msg = `🎉 掘金自动签到通知
━━━━━━━━━━━━━━━━
🧧 沾喜气结果：${data.dip_res}
💎 当前矿石：${data.now_score}
📈 较昨日增长：${data.growth}
✍️ 签到结果：${data.sign_res}
🎰 抽奖结果：${data.draw_res}
⛏️  游戏结果：${data.game_res}
━━━━━━━━━━━━━━━━
执行时间：${new Date().toLocaleString('zh-CN')}`;

    await sendDingTalk(msg);
    console.log('✅ 钉钉通知发送完成');
  } catch (error) {
    console.error('❌ 钉钉通知失败:', error.message);
  }
}

// 企业微信通知
async function sendWxWorkNotification(data) {
  try {
    const markdown = `## 🎉 掘金自动签到通知
> 🧧 沾喜气结果：<font color="comment">${data.dip_res}</font>
> 💎 当前矿石：<font color="comment">${data.now_score}</font>
> 📈 较昨日增长：<font color="comment">${data.growth}</font>
> ✍️ 签到结果：<font color="comment">${data.sign_res}</font>
> 🎰 抽奖结果：<font color="comment">${data.draw_res}</font>
> ⛏️  游戏结果：<font color="comment">${data.game_res}</font>
> 
> 执行时间：<font color="warning">${new Date().toLocaleString('zh-CN')}</font>`;

    const msg = await sendWxWork(markdown);
    console.log('✅ 企业微信通知发送完成');
    return msg;
  } catch (error) {
    console.error('❌ 企业微信通知失败:', error.message);
  }
}
