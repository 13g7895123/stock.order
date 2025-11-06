# 富邦 Neo API (fubon-neo) 安裝指南

## 套件資訊

- **套件名稱**: fubon-neo
- **版本**: 2.2.5
- **Python 版本要求**: Python 3.7+

## 可用的 Wheel 檔案

本專案 `docs/` 目錄下有以下 wheel 檔案：

```
fubon_neo-2.2.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl  (Linux 版本)
fubon_neo-2.2.5-cp37-abi3-win_amd64.whl  (Windows 版本 - 已有 Linux 版本，建議優先使用)
```

### Wheel 檔案命名解析

**Linux 版本**:
- `fubon_neo`: 套件名稱
- `2.2.5`: 版本號
- `cp37`: CPython 3.7
- `abi3`: Stable ABI (相容 Python 3.7+)
- `manylinux_2_17_x86_64`: **Linux x86_64 平台** (glibc 2.17+)

**Windows 版本**:
- `win_amd64`: **Windows 64-bit 平台**

## 安裝方式

### ✅ 支援的平台

本專案現已提供多平台支援：

#### Linux (推薦 - WSL2/Ubuntu)
- ✅ Linux x86_64 (glibc 2.17+)
- ✅ Ubuntu 18.04+
- ✅ WSL2 (Windows Subsystem for Linux)
- ✅ Python 3.7 ~ 3.12

#### Windows
- ✅ Windows 10/11 (64-bit)
- ✅ Windows Server (64-bit)
- ✅ Python 3.7 ~ 3.12

#### 不支援的環境
- ❌ macOS (Apple Silicon / Intel)
- ❌ Windows 32-bit
- ❌ ARM 架構

### Linux/WSL 安裝步驟（推薦）

如果你在 **Linux** 或 **WSL2** 環境：

```bash
# 方法 1: 使用 pip 直接安裝
pip install docs/fubon_neo-2.2.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# 方法 2: 在虛擬環境中安裝
source venv/bin/activate
pip install docs/fubon_neo-2.2.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

### Windows 安裝步驟

如果你在 **Windows** 環境（非 WSL）：

```powershell
# 方法 1: 直接安裝 wheel 檔案
pip install docs\fubon_neo-2.2.5-cp37-abi3-win_amd64.whl

# 方法 2: 使用完整路徑
pip install C:\path\to\stock.order\docs\fubon_neo-2.2.5-cp37-abi3-win_amd64.whl
```

### 備選方案: 使用 Mock 模式開發
如果暫時無法安裝 fubon-neo，本專案已實作完整的 Mock Broker：

```bash
# 後端會自動偵測並使用 Mock 模式
./start_api.sh
```

Mock 模式特點：
- ✅ 完整的 API 介面
- ✅ 模擬真實回應格式
- ✅ 適合開發和測試
- ⚠️ 不會執行真實交易

## 驗證安裝

安裝成功後，在 Python 中驗證：

```python
import fubon_neo

print(f"fubon-neo 版本: {fubon_neo.__version__}")
```

## 如何在本專案使用

### 1. 安裝 fubon-neo

```bash
# Linux/WSL 環境（推薦）
pip install docs/fubon_neo-2.2.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Windows 環境
pip install docs\fubon_neo-2.2.5-cp37-abi3-win_amd64.whl
```

### 2. 重啟 API 服務

```bash
# 後端會自動偵測 fubon-neo 是否可用
./start_api.sh
```

### 3. 確認模式

啟動後會顯示：

```
🔌 富邦券商實作狀態
━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ 使用真實 SDK: FubonBroker
  來源: src.brokers.fubon.broker
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

或如果使用 Mock：

```
🔌 富邦券商實作狀態
━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ 使用 Mock 模式: FubonBrokerMock
  原因: fubon-neo 套件未安裝
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 前端環境切換

前端應用支援環境切換：

- **測試環境**: 強制使用 Mock 資料（適合開發）
- **正式環境**: 使用真實 SDK（需要安裝 fubon-neo）

登入時會自動根據選擇的環境決定使用 Mock 或真實連接。

## 常見問題

### Q1: 在 Linux 安裝 Windows 版本出現錯誤
```
ERROR: fubon_neo-2.2.5-cp37-abi3-win_amd64.whl is not a supported wheel on this platform.
```

**原因**: 使用了錯誤的 wheel 檔案  
**解決**: 請安裝 Linux 版本：
```bash
pip install docs/fubon_neo-2.2.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

### Q2: 驗證安裝是否成功
```bash
python3 -c "import fubon_neo; print(f'fubon-neo 版本: {fubon_neo.__version__}')"
```
應該輸出：`fubon-neo 版本: 2.2.5`

### Q3: Mock 模式和真實模式有什麼差別？
| 項目 | Mock 模式 | 真實模式 |
|------|-----------|----------|
| 資料來源 | 模擬資料 | 富邦證券伺服器 |
| 下單功能 | ❌ 不會真的下單 | ✅ 真實下單 |
| 行情資料 | 固定數值 | 即時更新 |
| 適用情境 | 開發、測試 | 生產環境 |

### Q4: WSL2 和 Linux 原生環境有差別嗎？
沒有差別，兩者都可以使用相同的 Linux wheel 檔案。WSL2 本質上就是一個完整的 Linux 核心。

## 支援管道

如需協助：
1. 聯絡富邦證券 API 技術支援
2. 查閱富邦證券開發者文件
3. 檢查本專案的 `docs/brokers/fubon/README.md`

## 相關文件

- [富邦券商實作說明](brokers/fubon/README.md)
- [API 安裝指南](../INSTALLATION.md)
- [快速開始](../QUICKSTART.md)
