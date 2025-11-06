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

  const accountData = accountInfo?.data || {};
  const balanceData = balance?.data || {};
  const balanceValue = balance?.balance ?? balanceData.total_asset ?? 0;
  const marketValue = balanceData.market_value ?? balanceData.total_market_value ?? 0;
  const cashAvailable = balanceData.available_balance ?? balance?.balance ?? 0;
  const buyingPower = balance?.buying_power ?? balanceData.buying_power ?? 0;
  const profitLossData = profitLoss?.profit_loss || {};
  const positionsList = positions?.positions || [];

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
            {balanceValue?.toLocaleString?.() || Number(balanceValue || 0).toLocaleString()} 元
          </div>
        </div>

        <div className="card summary-card">
          <h3>📊 持股市值</h3>
          <div className="summary-value">
            {marketValue?.toLocaleString?.() || Number(marketValue || 0).toLocaleString()} 元
          </div>
        </div>

        <div className="card summary-card">
          <h3>💵 現金餘額</h3>
          <div className="summary-value">
            {cashAvailable?.toLocaleString?.() || Number(cashAvailable || 0).toLocaleString()} 元
          </div>
        </div>

        <div className="card summary-card">
          <h3>📈 今日損益</h3>
          <div className={`summary-value ${profitLossData.today_pl >= 0 ? 'profit' : 'loss'}`}>
            {profitLossData.today_pl >= 0 ? '+' : ''}{profitLossData.today_pl?.toLocaleString?.() || Number(profitLossData.today_pl || 0).toLocaleString()} 元
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
              <span>{accountData.account_id || '-'}</span>
            </div>
            <div className="info-item">
              <label>帳戶類型:</label>
              <span>{accountData.account_type || '-'}</span>
            </div>
            <div className="info-item">
              <label>帳戶狀態:</label>
              <span className="badge badge-success">
                {accountData.status || '正常'}
              </span>
            </div>
            <div className="info-item">
              <label>可用餘額:</label>
              <span className="highlight">
                {cashAvailable?.toLocaleString?.() || Number(cashAvailable || 0).toLocaleString()} 元
              </span>
            </div>
            <div className="info-item">
              <label>購買力:</label>
              <span>{buyingPower?.toLocaleString?.() || Number(buyingPower || 0).toLocaleString()} 元</span>
            </div>
            <div className="info-item">
              <label>持股總數:</label>
              <span>{positionsList.length} 支</span>
            </div>
            <div className="info-item">
              <label>今日損益:</label>
              <span className={profitLossData.today_pl >= 0 ? 'text-success' : 'text-danger'}>
                {profitLossData.today_pl >= 0 ? '+' : ''}{profitLossData.today_pl?.toLocaleString?.() || Number(profitLossData.today_pl || 0).toLocaleString()} 元
              </span>
            </div>
            <div className="info-item">
              <label>累計損益:</label>
              <span className={profitLossData.total_pl >= 0 ? 'text-success' : 'text-danger'}>
                {profitLossData.total_pl >= 0 ? '+' : ''}{profitLossData.total_pl?.toLocaleString?.() || Number(profitLossData.total_pl || 0).toLocaleString()} 元
              </span>
            </div>
          </div>
        </div>
      )}

      {/* 持股明細 */}
      {activeView === 'positions' && (
        <div className="card">
          <div className="card-header">持股明細</div>
          {positionsList.length > 0 ? (
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
                  {positionsList.map((pos, index) => (
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
