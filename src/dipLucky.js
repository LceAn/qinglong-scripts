/**
 * 沾喜气功能
 * 用法：const result = await dipLucky();
 */

const env = require('./env');

const headers = {
  'content-type': 'application/json; charset=utf-8',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'zh-CN,zh;q=0.9',
  'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
  'sec-ch-ua-mobile': '?0',
  referer: 'https://juejin.cn/',
  accept: '*/*',
  cookie: env.COOKIE,
};

/**
 * 获取抽奖幸运用户列表
 */
async function getLotteriesLuckyUsers(pageNo = 1, pageSize = 5) {
  const response = await fetch('https://api.juejin.cn/growth_api/v1/lottery_config/get', {
    method: 'GET',
    headers,
    credentials: 'include',
  });
  
  const data = await response.json();
  
  if (data.err_no !== 0) {
    throw new Error(`获取幸运用户失败：${data.err_msg}`);
  }
  
  // 返回第一个幸运用户
  return {
    count: data.data.history_count || 0,
    lotteries: data.data.histories || [],
  };
}

/**
 * 沾喜气
 * @returns {Promise<Object>} 沾喜气结果
 */
async function dipLucky() {
  try {
    // 获取幸运用户列表
    const luckyUsers = await getLotteriesLuckyUsers();
    
    if (luckyUsers.count === 0 || !luckyUsers.lotteries || luckyUsers.lotteries.length === 0) {
      return '无幸运用户可沾';
    }
    
    const firstLuckyUser = luckyUsers.lotteries[0];
    const historyId = firstLuckyUser.lottery_history_id;
    
    if (!historyId) {
      return '获取幸运用户 ID 失败';
    }
    
    // 调用沾喜气 API
    const dipResponse = await fetch('https://api.juejin.cn/growth_api/v1/lottery_lucky/dip', {
      method: 'POST',
      headers,
      credentials: 'include',
      body: JSON.stringify({
        history_id: historyId,
      }),
    });
    
    const dipData = await dipResponse.json();
    
    if (dipData.err_no !== 0) {
      // 可能已经沾过喜气了
      return `沾喜气失败：${dipData.err_msg || '未知错误'}`;
    }
    
    const result = dipData.data;
    return `沾喜气成功！获得 ${result.dip_value || 0} 幸运值，总幸运值：${result.total_value || 0}`;
    
  } catch (error) {
    return `沾喜气异常：${error.message}`;
  }
}

module.exports = dipLucky;
