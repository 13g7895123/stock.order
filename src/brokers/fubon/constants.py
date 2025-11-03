"""
Constants for Fubon Neo API
富邦證券 API 常數定義
"""

from enum import Enum


class Action(str, Enum):
    """交易動作"""
    BUY = "Buy"
    SELL = "Sell"


class PriceType(str, Enum):
    """價格類型"""
    LIMIT = "Limit"  # 限價
    MARKET = "Market"  # 市價
    MARKET_RANGE = "MarketRange"  # 範圍市價


class OrderType(str, Enum):
    """委託類型"""
    ROD = "ROD"  # Rest of Day - 當日有效
    IOC = "IOC"  # Immediate or Cancel - 立即成交否則取消
    FOK = "FOK"  # Fill or Kill - 全部成交否則取消


class OrderCondition(str, Enum):
    """委託條件"""
    CASH = "Cash"  # 現股
    MARGIN = "Margin"  # 融資
    SHORT = "Short"  # 融券


class MarketType(str, Enum):
    """市場類型"""
    STOCK = "Stock"  # 證券
    FUTURES = "Futures"  # 期貨
    OPTIONS = "Options"  # 選擇權


class OrderStatus(str, Enum):
    """委託狀態"""
    PENDING = "Pending"  # 等待中
    SUBMITTED = "Submitted"  # 已送出
    FILLED = "Filled"  # 已成交
    PARTIALLY_FILLED = "PartiallyFilled"  # 部分成交
    CANCELLED = "Cancelled"  # 已取消
    REJECTED = "Rejected"  # 已拒絕
    FAILED = "Failed"  # 失敗
