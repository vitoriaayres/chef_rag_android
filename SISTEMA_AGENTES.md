# 🤖 Sistema de Agentes e Monitoramento - Chef RAG v2

## 📋 Visão Geral

O Chef RAG v2 agora inclui um sistema avançado de agentes inteligentes e monitoramento em tempo real com integração LangSmith para análise de custos e performance.

## 🔧 Funcionalidades Implementadas

### 🤖 **Sistema de Agentes**
- **Agente Culinário Principal**: Especialista em receitas e técnicas de cozinha
- **Agente Nutricional**: Especialista em análise nutricional e dietas
- **Sistema de Ferramentas**: Busca receitas, análise nutricional, dicas de preparo
- **Rastreamento de Custos**: Monitoramento automático de tokens e custos

### 📊 **Dashboard de Monitoramento**
- **Métricas em Tempo Real**: Custos, tokens, interações
- **Histórico de Sessões**: Análise de uso ao longo do tempo
- **Análise de Agentes**: Performance individual de cada agente
- **Integração LangSmith**: Visualização de dados de tracing
- **Configurações**: Limites de custo e alertas

### 🔗 **Integração LangSmith**
- **Rastreamento Automático**: Todas as interações são logadas
- **Análise de Performance**: Tempo de execução e qualidade
- **Custos Detalhados**: Breakdown por modelo e operação
- **Sessões Organizadas**: Agrupamento lógico de interações

## 🚀 Como Usar

### 1. **Configuração Inicial**

```bash
# 1. Instalar dependências
python scripts/instalar_dependencias_agentes.py

# 2. Configurar ambiente (.env)
OPENAI_API_KEY=sua_chave_openai
LANGCHAIN_API_KEY=sua_chave_langsmith  # Opcional
LANGCHAIN_PROJECT=chef-rag-v2
```

### 2. **Acessar Dashboard**

```bash
# Executar Chef RAG
python main.py

# Escolher opção 13: Dashboard de Monitoramento
```

### 3. **Usar Sistema de Agentes**

O sistema de agentes é integrado automaticamente em todas as funcionalidades:
- Busca de receitas com agente culinário
- Análise nutricional com agente especializado  
- Monitoramento transparente de custos
- Rastreamento automático no LangSmith

## 📊 Estrutura de Arquivos

```
core_logic/
├── agent_environment.py      # Sistema principal de agentes
├── config.py                # Configurações + LangSmith

interfaces/
├── interface_monitoring_dashboard.py  # Dashboard de monitoramento

scripts/
├── instalar_dependencias_agentes.py  # Instalador de dependências

.env.example                  # Template de configuração
```

## 💰 Monitoramento de Custos

### **Recursos de Custo**
- ✅ **Rastreamento em Tempo Real**: Custos por token e operação
- ✅ **Limites Configuráveis**: Alertas quando exceder limites
- ✅ **Breakdown Detalhado**: Input vs Output tokens
- ✅ **Histórico**: Evolução de custos ao longo do tempo
- ✅ **Exportação**: Relatórios em JSON

### **Preços Monitorados** (Nov 2025)
- **GPT-4o-mini**: $0.000150 input / $0.000600 output (por 1K tokens)
- **GPT-4o**: $0.005 input / $0.015 output (por 1K tokens)
- **text-embedding-3-small**: $0.00002 (por 1K tokens)

## 🔗 Integração LangSmith

### **O que é o LangSmith?**
- Plataforma de observabilidade para aplicações LLM
- Rastreamento detalhado de chains e agentes
- Análise de performance e debugging
- Dashboard web para visualização

### **Configuração LangSmith**

1. **Criar Conta**: https://smith.langchain.com/
2. **Obter API Key**: No painel de configurações
3. **Configurar .env**:
   ```env
   LANGCHAIN_API_KEY=lsv2_pt_...
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=chef-rag-v2
   ```

### **Dados Enviados ao LangSmith**
- **Inputs/Outputs**: Perguntas do usuário e respostas
- **Metadata**: Tipo de agente, custos, tokens
- **Timing**: Duração de execução
- **Session ID**: Agrupamento de interações

## 🛠️ Arquitetura Técnica

### **Componentes Principais**

1. **EnvironmentAgentSystem**
   - Gerenciador principal dos agentes
   - Rastreamento de sessões e custos
   - Integração com LangSmith

2. **Agentes Especializados**
   - Culinary Agent: Receitas e técnicas
   - Nutrition Agent: Análise nutricional
   - Ferramentas: Busca, análise, dicas

3. **Sistema de Callbacks**
   - ChefRAGCostCallback: Rastreamento de tokens
   - LangSmith Tracing: Logs automáticos

4. **MonitoringDashboard**
   - Interface Tkinter com matplotlib
   - Métricas em tempo real
   - Controles de configuração

### **Fluxo de Dados**
```
Usuário → Agent System → LLM → Callback → Dashboard
                      ↓
                  LangSmith ← Session Tracking
```

## 📈 Métricas Disponíveis

### **Sessão Atual**
- Custo total em USD
- Tokens input/output
- Número de interações
- Tipos de agentes utilizados
- Tempo de execução

### **Histórico**
- Evolução de custos
- Performance dos agentes
- Padrões de uso
- Sessões anteriores

## 🎯 Benefícios

### **Para Desenvolvimento**
- 🔍 **Debugging**: Rastreamento detalhado de chains
- 📊 **Analytics**: Métricas de performance
- 💰 **Controle de Custos**: Monitoramento preciso
- 🔧 **Otimização**: Identificação de gargalos

### **Para Produção**
- 📈 **Observabilidade**: Visibilidade completa
- 🚨 **Alertas**: Notificações de limites
- 📋 **Relatórios**: Exportação de dados
- 🔄 **Escalabilidade**: Preparado para crescimento

## 🚀 Roadmap Futuro

### **Próximas Funcionalidades**
- [ ] Agentes especializados adicionais
- [ ] A/B testing de prompts
- [ ] Análise de sentiment
- [ ] Otimização automática de custos
- [ ] Dashboards web personalizados
- [ ] Integração com mais LLMs

### **Melhorias Planejadas**
- [ ] Cache inteligente para reduzir custos
- [ ] Batch processing para eficiência
- [ ] Rate limiting adaptativo
- [ ] Modelos locais para economia

---

## 📞 Suporte

Para dúvidas sobre o sistema de agentes:
1. **Documentação**: Veja este arquivo
2. **Logs**: Dashboard → Aba "Tempo Real"
3. **LangSmith**: https://smith.langchain.com/ (se configurado)
4. **Issues**: GitHub do projeto

---

**Desenvolvido por: Vitória Ayres**  
**Chef RAG v2 - Sistema de Assistência Culinária Inteligente**