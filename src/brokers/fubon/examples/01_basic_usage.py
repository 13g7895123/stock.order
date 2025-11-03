"""
富邦證券 API 使用範例 - 基本操作
Basic Usage Example for Fubon Neo API
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


def main():
    """基本使用範例"""
    
    # 從環境變數取得帳號資訊
    user_id = os.getenv('FUBON_USER_ID')
    password = os.getenv('FUBON_PASSWORD')
    cert_path = os.getenv('FUBON_CERT_PATH')
    
    if not all([user_id, password, cert_path]):
        logger.error("請設定環境變數: FUBON_USER_ID, FUBON_PASSWORD, FUBON_CERT_PATH")
        return
    
    # 使用 context manager 自動處理登入登出
    with FubonBroker() as broker:
        
        # 登入
        logger.info("登入中...")
        broker.login(user_id, password, cert_path)
        logger.info("登入成功!")
        
        # ===== 取得帳戶資訊 =====
        logger.info("\n===== 帳戶資訊 =====")
        account_info = broker.get_account_info()
        logger.info(f"帳戶資訊: {account_info}")
        
        # 取得帳戶餘額
        balance = broker.get_balance()
        logger.info(f"帳戶餘額: {balance}")
        
        # 取得可用購買力
        buying_power = broker.get_buying_power()
        logger.info(f"可用購買力: {buying_power:,.0f} 元")
        
        # ===== 查詢持股 =====
        logger.info("\n===== 持股資訊 =====")
        positions = broker.get_positions()
        logger.info(f"持股數量: {len(positions)} 檔")
        
        for position in positions:
            logger.info(
                f"股票: {position.get('symbol')} "
                f"數量: {position.get('quantity')} "
                f"成本: {position.get('cost_price')} "
                f"現價: {position.get('current_price')}"
            )
        
        # ===== 查詢報價 =====
        logger.info("\n===== 即時報價 =====")
        
        # 初始化即時行情
        broker.init_realtime()
        
        # 訂閱台積電報價
        symbol = "2330"
        logger.info(f"訂閱 {symbol} 報價...")
        broker.subscribe_quote(symbol)
        
        # 取得報價快照
        quote = broker.get_quote(symbol)
        logger.info(f"{symbol} 報價: {quote}")
        
        # ===== 查詢委託 =====
        logger.info("\n===== 委託查詢 =====")
        orders = broker.get_orders()
        logger.info(f"委託數量: {len(orders)} 筆")
        
        for order in orders[:5]:  # 只顯示前5筆
            logger.info(
                f"委託編號: {order.get('order_id')} "
                f"股票: {order.get('symbol')} "
                f"動作: {order.get('action')} "
                f"數量: {order.get('quantity')} "
                f"價格: {order.get('price')} "
                f"狀態: {order.get('status')}"
            )
        
        # ===== 下單範例 (請謹慎使用!) =====
        # 注意: 下方的下單範例已被註解，請根據實際需求謹慎使用
        
        # logger.info("\n===== 下單範例 =====")
        # try:
        #     # 買進台積電 1 股，限價 600 元
        #     order_result = broker.place_order(
        #         symbol="2330",
        #         action=Action.BUY,
        #         quantity=1,
        #         price=600.0,
        #         price_type=PriceType.LIMIT,
        #         order_type=OrderType.ROD,
        #         order_condition=OrderCondition.CASH
        #     )
        #     logger.info(f"下單成功: {order_result}")
        #     
        #     # 取消委託 (請填入實際的委託編號)
        #     # order_id = order_result.get('order_id')
        #     # broker.cancel_order(order_id)
        #     # logger.info(f"委託已取消: {order_id}")
        #     
        # except Exception as e:
        #     logger.error(f"下單失敗: {str(e)}")
        
        logger.info("\n所有操作完成!")


if __name__ == "__main__":
    main()
