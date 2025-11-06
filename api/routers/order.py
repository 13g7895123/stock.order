"""
Order Router
交易下單相關 API 端點
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any, Optional
import logging

from schemas import (
    PlaceOrderRequest, CancelOrderRequest, ModifyOrderRequest,
    QueryOrdersRequest, SuccessResponse
)
from dependencies import get_authenticated_broker
from src.brokers.fubon.broker import FubonBroker

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/place", summary="下單")
async def place_order(
    request: PlaceOrderRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    下單交易
    
    - **stock_code**: 股票代號 (4-6位數字)
    - **action**: 買賣動作 (Buy/Sell)
    - **price**: 價格 (市價單可不填)
    - **quantity**: 數量 (張)
    - **price_type**: 價格類型 (LMT=限價, MKT=市價, MKP=範圍市價)
    - **order_type**: 委託類型 (ROD=當日有效, IOC=立即成交否則取消, FOK=全部成交否則取消)
    - **order_condition**: 委託條件 (Cash=現股, MarginTrading=融資, ShortSelling=融券)
    
    ⚠️ **風險提醒**: 此為實際下單，請謹慎操作！
    """
    try:
        result = broker.place_order(
            stock_code=request.stock_code,
            action=request.action.value,
            price=request.price,
            quantity=request.quantity,
            price_type=request.price_type.value,
            order_type=request.order_type.value,
            order_condition=request.order_condition.value
        )
        
        if result and result.get('success'):
            return {
                "success": True,
                "message": "下單成功",
                "order_id": result.get('order_id'),
                "stock_code": request.stock_code,
                "action": request.action.value,
                "price": request.price,
                "quantity": request.quantity,
                "data": result
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message', '下單失敗')
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Place order error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"下單錯誤: {str(e)}"
        )


@router.post("/cancel", summary="取消委託")
async def cancel_order(
    request: CancelOrderRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    取消委託
    
    - **order_id**: 委託編號
    """
    try:
        result = broker.cancel_order(request.order_id)
        
        if result and result.get('success'):
            return {
                "success": True,
                "message": "取消委託成功",
                "order_id": request.order_id,
                "data": result
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message', '取消委託失敗')
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Cancel order error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取消委託錯誤: {str(e)}"
        )


@router.post("/modify", summary="修改委託")
async def modify_order(
    request: ModifyOrderRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    修改委託
    
    - **order_id**: 委託編號
    - **price**: 新價格 (選填)
    - **quantity**: 新數量 (選填)
    """
    try:
        result = broker.modify_order(
            order_id=request.order_id,
            price=request.price,
            quantity=request.quantity
        )
        
        if result and result.get('success'):
            return {
                "success": True,
                "message": "修改委託成功",
                "order_id": request.order_id,
                "data": result
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message', '修改委託失敗')
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Modify order error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"修改委託錯誤: {str(e)}"
        )


@router.post("/query", summary="查詢委託")
async def query_orders(
    request: QueryOrdersRequest,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    查詢委託列表
    
    - **status**: 委託狀態篩選 (選填)
    - **stock_code**: 股票代號篩選 (選填)
    - **start_date**: 開始日期 (選填)
    - **end_date**: 結束日期 (選填)
    """
    try:
        orders = broker.get_orders(
            status=request.status.value if request.status else None,
            stock_code=request.stock_code
        )
        
        if orders is not None:
            # 轉換為列表格式
            orders_list = orders.to_dict('records') if hasattr(orders, 'to_dict') else orders
            
            return {
                "success": True,
                "count": len(orders_list),
                "orders": orders_list
            }
        else:
            return {
                "success": True,
                "count": 0,
                "orders": []
            }
    
    except Exception as e:
        logger.error(f"Query orders error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查詢委託錯誤: {str(e)}"
        )


@router.get("/detail/{order_id}", summary="查詢單筆委託")
async def get_order_detail(
    order_id: str,
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    查詢單筆委託詳細資訊
    
    - **order_id**: 委託編號
    """
    try:
        order = broker.get_order(order_id)
        
        if order:
            return {
                "success": True,
                "order": order
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"找不到委託編號: {order_id}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get order detail error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查詢委託詳情錯誤: {str(e)}"
        )


@router.get("/today", summary="查詢當日委託")
async def get_today_orders(
    broker: FubonBroker = Depends(get_authenticated_broker)
):
    """
    查詢當日所有委託
    """
    try:
        orders = broker.get_orders()
        
        if orders is not None:
            orders_list = orders.to_dict('records') if hasattr(orders, 'to_dict') else orders
            
            return {
                "success": True,
                "count": len(orders_list),
                "orders": orders_list
            }
        else:
            return {
                "success": True,
                "count": 0,
                "orders": []
            }
    
    except Exception as e:
        logger.error(f"Get today orders error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查詢當日委託錯誤: {str(e)}"
        )
