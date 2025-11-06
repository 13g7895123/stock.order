"""
API Dependencies
API 依賴注入模組
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Any
import sys
import os
import logging

logger = logging.getLogger(__name__)

# 添加 src 目錄到路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 檢查 fubon-neo 是否可用
FUBON_NEO_AVAILABLE = False
try:
    import fubon_neo
    FUBON_NEO_AVAILABLE = True
    logger.info("fubon-neo SDK is available")
except ImportError:
    logger.warning("fubon-neo SDK not installed, only Mock mode available")

# 全局 broker 實例存儲
_broker_instances: dict = {}

security = HTTPBearer()


def get_broker_instance(session_id: str = "default", use_mock: bool = True) -> Any:
    """
    取得 Broker 實例
    
    Args:
        session_id: 會話 ID，用於支援多用戶
        use_mock: 是否使用 Mock 模式
    
    Returns:
        FubonBroker: Broker 實例（Mock 或 Real）
    
    Raises:
        HTTPException: 當正式環境要求但 SDK 未安裝時
    """
    # 生成帶模式標記的 session key
    session_key = f"{session_id}_{'mock' if use_mock else 'real'}"
    
    if session_key not in _broker_instances:
        # 如果要求使用真實 SDK 但未安裝，拋出錯誤
        if not use_mock and not FUBON_NEO_AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="正式環境需要安裝 fubon-neo SDK。請執行: pip install fubon-neo"
            )
        
        # 根據模式選擇 Broker
        if use_mock or not FUBON_NEO_AVAILABLE:
            from src.brokers.fubon.broker_mock import FubonBroker
            logger.info(f"Creating Mock FubonBroker for session {session_id}")
        else:
            from src.brokers.fubon.broker import FubonBroker
            logger.info(f"Creating Real FubonBroker for session {session_id}")
        
        _broker_instances[session_key] = FubonBroker()
    
    return _broker_instances[session_key]


def get_authenticated_broker(
    session_id: str = "default",
    use_mock: bool = True
) -> Any:
    """
    取得已認證的 Broker 實例
    
    Args:
        session_id: 會話 ID
        use_mock: 是否使用 Mock 模式
    
    Returns:
        FubonBroker: 已登入的 Broker 實例
    
    Raises:
        HTTPException: 未登入時拋出 401 錯誤
    """
    broker = get_broker_instance(session_id, use_mock)
    
    if not broker.is_logged_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in. Please login first."
        )
    
    return broker


def cleanup_broker_instance(session_id: str = "default"):
    """清理 Broker 實例"""
    if session_id in _broker_instances:
        broker = _broker_instances[session_id]
        if broker.is_logged_in:
            broker.logout()
        del _broker_instances[session_id]
