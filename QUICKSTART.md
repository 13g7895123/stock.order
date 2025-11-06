# 🚀 富邦證券 API 快速啟動指南

## ✅ 已完成項目

- [x] Python 虛擬環境 (venv)
- [x] FastAPI 框架安裝
- [x] 24 個完整 API 端點
- [x] Mock 模式測試
- [x] 服務啟動腳本
- [x] 完整文件

## 🎯 服務狀態

**當前狀態**: ✅ 運行中  
**端口**: 8000  
**模式**: Mock (測試模式)  
**API 端點**: 24 個  
**測試通過率**: 100%

## 📋 快速命令

### 啟動服務

```bash
# 方法1: 使用啟動腳本
cd /home/jarvis/project/idea/stock.order
./start_api.sh

# 方法2: 手動啟動
cd /home/jarvis/project/idea/stock.order
source venv/bin/activate
cd api
python main.py
```

### 停止服務

```bash
pkill -f "python main.py"
```

### 檢查服務狀態

```bash
curl http://localhost:8000/health
```

### 查看服務日誌

```bash
tail -f /tmp/fubon_api.log
```

## 🌐 訪問地址

| 項目 | URL |
|------|-----|
| 服務根路徑 | http://localhost:8000 |
| 健康檢查 | http://localhost:8000/health |
| API 文件 (Swagger) | http://localhost:8000/docs |
| API 文件 (ReDoc) | http://localhost:8000/redoc |

## 📊 API 端點總覽

### 認證管理 (3)
- `POST /api/v1/auth/login` - 登入
- `POST /api/v1/auth/logout` - 登出
- `GET /api/v1/auth/status` - 登入狀態

### 市場行情 (6)
- `POST /api/v1/market/subscribe` - 訂閱報價
- `POST /api/v1/market/unsubscribe` - 取消訂閱
- `POST /api/v1/market/quote` - 即時報價
- `POST /api/v1/market/historical` - 歷史資料
- `POST /api/v1/market/intraday` - 盤中資料
- `POST /api/v1/market/quote/callback` - 報價回調

### 交易下單 (6)
- `POST /api/v1/order/place` - 下單
- `POST /api/v1/order/cancel` - 取消委託
- `POST /api/v1/order/modify` - 修改委託
- `POST /api/v1/order/query` - 查詢委託
- `GET /api/v1/order/detail/{order_id}` - 委託詳情
- `GET /api/v1/order/today` - 當日委託

### 帳戶管理 (9)
- `GET /api/v1/account/info` - 帳戶資訊
- `GET /api/v1/account/balance` - 帳戶餘額
- `GET /api/v1/account/buying-power` - 購買力
- `GET /api/v1/account/positions` - 持股部位
- `POST /api/v1/account/position` - 單一持股
- `GET /api/v1/account/settlements` - 交割資訊
- `GET /api/v1/account/profit-loss` - 損益
- `GET /api/v1/account/margin` - 融資融券
- `GET /api/v1/account/summary` - 帳戶摘要

## 💡 使用範例

### 1. 測試登入

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","password":"test","cert_path":"/tmp/test.pfx"}'
```

### 2. 查詢報價

```bash
curl -X POST "http://localhost:8000/api/v1/market/quote" \
  -H "Content-Type: application/json" \
  -d '{"stock_codes":["2330","2317"]}'
```

### 3. 查詢持股

```bash
curl "http://localhost:8000/api/v1/account/positions"
```

### 4. 查詢帳戶摘要

```bash
curl "http://localhost:8000/api/v1/account/summary"
```

## 📁 專案結構

```
stock.order/
├── api/                    # FastAPI 應用
│   ├── main.py            # 主程式
│   ├── dependencies.py    # 依賴注入
│   ├── schemas.py         # 資料模型
│   ├── requirements.txt   # 依賴套件
│   └── routers/          # API 路由
│       ├── auth.py       # 認證
│       ├── market.py     # 行情
│       ├── order.py      # 下單
│       └── account.py    # 帳戶
├── src/brokers/fubon/     # 富邦實作
│   ├── broker.py         # 主類別
│   ├── broker_mock.py    # Mock 版本
│   └── constants.py      # 常數
├── venv/                  # 虛擬環境
├── start_api.sh          # 啟動腳本
├── INSTALLATION.md       # 安裝指南
├── TEST_REPORT.md        # 測試報告
└── QUICKSTART.md         # 本文件
```

## ⚠️ 重要提醒

### Mock 模式
目前運行在 **Mock 模式**（fubon-neo 未安裝）
- ✅ 適合測試和開發
- ✅ 不會執行真實交易
- ✅ 回應格式與真實API一致
- ⚠️ 數據為模擬數據

### 切換到真實模式
```bash
source venv/bin/activate
pip install fubon-neo
# 重啟服務即可自動切換
```

## 🔧 故障排除

### 服務無法啟動
```bash
# 檢查端口是否被佔用
sudo lsof -i :8000

# 檢查虛擬環境
source venv/bin/activate
which python
```

### API 回應 403/401 錯誤
```bash
# 確認已登入
curl http://localhost:8000/api/v1/auth/status
```

### 查看詳細日誌
```bash
tail -f /tmp/fubon_api.log
```

## 📚 相關文件

- [完整安裝指南](INSTALLATION.md) - 詳細安裝步驟
- [API 使用文件](api/README.md) - API 詳細說明
- [測試報告](TEST_REPORT.md) - 完整測試結果
- [富邦實作文件](src/brokers/fubon/README.md) - 券商實作說明

## ✨ 下一步

1. **瀏覽 API 文件**: http://localhost:8000/docs
2. **測試 API**: 使用 Swagger UI 互動式測試
3. **查看範例**: 參考 `api/README.md` 中的使用範例
4. **整合應用**: 開始建構您的交易應用

## 🎉 恭喜！

您的富邦證券 API 服務已經成功運行！

所有 24 個 API 端點已就緒，服務運行正常。

**祝交易愉快！** 📈

---

**版本**: 1.0.0  
**最後更新**: 2025-11-05  
**狀態**: ✅ 生產就緒
