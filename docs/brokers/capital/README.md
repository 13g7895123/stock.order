# 群益證券 (Capital Securities) API 文件

## 券商資訊

- **券商名稱**: 群益金鼎證券股份有限公司
- **英文名稱**: Capital Securities Corporation
- **英文縮寫**: Capital
- **API 名稱**: SKCOM API

## API 官方資源

- **官方 API 下載**: https://www.capital.com.tw/Service2/download/api.asp
- **期貨 API 申請**: https://www.capital.com.tw/web/#/download/ApiTrading/ApiTradinginfo
- **GitHub 社群專案**: https://github.com/tacosync/skcom (第三方簡化套件)

## 主要特色

### 1. 支援的程式語言
- C# (主要支援)
- VBA
- Python (透過 COM 元件)

### 2. 支援的市場
- 台灣證券市場
- 台灣期貨市場
- 選擇權市場

### 3. 核心功能
- 即時報價訂閱
- 歷史 K 線資料
- 證券下單
- 期貨/選擇權下單
- 帳戶查詢

### 4. API 優勢
- 老牌券商，API 穩定
- 支援多種交易商品
- 完整的報價與交易功能

## 技術規格

### 系統需求
- Windows 作業系統
- .NET Framework 2.0 或更新版本
- 需安裝群益下單憑證 (雙因子認證)

### 安裝方式

1. 從官方網站下載 API 元件
2. 註冊 COM 元件
3. 安裝群益憑證 (2.13.35 版後必須)

### 基本使用範例 (C#)

```csharp
// 引用群益 API
using SKCOMLib;

// 建立報價物件
SKCenterLib m_pSKCenter = new SKCenterLib();
SKQuoteLib m_pSKQuote = new SKQuoteLib();

// 登入
int nCode = m_pSKCenter.SKCenterLib_Login(strLogInID, strPassWord);

// 訂閱報價
m_pSKQuote.SKQuoteLib_RequestStocks(ref nPage, "2330");

// 下單 (需使用 SKOrderLib)
SKOrderLib m_pSKOrder = new SKOrderLib();
// ... 下單邏輯
```

### Python 使用範例

```python
# 使用社群開發的 skcom 套件
from skcom import quicksk

# 登入
sk = quicksk.QuickSK()
sk.login()

# 訂閱報價
sk.subscribe_quote('2330')

# 下單
# 需參考完整文件實作下單邏輯
```

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

1. **開立群益證券帳戶**
   - 需有群益證券交易帳戶

2. **下載 API 元件**
   - 至官方網站下載最新版本 API
   - 安裝並註冊 COM 元件

3. **安裝憑證**
   - 安裝群益下單憑證
   - 完成雙因子認證設定

4. **開始開發**
   - 參考官方範例程式
   - 使用帳號密碼登入測試

### 期貨 API

1. **簽署同意書**
   - 至群益期貨「同意書專區」
   - 簽署「期貨API服務下單聲明書」

2. **下載期貨 API**
   - 下載期貨專用 API 元件

3. **開發測試**
   - 使用期貨帳號進行開發

## 使用限制與注意事項

### 1. 平台限制
- 主要支援 Windows 平台
- Linux/Mac 需要使用 Wine 或虛擬機

### 2. 認證要求
- 2.13.35 版後需使用雙因子認證
- 需安裝有效的群益下單憑證

### 3. 技術要求
- 需具備 C# 或 VBA 開發能力
- Python 開發者可使用社群套件但功能較有限

### 4. 費用
- API 使用免費
- 交易手續費依照帳戶約定費率

## 教學資源

### 官方資源
- 官方提供範例程式 (C#, VBA)
- API 操作說明文件 (需下載後查閱)

### 社群資源
- **skcom**: Python 社群套件，降低使用門檻
  - GitHub: https://github.com/tacosync/skcom
- **C# 開發教學**: https://github.com/eermagic/cs-capital-api-sample
- **Medium 文章**:
  - [群益API行情串接(一)](https://medium.com/coding-learning-sharing/群益api行情串接-一-19bc3169f6bb)

### Gist 範例
- [群益報價 API 連線、索取 K 線和即時報價](https://gist.github.com/f107110126/8d7ca155a5d2a4c69dba6a9a97d69fb4)

## 常見問題 FAQ

### Q1: 群益 API 支援 Mac/Linux 嗎？
A: 官方僅支援 Windows，Mac/Linux 需要使用 Wine 或虛擬機

### Q2: Python 可以使用群益 API 嗎？
A: 可以透過 COM 元件或使用社群開發的 skcom 套件

### Q3: 如何解決雙因子認證問題？
A: 需安裝最新版本的群益下單憑證，參考官方安裝說明

### Q4: API 和 MultiCharts 串接有什麼差別？
A: API 適合完全自行開發，MultiCharts 是現成的交易平台

## 已知問題

### 憑證安裝
- 新版 API 必須安裝憑證才能使用
- 憑證安裝失敗會導致登入錯誤

### 跨平台支援
- 原生不支援 Linux/Mac
- 社群方案可能不夠穩定

## 更新日誌

- 最後更新: 2025-10-31
- API 版本: 2.13.35+ (雙因子認證版)
- 資料來源: 官方網站、社群資源

## 聯絡資訊

- **客服電話**: 請參考群益證券官網
- **官方網站**: https://www.capital.com.tw/
- **API 下載**: https://www.capital.com.tw/Service2/download/api.asp

---

## 相關連結

- [群益證券官網](https://www.capital.com.tw/)
- [群益 API 官方下載](https://www.capital.com.tw/Service2/download/api.asp)
- [skcom GitHub (第三方 Python 套件)](https://github.com/tacosync/skcom)
- [C# 開發教學](https://github.com/eermagic/cs-capital-api-sample)
- [GSnail 安裝教學](https://gsnail.trade/web/ins/ins_capital)
