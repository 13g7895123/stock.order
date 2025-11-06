"""
Pydantic Schemas
API 請求/回應的資料模型
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ==================== 認證相關 ====================

class LoginRequest(BaseModel):
    """登入請求"""
    user_id: str = Field(..., description="使用者帳號")
    password: str = Field(..., description="密碼")
    cert_path: str = Field(..., description="憑證路徑")
    person_id: Optional[str] = Field(None, description="身分證字號")
    use_mock: Optional[bool] = Field(True, description="是否使用 Mock 模式（測試環境為 True，正式環境為 False）")


class LoginResponse(BaseModel):
    """登入回應"""
    success: bool
    message: str
    user_id: Optional[str] = None
    session_id: str = "default"


# ==================== 市場行情相關 ====================

class QuoteRequest(BaseModel):
    """即時報價請求"""
    stock_codes: List[str] = Field(..., description="股票代號列表")


class HistoricalDataRequest(BaseModel):
    """歷史資料請求"""
    stock_code: str = Field(..., description="股票代號")
    interval: str = Field("D", description="時間間隔 (D=日, 1=1分鐘, 5=5分鐘等)")
    start_date: Optional[str] = Field(None, description="開始日期 (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="結束日期 (YYYY-MM-DD)")


class IntradayDataRequest(BaseModel):
    """盤中資料請求"""
    stock_code: str = Field(..., description="股票代號")


# ==================== 交易下單相關 ====================

class ActionEnum(str, Enum):
    """買賣動作"""
    BUY = "Buy"
    SELL = "Sell"


class PriceTypeEnum(str, Enum):
    """價格類型"""
    LIMIT = "LMT"      # 限價
    MARKET = "MKT"     # 市價
    MKP = "MKP"        # 範圍市價


class OrderTypeEnum(str, Enum):
    """委託類型"""
    ROD = "ROD"  # 當日有效
    IOC = "IOC"  # 立即成交否則取消
    FOK = "FOK"  # 全部成交否則取消


class OrderConditionEnum(str, Enum):
    """委託條件"""
    CASH = "Cash"        # 現股
    MARGIN_TRADING = "MarginTrading"  # 融資
    SHORT_SELLING = "ShortSelling"    # 融券


class PlaceOrderRequest(BaseModel):
    """下單請求"""
    stock_code: str = Field(..., description="股票代號", min_length=4, max_length=6)
    action: ActionEnum = Field(..., description="買賣動作")
    price: Optional[float] = Field(None, description="價格 (市價單可不填)", ge=0)
    quantity: int = Field(..., description="數量 (張)", gt=0)
    price_type: PriceTypeEnum = Field(PriceTypeEnum.LIMIT, description="價格類型")
    order_type: OrderTypeEnum = Field(OrderTypeEnum.ROD, description="委託類型")
    order_condition: OrderConditionEnum = Field(OrderConditionEnum.CASH, description="委託條件")
    
    @validator('stock_code')
    def validate_stock_code(cls, v):
        if not v.isdigit():
            raise ValueError('股票代號必須為數字')
        return v


class CancelOrderRequest(BaseModel):
    """取消委託請求"""
    order_id: str = Field(..., description="委託編號")


class ModifyOrderRequest(BaseModel):
    """修改委託請求"""
    order_id: str = Field(..., description="委託編號")
    price: Optional[float] = Field(None, description="新價格")
    quantity: Optional[int] = Field(None, description="新數量")


class OrderStatusEnum(str, Enum):
    """委託狀態"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class QueryOrdersRequest(BaseModel):
    """查詢委託請求"""
    status: Optional[OrderStatusEnum] = Field(None, description="委託狀態")
    stock_code: Optional[str] = Field(None, description="股票代號")
    start_date: Optional[str] = Field(None, description="開始日期")
    end_date: Optional[str] = Field(None, description="結束日期")


# ==================== 帳戶管理相關 ====================

class AccountInfoResponse(BaseModel):
    """帳戶資訊回應"""
    success: bool
    data: Optional[Dict[str, Any]] = None


class BalanceResponse(BaseModel):
    """帳戶餘額回應"""
    success: bool
    balance: Optional[float] = None
    buying_power: Optional[float] = None
    data: Optional[Dict[str, Any]] = None


class PositionsResponse(BaseModel):
    """持股部位回應"""
    success: bool
    positions: Optional[List[Dict[str, Any]]] = None
    total_count: int = 0


class PositionRequest(BaseModel):
    """查詢單一持股請求"""
    stock_code: str = Field(..., description="股票代號")


class SettlementsResponse(BaseModel):
    """交割資訊回應"""
    success: bool
    settlements: Optional[List[Dict[str, Any]]] = None


class ProfitLossResponse(BaseModel):
    """損益資訊回應"""
    success: bool
    profit_loss: Optional[Dict[str, Any]] = None


class MarginResponse(BaseModel):
    """融資融券資訊回應"""
    success: bool
    margin_info: Optional[Dict[str, Any]] = None


# ==================== 通用回應 ====================

class SuccessResponse(BaseModel):
    """成功回應"""
    success: bool = True
    message: str = "Operation successful"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """錯誤回應"""
    success: bool = False
    error: str
    detail: Optional[str] = None
