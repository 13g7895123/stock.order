# Python 多券商同步下單系統 - 完整開發計劃

> 建立日期: 2025-10-31
> 專案類型: Web 應用 + Windows 桌面橋接服務
> 主要語言: Python (後端) + TypeScript/React (前端) + Python (Windows 橋接)

---

## 目錄

- [專案概述](#專案概述)
- [系統架構](#系統架構)
- [技術棧](#技術棧)
- [開發環境](#開發環境)
- [開發階段](#開發階段)
- [詳細任務清單](#詳細任務清單)
- [資料庫設計](#資料庫設計)
- [API 設計](#api-設計)
- [開發規範](#開發規範)
- [測試策略](#測試策略)
- [部署計劃](#部署計劃)

---

## 專案概述

### 目標
開發一個支援多券商同步下單的 Web 應用系統，使用者可透過單一介面同時向多家券商下單，並即時接收通知。

### 核心功能
1. **多券商管理** - 支援永豐、富邦、玉山等券商
2. **同步下單** - 一次操作向多家券商同時下單
3. **股票驗證** - 自動驗證股票代號有效性
4. **即時通知** - Line Bot + WebSocket 推播
5. **交易記錄** - 完整記錄所有交易歷史
6. **Windows 券商支援** - 透過桌面橋接服務支援群益、凱基等

### 使用者流程
```
使用者登入
  → 設定券商 API 金鑰
  → 選擇要使用的券商
  → 輸入下單資訊 (股票代號、價格、數量)
  → 系統驗證
  → 多券商同步下單
  → 即時通知結果
  → 查看交易記錄
```

---

## 系統架構

### 總體架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                      使用者層                                │
│  Web Browser (React SPA) + Line Bot 通知                    │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                   展示層 (Nginx)                             │
│  - 反向代理                                                  │
│  - SSL 終止                                                  │
│  - 靜態檔案服務                                              │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  API 層 (FastAPI)                            │
│  - RESTful API                                              │
│  - WebSocket Server                                         │
│  - JWT 認證                                                 │
│  - 請求驗證                                                 │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  業務邏輯層                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐       │
│  │ 訂單管理    │  │ 多券商編排    │  │ 驗證服務    │       │
│  └─────────────┘  └──────────────┘  └─────────────┘       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐       │
│  │ 通知服務    │  │ 使用者管理    │  │ 風控模組    │       │
│  └─────────────┘  └──────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  券商適配層                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  直接整合 (跨平台)                                    │  │
│  │  - 永豐證券 (Shioaji)                                │  │
│  │  - 富邦證券 (Neo API)                                │  │
│  │  - 玉山證券 (Fugle API)                              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  代理整合 (透過 Windows 橋接)                         │  │
│  │  - Windows Broker Proxy → 桌面橋接服務               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  資料層                                      │
│  - MariaDB (主資料庫)                                       │
│  - Redis (快取 + 會話 + 訊息佇列)                           │
└─────────────────────────────────────────────────────────────┘

                            ↕ HTTP API
┌─────────────────────────────────────────────────────────────┐
│          Windows 桌面橋接服務 (可選)                         │
│  - Python + PyQt5 桌面應用                                  │
│  - Flask API Server                                         │
│  - 整合 Windows Only 券商 (群益、凱基等)                     │
└─────────────────────────────────────────────────────────────┘
```

### 資料流程

#### 下單流程
```
1. 使用者提交訂單
   ↓
2. API 層接收並驗證 JWT
   ↓
3. 訂單驗證服務
   - 股票代號驗證
   - 價格範圍檢查
   - 數量合理性
   ↓
4. 多券商編排器
   - 並行調用各券商 API
   - 收集執行結果
   ↓
5. 資料庫記錄
   - 訂單主記錄
   - 各券商執行記錄
   ↓
6. 通知發送
   - Line Bot 推播
   - WebSocket 即時通知
   ↓
7. 回傳結果給使用者
```

---

## 技術棧

### 後端 (Web 主系統)

**核心框架**
- **Python 3.11+** - 主要程式語言
- **FastAPI** - Web 框架
- **SQLAlchemy 2.0** - ORM
- **Alembic** - 資料庫遷移
- **Pydantic v2** - 資料驗證

**非同步任務**
- **Celery** - 非同步任務佇列
- **Redis** - 訊息 broker

**資料庫**
- **MariaDB 10.11** - 主資料庫
- **Redis 7** - 快取 + 會話

**券商整合**
- **Shioaji** - 永豐證券 SDK
- **fubon-neo** - 富邦證券 SDK
- **fugle-trade** - 玉山證券 SDK

**通知系統**
- **line-bot-sdk** - Line Bot
- **python-socketio** - WebSocket

**其他工具**
- **httpx** - HTTP 客戶端
- **python-jose** - JWT
- **passlib** - 密碼加密
- **python-dotenv** - 環境變數
- **loguru** - 日誌

### 前端

**核心框架**
- **React 18** - UI 框架
- **TypeScript** - 類型安全
- **Vite** - 建置工具

**UI 框架**
- **TailwindCSS** - CSS 框架
- **shadcn/ui** - UI 元件庫
- **Radix UI** - 無障礙元件

**狀態管理**
- **TanStack Query (React Query)** - 伺服器狀態
- **Zustand** - 客戶端狀態

**表單處理**
- **React Hook Form** - 表單管理
- **Zod** - Schema 驗證

**其他**
- **Axios** - HTTP 客戶端
- **Socket.IO Client** - WebSocket
- **React Router** - 路由

### Windows 桌面橋接服務

**核心**
- **Python 3.11+**
- **PyQt5** - GUI 框架
- **Flask** - API Server

**券商整合**
- **pywin32** - Windows COM 元件
- **群益 API** - 透過 COM
- **凱基 API** - 透過 COM

### 基礎設施

**容器化**
- **Docker** - 容器
- **Docker Compose** - 容器編排

**反向代理**
- **Nginx** - Web 伺服器

**資料庫管理**
- **phpMyAdmin** - MariaDB 管理介面

---

## 開發環境

### 必要軟體

**本機開發**
```bash
# 必須安裝
- Docker Desktop 4.x+
- Docker Compose 2.x+
- Git 2.x+
- Node.js 18+ (前端開發)
- Python 3.11+ (後端開發)
- VSCode 或其他 IDE

# 可選 (Windows 橋接服務開發)
- Python 3.11+ (Windows)
- PyQt5
```

### 環境設定

**後端開發環境**
```bash
# 建立虛擬環境
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 開發工具
```

**前端開發環境**
```bash
cd frontend
npm install
```

### IDE 設定

**VSCode 推薦擴充套件**
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-azuretools.vscode-docker"
  ]
}
```

---

## 開發階段

### Phase 1: 環境建置與基礎架構 (1-2週)

**目標**: 建立完整的開發環境和專案骨架

#### 任務清單
- [ ] 建立專案目錄結構
- [ ] 設定 Docker Compose 環境
  - [ ] MariaDB 容器設定
  - [ ] Redis 容器設定
  - [ ] phpMyAdmin 設定
  - [ ] Nginx 設定
- [ ] 後端基礎框架
  - [ ] FastAPI 應用初始化
  - [ ] 資料庫連線設定
  - [ ] Alembic 遷移設定
  - [ ] 基礎中介軟體 (CORS, 日誌等)
- [ ] 前端基礎框架
  - [ ] React + Vite 專案初始化
  - [ ] TailwindCSS 設定
  - [ ] 路由設定
  - [ ] API 客戶端設定
- [ ] 環境變數管理
  - [ ] .env 範例檔案
  - [ ] 環境變數載入
- [ ] Git 設定
  - [ ] .gitignore
  - [ ] Git hooks (pre-commit)

#### 檔案結構
```
stock-order-system/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── Makefile                    # 常用指令
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── .env.example
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── brokers/
│   │   ├── notifications/
│   │   ├── validators/
│   │   └── utils/
│   └── tests/
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── .env.example
│   ├── public/
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── hooks/
│       ├── types/
│       └── utils/
│
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
│
└── docs/
    ├── tasks.md           # 本文件
    ├── api-spec.md
    ├── database-schema.md
    └── deployment.md
```

### Phase 2: 跨平台券商整合 (2-3週)

**目標**: 整合永豐、富邦、玉山三家券商 API

#### 2.1 券商適配器基底設計

**任務**
- [ ] 設計 `BaseBrokerAdapter` 抽象類別
- [ ] 定義統一的介面方法
  - `login()` - 登入
  - `place_order()` - 下單
  - `get_order_status()` - 查詢訂單
  - `cancel_order()` - 取消訂單
  - `get_positions()` - 查詢持股
- [ ] 錯誤處理基底類別
- [ ] 重試機制設計
- [ ] 日誌記錄標準

**程式碼範例**
```python
# backend/app/brokers/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum

class BrokerName(str, Enum):
    SINOPAC = "sinopac"
    FUBON = "fubon"
    ESUN = "esun"
    CAPITAL = "capital"
    KGI = "kgi"

class OrderAction(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIAL_FILLED = "partial_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    FAILED = "failed"

class BaseBrokerAdapter(ABC):
    """券商適配器基底類別"""

    def __init__(self, broker_name: BrokerName):
        self.broker_name = broker_name
        self.is_connected = False

    @abstractmethod
    async def login(self, credentials: Dict[str, str]) -> bool:
        """登入券商

        Args:
            credentials: 登入憑證 (api_key, secret_key 等)

        Returns:
            bool: 登入是否成功
        """
        pass

    @abstractmethod
    async def logout(self) -> bool:
        """登出券商"""
        pass

    @abstractmethod
    async def place_order(
        self,
        stock_code: str,
        action: OrderAction,
        price: float,
        quantity: int,
        order_type: str = "ROD"
    ) -> Dict[str, Any]:
        """下單

        Returns:
            {
                "success": bool,
                "broker_order_id": str,
                "message": str,
                "timestamp": datetime
            }
        """
        pass

    @abstractmethod
    async def get_order_status(self, broker_order_id: str) -> Dict[str, Any]:
        """查詢訂單狀態"""
        pass

    @abstractmethod
    async def cancel_order(self, broker_order_id: str) -> bool:
        """取消訂單"""
        pass

    @abstractmethod
    async def get_positions(self) -> list[Dict[str, Any]]:
        """查詢持股"""
        pass

    async def health_check(self) -> bool:
        """健康檢查"""
        return self.is_connected
```

#### 2.2 永豐證券 (Shioaji) 整合

**任務**
- [ ] 安裝 Shioaji SDK
- [ ] 實作 `SinoPacAdapter`
- [ ] 登入測試
- [ ] 下單測試 (測試環境)
- [ ] 錯誤處理
- [ ] 單元測試

**實作重點**
```python
# backend/app/brokers/sinopac.py
import shioaji as sj
from .base import BaseBrokerAdapter, BrokerName, OrderAction

class SinoPacAdapter(BaseBrokerAdapter):
    def __init__(self):
        super().__init__(BrokerName.SINOPAC)
        self.api = sj.Shioaji()

    async def login(self, credentials: Dict[str, str]) -> bool:
        try:
            self.api.login(
                api_key=credentials["api_key"],
                secret_key=credentials["secret_key"]
            )
            self.is_connected = True
            return True
        except Exception as e:
            # 錯誤處理
            self.is_connected = False
            return False

    async def place_order(self, stock_code, action, price, quantity, order_type):
        # 取得合約
        contract = self.api.Contracts.Stocks[stock_code]

        # 建立訂單
        order = self.api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Buy if action == OrderAction.BUY else sj.constant.Action.Sell,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.OrderType.ROD
        )

        # 執行下單
        trade = self.api.place_order(contract, order)

        return {
            "success": True,
            "broker_order_id": trade.order.order_id,
            "message": "下單成功",
            "timestamp": datetime.now()
        }
```

#### 2.3 富邦證券 (Neo API) 整合

**任務**
- [ ] 安裝 fubon-neo SDK
- [ ] 實作 `FubonAdapter`
- [ ] 測試整合
- [ ] 單元測試

#### 2.4 玉山證券 (Fugle API) 整合

**任務**
- [ ] 安裝 fugle-trade SDK
- [ ] 實作 `ESunAdapter`
- [ ] 測試整合
- [ ] 單元測試

#### 2.5 券商工廠模式

**任務**
- [ ] 實作 `BrokerFactory`
- [ ] 根據名稱建立對應的適配器
- [ ] 設定管理

```python
# backend/app/brokers/factory.py
from .base import BrokerName, BaseBrokerAdapter
from .sinopac import SinoPacAdapter
from .fubon import FubonAdapter
from .esun import ESunAdapter

class BrokerFactory:
    @staticmethod
    def create_broker(broker_name: BrokerName) -> BaseBrokerAdapter:
        """根據券商名稱建立適配器"""
        if broker_name == BrokerName.SINOPAC:
            return SinoPacAdapter()
        elif broker_name == BrokerName.FUBON:
            return FubonAdapter()
        elif broker_name == BrokerName.ESUN:
            return ESunAdapter()
        else:
            raise ValueError(f"不支援的券商: {broker_name}")
```

### Phase 3: 核心功能開發 (2-3週)

**目標**: 實作訂單管理、驗證、多券商編排等核心業務邏輯

#### 3.1 資料庫模型

**任務**
- [ ] 設計資料表結構
- [ ] 建立 SQLAlchemy 模型
- [ ] Alembic 遷移腳本
- [ ] 索引優化

**資料模型**
```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# backend/app/models/broker_config.py
class BrokerConfig(Base):
    __tablename__ = "broker_configs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_name = Column(String(50), nullable=False)
    api_key_encrypted = Column(String(500), nullable=False)
    api_secret_encrypted = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 關聯
    user = relationship("User", back_populates="broker_configs")

# backend/app/models/order.py
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_code = Column(String(10), nullable=False, index=True)
    stock_name = Column(String(100))
    action = Column(String(10), nullable=False)  # buy/sell
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_type = Column(String(10), default="ROD")
    status = Column(String(20), default="pending", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 關聯
    user = relationship("User", back_populates="orders")
    executions = relationship("OrderExecution", back_populates="order")

# backend/app/models/order_execution.py
class OrderExecution(Base):
    __tablename__ = "order_executions"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    broker_name = Column(String(50), nullable=False)
    broker_order_id = Column(String(100))
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    executed_at = Column(DateTime(timezone=True), server_default=func.now())

    # 關聯
    order = relationship("Order", back_populates="executions")
```

#### 3.2 股票驗證服務

**任務**
- [ ] 股票代號格式驗證
- [ ] 股票存在性驗證 (證交所 API)
- [ ] 快取驗證結果 (Redis)
- [ ] 驗證規則配置

```python
# backend/app/validators/stock_validator.py
import re
import httpx
from typing import Optional
from app.core.cache import redis_client

class StockValidator:
    """股票代號驗證器"""

    STOCK_CODE_PATTERN = re.compile(r'^\d{4}$')
    CACHE_TTL = 3600  # 1小時

    async def validate_stock_code(self, stock_code: str) -> tuple[bool, Optional[str]]:
        """驗證股票代號

        Returns:
            (is_valid, error_message)
        """
        # 格式驗證
        if not self.STOCK_CODE_PATTERN.match(stock_code):
            return False, "股票代號格式錯誤，應為4位數字"

        # 快取檢查
        cache_key = f"stock:valid:{stock_code}"
        cached = await redis_client.get(cache_key)
        if cached:
            return True, None

        # 呼叫證交所 API 驗證
        is_valid = await self._check_stock_exists(stock_code)
        if is_valid:
            # 快取結果
            await redis_client.setex(cache_key, self.CACHE_TTL, "1")
            return True, None
        else:
            return False, f"股票代號 {stock_code} 不存在"

    async def _check_stock_exists(self, stock_code: str) -> bool:
        """查詢證交所確認股票是否存在"""
        try:
            # 證交所 OpenAPI
            url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
                stocks = response.json()
                return any(s["Code"] == stock_code for s in stocks)
        except:
            # 如果 API 失敗，預設通過驗證
            return True
```

#### 3.3 訂單服務

**任務**
- [ ] 訂單建立邏輯
- [ ] 訂單查詢
- [ ] 訂單狀態更新
- [ ] 交易記錄查詢

```python
# backend/app/services/order_service.py
from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    async def create_order(
        self,
        user_id: int,
        order_data: OrderCreate
    ) -> Order:
        """建立訂單"""
        order = Order(
            user_id=user_id,
            stock_code=order_data.stock_code,
            action=order_data.action,
            price=order_data.price,
            quantity=order_data.quantity,
            order_type=order_data.order_type,
            status="pending"
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    async def get_user_orders(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Order]:
        """查詢使用者訂單"""
        return self.db.query(Order)\
            .filter(Order.user_id == user_id)\
            .order_by(Order.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
```

#### 3.4 多券商訂單編排器

**任務**
- [ ] 並行執行多券商下單
- [ ] 結果收集與彙整
- [ ] 錯誤處理與重試
- [ ] 部分成功處理

```python
# backend/app/services/orchestrator.py
import asyncio
from typing import List, Dict, Any
from app.brokers.factory import BrokerFactory
from app.models.order import Order
from app.models.order_execution import OrderExecution

class OrderOrchestrator:
    """多券商訂單編排器"""

    def __init__(self, db: Session):
        self.db = db
        self.broker_factory = BrokerFactory()

    async def execute_multi_broker_order(
        self,
        order: Order,
        broker_configs: List[BrokerConfig]
    ) -> Dict[str, Any]:
        """執行多券商下單

        Args:
            order: 訂單物件
            broker_configs: 使用者的券商設定列表

        Returns:
            {
                "order_id": int,
                "total_brokers": int,
                "success_count": int,
                "failed_count": int,
                "results": [...]
            }
        """
        # 更新訂單狀態
        order.status = "processing"
        self.db.commit()

        # 建立並行任務
        tasks = []
        for config in broker_configs:
            task = self._execute_single_broker_order(order, config)
            tasks.append(task)

        # 並行執行
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 統計結果
        success_count = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
        failed_count = len(results) - success_count

        # 更新訂單狀態
        if success_count > 0:
            order.status = "completed" if failed_count == 0 else "partial_completed"
        else:
            order.status = "failed"
        self.db.commit()

        return {
            "order_id": order.id,
            "total_brokers": len(broker_configs),
            "success_count": success_count,
            "failed_count": failed_count,
            "results": results
        }

    async def _execute_single_broker_order(
        self,
        order: Order,
        broker_config: BrokerConfig
    ) -> Dict[str, Any]:
        """執行單一券商下單"""
        execution = OrderExecution(
            order_id=order.id,
            broker_name=broker_config.broker_name,
            status="pending"
        )
        self.db.add(execution)
        self.db.commit()

        try:
            # 建立券商適配器
            adapter = self.broker_factory.create_broker(broker_config.broker_name)

            # 登入
            credentials = {
                "api_key": decrypt(broker_config.api_key_encrypted),
                "secret_key": decrypt(broker_config.api_secret_encrypted)
            }
            await adapter.login(credentials)

            # 下單
            result = await adapter.place_order(
                stock_code=order.stock_code,
                action=order.action,
                price=float(order.price),
                quantity=order.quantity,
                order_type=order.order_type
            )

            # 更新執行記錄
            execution.status = "success"
            execution.broker_order_id = result.get("broker_order_id")
            self.db.commit()

            return result

        except Exception as e:
            # 錯誤處理
            execution.status = "failed"
            execution.error_message = str(e)
            self.db.commit()

            return {
                "success": False,
                "broker_name": broker_config.broker_name,
                "error": str(e)
            }
```

#### 3.5 API 端點

**任務**
- [ ] 訂單 CRUD API
- [ ] 券商設定 API
- [ ] 驗證 API
- [ ] 查詢 API

```python
# backend/app/api/v1/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.services.order_service import OrderService
from app.services.orchestrator import OrderOrchestrator
from app.validators.stock_validator import StockValidator
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """建立訂單並執行多券商下單"""

    # 驗證股票代號
    validator = StockValidator()
    is_valid, error_msg = await validator.validate_stock_code(order_data.stock_code)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # 建立訂單
    order_service = OrderService(db)
    order = await order_service.create_order(current_user.id, order_data)

    # 取得使用者的券商設定
    broker_configs = db.query(BrokerConfig)\
        .filter(BrokerConfig.user_id == current_user.id)\
        .filter(BrokerConfig.is_active == True)\
        .all()

    if not broker_configs:
        raise HTTPException(status_code=400, detail="尚未設定任何券商")

    # 執行多券商下單
    orchestrator = OrderOrchestrator(db)
    result = await orchestrator.execute_multi_broker_order(order, broker_configs)

    # 發送通知 (背景任務)
    # background_tasks.add_task(send_notifications, order, result)

    return {
        "order": order,
        "execution_result": result
    }

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """查詢訂單列表"""
    order_service = OrderService(db)
    orders = await order_service.get_user_orders(
        current_user.id,
        skip=skip,
        limit=limit
    )
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """查詢單一訂單"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="訂單不存在")

    return order
```

### Phase 4: 通知系統 (1週)

**目標**: 整合 Line Bot 和 WebSocket 即時推播

#### 4.1 Line Bot 整合

**任務**
- [ ] Line Bot 設定 (Messaging API)
- [ ] Webhook 處理
- [ ] 訊息範本設計
- [ ] 推播服務實作

```python
# backend/app/notifications/line_bot.py
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, FlexSendMessage
from app.core.config import settings

class LineNotificationService:
    def __init__(self):
        self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

    async def send_order_notification(
        self,
        user_line_id: str,
        order: Order,
        execution_result: Dict[str, Any]
    ):
        """發送訂單通知"""

        # 建立通知訊息
        message = self._create_order_message(order, execution_result)

        try:
            self.line_bot_api.push_message(user_line_id, message)
        except Exception as e:
            # 錯誤處理
            logger.error(f"Line 推播失敗: {e}")

    def _create_order_message(
        self,
        order: Order,
        result: Dict[str, Any]
    ) -> TextSendMessage:
        """建立訂單通知訊息"""

        # 格式化訊息
        action_text = "買進" if order.action == "buy" else "賣出"

        message_lines = [
            "📊 下單結果通知",
            "",
            f"股票: {order.stock_code} {order.stock_name or ''}",
            f"動作: {action_text}",
            f"價格: ${order.price}",
            f"數量: {order.quantity} 張",
            "",
            "執行結果:"
        ]

        # 各券商結果
        for broker_result in result.get("results", []):
            broker_name = broker_result.get("broker_name", "未知")
            if broker_result.get("success"):
                order_id = broker_result.get("broker_order_id", "")
                message_lines.append(f"✅ {broker_name}: 成功 ({order_id})")
            else:
                error = broker_result.get("error", "未知錯誤")
                message_lines.append(f"❌ {broker_name}: 失敗 ({error})")

        message_lines.append("")
        message_lines.append(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        message_text = "\n".join(message_lines)

        return TextSendMessage(text=message_text)
```

#### 4.2 WebSocket 即時推播

**任務**
- [ ] WebSocket 伺服器設定
- [ ] 客戶端連線管理
- [ ] 訂單狀態推播
- [ ] 前端 WebSocket 客戶端

```python
# backend/app/api/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

class ConnectionManager:
    """WebSocket 連線管理器"""

    def __init__(self):
        # user_id -> Set[WebSocket]
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """建立連線"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        """斷開連線"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)

    async def send_personal_message(
        self,
        message: dict,
        user_id: int
    ):
        """發送個人訊息"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/orders")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str
):
    """WebSocket 端點"""
    # 驗證 token
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=4001)
        return

    await manager.connect(websocket, user.id)

    try:
        while True:
            # 接收客戶端訊息 (心跳等)
            data = await websocket.receive_text()

            # 處理訊息
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)

# 使用範例: 發送訂單更新
async def notify_order_update(user_id: int, order: Order, result: dict):
    """通知訂單更新"""
    message = {
        "type": "order_update",
        "order_id": order.id,
        "status": order.status,
        "result": result
    }
    await manager.send_personal_message(message, user_id)
```

### Phase 5: Windows 桌面橋接服務 (2週)

**目標**: 開發 Python 桌面應用，支援 Windows Only 券商

#### 5.1 桌面應用框架

**任務**
- [ ] PyQt5 專案建立
- [ ] 主視窗設計
- [ ] 系統托盤圖示
- [ ] 自動啟動設定

**檔案結構**
```
windows-broker-bridge/
├── requirements.txt
├── main.py                     # 主程式
├── config.ini                  # 設定檔
├── app/
│   ├── __init__.py
│   ├── gui/                    # GUI 介面
│   │   ├── main_window.py
│   │   ├── broker_config_dialog.py
│   │   └── log_viewer.py
│   ├── api/                    # API Server
│   │   ├── server.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── brokers/                # 券商適配器
│   │   ├── base.py
│   │   ├── capital.py          # 群益
│   │   └── kgi.py              # 凱基
│   └── utils/
│       ├── logger.py
│       └── config.py
└── resources/
    └── icon.ico
```

#### 5.2 API Server

**任務**
- [ ] Flask API Server
- [ ] 健康檢查端點
- [ ] 訂單處理端點
- [ ] 券商管理端點

```python
# windows-broker-bridge/app/api/server.py
from flask import Flask, request, jsonify
from app.brokers.factory import WindowsBrokerFactory

app = Flask(__name__)
broker_factory = WindowsBrokerFactory()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "brokers": broker_factory.get_active_brokers()
    })

@app.route('/api/orders', methods=['POST'])
def place_order():
    """下單"""
    data = request.json

    broker_name = data.get("broker")
    stock_code = data.get("stock_code")
    action = data.get("action")
    price = data.get("price")
    quantity = data.get("quantity")

    try:
        # 取得券商適配器
        broker = broker_factory.get_broker(broker_name)

        # 執行下單
        result = broker.place_order(
            stock_code=stock_code,
            action=action,
            price=price,
            quantity=quantity
        )

        return jsonify({
            "success": True,
            "broker_order_id": result["order_id"],
            "message": "下單成功"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

def start_api_server(host='127.0.0.1', port=5000):
    """啟動 API Server"""
    app.run(host=host, port=port, threaded=True)
```

#### 5.3 群益券商整合

**任務**
- [ ] COM 元件載入
- [ ] 登入實作
- [ ] 下單實作
- [ ] 錯誤處理

```python
# windows-broker-bridge/app/brokers/capital.py
import win32com.client
from .base import WindowsBrokerBase

class CapitalBroker(WindowsBrokerBase):
    """群益證券適配器"""

    def __init__(self):
        super().__init__("capital")
        self.skCenter = None
        self.skOrder = None

    def initialize(self):
        """初始化 COM 元件"""
        try:
            self.skCenter = win32com.client.Dispatch("SKCOMLib.SKCenterLib")
            self.skOrder = win32com.client.Dispatch("SKCOMLib.SKOrderLib")
            return True
        except Exception as e:
            self.logger.error(f"群益 API 初始化失敗: {e}")
            return False

    def login(self, user_id: str, password: str):
        """登入"""
        try:
            result = self.skCenter.SKCenterLib_Login(user_id, password)
            if result == 0:
                self.is_connected = True
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"群益登入失敗: {e}")
            return False

    def place_order(
        self,
        stock_code: str,
        action: str,
        price: float,
        quantity: int
    ) -> dict:
        """下單"""
        if not self.is_connected:
            raise Exception("尚未登入")

        try:
            # 群益下單邏輯
            # ... (根據群益 API 文件實作)

            return {
                "success": True,
                "order_id": "CAPITAL_ORDER_ID",
                "message": "下單成功"
            }

        except Exception as e:
            raise Exception(f"群益下單失敗: {e}")
```

#### 5.4 GUI 介面

**任務**
- [ ] 主視窗
- [ ] 券商設定對話框
- [ ] 日誌檢視器
- [ ] 系統設定

```python
# windows-broker-bridge/app/gui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QSystemTrayIcon
)
from PyQt5.QtCore import QThread, pyqtSignal
from app.api.server import start_api_server

class APIServerThread(QThread):
    """API Server 執行緒"""
    def run(self):
        start_api_server(host='127.0.0.1', port=5000)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.api_thread = None

    def init_ui(self):
        """初始化介面"""
        self.setWindowTitle("券商橋接服務")
        self.setGeometry(100, 100, 800, 600)

        # 中央 Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # 狀態面板
        status_label = QLabel("服務狀態: 未啟動")
        layout.addWidget(status_label)

        # 啟動/停止按鈕
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("啟動服務")
        self.stop_btn = QPushButton("停止服務")
        self.start_btn.clicked.connect(self.start_service)
        self.stop_btn.clicked.connect(self.stop_service)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        # 日誌區域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        central_widget.setLayout(layout)

    def start_service(self):
        """啟動服務"""
        self.api_thread = APIServerThread()
        self.api_thread.start()
        self.log_text.append("API Server 已啟動於 http://localhost:5000")

    def stop_service(self):
        """停止服務"""
        if self.api_thread:
            self.api_thread.terminate()
            self.log_text.append("API Server 已停止")
```

### Phase 6: 前端開發 (2-3週)

**目標**: 建立 React 使用者介面

#### 6.1 專案結構與路由

**任務**
- [ ] React Router 設定
- [ ] 佈局元件
- [ ] 導航選單
- [ ] 認證保護路由

```typescript
// frontend/src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/Layout';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { OrderPage } from './pages/OrderPage';
import { HistoryPage } from './pages/HistoryPage';
import { SettingsPage } from './pages/SettingsPage';
import { ProtectedRoute } from './components/ProtectedRoute';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/order" element={<OrderPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
```

#### 6.2 下單表單

**任務**
- [ ] 表單設計
- [ ] 即時驗證
- [ ] 券商選擇
- [ ] 送出處理

```typescript
// frontend/src/components/OrderForm/OrderForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCreateOrder } from '@/hooks/useOrders';

const orderSchema = z.object({
  stock_code: z.string().regex(/^\d{4}$/, '請輸入4位數股票代號'),
  action: z.enum(['buy', 'sell']),
  price: z.number().positive('價格必須大於0'),
  quantity: z.number().int().positive('數量必須大於0'),
  order_type: z.enum(['ROD', 'IOC', 'FOK']),
  brokers: z.array(z.string()).min(1, '請至少選擇一家券商')
});

type OrderFormData = z.infer<typeof orderSchema>;

export function OrderForm() {
  const { mutate: createOrder, isLoading } = useCreateOrder();

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<OrderFormData>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      action: 'buy',
      order_type: 'ROD',
      brokers: []
    }
  });

  const onSubmit = (data: OrderFormData) => {
    createOrder(data, {
      onSuccess: () => {
        // 成功處理
        toast.success('下單成功！');
      },
      onError: (error) => {
        // 錯誤處理
        toast.error(`下單失敗: ${error.message}`);
      }
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* 股票代號 */}
      <div>
        <label>股票代號</label>
        <input
          {...register('stock_code')}
          placeholder="2330"
          className="w-full px-3 py-2 border rounded"
        />
        {errors.stock_code && (
          <p className="text-red-500">{errors.stock_code.message}</p>
        )}
      </div>

      {/* 買賣動作 */}
      <div>
        <label>動作</label>
        <select {...register('action')} className="w-full px-3 py-2 border rounded">
          <option value="buy">買進</option>
          <option value="sell">賣出</option>
        </select>
      </div>

      {/* 價格 */}
      <div>
        <label>價格</label>
        <input
          type="number"
          step="0.01"
          {...register('price', { valueAsNumber: true })}
          className="w-full px-3 py-2 border rounded"
        />
        {errors.price && (
          <p className="text-red-500">{errors.price.message}</p>
        )}
      </div>

      {/* 數量 */}
      <div>
        <label>數量</label>
        <input
          type="number"
          {...register('quantity', { valueAsNumber: true })}
          className="w-full px-3 py-2 border rounded"
        />
        {errors.quantity && (
          <p className="text-red-500">{errors.quantity.message}</p>
        )}
      </div>

      {/* 券商選擇 */}
      <div>
        <label>選擇券商</label>
        <BrokerSelector {...register('brokers')} />
        {errors.brokers && (
          <p className="text-red-500">{errors.brokers.message}</p>
        )}
      </div>

      {/* 送出按鈕 */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        {isLoading ? '處理中...' : '送出訂單'}
      </button>
    </form>
  );
}
```

#### 6.3 交易記錄

**任務**
- [ ] 訂單列表
- [ ] 篩選與排序
- [ ] 詳細資訊展開
- [ ] 分頁

```typescript
// frontend/src/pages/HistoryPage.tsx
import { useOrders } from '@/hooks/useOrders';
import { OrderTable } from '@/components/OrderTable';

export function HistoryPage() {
  const { data: orders, isLoading } = useOrders();

  if (isLoading) return <div>載入中...</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">交易記錄</h1>
      <OrderTable orders={orders} />
    </div>
  );
}
```

#### 6.4 WebSocket 整合

**任務**
- [ ] WebSocket 連線管理
- [ ] 訂單更新監聽
- [ ] 自動重連
- [ ] 即時通知顯示

```typescript
// frontend/src/hooks/useWebSocket.ts
import { useEffect, useRef } from 'react';
import { useQueryClient } from '@tanstack/react-query';

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const queryClient = useQueryClient();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const ws = new WebSocket(`ws://localhost:8000/ws/orders?token=${token}`);

    ws.onopen = () => {
      console.log('WebSocket 已連線');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'order_update') {
        // 更新訂單快取
        queryClient.invalidateQueries(['orders']);

        // 顯示通知
        toast.success(`訂單 ${data.order_id} 狀態更新`);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket 錯誤:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket 已斷線');
      // 自動重連
      setTimeout(() => {
        // 重新連線邏輯
      }, 5000);
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [queryClient]);

  return wsRef;
}
```

### Phase 7: 測試與優化 (1-2週)

**目標**: 完整的測試覆蓋率和效能優化

#### 7.1 後端測試

**任務**
- [ ] 單元測試 (pytest)
- [ ] 整合測試
- [ ] API 測試
- [ ] 覆蓋率報告

```python
# backend/tests/test_order_service.py
import pytest
from app.services.order_service import OrderService
from app.models.order import Order

@pytest.fixture
def order_service(db_session):
    return OrderService(db_session)

def test_create_order(order_service, test_user):
    """測試建立訂單"""
    order_data = {
        "stock_code": "2330",
        "action": "buy",
        "price": 600,
        "quantity": 1
    }

    order = await order_service.create_order(test_user.id, order_data)

    assert order.id is not None
    assert order.stock_code == "2330"
    assert order.status == "pending"

# backend/tests/test_validators.py
def test_stock_code_validation():
    """測試股票代號驗證"""
    validator = StockValidator()

    # 有效代號
    is_valid, _ = await validator.validate_stock_code("2330")
    assert is_valid is True

    # 無效格式
    is_valid, error = await validator.validate_stock_code("ABC")
    assert is_valid is False
    assert "格式錯誤" in error
```

#### 7.2 前端測試

**任務**
- [ ] 元件測試 (Vitest + Testing Library)
- [ ] E2E 測試 (Playwright)
- [ ] 視覺回歸測試

```typescript
// frontend/src/components/OrderForm/OrderForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { OrderForm } from './OrderForm';

describe('OrderForm', () => {
  it('應該正確渲染表單欄位', () => {
    render(<OrderForm />);

    expect(screen.getByLabelText('股票代號')).toBeInTheDocument();
    expect(screen.getByLabelText('價格')).toBeInTheDocument();
    expect(screen.getByLabelText('數量')).toBeInTheDocument();
  });

  it('應該驗證股票代號格式', async () => {
    render(<OrderForm />);

    const stockInput = screen.getByLabelText('股票代號');
    fireEvent.change(stockInput, { target: { value: 'ABC' } });

    const submitBtn = screen.getByText('送出訂單');
    fireEvent.click(submitBtn);

    expect(await screen.findByText(/請輸入4位數/)).toBeInTheDocument();
  });
});
```

#### 7.3 效能優化

**任務**
- [ ] 資料庫查詢優化
- [ ] Redis 快取策略
- [ ] API 回應時間優化
- [ ] 前端 Bundle 優化

### Phase 8: 部署與文件 (1週)

**目標**: 完整的部署流程和使用者文件

#### 8.1 Docker 部署

**任務**
- [ ] 生產環境 docker-compose
- [ ] 環境變數設定
- [ ] 健康檢查
- [ ] 日誌管理

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - ENV=production
      - DATABASE_URL=mysql+pymysql://...
    depends_on:
      - mariadb
      - redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ... 其他服務
```

#### 8.2 文件撰寫

**任務**
- [ ] API 文件 (OpenAPI/Swagger)
- [ ] 使用者手冊
- [ ] 部署指南
- [ ] 開發者指南

---

## 資料庫設計

### Schema 概覽

```sql
-- 使用者表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    line_user_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- 券商設定表
CREATE TABLE broker_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    broker_name VARCHAR(50) NOT NULL,
    api_key_encrypted VARCHAR(500) NOT NULL,
    api_secret_encrypted VARCHAR(500) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_broker (user_id, broker_name),
    UNIQUE KEY uk_user_broker (user_id, broker_name)
);

-- 訂單主表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    stock_code VARCHAR(10) NOT NULL,
    stock_name VARCHAR(100),
    action ENUM('buy', 'sell') NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    order_type VARCHAR(10) DEFAULT 'ROD',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_orders (user_id, created_at DESC),
    INDEX idx_stock_code (stock_code),
    INDEX idx_status (status)
);

-- 訂單執行記錄表
CREATE TABLE order_executions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    broker_name VARCHAR(50) NOT NULL,
    broker_order_id VARCHAR(100),
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    INDEX idx_order_executions (order_id),
    INDEX idx_broker_order (broker_name, broker_order_id)
);

-- 通知記錄表
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    user_id INT NOT NULL,
    notification_type ENUM('line', 'websocket', 'email') NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    sent_at TIMESTAMP NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_notifications (user_id, created_at DESC)
);

-- 稽核日誌表
CREATE TABLE audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id INT,
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_logs (user_id, created_at DESC),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
);
```

---

## API 設計

### 認證相關

```
POST   /api/v1/auth/register      # 註冊
POST   /api/v1/auth/login         # 登入
POST   /api/v1/auth/refresh       # 刷新 token
POST   /api/v1/auth/logout        # 登出
GET    /api/v1/auth/me            # 取得當前使用者
```

### 訂單相關

```
POST   /api/v1/orders             # 建立訂單
GET    /api/v1/orders             # 查詢訂單列表
GET    /api/v1/orders/{id}        # 查詢單一訂單
GET    /api/v1/orders/{id}/executions  # 查詢執行記錄
```

### 券商管理

```
GET    /api/v1/brokers            # 取得已設定券商
POST   /api/v1/brokers            # 新增券商設定
PUT    /api/v1/brokers/{id}       # 更新券商設定
DELETE /api/v1/brokers/{id}       # 刪除券商設定
POST   /api/v1/brokers/{id}/test  # 測試券商連線
```

### 股票驗證

```
GET    /api/v1/stocks/validate/{code}  # 驗證股票代號
GET    /api/v1/stocks/search            # 搜尋股票
```

### WebSocket

```
WS     /ws/orders                 # 訂單即時通知
```

---

## 開發規範

### Git Workflow

```
main (生產環境)
  ├── develop (開發環境)
  │     ├── feature/order-management
  │     ├── feature/line-bot
  │     └── feature/frontend-ui
  └── hotfix/critical-bug
```

**分支命名規則**
- `feature/功能名稱` - 新功能
- `bugfix/問題描述` - Bug 修復
- `hotfix/緊急修復` - 緊急修復
- `refactor/重構範圍` - 重構

**Commit 訊息規範**
```
<type>(<scope>): <subject>

<body>

<footer>
```

類型:
- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文件更新
- `style`: 程式碼格式
- `refactor`: 重構
- `test`: 測試
- `chore`: 建置/工具

範例:
```
feat(order): 實作多券商同步下單功能

- 新增 OrderOrchestrator 類別
- 實作並行下單邏輯
- 新增錯誤處理機制

Closes #123
```

### 程式碼風格

**Python (後端)**
- 遵循 PEP 8
- 使用 Black 格式化
- 使用 Ruff 檢查
- 使用 mypy 型別檢查

```python
# 良好範例
async def create_order(
    user_id: int,
    order_data: OrderCreate,
    db: Session
) -> Order:
    """建立訂單

    Args:
        user_id: 使用者 ID
        order_data: 訂單資料
        db: 資料庫會話

    Returns:
        Order: 建立的訂單物件

    Raises:
        ValueError: 當資料驗證失敗時
    """
    # 實作邏輯
    pass
```

**TypeScript (前端)**
- 遵循 ESLint 規則
- 使用 Prettier 格式化
- 嚴格型別檢查

```typescript
// 良好範例
interface OrderFormData {
  stock_code: string;
  action: 'buy' | 'sell';
  price: number;
  quantity: number;
}

const handleSubmit = async (data: OrderFormData): Promise<void> => {
  // 實作邏輯
};
```

### 測試要求

**測試覆蓋率目標**
- 後端: 80% 以上
- 前端: 70% 以上

**測試類型**
- 單元測試: 所有服務和工具函數
- 整合測試: API 端點
- E2E 測試: 關鍵使用者流程

---

## 測試策略

### 後端測試

**單元測試**
```bash
# 執行所有測試
pytest

# 執行特定測試
pytest tests/test_order_service.py

# 產生覆蓋率報告
pytest --cov=app --cov-report=html
```

**測試資料庫**
使用 SQLite in-memory 或獨立測試資料庫

### 前端測試

**元件測試**
```bash
# 執行測試
npm test

# 監看模式
npm test -- --watch
```

**E2E 測試**
```bash
# 執行 E2E 測試
npx playwright test
```

---

## 部署計劃

### 開發環境

```bash
# 啟動所有服務
docker-compose up -d

# 查看日誌
docker-compose logs -f backend

# 重新建置
docker-compose up -d --build
```

### 生產環境

**需求**
- Docker 和 Docker Compose
- 至少 2GB RAM
- 10GB 硬碟空間

**部署步驟**
```bash
# 1. 複製環境變數
cp .env.example .env
# 編輯 .env 設定正式環境參數

# 2. 建置並啟動
docker-compose -f docker-compose.prod.yml up -d

# 3. 資料庫遷移
docker-compose exec backend alembic upgrade head

# 4. 建立管理員帳號
docker-compose exec backend python scripts/create_admin.py
```

### 監控與維護

**健康檢查**
```bash
curl http://localhost/api/health
```

**日誌查看**
```bash
docker-compose logs -f --tail=100 backend
```

**備份**
```bash
# 資料庫備份
docker-compose exec mariadb mysqldump -u root -p stock_order > backup.sql
```

---

## Makefile 常用指令

```makefile
# Makefile

.PHONY: help install dev build test clean

help:
	@echo "可用指令:"
	@echo "  make install   - 安裝依賴"
	@echo "  make dev       - 啟動開發環境"
	@echo "  make build     - 建置專案"
	@echo "  make test      - 執行測試"
	@echo "  make clean     - 清理環境"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up -d

build:
	docker-compose build

test:
	cd backend && pytest
	cd frontend && npm test

clean:
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules
```

---

## 時程總覽

| 階段 | 時間 | 主要產出 |
|------|------|---------|
| Phase 1: 基礎架構 | 1-2週 | Docker 環境、專案骨架 |
| Phase 2: 券商整合 | 2-3週 | 3家券商適配器 |
| Phase 3: 核心功能 | 2-3週 | 訂單系統、驗證系統 |
| Phase 4: 通知系統 | 1週 | Line Bot、WebSocket |
| Phase 5: Windows 橋接 | 2週 | 桌面應用 |
| Phase 6: 前端開發 | 2-3週 | React 介面 |
| Phase 7: 測試優化 | 1-2週 | 完整測試 |
| Phase 8: 部署文件 | 1週 | 部署與文件 |
| **總計** | **12-17週** | **完整系統** |

---

## 風險管理

### 技術風險

1. **券商 API 變更**
   - 風險: 券商可能更新 API 導致失效
   - 對策: 版本鎖定、定期檢查、適配器模式

2. **效能問題**
   - 風險: 並行下單可能造成效能瓶頸
   - 對策: 非同步處理、佇列機制、負載測試

3. **安全性**
   - 風險: API 金鑰洩露
   - 對策: 加密儲存、HTTPS、JWT、定期稽核

### 進度風險

1. **時程延遲**
   - 風險: 某階段開發超時
   - 對策: 每週檢視進度、MVP 優先、靈活調整

2. **範圍蔓延**
   - 風險: 功能不斷增加
   - 對策: 嚴格需求管理、版本規劃

---

## 下一步行動

### 立即開始

1. ✅ 建立 Git repository
2. ✅ 設定開發環境
3. ✅ 建立專案結構
4. ⬜ 開始 Phase 1 開發

### 本週目標

- [ ] 完成 Docker 環境設定
- [ ] 建立後端 FastAPI 骨架
- [ ] 建立前端 React 骨架
- [ ] 設定 MariaDB 和 Redis

### 本月目標

- [ ] 完成 Phase 1 和 Phase 2
- [ ] 整合至少一家券商 API
- [ ] 建立基本的下單流程

---

## 附錄

### 相關資源

- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [React 官方文件](https://react.dev/)
- [永豐 Shioaji 文件](https://sinotrade.github.io/)
- [富邦 Neo API 文件](https://www.fbs.com.tw/TradeAPI/en/)
- [玉山 Fugle API 文件](https://developer.fugle.tw/)

### 聯絡資訊

- 專案管理: [待填寫]
- 技術支援: [待填寫]
- Bug 回報: GitHub Issues

---

**文件版本**: 1.0.0
**最後更新**: 2025-10-31
**維護者**: [待填寫]
