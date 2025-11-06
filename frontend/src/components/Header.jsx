import React from 'react';
import './Header.css';

function Header({ isLoggedIn, userInfo, onLogout }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1>🏦 富邦證券 API 測試工具</h1>
        </div>

        <div className="header-right">
          {/* 登入狀態 */}
          {isLoggedIn && (
            <div className="user-info">
              <span className="badge badge-success">
                ✓ 已登入: {userInfo?.user_id}
              </span>
              <button className="btn btn-secondary btn-sm" onClick={onLogout}>
                登出
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;
