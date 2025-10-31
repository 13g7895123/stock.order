# 凱基證券 (KGI Securities) API 文件

## 券商資訊

- **券商名稱**: 凱基證券股份有限公司
- **英文名稱**: KGI Securities Co., Ltd.
- **英文縮寫**: KGI
- **API 名稱**: KGI API

## API 官方資源

- **官方網站**: https://www.kgieworld.com.tw/
- **API 服務說明**: https://www.kgieworld.com.tw/service/Service_3_5.aspx?frm=15
- **凱基期貨 API**: 需透過營業員申請

## 主要特色

### 1. 支援的程式語言
- **C#**
- **VBA**
- **Python**

### 2. 支援的市場
- 台灣證券市場
- 台灣期貨市場
- 美股市場 (需另外申請)
- 海外期貨

### 3. 核心功能
- 即時行情報價
- 證券下單
- 期貨/選擇權下單
- 帳戶查詢
- 美股即時行情 (與 NASDAQ 合作)

### 4. API 優勢
- 支援國內外市場
- 提供美股即時行情
- 多種程式語言支援
- 完整的證券與期貨功能

## 技術規格

### 系統需求
- Windows 作業系統
- .NET Framework (C# 開發需要)
- 凱基證券帳戶與交易憑證

### 安裝方式

1. **下載 API 元件**
   - 證券 API 和期貨 API 需分別下載
   - 從凱基期貨網站下載

2. **安裝元件**
   - 解壓縮並安裝 API 元件
   - 註冊 COM 元件 (如需要)

3. **設定憑證**
   - 安裝凱基數位憑證
   - 完成身份驗證設定

### 基本使用範例 (C#)

```csharp
// 引用凱基 API
// 詳細使用方式請參考官方提供的範例程式

// 初始化
// KGI API 初始化程式碼

// 登入
// 使用帳號、密碼、憑證登入

// 訂閱報價
// 訂閱股票即時報價

// 下單
// 執行買賣下單
```

### MetaTrader 5 整合

凱基 API 可與 MT5 整合使用：

1. 下載 KGI Smart Platform API
2. 複製 DLL 檔案：
   - Package.dll
   - PushClient.dll
   - QuoteCom.dll
3. 放入 MT5 指定目錄
4. 設定 MT5 連線參數

## 下單參數說明

### 買賣別
- 買進
- 賣出

### 價格類型
- 限價
- 市價
- 範圍市價

### 委託類型
- ROD (當日有效)
- IOC (立即成交否則取消)
- FOK (全部成交否則取消)

## 申請流程

### 證券 API

1. **開立凱基證券帳戶**
   - 需有凱基證券交易帳戶

2. **聯繫營業員**
   - 向您的凱基營業員申請 API 服務
   - 填寫相關申請表單

3. **簽署風險預告書**
   - 簽署 API 交易風險預告書
   - 了解程式交易風險

4. **下載 API**
   - 從官方網站或透過營業員取得
   - 下載對應的 API 版本

5. **安裝與測試**
   - 安裝 API 元件
   - 參考範例程式進行測試

### 期貨 API

1. **開立凱基期貨帳戶**
   - 需有凱基期貨交易帳戶

2. **線上申請**
   - 至凱基期貨網站申請
   - 或透過營業員協助申請

3. **下載期貨 API**
   - 從凱基期貨網站下載
   - 證券與期貨 API 需分別下載

4. **開始開發**
   - 參考官方文件與範例
   - 進行程式開發與測試

### 美股 API

凱基證券提供美股即時行情 API：

1. **申請條件**
   - 需有凱基證券帳戶
   - 與 NASDAQ 合作提供即時行情

2. **特色**
   - 真正的美股即時行情
   - 高度客製化資料串接
   - 詳細的 API 說明文件
   - 支援 C# 程式語言

3. **申請方式**
   - 聯繫凱基營業員
   - 填寫美股 API 申請表

## 使用限制與注意事項

### 1. 平台限制
- 主要支援 Windows 平台
- 需要 Windows 環境執行

### 2. 使用資格
- 需具備凱基證券/期貨帳戶
- 需簽署 API 服務相關文件
- 需通過營業員審核

### 3. 技術要求
- 需具備程式開發能力
- 建議熟悉 C# 或 Python
- 需了解金融市場交易規則

### 4. API 分離
- 證券 API 和期貨 API 需分別下載
- 不同市場可能有不同的 API 版本

### 5. 費用
- API 使用免費
- 交易手續費依照帳戶約定費率
- 美股行情可能有額外費用

## 教學資源

### 官方資源
- **API 操作說明**: 下載 API 後附帶的操作手冊
- **範例程式**: API 套件包含 C#、VBA、Python 範例

### 社群資源

#### 部落格教學
- **EyeTrading**: [凱基API 操作記錄--下載與安裝](https://eyetrading.github.io/tutor/kgi_api_install/)
- **凱基期貨 API 申請教學**: [如何申請凱基期貨API教學](https://www.rich8.com.tw/index.php/futures-lesson/111-api)
- **凱基期貨李佳舫部落格**: [程式交易常見問題](https://saysayrich.com/en/faq_category/quantify-future/)

#### MT5 整合
- **青禾金融資訊**: [凱基行情 API 設定說明](https://www.greenshop.com.tw/2021/07/21/mt5-kgi-api/)

### Facebook 社群
- 有相關的程式交易社團討論凱基 API 使用

## 常見問題 FAQ

### Q1: 凱基證券和凱基期貨的 API 一樣嗎？
A: 不一樣，需要分別下載和申請

### Q2: Python 可以使用凱基 API 嗎？
A: 可以，凱基提供 Python 範例

### Q3: 可以交易美股嗎？
A: 可以，但需另外申請美股 API 服務

### Q4: API 支援 Mac 嗎？
A: 官方主要支援 Windows，Mac 可能需要使用虛擬機

### Q5: 如何取得 API 文件？
A: 下載 API 元件後，內附完整操作說明文件 (PDF)

## 與其他平台整合

### MultiCharts
- 凱基 API 可與 MultiCharts 整合
- 用於程式交易策略執行

### MetaTrader 5
- 支援與 MT5 整合
- 可用於技術分析與自動交易

## 注意事項

### 文件取得
- 完整 API 文件需要下載 API 元件後才能查看
- 檔名通常為「元大證券API操作說明.pdf」或類似名稱

### 申請流程
- 建議直接聯繫凱基營業員了解最新申請流程
- 不同服務 (證券/期貨/美股) 可能有不同的申請方式

## 更新日誌

- 最後更新: 2025-10-31
- 資料來源: 官方網站、社群部落格

## 聯絡資訊

- **客服電話**: 請參考凱基證券官網
- **官方網站**: https://www.kgieworld.com.tw/
- **凱基期貨**: https://www.kgifutures.com.tw/
- **技術支援**: 透過營業員或客服

---

## 相關連結

- [凱基證券官網](https://www.kgieworld.com.tw/)
- [凱基 API 服務說明](https://www.kgieworld.com.tw/service/Service_3_5.aspx?frm=15)
- [EyeTrading 安裝教學](https://eyetrading.github.io/tutor/kgi_api_install/)
- [凱基期貨 API 申請](https://www.rich8.com.tw/index.php/futures-lesson/111-api)
- [MT5 整合教學](https://www.greenshop.com.tw/2021/07/21/mt5-kgi-api/)
