"""
Fubon Broker API Implementation
富邦證券 Neo API 主要實作類別
"""

import logging
from typing import Optional, Dict, List, Any, Callable
from datetime import datetime
from .constants import Action, PriceType, OrderType, OrderCondition, MarketType


logger = logging.getLogger(__name__)


class FubonBroker:
    """
    富邦證券 Neo API 封裝類別
    
    提供完整的證券交易、行情查詢、帳戶管理功能
    """
    
    def __init__(self):
        """初始化 Fubon Broker"""
        self.sdk = None
        self.is_logged_in = False
        self.user_id = None
        self.realtime_initialized = False
        self.mock_mode = False  # Mock 模式標記
        
        # 回調函數存儲
        self.quote_callbacks: Dict[str, List[Callable]] = {}
        self.order_callbacks: List[Callable] = []
        
        logger.info("FubonBroker initialized")
    
    def login(
        self,
        user_id: str,
        password: str,
        cert_path: str,
        person_id: Optional[str] = None,
        cert_pass: str = ''
    ) -> bool:
        """
        登入富邦證券帳戶
        
        Args:
            user_id: 使用者帳號 (會轉為 personal_id)
            password: 密碼
            cert_path: 憑證路徑
            person_id: 身分證字號(選填，與 user_id 同義)
            cert_pass: 憑證密碼(選填)
        
        Returns:
            bool: 登入是否成功
        
        Raises:
            Exception: 登入失敗時拋出異常
        """
        try:
            # 延遲導入以避免未安裝時的錯誤
            try:
                from fubon_neo.sdk import FubonSDK
                self.mock_mode = False
            except ImportError:
                # 使用 Mock 模式
                logger.warning("fubon-neo not installed, using Mock mode")
                self.mock_mode = True
                self.is_logged_in = True
                self.user_id = user_id
                return True
            
            # 使用 person_id 或 user_id (兩者同義)
            personal_id = person_id or user_id
            logger.info(f"Attempting to login with personal_id: {personal_id}")
            
            self.sdk = FubonSDK()
            
            # fubon-neo SDK 使用 personal_id 和 pass (注意不是 password!)
            result = self.sdk.login(
                personal_id,  # 位置參數 1
                password,     # 位置參數 2 (SDK內部叫 pass)
                cert_path,    # 位置參數 3
                cert_pass     # 位置參數 4
            )
            
            if result and result.is_success:
                self.is_logged_in = True
                self.user_id = user_id
                logger.info(f"Successfully logged in as {personal_id}")
                logger.info(f"Accounts: {result.data}")
                return True
            else:
                error_msg = result.message if result else "Unknown error"
                logger.error(f"Login failed: {error_msg}")
                return False
                
        except ImportError:
            logger.error("fubon-neo package not installed. Run: pip install fubon-neo")
            raise Exception("fubon-neo package not installed. Please install it first.")
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise
    
    def logout(self) -> bool:
        """
        登出
        
        Returns:
            bool: 登出是否成功
        """
        try:
            if self.sdk and self.is_logged_in:
                self.sdk.logout()
                self.is_logged_in = False
                self.realtime_initialized = False
                logger.info("Successfully logged out")
                return True
            return False
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return False
    
    def _ensure_logged_in(self):
        """確保已登入，否則拋出異常"""
        if not self.is_logged_in:
            raise Exception("Not logged in. Please call login() first.")
    
    def init_realtime(self) -> bool:
        """
        初始化即時行情功能
        
        Returns:
            bool: 初始化是否成功
        """
        try:
            self._ensure_logged_in()
            
            if not self.realtime_initialized:
                self.sdk.init_realtime()
                self.realtime_initialized = True
                logger.info("Realtime market data initialized")
            
            return True
        except Exception as e:
            logger.error(f"Failed to initialize realtime: {str(e)}")
            raise
    
    # ===== 行情查詢功能 =====
    
    def subscribe_quote(
        self,
        symbol: str,
        callback: Optional[Callable] = None
    ) -> bool:
        """
        訂閱即時報價
        
        Args:
            symbol: 股票代號 (例如: "2330")
            callback: 報價更新時的回調函數
        
        Returns:
            bool: 訂閱是否成功
        """
        try:
            self._ensure_logged_in()
            
            if not self.realtime_initialized:
                self.init_realtime()
            
            # 訂閱報價
            self.sdk.quote.subscribe(symbol)
            
            # 儲存回調函數
            if callback:
                if symbol not in self.quote_callbacks:
                    self.quote_callbacks[symbol] = []
                self.quote_callbacks[symbol].append(callback)
            
            logger.info(f"Subscribed to quote: {symbol}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to subscribe quote {symbol}: {str(e)}")
            raise
    
    def unsubscribe_quote(self, symbol: str) -> bool:
        """
        取消訂閱即時報價
        
        Args:
            symbol: 股票代號
        
        Returns:
            bool: 取消訂閱是否成功
        """
        try:
            self._ensure_logged_in()
            
            self.sdk.quote.unsubscribe(symbol)
            
            # 清除回調函數
            if symbol in self.quote_callbacks:
                del self.quote_callbacks[symbol]
            
            logger.info(f"Unsubscribed from quote: {symbol}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unsubscribe quote {symbol}: {str(e)}")
            raise
    
    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        取得即時報價快照
        
        Args:
            symbol: 股票代號
        
        Returns:
            Dict: 報價資料
        """
        try:
            self._ensure_logged_in()
            
            quote = self.sdk.quote.get_quote(symbol)
            
            logger.debug(f"Retrieved quote for {symbol}")
            return quote
            
        except Exception as e:
            logger.error(f"Failed to get quote {symbol}: {str(e)}")
            raise
    
    def get_historical_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> Optional[List[Dict[str, Any]]]:
        """
        取得歷史行情資料
        
        Args:
            symbol: 股票代號
            start_date: 開始日期 (YYYY-MM-DD)
            end_date: 結束日期 (YYYY-MM-DD)
            interval: 時間間隔 (1d, 1h, 30m, 5m, 1m)
        
        Returns:
            List[Dict]: 歷史資料列表
        """
        try:
            self._ensure_logged_in()
            
            data = self.sdk.market_data.get_historical_data(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                interval=interval
            )
            
            logger.info(f"Retrieved historical data for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to get historical data {symbol}: {str(e)}")
            raise
    
    def get_intraday_data(
        self,
        symbol: str,
        interval: str = "1m"
    ) -> Optional[List[Dict[str, Any]]]:
        """
        取得當日盤中資料
        
        Args:
            symbol: 股票代號
            interval: 時間間隔 (1m, 5m, 15m, 30m, 1h)
        
        Returns:
            List[Dict]: 盤中資料列表
        """
        try:
            self._ensure_logged_in()
            
            data = self.sdk.market_data.get_intraday(
                symbol=symbol,
                interval=interval
            )
            
            logger.debug(f"Retrieved intraday data for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to get intraday data {symbol}: {str(e)}")
            raise
    
    # ===== 下單功能 =====
    
    def place_order(
        self,
        symbol: str,
        action: Action,
        quantity: int,
        price: Optional[float] = None,
        price_type: PriceType = PriceType.LIMIT,
        order_type: OrderType = OrderType.ROD,
        order_condition: OrderCondition = OrderCondition.CASH
    ) -> Optional[Dict[str, Any]]:
        """
        下單
        
        Args:
            symbol: 股票代號
            action: 買賣動作 (Buy/Sell)
            quantity: 數量 (股)
            price: 價格 (限價單必填)
            price_type: 價格類型 (Limit/Market/MarketRange)
            order_type: 委託類型 (ROD/IOC/FOK)
            order_condition: 委託條件 (Cash/Margin/Short)
        
        Returns:
            Dict: 委託結果
        """
        try:
            self._ensure_logged_in()
            
            # 驗證參數
            if price_type == PriceType.LIMIT and price is None:
                raise ValueError("Price is required for limit orders")
            
            # 建立委託參數
            order_params = {
                'stock_no': symbol,
                'action': action.value,
                'quantity': quantity,
                'price_type': price_type.value,
                'order_type': order_type.value,
                'order_condition': order_condition.value
            }
            
            if price is not None:
                order_params['price'] = price
            
            # 送出委託
            order_result = self.sdk.order.place_order(**order_params)
            
            logger.info(f"Order placed: {symbol} {action.value} {quantity}@{price}")
            return order_result
            
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            raise
    
    def cancel_order(self, order_id: str) -> bool:
        """
        取消委託
        
        Args:
            order_id: 委託編號
        
        Returns:
            bool: 取消是否成功
        """
        try:
            self._ensure_logged_in()
            
            result = self.sdk.order.cancel_order(order_id)
            
            logger.info(f"Order cancelled: {order_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to cancel order {order_id}: {str(e)}")
            raise
    
    def modify_order(
        self,
        order_id: str,
        price: Optional[float] = None,
        quantity: Optional[int] = None
    ) -> bool:
        """
        修改委託
        
        Args:
            order_id: 委託編號
            price: 新價格
            quantity: 新數量
        
        Returns:
            bool: 修改是否成功
        """
        try:
            self._ensure_logged_in()
            
            modify_params = {'order_id': order_id}
            
            if price is not None:
                modify_params['price'] = price
            if quantity is not None:
                modify_params['quantity'] = quantity
            
            result = self.sdk.order.modify_order(**modify_params)
            
            logger.info(f"Order modified: {order_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to modify order {order_id}: {str(e)}")
            raise
    
    def get_orders(
        self,
        status: Optional[str] = None,
        symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        查詢委託列表
        
        Args:
            status: 委託狀態篩選 (選填)
            symbol: 股票代號篩選 (選填)
        
        Returns:
            List[Dict]: 委託列表
        """
        try:
            self._ensure_logged_in()
            
            query_params = {}
            if status:
                query_params['status'] = status
            if symbol:
                query_params['symbol'] = symbol
            
            orders = self.sdk.order.get_orders(**query_params)
            
            logger.debug(f"Retrieved orders: {len(orders)} orders")
            return orders
            
        except Exception as e:
            logger.error(f"Failed to get orders: {str(e)}")
            raise
    
    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        查詢特定委託
        
        Args:
            order_id: 委託編號
        
        Returns:
            Dict: 委託資料
        """
        try:
            self._ensure_logged_in()
            
            order = self.sdk.order.get_order(order_id)
            
            logger.debug(f"Retrieved order: {order_id}")
            return order
            
        except Exception as e:
            logger.error(f"Failed to get order {order_id}: {str(e)}")
            raise
    
    # ===== 帳戶管理功能 =====
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        取得帳戶資訊
        
        Returns:
            Dict: 帳戶資訊
        """
        try:
            self._ensure_logged_in()
            
            account_info = self.sdk.get_account()
            
            logger.debug("Retrieved account info")
            return account_info
            
        except Exception as e:
            logger.error(f"Failed to get account info: {str(e)}")
            raise
    
    def get_balance(self) -> Dict[str, Any]:
        """
        取得帳戶餘額
        
        Returns:
            Dict: 餘額資訊
        """
        try:
            self._ensure_logged_in()
            
            balance = self.sdk.account.get_balance()
            
            logger.debug("Retrieved account balance")
            return balance
            
        except Exception as e:
            logger.error(f"Failed to get balance: {str(e)}")
            raise
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """
        取得持股部位
        
        Returns:
            List[Dict]: 持股列表
        """
        try:
            self._ensure_logged_in()
            
            positions = self.sdk.account.get_positions()
            
            logger.debug(f"Retrieved positions: {len(positions)} positions")
            return positions
            
        except Exception as e:
            logger.error(f"Failed to get positions: {str(e)}")
            raise
    
    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        取得特定股票持股
        
        Args:
            symbol: 股票代號
        
        Returns:
            Dict: 持股資訊
        """
        try:
            self._ensure_logged_in()
            
            position = self.sdk.account.get_position(symbol)
            
            logger.debug(f"Retrieved position for {symbol}")
            return position
            
        except Exception as e:
            logger.error(f"Failed to get position {symbol}: {str(e)}")
            raise
    
    def get_settlements(self) -> List[Dict[str, Any]]:
        """
        取得交割資訊
        
        Returns:
            List[Dict]: 交割資訊列表
        """
        try:
            self._ensure_logged_in()
            
            settlements = self.sdk.account.get_settlements()
            
            logger.debug(f"Retrieved settlements: {len(settlements)} records")
            return settlements
            
        except Exception as e:
            logger.error(f"Failed to get settlements: {str(e)}")
            raise
    
    def get_profit_loss(self) -> Dict[str, Any]:
        """
        取得損益資訊
        
        Returns:
            Dict: 損益資訊
        """
        try:
            self._ensure_logged_in()
            
            pnl = self.sdk.account.get_profit_loss()
            
            logger.debug("Retrieved profit/loss info")
            return pnl
            
        except Exception as e:
            logger.error(f"Failed to get profit/loss: {str(e)}")
            raise
    
    # ===== 進階功能 =====
    
    def get_margin_info(self) -> Dict[str, Any]:
        """
        取得融資融券資訊
        
        Returns:
            Dict: 融資融券資訊
        """
        try:
            self._ensure_logged_in()
            
            margin_info = self.sdk.account.get_margin_info()
            
            logger.debug("Retrieved margin info")
            return margin_info
            
        except Exception as e:
            logger.error(f"Failed to get margin info: {str(e)}")
            raise
    
    def get_buying_power(self) -> float:
        """
        取得可用購買力
        
        Returns:
            float: 可用購買力金額
        """
        try:
            self._ensure_logged_in()
            
            buying_power = self.sdk.account.get_buying_power()
            
            logger.debug(f"Retrieved buying power: {buying_power}")
            return buying_power
            
        except Exception as e:
            logger.error(f"Failed to get buying power: {str(e)}")
            raise
    
    def set_order_callback(self, callback: Callable) -> None:
        """
        設定委託狀態變更回調函數
        
        Args:
            callback: 回調函數
        """
        self.order_callbacks.append(callback)
        
        if self.sdk:
            self.sdk.order.set_callback(callback)
        
        logger.info("Order callback set")
    
    def __enter__(self):
        """Context manager 進入"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 退出"""
        self.logout()
        return False
    
    def __repr__(self):
        """物件字串表示"""
        return f"FubonBroker(user_id={self.user_id}, logged_in={self.is_logged_in})"
