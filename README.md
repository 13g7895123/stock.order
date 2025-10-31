# 台灣券商 API 下單整合專案

這是一個整理台灣證券商 API 資訊的專案，旨在幫助開發者快速了解各家券商的程式交易 API 服務。

## 專案簡介

本專案收集並整理台灣主要券商的 API 下單服務資訊，包括：
- API 官方文件連結
- 支援的程式語言
- 申請流程說明
- 技術規格說明
- 使用範例
- 常見問題解答

## 支援的券商清單

### ⭐ 推薦 - 開發者友善

這些券商提供現代化的 API，文件完整，支援多種程式語言和作業系統：

| 券商 | 縮寫 | API 名稱 | 主要語言 | 跨平台 | 特色 |
|------|------|----------|----------|--------|------|
| [永豐證券](docs/brokers/sinopac/) | SinoPac | Shioaji | Python | ✓ | Python 專用，文件完整 |
| [富邦證券](docs/brokers/fubon/) | Fubon | Neo API | Python/C#/Node.js | ✓ | 多語言，跨平台 |
| [玉山證券](docs/brokers/esun/) | E.SUN | Fugle API | Python/JavaScript | ✓ | 現代化，易上手 |
| [元富證券](docs/brokers/masterlink/) | MasterLink | 活躍新手 API | Python/C# | 部分 | 提供模擬交易所 |

### 📊 傳統 API

這些券商提供穩定的 API 服務，但主要支援 Windows 和 .NET 平台：

| 券商 | 縮寫 | 主要語言 | 文件狀態 | 特色 |
|------|------|----------|----------|------|
| [群益證券](docs/brokers/capital/) | Capital | C#/VBA/Python | 完整 | 老牌穩定，社群套件豐富 |
| [凱基證券](docs/brokers/kgi/) | KGI | C#/VBA/Python | 完整 | 支援美股 API |
| [元大證券](docs/brokers/yuanta/) | Yuanta | C#/VB | 完整 | 無申請門檻，台灣最大 |
| [統一證券](docs/brokers/president/) | President | C#/VB | 完整 | 證券期貨皆支援 |
| [康和證券](docs/brokers/concord/) | Concord | C#/VBA/VB | 完整 | 2 款 API 可選 |

### 📋 資訊有限

這些券商有提供 API 服務，但公開資訊較少，建議直接聯繫營業員：

| 券商 | 縮寫 | 備註 |
|------|------|------|
| [國泰證券](docs/brokers/cathay/) | Cathay | 需透過營業員申請 |
| [日盛證券](docs/brokers/jihsun/) | JihSun | 網路資料較舊，建議確認最新狀態 |

## 快速選擇指南

### 我該選擇哪家券商？

#### 🐍 如果你主要使用 Python
1. **永豐證券 (Shioaji)** - 最推薦，Python 原生支援
2. **富邦證券 (Neo API)** - 多語言支援
3. **玉山證券 (Fugle API)** - 現代化設計

#### 💻 如果你使用 C# 或 .NET
1. **富邦證券 (Neo API)** - 現代化跨平台
2. **群益證券** - 穩定可靠
3. **元大證券** - 無門檻限制

#### 🍎 如果你使用 Mac/Linux
1. **永豐證券 (Shioaji)** - 原生支援
2. **富邦證券 (Neo API)** - 跨平台支援
3. **玉山證券 (Fugle API)** - 全平台支援

#### 📚 如果你是初學者
1. **玉山證券 (Fugle API)** - 文件易讀
2. **永豐證券 (Shioaji)** - 教學資源豐富
3. **富邦證券 (Neo API)** - 現代化設計

#### 📈 如果你需要期貨交易
1. **康和證券** - 期貨專業
2. **統一證券** - 期貨證券皆可
3. **凱基證券** - 國內外期貨

## 目錄結構

```
stock.order/
├── README.md                    # 本文件
└── docs/
    └── brokers/                 # 各券商 API 文件
        ├── sinopac/            # 永豐證券 (Shioaji)
        ├── capital/            # 群益證券
        ├── fubon/              # 富邦證券 (Neo API)
        ├── kgi/                # 凱基證券
        ├── yuanta/             # 元大證券
        ├── esun/               # 玉山證券 (Fugle API)
        ├── masterlink/         # 元富證券
        ├── cathay/             # 國泰證券
        ├── president/          # 統一證券
        ├── jihsun/             # 日盛證券
        └── concord/            # 康和證券
```

## 各券商詳細資訊

### 1. [永豐證券 (SinoPac)](docs/brokers/sinopac/)
- **API**: Shioaji
- **語言**: Python
- **平台**: Windows / macOS / Linux
- **特色**: Python 專用 API，文件完整，社群活躍

### 2. [群益證券 (Capital)](docs/brokers/capital/)
- **API**: SKCOM API
- **語言**: C# / VBA / Python (透過 COM)
- **平台**: Windows (主要)
- **特色**: 老牌穩定，社群有簡化套件

### 3. [富邦證券 (Fubon)](docs/brokers/fubon/)
- **API**: Fubon Neo API
- **語言**: Python / C# / Node.js
- **平台**: Windows / macOS / Linux
- **特色**: 新一代 API，多語言跨平台支援

### 4. [凱基證券 (KGI)](docs/brokers/kgi/)
- **API**: KGI API
- **語言**: C# / VBA / Python
- **平台**: Windows
- **特色**: 支援美股即時行情，與 NASDAQ 合作

### 5. [元大證券 (Yuanta)](docs/brokers/yuanta/)
- **API**: Yuanta API / OneAPI
- **語言**: C# / VB
- **平台**: Windows
- **特色**: 台灣最大券商，無申請門檻

### 6. [玉山證券 (E.SUN)](docs/brokers/esun/)
- **API**: 富果交易 API (Fugle Trading API)
- **語言**: Python / JavaScript
- **平台**: Windows / macOS / Linux
- **特色**: 與 Fugle 合作，現代化設計，文件易讀

### 7. [元富證券 (MasterLink)](docs/brokers/masterlink/)
- **API**: 元富數位 API / 活躍新手 API
- **語言**: Python / C#
- **平台**: 部分跨平台
- **特色**: 提供模擬交易所，可與 TQuant Lab 整合

### 8. [國泰證券 (Cathay)](docs/brokers/cathay/)
- **API**: 國泰 API
- **狀態**: 公開資訊較少
- **建議**: 聯繫營業員取得詳細資訊

### 9. [統一證券 (President)](docs/brokers/president/)
- **API**: 統一證券 API / PFCF API
- **語言**: C# / VB.NET
- **平台**: Windows
- **特色**: 證券和期貨分別有 API

### 10. [日盛證券 (JihSun)](docs/brokers/jihsun/)
- **API**: HTS API
- **狀態**: 網路資料較舊
- **建議**: 聯繫營業員確認最新狀態

### 11. [康和證券 (Concord)](docs/brokers/concord/)
- **API**: OCX API / 超級飆速 API
- **語言**: C# / VBA / VB.NET
- **平台**: Windows
- **特色**: 提供 2 款不同特性的 API

## 功能比較表

| 券商 | Python | C# | JavaScript | 跨平台 | 模擬環境 | 文件品質 |
|------|--------|----|-----------| -------|---------|---------|
| 永豐證券 | ✓ | - | - | ✓ | ✓ | ⭐⭐⭐⭐⭐ |
| 群益證券 | 部分 | ✓ | - | - | - | ⭐⭐⭐⭐ |
| 富邦證券 | ✓ | ✓ | ✓ | ✓ | ? | ⭐⭐⭐⭐⭐ |
| 凱基證券 | ✓ | ✓ | - | - | - | ⭐⭐⭐ |
| 元大證券 | 社群 | ✓ | - | - | - | ⭐⭐⭐ |
| 玉山證券 | ✓ | - | ✓ | ✓ | ✓ | ⭐⭐⭐⭐⭐ |
| 元富證券 | ✓ | ✓ | - | 部分 | ✓ | ⭐⭐⭐⭐ |
| 國泰證券 | ? | ? | ? | ? | ? | ⭐⭐ |
| 統一證券 | - | ✓ | - | - | - | ⭐⭐⭐ |
| 日盛證券 | - | ✓ | - | - | - | ⭐⭐ |
| 康和證券 | - | ✓ | - | - | - | ⭐⭐⭐ |

## 使用前須知

### 📋 申請條件
- 需要有該券商的證券或期貨帳戶
- 需簽署 API 交易風險預告書
- 部分券商可能需要通過審核

### 💰 費用
- API 使用通常免費
- 交易手續費依照帳戶約定費率
- 部分服務可能有額外費用（如美股行情）

### ⚠️ 風險提醒
- 程式交易有風險，請確保充分了解
- 務必先在模擬環境測試
- 妥善保管 API 金鑰和憑證
- 建議實作風控機制

### 🔒 安全性建議
1. 不要在程式碼中硬編碼帳號密碼
2. 使用環境變數或設定檔存放敏感資訊
3. 不要分享您的 API 金鑰
4. 定期更換密碼和憑證
5. 注意憑證有效期限

## 開發建議

### 選擇券商的考量因素

1. **程式語言偏好**
   - Python 開發者：永豐、富邦、玉山
   - C# 開發者：富邦、群益、元大
   - JavaScript 開發者：富邦、玉山

2. **作業系統**
   - Mac/Linux：永豐、富邦、玉山
   - Windows：所有券商

3. **文件品質**
   - 重視文件：永豐、富邦、玉山
   - 可接受較少文件：其他券商

4. **交易需求**
   - 證券為主：大部分券商
   - 期貨為主：康和、統一、凱基
   - 美股：凱基

5. **開發經驗**
   - 初學者：玉山、永豐
   - 有經驗：任何券商

## 社群資源

### 相關社群
- PTT Stock 板
- Facebook 量化交易社團
- GitHub 相關專案

### 推薦閱讀
- 量化交易入門教學
- Python 程式交易教學
- 台股交易規則說明

## 貢獻指南

歡迎提供更新或補充資訊：

1. Fork 本專案
2. 建立新分支
3. 提交您的修改
4. 發送 Pull Request

### 需要幫助的部分
- 補充更詳細的使用範例
- 更新過時的資訊
- 增加更多券商
- 翻譯成其他語言

## 免責聲明

1. 本專案僅供資訊參考，不構成投資建議
2. API 資訊可能隨時變動，請以券商官方最新資訊為準
3. 使用 API 進行交易前，請確保充分了解相關風險
4. 本專案與各券商無官方關聯
5. 投資有風險，交易請謹慎

## 授權

本專案採用 MIT 授權條款。

## 聯絡資訊

如有問題或建議，歡迎：
- 提出 Issue
- 發送 Pull Request
- 聯繫專案維護者

## 致謝

感謝所有提供 API 服務的券商，以及開源社群的貢獻者。

---

## 更新日誌

### 2025-10-31
- 初始版本發布
- 完成 11 家券商的資訊整理
- 建立專案架構和文件

## 下一步計劃

- [ ] 增加實際的程式碼範例
- [ ] 建立統一的介面層設計
- [ ] 實作多券商切換機制
- [ ] 增加效能比較測試
- [ ] 建立常見問題集
- [ ] 增加影片教學連結

## Star History

如果這個專案對您有幫助，歡迎給個 Star ⭐

---

**最後更新**: 2025-10-31
**維護狀態**: 積極維護中
**文件版本**: 1.0.0
