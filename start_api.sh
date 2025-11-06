#!/bin/bash
# Fubon API 服務啟動腳本

echo "========================================="
echo "富邦證券 API 服務啟動腳本"
echo "========================================="
echo ""

# 檢查是否在專案根目錄
if [ ! -d "api" ]; then
    echo "❌ 錯誤: 請在專案根目錄執行此腳本"
    exit 1
fi

# 檢查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 未安裝 Python3"
    exit 1
fi

echo "📦 檢查環境..."

# 檢查是否需要安裝 venv
if [ ! -f "venv/bin/activate" ]; then
    echo "⚠️  虛擬環境不存在或不完整"
    echo ""
    echo "請先安裝 python3-venv:"
    echo "  sudo apt install python3.12-venv"
    echo ""
    echo "然後建立虛擬環境:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r api/requirements.txt"
    echo ""
    exit 1
fi

# 啟動虛擬環境
echo "🔧 啟動虛擬環境..."
source venv/bin/activate

# 檢查依賴
echo "📦 檢查依賴套件..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 安裝依賴套件..."
    pip install -r api/requirements.txt
fi

# 檢查環境變數
if [ ! -f "api/.env" ]; then
    echo "⚠️  警告: 未找到 .env 檔案"
    echo "請從 api/.env.example 複製並設定:"
    echo "  cp api/.env.example api/.env"
    echo "  nano api/.env"
    echo ""
fi

# 啟動服務
echo ""
echo "🚀 啟動 FastAPI 服務..."
echo "   URL: http://localhost:8000"
echo "   API 文件: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服務"
echo ""

cd api
python main.py
