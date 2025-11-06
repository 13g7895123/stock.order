import React, { useState } from 'react';
import api from '../api';
import './MarketPanel.css';

function MarketPanel() {
  const [stockCodes, setStockCodes] = useState('2330,2317');
  const [quoteData, setQuoteData] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [intradayData, setIntradayData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleGetQuote = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const codes = stockCodes.split(',').map(c => c.trim());
      const result = await api.getQuote(codes);
      setQuoteData(result);
      setMessage({ type: 'success', text: '即時報價查詢成功！' });
    } catch (error) {
      console.error('查詢報價錯誤:', error);
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.error || '查詢失敗'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGetHistorical = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const codes = stockCodes.split(',').map(c => c.trim());
      const result = await api.getHistoricalData(codes[0], 'D');
      setHistoricalData(result);
      setMessage({ type: 'success', text: '歷史資料查詢成功！' });
    } catch (error) {
      console.error('查詢歷史資料錯誤:', error);
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.error || '查詢失敗'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGetIntraday = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const codes = stockCodes.split(',').map(c => c.trim());
      const result = await api.getIntradayData(codes[0]);
      setIntradayData(result);
      setMessage({ type: 'success', text: '盤中資料查詢成功！' });
    } catch (error) {
      console.error('查詢盤中資料錯誤:', error);
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.error || '查詢失敗'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const codes = stockCodes.split(',').map(c => c.trim());
      const result = await api.subscribeQuote(codes);
      setMessage({ 
        type: 'success', 
        text: `成功訂閱 ${result.subscribed?.join(', ')} 的即時報價`
      });
    } catch (error) {
      console.error('訂閱錯誤:', error);
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.error || '訂閱失敗'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="market-panel">
      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="card">
        <div className="card-header">📊 市場行情查詢</div>

        <div className="form-group">
          <label className="form-label">股票代碼（多個用逗號分隔）</label>
          <input
            type="text"
            className="form-input"
            value={stockCodes}
            onChange={(e) => setStockCodes(e.target.value)}
            placeholder="例如: 2330,2317"
          />
          <small className="form-help">
            常用代碼: 2330(台積電), 2317(鴻海), 2454(聯發科), 2412(中華電)
          </small>
        </div>

        <div className="button-group">
          <button 
            className="btn btn-primary"
            onClick={handleGetQuote}
            disabled={loading}
          >
            {loading ? '查詢中...' : '📈 即時報價'}
          </button>
          <button 
            className="btn btn-primary"
            onClick={handleGetHistorical}
            disabled={loading}
          >
            {loading ? '查詢中...' : '📉 歷史資料'}
          </button>
          <button 
            className="btn btn-primary"
            onClick={handleGetIntraday}
            disabled={loading}
          >
            {loading ? '查詢中...' : '⏰ 盤中走勢'}
          </button>
          <button 
            className="btn btn-success"
            onClick={handleSubscribe}
            disabled={loading}
          >
            {loading ? '訂閱中...' : '🔔 訂閱報價'}
          </button>
        </div>
      </div>

      {quoteData && (
        <div className="card">
          <div className="card-header">即時報價</div>
          {quoteData.quotes && quoteData.quotes.length > 0 ? (
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>股票代碼</th>
                    <th>股票名稱</th>
                    <th>成交價</th>
                    <th>漲跌</th>
                    <th>漲跌幅</th>
                    <th>成交量</th>
                    <th>買價/量</th>
                    <th>賣價/量</th>
                  </tr>
                </thead>
                <tbody>
                  {quoteData.quotes.map((quote, index) => (
                    <tr key={index}>
                      <td>{quote.code}</td>
                      <td>{quote.name}</td>
                      <td className="price">{quote.price}</td>
                      <td className={quote.change >= 0 ? 'text-success' : 'text-danger'}>
                        {quote.change >= 0 ? '+' : ''}{quote.change}
                      </td>
                      <td className={quote.change_percent >= 0 ? 'text-success' : 'text-danger'}>
                        {quote.change_percent >= 0 ? '+' : ''}{quote.change_percent}%
                      </td>
                      <td>{quote.volume}</td>
                      <td>{quote.bid_price} / {quote.bid_volume}</td>
                      <td>{quote.ask_price} / {quote.ask_volume}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="no-data">無報價資料</p>
          )}
        </div>
      )}

      {historicalData && (
        <div className="card">
          <div className="card-header">歷史資料</div>
          {historicalData.data && historicalData.data.length > 0 ? (
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>日期</th>
                    <th>開盤</th>
                    <th>最高</th>
                    <th>最低</th>
                    <th>收盤</th>
                    <th>成交量</th>
                  </tr>
                </thead>
                <tbody>
                  {historicalData.data.slice(0, 10).map((item, index) => (
                    <tr key={index}>
                      <td>{item.date}</td>
                      <td>{item.open}</td>
                      <td>{item.high}</td>
                      <td>{item.low}</td>
                      <td>{item.close}</td>
                      <td>{item.volume}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {historicalData.data.length > 10 && (
                <p className="text-muted text-center">
                  顯示最近 10 筆，共 {historicalData.data.length} 筆資料
                </p>
              )}
            </div>
          ) : (
            <p className="no-data">無歷史資料</p>
          )}
        </div>
      )}

      {intradayData && (
        <div className="card">
          <div className="card-header">盤中走勢</div>
          <div className="json-viewer">
            <pre>{JSON.stringify(intradayData, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default MarketPanel;
