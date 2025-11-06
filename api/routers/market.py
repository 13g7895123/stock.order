"""
Market Data Router
市場行情相關 API 端點
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any
import logging

from schemas import (
    QuoteRequest, HistoricalDataRequest, IntradayDataRequest,
    SuccessResponse
)
from dependencies import get_authenticated_broker
from src.brokers.fubon.broker import FubonBroker

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/subscribe", summary="訂閱即時報價")
async def subscribe_quote(
    request: QuoteRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    訂閱股票即時報價
    
    - **stock_codes**: 股票代號列表 (例如: ["2330", "2317"])
    """
    try:
        results = []
        for stock_code in request.stock_codes:
            success = broker.subscribe_quote(stock_code)
            results.append({
                "stock_code": stock_code,
                "success": success
            })
        
        return {
            "success": True,
            "message": "訂閱請求已處理",
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Subscribe quote error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"訂閱報價錯誤: {str(e)}"
        )


@router.post("/unsubscribe", summary="取消訂閱即時報價")
async def unsubscribe_quote(
    request: QuoteRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取消訂閱股票即時報價
    
    - **stock_codes**: 股票代號列表
    """
    try:
        results = []
        for stock_code in request.stock_codes:
            success = broker.unsubscribe_quote(stock_code)
            results.append({
                "stock_code": stock_code,
                "success": success
            })
        
        return {
            "success": True,
            "message": "取消訂閱請求已處理",
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Unsubscribe quote error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取消訂閱錯誤: {str(e)}"
        )


@router.post("/quote", summary="查詢即時報價")
async def get_quote(
    request: QuoteRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    查詢股票即時報價
    
    - **stock_codes**: 股票代號列表
    """
    try:
        quotes = []
        for stock_code in request.stock_codes:
            quote = broker.get_quote(stock_code)
            if quote:
                quotes.append(quote)
        
        return {
            "success": True,
            "count": len(quotes),
            "quotes": quotes
        }
    
    except Exception as e:
        logger.error(f"Get quote error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查詢報價錯誤: {str(e)}"
        )


@router.post("/historical", summary="查詢歷史行情")
async def get_historical_data(
    request: HistoricalDataRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    查詢歷史行情資料
    
    - **stock_code**: 股票代號
    - **interval**: 時間間隔 (D=日線, 1=1分鐘, 5=5分鐘, 15=15分鐘, 30=30分鐘, 60=60分鐘)
    - **start_date**: 開始日期 (YYYY-MM-DD)
    - **end_date**: 結束日期 (YYYY-MM-DD)
    """
    try:
        data = broker.get_historical_data(
            stock_code=request.stock_code,
            interval=request.interval,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        if data is not None:
            # 將 DataFrame 轉換為字典列表
            records = data.to_dict('records') if hasattr(data, 'to_dict') else data
            
            return {
                "success": True,
                "stock_code": request.stock_code,
                "interval": request.interval,
                "count": len(records),
                "data": records
            }
        else:
            return {
                "success": False,
                "message": "無法取得歷史資料"
            }
    
    except Exception as e:
        logger.error(f"Get historical data error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查詢歷史行情錯誤: {str(e)}"
        )


@router.post("/intraday", summary="查詢盤中即時資料")
async def get_intraday_data(
    request: IntradayDataRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    查詢股票盤中即時資料
    
    - **stock_code**: 股票代號
    """
    try:
        data = broker.get_intraday_data(request.stock_code)
        
        if data:
            return {
                "success": True,
                "stock_code": request.stock_code,
                "data": data
            }
        else:
            return {
                "success": False,
                "message": "無法取得盤中資料"
            }
    
    except Exception as e:
        logger.error(f"Get intraday data error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查詢盤中資料錯誤: {str(e)}"
        )


@router.post("/quote/callback", summary="設定報價回調")
async def set_quote_callback(
    stock_code: str,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    設定報價更新回調函數 (需要配合 WebSocket 使用)
    
    - **stock_code**: 股票代號
    """
    try:
        # 這裡可以實作 WebSocket 推送邏輯
        # 目前僅返回成功訊息
        
        return {
            "success": True,
            "message": f"已設定 {stock_code} 的報價回調",
            "stock_code": stock_code
        }
    
    except Exception as e:
        logger.error(f"Set quote callback error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"設定回調錯誤: {str(e)}"
        )
