# 富邦證券 (Fubon Securities) API 文件

## 券商資訊

- **券商名稱**: 富邦綜合證券股份有限公司
- **英文名稱**: Fubon Securities Co., Ltd.
- **英文縮寫**: Fubon / FBS
- **API 名稱**: Fubon Neo API (新一代 API)

## API 官方資源

- **官方網站**: https://www.fbs.com.tw/TradeAPI/en/
- **開發者文件**: https://www.fbs.com.tw/TradeAPI/en/docs/trading/introduction/
- **期貨 API (gTrade)**: https://www.fubon.com/futures/home/instructions/gtrade.html

## 主要特色

### 1. 支援的程式語言
- **Python** (推薦)
- **C#**
- **Node.js (JavaScript)**

### 2. 支援的作業系統
- **Windows**
- **macOS**
- **Linux**

### 3. 支援的市場
- 台灣證券市場
- 台灣期貨市場
- 全球市場

### 4. 核心功能
- 即時市場行情 (Live Market Data)
- 歷史行情資料 (Archived Market Data)
- 無縫下單執行 (Seamless Order Execution)
- 帳戶監控 (Account Oversight)
- 投資組合監控 (Portfolio Oversight)

### 5. API 優勢
- **跨平台支援**: Windows、macOS、Linux 全支援
- **多語言 SDK**: 支援主流程式語言
- **現代化架構**: 新一代 API 設計
- **完整文件**: 提供詳細的開發者文件

## 技術規格

### 安裝方式

#### Python
```bash
pip install fubon-neo
```

#### Node.js
```bash
npm install @fubon/neo
```

#### C#
需從官方網站下載 SDK

### 基本使用範例 (Python)

```python
from fubon_neo.sdk import FubonSDK

# 初始化 SDK
sdk = FubonSDK()

# 登入
sdk.login(
    user_id="YOUR_USER_ID",
    password="YOUR_PASSWORD",
    cert_path="YOUR_CERT_PATH"
)

# 訂閱即時報價
sdk.init_realtime()
sdk.quote.subscribe("2330")  # 台積電

# 下單
order = sdk.order.place_order(
    stock_no="2330",
    action="Buy",
    price=600,
    quantity=1,
    price_type="Limit",
    order_type="ROD"
)

# 查詢帳戶
account_info = sdk.get_account()
```

### 基本使用範例 (Node.js)

```javascript
const { FubonSDK } = require('@fubon/neo');

// 初始化 SDK
const sdk = new FubonSDK();

// 登入
await sdk.login({
  userId: 'YOUR_USER_ID',
  password: 'YOUR_PASSWORD',
  certPath: 'YOUR_CERT_PATH'
});

// 訂閱報價
await sdk.quote.subscribe('2330');

// 下單
const order = await sdk.order.placeOrder({
  stockNo: '2330',
  action: 'Buy',
  price: 600,
  quantity: 1,
  priceType: 'Limit',
  orderType: 'ROD'
});
```

## 下單參數說明

### Action (動作)
- `Buy`: 買進
- `Sell`: 賣出

### Price Type (價格類型)
- `Limit`: 限價
- `Market`: 市價
- `MarketRange`: 範圍市價

### Order Type (委託類型)
- `ROD`: 當日有效 (Rest of Day)
- `IOC`: 立即成交否則取消 (Immediate or Cancel)
- `FOK`: 全部成交否則取消 (Fill or Kill)

### Order Condition (委託條件)
- `Cash`: 現股
- `Margin`: 融資
- `Short`: 融券

## 申請流程

### 1. 開立富邦證券帳戶
- 需要有富邦證券交易帳戶
- 可線上或臨櫃開戶

### 2. 申請 API 服務
- 聯繫您的富邦證券營業員
- 填寫 API 服務申請表
- 簽署程式交易風險預告書

### 3. 取得憑證
- 申請核准後下載數位憑證
- 用於 API 登入驗證

### 4. 下載 SDK
- 從官方網站下載對應語言的 SDK
- 安裝並設定開發環境

### 5. 開始開發
- 參考官方文件進行開發
- 建議先在測試環境測試

## 使用限制與注意事項

### 1. 使用資格
- 需要具備富邦證券帳戶
- 需簽署 API 交易風險預告書
- 需通過營業員審核

### 2. 技術要求
- 需具備程式開發能力 (Python/C#/Node.js)
- 建議熟悉非同步程式設計
- 需了解金融市場交易規則

### 3. 安全性要求
- 妥善保管憑證檔案
- 不可分享帳號密碼
- 建議使用環境變數儲存敏感資訊

### 4. 交易限制
- 遵守台灣證券交易所交易規則
- 注意當日沖銷條件
- 遵守漲跌幅限制
- API 可能有呼叫頻率限制

### 5. 費用
- API 使用免費
- 交易手續費依照帳戶約定費率
- 可能需要達到一定的交易條件

## 教學資源

### 官方資源
- **開發者文件**: https://www.fbs.com.tw/TradeAPI/en/docs/trading/introduction/
- **官方範例**: SDK 內附範例程式
- **API 規格**: 詳細的 API Reference

### 社群資源
- **GitHub 教學**:
  - [C# 富邦期貨 API 開發教學](https://github.com/eermagic/csharp-fubon-future-api-guide)
  - [股票交易自動化串接教學範例](https://github.com/phenomenoner/TopTrader_I)

- **部落格文章**:
  - 理財工程師 Mars: [C# 富邦期貨 API 開發教學](https://blog.hungwin.com.tw/csharp-fubon-future-api-guide/)

## 富邦期貨 gTrade API

除了 Neo API，富邦也提供期貨專用的 gTrade API：

- **文件**: https://www.fubon.com/futures/home/instructions/gtrade.html
- **適用**: 期貨交易
- **功能**: 期貨下單、查詢、行情

## 常見問題 FAQ

### Q1: Neo API 支援哪些作業系統？
A: 支援 Windows、macOS 和 Linux 三大平台

### Q2: Python、C#、Node.js 功能有差異嗎？
A: 核心功能相同，但各語言 SDK 可能有些微差異，建議參考各自文件

### Q3: 可以同時使用多個帳號嗎？
A: 可以，但需要分別申請並管理各自的憑證

### Q4: API 有測試環境嗎？
A: 請聯繫富邦證券確認是否提供模擬環境

### Q5: 如何處理斷線重連？
A: SDK 通常有內建重連機制，詳見官方文件

## 版本資訊

### Neo API
- 這是富邦證券的新一代 API
- 於近期推出，提供更現代化的開發體驗
- 持續更新維護中

### 傳統 API vs Neo API
- Neo API 提供更好的跨平台支援
- Neo API 提供更多程式語言選擇
- 建議新專案使用 Neo API

## 更新日誌

- 最後更新: 2025-10-31
- 資料來源: 官方網站、開發者文件

## 聯絡資訊

- **客服電話**: 請參考富邦證券官網
- **官方網站**: https://www.fbs.com.tw/
- **API 官網**: https://www.fbs.com.tw/TradeAPI/en/
- **技術支援**: 透過營業員或官方客服

---

## 相關連結

- [富邦證券官網](https://www.fbs.com.tw/)
- [Fubon Neo API 官網](https://www.fbs.com.tw/TradeAPI/en/)
- [Neo API 開發者文件](https://www.fbs.com.tw/TradeAPI/en/docs/trading/introduction/)
- [富邦期貨 gTrade API](https://www.fubon.com/futures/home/instructions/gtrade.html)
- [C# 開發教學 (GitHub)](https://github.com/eermagic/csharp-fubon-future-api-guide)
