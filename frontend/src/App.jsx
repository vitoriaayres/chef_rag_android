import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import UserProfile from './UserProfile';
import RecipeResults from './RecipeResults';
import './index.css';

const App = () => {
  const [currentMode, setCurrentMode] = useState('select'); // 'select', 'webcam', 'upload', 'history', 'book', 'profile'
  const [isWebcamActive, setIsWebcamActive] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [bookStatus, setBookStatus] = useState(null);
  const [showProfile, setShowProfile] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [voiceStatus, setVoiceStatus] = useState(null);
  
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const fileInputRef = useRef(null);

  // Inicializar webcam
  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { width: 640, height: 480 } 
      });
      videoRef.current.srcObject = stream;
      streamRef.current = stream;
      setIsWebcamActive(true);
      setError(null);
    } catch (err) {
      setError('Erro ao acessar a webcam. Verifique as permissões.');
    }
  };

  // Parar webcam
  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setIsWebcamActive(false);
  };

  // Capturar imagem da webcam
  const captureImage = async () => {
    if (!videoRef.current) return;

    setIsProcessing(true);
    setError(null);

    try {
      // Criar canvas para capturar a imagem
      const canvas = document.createElement('canvas');
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      
      // Converter para blob
      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'webcam_capture.jpg');
        formData.append('source', 'webcam');

        try {
          const response = await axios.post('/api/analyze-ingredient', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          
          setResult(response.data);
          loadHistory(); // Atualizar histórico
        } catch (err) {
          setError('Erro ao analisar a imagem: ' + err.message);
        }
      }, 'image/jpeg', 0.8);
    } catch (err) {
      setError('Erro ao capturar imagem: ' + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  // Upload de arquivo
  const handleFileUpload = async (file) => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);
    formData.append('source', 'upload');

    try {
      const response = await axios.post('/api/analyze-ingredient', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setResult(response.data);
      loadHistory(); // Atualizar histórico
    } catch (err) {
      setError('Erro ao analisar a imagem: ' + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  // Carregar status do livro
  const loadBookStatus = async () => {
    try {
      const response = await axios.get('/api/book/status');
      setBookStatus(response.data);
    } catch (err) {
      console.error('Erro ao verificar status do livro:', err);
    }
  };

  // Upload do livro
  const uploadBook = async (file) => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);

    const formData = new FormData();
    formData.append('book', file);

    try {
      const response = await axios.post('/api/book/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      await loadBookStatus(); // Atualizar status
      setResult({
        type: 'book_upload',
        message: response.data.message,
        data: response.data
      });
    } catch (err) {
      setError('Erro no upload do livro: ' + (err.response?.data?.error || err.message));
    } finally {
      setIsProcessing(false);
    }
  };

  // Processar livro
  const processBook = async () => {
    setIsProcessing(true);
    setError(null);

    try {
      const response = await axios.post('/api/book/process');
      
      await loadBookStatus(); // Atualizar status
      setResult({
        type: 'book_process',
        message: response.data.message,
        data: response.data
      });
    } catch (err) {
      setError('Erro ao processar livro: ' + (err.response?.data?.error || err.message));
    } finally {
      setIsProcessing(false);
    }
  };

  // Carregar histórico
  const loadHistory = async () => {
    try {
      const response = await axios.get('/api/history');
      setHistory(response.data.recent_analyses || []);
      setStats(response.data.statistics || null);
    } catch (err) {
      console.error('Erro ao carregar histórico:', err);
    }
  };

  // === FUNÇÕES DE RECONHECIMENTO DE VOZ ===
  
  const checkVoiceStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/voice/status');
      const data = await response.json();
      setVoiceStatus(data);
      return data;
    } catch (error) {
      console.error('Erro ao verificar status de voz:', error);
      setVoiceStatus({ available: false, message: 'Erro de conexão' });
      return null;
    }
  };

  const startVoiceRecognition = async () => {
    setIsListening(true);
    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/voice/analyze-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          timeout: 5,
          phrase_limit: 10
        })
      });

      const data = await response.json();

      if (data.success) {
        setResult({
          type: 'voice',
          ingredient: data.ingredient,
          recipes: data.recipes,
          processing_time: data.processing_time
        });
      } else {
        setError(data.message || 'Erro no reconhecimento de voz');
      }
    } catch (error) {
      setError('Erro ao processar reconhecimento de voz: ' + error.message);
    } finally {
      setIsListening(false);
      setIsProcessing(false);
    }
  };

  // Drag and drop
  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    const imageFile = files.find(file => file.type.startsWith('image/'));
    
    if (imageFile) {
      handleFileUpload(imageFile);
    }
  };

  // Carregar histórico e status do livro ao montar componente
  useEffect(() => {
    loadHistory();
    loadBookStatus();
  }, []);

  // Verificar status de voz quando o modo voz é selecionado
  useEffect(() => {
    if (currentMode === 'voice' && voiceStatus === null) {
      checkVoiceStatus();
    }
  }, [currentMode]);

  // Limpar webcam ao desmontar
  useEffect(() => {
    return () => {
      stopWebcam();
    };
  }, []);

  const renderModeSelector = () => (
    <div className="mode-selector">
      <h2>🧑‍🍳 Chef RAG - Sistema Inteligente de Receitas</h2>
      <p style={{ textAlign: 'center', marginBottom: '1.5rem', color: '#666' }}>
        Escolha como você quer analisar seus ingredientes:
      </p>
      
      {/* Status do livro */}
      {bookStatus && (
        <div style={{ 
          background: bookStatus.is_ready ? '#d4edda' : '#fff3cd', 
          border: `1px solid ${bookStatus.is_ready ? '#c3e6cb' : '#ffeaa7'}`,
          borderRadius: '8px', 
          padding: '1rem', 
          marginBottom: '1.5rem',
          textAlign: 'center'
        }}>
          {bookStatus.is_ready ? (
            <div>
              <span style={{ color: '#155724' }}>✅ Sistema pronto!</span>
              <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem', color: '#155724' }}>
                Livro carregado: {bookStatus.processed_pages} páginas processadas
              </p>
            </div>
          ) : bookStatus.pdf_exists ? (
            <div>
              <span style={{ color: '#856404' }}>⚠️ Livro precisa ser processado</span>
              <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem', color: '#856404' }}>
                PDF encontrado, mas base de dados não criada
              </p>
            </div>
          ) : (
            <div>
              <span style={{ color: '#856404' }}>📚 Nenhum livro encontrado</span>
              <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem', color: '#856404' }}>
                Faça upload de um livro de receitas para começar
              </p>
            </div>
          )}
        </div>
      )}

      <div className="mode-buttons">
        <button 
          className="mode-button"
          onClick={() => setCurrentMode('webcam')}
          disabled={!bookStatus?.is_ready}
        >
          <span className="icon">📷</span>
          <h3>Webcam</h3>
          <p>Capturar ingredientes em tempo real</p>
        </button>
        
        <button 
          className="mode-button"
          onClick={() => setCurrentMode('upload')}
          disabled={!bookStatus?.is_ready}
        >
          <span className="icon">📁</span>
          <h3>Upload</h3>
          <p>Enviar foto do computador</p>
        </button>
        
        <button 
          className="mode-button"
          onClick={() => setCurrentMode('voice')}
          disabled={!bookStatus?.is_ready}
        >
          <span className="icon">🎤</span>
          <h3>Reconhecimento de Voz</h3>
          <p>Dite os ingredientes que você tem</p>
        </button>
      </div>
      
      <div className="mode-buttons" style={{ marginTop: '1rem' }}>
        <button 
          className="mode-button" 
          onClick={() => {
            setCurrentMode('history');
            loadHistory();
          }}
        >
          <span className="icon">📊</span>
          <h3>Ver Histórico</h3>
          <p>Análises anteriores e estatísticas</p>
        </button>
        
        <button 
          className="mode-button"
          onClick={() => setShowProfile(true)}
        >
          <span className="icon">👤</span>
          <h3>Meu Perfil</h3>
          <p>Preferências e configurações</p>
        </button>
        
        <button 
          className="mode-button"
          onClick={() => {
            setCurrentMode('book');
            loadBookStatus();
          }}
        >
          <span className="icon">📚</span>
          <h3>Gerenciar Livro</h3>
          <p>Upload ou processar livro de receitas</p>
        </button>
      </div>
    </div>
  );

  const renderWebcamMode = () => (
    <div className="capture-area">
      <div className="webcam-container">
        <h3>📷 Modo Webcam</h3>
        
        {!isWebcamActive ? (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <p>Clique no botão abaixo para iniciar a webcam</p>
            <button className="capture-button" onClick={startWebcam}>
              Iniciar Webcam
            </button>
          </div>
        ) : (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="webcam-video"
            />
            
            <div className="webcam-controls">
              <button 
                className="capture-button"
                onClick={captureImage}
                disabled={isProcessing}
              >
                📸 {isProcessing ? 'Analisando...' : 'Capturar e Analisar'}
              </button>
              
              <button 
                className="capture-button"
                onClick={stopWebcam}
                style={{ background: '#dc3545' }}
              >
                ⏹️ Parar
              </button>
            </div>
          </>
        )}
        
        <button 
          className="capture-button"
          onClick={() => setCurrentMode('select')}
          style={{ background: '#6c757d', marginTop: '1rem' }}
        >
          ⬅️ Voltar
        </button>
      </div>
    </div>
  );

  const renderVoiceMode = () => (
    <div className="capture-area">
      <div className="voice-container">
        <h3>🎤 Reconhecimento de Voz</h3>
        
        <div className="voice-status">
          {voiceStatus === null && (
            <div style={{ textAlign: 'center', padding: '1rem' }}>
              <button 
                className="capture-button"
                onClick={checkVoiceStatus}
                style={{ background: '#17a2b8' }}
              >
                🔧 Testar Microfone
              </button>
            </div>
          )}
          
          {voiceStatus && !voiceStatus.available && (
            <div className="error-message" style={{ 
              background: '#f8d7da', 
              color: '#721c24', 
              padding: '1rem', 
              borderRadius: '8px',
              margin: '1rem 0'
            }}>
              ❌ {voiceStatus.message}
            </div>
          )}
          
          {voiceStatus && voiceStatus.available && (
            <div className="success-message" style={{ 
              background: '#d4edda', 
              color: '#155724', 
              padding: '1rem', 
              borderRadius: '8px',
              margin: '1rem 0'
            }}>
              ✅ {voiceStatus.message}
            </div>
          )}
        </div>

        <div className="voice-controls" style={{ textAlign: 'center', padding: '2rem' }}>
          {isListening ? (
            <div>
              <div className="listening-indicator" style={{
                width: '80px',
                height: '80px',
                background: 'linear-gradient(45deg, #ff6b6b, #ee5a24)',
                borderRadius: '50%',
                margin: '0 auto 1rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '2rem',
                animation: 'pulse 1s infinite'
              }}>
                🎤
              </div>
              <p>🔴 Escutando... Fale agora!</p>
              <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
                Exemplo: "Tenho tomate, cebola e alho"
              </p>
            </div>
          ) : (
            <div>
              <div style={{
                width: '80px',
                height: '80px',
                background: 'linear-gradient(45deg, #667eea, #764ba2)',
                borderRadius: '50%',
                margin: '0 auto 1rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '2rem'
              }}>
                🎤
              </div>
              <p>Clique para começar a falar seus ingredientes</p>
              
              <button 
                className="capture-button"
                onClick={startVoiceRecognition}
                disabled={!voiceStatus?.available || isProcessing}
                style={{ 
                  background: voiceStatus?.available ? 'linear-gradient(45deg, #28a745, #20c997)' : '#6c757d',
                  fontSize: '1.1rem',
                  padding: '1rem 2rem'
                }}
              >
                {isProcessing ? '🧠 Processando...' : '🎙️ Iniciar Gravação'}
              </button>
              
              <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
                💡 <strong>Dica:</strong> Fale claramente e mencione todos os ingredientes que você tem
              </div>
            </div>
          )}
        </div>
        
        <button 
          className="capture-button"
          onClick={() => setCurrentMode('select')}
          style={{ background: '#6c757d', marginTop: '1rem' }}
        >
          ⬅️ Voltar
        </button>
      </div>
    </div>
  );

  const renderUploadMode = () => (
    <div className="capture-area">
      <h3>📁 Upload de Imagem</h3>
      
      <div 
        className="file-upload-area"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="upload-icon">📤</div>
        <p><strong>Clique aqui</strong> ou arraste uma imagem</p>
        <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
          Formatos aceitos: JPG, PNG, JPEG, GIF
        </p>
      </div>
      
      <input
        ref={fileInputRef}
        type="file"
        className="file-input"
        accept="image/*"
        onChange={(e) => {
          if (e.target.files[0]) {
            handleFileUpload(e.target.files[0]);
          }
        }}
      />
      
      <button 
        className="capture-button"
        onClick={() => setCurrentMode('select')}
        style={{ background: '#6c757d', marginTop: '1rem' }}
      >
        ⬅️ Voltar
      </button>
    </div>
  );

  const renderBookMode = () => (
    <div className="capture-area">
      <h3>📚 Gerenciamento do Livro de Receitas</h3>
      
      {bookStatus && (
        <div style={{ marginBottom: '2rem' }}>
          <h4>Status Atual:</h4>
          <div style={{ 
            background: bookStatus.is_ready ? '#d4edda' : bookStatus.pdf_exists ? '#fff3cd' : '#f8d7da',
            border: `1px solid ${bookStatus.is_ready ? '#c3e6cb' : bookStatus.pdf_exists ? '#ffeaa7' : '#f5c6cb'}`,
            borderRadius: '8px',
            padding: '1rem',
            marginBottom: '1rem'
          }}>
            {bookStatus.is_ready ? (
              <div>
                <strong style={{ color: '#155724' }}>✅ Sistema Pronto</strong>
                <p style={{ margin: '0.5rem 0', color: '#155724' }}>
                  Livro processado com {bookStatus.processed_pages} páginas na base de dados
                </p>
              </div>
            ) : bookStatus.pdf_exists ? (
              <div>
                <strong style={{ color: '#856404' }}>⚠️ Livro Não Processado</strong>
                <p style={{ margin: '0.5rem 0', color: '#856404' }}>
                  PDF encontrado ({bookStatus.total_pages} páginas), mas precisa ser processado para criar a base de dados vetorial
                </p>
                <button 
                  className="capture-button"
                  onClick={processBook}
                  disabled={isProcessing}
                  style={{ marginTop: '1rem' }}
                >
                  {isProcessing ? '⚙️ Processando...' : '⚙️ Processar Livro'}
                </button>
              </div>
            ) : (
              <div>
                <strong style={{ color: '#721c24' }}>❌ Nenhum Livro Encontrado</strong>
                <p style={{ margin: '0.5rem 0', color: '#721c24' }}>
                  Faça upload de um livro de receitas em PDF para começar
                </p>
              </div>
            )}
          </div>
        </div>
      )}
      
      <div style={{ marginBottom: '2rem' }}>
        <h4>Upload de Novo Livro:</h4>
        <div 
          className="file-upload-area"
          onDragOver={(e) => {
            e.preventDefault();
            e.currentTarget.classList.add('dragover');
          }}
          onDragLeave={(e) => {
            e.preventDefault();
            e.currentTarget.classList.remove('dragover');
          }}
          onDrop={(e) => {
            e.preventDefault();
            e.currentTarget.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            const pdfFile = files.find(file => file.type === 'application/pdf');
            
            if (pdfFile) {
              uploadBook(pdfFile);
            } else {
              setError('Por favor, selecione um arquivo PDF');
            }
          }}
          onClick={() => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.pdf';
            input.onchange = (e) => {
              if (e.target.files[0]) {
                uploadBook(e.target.files[0]);
              }
            };
            input.click();
          }}
        >
          <div className="upload-icon">📄</div>
          <p><strong>Clique aqui</strong> ou arraste um arquivo PDF</p>
          <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
            Livros de receitas em formato PDF
          </p>
        </div>
      </div>
      
      <div style={{ background: '#f8f9fa', padding: '1rem', borderRadius: '8px', marginBottom: '1rem' }}>
        <h4>ℹ️ Informações:</h4>
        <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>
          <li>O livro deve estar em formato PDF</li>
          <li>O processamento pode levar alguns minutos dependendo do tamanho</li>
          <li>Após o processamento, você poderá analisar ingredientes</li>
          <li>A base de dados vetorial é criada uma única vez por livro</li>
        </ul>
      </div>
      
      <button 
        className="capture-button"
        onClick={() => {
          setCurrentMode('select');
          setResult(null);
          setError(null);
        }}
        style={{ background: '#6c757d' }}
      >
        ⬅️ Voltar
      </button>
    </div>
  );

  const renderHistoryMode = () => (
    <div className="history-container">
      <h3>📊 Histórico de Análises</h3>
      
      {stats && (
        <div className="history-stats">
          <div className="stat-card">
            <h4>Total</h4>
            <div className="value">{stats.total_analyses || 0}</div>
          </div>
          <div className="stat-card">
            <h4>Webcam</h4>
            <div className="value">{stats.webcam_analyses || 0}</div>
          </div>
          <div className="stat-card">
            <h4>Upload</h4>
            <div className="value">{stats.folder_analyses || 0}</div>
          </div>
          <div className="stat-card">
            <h4>Sucessos</h4>
            <div className="value">{stats.successful_analyses || 0}</div>
          </div>
        </div>
      )}
      
      <div className="history-list">
        {history.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666', padding: '2rem' }}>
            Nenhuma análise encontrada. Comece analisando alguns ingredientes! 🥕
          </p>
        ) : (
          history.map((item, index) => (
            <div key={index} className="history-item">
              <div className="history-info">
                <h4>
                  {item.source_mode === 'webcam' ? '📷' : '📁'} {item.ingredient_identified}
                </h4>
                <p>{item.image_name || 'Captura da webcam'}</p>
              </div>
              <div className="history-time">
                {new Date(item.timestamp).toLocaleDateString('pt-BR', {
                  day: '2-digit',
                  month: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </div>
            </div>
          ))
        )}
      </div>
      
      <button 
        className="capture-button"
        onClick={() => setCurrentMode('select')}
        style={{ background: '#6c757d', marginTop: '1rem' }}
      >
        ⬅️ Voltar
      </button>
    </div>
  );

  const renderResults = () => {
    if (isProcessing) {
      return (
        <div className="results-container">
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>
              {result?.type === 'book_upload' && '📚 Fazendo upload do livro...'}
              {result?.type === 'book_process' && '⚙️ Processando livro e criando base de dados...'}
              {!result?.type && '🧠 Analisando ingrediente com IA...'}
            </p>
          </div>
        </div>
      );
    }

    if (result) {
      if (result.type === 'book_upload' || result.type === 'book_process') {
        return (
          <div className="results-container">
            <div className="recipe-result">
              <h3>
                {result.type === 'book_upload' ? '📚' : '⚙️'} {result.message}
              </h3>
              
              {result.data && (
                <div style={{ marginTop: '1rem' }}>
                  {result.data.total_pages && (
                    <p>📄 Total de páginas: {result.data.total_pages}</p>
                  )}
                  {result.data.total_pages_processed && (
                    <p>✅ Páginas processadas: {result.data.total_pages_processed}</p>
                  )}
                  {result.data.needs_processing && (
                    <p style={{ color: '#856404' }}>⚠️ O livro precisa ser processado antes de usar</p>
                  )}
                  {result.data.is_ready && (
                    <p style={{ color: '#155724' }}>🎉 Sistema pronto para análise de ingredientes!</p>
                  )}
                </div>
              )}
              
              <button 
                className="capture-button"
                onClick={() => {
                  setResult(null);
                  setError(null);
                  loadBookStatus();
                }}
                style={{ marginTop: '1rem' }}
              >
                🔄 Continuar
              </button>
            </div>
          </div>
        );
      }
      
      // Resultado normal de análise de ingrediente
      return (
        <RecipeResults 
          result={result}
          onBack={() => {
            setResult(null);
            setError(null);
          }}
        />
      );
    }

    return null;
  };

  return (
    <div className="app">
      <header className="header">
        <h1>
          🧑‍🍳 Chef RAG
        </h1>
      </header>
      
      <main className="main-content">
        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}
        
        {currentMode === 'select' && renderModeSelector()}
        {currentMode === 'webcam' && renderWebcamMode()}
        {currentMode === 'voice' && renderVoiceMode()}
        {currentMode === 'upload' && renderUploadMode()}
        {currentMode === 'history' && renderHistoryMode()}
        {currentMode === 'book' && renderBookMode()}
        
        {renderResults()}
      </main>
      
      {/* Modal do Perfil do Usuário */}
      {showProfile && (
        <UserProfile onClose={() => setShowProfile(false)} />
      )}
    </div>
  );
};

export default App;