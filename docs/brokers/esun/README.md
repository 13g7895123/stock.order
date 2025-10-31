# 玉山證券 (E.SUN Securities) API 文件

## 券商資訊

- **券商名稱**: 玉山綜合證券股份有限公司
- **英文名稱**: E.SUN Securities Co., Ltd.
- **英文縮寫**: E.SUN / ESUN
- **API 名稱**: 玉山證券富果帳戶交易 API (Fugle Trading API)

## API 官方資源

- **API 官網**: https://fugletradingapi.esunsec.com.tw/
- **開發者文件**: https://developer.fugle.tw/
- **交易 API 文件**: https://developer.fugle.tw/docs/trading/intro/
- **事前準備**: https://developer.fugle.tw/docs/trading/prerequisites/

## 主要特色

### 1. 四大服務優勢

玉山證券富果帳戶交易 API 展現以下特色：

1. **無平台開發限制**
   - 支援 Windows、Mac、Linux
   - 跨平台完整支援

2. **模擬多種交易測試環境**
   - 提供完整的模擬交易環境
   - 可在模擬環境測試下單操作
   - 練習查詢帳戶資訊、搜尋股票

3. **多語言 SDK**
   - Python
   - JavaScript (Node.js)
   - 其他語言陸續支援

4. **說明文件易讀**
   - 詳細的開發者文件
   - 清楚的範例程式碼
   - 完整的 API Reference

### 2. 支援的市場
- 台灣股票市場

### 3. 核心功能
- 台股即時報價
- 台股下單交易
- 帳戶資訊查詢
- 委託查詢
- 成交查詢
- 庫存查詢
- 搜尋股票

### 4. 技術優勢
- 由 Fugle 技術團隊與玉山證券合作開發
- 現代化的 API 設計
- RESTful API 架構
- 完整的開發者支援

## 技術規格

### 支援平台
- Windows
- macOS
- Linux

### 支援語言
- Python (官方 SDK)
- JavaScript/Node.js (官方 SDK)

### 安裝方式

#### Python SDK
```bash
pip install fugle-trade
```

#### Node.js SDK
```bash
npm install @fugle/trade
```

### Python 使用範例

```python
from fugle_trade.sdk import SDK
from fugle_trade.constant import APCode, Trade, PriceFlag, BSFlag, Action

# 初始化 SDK
sdk = SDK(config_path='config.ini')

# 登入
sdk.login()

# 取得帳戶資訊
accounts = sdk.get_accounts()

# 下單
order = sdk.place_order(
    stock_no='2330',          # 股票代號
    buy_sell=BSFlag.Buy,      # 買賣別
    price='600',              # 價格
    quantity=1,               # 數量
    ap_code=APCode.Common,    # 盤別
    price_flag=PriceFlag.Limit,  # 價格旗標
    trade=Trade.Cash          # 交易類別
)

# 查詢委託
orders = sdk.get_orders()

# 查詢庫存
inventories = sdk.get_inventories()
```

### Node.js 使用範例

```javascript
const { FugleTrade } = require('@fugle/trade');

// 初始化
const fugle = new FugleTrade({
  configPath: 'config.ini'
});

// 登入
await fugle.login();

// 取得帳戶資訊
const accounts = await fugle.getAccounts();

// 下單
const order = await fugle.placeOrder({
  stockNo: '2330',
  buySell: 'B',
  price: '600',
  quantity: 1,
  apCode: '1',
  priceFlag: '0',
  trade: '0'
});

// 查詢委託
const orders = await fugle.getOrders();
```

## 下單參數說明

### BSFlag (買賣別)
- `Buy` (B): 買進
- `Sell` (S): 賣出

### APCode (盤別)
- `Common`: 普通盤
- `AfterMarket`: 盤後交易
- `OddLot`: 零股交易

### PriceFlag (價格類型)
- `Limit`: 限價
- `Market`: 市價
- `MarketOnClose`: 收盤市價

### Trade (交易類別)
- `Cash`: 現股
- `Margin`: 融資
- `Short`: 融券
- `DayTrading`: 當沖

## 申請流程

### 1. 開立玉山證券富果帳戶

玉山證券富果帳戶是專門為程式交易設計的帳戶：

- **線上開戶**: 透過玉山證券官網或富果平台
- **開戶條件**: 年滿 20 歲，具中華民國身分
- **所需文件**: 身分證、第二證件、銀行帳戶

### 2. 申請 API 權限

- 登入富果交易 API 官網
- 提出 API 使用申請
- 簽署相關同意書

### 3. 取得 API 憑證

- 申請核准後取得憑證檔案
- 下載並妥善保管憑證
- 憑證用於 API 認證

### 4. 設定開發環境

- 安裝 Python 或 Node.js
- 安裝對應的 SDK
- 設定 config.ini 設定檔

### 5. 開始開發

- 參考官方文件
- 先在模擬環境測試
- 確認無誤後正式交易

## 模擬交易環境

### 特色
- 完整的模擬交易功能
- 可在模擬環境練習
  - 下單操作
  - 查詢帳戶資訊
  - 搜尋股票
  - 測試交易策略

### 使用方式
- 在設定檔中切換為模擬模式
- 使用與正式環境相同的 API
- 不會有實際金流

## 使用限制與注意事項

### 1. 帳戶要求
- 需開立玉山證券富果帳戶
- 與一般玉山證券帳戶可能有差異
- 建議確認帳戶類型

### 2. 技術要求
- 需具備程式開發能力
- 熟悉 Python 或 JavaScript
- 了解台股交易規則

### 3. 安全性
- 妥善保管憑證檔案
- 不可分享 API 金鑰
- 建議使用環境變數存放敏感資訊

### 4. 交易限制
- 遵守台股交易規則
- 注意漲跌幅限制
- 遵守當沖規定

### 5. API 限制
- 可能有呼叫頻率限制
- 注意模擬與正式環境差異

### 6. 費用
- API 使用免費
- 交易手續費依照約定費率

## 教學資源

### 官方資源

1. **開發者文件**: https://developer.fugle.tw/
   - 完整的 API 文件
   - 詳細的參數說明
   - 範例程式碼

2. **事前準備指南**: https://developer.fugle.tw/docs/trading/prerequisites/
   - 帳戶申請流程
   - 憑證下載說明
   - SDK 安裝教學

3. **快速開始**: https://developer.fugle.tw/docs/trading/quickstart/
   - 5 分鐘快速上手
   - 基本操作範例

### 社群資源

#### 部落格文章
- **ARON HACK**: [申請玉山證券富果帳戶及台股API常見問題](https://aronhack.com/zh/apply-esun-fugle-account-and-taiwan-stock-api/)
  - 詳細的申請流程
  - 常見問題解答

### 社群討論
- 量化交易社群
- Facebook 相關社團

## 與 Fugle 的關係

### Fugle 是什麼？
- Fugle (富果) 是台灣的金融科技公司
- 專注於開發者友善的金融 API

### 合作關係
- 玉山證券與 Fugle 技術團隊合作
- 共同開發「玉山證券富果帳戶交易 API」
- 由 Fugle 提供技術支援和開發者平台

### Fugle 的其他服務
- 富果股市 API: https://developer.fugle.tw/
  - 市場行情 API
  - 即時報價
  - 歷史資料

## 常見問題 FAQ

### Q1: 玉山證券富果帳戶和一般玉山證券帳戶有什麼不同？
A: 富果帳戶是專為程式交易設計的帳戶，提供 API 服務

### Q2: 支援哪些作業系統？
A: 支援 Windows、macOS、Linux 全平台

### Q3: 有模擬交易環境嗎？
A: 有，提供完整的模擬交易環境供測試

### Q4: 支援哪些程式語言？
A: 官方提供 Python 和 JavaScript SDK

### Q5: 文件容易閱讀嗎？
A: 是的，這是玉山證券富果 API 的四大優勢之一

### Q6: 如何申請？
A: 需先開立玉山證券富果帳戶，再申請 API 權限

## 優勢總結

### 開發者友善
- 現代化的 API 設計
- 清楚的文件
- 完整的範例

### 跨平台支援
- 不限於 Windows
- Mac 和 Linux 原生支援

### 測試環境完整
- 提供模擬交易環境
- 降低開發風險

### 多語言支援
- Python 和 JavaScript 官方 SDK
- 適合不同背景的開發者

## 更新日誌

- 最後更新: 2025-10-31
- 資料來源: 官方網站、開發者文件

## 聯絡資訊

- **玉山證券官網**: https://www.esunsec.com.tw/
- **API 官網**: https://fugletradingapi.esunsec.com.tw/
- **開發者平台**: https://developer.fugle.tw/
- **技術支援**: 透過開發者平台或客服

---

## 相關連結

- [玉山證券官網](https://www.esunsec.com.tw/)
- [玉山證券富果 API](https://fugletradingapi.esunsec.com.tw/)
- [Fugle 開發者平台](https://developer.fugle.tw/)
- [交易 API 文件](https://developer.fugle.tw/docs/trading/intro/)
- [事前準備指南](https://developer.fugle.tw/docs/trading/prerequisites/)
- [申請教學 (ARON HACK)](https://aronhack.com/zh/apply-esun-fugle-account-and-taiwan-stock-api/)
