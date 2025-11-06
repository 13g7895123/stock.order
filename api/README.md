# 富邦證券 FastAPI 服務

這是一個基於 FastAPI 的富邦證券 RESTful API 服務，提供完整的證券交易功能。

## 功能特色

### 🔐 認證管理
- 登入/登出
- 會話管理
- 狀態檢查

### 📊 市場行情
- 即時報價訂閱/取消訂閱
- 即時報價查詢
- 歷史行情資料查詢
- 盤中即時資料查詢

### 💰 交易下單
- 限價單/市價單/範圍市價
- ROD/IOC/FOK 委託類型
- 現股/融資/融券
- 委託查詢/修改/取消

### 👤 帳戶管理
- 帳戶資訊查詢
- 帳戶餘額查詢
- 可用購買力計算
- 持股部位查詢
- 交割資訊查詢
- 損益資訊查詢
- 融資融券資訊查詢

## 安裝

### 1. 啟動虛擬環境

```bash
cd /home/jarvis/project/idea/stock.order
source venv/bin/activate
```

### 2. 安裝依賴

```bash
cd api
pip install -r requirements.txt
```

### 3. 設定環境變數

```bash
cp .env.example .env
# 編輯 .env 填入您的帳號資訊
```

## 啟動服務

### 開發模式

```bash
python main.py
```

或使用 uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 生產模式

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API 文件

啟動服務後，訪問以下 URL 查看 API 文件：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 端點

### 認證 `/api/v1/auth`

| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/login` | 登入 |
| POST | `/logout` | 登出 |
| GET | `/status` | 檢查登入狀態 |

### 市場行情 `/api/v1/market`

| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/subscribe` | 訂閱即時報價 |
| POST | `/unsubscribe` | 取消訂閱 |
| POST | `/quote` | 查詢即時報價 |
| POST | `/historical` | 查詢歷史行情 |
| POST | `/intraday` | 查詢盤中資料 |

### 交易下單 `/api/v1/order`

| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/place` | 下單 |
| POST | `/cancel` | 取消委託 |
| POST | `/modify` | 修改委託 |
| POST | `/query` | 查詢委託 |
| GET | `/detail/{order_id}` | 查詢單筆委託 |
| GET | `/today` | 查詢當日委託 |

### 帳戶管理 `/api/v1/account`

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/info` | 帳戶資訊 |
| GET | `/balance` | 帳戶餘額 |
| GET | `/buying-power` | 可用購買力 |
| GET | `/positions` | 持股部位 |
| POST | `/position` | 單一持股 |
| GET | `/settlements` | 交割資訊 |
| GET | `/profit-loss` | 損益資訊 |
| GET | `/margin` | 融資融券 |
| GET | `/summary` | 帳戶摘要 |

## 使用範例

### 1. 登入

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_user_id",
    "password": "your_password",
    "cert_path": "/path/to/cert.pfx"
  }'
```

### 2. 查詢即時報價

```bash
curl -X POST "http://localhost:8000/api/v1/market/quote" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "stock_codes": ["2330", "2317"]
  }'
```

### 3. 下單 (限價單)

```bash
curl -X POST "http://localhost:8000/api/v1/order/place" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "stock_code": "2330",
    "action": "Buy",
    "price": 600.0,
    "quantity": 1,
    "price_type": "LMT",
    "order_type": "ROD",
    "order_condition": "Cash"
  }'
```

### 4. 查詢持股

```bash
curl -X GET "http://localhost:8000/api/v1/account/positions" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Python 客戶端範例

```python
import requests

# API 基礎 URL
BASE_URL = "http://localhost:8000/api/v1"

# 1. 登入
response = requests.post(f"{BASE_URL}/auth/login", json={
    "user_id": "your_user_id",
    "password": "your_password",
    "cert_path": "/path/to/cert.pfx"
})
result = response.json()
print("登入結果:", result)

# 2. 查詢報價
response = requests.post(f"{BASE_URL}/market/quote", json={
    "stock_codes": ["2330", "2317"]
})
quotes = response.json()
print("報價:", quotes)

# 3. 查詢帳戶摘要
response = requests.get(f"{BASE_URL}/account/summary")
summary = response.json()
print("帳戶摘要:", summary)

# 4. 登出
response = requests.post(f"{BASE_URL}/auth/logout")
print("登出結果:", response.json())
```

## 目錄結構

```
api/
├── __init__.py           # 套件初始化
├── main.py              # FastAPI 主應用
├── dependencies.py      # 依賴注入
├── schemas.py           # Pydantic 資料模型
├── requirements.txt     # Python 依賴
├── .env.example        # 環境變數範例
├── README.md           # 本文件
└── routers/            # API 路由
    ├── __init__.py
    ├── auth.py         # 認證路由
    ├── market.py       # 市場行情路由
    ├── order.py        # 交易下單路由
    └── account.py      # 帳戶管理路由
```

## 安全性提醒

⚠️ **重要安全事項**:

1. **不要提交敏感資訊**: `.env` 檔案包含敏感資訊，請勿提交到版本控制
2. **HTTPS**: 生產環境務必使用 HTTPS
3. **認證**: 實作適當的認證機制 (目前為簡化版)
4. **CORS**: 生產環境應限制 CORS 來源
5. **Rate Limiting**: 建議加入 API 呼叫頻率限制
6. **日誌**: 不要記錄敏感資訊

## 開發建議

### 測試

```bash
# 安裝測試依賴
pip install pytest pytest-asyncio httpx

# 執行測試
pytest
```

### 程式碼檢查

```bash
# 安裝檢查工具
pip install black flake8 mypy

# 格式化程式碼
black .

# 檢查風格
flake8 .

# 類型檢查
mypy .
```

## 常見問題

### Q: 無法連線到 API？
A: 確認防火牆設定，確保 8000 port 可以訪問。

### Q: 登入失敗？
A: 檢查帳號密碼是否正確，憑證路徑是否正確。

### Q: 下單失敗？
A: 確認帳戶有足夠額度，檢查市場是否開盤。

### Q: 如何支援多用戶？
A: 使用 `session_id` 參數區分不同用戶的 broker 實例。

## 授權

MIT License

## 聯絡方式

如有問題或建議，請提出 Issue。

---

**最後更新**: 2025-11-05
**版本**: 1.0.0
