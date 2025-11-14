# 🍳 Chef RAG v2 - Sistema Inteligente de Culinária

Um sistema avançado de assistente culinário que combina Inteligência Artificial, sistemas inspirados no LangChain/LangGraph, RAG (Retrieval-Augmented Generation) e análise de imagens para oferecer uma experiência culinária completa e personalizada.

## ✨ Principais Funcionalidades

### 🧠 Sistemas Inteligentes (LangChain/LangGraph Inspired)
- **ChefAgent**: Agente inteligente com ferramentas especializadas
- **ChefWorkflow**: Pipeline de processamento de 7 etapas
- **SimpleRAGSystem**: Sistema RAG avançado para consultas inteligentes
- **ChefMemory**: Gerenciamento de memória e contexto

### 📱 Interfaces Múltiplas
- **Web Interface**: React/Vite moderna
- **Mobile App**: React Native multiplataforma  
- **API REST**: APIs completas para integração
- **CLI**: Interface de linha de comando

### 🔍 IA Avançada
- Análise inteligente de imagens de alimentos
- Reconhecimento de ingredientes por foto
- Sugestões de receitas personalizadas
- Cálculo automático de nutrição
- Geração de listas de compras
- Timer inteligente para receitas

## 🏗️ Arquitetura

```
Chef RAG System
├── 🐍 Backend Python
│   ├── Google Gemini (Vision + Text)
│   ├── ChromaDB (Banco Vetorial)
│   ├── SQLite (Histórico)
│   └── Flask API
├── ⚛️ Frontend React
│   ├── Captura Webcam
│   ├── Upload de Arquivos
│   └── Visualização de Histórico
└── 📚 Base de Conhecimento
    └── Livro de Receitas (PDF)
```

## 🚀 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.10+
- Node.js 16+
- Webcam (opcional)

### 2. Configurar Backend

```bash
# 1. Clonar repositório
git clone [url-do-repo]
cd chef_rag_v2

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente (Windows)
.\venv\Scripts\activate

# 4. Instalar dependências Python
pip install python-dotenv pdfplumber google-generativeai watchdog pillow chromadb flask flask-cors opencv-python

# 5. Configurar variáveis de ambiente
# Criar arquivo .env com:
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env
```

### 3. Configurar Frontend

```bash
# Navegar para pasta frontend
cd frontend

# Instalar dependências
npm install

# Voltar para raiz
cd ..
```

### 4. Processar Livro de Receitas

```bash
# Colocar livro PDF em data/pdf/livro.pdf
# Executar processamento
python pdf_inge.py
```

## 🎮 Como Usar

### Opção 1: Sistema Completo (Recomendado)

```bash
python start.py
```

Escolha opção 1 para iniciar API + Frontend automaticamente.

### Opção 2: Separadamente

**Terminal 1 - API:**
```bash
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Opção 3: Sistema Original (Terminal)

```bash
python main.py
```

## 📖 Guia de Uso

### 🌐 Interface Web (http://localhost:3000)

1. **Modo Webcam**:
   - Clique em "Webcam"
   - Permita acesso à câmera
   - Posicione ingrediente na frente da câmera
   - Clique "Capturar e Analisar"

2. **Modo Upload**:
   - Clique em "Upload"
   - Arraste imagem ou clique para selecionar
   - Aguarde análise automática

3. **Histórico**:
   - Visualize todas as análises anteriores
   - Veja estatísticas de uso
   - Busque por ingredientes específicos

### 🐍 Sistema Terminal

1. Escolha modo (Webcam/Pasta/Histórico)
2. Para webcam: pressione 'E' para capturar
3. Para pasta: coloque imagens em `data/imagens/`
4. Veja sugestões em tempo real

## 📁 Estrutura do Projeto

```
chef_rag_v2/
├── 📄 api.py                 # API Flask
├── 📄 start.py               # Script de inicialização
├── 📄 main.py                # Sistema Python original
├── 📄 .env                   # Variáveis de ambiente
├── 📄 .gitignore             # Arquivos ignorados
├── 🗂️ core_logic/           # Lógica principal
│   ├── config.py            # Configurações
│   ├── rag_system.py        # Sistema RAG
│   ├── database.py          # Banco de histórico
│   └── chroma_db/           # Banco vetorial
├── 🗂️ data/                 # Dados
│   ├── pdf/livro.pdf        # Livro de receitas
│   ├── imagens/             # Imagens para análise
│   └── history.db           # Histórico SQLite
├── 🗂️ frontend/             # Interface web
│   ├── src/App.jsx          # Componente principal
│   ├── src/index.css        # Estilos
│   └── package.json         # Dependências
└── 🗂️ venv/                 # Ambiente virtual
```

## 🔧 Configuração da API Google

1. Acesse [Google AI Studio](https://aistudio.google.com/)
2. Crie um projeto e gere uma API key
3. Adicione no arquivo `.env`:
   ```
   GOOGLE_API_KEY=sua_chave_aqui
   ```

## 📊 Dados Armazenados

- **ChromaDB**: Embeddings das receitas do livro
- **SQLite**: Histórico de análises com timestamps
- **Arquivos**: PDFs, imagens temporárias

## 🛡️ Privacidade

- Imagens são processadas localmente
- Histórico fica no seu computador
- Apenas texto é enviado para Google Gemini
- Nenhum dado pessoal é compartilhado

## 🔗 Endpoints da API

- `GET /api/health` - Status da API
- `POST /api/analyze-ingredient` - Analisar imagem
- `GET /api/history` - Buscar histórico
- `GET /api/statistics` - Estatísticas
- `GET /api/history/search?ingredient=X` - Busca específica

## 🐛 Solução de Problemas

### Erro: "Webcam não encontrada"
- Verificar permissões do navegador
- Testar com outro navegador
- Verificar se câmera funciona em outros apps

### Erro: "Chave da API inválida"
- Verificar arquivo `.env`
- Confirmar chave no Google AI Studio
- Reiniciar aplicação

### Erro: "Módulo não encontrado"
- Ativar ambiente virtual: `.\venv\Scripts\activate`
- Reinstalar dependências: `pip install -r requirements.txt`

### Frontend não inicia
- Verificar se Node.js está instalado
- Executar `npm install` na pasta frontend
- Verificar se porta 3000 está livre

## 🤝 Contribuindo

1. Fork do projeto
2. Criar branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Pull Request

## 📝 Licença

MIT License - veja arquivo LICENSE para detalhes.

## 🙏 Créditos

- **Google Gemini**: IA para visão computacional e geração de texto
- **ChromaDB**: Banco de dados vetorial
- **React**: Framework frontend
- **Flask**: Framework API
- **OpenCV**: Captura de webcam

---

Desenvolvido com ❤️ para transformar ingredientes em receitas incríveis! 🧑‍🍳✨