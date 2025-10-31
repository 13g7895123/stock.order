# 元大證券 (Yuanta Securities) API 文件

## 券商資訊

- **券商名稱**: 元大證券股份有限公司
- **英文名稱**: Yuanta Securities Co., Ltd.
- **英文縮寫**: Yuanta
- **API 名稱**: Yuanta API / OneAPI

## API 官方資源

- **API 下單頁面**: https://www.yuanta.com.tw/file-repository/content/API/page/index.html
- **API 服務申請**: https://www.yuanta.com.tw/eyuanta/Securities/DigitalArea/ApiOrder
- **元大期貨 API**: https://www.yuantafutures.com.tw/ytf/easywin/api/download.html
- **期貨 API 申請**: https://www.yuantafutures.com.tw/apisigning
- **歷史資料 API**: https://ys.yuanta.com.tw/quartet/api/YuantaOneHis.pdf

## 主要特色

### 1. 支援的市場
- 台灣證券市場
- 台灣期貨市場
- 選擇權市場

### 2. 核心功能
- 即時報價 (Quote API)
- 證券下單 (Trading API)
- 期貨下單
- 歷史資料查詢
- 帳戶資訊查詢

### 3. API 優勢
- 元大為台灣最大券商之一
- API 服務穩定
- 申請無門檻限制
- 提供報價與交易雙 API

## 技術規格

### 系統需求
- Windows 作業系統 (主要)
- .NET Framework
- 元大證券帳戶與憑證

### API 元件

元大提供以下 API 元件：

1. **交易 API (Trading API)**
   - 用於下單、改單、刪單
   - 查詢委託、成交

2. **報價 API (Quote API)**
   - 即時行情訂閱
   - 歷史資料查詢

### 安裝方式

1. **線上簽署同意書**
   - 透過「e櫃台」APP 或元大官網
   - 簽署「API服務申請暨交易風險預告書」

2. **下載 API 元件**
   - 從官方網站下載
   - 包含範例程式與操作文件

3. **解壓縮並查看文件**
   - 解壓縮後可找到「元大證券API操作說明.pdf」
   - 包含不同程式語言的範例

### 基本使用流程

```
1. 申請並簽署同意書
2. 下載 API 元件
3. 閱讀操作說明文件
4. 安裝憑證
5. 參考範例程式開發
6. 測試與上線
```

### Python 使用範例

```python
# 使用社群開發的 Yuanta API Python 封裝
# GitHub: https://github.com/penut85420/YuantaAPI-Python

# 基本使用流程
# 1. 初始化 API
# 2. 登入
# 3. 訂閱報價
# 4. 執行交易
```

## 申請流程

### 證券 API

1. **確認帳戶資格**
   - 需有元大證券帳戶
   - **無門檻限制** - 所有客戶皆可申請

2. **線上簽署同意書**
   - 方式一：使用「投資先生」APP
   - 方式二：使用「e櫃台」
   - 方式三：元大證券官網線上簽署

3. **簽署文件**
   - 簽署「API服務申請暨交易風險預告書」

4. **下載 API**
   - 簽署完成後即可下載
   - 分為交易 API 和報價 API

5. **開始開發**
   - 參考操作說明文件
   - 使用範例程式開發

### 期貨 API

1. **開立期貨帳戶**
   - 需有元大期貨帳戶

2. **線上申請**
   - 至元大期貨網站申請
   - 網址：https://www.yuantafutures.com.tw/apisigning

3. **簽署同意書**
   - 依監管要求簽署相關文件

4. **下載期貨 API**
   - 從期貨網站下載

## 使用限制與注意事項

### 1. 使用資格
- **證券 API**: 無門檻限制
- 需簽署 API 服務申請書
- 需了解程式交易風險

### 2. 技術限制
- 元大僅提供 API 連線元件
- **不提供程式開發教學**
- **不提供除錯服務**
- 需自行具備程式開發能力

### 3. 技術要求
- 需具備程式開發技能
- 需能自行除錯
- 建議熟悉 .NET 或相關技術

### 4. 服務啟用
- 交易 API 和報價 API 需分別申請啟用
- 依監管要求需先核准才能使用

### 5. 費用
- API 使用免費
- 交易手續費依照帳戶約定費率

## 教學資源

### 官方資源
- **API 操作說明**: 下載 API 後包含完整 PDF 文件
- **範例程式**: 包含多種程式語言範例
- **規格文件**: 詳細的 API 規格說明

### 社群資源

#### GitHub 專案
- **YuantaAPI-Python**: https://github.com/penut85420/YuantaAPI-Python
  - Python 封裝的元大 API
  - 簡化使用流程

#### 部落格文章
- **Medium**: [元大API即時行情串接(一)](https://medium.com/coding-learning-sharing/元大api即時行情串接-一-f431aa86477a)

#### 安裝教學
- **GSnail**: [安裝元大證券 OneAPI](https://www.gsnail.trade/web/ins/ins_yuanta)

### 社群討論
- Facebook 量化交易社團
- PTT Stock 板

## API 版本

### OneAPI
- 元大新版 API 統稱為 OneAPI
- 整合交易與報價功能

### 歷史資料 API
- 提供歷史行情資料查詢
- 文件：https://ys.yuanta.com.tw/quartet/api/YuantaOneHis.pdf

## 常見問題 FAQ

### Q1: 元大 API 有申請門檻嗎？
A: 沒有，所有元大客戶都可申請，無門檻限制

### Q2: 元大提供程式開發教學嗎？
A: 不提供，僅提供 API 元件和文件，需自行具備開發能力

### Q3: API 支援哪些程式語言？
A: 提供多種語言範例，包含 C#、VB 等，也可用 Python 透過社群套件

### Q4: 如何取得 API 文件？
A: 下載 API 元件後，解壓縮可找到「元大證券API操作說明.pdf」

### Q5: 報價 API 和交易 API 要分開申請嗎？
A: 是的，兩者需分別申請和啟用

### Q6: 遇到技術問題可以找誰？
A: 元大不提供開發和除錯服務，需自行解決或尋求社群協助

## 支援說明

### 官方支援範圍
- 提供 API 元件
- 提供操作說明文件
- 提供範例程式碼

### 官方不支援項目
- 程式開發教學
- 程式除錯服務
- 客製化開發需求

### 建議
- 加入量化交易社群
- 參考社群的開源專案
- 尋求有經驗的開發者協助

## 與其他平台比較

### 優勢
- 無申請門檻
- 台灣最大券商之一
- API 服務穩定

### 需注意
- 不提供開發教學和除錯
- 需自行具備完整開發能力
- 主要支援 Windows

## 更新日誌

- 最後更新: 2025-10-31
- 資料來源: 官方網站、社群資源

## 聯絡資訊

- **客服電話**: 請參考元大證券官網
- **官方網站**: https://www.yuanta.com.tw/
- **API 頁面**: https://www.yuanta.com.tw/file-repository/content/API/page/index.html
- **期貨 API**: https://www.yuantafutures.com.tw/

---

## 相關連結

- [元大證券官網](https://www.yuanta.com.tw/)
- [元大 API 下單](https://www.yuanta.com.tw/file-repository/content/API/page/index.html)
- [元大期貨 API](https://www.yuantafutures.com.tw/ytf/easywin/api/download.html)
- [元大期貨 API 申請](https://www.yuantafutures.com.tw/apisigning)
- [YuantaAPI-Python (GitHub)](https://github.com/penut85420/YuantaAPI-Python)
- [GSnail 安裝教學](https://www.gsnail.trade/web/ins/ins_yuanta)
- [元大期貨 API 申請及使用教學](https://itrader.com.tw/%E5%85%83%E5%A4%A7%E6%9C%9F%E8%B2%A8-api-%E7%94%B3%E8%AB%8B%E5%8F%8A%E4%BD%BF%E7%94%A8/)
