"""
單元測試 - 富邦證券 Broker 類別
Unit Tests for Fubon Broker
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from fubon.broker import FubonBroker
from fubon.constants import Action, PriceType, OrderType, OrderCondition


class TestFubonBroker(unittest.TestCase):
    """FubonBroker 類別測試"""
    
    def setUp(self):
        """測試前準備"""
        self.broker = FubonBroker()
    
    def tearDown(self):
        """測試後清理"""
        if self.broker.is_logged_in:
            self.broker.logout()
    
    def test_init(self):
        """測試初始化"""
        self.assertIsNotNone(self.broker)
        self.assertFalse(self.broker.is_logged_in)
        self.assertIsNone(self.broker.sdk)
        self.assertIsNone(self.broker.user_id)
    
    @patch('fubon.broker.FubonSDK')
    def test_login_success(self, mock_sdk_class):
        """測試成功登入"""
        # Mock SDK
        mock_sdk = MagicMock()
        mock_sdk.login.return_value = True
        mock_sdk_class.return_value = mock_sdk
        
        # 執行登入
        result = self.broker.login('test_user', 'test_pass', 'test_cert')
        
        # 驗證
        self.assertTrue(result)
        self.assertTrue(self.broker.is_logged_in)
        self.assertEqual(self.broker.user_id, 'test_user')
        mock_sdk.login.assert_called_once()
    
    @patch('fubon.broker.FubonSDK')
    def test_login_failure(self, mock_sdk_class):
        """測試登入失敗"""
        # Mock SDK
        mock_sdk = MagicMock()
        mock_sdk.login.return_value = False
        mock_sdk_class.return_value = mock_sdk
        
        # 執行登入
        result = self.broker.login('test_user', 'test_pass', 'test_cert')
        
        # 驗證
        self.assertFalse(result)
        self.assertFalse(self.broker.is_logged_in)
    
    def test_ensure_logged_in(self):
        """測試未登入時的錯誤處理"""
        with self.assertRaises(Exception) as context:
            self.broker._ensure_logged_in()
        
        self.assertIn('Not logged in', str(context.exception))
    
    @patch('fubon.broker.FubonSDK')
    def test_logout(self, mock_sdk_class):
        """測試登出"""
        # 先登入
        mock_sdk = MagicMock()
        mock_sdk.login.return_value = True
        mock_sdk_class.return_value = mock_sdk
        
        self.broker.login('test_user', 'test_pass', 'test_cert')
        
        # 執行登出
        result = self.broker.logout()
        
        # 驗證
        self.assertTrue(result)
        self.assertFalse(self.broker.is_logged_in)
        mock_sdk.logout.assert_called_once()
    
    @patch('fubon.broker.FubonSDK')
    def test_context_manager(self, mock_sdk_class):
        """測試 context manager"""
        mock_sdk = MagicMock()
        mock_sdk.login.return_value = True
        mock_sdk_class.return_value = mock_sdk
        
        with FubonBroker() as broker:
            broker.login('test_user', 'test_pass', 'test_cert')
            self.assertTrue(broker.is_logged_in)
        
        # 驗證自動登出
        mock_sdk.logout.assert_called_once()
    
    def test_repr(self):
        """測試字串表示"""
        repr_str = repr(self.broker)
        self.assertIn('FubonBroker', repr_str)
        self.assertIn('logged_in=False', repr_str)


class TestFubonBrokerMarketData(unittest.TestCase):
    """市場行情功能測試"""
    
    def setUp(self):
        """測試前準備"""
        self.broker = FubonBroker()
        self.broker.sdk = MagicMock()
        self.broker.is_logged_in = True
    
    def test_init_realtime(self):
        """測試初始化即時行情"""
        result = self.broker.init_realtime()
        
        self.assertTrue(result)
        self.assertTrue(self.broker.realtime_initialized)
        self.broker.sdk.init_realtime.assert_called_once()
    
    def test_subscribe_quote(self):
        """測試訂閱報價"""
        callback = Mock()
        
        result = self.broker.subscribe_quote('2330', callback)
        
        self.assertTrue(result)
        self.broker.sdk.quote.subscribe.assert_called_once_with('2330')
        self.assertIn('2330', self.broker.quote_callbacks)
    
    def test_unsubscribe_quote(self):
        """測試取消訂閱報價"""
        # 先訂閱
        self.broker.subscribe_quote('2330')
        
        # 取消訂閱
        result = self.broker.unsubscribe_quote('2330')
        
        self.assertTrue(result)
        self.broker.sdk.quote.unsubscribe.assert_called_once_with('2330')
        self.assertNotIn('2330', self.broker.quote_callbacks)
    
    def test_get_quote(self):
        """測試取得報價"""
        mock_quote = {'symbol': '2330', 'price': 600}
        self.broker.sdk.quote.get_quote.return_value = mock_quote
        
        quote = self.broker.get_quote('2330')
        
        self.assertEqual(quote, mock_quote)
        self.broker.sdk.quote.get_quote.assert_called_once_with('2330')


class TestFubonBrokerOrder(unittest.TestCase):
    """下單功能測試"""
    
    def setUp(self):
        """測試前準備"""
        self.broker = FubonBroker()
        self.broker.sdk = MagicMock()
        self.broker.is_logged_in = True
    
    def test_place_order_limit(self):
        """測試限價單下單"""
        mock_result = {'order_id': '12345', 'status': 'Submitted'}
        self.broker.sdk.order.place_order.return_value = mock_result
        
        result = self.broker.place_order(
            symbol='2330',
            action=Action.BUY,
            quantity=1,
            price=600.0,
            price_type=PriceType.LIMIT,
            order_type=OrderType.ROD
        )
        
        self.assertEqual(result, mock_result)
        self.broker.sdk.order.place_order.assert_called_once()
    
    def test_place_order_market(self):
        """測試市價單下單"""
        mock_result = {'order_id': '12345', 'status': 'Submitted'}
        self.broker.sdk.order.place_order.return_value = mock_result
        
        result = self.broker.place_order(
            symbol='2330',
            action=Action.SELL,
            quantity=1,
            price_type=PriceType.MARKET,
            order_type=OrderType.ROD
        )
        
        self.assertEqual(result, mock_result)
    
    def test_place_order_without_price(self):
        """測試限價單未提供價格"""
        with self.assertRaises(ValueError):
            self.broker.place_order(
                symbol='2330',
                action=Action.BUY,
                quantity=1,
                price_type=PriceType.LIMIT  # 限價單但沒給價格
            )
    
    def test_cancel_order(self):
        """測試取消委託"""
        self.broker.sdk.order.cancel_order.return_value = True
        
        result = self.broker.cancel_order('12345')
        
        self.assertTrue(result)
        self.broker.sdk.order.cancel_order.assert_called_once_with('12345')
    
    def test_modify_order(self):
        """測試修改委託"""
        self.broker.sdk.order.modify_order.return_value = True
        
        result = self.broker.modify_order('12345', price=605.0)
        
        self.assertTrue(result)
        self.broker.sdk.order.modify_order.assert_called_once()
    
    def test_get_orders(self):
        """測試查詢委託"""
        mock_orders = [
            {'order_id': '1', 'symbol': '2330'},
            {'order_id': '2', 'symbol': '2317'}
        ]
        self.broker.sdk.order.get_orders.return_value = mock_orders
        
        orders = self.broker.get_orders()
        
        self.assertEqual(len(orders), 2)
        self.broker.sdk.order.get_orders.assert_called_once()


class TestFubonBrokerAccount(unittest.TestCase):
    """帳戶管理功能測試"""
    
    def setUp(self):
        """測試前準備"""
        self.broker = FubonBroker()
        self.broker.sdk = MagicMock()
        self.broker.is_logged_in = True
    
    def test_get_account_info(self):
        """測試取得帳戶資訊"""
        mock_account = {'account_id': '1234567', 'name': 'Test User'}
        self.broker.sdk.get_account.return_value = mock_account
        
        account = self.broker.get_account_info()
        
        self.assertEqual(account, mock_account)
        self.broker.sdk.get_account.assert_called_once()
    
    def test_get_balance(self):
        """測試取得餘額"""
        mock_balance = {'cash_balance': 1000000}
        self.broker.sdk.account.get_balance.return_value = mock_balance
        
        balance = self.broker.get_balance()
        
        self.assertEqual(balance, mock_balance)
    
    def test_get_positions(self):
        """測試取得持股"""
        mock_positions = [
            {'symbol': '2330', 'quantity': 1000},
            {'symbol': '2317', 'quantity': 2000}
        ]
        self.broker.sdk.account.get_positions.return_value = mock_positions
        
        positions = self.broker.get_positions()
        
        self.assertEqual(len(positions), 2)
    
    def test_get_position(self):
        """測試取得特定持股"""
        mock_position = {'symbol': '2330', 'quantity': 1000}
        self.broker.sdk.account.get_position.return_value = mock_position
        
        position = self.broker.get_position('2330')
        
        self.assertEqual(position, mock_position)
        self.broker.sdk.account.get_position.assert_called_once_with('2330')
    
    def test_get_buying_power(self):
        """測試取得購買力"""
        self.broker.sdk.account.get_buying_power.return_value = 500000.0
        
        buying_power = self.broker.get_buying_power()
        
        self.assertEqual(buying_power, 500000.0)


if __name__ == '__main__':
    unittest.main()
