# 富邦證券 API 前端應用

這是一個用於測試富邦證券 API 的網頁前端應用，提供完整的交易功能介面。

## 功能特色

### 🔐 認證管理
- 使用者登入/登出
- 支援憑證檔案上傳
- 環境切換（正式/測試）
- 登入狀態顯示

### 📊 市場行情
- 即時報價查詢
- 歷史資料查詢
- 盤中走勢圖
- 報價訂閱管理

### 👤 帳戶管理
- 帳戶資訊總覽
- 資金餘額查詢
- 持股明細展示
- 損益統計分析

### 💰 交易下單
- 快速下單介面
- 支援限價/市價單
- 今日委託查詢
- 訂單取消/修改

## 技術架構

- **前端框架**: React 18
- **建構工具**: Vite 5
- **HTTP 客戶端**: Axios
- **樣式**: 原生 CSS（不使用第三方 UI 框架）

## 快速開始

### 前置需求

- Node.js 16+
- npm 或 yarn
- 後端 API 服務運行中（預設 http://localhost:8000）

### 安裝步驟

1. 進入前端目錄：
```bash
cd frontend
```

2. 安裝依賴：
```bash
npm install
```

3. 啟動開發伺服器：
```bash
npm run dev
```

4. 開啟瀏覽器訪問：http://localhost:3000

### 使用啟動腳本

也可以使用專案根目錄的啟動腳本：

```bash
./start_frontend.sh
```

## 專案結構

```
frontend/
├── index.html              # HTML 入口
├── package.json            # 專案配置
├── vite.config.js          # Vite 配置
└── src/
    ├── main.jsx            # 應用入口
    ├── App.jsx             # 主要應用組件
    ├── App.css             # 應用樣式
    ├── index.css           # 全域樣式
    ├── api.js              # API 封裝
    └── components/         # React 組件
        ├── Header.jsx      # 頂部導航
        ├── LoginPanel.jsx  # 登入面板
        ├── MarketPanel.jsx # 市場行情
        ├── AccountPanel.jsx # 帳戶管理
        └── OrderPanel.jsx  # 交易下單
```

## 環境配置

應用支援兩種環境模式：

### 測試環境（預設）
- 使用 Mock 資料
- 可使用任意帳號密碼登入
- 適合功能測試和開發

### 正式環境
- 連接真實 API
- 需要真實帳號和憑證
- 用於實際交易

在頂部導航可以隨時切換環境，切換時會自動登出。

## API 整合

所有 API 呼叫都封裝在 `src/api.js` 中：

```javascript
import api from './api';

// 使用範例
const result = await api.login({
  user_id: 'test_user',
  password: 'test_password',
  cert_path: '/tmp/test.pfx'
});
```

### 可用的 API 方法

**認證相關**
- `login(credentials)` - 登入
- `logout()` - 登出
- `checkStatus()` - 檢查登入狀態

**市場行情**
- `getQuote(stockCodes)` - 即時報價
- `getHistoricalData(stockCode, interval, startDate, endDate)` - 歷史資料
- `getIntradayData(stockCode)` - 盤中走勢
- `subscribeQuote(stockCodes)` - 訂閱報價
- `unsubscribeQuote(stockCodes)` - 取消訂閱

**交易下單**
- `placeOrder(orderData)` - 下單
- `cancelOrder(orderId)` - 取消訂單
- `modifyOrder(orderId, price, quantity)` - 修改訂單
- `queryOrders(filters)` - 查詢訂單
- `getOrderDetail(orderId)` - 訂單詳情
- `getTodayOrders()` - 今日委託

**帳戶管理**
- `getAccountInfo()` - 帳戶資訊
- `getBalance()` - 資金餘額
- `getBuyingPower()` - 購買力
- `getPositions()` - 持股明細
- `getPosition(stockCode)` - 單一持股
- `getSettlements()` - 交割資訊
- `getProfitLoss()` - 損益統計
- `getMarginInfo()` - 融資融券
- `getAccountSummary()` - 帳戶摘要

## 憑證上傳功能

應用支援兩種憑證設定方式：

### 1. 輸入憑證路徑
直接輸入伺服器上憑證檔案的路徑

### 2. 上傳憑證檔案
- 支援拖曳上傳
- 支援點擊選擇檔案
- 接受 .pfx 和 .p12 格式

> ⚠️ 注意：測試模式下檔案不會真的上傳到伺服器，僅用於演示介面功能。

## 開發指南

### 新增功能

1. 在 `src/api.js` 新增 API 方法
2. 建立對應的 React 組件
3. 在 `App.jsx` 中整合新組件
4. 添加相應的樣式

### 建構生產版本

```bash
npm run build
```

建構產物會輸出到 `dist/` 目錄。

### 預覽生產版本

```bash
npm run preview
```

## 瀏覽器支援

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## 常見問題

### Q: 無法連接到後端 API
A: 確認後端服務是否運行在 http://localhost:8000

### Q: 登入後無法查詢資料
A: 檢查是否使用測試模式，以及後端是否正常回應

### Q: 憑證上傳無效
A: 測試模式下憑證不會真的上傳，這是正常的

## 授權

MIT License

## 聯絡資訊

如有問題或建議，請聯繫開發團隊。
