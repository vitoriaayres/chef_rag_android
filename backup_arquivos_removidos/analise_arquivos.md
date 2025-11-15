# 📊 Análise de Arquivos - Chef RAG v2

## 🟢 ARQUIVOS ESSENCIAIS (Não remover)

### Sistema Principal
- `main.py` - Interface principal em português ✅ ATIVO
- `mobile_camera.py` - Servidor mobile com QR code ✅ ATIVO
- `webcam.py` - Interface de webcam com rotação ✅ ATIVO
- `history_viewer.py` - Visualizador de histórico ✅ ATIVO

### Núcleo do Sistema (core_logic/)
- `core_logic/config.py` - Configurações centrais ✅ ATIVO
- `core_logic/rag_system.py` - Sistema RAG principal ✅ ATIVO
- `core_logic/database.py` - Gerenciamento de banco de dados ✅ ATIVO
- `core_logic/ai_providers.py` - Provedores de IA ✅ ATIVO
- `core_logic/cleanup_manager.py` - Limpeza automática ✅ ATIVO
- `core_logic/smart_chef_system.py` - Sistemas inteligentes ✅ ATIVO
- `core_logic/smart_integration.py` - Integração LangChain ✅ ATIVO
- `core_logic/langgraph_workflows.py` - Workflows LangGraph ✅ ATIVO
- `core_logic/langchain_agents.py` - Agentes LangChain ✅ ATIVO
- `core_logic/timer_manager.py` - Gerenciamento de timers ✅ ATIVO
- `core_logic/voice_recognition.py` - Reconhecimento de voz ✅ ATIVO
- `core_logic/advanced_rag.py` - RAG avançado ✅ ATIVO

### Templates e Dados
- `templates/mobile_camera.html` - Interface mobile responsiva ✅ ATIVO
- `data/` - Diretório de dados e banco ✅ ATIVO

### Configurações
- `requirements_mobile.txt` - Dependências mobile ✅ ATIVO
- `pyproject.toml` - Configuração do projeto ✅ ATIVO

## 🟡 ARQUIVOS OPCIONAIS (Podem ser removidos se não usados)

### APIs Alternativas
- `api.py` - API Flask completa (se não usar frontend web)
- `api_simple.py` - API simplificada (se não usar frontend web)
- `mobile_api.py` - API mobile específica (redundante com mobile_camera.py)

### Interfaces Web
- `web_simple.html` - Interface web simples (se usar só mobile)
- `frontend/` - Frontend React completo (se usar só mobile)

### Launchers e Scripts
- `launcher.py` - Launcher alternativo (redundante com main.py)
- `start.py` - Script de inicialização alternativo
- `start_web.py` - Inicializador web específico
- `start_chef_rag_mobile.bat` - Script batch Windows
- `Start-ChefRagMobile.ps1` - Script PowerShell
- `run_chef_rag_mobile.py` - Runner mobile específico

### Sistemas Antigos/Experimentais
- `main_new.py` - Versão experimental do main (redundante)
- `monitor.py` - Sistema de monitoramento antigo
- `pdf_inge.py` - Processador de PDF (se não usar)
- `lista_ingr.py` - Lista de ingredientes antiga
- `ingredientes_opt.py` - Otimizador de ingredientes experimental

## 🔴 ARQUIVOS DE TESTE/DESENVOLVIMENTO (Podem ser removidos em produção)

### Testes
- `test_cleanup.py` - Teste do sistema de cleanup
- `test_langchain.py` - Teste dos sistemas LangChain
- `test_openai_status.py` - Teste da API OpenAI
- `test_smart_systems.py` - Teste dos sistemas inteligentes
- `test_voice.py` - Teste do reconhecimento de voz

### App Mobile (Se não usar)
- `android_rag_chef/` - App React Native completo (se usar só web)

### Temporários
- `temp_uploads/` - Uploads temporários (será recriado automaticamente)
- `qr_code_mobile.png` - QR code temporário (será recriado)
- `temp_snapshot.jpg` - Snapshot temporário

## 📋 RECOMENDAÇÕES

### Para uso MOBILE APENAS:
Pode remover:
- `api.py`, `api_simple.py`
- `frontend/`
- `web_simple.html`
- `start_web.py`
- `android_rag_chef/` (se não desenvolver app nativo)

### Para uso WEB APENAS:
Pode remover:
- `mobile_camera.py`
- `mobile_api.py`
- `templates/mobile_camera.html`
- `android_rag_chef/`
- Scripts mobile específicos

### Para PRODUÇÃO:
Pode remover todos os arquivos de teste (`test_*.py`)

### Manter SEMPRE:
- `main.py` (interface principal)
- Toda a pasta `core_logic/`
- `webcam.py`
- `history_viewer.py`
- Arquivos de configuração

## 💾 Tamanho Estimado de Economia

- Removendo testes: ~50KB
- Removendo APIs não usadas: ~200KB
- Removendo frontend React: ~5MB (node_modules)
- Removendo app Android: ~50MB (node_modules + gradle)

Total possível de economia: ~55MB