import React, { useState, useEffect } from 'react';
import api from './api';
import LoginPanel from './components/LoginPanel';
import MarketPanel from './components/MarketPanel';
import AccountPanel from './components/AccountPanel';
import OrderPanel from './components/OrderPanel';
import Header from './components/Header';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [activeTab, setActiveTab] = useState('market');
  const [loading, setLoading] = useState(false);

  // 檢查登入狀態
  useEffect(() => {
    checkLoginStatus();
  }, []);

  const checkLoginStatus = async () => {
    try {
      const status = await api.checkStatus();
      setIsLoggedIn(status.is_logged_in);
      setUserInfo(status);
    } catch (error) {
      console.error('檢查登入狀態失敗:', error);
      setIsLoggedIn(false);
    }
  };

  const handleLogin = async (credentials) => {
    setLoading(true);
    try {
      const result = await api.login(credentials);
      if (result.success) {
        setIsLoggedIn(true);
        setUserInfo(result);
        return { success: true, message: result.message || '登入成功！' };
      } else {
        return { success: false, message: result.message || '登入失敗' };
      }
    } catch (error) {
      console.error('登入錯誤:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || error.response?.data?.error || error.message || '登入失敗'
      };
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await api.logout();
      setIsLoggedIn(false);
      setUserInfo(null);
      setActiveTab('market');
    } catch (error) {
      console.error('登出錯誤:', error);
    }
  };

  return (
    <div className="app">
      <Header 
        isLoggedIn={isLoggedIn}
        userInfo={userInfo}
        onLogout={handleLogout}
      />

      <div className="container">
        {!isLoggedIn ? (
          <LoginPanel 
            onLogin={handleLogin}
            loading={loading}
          />
        ) : (
          <>
            <div className="tabs">
              <button 
                className={`tab ${activeTab === 'market' ? 'active' : ''}`}
                onClick={() => setActiveTab('market')}
              >
                📊 市場行情
              </button>
              <button 
                className={`tab ${activeTab === 'account' ? 'active' : ''}`}
                onClick={() => setActiveTab('account')}
              >
                👤 帳戶資訊
              </button>
              <button 
                className={`tab ${activeTab === 'order' ? 'active' : ''}`}
                onClick={() => setActiveTab('order')}
              >
                💰 交易下單
              </button>
            </div>

            <div className="tab-content">
              {activeTab === 'market' && <MarketPanel />}
              {activeTab === 'account' && <AccountPanel />}
              {activeTab === 'order' && <OrderPanel />}
            </div>
          </>
        )}
      </div>

      <footer className="footer">
        <p>富邦證券 API 測試工具 v1.0.0</p>
        <p>連線位址: <span className="badge badge-info">{api.baseURL}</span></p>
      </footer>
    </div>
  );
}

export default App;
