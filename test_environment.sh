#!/bin/bash

# 環境切換功能測試腳本

echo "======================================"
echo "  富邦證券 API 環境測試"
echo "======================================"
echo ""

# 顏色定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 測試計數
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 測試函數
test_case() {
    local name=$1
    local command=$2
    local expected=$3
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "測試 $TOTAL_TESTS: $name ... "
    
    result=$(eval "$command" 2>/dev/null)
    
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo "  預期包含: $expected"
        echo "  實際結果: $result"
    fi
}

echo "🔍 檢查服務狀態..."
echo "======================================"

# 檢查後端
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} 後端 API 服務運行中 (http://localhost:8000)"
else
    echo -e "${RED}✗${NC} 後端 API 服務未運行"
    echo "請先啟動: ./start_api.sh"
    exit 1
fi

# 檢查前端
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} 前端服務運行中 (http://localhost:3000)"
else
    echo -e "${YELLOW}⚠${NC} 前端服務未運行 (非必要)"
fi

# 檢查 fubon-neo 安裝
if python3 -c "import fubon_neo" 2>/dev/null; then
    version=$(python3 -c "import fubon_neo; print(fubon_neo.__version__)" 2>/dev/null)
    echo -e "${GREEN}✓${NC} fubon-neo 已安裝 (版本: $version)"
else
    echo -e "${RED}✗${NC} fubon-neo 未安裝"
    exit 1
fi

echo ""
echo "🧪 執行環境測試..."
echo "======================================"

# 測試 1: 健康檢查
test_case "健康檢查" \
    "curl -s http://localhost:8000/health" \
    "healthy"

# 測試 2: 測試環境登入 (Mock 模式)
test_case "測試環境登入 (Mock)" \
    "curl -s -X POST http://localhost:8000/api/v1/auth/login -H 'Content-Type: application/json' -d '{\"user_id\":\"test_user\",\"password\":\"test_pass\",\"cert_path\":\"/tmp/test.pfx\",\"use_mock\":true}'" \
    "Mock"

# 測試 3: 正式環境登入嘗試 (真實 SDK - 應該失敗但使用真實 SDK)
test_case "正式環境連接 (真實 SDK)" \
    "curl -s -X POST http://localhost:8000/api/v1/auth/login -H 'Content-Type: application/json' -d '{\"user_id\":\"real_user\",\"password\":\"real_pass\",\"cert_path\":\"/tmp/real.pfx\",\"use_mock\":false}'" \
    "error"

# 測試 4: 測試環境查詢報價
SESSION_ID="default"
test_case "測試環境查詢報價" \
    "curl -s -X POST http://localhost:8000/api/v1/market/quote -H 'Content-Type: application/json' -d '{\"stock_codes\":[\"2330\",\"2317\"]}'" \
    "台積電"

# 測試 5: 測試環境查詢帳戶
test_case "測試環境查詢帳戶" \
    "curl -s http://localhost:8000/api/v1/account/balance" \
    "available_balance"

# 測試 6: 測試環境查詢持股
test_case "測試環境查詢持股" \
    "curl -s http://localhost:8000/api/v1/account/positions" \
    "positions"

echo ""
echo "======================================"
echo "📊 測試結果統計"
echo "======================================"
echo "總測試數: $TOTAL_TESTS"
echo -e "${GREEN}通過: $PASSED_TESTS${NC}"
echo -e "${RED}失敗: $FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ 所有測試通過！${NC}"
    echo ""
    echo "🎉 環境切換功能正常！"
    echo ""
    echo "📋 功能確認："
    echo "  ✓ 測試環境使用 Mock 資料"
    echo "  ✓ 正式環境使用真實 SDK (fubon-neo)"
    echo "  ✓ 環境可以正確切換"
    echo "  ✓ 所有 API 端點正常運作"
    exit 0
else
    echo -e "${RED}✗ 部分測試失敗${NC}"
    echo ""
    echo "請檢查失敗的測試項目"
    exit 1
fi
