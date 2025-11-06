#!/bin/bash

# 富邦證券 API 前端啟動腳本

echo "======================================"
echo "  富邦證券 API 前端應用"
echo "======================================"
echo ""

# 檢查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 錯誤: 找不到 Node.js"
    echo "請先安裝 Node.js: https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js 版本: $(node --version)"
echo "✓ npm 版本: $(npm --version)"
echo ""

# 進入前端目錄
cd "$(dirname "$0")/frontend" || exit 1

# 檢查 node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 首次執行，正在安裝依賴套件..."
    npm install
    echo ""
fi

# 檢查後端 API 是否運行
echo "🔍 檢查後端 API 服務..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✓ 後端 API 服務正常運行"
else
    echo "⚠️  警告: 後端 API 服務未運行"
    echo "   請先啟動後端服務: ./start_api.sh"
fi
echo ""

# 啟動開發伺服器
echo "🚀 啟動前端開發伺服器..."
echo "   前端地址: http://localhost:3000"
echo "   API 代理: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服務"
echo "======================================"
echo ""

npm run dev
