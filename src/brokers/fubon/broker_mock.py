"""
Mock Fubon Broker for Testing
模擬富邦券商用於測試 API
"""

import logging
from typing import Optional, Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class FubonBroker:
    """
    富邦證券 Mock 版本 (用於測試)
    實際使用時請替換為真實的 fubon-neo SDK
    """
    
    def __init__(self):
        """初始化 Mock Broker"""
        self.is_logged_in = False
        self.user_id = None
        self.last_error: Optional[str] = None
        logger.info("Mock FubonBroker initialized")
    
    def login(self, user_id: str, password: str, cert_path: str, person_id: Optional[str] = None) -> bool:
        """模擬登入"""
        logger.info(f"Mock login with user_id: {user_id}")
        self.is_logged_in = True
        self.user_id = user_id
        self.last_error = None
        return True
    
    def logout(self) -> bool:
        """模擬登出"""
        logger.info("Mock logout")
        self.is_logged_in = False
        self.user_id = None
        self.last_error = None
        return True
    
    # 市場行情功能
    def subscribe_quote(self, stock_code: str) -> bool:
        """模擬訂閱報價"""
        logger.info(f"Mock subscribe quote: {stock_code}")
        return True
    
    def unsubscribe_quote(self, stock_code: str) -> bool:
        """模擬取消訂閱"""
        logger.info(f"Mock unsubscribe quote: {stock_code}")
        return True
    
    def get_quote(self, stock_code: str) -> Optional[Dict]:
        """模擬取得報價"""
        return {
            "stock_code": stock_code,
            "price": 600.0,
            "volume": 1000,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_historical_data(self, stock_code: str, interval: str = "D", 
                          start_date: Optional[str] = None, 
                          end_date: Optional[str] = None) -> Optional[List[Dict]]:
        """模擬取得歷史資料"""
        return [
            {
                "date": "2024-01-01",
                "open": 590.0,
                "high": 610.0,
                "low": 585.0,
                "close": 600.0,
                "volume": 10000
            }
        ]
    
    def get_intraday_data(self, stock_code: str) -> Optional[Dict]:
        """模擬取得盤中資料"""
        return {
            "stock_code": stock_code,
            "current_price": 600.0,
            "high": 610.0,
            "low": 590.0,
            "volume": 5000
        }
    
    # 交易下單功能
    def place_order(self, stock_code: str, action: str, price: Optional[float], 
                   quantity: int, price_type: str = "LMT", 
                   order_type: str = "ROD", order_condition: str = "Cash") -> Dict:
        """模擬下單"""
        logger.warning(f"Mock place order: {action} {stock_code} @ {price} x {quantity}")
        return {
            "success": True,
            "order_id": f"MOCK_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "message": "Mock order placed successfully"
        }
    
    def cancel_order(self, order_id: str) -> Dict:
        """模擬取消委託"""
        logger.info(f"Mock cancel order: {order_id}")
        return {
            "success": True,
            "message": "Mock order cancelled"
        }
    
    def modify_order(self, order_id: str, price: Optional[float] = None, 
                    quantity: Optional[int] = None) -> Dict:
        """模擬修改委託"""
        logger.info(f"Mock modify order: {order_id}")
        return {
            "success": True,
            "message": "Mock order modified"
        }
    
    def get_orders(self, status: Optional[str] = None, 
                  stock_code: Optional[str] = None) -> Optional[List[Dict]]:
        """模擬查詢委託"""
        return [
            {
                "order_id": "MOCK_001",
                "stock_code": "2330",
                "action": "Buy",
                "price": 600.0,
                "quantity": 1,
                "status": "filled"
            }
        ]
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """模擬查詢單筆委託"""
        return {
            "order_id": order_id,
            "stock_code": "2330",
            "action": "Buy",
            "price": 600.0,
            "quantity": 1,
            "status": "filled"
        }
    
    # 帳戶管理功能
    def get_account_info(self) -> Optional[Dict]:
        """模擬取得帳戶資訊"""
        return {
            "account_id": self.user_id,
            "account_type": "Mock Account",
            "status": "active"
        }
    
    def get_balance(self) -> Optional[Dict]:
        """模擬取得帳戶餘額"""
        return {
            "balance": 1000000.0,
            "buying_power": 800000.0,
            "available_balance": 800000.0
        }
    
    def get_buying_power(self) -> Optional[float]:
        """模擬取得購買力"""
        return 800000.0
    
    def get_positions(self) -> Optional[List[Dict]]:
        """模擬取得持股"""
        return [
            {
                "stock_code": "2330",
                "stock_name": "台積電",
                "quantity": 10,
                "average_cost": 580.0,
                "current_price": 600.0,
                "market_value": 6000.0,
                "profit_loss": 200.0,
                "profit_loss_pct": 3.45
            },
            {
                "stock_code": "2317",
                "stock_name": "鴻海",
                "quantity": 20,
                "average_cost": 100.0,
                "current_price": 105.0,
                "market_value": 2100.0,
                "profit_loss": 100.0,
                "profit_loss_pct": 5.0
            }
        ]
    
    def get_position(self, stock_code: str) -> Optional[Dict]:
        """模擬取得單一持股"""
        positions = self.get_positions()
        if positions:
            for pos in positions:
                if pos["stock_code"] == stock_code:
                    return pos
        return None
    
    def get_settlements(self) -> Optional[List[Dict]]:
        """模擬取得交割資訊"""
        return [
            {
                "date": "2024-01-03",
                "amount": 600000.0,
                "type": "買進交割"
            }
        ]
    
    def get_profit_loss(self) -> Optional[Dict]:
        """模擬取得損益"""
        return {
            "realized_profit_loss": 50000.0,
            "unrealized_profit_loss": 300.0,
            "total_profit_loss": 50300.0,
            "return_rate": 5.03
        }
    
    def get_margin_info(self) -> Optional[Dict]:
        """模擬取得融資融券資訊"""
        return {
            "margin_limit": 500000.0,
            "margin_used": 0.0,
            "margin_available": 500000.0,
            "short_limit": 200000.0,
            "short_used": 0.0,
            "short_available": 200000.0
        }
