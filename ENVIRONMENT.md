# 環境模式說明文件

## 環境架構

本系統支援兩種運行環境模式：

### 1. 測試環境（Mock 模式）✅
- **use_mock**: `true`
- **資料來源**: Mock 資料（模擬資料）
- **SDK 需求**: 無需安裝 fubon-neo
- **適用場景**: 
  - 功能測試
  - 介面開發
  - 學習使用
  - CI/CD 測試
- **特點**:
  - 返回固定的模擬資料
  - 不會執行真實交易
  - 無需真實帳號和憑證
  - 立即可用

### 2. 正式環境（Real 模式）⚠️
- **use_mock**: `false`
- **資料來源**: 富邦 Neo API（真實資料）
- **SDK 需求**: 必須安裝 fubon-neo 套件
- **適用場景**:
  - 真實交易
  - 實時行情查詢
  - 帳戶管理
- **特點**:
  - 連接富邦證券真實 API
  - 執行真實交易委託
  - 需要真實帳號和憑證
  - 需要安裝 SDK

## 安裝 fubon-neo SDK

如果要使用正式環境，需要安裝富邦 Neo SDK：

```bash
# 進入虛擬環境
source venv/bin/activate

# 安裝 fubon-neo（請聯繫富邦證券取得套件）
pip install fubon-neo
```

> **注意**: fubon-neo 不在 PyPI 上，需要向富邦證券申請並取得安裝套件。

## 前端環境切換

前端應用頂部導航欄提供環境切換功能：

- **測試環境**: 使用 Mock 資料，無需 SDK
- **正式環境**: 使用真實 SDK，需要安裝 fubon-neo

切換環境時：
1. 系統會提示確認（如果已登入）
2. 自動登出當前會話
3. 下次登入時使用新環境的模式

## API 登入參數

登入 API 接受 `use_mock` 參數來決定使用哪種模式：

```json
{
  "user_id": "your_account",
  "password": "your_password",
  "cert_path": "/path/to/cert.pfx",
  "use_mock": true  // true=測試環境, false=正式環境
}
```

### 測試環境登入範例

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "password": "test_password",
    "cert_path": "/tmp/test.pfx",
    "use_mock": true
  }'
```

**回應**:
```json
{
  "success": true,
  "message": "登入成功 - Mock 模式（測試環境）",
  "user_id": "test_user",
  "session_id": "default"
}
```

### 正式環境登入範例（需要 SDK）

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "real_account",
    "password": "real_password",
    "cert_path": "/path/to/real/cert.pfx",
    "use_mock": false
  }'
```

**成功回應**:
```json
{
  "success": true,
  "message": "登入成功 - 真實 SDK（正式環境）",
  "user_id": "real_account",
  "session_id": "default"
}
```

**失敗回應（SDK 未安裝）**:
```json
{
  "detail": "正式環境需要安裝 fubon-neo SDK。請執行: pip install fubon-neo"
}
```

## 環境檢測機制

系統在啟動時會自動檢測 fubon-neo SDK：

```python
# 後端自動檢測
FUBON_NEO_AVAILABLE = False
try:
    import fubon_neo
    FUBON_NEO_AVAILABLE = True
    logger.info("fubon-neo SDK is available")
except ImportError:
    logger.warning("fubon-neo SDK not installed, only Mock mode available")
```

如果嘗試使用正式環境但 SDK 未安裝，會返回 503 錯誤。

## 資料差異說明

### Mock 模式資料特徵
- 固定的模擬資料
- 持股: 2330 台積電、2317 鴻海
- 帳戶餘額: 1,000,000 元
- 訂單狀態: 模擬狀態變化
- 不會真的送出交易

### Real 模式資料特徵
- 即時市場資料
- 真實帳戶持股
- 實際資金餘額
- 真實訂單委託
- **會執行真實交易** ⚠️

## 安全建議

1. **開發/測試階段**: 使用測試環境（Mock 模式）
2. **正式交易前**: 務必確認環境設定正確
3. **憑證安全**: 不要將真實憑證檔案提交到版本控制
4. **帳號安全**: 不要在程式碼中硬編碼真實帳號密碼
5. **測試交易**: 建議先使用富邦提供的測試帳號

## 環境狀態查詢

可以透過登入狀態 API 查詢當前環境模式：

```bash
curl -X GET http://localhost:8000/api/v1/auth/status
```

**回應**:
```json
{
  "is_logged_in": true,
  "user_id": "test_user",
  "session_id": "default"
}
```

## 常見問題

### Q1: 切換環境需要重啟服務嗎？
A: 不需要。環境模式在登入時決定，切換環境只需要重新登入。

### Q2: 可以同時使用兩種環境嗎？
A: 可以。透過不同的 session_id 可以維持多個會話，每個會話可以使用不同的環境。

### Q3: Mock 模式的資料會變化嗎？
A: Mock 模式返回固定的模擬資料，但會模擬合理的狀態變化（如訂單狀態）。

### Q4: 如何確認目前使用哪種環境？
A: 登入成功後，message 欄位會顯示 "Mock 模式（測試環境）" 或 "真實 SDK（正式環境）"。

### Q5: 正式環境需要哪些準備？
A: 
1. 安裝 fubon-neo SDK
2. 準備富邦證券帳號
3. 準備憑證檔案 (.pfx)
4. 確認帳戶有足夠權限

## 總結

| 項目 | 測試環境 | 正式環境 |
|------|---------|---------|
| SDK 需求 | ❌ 不需要 | ✅ 必須安裝 |
| 資料來源 | Mock 資料 | 真實 API |
| 交易執行 | ❌ 不執行 | ✅ 真實執行 |
| 帳號需求 | ❌ 任意 | ✅ 真實帳號 |
| 憑證需求 | ❌ 任意 | ✅ 真實憑證 |
| 適用場景 | 開發測試 | 正式交易 |

**預設建議**: 使用測試環境進行開發和測試，確認功能無誤後再切換至正式環境。
