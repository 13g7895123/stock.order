"""
富邦證券 API 使用範例 - 下單與委託管理
Order Management Example for Fubon Neo API
"""

import os
import logging
from dotenv import load_dotenv
from fubon.broker import FubonBroker
from fubon.constants import Action, PriceType, OrderType, OrderCondition

# 載入環境變數
load_dotenv()

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def order_status_callback(order_data):
    """委託狀態變更回調函數"""
    logger.info(f"委託狀態更新: {order_data}")


def main():
    """下單與委託管理範例"""
    
    # 從環境變數取得帳號資訊
    user_id = os.getenv('FUBON_USER_ID')
    password = os.getenv('FUBON_PASSWORD')
    cert_path = os.getenv('FUBON_CERT_PATH')
    
    if not all([user_id, password, cert_path]):
        logger.error("請設定環境變數: FUBON_USER_ID, FUBON_PASSWORD, FUBON_CERT_PATH")
        return
    
    with FubonBroker() as broker:
        # 登入
        logger.info("登入中...")
        broker.login(user_id, password, cert_path)
        logger.info("登入成功!")
        
        # 設定委託狀態回調
        broker.set_order_callback(order_status_callback)
        
        # ===== 查詢當日委託 =====
        logger.info("\n===== 查詢當日委託 =====")
        
        orders = broker.get_orders()
        logger.info(f"當日委託總數: {len(orders)} 筆")
        
        if orders:
            logger.info("\n最近的委託:")
            for order in orders[:10]:  # 顯示最近10筆
                logger.info(
                    f"委託編號: {order.get('order_id')} | "
                    f"股票: {order.get('symbol')} | "
                    f"動作: {order.get('action')} | "
                    f"數量: {order.get('quantity')} | "
                    f"價格: {order.get('price')} | "
                    f"類型: {order.get('order_type')} | "
                    f"狀態: {order.get('status')}"
                )
        
        # ===== 下單範例 =====
        logger.info("\n===== 下單範例 (已註解，請謹慎使用) =====")
        
        # 警告: 以下程式碼會實際下單，請確認後再使用!
        ENABLE_TRADING = False  # 設為 True 以啟用實際下單
        
        if ENABLE_TRADING:
            try:
                # 範例 1: 限價單買進
                logger.info("\n範例 1: 限價單買進")
                order1 = broker.place_order(
                    symbol="2330",              # 台積電
                    action=Action.BUY,          # 買進
                    quantity=1,                 # 1股 (1張 = 1000股)
                    price=600.0,                # 限價 600元
                    price_type=PriceType.LIMIT, # 限價
                    order_type=OrderType.ROD,   # 當日有效
                    order_condition=OrderCondition.CASH  # 現股
                )
                logger.info(f"委託成功: {order1}")
                order1_id = order1.get('order_id')
                
                # 範例 2: 市價單賣出
                logger.info("\n範例 2: 市價單賣出")
                order2 = broker.place_order(
                    symbol="2317",               # 鴻海
                    action=Action.SELL,          # 賣出
                    quantity=1,                  # 1股
                    price_type=PriceType.MARKET, # 市價
                    order_type=OrderType.ROD,    # 當日有效
                    order_condition=OrderCondition.CASH
                )
                logger.info(f"委託成功: {order2}")
                
                # 範例 3: IOC 限價單
                logger.info("\n範例 3: IOC 限價單")
                order3 = broker.place_order(
                    symbol="2454",              # 聯發科
                    action=Action.BUY,
                    quantity=1,
                    price=1000.0,
                    price_type=PriceType.LIMIT,
                    order_type=OrderType.IOC,   # 立即成交否則取消
                    order_condition=OrderCondition.CASH
                )
                logger.info(f"委託成功: {order3}")
                
                # ===== 修改委託 =====
                logger.info("\n===== 修改委託 =====")
                
                # 修改委託價格
                if order1_id:
                    logger.info(f"修改委託 {order1_id} 的價格...")
                    modify_result = broker.modify_order(
                        order_id=order1_id,
                        price=605.0  # 改為 605元
                    )
                    logger.info(f"修改結果: {modify_result}")
                
                # ===== 取消委託 =====
                logger.info("\n===== 取消委託 =====")
                
                # 取消委託
                if order1_id:
                    logger.info(f"取消委託 {order1_id}...")
                    cancel_result = broker.cancel_order(order1_id)
                    logger.info(f"取消結果: {cancel_result}")
                
            except Exception as e:
                logger.error(f"下單操作失敗: {str(e)}")
        else:
            logger.info("下單功能已關閉，請設定 ENABLE_TRADING = True 以啟用")
        
        # ===== 查詢特定委託 =====
        logger.info("\n===== 查詢特定委託 =====")
        
        if orders and len(orders) > 0:
            # 查詢第一筆委託的詳細資訊
            first_order_id = orders[0].get('order_id')
            logger.info(f"查詢委託 {first_order_id}...")
            
            order_detail = broker.get_order(first_order_id)
            if order_detail:
                logger.info(f"委託詳情: {order_detail}")
        
        # ===== 依狀態查詢委託 =====
        logger.info("\n===== 依狀態查詢委託 =====")
        
        # 查詢已成交的委託
        filled_orders = broker.get_orders(status='Filled')
        logger.info(f"已成交委託: {len(filled_orders)} 筆")
        
        # 查詢等待中的委託
        pending_orders = broker.get_orders(status='Pending')
        logger.info(f"等待中委託: {len(pending_orders)} 筆")
        
        # ===== 依股票查詢委託 =====
        logger.info("\n===== 依股票查詢委託 =====")
        
        symbol = "2330"
        symbol_orders = broker.get_orders(symbol=symbol)
        logger.info(f"{symbol} 的委託: {len(symbol_orders)} 筆")
        
        # ===== 檢查購買力 =====
        logger.info("\n===== 檢查購買力 =====")
        
        buying_power = broker.get_buying_power()
        logger.info(f"可用購買力: {buying_power:,.0f} 元")
        
        # 計算可買張數 (假設股價 600 元)
        stock_price = 600
        shares_per_lot = 1000
        lot_price = stock_price * shares_per_lot
        max_lots = int(buying_power / lot_price)
        
        logger.info(f"以 {stock_price} 元計算，可買 {max_lots} 張")
        
        logger.info("\n所有操作完成!")


if __name__ == "__main__":
    main()
