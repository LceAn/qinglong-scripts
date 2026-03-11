/**
 * 掘金自动签到脚本 v3.0（整合优化版）
 * 功能：签到 + 抽奖 + 挖矿 + 沾喜气 + 多通道通知
 * 作者：G
 * 优化：2026-03-11
 * 
 * cron: 51 9 * * * juejin_v3.js
 * 
 * 环境变量:
 * - JUEJIN_COOKIE: 必填，掘金 Cookie
 * - JUEJIN_ENABLE_MAIL: 可选，默认 true，启用邮件通知
 * - JUEJIN_ENABLE_DINGTALK: 可选，默认 true，启用钉钉通知
 * - JUEJIN_ENABLE_WXWORK: 可选，默认 true，启用企业微信通知
 * - JUEJIN_RETRY_TIMES: 可选，默认 3，重试次数
 * - JUEJIN_RETRY_DELAY: 可选，默认 1000，重试延迟 (ms)
 */

const fetch = require('node-fetch');

// ==================== 配置 ====================
const CONFIG = {
  COOKIE: process.env.JUEJIN_COOKIE || '',
  ENABLE_MAIL: process.env.JUEJIN_ENABLE_MAIL !== 'false',
  ENABLE_DINGTALK: process.env.JUEJIN_ENABLE_DINGTALK !== 'false',
  ENABLE_WXWORK: process.env.JUEJIN_ENABLE_WXWORK !== 'false',
  RETRY_TIMES: parseInt(process.env.JUEJIN_RETRY_TIMES) || 3,
  RETRY_DELAY: parseInt(process.env.JUEJIN_RETRY_DELAY) || 1000,
};

// API Headers
const getHeaders = () => ({
  'content-type': 'application/json; charset=utf-8',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'zh-CN,zh;q=0.9',
  'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
  'sec-ch-ua-mobile': '?0',
  referer: 'https://juejin.cn/',
  accept: '*/*',
  cookie: CONFIG.COOKIE,
});

// ==================== 工具函数 ====================

// 带重试的 fetch 请求
async function request(url, options = {}, retries = CONFIG.RETRY_TIMES) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: { ...getHeaders(), ...options.headers },
        credentials: 'include',
      });
      const data = await response.json();
      
      if (data.err_no !== 0) {
        throw new Error(data.err_msg || `API 错误：${data.err_no}`);
      }
      
      return data;
    } catch (error) {
      const isLastTry = i === retries - 1;
      console.log(`请求失败 (尝试 ${i + 1}/${retries}): ${error.message}`);
      
      if (!isLastTry) {
        await sleep(CONFIG.RETRY_DELAY);
      } else {
        throw error;
      }
    }
  }
}

// 安全执行（捕获错误并返回错误信息）
async function safeExecute(fn, name) {
  try {
    const result = await fn();
    return result || `${name}成功`;
  } catch (error) {
    const errorMsg = `${name}失败：${error.message}`;
    console.error(errorMsg);
    return errorMsg;
  }
}

// 休眠
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// ==================== 核心功能 ====================

// 检查今日是否已签到
async function checkTodayStatus() {
  const data = await request('https://api.juejin.cn/growth_api/v1/get_today_status', {
    method: 'GET',
  });
  return data.data; // true = 已签到
}

// 签到
async function doSignIn() {
  const data = await request('https://api.juejin.cn/growth_api/v1/check_in', {
    method: 'POST',
  });
  return {
    success: true,
    message: `签到成功！当前积分：${data.data.sum_point}`,
    sumPoint: data.data.sum_point,
    increment: data.data.sum_point - (data.data.sum_point - data.data.incr_point),
  };
}

// 获取当前积分
async function getCurPoint() {
  const data = await request('https://api.juejin.cn/growth_api/v1/get_cur_point', {
    method: 'GET',
  });
  return data.data;
}

// 查询免费抽奖次数
async function getLotteryConfig() {
  const data = await request('https://api.juejin.cn/growth_api/v1/lottery_config/get', {
    method: 'GET',
  });
  return data.data;
}

// 抽奖
async function doDraw() {
  const config = await getLotteryConfig();
  
  if (config.free_count === 0) {
    return '今日已免费抽奖';
  }
  
  const data = await request('https://api.juejin.cn/growth_api/v1/lottery/draw', {
    method: 'POST',
  });
  
  const lotteryName = data.data.lottery_name || '未知奖品';
  const lotteryType = data.data.lottery_type;
  
  // 矿石奖励类型
  if (lotteryType === 1) {
    return `抽奖成功！获得 ${lotteryName} (+66 矿石)`;
  }
  
  return `抽奖成功！获得 ${lotteryName}`;
}

// 挖矿游戏（简化版，调用外部模块）
async function doGame() {
  try {
    const { autoGame } = require('../lib/games/autoRun');
    await autoGame();
    return '挖矿成功！';
  } catch (error) {
    throw new Error(`挖矿失败：${error.message}`);
  }
}

// 沾喜气
async function doDipLucky() {
  try {
    const dipLucky = require('../lib/dipLucky');
    return await dipLucky();
  } catch (error) {
    throw new Error(`沾喜气失败：${error.message}`);
  }
}

// ==================== 通知模块 ====================

async function sendMailNotification(data) {
  try {
    const sendMail = require('../lib/sendMail');
    const html = `
<h1 style="text-align: center">🎉 掘金自动签到通知</h1>
<table style="margin: 20px auto; border-collapse: collapse; width: 80%;">
  <tr style="background: #f5f5f5;">
    <td style="padding: 10px; border: 1px solid #ddd;"><strong>项目</strong></td>
    <td style="padding: 10px; border: 1px solid #ddd;"><strong>结果</strong></td>
  </tr>
  <tr><td style="padding: 10px; border: 1px solid #ddd;">🧧 沾喜气</td><td style="padding: 10px; border: 1px solid #ddd;">${data.dip_res}</td></tr>
  <tr><td style="padding: 10px; border: 1px solid #ddd;">💎 当前矿石</td><td style="padding: 10px; border: 1px solid #ddd;">${data.now_score}</td></tr>
  <tr><td style="padding: 10px; border: 1px solid #ddd;">📈 较昨日增长</td><td style="padding: 10px; border: 1px solid #ddd;">${data.growth}</td></tr>
  <tr><td style="padding: 10px; border: 1px solid #ddd;">✍️ 签到结果</td><td style="padding: 10px; border: 1px solid #ddd;">${data.sign_res}</td></tr>
  <tr><td style="padding: 10px; border: 1px solid #ddd;">🎰 抽奖结果</td><td style="padding: 10px; border: 1px solid #ddd;">${data.draw_res}</td></tr>
  <tr><td style="padding: 10px; border: 1px solid #ddd;">⛏️ 游戏结果</td><td style="padding: 10px; border: 1px solid #ddd;">${data.game_res}</td></tr>
</table>
<p style="text-align: center; color: #999; font-size: 12px; margin-top: 20px;">执行时间：${new Date().toLocaleString('zh-CN')}</p>
`;
    await sendMail({ from: '掘金', subject: '🎉 自动签到通知', html });
    console.log('✅ 邮件通知发送完成');
  } catch (error) {
    console.error('❌ 邮件通知失败:', error.message);
  }
}

async function sendDingTalkNotification(data) {
  try {
    const sendDingTalk = require('../lib/sendDingTalk');
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

async function sendWxWorkNotification(data) {
  try {
    const sendWxWork = require('../lib/sendWxWork');
    const markdown = `## 🎉 掘金自动签到通知
> 🧧 沾喜气结果：<font color="comment">${data.dip_res}</font>
> 💎 当前矿石：<font color="comment">${data.now_score}</font>
> 📈 较昨日增长：<font color="comment">${data.growth}</font>
> ✍️ 签到结果：<font color="comment">${data.sign_res}</font>
> 🎰 抽奖结果：<font color="comment">${data.draw_res}</font>
> ⛏️  游戏结果：<font color="comment">${data.game_res}</font>
> 
> 执行时间：<font color="warning">${new Date().toLocaleString('zh-CN')}</font>`;

    await sendWxWork(markdown);
    console.log('✅ 企业微信通知发送完成');
  } catch (error) {
    console.error('❌ 企业微信通知失败:', error.message);
  }
}

// ==================== 主流程 ====================

(async () => {
  // 检查 Cookie
  if (!CONFIG.COOKIE) {
    console.error('❌ 错误：JUEJIN_COOKIE 环境变量未设置！');
    process.exit(1);
  }
  
  console.log('='.repeat(60));
  console.log('🎉 掘金自动签到任务启动');
  console.log('='.repeat(60));
  
  const startTime = Date.now();
  const result = {
    sign_res: '',
    draw_res: '',
    game_res: '',
    dip_res: '',
    yesterday_score: 0,
    now_score: 0,
    growth: 0,
  };
  
  try {
    // 1. 获取昨日积分
    console.log('\n📊 查询昨日矿石...');
    result.yesterday_score = await safeExecute(getCurPoint, '查询昨日矿石');
    console.log(`昨日矿石：${result.yesterday_score}`);
    await sleep(500);
    
    // 2. 检查是否已签到
    console.log('\n🔍 检查签到状态...');
    const hasSigned = await checkTodayStatus();
    if (hasSigned) {
      result.sign_res = '今日已签到';
      console.log('今日已签到，跳过');
    } else {
      console.log('✍️  执行签到...');
      const signResult = await safeExecute(doSignIn, '签到');
      result.sign_res = signResult.message || signResult;
      console.log(result.sign_res);
    }
    await sleep(500);
    
    // 3. 抽奖
    console.log('\n🎰 执行抽奖...');
    result.draw_res = await safeExecute(doDraw, '抽奖');
    console.log(result.draw_res);
    await sleep(500);
    
    // 4. 挖矿游戏
    console.log('\n⛏️  执行挖矿...');
    result.game_res = await safeExecute(doGame, '挖矿');
    console.log(result.game_res);
    await sleep(500);
    
    // 5. 获取当前积分
    console.log('\n📊 查询当前矿石...');
    result.now_score = await safeExecute(getCurPoint, '查询当前矿石');
    console.log(`当前矿石：${result.now_score}`);
    await sleep(500);
    
    // 6. 沾喜气
    console.log('\n🧧 执行沾喜气...');
    result.dip_res = await safeExecute(doDipLucky, '沾喜气');
    console.log(result.dip_res);
    
    // 7. 计算增长
    result.growth = typeof result.now_score === 'number' && typeof result.yesterday_score === 'number'
      ? result.now_score - result.yesterday_score
      : '未知';
    
    // 8. 发送通知
    console.log('\n📬 发送通知...');
    
    const notifyPromises = [];
    
    if (CONFIG.ENABLE_MAIL) {
      notifyPromises.push(sendMailNotification(result));
    }
    
    if (CONFIG.ENABLE_DINGTALK) {
      notifyPromises.push(sendDingTalkNotification(result));
    }
    
    if (CONFIG.ENABLE_WXWORK) {
      notifyPromises.push(sendWxWorkNotification(result));
    }
    
    if (notifyPromises.length > 0) {
      await Promise.allSettled(notifyPromises);
      console.log('通知发送完成');
    } else {
      console.log('所有通知通道已禁用');
    }
    
  } catch (error) {
    console.error('\n❌ 任务执行异常:', error.message);
  }
  
  // 9. 执行耗时统计
  const duration = ((Date.now() - startTime) / 1000).toFixed(2);
  console.log('\n' + '='.repeat(60));
  console.log(`✅ 任务完成，总耗时：${duration}秒`);
  console.log('='.repeat(60));
})();
