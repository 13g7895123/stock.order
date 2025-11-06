import React, { useState } from 'react';
import './LoginPanel.css';

function LoginPanel({ onLogin, loading, currentEnv }) {
  const [formData, setFormData] = useState({
    user_id: 'test_user',
    password: 'test_password',
    cert_path: '/tmp/test.pfx',
    person_id: '',
    cert_password: ''
  });
  const [certFile, setCertFile] = useState(null);
  const [message, setMessage] = useState(null);
  const [uploadMethod, setUploadMethod] = useState('path'); // 'path' or 'file'

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setCertFile(file);
      // 實際應用中，這裡需要將檔案上傳到後端
      // 暫時使用檔案名稱作為路徑
      setFormData({
        ...formData,
        cert_path: `/uploaded/${file.name}`
      });
      setMessage({
        type: 'info',
        text: `已選擇憑證檔案: ${file.name} (實際使用時需上傳到伺服器)`
      });
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setCertFile(file);
      setFormData({
        ...formData,
        cert_path: `/uploaded/${file.name}`
      });
      setMessage({
        type: 'info',
        text: `已選擇憑證檔案: ${file.name}`
      });
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);

    const result = await onLogin(formData);
    
    setMessage({
      type: result.success ? 'success' : 'error',
      text: result.message
    });
  };

  return (
    <div className="login-panel">
      <div className="card login-card">
        <div className="login-header">
          <h2>🔐 登入富邦證券</h2>
          <p className="text-muted">
            {currentEnv === 'test' ? '測試模式：可使用任意帳號密碼登入' : '正式模式：需要真實的帳號和憑證'}
          </p>
        </div>

        {message && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">使用者帳號 *</label>
            <input
              type="text"
              name="user_id"
              className="form-input"
              value={formData.user_id}
              onChange={handleChange}
              required
              placeholder="請輸入使用者帳號"
            />
          </div>

          <div className="form-group">
            <label className="form-label">密碼 *</label>
            <input
              type="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="請輸入密碼"
            />
          </div>

          <div className="form-group">
            <label className="form-label">身分證字號</label>
            <input
              type="text"
              name="person_id"
              className="form-input"
              value={formData.person_id}
              onChange={handleChange}
              placeholder="選填"
            />
          </div>

          <div className="form-group">
            <label className="form-label">憑證密碼 {currentEnv === 'production' ? '*' : ''}</label>
            <input
              type="password"
              name="cert_password"
              className="form-input"
              value={formData.cert_password}
              onChange={handleChange}
              placeholder={currentEnv === 'production' ? '正式環境必填' : '測試環境可留空'}
              required={currentEnv === 'production'}
            />
            <small className="form-help">
              正式環境登入需要提供對應的憑證密碼
            </small>
          </div>

          {/* 憑證上傳方式選擇 */}
          <div className="form-group">
            <label className="form-label">憑證設定方式</label>
            <div className="radio-group">
              <label className="radio-label">
                <input
                  type="radio"
                  value="path"
                  checked={uploadMethod === 'path'}
                  onChange={(e) => setUploadMethod(e.target.value)}
                />
                輸入憑證路徑
              </label>
              <label className="radio-label">
                <input
                  type="radio"
                  value="file"
                  checked={uploadMethod === 'file'}
                  onChange={(e) => setUploadMethod(e.target.value)}
                />
                上傳憑證檔案
              </label>
            </div>
          </div>

          {uploadMethod === 'path' ? (
            <div className="form-group">
              <label className="form-label">憑證路徑 *</label>
              <input
                type="text"
                name="cert_path"
                className="form-input"
                value={formData.cert_path}
                onChange={handleChange}
                required
                placeholder="/path/to/certificate.pfx"
              />
              <small className="form-help">
                請輸入伺服器上憑證檔案的完整路徑
              </small>
            </div>
          ) : (
            <div className="form-group">
              <label className="form-label">上傳憑證檔案 *</label>
              <div
                className={`file-upload ${certFile ? 'active' : ''}`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => document.getElementById('cert-file').click()}
              >
                <input
                  id="cert-file"
                  type="file"
                  accept=".pfx,.p12"
                  onChange={handleFileChange}
                />
                {certFile ? (
                  <div>
                    <p>✓ 已選擇檔案</p>
                    <p className="file-name">{certFile.name}</p>
                    <small>點擊重新選擇</small>
                  </div>
                ) : (
                  <div>
                    <p>📁 點擊選擇檔案或拖曳至此</p>
                    <small>支援 .pfx, .p12 格式</small>
                  </div>
                )}
              </div>
              <small className="form-help">
                ⚠️ 測試模式下檔案不會真的上傳，僅用於演示
              </small>
            </div>
          )}

          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary btn-block"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="loading"></span>
                  登入中...
                </>
              ) : (
                '登入'
              )}
            </button>
          </div>
        </form>

        <div className="login-tips">
          <h4>💡 使用提示</h4>
          <ul>
            <li><strong>測試模式</strong>：任意帳號密碼即可登入，使用 Mock 資料</li>
            <li><strong>正式模式</strong>：需要真實的富邦證券帳號和憑證檔案</li>
            <li>憑證檔案格式：.pfx 或 .p12</li>
            <li>登入後可以測試所有 API 功能</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default LoginPanel;
