# 富邦證券 Neo API - 完整實作

## 🎯 專案概述

這是一個完整的富邦證券 Neo API Python 封裝實作，提供簡單易用的介面進行：
- 📊 市場行情查詢（即時報價、歷史資料）
- 💼 證券交易下單（限價、市價、多種委託類型）
- 💰 帳戶管理（餘額、持股、損益）
- 📈 投資組合分析

## 📦 快速開始

### 安裝

```bash
cd src/brokers/fubon
pip install -r requirements.txt
```

### 設定環境變數

```bash
cp .env.example .env
# 編輯 .env，填入您的富邦證券帳號資訊
```

### 基本使用

```python
from fubon import FubonBroker
from fubon.constants import Action, PriceType, OrderType

# 使用 Context Manager 自動處理登入登出
with FubonBroker() as broker:
    # 登入
    broker.login(user_id, password, cert_path)
    
    # 查詢帳戶
    account = broker.get_account_info()
    
    # 查詢持股
    positions = broker.get_positions()
    
    # 訂閱即時報價
    broker.init_realtime()
    broker.subscribe_quote("2330")
    quote = broker.get_quote("2330")
    
    # 下單 (請謹慎使用!)
    # order = broker.place_order(
    #     symbol="2330",
    #     action=Action.BUY,
    #     quantity=1,
    #     price=600.0,
    #     price_type=PriceType.LIMIT,
    #     order_type=OrderType.ROD
    # )
```

## 📚 文件連結

- **[完整使用說明](README.md)** - 詳細的 API 文件、使用範例、注意事項
- **[實作清單](IMPLEMENTATION.md)** - 完整的功能清單和檔案結構
- **[實作報告](../../docs/fubon_implementation_report.md)** - 詳細的完成報告

## 💡 使用範例

提供 4 個完整的實戰範例：

| 範例 | 檔案 | 說明 |
|------|------|------|
| 基本操作 | [01_basic_usage.py](examples/01_basic_usage.py) | 登入、查詢帳戶、持股、報價 |
| 市場行情 | [02_market_data.py](examples/02_market_data.py) | 即時報價、歷史資料、技術分析 |
| 下單管理 | [03_order_management.py](examples/03_order_management.py) | 下單、修改、取消委託 |
| 帳戶管理 | [04_account_portfolio.py](examples/04_account_portfolio.py) | 完整的帳戶與投資組合分析 |

執行範例：
```bash
python examples/01_basic_usage.py
python examples/02_market_data.py
python examples/03_order_management.py
python examples/04_account_portfolio.py
```

## 🧪 測試

執行單元測試：
```bash
python -m pytest tests/ -v
```

或個別測試：
```bash
python tests/test_broker.py
python tests/test_constants.py
```

## ✨ 主要特色

### 完整的功能實作

#### 🔐 帳戶管理
```python
broker.get_account_info()      # 帳戶資訊
broker.get_balance()            # 帳戶餘額
broker.get_buying_power()       # 可用購買力
broker.get_margin_info()        # 融資融券資訊
```

#### 📊 市場行情
```python
broker.init_realtime()                                    # 初始化即時行情
broker.subscribe_quote("2330")                           # 訂閱報價
broker.get_quote("2330")                                 # 取得報價
broker.get_historical_data("2330", "2024-01-01", "2024-12-31")  # 歷史資料
broker.get_intraday_data("2330", interval="1m")         # 盤中資料
```

#### 💼 交易下單
```python
broker.place_order(                    # 下單
    symbol="2330",
    action=Action.BUY,
    quantity=1,
    price=600.0,
    price_type=PriceType.LIMIT,
    order_type=OrderType.ROD
)

broker.cancel_order(order_id)          # 取消委託
broker.modify_order(order_id, price=605)  # 修改委託
broker.get_orders()                     # 查詢委託
```

#### 📈 投資組合
```python
broker.get_positions()          # 所有持股
broker.get_position("2330")     # 特定持股
broker.get_profit_loss()        # 損益資訊
broker.get_settlements()        # 交割資訊
```

### 完整的常數定義

```python
from fubon.constants import (
    Action,              # BUY, SELL
    PriceType,          # LIMIT, MARKET, MARKET_RANGE
    OrderType,          # ROD, IOC, FOK
    OrderCondition,     # CASH, MARGIN, SHORT
    MarketType,         # STOCK, FUTURES, OPTIONS
    OrderStatus         # PENDING, FILLED, CANCELLED, etc.
)
```

## 📊 實作統計

| 項目 | 數量 |
|------|------|
| 總程式碼行數 | **1,781 行** |
| 核心類別方法 | **30+ 個** |
| 使用範例 | **4 個完整腳本** |
| 單元測試 | **20+ 個測試案例** |
| 文件頁面 | **3 份詳細文件** |
| 常數定義 | **6 組 Enum** |

## 📂 專案結構

```
src/brokers/fubon/
├── __init__.py                      # 套件初始化與匯出
├── broker.py                        # FubonBroker 主類別 (600+ 行)
├── constants.py                     # 常數定義 (Action, PriceType 等)
├── requirements.txt                 # 相依套件清單
├── .env.example                    # 環境變數範例
├── README.md                       # 完整使用說明 (400+ 行)
├── IMPLEMENTATION.md               # 實作清單
├── QUICKSTART.md                   # 快速開始指南 (本檔案)
├── examples/                       # 使用範例
│   ├── 01_basic_usage.py          # 基本操作 (150 行)
│   ├── 02_market_data.py          # 市場行情 (180 行)
│   ├── 03_order_management.py     # 下單管理 (200 行)
│   └── 04_account_portfolio.py    # 帳戶管理 (250 行)
└── tests/                          # 單元測試
    ├── __init__.py
    ├── test_broker.py             # Broker 類別測試 (300+ 行)
    └── test_constants.py          # 常數定義測試 (50 行)
```

## ⚠️ 重要提醒

### 安全性
- ⚠️ 使用 `.env` 檔案管理帳號密碼
- ⚠️ 絕不將 `.env` 提交到版本控制
- ⚠️ 妥善保管數位憑證檔案

### 交易風險
- ⚠️ 實際下單前務必測試
- ⚠️ 使用小額測試確認功能
- ⚠️ 設定停損停利機制
- ⚠️ 注意交易成本

### API 使用
- ⚠️ 注意 API 呼叫頻率限制
- ⚠️ 遵守證交所交易規則
- ⚠️ 交易時間 09:00-13:30

## 🔧 系統需求

- Python 3.8+
- 富邦證券帳戶
- 富邦證券 API 權限
- 數位憑證檔案

## 📖 相關資源

- [富邦證券 Neo API 官網](https://www.fbs.com.tw/TradeAPI/en/)
- [開發者文件](https://www.fbs.com.tw/TradeAPI/en/docs/trading/introduction/)
- [富邦證券官網](https://www.fbs.com.tw/)

## 💬 常見問題

### Q: 如何取得 API 權限？
A: 請聯繫您的富邦證券營業員申請 API 服務。

### Q: 憑證檔案在哪裡？
A: 申請核准後可從富邦證券官網下載。

### Q: 支援模擬交易嗎？
A: 請聯繫富邦證券確認是否提供測試環境。

### Q: 登入失敗怎麼辦？
A: 確認帳號密碼正確、憑證路徑正確、憑證未過期。

## 📄 授權與免責聲明

本程式碼僅供學習和研究使用，不構成任何投資建議。使用本程式碼進行實際交易所產生的任何損失，作者不承擔任何責任。投資有風險，交易請謹慎。

---

**準備開始了嗎？** 參考 [README.md](README.md) 獲取完整的 API 文件！
