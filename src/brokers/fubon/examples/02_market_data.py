"""
富邦證券 API 使用範例 - 市場行情查詢
Market Data Example for Fubon Neo API
"""

import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fubon.broker import FubonBroker

# 載入環境變數
load_dotenv()

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def quote_callback(quote_data):
    """報價更新回調函數"""
    logger.info(f"報價更新: {quote_data}")


def main():
    """市場行情查詢範例"""
    
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
        
        # ===== 即時報價 =====
        logger.info("\n===== 即時報價 =====")
        
        # 初始化即時行情
        broker.init_realtime()
        
        # 訂閱多檔股票
        symbols = ["2330", "2317", "2454", "2881", "2882"]  # 台積電、鴻海、聯發科、富邦金、國泰金
        
        for symbol in symbols:
            logger.info(f"訂閱 {symbol}...")
            broker.subscribe_quote(symbol, callback=quote_callback)
            
            # 取得報價快照
            quote = broker.get_quote(symbol)
            if quote:
                logger.info(
                    f"{symbol} - "
                    f"最新: {quote.get('last_price')} "
                    f"漲跌: {quote.get('change')} "
                    f"漲跌幅: {quote.get('change_percent')}% "
                    f"成交量: {quote.get('volume')}"
                )
        
        # ===== 歷史資料查詢 =====
        logger.info("\n===== 歷史資料查詢 =====")
        
        # 查詢台積電過去30天的日線資料
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        symbol = "2330"
        logger.info(f"查詢 {symbol} 歷史資料...")
        
        historical_data = broker.get_historical_data(
            symbol=symbol,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            interval='1d'  # 日線
        )
        
        if historical_data:
            logger.info(f"取得 {len(historical_data)} 筆歷史資料")
            
            # 顯示最近5天的資料
            for data in historical_data[-5:]:
                logger.info(
                    f"日期: {data.get('date')} "
                    f"開盤: {data.get('open')} "
                    f"最高: {data.get('high')} "
                    f"最低: {data.get('low')} "
                    f"收盤: {data.get('close')} "
                    f"成交量: {data.get('volume')}"
                )
        
        # ===== 盤中即時資料 =====
        logger.info("\n===== 盤中即時資料 =====")
        
        # 查詢台積電今日1分鐘K線
        intraday_data = broker.get_intraday_data(
            symbol=symbol,
            interval='1m'
        )
        
        if intraday_data:
            logger.info(f"取得 {len(intraday_data)} 筆盤中資料")
            
            # 顯示最近5筆資料
            for data in intraday_data[-5:]:
                logger.info(
                    f"時間: {data.get('time')} "
                    f"開盤: {data.get('open')} "
                    f"最高: {data.get('high')} "
                    f"最低: {data.get('low')} "
                    f"收盤: {data.get('close')} "
                    f"成交量: {data.get('volume')}"
                )
        
        # ===== 技術分析應用範例 =====
        logger.info("\n===== 簡單技術分析 =====")
        
        if historical_data and len(historical_data) >= 5:
            # 計算5日平均價
            recent_5_days = historical_data[-5:]
            avg_price = sum(d.get('close', 0) for d in recent_5_days) / 5
            logger.info(f"{symbol} 5日平均價: {avg_price:.2f}")
            
            # 計算漲跌
            first_close = recent_5_days[0].get('close', 0)
            last_close = recent_5_days[-1].get('close', 0)
            change = last_close - first_close
            change_percent = (change / first_close * 100) if first_close > 0 else 0
            
            logger.info(f"5日漲跌: {change:.2f} ({change_percent:.2f}%)")
        
        # 等待一段時間接收即時報價更新
        logger.info("\n等待接收即時報價更新... (按 Ctrl+C 結束)")
        try:
            import time
            time.sleep(30)  # 等待30秒
        except KeyboardInterrupt:
            logger.info("停止接收報價")
        
        # 取消訂閱
        for symbol in symbols:
            broker.unsubscribe_quote(symbol)
            logger.info(f"已取消訂閱 {symbol}")
        
        logger.info("\n所有操作完成!")


if __name__ == "__main__":
    main()
