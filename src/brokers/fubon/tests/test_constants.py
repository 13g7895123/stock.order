"""
單元測試 - 富邦證券常數定義
Unit Tests for Fubon Constants
"""

import unittest
from fubon.constants import (
    Action,
    PriceType,
    OrderType,
    OrderCondition,
    MarketType,
    OrderStatus
)


class TestConstants(unittest.TestCase):
    """常數定義測試"""
    
    def test_action_values(self):
        """測試交易動作值"""
        self.assertEqual(Action.BUY, "Buy")
        self.assertEqual(Action.SELL, "Sell")
    
    def test_price_type_values(self):
        """測試價格類型值"""
        self.assertEqual(PriceType.LIMIT, "Limit")
        self.assertEqual(PriceType.MARKET, "Market")
        self.assertEqual(PriceType.MARKET_RANGE, "MarketRange")
    
    def test_order_type_values(self):
        """測試委託類型值"""
        self.assertEqual(OrderType.ROD, "ROD")
        self.assertEqual(OrderType.IOC, "IOC")
        self.assertEqual(OrderType.FOK, "FOK")
    
    def test_order_condition_values(self):
        """測試委託條件值"""
        self.assertEqual(OrderCondition.CASH, "Cash")
        self.assertEqual(OrderCondition.MARGIN, "Margin")
        self.assertEqual(OrderCondition.SHORT, "Short")
    
    def test_market_type_values(self):
        """測試市場類型值"""
        self.assertEqual(MarketType.STOCK, "Stock")
        self.assertEqual(MarketType.FUTURES, "Futures")
        self.assertEqual(MarketType.OPTIONS, "Options")
    
    def test_order_status_values(self):
        """測試委託狀態值"""
        self.assertEqual(OrderStatus.PENDING, "Pending")
        self.assertEqual(OrderStatus.SUBMITTED, "Submitted")
        self.assertEqual(OrderStatus.FILLED, "Filled")
        self.assertEqual(OrderStatus.PARTIALLY_FILLED, "PartiallyFilled")
        self.assertEqual(OrderStatus.CANCELLED, "Cancelled")
        self.assertEqual(OrderStatus.REJECTED, "Rejected")
        self.assertEqual(OrderStatus.FAILED, "Failed")


if __name__ == '__main__':
    unittest.main()
