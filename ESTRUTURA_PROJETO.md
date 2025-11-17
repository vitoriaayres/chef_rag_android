# 📁 Estrutura do Projeto - Chef RAG v2

## 🏗️ Organização de Arquivos

```
chef_rag_v2/
├── 📄 main.py                     # Arquivo principal do sistema
├── 📄 requirements.txt            # Dependências Python
├── 📄 pyproject.toml             # Configurações do projeto
├── 📄 README.md                  # Documentação principal
├── 📄 receitas_estruturadas.csv  # Base de dados de receitas
├── 
├── 🗂️ interfaces/                # 🖥️ Interfaces Gráficas
│   ├── interface_calculadora_calorias.py
│   ├── interface_cozinha_passo_passo.py
│   ├── interface_cozinha_passo_passo_v2.py
│   ├── interface_cronometros_cozinha.py
│   ├── interface_filtros_dieta.py
│   ├── interface_ingredientes_manual.py
│   ├── interface_perfil_usuario.py
│   ├── interface_principal_chef.py
│   ├── interface_upload_foto.py
│   └── interface_verificador_alergias.py
│
├── 🗂️ vision/                    # 📷 Processamento de Imagens
│   ├── camera_mobile.py          # Servidor mobile para câmera
│   ├── webcam.py                 # Câmera padrão
│   └── webcam_yolo.py            # Câmera com YOLO
│
├── 🗂️ audio/                     # 🎤 Reconhecimento de Voz
│   ├── reconhecimento_voz_simples.py
│   ├── reconhecimento_voz_simples_corrigida.py
│   └── reconhecimento_voz_grafico.py
│
├── 🗂️ scripts/                   # 🔧 Scripts Utilitários
│   ├── sistema_busca_csv.py      # Sistema de busca
│   ├── visualizador_historico.py # Visualizador de histórico
│   └── instalar_dependencias_voz.py
│
├── 🗂️ core_logic/                # 🧠 Lógica Principal
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── sistema_rag.py
│   ├── agentes_langchain.py
│   ├── fluxos_trabalho_langgraph.py
│   ├── gerenciador_limpeza.py
│   ├── gerenciador_timer.py
│   ├── integracao_inteligente.py
│   ├── provedores_ia.py
│   ├── rag_avancado.py
│   ├── reconhecimento_voz.py
│   ├── sistema_chef_inteligente.py
│   └── chroma_db/
│
├── 🗂️ data/                      # 📊 Dados e Assets
│   ├── imagens/
│   ├── pdf/
│   └── history_export.json
│
├── 🗂️ frontend/                  # 🌐 Interface Web
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│
├── 🗂️ android_rag_chef/          # 📱 App Android
│   ├── android/
│   ├── ios/
│   ├── src/
│   ├── app.json
│   ├── package.json
│   └── ...
│
├── 🗂️ templates/                 # 📋 Templates
└── 🗂️ temp_uploads/              # 📁 Uploads Temporários
```

## 🎯 Categorização por Funcionalidade

### 🖥️ **interfaces/** - Interface Gráfica
- Todas as interfaces Tkinter
- Calculadora de calorias com aba de créditos
- Interfaces de passo-a-passo de receitas
- Cronômetros e filtros

### 📷 **vision/** - Processamento Visual
- Câmera do PC e mobile
- Processamento YOLO
- Análise de imagens

### 🎤 **audio/** - Processamento de Áudio
- Reconhecimento de voz
- Interfaces de áudio
- Scripts de voz

### 🔧 **scripts/** - Utilitários
- Sistema de busca CSV
- Visualizadores
- Scripts de instalação

### 🧠 **core_logic/** - Lógica Central
- Sistema RAG
- Banco de dados
- Agentes de IA
- Configurações

## 🚀 Como Executar

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Executar sistema principal
python main.py
```

## 📝 Desenvolvido por

**Vitória Ayres** - Sistema de Assistência Culinária Inteligente

### 🛠️ Tecnologias Utilizadas
- Python, LangChain, ChromaDB
- OpenCV, YOLO, Tkinter
- SQLite, Pandas, Flask
- Speech Recognition, RAG