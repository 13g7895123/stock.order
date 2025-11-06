import React, { useState, useEffect } from 'react';
import api from '../api';
import './OrderPanel.css';

function OrderPanel() {
  const [orderForm, setOrderForm] = useState({
    stock_code: '2330',
    action: 'Buy',
    price_type: 'LMT',
    price: '',
    quantity: 1000,
    order_type: 'ROD',
    order_condition: 'Cash'
  });
  const [todayOrders, setTodayOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    loadTodayOrders();
  }, []);

  const loadTodayOrders = async () => {
    try {
      const result = await api.getTodayOrders();
      setTodayOrders(result.orders || []);
    } catch (error) {
      console.error('載入今日委託錯誤:', error);
    }
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    const nextValue =
      name === 'quantity'
        ? (value === '' ? '' : Number(value))
        : value;
    setOrderForm({
      ...orderForm,
      [name]: nextValue
    });
  };

  const handlePlaceOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const result = await api.placeOrder(orderForm);
      setMessage({
        type: 'success',
        text: result.message || `下單成功！訂單編號: ${result.order_id}`
      });
      // 重新載入今日委託
      await loadTodayOrders();
      // 重置表單
      setOrderForm({
        ...orderForm,
        price: '',
        quantity: 1000
      });
    } catch (error) {
      console.error('下單錯誤:', error);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || error.response?.data?.error || '下單失敗'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm(`確定要取消訂單 ${orderId} 嗎？`)) {
      return;
    }

    try {
      const result = await api.cancelOrder(orderId);
      setMessage({
        type: 'success',
        text: result.message
      });
      await loadTodayOrders();
    } catch (error) {
      console.error('取消訂單錯誤:', error);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || error.response?.data?.error || '取消失敗'
      });
    }
  };

  const getOrderStatusBadge = (status) => {
    const statusMap = {
      'pending': { class: 'badge-warning', text: '委託中' },
      'filled': { class: 'badge-success', text: '已成交' },
      'partially_filled': { class: 'badge-info', text: '部分成交' },
      'cancelled': { class: 'badge-secondary', text: '已取消' },
      'rejected': { class: 'badge-error', text: '已拒絕' }
    };
    const badge = statusMap[status] || { class: 'badge-info', text: status };
    return <span className={`badge ${badge.class}`}>{badge.text}</span>;
  };

  return (
    <div className="order-panel">
      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      {/* 下單表單 */}
      <div className="card">
        <div className="card-header">💰 快速下單</div>
        
        <form onSubmit={handlePlaceOrder}>
          <div className="grid grid-3">
            <div className="form-group">
              <label className="form-label">股票代碼 *</label>
              <input
                type="text"
                name="stock_code"
                className="form-input"
                value={orderForm.stock_code}
                onChange={handleFormChange}
                required
                placeholder="例如: 2330"
              />
            </div>

            <div className="form-group">
              <label className="form-label">買賣別 *</label>
              <select
                name="action"
                className="form-select"
                value={orderForm.action}
                onChange={handleFormChange}
                required
              >
                <option value="Buy">買進</option>
                <option value="Sell">賣出</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">價格類型 *</label>
              <select
                name="price_type"
                className="form-select"
                value={orderForm.price_type}
                onChange={handleFormChange}
                required
              >
                <option value="LMT">限價 (LMT)</option>
                <option value="MKT">市價 (MKT)</option>
                <option value="MKP">範圍市價 (MKP)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">
                價格 {orderForm.price_type !== 'MKT' ? '*' : ''}
              </label>
              <input
                type="number"
                name="price"
                className="form-input"
                value={orderForm.price}
                onChange={handleFormChange}
                required={orderForm.price_type !== 'MKT'}
                disabled={orderForm.price_type === 'MKT'}
                placeholder={orderForm.price_type === 'MKT' ? '市價' : '請輸入價格'}
                step="0.01"
              />
            </div>

            <div className="form-group">
              <label className="form-label">數量（股）*</label>
              <input
                type="number"
                name="quantity"
                className="form-input"
                value={orderForm.quantity}
                onChange={handleFormChange}
                required
                min="1000"
                step="1000"
              />
              <small className="form-help">
                台股最小交易單位為 1000 股（1 張）
              </small>
            </div>

            <div className="form-group">
              <label className="form-label">委託類型 *</label>
              <select
                name="order_type"
                className="form-select"
                value={orderForm.order_type}
                onChange={handleFormChange}
                required
              >
                <option value="ROD">當日有效 (ROD)</option>
                <option value="IOC">立即成交否則取消 (IOC)</option>
                <option value="FOK">全部成交否則取消 (FOK)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">委託條件 *</label>
              <select
                name="order_condition"
                className="form-select"
                value={orderForm.order_condition}
                onChange={handleFormChange}
                required
              >
                <option value="Cash">現股</option>
                <option value="MarginTrading">融資</option>
                <option value="ShortSelling">融券</option>
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button 
              type="submit" 
              className={`btn ${orderForm.action === 'Buy' ? 'btn-success' : 'btn-danger'} btn-large`}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="loading"></span>
                  下單中...
                </>
              ) : (
                <>
                  {orderForm.action === 'Buy' ? '🟢 買進' : '🔴 賣出'}
                </>
              )}
            </button>
          </div>
        </form>

        <div className="order-tips">
          <h4>💡 下單提示</h4>
          <ul>
            <li><strong>限價單 (LMT)</strong>: 指定價格進行買賣</li>
            <li><strong>市價單 (MKT)</strong>: 以當前市場價格成交</li>
            <li><strong>ROD</strong>: 委託當日有效，收盤前未成交自動取消</li>
            <li><strong>IOC</strong>: 立即成交否則取消，未成交部分取消</li>
            <li><strong>FOK</strong>: 全部成交否則取消，無法全部成交則取消</li>
          </ul>
        </div>
      </div>

      {/* 今日委託 */}
      <div className="card">
        <div className="card-header flex-between">
          <span>📋 今日委託</span>
          <button 
            className="btn btn-secondary btn-sm"
            onClick={loadTodayOrders}
          >
            🔄 重新整理
          </button>
        </div>

        {todayOrders.length > 0 ? (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>訂單編號</th>
                  <th>時間</th>
                  <th>股票代碼</th>
                  <th>買賣</th>
                  <th>類型</th>
                  <th>價格</th>
                  <th>數量</th>
                  <th>已成交</th>
                  <th>狀態</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {todayOrders.map((order, index) => (
                  <tr key={index}>
                    <td className="order-id">{order.order_id}</td>
                    <td>{order.order_time}</td>
                    <td>{order.stock_code}</td>
                    <td>
                      <span className={`badge ${order.action === 'Buy' ? 'badge-success' : 'badge-error'}`}>
                        {order.action === 'Buy' ? '買進' : '賣出'}
                      </span>
                    </td>
                    <td>{order.price_type}</td>
                    <td>{order.price || '市價'}</td>
                    <td>{order.quantity}</td>
                    <td>{order.filled_quantity || 0}</td>
                    <td>{getOrderStatusBadge(order.status)}</td>
                    <td>
                      {order.status === 'pending' && (
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleCancelOrder(order.order_id)}
                        >
                          取消
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="no-data">今日尚無委託紀錄</p>
        )}
      </div>
    </div>
  );
}

export default OrderPanel;
