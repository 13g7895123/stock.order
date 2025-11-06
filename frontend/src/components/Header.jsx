import React from 'react';
import { ENV_CONFIG } from '../api';
import './Header.css';

function Header({ currentEnv, onEnvChange, isLoggedIn, userInfo, onLogout }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1>🏦 富邦證券 API 測試工具</h1>
        </div>

        <div className="header-right">
          {/* 環境切換 */}
          <div className="env-selector">
            <label>環境:</label>
            <select 
              value={currentEnv} 
              onChange={(e) => onEnvChange(e.target.value)}
              className="form-select"
            >
              {Object.keys(ENV_CONFIG).map(key => (
                <option key={key} value={key}>
                  {ENV_CONFIG[key].name}
                </option>
              ))}
            </select>
          </div>

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

      {/* 環境說明 */}
      <div className="env-description">
        <span className={`badge ${currentEnv === 'production' ? 'badge-warning' : 'badge-info'}`}>
          {currentEnv === 'production' ? '⚠️' : 'ℹ️'} {ENV_CONFIG[currentEnv].description}
        </span>
      </div>
    </header>
  );
}

export default Header;
