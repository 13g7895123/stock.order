import React, { useRef, useState } from 'react';
import api from '../api';
import './LoginPanel.css';

function LoginPanel({ onLogin, loading }) {
  const [formData, setFormData] = useState({
    user_id: '',
    password: '',
    cert_password: '',
    cert_path: '',
    person_id: ''
  });
  const [message, setMessage] = useState(null);
  const [uploadMethod, setUploadMethod] = useState('file');
  const [certFile, setCertFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = async (file) => {
    if (!file) {
      return;
    }

    setMessage(null);
    setCertFile(file);
    setUploading(true);

    try {
      const response = await api.uploadCertificate(file);

      if (response.success && response.cert_path) {
        setFormData((prev) => ({
          ...prev,
          cert_path: response.cert_path
        }));

        setMessage({
          type: 'success',
          text: `憑證已上傳：${file.name}`
        });
      } else {
        setMessage({
          type: 'error',
          text: response?.message || '憑證上傳失敗，請再試一次'
        });
        setCertFile(null);
      }
    } catch (error) {
      console.error('Certificate upload error:', error);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || error.message || '憑證上傳失敗'
      });
      setCertFile(null);
      setFormData((prev) => ({
        ...prev,
        cert_path: ''
      }));
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer?.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleMethodChange = (value) => {
    setUploadMethod(value);
    if (value === 'path') {
      setCertFile(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage(null);

    if (!formData.cert_path) {
      setMessage({
        type: 'error',
        text: '請先上傳憑證檔案或輸入憑證路徑'
      });
      return;
    }

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
            請輸入真實帳號、密碼與憑證資訊以連線至富邦 Neo SDK
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
            <label className="form-label">憑證密碼 *</label>
            <input
              type="password"
              name="cert_password"
              className="form-input"
              value={formData.cert_password}
              onChange={handleChange}
              required
              placeholder="請輸入憑證密碼"
            />
            <small className="form-help">
              正式環境登入必須提供憑證密碼
            </small>
          </div>

          <div className="form-group">
            <label className="form-label">憑證取得方式</label>
            <div className="radio-group">
              <label className="radio-label">
                <input
                  type="radio"
                  value="file"
                  checked={uploadMethod === 'file'}
                  onChange={(event) => handleMethodChange(event.target.value)}
                />
                上傳憑證檔案
              </label>
              <label className="radio-label">
                <input
                  type="radio"
                  value="path"
                  checked={uploadMethod === 'path'}
                  onChange={(event) => handleMethodChange(event.target.value)}
                />
                輸入伺服器路徑
              </label>
            </div>
          </div>

          {uploadMethod === 'file' ? (
            <div className="form-group">
              <label className="form-label">上傳憑證檔案 *</label>
              <div
                className={`file-upload ${certFile ? 'active' : ''}`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pfx,.p12"
                  onChange={handleFileChange}
                />
                {uploading ? (
                  <div>
                    <span className="loading"></span>
                    <p>上傳中，請稍候...</p>
                  </div>
                ) : certFile ? (
                  <div>
                    <p>✓ 已選擇檔案</p>
                    <p className="file-name">{certFile.name}</p>
                    <small>點擊或重新拖曳以更換檔案</small>
                  </div>
                ) : (
                  <div>
                    <p>📁 點擊選擇檔案或拖曳至此</p>
                    <small>支援 .pfx, .p12 格式</small>
                  </div>
                )}
              </div>
              {formData.cert_path && (
                <small className="form-help">
                  憑證儲存路徑：{formData.cert_path}
                </small>
              )}
            </div>
          ) : (
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
                請輸入後端伺服器可存取的憑證檔案完整路徑
              </small>
            </div>
          )}

          <div className="form-actions">
            <button
              type="submit"
              className="btn btn-primary btn-block"
              disabled={loading || uploading}
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
            <li>需要真實的富邦證券帳號與對應憑證檔案 (.pfx / .p12)</li>
            <li>可直接上傳憑證檔案，系統會提供伺服器上的儲存路徑</li>
            <li>若伺服器已存在憑證，也可以改用輸入路徑的方式登入</li>
            <li>登入成功後即可使用所有行情、帳戶與交易功能</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default LoginPanel;
