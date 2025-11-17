# 🍳 Chef RAG v2 - Sistema Inteligente de Culinária

## Visão Geral

Chef RAG v2 é um sistema avançado de assistente culinário que combina Inteligência Artificial, Reconhecimento de Imagens, RAG (Retrieval-Augmented Generation) e sistemas inteligentes inspirados no LangChain/LangGraph para fornecer uma experiência culinária personalizada e interativa.

## 🚀 Características Principais

### 🧠 Sistemas Inteligentes (LangChain/LangGraph Inspired)
- **ChefAgent**: Sistema de agente inteligente com ferramentas especializadas
- **ChefWorkflow**: Pipeline de processamento de 7 etapas
- **SimpleRAGSystem**: Sistema RAG avançado para consultas inteligentes
- **ChefMemory**: Gerenciamento de memória e contexto

### 📱 Interfaces Múltiplas
- **Web Interface**: Interface web moderna com React/Vite
- **Mobile App**: Aplicativo React Native multiplataforma
- **API REST**: APIs completas para integração
- **CLI**: Interface de linha de comando

### 🔍 Capacidades de IA
- Análise inteligente de imagens de alimentos
- Reconhecimento de ingredientes por foto
- Sugestões de receitas personalizadas
- Cálculo automático de nutrição
- Geração de listas de compras
- Timer inteligente para receitas

## 📁 Estrutura do Projeto

```
chef_rag_v2/
├── 🧠 core_logic/              # Lógica principal e sistemas inteligentes
│   ├── smart_chef_system.py    # Sistemas LangChain/LangGraph inspirados
│   ├── smart_integration.py    # Camada de integração
│   ├── cleanup_manager.py      # Gerenciamento automático de imagens
│   ├── rag_system.py          # Sistema RAG original
│   ├── ai_providers.py        # Provedores de IA
│   ├── voice_recognition.py   # Reconhecimento de voz
│   ├── timer_manager.py       # Gerenciamento de timers
│   └── database.py            # Gerenciamento de banco de dados
├── 📱 android_rag_chef/        # App React Native
├── 🌐 frontend/               # Interface Web React
├── 🧪 test_*.py              # Testes automatizados
├── 🚀 main.py                 # Aplicação principal
└── 📊 monitor.py             # Monitoramento do sistema
```

## 🛠 Instalação e Configuração

### Pré-requisitos
```bash
# Python 3.8+
pip install -r requirements_mobile.txt

# Node.js para frontend
npm install
```

### Configuração
1. Clone o repositório
2. Configure as variáveis de ambiente no arquivo `.env`
3. Instale as dependências Python
4. Execute o sistema

## 🎯 Uso

### Sistema Principal
```bash
python main.py
```

### Sistemas Inteligentes
```python
from core_logic.smart_chef_system import ChefAgent, ChefWorkflow, SimpleRAGSystem

# Usando o Agente Inteligente
agent = ChefAgent()
response = agent.process_with_smart_agent("frango com legumes", image_path="imagem.jpg")

# Usando o Workflow
workflow = ChefWorkflow()
result = workflow.process_with_smart_workflow("ingredientes: frango, batata", image_path="imagem.jpg")

# Usando RAG System
rag = SimpleRAGSystem()
answer = rag.query_with_smart_rag("Como fazer risoto?")
```

### Testes
```bash
# Testar todos os sistemas
python test_smart_systems.py

# Demo interativo
python test_smart_systems.py --demo

# Comparação de performance
python test_smart_systems.py --performance
```

## 🧠 Sistemas Inteligentes Detalhados

### ChefAgent - Agente Inteligente
Sistema inspirado no LangChain que utiliza ferramentas especializadas:

**Ferramentas Disponíveis:**
- 🖼️ **Image Analysis Tool**: Análise de imagens de alimentos
- 🔍 **Recipe Search Tool**: Busca inteligente de receitas
- 🥗 **Nutrition Calculator**: Cálculo de informações nutricionais
- ⏰ **Timer Tool**: Gerenciamento de timers de cozimento
- 🛒 **Shopping List Tool**: Geração de listas de compras

**Capacidades:**
- Análise contextual de entrada
- Seleção automática de ferramentas
- Execução sequencial inteligente
- Formatação de resposta estruturada

### ChefWorkflow - Pipeline Inteligente
Sistema inspirado no LangGraph com pipeline de 7 etapas:

**Etapas do Workflow:**
1. 🔍 **Input Analysis**: Análise da entrada do usuário
2. 🖼️ **Image Processing**: Processamento de imagens (se fornecidas)
3. 🍽️ **Recipe Search**: Busca de receitas relevantes
4. 🥗 **Nutrition Calculation**: Cálculo nutricional
5. 🛒 **Shopping List Generation**: Geração de lista de compras
6. ⏰ **Timeline Creation**: Criação de cronograma de preparo
7. 📋 **Response Generation**: Formatação da resposta final

**Características:**
- Processamento sequencial otimizado
- Validação entre etapas
- Fallback para sistemas anteriores
- Métricas de performance detalhadas

### SimpleRAGSystem - RAG Inteligente
Sistema RAG nativo para consultas contextuais:

**Funcionalidades:**
- 🗄️ Base de conhecimento culinário
- 🔍 Busca por similaridade
- 📊 Scoring de relevância
- 🧠 Geração de respostas contextuais

**Características:**
- Sem dependências externas
- Alta performance
- Respostas precisas e relevantes
- Integração com outros sistemas

### ChefMemory - Gerenciamento de Memória
Sistema de memória e contexto:

**Capacidades:**
- 💾 Buffer de conversação
- 🔍 Recuperação de contexto
- 📈 Histórico de interações
- 🎯 Personalização baseada em histórico

## 📊 Métricas e Performance

### Benchmarks
- **ChefAgent**: ~1.2s tempo médio de resposta
- **ChefWorkflow**: ~2.1s para análise completa
- **SimpleRAGSystem**: ~0.3s para consultas
- **Memory Operations**: ~0.1s para recuperação

### Recursos Utilizados
- CPU: Otimizado para uso eficiente
- Memória: Sistema de cache inteligente
- Storage: Cleanup automático de imagens temporárias

## 🔄 Integração e APIs

### API Endpoints
```
POST /analyze_image       # Análise de imagens
POST /smart_agent        # Processamento com agente
POST /smart_workflow     # Pipeline completo
GET  /recipe_search      # Busca de receitas
POST /nutrition         # Cálculo nutricional
```

### Mobile Integration
- Interface nativa React Native
- Câmera integrada para análise de imagens
- Sincronização com sistema principal
- Notificações push para timers

## 🧪 Testes e Qualidade

### Cobertura de Testes
- ✅ Testes unitários para todos os sistemas
- ✅ Testes de integração
- ✅ Testes de performance
- ✅ Testes de UI/UX

### Continuous Integration
- Verificação automática de código
- Testes em múltiplas plataformas
- Validação de performance
- Cleanup automático de recursos

## 🚀 Implantação

### Desenvolvimento Local
```bash
python main.py
```

### Produção
```bash
python start.py --production
```

### Docker
```bash
docker build -t chef-rag-v2 .
docker run -p 8000:8000 chef-rag-v2
```

## 📈 Roadmap

### Próximas Funcionalidades
- 🛒 **Lista de Compras Automática**: Sistema avançado de geração automática
- 📊 **Dashboard de Estatísticas**: Analytics e métricas de uso
- 🔗 **Integração com Supermercados**: APIs para preços e disponibilidade
- 🤖 **IA Conversacional**: Chatbot avançado
- 🌐 **Multi-idiomas**: Suporte internacional

### Melhorias Técnicas
- Performance optimization
- Escalabilidade horizontal
- Monitoramento avançado
- Segurança aprimorada

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente e teste
4. Envie um Pull Request

### Padrões de Código
- Python: PEP 8
- JavaScript: ESLint + Prettier
- Documentação: Docstrings obrigatórias
- Testes: Cobertura mínima de 80%

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 📞 Contato e Suporte

- **Issues**: Use o GitHub Issues para bugs e sugestões
- **Documentação**: Wiki do projeto
- **Comunidade**: Discord/Telegram (links em breve)

---

## 🏆 Destaques Técnicos

### Inovações Implementadas
1. **Sistemas Nativos Inspirados em LangChain/LangGraph**: Implementação completa sem dependências externas
2. **Pipeline de 7 Etapas**: Processamento inteligente e otimizado
3. **RAG System Nativo**: Busca contextual avançada
4. **Cleanup Automático**: Gerenciamento inteligente de recursos
5. **Múltiplas Interfaces**: Web, Mobile, CLI e API

### Diferenciais Competitivos
- ⚡ **Performance Superior**: Sistemas otimizados para baixa latência
- 🔧 **Flexibilidade**: Múltiplas opções de integração
- 🧠 **Inteligência**: IA avançada para culinária
- 📱 **Multiplataforma**: Funciona em qualquer dispositivo
- 🔄 **Escalável**: Arquitetura preparada para crescimento

---

*Chef RAG v2 - Transformando a experiência culinária através da Inteligência Artificial* 🍳✨