"""
Authentication Router
認證相關 API 端點
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
import logging

from schemas import LoginRequest, LoginResponse, SuccessResponse
from dependencies import get_broker_instance, cleanup_broker_instance

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/login", response_model=LoginResponse, summary="登入")
async def login(
    request: LoginRequest,
    session_id: str = "default"
):
    """
    登入富邦證券帳戶
    
    - **user_id**: 使用者帳號
    - **password**: 密碼
    - **cert_path**: 憑證路徑
    - **person_id**: 身分證字號 (選填)
    - **use_mock**: 是否使用 Mock 模式 (True=測試環境, False=正式環境)
    """
    try:
        # 根據 use_mock 參數獲取對應的 broker
        broker = get_broker_instance(session_id, use_mock=request.use_mock)
        
        # 如果已經登入，先登出
        if broker.is_logged_in:
            broker.logout()
        
        # 執行登入
        success = broker.login(
            user_id=request.user_id,
            password=request.password,
            cert_path=request.cert_path,
            person_id=request.person_id
        )
        
        mode_text = "Mock 模式（測試環境）" if request.use_mock else "真實 SDK（正式環境）"
        
        if success:
            return LoginResponse(
                success=True,
                message=f"登入成功 - {mode_text}",
                user_id=request.user_id,
                session_id=session_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="登入失敗，請檢查帳號密碼"
            )
    
    except HTTPException:
        # 重新拋出 HTTPException（如 SDK 未安裝的 503 錯誤）
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登入錯誤: {str(e)}"
        )


@router.post("/logout", response_model=SuccessResponse, summary="登出")
async def logout(session_id: str = "default"):
    """
    登出富邦證券帳戶
    """
    try:
        broker = get_broker_instance(session_id)
        
        if not broker.is_logged_in:
            return SuccessResponse(
                success=True,
                message="尚未登入"
            )
        
        success = broker.logout()
        
        if success:
            cleanup_broker_instance(session_id)
            return SuccessResponse(
                success=True,
                message="登出成功"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="登出失敗"
            )
    
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登出錯誤: {str(e)}"
        )


@router.get("/status", summary="檢查登入狀態")
async def check_status(session_id: str = "default"):
    """
    檢查當前登入狀態
    """
    try:
        broker = get_broker_instance(session_id)
        
        return {
            "success": True,
            "is_logged_in": broker.is_logged_in,
            "user_id": broker.user_id if broker.is_logged_in else None,
            "session_id": session_id
        }
    
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"狀態檢查錯誤: {str(e)}"
        )
