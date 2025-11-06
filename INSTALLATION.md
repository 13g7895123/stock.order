# 富邦證券 API 安裝與啟動指南

## 🚀 快速開始

### 1. 安裝必要工具

```bash
# 安裝 Python venv 和 pip
sudo apt update
sudo apt install python3.12-venv python3-pip

# 確認安裝
python3 --version
pip3 --version
```

### 2. 建立虛擬環境

```bash
# 在專案根目錄
cd /home/jarvis/project/idea/stock.order

# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 確認虛擬環境已啟動（提示符會變成 (venv) ...）
which python  # 應該顯示專案內的 venv/bin/python
```

### 3. 安裝依賴

```bash
# 確保在虛擬環境中
source venv/bin/activate

# 安裝 API 依賴
cd api
pip install -r requirements.txt

# 返回專案根目錄
cd ..
```

### 4. 設定環境變數

```bash
# 複製環境變數範例
cp api/.env.example api/.env

# 編輯環境變數（填入您的帳號資訊）
nano api/.env
```

需要設定的項目：
- `FUBON_USER_ID`: 您的富邦證券帳號
- `FUBON_PASSWORD`: 密碼
- `FUBON_CERT_PATH`: 憑證檔案路徑
- `FUBON_PERSON_ID`: 身分證字號

### 5. 啟動服務

#### 方法一：使用啟動腳本（推薦）

```bash
./start_api.sh
```

#### 方法二：手動啟動

```bash
# 啟動虛擬環境
source venv/bin/activate

# 啟動 FastAPI
cd api
python main.py
```

#### 方法三：使用 uvicorn

```bash
source venv/bin/activate
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 訪問 API

服務啟動後，可以訪問：

- **API 文件（Swagger）**: http://localhost:8000/docs
- **API 文件（ReDoc）**: http://localhost:8000/redoc
- **健康檢查**: http://localhost:8000/health

## 📋 完整 API 功能列表

### 認證管理 (`/api/v1/auth`)

- ✅ `POST /login` - 登入
- ✅ `POST /logout` - 登出
- ✅ `GET /status` - 檢查登入狀態

### 市場行情 (`/api/v1/market`)

- ✅ `POST /subscribe` - 訂閱即時報價
- ✅ `POST /unsubscribe` - 取消訂閱即時報價
- ✅ `POST /quote` - 查詢即時報價
- ✅ `POST /historical` - 查詢歷史行情資料
- ✅ `POST /intraday` - 查詢盤中即時資料
- ✅ `POST /quote/callback` - 設定報價回調

### 交易下單 (`/api/v1/order`)

- ✅ `POST /place` - 下單（限價/市價/範圍市價）
- ✅ `POST /cancel` - 取消委託
- ✅ `POST /modify` - 修改委託
- ✅ `POST /query` - 查詢委託列表
- ✅ `GET /detail/{order_id}` - 查詢單筆委託
- ✅ `GET /today` - 查詢當日委託

### 帳戶管理 (`/api/v1/account`)

- ✅ `GET /info` - 取得帳戶資訊
- ✅ `GET /balance` - 取得帳戶餘額
- ✅ `GET /buying-power` - 取得可用購買力
- ✅ `GET /positions` - 取得持股部位
- ✅ `POST /position` - 取得單一持股
- ✅ `GET /settlements` - 取得交割資訊
- ✅ `GET /profit-loss` - 取得損益資訊
- ✅ `GET /margin` - 取得融資融券資訊
- ✅ `GET /summary` - 取得帳戶摘要

## 🔧 使用範例

### 使用 curl 測試

```bash
# 1. 登入
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_user_id",
    "password": "your_password",
    "cert_path": "/path/to/cert.pfx"
  }'

# 2. 檢查狀態
curl "http://localhost:8000/api/v1/auth/status"

# 3. 查詢即時報價
curl -X POST "http://localhost:8000/api/v1/market/quote" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_codes": ["2330", "2317"]
  }'

# 4. 查詢持股
curl "http://localhost:8000/api/v1/account/positions"

# 5. 查詢帳戶摘要
curl "http://localhost:8000/api/v1/account/summary"

# 6. 登出
curl -X POST "http://localhost:8000/api/v1/auth/logout"
```

### 使用 Python 客戶端

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 登入
response = requests.post(f"{BASE_URL}/auth/login", json={
    "user_id": "your_user_id",
    "password": "your_password",
    "cert_path": "/path/to/cert.pfx"
})
print("登入:", response.json())

# 查詢報價
response = requests.post(f"{BASE_URL}/market/quote", json={
    "stock_codes": ["2330", "2317", "2454"]
})
print("報價:", response.json())

# 查詢歷史資料
response = requests.post(f"{BASE_URL}/market/historical", json={
    "stock_code": "2330",
    "interval": "D",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
})
print("歷史資料:", response.json())

# 查詢持股
response = requests.get(f"{BASE_URL}/account/positions")
print("持股:", response.json())

# 查詢帳戶摘要
response = requests.get(f"{BASE_URL}/account/summary")
print("帳戶摘要:", response.json())

# 下單（請謹慎使用）
response = requests.post(f"{BASE_URL}/order/place", json={
    "stock_code": "2330",
    "action": "Buy",
    "price": 600.0,
    "quantity": 1,
    "price_type": "LMT",
    "order_type": "ROD",
    "order_condition": "Cash"
})
print("下單結果:", response.json())

# 查詢委託
response = requests.get(f"{BASE_URL}/order/today")
print("當日委託:", response.json())

# 登出
response = requests.post(f"{BASE_URL}/auth/logout")
print("登出:", response.json())
```

## 🗂️ 專案結構

```
stock.order/
├── api/                      # FastAPI 應用
│   ├── __init__.py
│   ├── main.py              # 主應用程式
│   ├── dependencies.py      # 依賴注入
│   ├── schemas.py           # Pydantic 模型
│   ├── requirements.txt     # Python 依賴
│   ├── .env.example        # 環境變數範例
│   ├── README.md           # API 文件
│   └── routers/            # API 路由
│       ├── __init__.py
│       ├── auth.py         # 認證路由
│       ├── market.py       # 市場行情路由
│       ├── order.py        # 交易下單路由
│       └── account.py      # 帳戶管理路由
├── src/                     # 源代碼
│   └── brokers/
│       └── fubon/          # 富邦證券實作
│           ├── broker.py
│           ├── constants.py
│           └── ...
├── venv/                    # 虛擬環境
├── start_api.sh            # 啟動腳本
└── INSTALLATION.md         # 本文件
```

## ⚠️ 常見問題

### Q1: venv 建立失敗？

```bash
# 安裝 venv
sudo apt install python3.12-venv

# 重新建立
python3 -m venv venv
```

### Q2: pip 找不到？

```bash
# 安裝 pip
sudo apt install python3-pip
```

### Q3: 無法啟動 API？

```bash
# 確認已安裝 FastAPI
pip list | grep fastapi

# 重新安裝
pip install -r api/requirements.txt
```

### Q4: 端口 8000 已被占用？

```bash
# 查看占用端口的程序
sudo lsof -i :8000

# 修改端口（編輯 api/main.py）
# 或使用 uvicorn 指定端口
uvicorn main:app --port 8001
```

### Q5: 登入失敗？

確認：
1. 憑證路徑是否正確
2. 帳號密碼是否正確
3. 富邦證券 API 服務是否正常
4. 網路連線是否正常

## 📊 功能覆蓋率

✅ **市場行情**: 100% (6/6 功能)
✅ **交易下單**: 100% (6/6 功能)  
✅ **帳戶管理**: 100% (9/9 功能)
✅ **認證管理**: 100% (3/3 功能)

**總計**: 24 個 API 端點，涵蓋富邦證券所有核心功能

## 🔒 安全提醒

1. **不要提交 .env 檔案**到版本控制
2. **生產環境使用 HTTPS**
3. **實作適當的認證機制**
4. **限制 CORS 來源**
5. **加入 Rate Limiting**
6. **定期更新依賴套件**

## 📚 相關文件

- [富邦證券實作文件](../src/brokers/fubon/README.md)
- [API 使用文件](api/README.md)
- [主專案說明](../README.md)

---

**最後更新**: 2025-11-05  
**版本**: 1.0.0
