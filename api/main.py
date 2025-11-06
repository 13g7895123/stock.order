"""
FastAPI Main Application
富邦證券 API 主應用程式
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import Dict, Any
from datetime import datetime

from routers import auth, market, order, account
from dependencies import get_broker_instance

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 建立 FastAPI 應用
app = FastAPI(
    title="Fubon Neo API",
    description="富邦證券 Neo API RESTful 服務",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應該設定具體的來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["認證"])
app.include_router(market.router, prefix="/api/v1/market", tags=["市場行情"])
app.include_router(order.router, prefix="/api/v1/order", tags=["交易下單"])
app.include_router(account.router, prefix="/api/v1/account", tags=["帳戶管理"])


@app.get("/", tags=["系統"])
async def root():
    """根路徑"""
    return {
        "service": "Fubon Neo API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["系統"])
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 異常處理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """一般異常處理"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
