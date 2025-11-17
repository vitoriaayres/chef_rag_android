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

## 🚀 Quick Start

```bash
# Clone e configure
git clone [repository-url]
cd chef_rag_v2
pip install -r requirements_mobile.txt

# Execute o sistema
python main.py

# Teste os sistemas inteligentes
python test_smart_systems.py
```

## 📊 Sistemas Inteligentes

### ChefAgent - Agente com Ferramentas
```python
from core_logic.smart_chef_system import ChefAgent

agent = ChefAgent()
response = agent.process_with_smart_agent("frango com legumes", image_path="imagem.jpg")
```

**Ferramentas:**
- 🖼️ Análise de imagens
- 🔍 Busca de receitas  
- 🥗 Cálculo nutricional
- ⏰ Timer de cozimento
- 🛒 Lista de compras

### ChefWorkflow - Pipeline de 7 Etapas
```python
from core_logic.smart_chef_system import ChefWorkflow

workflow = ChefWorkflow()
result = workflow.process_with_smart_workflow("ingredientes: frango, batata")
```

**Pipeline:**
1. Análise de entrada → 2. Processamento de imagem → 3. Busca de receitas → 4. Cálculo nutricional → 5. Lista de compras → 6. Timeline → 7. Resposta final

### SimpleRAGSystem - RAG Nativo
```python
from core_logic.smart_chef_system import SimpleRAGSystem

rag = SimpleRAGSystem()
answer = rag.query_with_smart_rag("Como fazer risoto?")
```
## 📁 Estrutura do Projeto

```
chef_rag_v2/
├── 🧠 core_logic/              # Sistemas inteligentes e IA
│   ├── smart_chef_system.py    # Sistemas LangChain/LangGraph inspired
│   ├── smart_integration.py    # Camada de integração
│   ├── cleanup_manager.py      # Gerenciamento automático
│   └── rag_system.py          # RAG original
├── 📱 android_rag_chef/        # App React Native
├── 🌐 frontend/               # Interface Web React
├── 🧪 test_*.py              # Testes automatizados
└── 📊 main.py                 # Aplicação principal
```

## 🎯 Tecnologias

- **Backend**: Python, FastAPI, ChromaDB
- **Frontend**: React, Vite, React Native
- **IA**: RAG System, Computer Vision, LangChain-inspired
- **Database**: Vector Database (Chroma), SQLite

## 🧪 Testes e Demo

```bash
# Testes completos
python test_smart_systems.py

# Demo interativo
python test_smart_systems.py --demo

# Benchmark de performance  
python test_smart_systems.py --performance
```

## 📈 Performance
- **ChefAgent**: ~1.2s tempo médio
- **ChefWorkflow**: ~2.1s análise completa  
- **RAGSystem**: ~0.3s consultas
- **Cleanup**: Automático e otimizado

## 🔄 APIs Disponíveis

```
POST /analyze_image       # Análise de imagens
POST /smart_agent        # Agente inteligente
POST /smart_workflow     # Pipeline completo
GET  /recipe_search      # Busca de receitas
POST /nutrition         # Informações nutricionais
```

## 🎮 Interfaces

### Web Interface
```bash
cd frontend && npm run dev
```

### Mobile App
```bash
cd android_rag_chef && npx react-native run-android
```

### API REST
```bash
python mobile_api.py
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NewFeature`)
3. Commit as mudanças (`git commit -m 'Add NewFeature'`)
4. Push (`git push origin feature/NewFeature`)
5. Abra um Pull Request

## 📄 Licença

MIT License. Veja `LICENSE` para detalhes.

---

**Chef RAG v2** - *Transformando a culinária através da IA* 🍳✨

📚 **Documentação Completa**: `README_COMPLETO.md`