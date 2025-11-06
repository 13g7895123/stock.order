import axios from 'axios';

// 建立 axios 實例
const createApiClient = (baseURL) => {
  return axios.create({
    baseURL,
    timeout: 30000,
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

// API 類別
class FubonAPI {
  constructor(baseURL) {
    this.client = createApiClient(baseURL);
    this.baseURL = baseURL;
  }

  // 更新 base URL
  setBaseURL(baseURL) {
    this.baseURL = baseURL;
    this.client = createApiClient(baseURL);
  }

  // ========== 認證相關 ==========
  
  async login(credentials, environment = 'test') {
    // 根據環境設定 use_mock 參數
    const loginData = {
      ...credentials,
      use_mock: environment === 'test'  // 測試環境使用 Mock，正式環境使用真實 SDK
    };
    const response = await this.client.post('/api/v1/auth/login', loginData);
    return response.data;
  }

  async logout() {
    const response = await this.client.post('/api/v1/auth/logout');
    return response.data;
  }

  async checkStatus() {
    const response = await this.client.get('/api/v1/auth/status');
    return response.data;
  }

  // ========== 市場行情 ==========
  
  async subscribeQuote(stockCodes) {
    const response = await this.client.post('/api/v1/market/subscribe', {
      stock_codes: stockCodes
    });
    return response.data;
  }

  async unsubscribeQuote(stockCodes) {
    const response = await this.client.post('/api/v1/market/unsubscribe', {
      stock_codes: stockCodes
    });
    return response.data;
  }

  async getQuote(stockCodes) {
    const response = await this.client.post('/api/v1/market/quote', {
      stock_codes: stockCodes
    });
    return response.data;
  }

  async getHistoricalData(stockCode, interval = 'D', startDate = null, endDate = null) {
    const response = await this.client.post('/api/v1/market/historical', {
      stock_code: stockCode,
      interval,
      start_date: startDate,
      end_date: endDate
    });
    return response.data;
  }

  async getIntradayData(stockCode) {
    const response = await this.client.post('/api/v1/market/intraday', {
      stock_code: stockCode
    });
    return response.data;
  }

  // ========== 交易下單 ==========
  
  async placeOrder(orderData) {
    const response = await this.client.post('/api/v1/order/place', orderData);
    return response.data;
  }

  async cancelOrder(orderId) {
    const response = await this.client.post('/api/v1/order/cancel', {
      order_id: orderId
    });
    return response.data;
  }

  async modifyOrder(orderId, price = null, quantity = null) {
    const response = await this.client.post('/api/v1/order/modify', {
      order_id: orderId,
      price,
      quantity
    });
    return response.data;
  }

  async queryOrders(filters = {}) {
    const response = await this.client.post('/api/v1/order/query', filters);
    return response.data;
  }

  async getOrderDetail(orderId) {
    const response = await this.client.get(`/api/v1/order/detail/${orderId}`);
    return response.data;
  }

  async getTodayOrders() {
    const response = await this.client.get('/api/v1/order/today');
    return response.data;
  }

  // ========== 帳戶管理 ==========
  
  async getAccountInfo() {
    const response = await this.client.get('/api/v1/account/info');
    return response.data;
  }

  async getBalance() {
    const response = await this.client.get('/api/v1/account/balance');
    return response.data;
  }

  async getBuyingPower() {
    const response = await this.client.get('/api/v1/account/buying-power');
    return response.data;
  }

  async getPositions() {
    const response = await this.client.get('/api/v1/account/positions');
    return response.data;
  }

  async getPosition(stockCode) {
    const response = await this.client.post('/api/v1/account/position', {
      stock_code: stockCode
    });
    return response.data;
  }

  async getSettlements() {
    const response = await this.client.get('/api/v1/account/settlements');
    return response.data;
  }

  async getProfitLoss() {
    const response = await this.client.get('/api/v1/account/profit-loss');
    return response.data;
  }

  async getMarginInfo() {
    const response = await this.client.get('/api/v1/account/margin');
    return response.data;
  }

  async getAccountSummary() {
    const response = await this.client.get('/api/v1/account/summary');
    return response.data;
  }

  // ========== 健康檢查 ==========
  
  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }
}

// 環境配置
export const ENV_CONFIG = {
  production: {
    name: '正式環境',
    baseURL: 'http://localhost:8000',
    description: '使用真實 SDK（需安裝 fubon-neo）',
    mode: 'production'
  },
  test: {
    name: '測試環境',
    baseURL: 'http://localhost:8000',
    description: '使用 Mock 資料進行測試',
    mode: 'test'
  }
};

// 預設使用測試環境
export const api = new FubonAPI(ENV_CONFIG.test.baseURL);

export default api;
