# 元富證券 (MasterLink Securities) API 文件

## 券商資訊

- **券商名稱**: 元富證券股份有限公司
- **英文名稱**: MasterLink Securities Corporation
- **英文縮寫**: MasterLink / MLS
- **API 名稱**: 元富數位 API / 元富活躍新手 API

## API 官方資源

- **數位 API 專區**: https://mlapi.masterlink.com.tw/web_api/service/home
- **元富活躍新手 API**: https://ml-fugle-api.masterlink.com.tw/FugleSDK/
- **快速開始**: https://ml-fugle-api.masterlink.com.tw/FugleSDK/docs/trading/quickstart/
- **事前準備**: https://ml-fugle-api.masterlink.com.tw/FugleSDK/docs/trading/prepare/
- **TEJ 教學**: https://www.tejwin.com/insight/元富證-api/

## 主要特色

### 1. 支援的程式語言
- **Python** (官方支援)
- **C#** (官方支援)

### 2. 支援的市場
- 台灣證券市場
- 台灣期貨市場

### 3. 核心功能
- 程式交易
- 量化交易
- 即時報價
- 歷史資料
- 證券下單
- 期貨下單
- 帳戶查詢

### 4. 特殊功能
- **模擬交易所**
  - 在台股開盤至收盤期間
  - 提供行情逐筆撮合機制
  - 用於測試交易策略

### 5. 與 TQuant Lab 整合
- 可搭配 TQuant Lab 使用
- 提供策略回測功能
- 自動化下單整合

## 技術規格

### API 服務申請條件
- 需經過申請流程
- 通過認證核准後才可使用
- 需簽署相關同意書

### 技術要求

元富證券的重要說明：
- **僅提供 API 元件**
- 客戶需**自行開發前端程式與 UI 介面**
- 需具備**程式開發能力**
- 需具備**除錯能力**

### 安裝方式

#### 下載 SDK
```bash
# 從官方網站下載對應的 SDK
# Python SDK 或 C# SDK
```

#### Python SDK 安裝 (如有提供)
```bash
# 參考官方文件進行安裝
pip install masterlink-api  # 範例，實際名稱以官方為準
```

### 基本使用流程

```
1. 申請元富證券帳戶
2. 申請 API 服務
3. 簽署風險預告書
4. 下載 SDK 和憑證
5. 參考文件開發
6. 測試與上線
```

## 申請流程

### 1. 開立元富證券帳戶
- 需有元富證券交易帳戶
- 線上或臨櫃開戶

### 2. 申請 API 服務

**線上簽署流程**：
- 提出 API 服務申請
- 線上簽署同意書和風險預告書

### 3. 取得憑證
- 申請核准後下載憑證
- 憑證用於 API 認證

### 4. 下載 SDK
- 從官方網站下載
- 選擇 Python 或 C# 版本

### 5. 參考文件開發
- 閱讀 API 文件
- 參考範例程式
- 自行開發前端介面

## 元富活躍新手 API

元富與 Fugle 合作推出的新手友善 API：

### 特色
- 類似玉山證券富果 API 的架構
- 開發者友善的設計
- 詳細的文件說明

### 資源
- **官網**: https://ml-fugle-api.masterlink.com.tw/FugleSDK/
- **快速開始**: 提供 5-10 分鐘快速上手指南
- **完整文件**: 詳細的 API Reference

## 使用限制與注意事項

### 1. 開發要求
- **必須自行開發前端程式**
- **必須自行開發 UI 介面**
- 元富僅提供 API 元件
- 不提供完整的交易軟體

### 2. 技術要求
- 需具備程式開發能力
- 需具備程式除錯能力
- 建議熟悉 Python 或 C#

### 3. 帳戶要求
- 需有元富證券帳戶
- 需申請並獲得 API 使用權限
- 需簽署相關風險預告書

### 4. 費用
- API 使用免費
- 交易手續費依照帳戶約定費率

### 5. 支援範圍
- 提供 API 元件和文件
- 不提供軟體開發服務
- 不提供 UI 介面

## 模擬交易所功能

### 特色
元富數位 API 提供模擬交易所功能：

- **運作時間**: 台股開盤至收盤期間
- **撮合機制**: 提供行情逐筆撮合
- **用途**: 測試交易策略

### 優勢
- 真實市場行情
- 即時撮合測試
- 零風險策略驗證

## TQuant Lab 整合

### 什麼是 TQuant Lab？
- TEJ 提供的量化交易平台
- 可與元富 API 整合

### 整合功能
- 策略回測
- 自動化下單
- 績效分析

### 教學資源
- **TEJ 教學**: https://www.tejwin.com/insight/元富證-api/
  - 詳細的整合教學
  - TQuant Lab 使用說明
  - 自動化下單流程

## 教學資源

### 官方資源

1. **元富數位 API 專區**
   - https://mlapi.masterlink.com.tw/web_api/service/home
   - 申請流程說明
   - API 服務介紹

2. **元富活躍新手 API 文件**
   - https://ml-fugle-api.masterlink.com.tw/FugleSDK/
   - 完整的開發者文件
   - 快速開始指南

3. **快速開始指南**
   - https://ml-fugle-api.masterlink.com.tw/FugleSDK/docs/trading/quickstart/
   - 風險預告書申請
   - 憑證下載
   - SDK 下載

### 第三方教學

1. **TEJ 教學**
   - https://www.tejwin.com/insight/元富證-api/
   - 元富 API 初學者指南
   - TQuant Lab 整合教學

2. **量化交易教學**
   - QuantPass: [元富證券API權限申請](https://quantpass.org/masterlink-api/)
   - API 介紹與串接教學

## 常見問題 FAQ

### Q1: 元富 API 需要自己寫程式嗎？
A: 是的，元富僅提供 API 元件，需自行開發前端程式和 UI

### Q2: 有提供完整的交易軟體嗎？
A: 沒有，需要自行開發，或搭配 TQuant Lab 等第三方平台

### Q3: 支援哪些程式語言？
A: 官方支援 Python 和 C#

### Q4: 有模擬交易功能嗎？
A: 有，提供模擬交易所，可在開盤時間測試策略

### Q5: 元富活躍新手 API 和數位 API 有什麼差別？
A: 活躍新手 API 是與 Fugle 合作的新版 API，對開發者更友善

### Q6: 可以和 TQuant Lab 整合嗎？
A: 可以，元富 API 支援與 TQuant Lab 整合

## 與其他券商比較

### 優勢
- 提供模擬交易所功能
- 支援 Python 和 C#
- 可與 TQuant Lab 整合
- 新版活躍新手 API 對開發者友善

### 需注意
- 需完全自行開發前端
- 需具備完整開發能力
- 沒有提供現成的交易介面

## API 版本

### 元富數位 API
- 傳統的元富 API
- 需要較多的開發工作

### 元富活躍新手 API
- 與 Fugle 合作開發
- 現代化的 API 設計
- 開發者體驗較佳
- 文件較完整

**建議**: 新專案優先考慮活躍新手 API

## 適合對象

### 適合
- 具備程式開發能力的交易者
- 想要完全客製化交易系統的開發者
- 需要量化交易功能的使用者
- 使用 TQuant Lab 的用戶

### 不適合
- 不會寫程式的一般投資人
- 想要現成交易軟體的使用者
- 沒有時間開發介面的交易者

## 更新日誌

- 最後更新: 2025-10-31
- 資料來源: 官方網站、開發者文件、第三方教學

## 聯絡資訊

- **元富證券官網**: https://www.masterlink.com.tw/
- **數位 API**: https://mlapi.masterlink.com.tw/web_api/service/home
- **活躍新手 API**: https://ml-fugle-api.masterlink.com.tw/FugleSDK/
- **客服**: 請參考元富證券官網

---

## 相關連結

- [元富證券官網](https://www.masterlink.com.tw/)
- [元富數位 API](https://mlapi.masterlink.com.tw/web_api/service/home)
- [元富活躍新手 API](https://ml-fugle-api.masterlink.com.tw/FugleSDK/)
- [快速開始指南](https://ml-fugle-api.masterlink.com.tw/FugleSDK/docs/trading/quickstart/)
- [事前準備](https://ml-fugle-api.masterlink.com.tw/FugleSDK/docs/trading/prepare/)
- [TEJ 教學文章](https://www.tejwin.com/insight/元富證-api/)
- [QuantPass 教學](https://quantpass.org/masterlink-api/)
