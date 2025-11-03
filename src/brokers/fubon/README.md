# 富邦證券 Neo API 實作

這是一個完整的富邦證券 Neo API Python 封裝實作，提供簡單易用的介面進行證券交易、市場行情查詢和帳戶管理。

## 📋 目錄

- [功能特色](#功能特色)
- [系統需求](#系統需求)
- [安裝說明](#安裝說明)
- [快速開始](#快速開始)
- [API 文件](#api-文件)
- [使用範例](#使用範例)
- [注意事項](#注意事項)
- [常見問題](#常見問題)

## ✨ 功能特色

### 🔐 帳戶管理
- ✅ 帳戶登入/登出
- ✅ 查詢帳戶資訊
- ✅ 查詢帳戶餘額
- ✅ 查詢可用購買力
- ✅ 查詢融資融券資訊

### 📊 市場行情
- ✅ 即時報價訂閱
- ✅ 即時報價查詢
- ✅ 歷史行情資料
- ✅ 盤中即時資料
- ✅ 多檔股票監控

### 📈 投資組合
- ✅ 查詢持股部位
- ✅ 查詢單一持股
- ✅ 損益計算
- ✅ 交割資訊查詢
- ✅ 投資組合分析

### 💼 交易下單
- ✅ 限價單/市價單
- ✅ ROD/IOC/FOK 委託類型
- ✅ 現股/融資/融券
- ✅ 委託查詢
- ✅ 修改委託
- ✅ 取消委託

## 🖥️ 系統需求

- Python 3.8 或以上版本
- 富邦證券帳戶
- 富邦證券 API 使用權限
- 數位憑證檔案

## 📦 安裝說明

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

複製環境變數範例檔案:

```bash
cp .env.example .env
```

編輯 `.env` 檔案，填入您的帳號資訊:

```bash
FUBON_USER_ID=your_user_id
FUBON_PASSWORD=your_password
FUBON_CERT_PATH=/path/to/certificate.pfx
```

### 3. 驗證安裝

```python
from fubon import FubonBroker

broker = FubonBroker()
print(broker)
```

## 🚀 快速開始

### 基本使用範例

```python
import os
from fubon import FubonBroker
from fubon.constants import Action, PriceType, OrderType

# 建立 broker 實例
broker = FubonBroker()

# 登入
broker.login(
    user_id=os.getenv('FUBON_USER_ID'),
    password=os.getenv('FUBON_PASSWORD'),
    cert_path=os.getenv('FUBON_CERT_PATH')
)

# 查詢帳戶資訊
account = broker.get_account_info()
print(f"帳戶: {account}")

# 查詢持股
positions = broker.get_positions()
print(f"持股: {len(positions)} 檔")

# 訂閱即時報價
broker.init_realtime()
broker.subscribe_quote("2330")
quote = broker.get_quote("2330")
print(f"台積電報價: {quote}")

# 下單 (請謹慎使用!)
# order = broker.place_order(
#     symbol="2330",
#     action=Action.BUY,
#     quantity=1,
#     price=600.0,
#     price_type=PriceType.LIMIT,
#     order_type=OrderType.ROD
# )

# 登出
broker.logout()
```

### 使用 Context Manager

```python
from fubon import FubonBroker

with FubonBroker() as broker:
    broker.login(user_id, password, cert_path)
    
    # 執行操作
    positions = broker.get_positions()
    
    # 自動登出
```

## 📚 API 文件

### FubonBroker 類別

#### 登入/登出

```python
# 登入
broker.login(user_id: str, password: str, cert_path: str, person_id: Optional[str] = None) -> bool

# 登出
broker.logout() -> bool
```

#### 行情查詢

```python
# 初始化即時行情
broker.init_realtime() -> bool

# 訂閱報價
broker.subscribe_quote(symbol: str, callback: Optional[Callable] = None) -> bool

# 取消訂閱
broker.unsubscribe_quote(symbol: str) -> bool

# 取得報價快照
broker.get_quote(symbol: str) -> Optional[Dict]

# 取得歷史資料
broker.get_historical_data(symbol: str, start_date: str, end_date: str, interval: str = "1d") -> Optional[List[Dict]]

# 取得盤中資料
broker.get_intraday_data(symbol: str, interval: str = "1m") -> Optional[List[Dict]]
```

#### 交易下單

```python
# 下單
broker.place_order(
    symbol: str,
    action: Action,
    quantity: int,
    price: Optional[float] = None,
    price_type: PriceType = PriceType.LIMIT,
    order_type: OrderType = OrderType.ROD,
    order_condition: OrderCondition = OrderCondition.CASH
) -> Optional[Dict]

# 取消委託
broker.cancel_order(order_id: str) -> bool

# 修改委託
broker.modify_order(order_id: str, price: Optional[float] = None, quantity: Optional[int] = None) -> bool

# 查詢委託
broker.get_orders(status: Optional[str] = None, symbol: Optional[str] = None) -> List[Dict]

# 查詢特定委託
broker.get_order(order_id: str) -> Optional[Dict]
```

#### 帳戶管理

```python
# 取得帳戶資訊
broker.get_account_info() -> Dict

# 取得餘額
broker.get_balance() -> Dict

# 取得持股
broker.get_positions() -> List[Dict]

# 取得特定持股
broker.get_position(symbol: str) -> Optional[Dict]

# 取得交割資訊
broker.get_settlements() -> List[Dict]

# 取得損益
broker.get_profit_loss() -> Dict

# 取得融資融券資訊
broker.get_margin_info() -> Dict

# 取得購買力
broker.get_buying_power() -> float
```

### 常數定義

```python
from fubon.constants import Action, PriceType, OrderType, OrderCondition

# 交易動作
Action.BUY      # 買進
Action.SELL     # 賣出

# 價格類型
PriceType.LIMIT         # 限價
PriceType.MARKET        # 市價
PriceType.MARKET_RANGE  # 範圍市價

# 委託類型
OrderType.ROD   # 當日有效
OrderType.IOC   # 立即成交否則取消
OrderType.FOK   # 全部成交否則取消

# 委託條件
OrderCondition.CASH    # 現股
OrderCondition.MARGIN  # 融資
OrderCondition.SHORT   # 融券
```

## 💡 使用範例

專案提供了完整的使用範例，位於 `examples/` 目錄:

### 01_basic_usage.py - 基本操作
- 帳戶登入
- 查詢帳戶資訊
- 查詢持股
- 查詢報價

執行:
```bash
python examples/01_basic_usage.py
```

### 02_market_data.py - 市場行情
- 即時報價訂閱
- 歷史資料查詢
- 盤中資料查詢
- 技術分析範例

執行:
```bash
python examples/02_market_data.py
```

### 03_order_management.py - 下單管理
- 委託查詢
- 下單範例 (已註解)
- 修改委託
- 取消委託

執行:
```bash
python examples/03_order_management.py
```

### 04_account_portfolio.py - 帳戶管理
- 完整帳戶資訊
- 持股分析
- 損益計算
- 投資組合分析

執行:
```bash
python examples/04_account_portfolio.py
```

## ⚠️ 注意事項

### 安全性
- ⚠️ **絕對不要** 將帳號密碼提交到版本控制系統
- ⚠️ 使用 `.env` 檔案管理敏感資訊
- ⚠️ 確保 `.env` 已加入 `.gitignore`
- ⚠️ 妥善保管數位憑證檔案

### 交易風險
- ⚠️ 實際下單前請務必確認參數
- ⚠️ 建議先在測試環境測試
- ⚠️ 使用小額測試確認功能
- ⚠️ 設定停損停利機制
- ⚠️ 注意交易成本和手續費

### API 限制
- ⚠️ 注意 API 呼叫頻率限制
- ⚠️ 遵守證交所交易規則
- ⚠️ 注意市場漲跌幅限制
- ⚠️ 交易時間限制 (09:00-13:30)

### 錯誤處理
- ✅ 程式碼包含完整的錯誤處理
- ✅ 建議使用 try-except 捕捉異常
- ✅ 記錄詳細的操作日誌
- ✅ 監控委託狀態變化

## 🔧 常見問題

### Q1: 如何取得富邦證券 API 權限?
A: 請聯繫您的富邦證券營業員申請 API 服務，並簽署相關文件。

### Q2: 憑證檔案在哪裡?
A: 申請核准後，可從富邦證券官網下載數位憑證檔案 (.pfx)。

### Q3: 支援模擬交易嗎?
A: 請聯繫富邦證券確認是否提供測試環境。

### Q4: 如何處理登入失敗?
A: 確認帳號密碼正確、憑證檔案路徑正確、憑證未過期。

### Q5: 可以同時執行多個實例嗎?
A: 可以，但需注意 API 呼叫頻率限制。

### Q6: 如何取得更多技術支援?
A: 參考官方文件或聯繫富邦證券技術支援。

## 📖 相關資源

- [富邦證券 Neo API 官網](https://www.fbs.com.tw/TradeAPI/en/)
- [開發者文件](https://www.fbs.com.tw/TradeAPI/en/docs/trading/introduction/)
- [富邦證券官網](https://www.fbs.com.tw/)

## 📄 授權

此實作僅供學習和研究使用，實際交易請自行承擔風險。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## ⚖️ 免責聲明

本程式碼僅供參考學習使用，不構成任何投資建議。使用本程式碼進行實際交易所產生的任何損失，作者不承擔任何責任。投資有風險，交易請謹慎。
