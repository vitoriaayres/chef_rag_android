@echo off
echo ========================================
echo   Chef RAG Mobile - Iniciando Sistema
echo ========================================

cd /d "C:\Users\Interfocus\Desktop\projetos_pessoais\chef_rag_v2"

echo.
echo 🚀 Iniciando API Backend...
start "Chef RAG API" python mobile_api.py

echo.
echo ⏳ Aguardando API inicializar...
timeout /t 3 /nobreak > nul

cd android_rag_chef

echo.
echo 📱 Iniciando Metro Bundler...
start "Metro Bundler" npm start

echo.
echo ✅ Ambos os serviços foram iniciados!
echo.
echo 📱 Metro Bundler: Abriu em janela separada
echo 🌐 API Backend: http://localhost:5000/api/health
echo.
echo Para testar a API, acesse: http://localhost:5000/api/health
echo Para desenvolvimento mobile, use o Metro no terminal aberto.
echo.
pause