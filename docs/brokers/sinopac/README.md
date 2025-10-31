# 永豐證券 (SinoPac Securities) API 文件

## 券商資訊

- **券商名稱**: 永豐金證券股份有限公司
- **英文名稱**: SinoPac Securities
- **英文縮寫**: SinoPac
- **API 名稱**: Shioaji (澄清)

## API 官方資源

- **官方網站**: https://www.sinotrade.com.tw/ec/20191125/Main/index.aspx
- **開發者文件**: https://sinotrade.github.io/
- **證券下單文件**: https://sinotrade.github.io/zh_TW/tutor/order/Stock/
- **GitHub**: https://github.com/Sinopac/Shioaji

## 主要特色

### 1. 支援的程式語言
- Python (主要支援)

### 2. 支援的市場
- 台灣證券市場
- 台灣期貨市場
- 全球金融市場

### 3. 核心功能
- 自動化交易策略
- 即時市場報價
- 即時帳戶餘額監控
- 投資組合即時監控
- 歷史資料查詢

### 4. API 優勢
- 完整的 Python 整合
- 豐富的開發者文件
- 活躍的社群支援
- 提供模擬交易環境

## 技術規格

### 安裝方式

```bash
pip install shioaji
```

### 基本使用範例

```python
import shioaji as sj

# 建立 API 連線
api = sj.Shioaji()

# 登入
api.login(
    api_key="YOUR_API_KEY",
    secret_key="YOUR_SECRET_KEY"
)

# 取得股票資訊
contract = api.Contracts.Stocks["2330"]  # 台積電

# 下單
order = api.Order(
    price=600,
    quantity=1,
    action=sj.constant.Action.Buy,
    price_type=sj.constant.StockPriceType.LMT,
    order_type=sj.constant.OrderType.ROD,
)

# 執行下單
trade = api.place_order(contract, order)
```

## 下單參數說明

### Action (動作)
- `Buy`: 買進
- `Sell`: 賣出

### Price Type (價格類型)
- `LMT`: 限價 (Limit)
- `MKT`: 市價 (Market)
- `MKP`: 範圍市價

### Order Type (委託類型)
- `ROD`: 當日有效 (Rest of Day)
- `IOC`: 立即成交否則取消 (Immediate or Cancel)
- `FOK`: 全部成交否則取消 (Fill or Kill)

## 申請流程

1. **開立永豐金證券帳戶**
   - 需要有永豐金證券的證券或期貨帳戶

2. **申請 API 權限**
   - 登入永豐金證券官網
   - 填寫 API 服務申請表
   - 簽署相關風險預告書

3. **取得 API Key**
   - 申請核准後取得 API Key 和 Secret Key
   - 用於程式登入驗證

4. **開始開發**
   - 安裝 Shioaji SDK
   - 使用 API Key 進行開發測試

## 使用限制與注意事項

### 1. 使用資格
- 需要具備永豐金證券帳戶
- 需簽署 API 交易風險預告書

### 2. 技術要求
- 需具備 Python 程式開發能力
- 建議熟悉金融市場交易規則

### 3. 交易限制
- 遵守台灣證券交易所交易規則
- 需注意當日沖銷條件
- 遵守漲跌幅限制

### 4. 費用
- API 使用免費
- 交易手續費依照帳戶約定費率

## 教學資源

### 官方教學
- **豐雲學堂**: https://www.sinotrade.com.tw/richclub/PythonAPI/
  - 提供完整的 Python API 教學影片
  - 包含從入門到實戰的完整課程

### 社群資源
- GitHub Issues: 可以在官方 GitHub 提問
- 量化交易社群: 有許多開發者分享經驗

## 常見問題 FAQ

### Q1: Shioaji 支援哪些作業系統？
A: 支援 Windows、macOS 和 Linux

### Q2: 可以在模擬環境測試嗎？
A: 可以，Shioaji 提供模擬交易功能供開發者測試

### Q3: API 有呼叫次數限制嗎？
A: 請參考官方文件或聯繫永豐金證券確認最新限制

### Q4: 如何處理斷線重連？
A: Shioaji 有內建的重連機制，詳見官方文件

## 更新日誌

- 最後更新: 2025-10-31
- 資料來源: 官方網站、開發者文件

## 聯絡資訊

- **客服電話**: 請參考永豐金證券官網
- **官方網站**: https://www.sinotrade.com.tw/
- **技術支援**: 透過官方 GitHub Issues 提問

---

## 相關連結

- [永豐金證券官網](https://www.sinotrade.com.tw/)
- [Shioaji 開發者文件](https://sinotrade.github.io/)
- [Shioaji GitHub](https://github.com/Sinopac/Shioaji)
- [Python API 教學影片](https://www.sinotrade.com.tw/richclub/PythonAPI/)
