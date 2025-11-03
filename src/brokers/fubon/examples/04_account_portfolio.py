"""
富邦證券 API 使用範例 - 帳戶與投資組合管理
Account & Portfolio Management Example for Fubon Neo API
"""

import os
import logging
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


def main():
    """帳戶與投資組合管理範例"""
    
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
        
        # ===== 帳戶資訊 =====
        logger.info("\n===== 帳戶資訊 =====")
        
        account_info = broker.get_account_info()
        logger.info(f"帳戶資訊:")
        logger.info(f"  帳號: {account_info.get('account_id')}")
        logger.info(f"  帳戶名稱: {account_info.get('account_name')}")
        logger.info(f"  帳戶類型: {account_info.get('account_type')}")
        
        # ===== 帳戶餘額 =====
        logger.info("\n===== 帳戶餘額 =====")
        
        balance = broker.get_balance()
        logger.info(f"餘額資訊:")
        logger.info(f"  現金餘額: {balance.get('cash_balance', 0):,.0f} 元")
        logger.info(f"  可用餘額: {balance.get('available_balance', 0):,.0f} 元")
        logger.info(f"  凍結金額: {balance.get('frozen_amount', 0):,.0f} 元")
        
        # 可用購買力
        buying_power = broker.get_buying_power()
        logger.info(f"  可用購買力: {buying_power:,.0f} 元")
        
        # ===== 持股部位 =====
        logger.info("\n===== 持股部位 =====")
        
        positions = broker.get_positions()
        logger.info(f"持股總數: {len(positions)} 檔")
        
        if positions:
            total_market_value = 0
            total_cost = 0
            total_pnl = 0
            
            logger.info("\n詳細持股:")
            logger.info(f"{'股票代號':<8} {'股票名稱':<12} {'數量':<8} {'成本價':<10} {'現價':<10} {'市值':<12} {'損益':<12} {'報酬率':<10}")
            logger.info("-" * 100)
            
            for position in positions:
                symbol = position.get('symbol', 'N/A')
                name = position.get('name', 'N/A')
                quantity = position.get('quantity', 0)
                cost_price = position.get('cost_price', 0)
                current_price = position.get('current_price', 0)
                market_value = quantity * current_price
                cost_value = quantity * cost_price
                pnl = market_value - cost_value
                pnl_percent = (pnl / cost_value * 100) if cost_value > 0 else 0
                
                logger.info(
                    f"{symbol:<8} {name:<12} {quantity:<8} {cost_price:<10.2f} {current_price:<10.2f} "
                    f"{market_value:<12,.0f} {pnl:<12,.0f} {pnl_percent:<10.2f}%"
                )
                
                total_market_value += market_value
                total_cost += cost_value
                total_pnl += pnl
            
            logger.info("-" * 100)
            logger.info(f"{'總計':<20} {'':>28} {total_market_value:<12,.0f} {total_pnl:<12,.0f} {(total_pnl/total_cost*100):<10.2f}%")
            
            # ===== 投資組合摘要 =====
            logger.info("\n===== 投資組合摘要 =====")
            logger.info(f"持股總成本: {total_cost:,.0f} 元")
            logger.info(f"持股總市值: {total_market_value:,.0f} 元")
            logger.info(f"未實現損益: {total_pnl:,.0f} 元")
            logger.info(f"投資報酬率: {(total_pnl/total_cost*100):.2f}%")
            
            # 加上現金餘額
            total_assets = total_market_value + balance.get('cash_balance', 0)
            logger.info(f"\n總資產: {total_assets:,.0f} 元")
            logger.info(f"  現金: {balance.get('cash_balance', 0):,.0f} 元 ({balance.get('cash_balance', 0)/total_assets*100:.1f}%)")
            logger.info(f"  股票: {total_market_value:,.0f} 元 ({total_market_value/total_assets*100:.1f}%)")
        
        # ===== 查詢特定持股 =====
        logger.info("\n===== 查詢特定持股 =====")
        
        if positions:
            # 查詢第一檔持股的詳細資訊
            first_symbol = positions[0].get('symbol')
            logger.info(f"查詢 {first_symbol} 持股...")
            
            position_detail = broker.get_position(first_symbol)
            if position_detail:
                logger.info(f"持股詳情:")
                logger.info(f"  股票代號: {position_detail.get('symbol')}")
                logger.info(f"  持有數量: {position_detail.get('quantity')}")
                logger.info(f"  可賣數量: {position_detail.get('available_quantity')}")
                logger.info(f"  成本價: {position_detail.get('cost_price'):.2f}")
                logger.info(f"  現價: {position_detail.get('current_price'):.2f}")
                logger.info(f"  市值: {position_detail.get('market_value'):,.0f}")
                logger.info(f"  損益: {position_detail.get('pnl'):,.0f}")
        
        # ===== 損益資訊 =====
        logger.info("\n===== 損益資訊 =====")
        
        try:
            pnl_info = broker.get_profit_loss()
            logger.info(f"今日損益:")
            logger.info(f"  已實現損益: {pnl_info.get('realized_pnl', 0):,.0f} 元")
            logger.info(f"  未實現損益: {pnl_info.get('unrealized_pnl', 0):,.0f} 元")
            logger.info(f"  總損益: {pnl_info.get('total_pnl', 0):,.0f} 元")
        except Exception as e:
            logger.warning(f"無法取得損益資訊: {str(e)}")
        
        # ===== 交割資訊 =====
        logger.info("\n===== 交割資訊 =====")
        
        try:
            settlements = broker.get_settlements()
            logger.info(f"交割紀錄: {len(settlements)} 筆")
            
            if settlements:
                logger.info("\n最近的交割:")
                for settlement in settlements[:5]:  # 顯示最近5筆
                    logger.info(
                        f"日期: {settlement.get('date')} | "
                        f"類型: {settlement.get('type')} | "
                        f"金額: {settlement.get('amount'):,.0f} 元 | "
                        f"狀態: {settlement.get('status')}"
                    )
        except Exception as e:
            logger.warning(f"無法取得交割資訊: {str(e)}")
        
        # ===== 融資融券資訊 =====
        logger.info("\n===== 融資融券資訊 =====")
        
        try:
            margin_info = broker.get_margin_info()
            logger.info(f"融資額度: {margin_info.get('margin_limit', 0):,.0f} 元")
            logger.info(f"已用融資: {margin_info.get('margin_used', 0):,.0f} 元")
            logger.info(f"可用融資: {margin_info.get('margin_available', 0):,.0f} 元")
            logger.info(f"融券額度: {margin_info.get('short_limit', 0):,.0f} 元")
            logger.info(f"已用融券: {margin_info.get('short_used', 0):,.0f} 元")
            logger.info(f"可用融券: {margin_info.get('short_available', 0):,.0f} 元")
        except Exception as e:
            logger.warning(f"無法取得融資融券資訊: {str(e)}")
        
        # ===== 投資組合分析 =====
        logger.info("\n===== 投資組合分析 =====")
        
        if positions:
            # 找出前3大持股
            sorted_positions = sorted(
                positions,
                key=lambda x: x.get('market_value', 0),
                reverse=True
            )
            
            logger.info("前3大持股:")
            for i, pos in enumerate(sorted_positions[:3], 1):
                weight = (pos.get('market_value', 0) / total_market_value * 100) if total_market_value > 0 else 0
                logger.info(
                    f"{i}. {pos.get('symbol')} {pos.get('name')} - "
                    f"市值: {pos.get('market_value', 0):,.0f} 元 "
                    f"({weight:.1f}%)"
                )
            
            # 找出最賺錢和最賠錢的持股
            best_performer = max(positions, key=lambda x: x.get('pnl_percent', 0))
            worst_performer = min(positions, key=lambda x: x.get('pnl_percent', 0))
            
            logger.info(f"\n最賺錢: {best_performer.get('symbol')} "
                       f"({best_performer.get('pnl_percent', 0):.2f}%)")
            logger.info(f"最賠錢: {worst_performer.get('symbol')} "
                       f"({worst_performer.get('pnl_percent', 0):.2f}%)")
        
        logger.info("\n所有操作完成!")


if __name__ == "__main__":
    main()
