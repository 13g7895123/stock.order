import React, { useState, useEffect } from 'react';
import api from '../api';
import './AccountPanel.css';

function AccountPanel() {
  const [accountInfo, setAccountInfo] = useState(null);
  const [balance, setBalance] = useState(null);
  const [positions, setPositions] = useState(null);
  const [profitLoss, setProfitLoss] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeView, setActiveView] = useState('summary');

  useEffect(() => {
    loadAccountSummary();
  }, []);

  const loadAccountSummary = async () => {
    setLoading(true);
    try {
      const [infoRes, balanceRes, positionsRes, plRes] = await Promise.all([
        api.getAccountInfo(),
        api.getBalance(),
        api.getPositions(),
        api.getProfitLoss()
      ]);
      
      setAccountInfo(infoRes);
      setBalance(balanceRes);
      setPositions(positionsRes);
      setProfitLoss(plRes);
    } catch (error) {
      console.error('載入帳戶資料錯誤:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="account-panel">
        <div className="card">
          <div className="loading-container">
            <span className="loading"></span>
            <p>載入帳戶資料中...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="account-panel">
      {/* 帳戶概覽 */}
      <div className="account-summary">
        <div className="card summary-card">
          <h3>💰 帳戶淨值</h3>
          <div className="summary-value">
            {balance?.total_asset?.toLocaleString() || '0'} 元
          </div>
        </div>

        <div className="card summary-card">
          <h3>📊 持股市值</h3>
          <div className="summary-value">
            {balance?.market_value?.toLocaleString() || '0'} 元
          </div>
        </div>

        <div className="card summary-card">
          <h3>💵 現金餘額</h3>
          <div className="summary-value">
            {balance?.available_balance?.toLocaleString() || '0'} 元
          </div>
        </div>

        <div className="card summary-card">
          <h3>📈 今日損益</h3>
          <div className={`summary-value ${profitLoss?.today_pl >= 0 ? 'profit' : 'loss'}`}>
            {profitLoss?.today_pl >= 0 ? '+' : ''}{profitLoss?.today_pl?.toLocaleString() || '0'} 元
          </div>
        </div>
      </div>

      {/* 詳細資訊切換 */}
      <div className="tabs">
        <button 
          className={`tab ${activeView === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveView('summary')}
        >
          帳戶摘要
        </button>
        <button 
          className={`tab ${activeView === 'positions' ? 'active' : ''}`}
          onClick={() => setActiveView('positions')}
        >
          持股明細
        </button>
        <button 
          className={`tab ${activeView === 'details' ? 'active' : ''}`}
          onClick={() => setActiveView('details')}
        >
          完整資訊
        </button>
      </div>

      {/* 帳戶摘要 */}
      {activeView === 'summary' && (
        <div className="card">
          <div className="card-header">帳戶摘要</div>
          <div className="info-grid">
            <div className="info-item">
              <label>帳戶代碼:</label>
              <span>{accountInfo?.account_id || '-'}</span>
            </div>
            <div className="info-item">
              <label>帳戶類型:</label>
              <span>{accountInfo?.account_type || '-'}</span>
            </div>
            <div className="info-item">
              <label>帳戶狀態:</label>
              <span className="badge badge-success">
                {accountInfo?.status || '正常'}
              </span>
            </div>
            <div className="info-item">
              <label>可用餘額:</label>
              <span className="highlight">
                {balance?.available_balance?.toLocaleString() || '0'} 元
              </span>
            </div>
            <div className="info-item">
              <label>購買力:</label>
              <span>{balance?.buying_power?.toLocaleString() || '0'} 元</span>
            </div>
            <div className="info-item">
              <label>持股總數:</label>
              <span>{positions?.positions?.length || 0} 支</span>
            </div>
            <div className="info-item">
              <label>今日損益:</label>
              <span className={profitLoss?.today_pl >= 0 ? 'text-success' : 'text-danger'}>
                {profitLoss?.today_pl >= 0 ? '+' : ''}{profitLoss?.today_pl?.toLocaleString() || '0'} 元
              </span>
            </div>
            <div className="info-item">
              <label>累計損益:</label>
              <span className={profitLoss?.total_pl >= 0 ? 'text-success' : 'text-danger'}>
                {profitLoss?.total_pl >= 0 ? '+' : ''}{profitLoss?.total_pl?.toLocaleString() || '0'} 元
              </span>
            </div>
          </div>
        </div>
      )}

      {/* 持股明細 */}
      {activeView === 'positions' && (
        <div className="card">
          <div className="card-header">持股明細</div>
          {positions?.positions && positions.positions.length > 0 ? (
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>股票代碼</th>
                    <th>股票名稱</th>
                    <th>持有股數</th>
                    <th>成本價</th>
                    <th>現價</th>
                    <th>市值</th>
                    <th>損益</th>
                    <th>報酬率</th>
                  </tr>
                </thead>
                <tbody>
                  {positions.positions.map((pos, index) => (
                    <tr key={index}>
                      <td>{pos.stock_code}</td>
                      <td>{pos.stock_name}</td>
                      <td>{pos.quantity?.toLocaleString()}</td>
                      <td>{pos.average_price}</td>
                      <td>{pos.current_price}</td>
                      <td>{pos.market_value?.toLocaleString()}</td>
                      <td className={pos.unrealized_pl >= 0 ? 'text-success' : 'text-danger'}>
                        {pos.unrealized_pl >= 0 ? '+' : ''}{pos.unrealized_pl?.toLocaleString()}
                      </td>
                      <td className={pos.return_rate >= 0 ? 'text-success' : 'text-danger'}>
                        {pos.return_rate >= 0 ? '+' : ''}{pos.return_rate}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="no-data">目前無持股</p>
          )}
        </div>
      )}

      {/* 完整資訊 */}
      {activeView === 'details' && (
        <div className="grid grid-2">
          <div className="card">
            <div className="card-header">帳戶資訊</div>
            <div className="json-viewer">
              <pre>{JSON.stringify(accountInfo, null, 2)}</pre>
            </div>
          </div>

          <div className="card">
            <div className="card-header">資金餘額</div>
            <div className="json-viewer">
              <pre>{JSON.stringify(balance, null, 2)}</pre>
            </div>
          </div>

          <div className="card">
            <div className="card-header">持股部位</div>
            <div className="json-viewer">
              <pre>{JSON.stringify(positions, null, 2)}</pre>
            </div>
          </div>

          <div className="card">
            <div className="card-header">損益統計</div>
            <div className="json-viewer">
              <pre>{JSON.stringify(profitLoss, null, 2)}</pre>
            </div>
          </div>
        </div>
      )}

      {/* 重新整理按鈕 */}
      <div className="actions">
        <button className="btn btn-primary" onClick={loadAccountSummary}>
          🔄 重新整理
        </button>
      </div>
    </div>
  );
}

export default AccountPanel;
