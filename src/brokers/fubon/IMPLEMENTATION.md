# 富邦證券 API 實作檔案清單

## 專案結構

```
src/brokers/fubon/
├── __init__.py                 # 套件初始化
├── broker.py                   # 主要 Broker 類別實作
├── constants.py                # 常數定義
├── requirements.txt            # 相依套件
├── .env.example               # 環境變數範例
├── README.md                  # 完整說明文件
├── examples/                  # 使用範例
│   ├── 01_basic_usage.py     # 基本操作範例
│   ├── 02_market_data.py     # 市場行情範例
│   ├── 03_order_management.py # 下單管理範例
│   └── 04_account_portfolio.py # 帳戶管理範例
└── tests/                     # 單元測試
    ├── __init__.py
    ├── test_broker.py        # Broker 類別測試
    └── test_constants.py     # 常數定義測試
```

## 已實作功能清單

### ✅ 核心類別 (broker.py)

#### 登入/登出
- [x] `login()` - 登入富邦證券帳戶
- [x] `logout()` - 登出
- [x] Context Manager 支援 (`__enter__`, `__exit__`)

#### 市場行情
- [x] `init_realtime()` - 初始化即時行情
- [x] `subscribe_quote()` - 訂閱即時報價
- [x] `unsubscribe_quote()` - 取消訂閱報價
- [x] `get_quote()` - 取得報價快照
- [x] `get_historical_data()` - 取得歷史行情
- [x] `get_intraday_data()` - 取得盤中資料

#### 交易下單
- [x] `place_order()` - 下單
- [x] `cancel_order()` - 取消委託
- [x] `modify_order()` - 修改委託
- [x] `get_orders()` - 查詢委託列表
- [x] `get_order()` - 查詢特定委託

#### 帳戶管理
- [x] `get_account_info()` - 取得帳戶資訊
- [x] `get_balance()` - 取得帳戶餘額
- [x] `get_positions()` - 取得持股部位
- [x] `get_position()` - 取得特定持股
- [x] `get_settlements()` - 取得交割資訊
- [x] `get_profit_loss()` - 取得損益資訊
- [x] `get_margin_info()` - 取得融資融券資訊
- [x] `get_buying_power()` - 取得購買力
- [x] `set_order_callback()` - 設定委託狀態回調

### ✅ 常數定義 (constants.py)

- [x] `Action` - 交易動作 (Buy, Sell)
- [x] `PriceType` - 價格類型 (Limit, Market, MarketRange)
- [x] `OrderType` - 委託類型 (ROD, IOC, FOK)
- [x] `OrderCondition` - 委託條件 (Cash, Margin, Short)
- [x] `MarketType` - 市場類型 (Stock, Futures, Options)
- [x] `OrderStatus` - 委託狀態

### ✅ 使用範例 (examples/)

1. **01_basic_usage.py** - 基本操作
   - 登入/登出
   - 查詢帳戶資訊、餘額、購買力
   - 查詢持股
   - 查詢報價
   - 查詢委託

2. **02_market_data.py** - 市場行情
   - 訂閱多檔即時報價
   - 查詢歷史資料
   - 查詢盤中資料
   - 簡單技術分析範例

3. **03_order_management.py** - 下單管理
   - 查詢當日委託
   - 限價單/市價單範例 (已註解)
   - IOC 委託範例
   - 修改委託
   - 取消委託
   - 依狀態/股票查詢委託
   - 檢查購買力

4. **04_account_portfolio.py** - 帳戶管理
   - 完整帳戶資訊
   - 帳戶餘額詳情
   - 持股部位分析
   - 投資組合摘要
   - 損益計算
   - 交割資訊
   - 融資融券資訊
   - 投資組合分析 (前3大持股、最賺/賠)

### ✅ 測試 (tests/)

- [x] `test_broker.py` - Broker 類別完整測試
  - 初始化測試
  - 登入/登出測試
  - Context Manager 測試
  - 市場行情功能測試
  - 下單功能測試
  - 帳戶管理功能測試

- [x] `test_constants.py` - 常數定義測試
  - 所有 Enum 值驗證

### ✅ 文件

- [x] `README.md` - 完整說明文件
  - 功能特色
  - 系統需求
  - 安裝說明
  - 快速開始
  - API 文件
  - 使用範例
  - 注意事項
  - 常見問題
  - 相關資源

- [x] `requirements.txt` - 相依套件清單
- [x] `.env.example` - 環境變數範例

## 功能覆蓋率

根據富邦證券 Neo API 官方文件，本實作涵蓋了以下核心功能:

### ✅ 即時市場行情 (Live Market Data)
- 即時報價訂閱
- 報價查詢
- 多檔監控

### ✅ 歷史行情資料 (Archived Market Data)
- 日線資料
- 分鐘線資料
- 自訂時間區間

### ✅ 無縫下單執行 (Seamless Order Execution)
- 限價單
- 市價單
- 範圍市價
- 多種委託類型 (ROD/IOC/FOK)
- 現股/融資/融券
- 委託管理 (查詢/修改/取消)

### ✅ 帳戶監控 (Account Oversight)
- 帳戶資訊
- 餘額查詢
- 購買力計算
- 融資融券

### ✅ 投資組合監控 (Portfolio Oversight)
- 持股查詢
- 損益計算
- 交割資訊
- 投資組合分析

## 使用建議

1. **開發階段**: 使用範例程式了解各項功能
2. **測試階段**: 執行單元測試確保功能正常
3. **生產環境**: 
   - 妥善保管帳號密碼
   - 使用環境變數管理敏感資訊
   - 加入完整的錯誤處理
   - 記錄詳細日誌
   - 設定風險控管機制

## 注意事項

⚠️ **重要**: 本實作為富邦證券 Neo API 的 Python 封裝，實際功能和行為依賴於官方 `fubon-neo` 套件。某些功能的實際可用性可能因 API 版本或權限而異。

⚠️ **交易風險**: 實際交易前請務必在測試環境充分測試，並了解所有交易風險。

⚠️ **API 限制**: 請遵守富邦證券的 API 使用規範，注意呼叫頻率限制。
