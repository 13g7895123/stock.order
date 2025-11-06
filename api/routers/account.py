"""
Account Router
帳戶管理相關 API 端點
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any
import logging

from schemas import (
    AccountInfoResponse, BalanceResponse, PositionsResponse,
    PositionRequest, SettlementsResponse, ProfitLossResponse,
    MarginResponse
)
from dependencies import get_authenticated_broker
from src.brokers.fubon.broker import FubonBroker

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/info", response_model=AccountInfoResponse, summary="取得帳戶資訊")
async def get_account_info(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得帳戶基本資訊
    
    包含帳戶狀態、帳號等資訊
    """
    try:
        info = broker.get_account_info()
        
        if info:
            return AccountInfoResponse(
                success=True,
                data=info
            )
        else:
            return AccountInfoResponse(
                success=False,
                data=None
            )
    
    except Exception as e:
        logger.error(f"Get account info error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得帳戶資訊錯誤: {str(e)}"
        )


@router.get("/balance", response_model=BalanceResponse, summary="取得帳戶餘額")
async def get_balance(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得帳戶餘額資訊
    
    包含現金餘額、可用餘額等
    """
    try:
        balance = broker.get_balance()
        
        if balance:
            return BalanceResponse(
                success=True,
                balance=balance.get('balance'),
                buying_power=balance.get('buying_power'),
                data=balance
            )
        else:
            return BalanceResponse(
                success=False
            )
    
    except Exception as e:
        logger.error(f"Get balance error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得餘額錯誤: {str(e)}"
        )


@router.get("/buying-power", summary="取得可用購買力")
async def get_buying_power(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得可用購買力
    
    計算當前可用於購買股票的金額
    """
    try:
        buying_power = broker.get_buying_power()
        
        return {
            "success": True,
            "buying_power": buying_power,
            "formatted": f"NT$ {buying_power:,.0f}" if buying_power else "N/A"
        }
    
    except Exception as e:
        logger.error(f"Get buying power error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得購買力錯誤: {str(e)}"
        )


@router.get("/positions", response_model=PositionsResponse, summary="取得持股部位")
async def get_positions(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得所有持股部位
    
    包含股票代號、持股數量、成本、市值等
    """
    try:
        positions = broker.get_positions()
        
        if positions is not None:
            # 轉換為列表格式
            positions_list = positions.to_dict('records') if hasattr(positions, 'to_dict') else positions
            
            return PositionsResponse(
                success=True,
                positions=positions_list,
                total_count=len(positions_list)
            )
        else:
            return PositionsResponse(
                success=True,
                positions=[],
                total_count=0
            )
    
    except Exception as e:
        logger.error(f"Get positions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得持股部位錯誤: {str(e)}"
        )


@router.post("/position", summary="取得單一持股")
async def get_position(
    request: PositionRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得特定股票的持股資訊
    
    - **stock_code**: 股票代號
    """
    try:
        position = broker.get_position(request.stock_code)
        
        if position:
            return {
                "success": True,
                "stock_code": request.stock_code,
                "position": position
            }
        else:
            return {
                "success": False,
                "message": f"無持股資訊: {request.stock_code}"
            }
    
    except Exception as e:
        logger.error(f"Get position error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得持股錯誤: {str(e)}"
        )


@router.get("/settlements", response_model=SettlementsResponse, summary="取得交割資訊")
async def get_settlements(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得交割資訊
    
    包含應收應付款項、交割日期等
    """
    try:
        settlements = broker.get_settlements()
        
        if settlements is not None:
            settlements_list = settlements.to_dict('records') if hasattr(settlements, 'to_dict') else settlements
            
            return SettlementsResponse(
                success=True,
                settlements=settlements_list
            )
        else:
            return SettlementsResponse(
                success=True,
                settlements=[]
            )
    
    except Exception as e:
        logger.error(f"Get settlements error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得交割資訊錯誤: {str(e)}"
        )


@router.get("/profit-loss", response_model=ProfitLossResponse, summary="取得損益資訊")
async def get_profit_loss(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得帳戶損益資訊
    
    包含已實現損益、未實現損益等
    """
    try:
        profit_loss = broker.get_profit_loss()
        
        if profit_loss:
            return ProfitLossResponse(
                success=True,
                profit_loss=profit_loss
            )
        else:
            return ProfitLossResponse(
                success=False
            )
    
    except Exception as e:
        logger.error(f"Get profit/loss error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得損益資訊錯誤: {str(e)}"
        )


@router.get("/margin", response_model=MarginResponse, summary="取得融資融券資訊")
async def get_margin_info(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得融資融券資訊
    
    包含融資額度、融券額度、已用額度等
    """
    try:
        margin_info = broker.get_margin_info()
        
        if margin_info:
            return MarginResponse(
                success=True,
                margin_info=margin_info
            )
        else:
            return MarginResponse(
                success=False
            )
    
    except Exception as e:
        logger.error(f"Get margin info error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得融資融券資訊錯誤: {str(e)}"
        )


@router.get("/summary", summary="取得帳戶摘要")
async def get_account_summary(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取得帳戶完整摘要
    
    包含餘額、持股、損益等所有資訊的摘要
    """
    try:
        # 取得各項資訊
        balance = broker.get_balance()
        positions = broker.get_positions()
        profit_loss = broker.get_profit_loss()
        
        # 計算持股數量
        position_count = len(positions) if positions is not None else 0
        
        # 計算總市值
        total_market_value = 0
        if positions is not None and hasattr(positions, 'to_dict'):
            positions_list = positions.to_dict('records')
            total_market_value = sum(p.get('market_value', 0) for p in positions_list)
        
        return {
            "success": True,
            "summary": {
                "balance": balance,
                "position_count": position_count,
                "total_market_value": total_market_value,
                "profit_loss": profit_loss,
                "user_id": broker.user_id
            }
        }
    
    except Exception as e:
        logger.error(f"Get account summary error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取得帳戶摘要錯誤: {str(e)}"
        )
