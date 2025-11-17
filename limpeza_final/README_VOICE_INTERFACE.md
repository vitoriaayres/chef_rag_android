# 🎤 Interface de Voz Avançada - Chef RAG v2

## 🌟 Funcionalidades

### 🎯 **Reconhecimento de Voz Inteligente**
- **Múltiplas Engines**: Google Speech-to-Text + CMU Sphinx (offline)
- **Tempo Real**: Visualização durante gravação
- **Alta Precisão**: Otimizado para português brasileiro

### 📊 **Métricas Avançadas**
- **Acurácia Visual**: Percentual de confiança em tempo real
- **Tempo de Processamento**: Monitoramento de performance
- **Histórico Detalhado**: Todos os reconhecimentos salvos
- **Gráficos Interativos**: Evolução da acurácia ao longo do tempo

### 📄 **Integração com PDF**
- **Extração de Texto**: Análise automática de receitas em PDF
- **Comparação Inteligente**: Voz vs PDF de ingredientes
- **Relatório de Compatibilidade**: Análise de similaridade

### 💾 **Sistema de Histórico**
- **Persistência**: Histórico salvo automaticamente
- **Filtros Avançados**: Por período, acurácia, etc.
- **Exportação**: Dados em formato JSON
- **Estatísticas**: Gráficos de performance

## 🚀 Como Usar

### 1️⃣ **Instalação Automática**
```bash
python install_voice_deps.py
```

### 2️⃣ **Instalação Manual**
```bash
pip install -r requirements_voice.txt
```

### 3️⃣ **Executar Interface**
```bash
python main.py
# Escolha opção 5: "🎤 Interface de Voz Avançada"
```

## 🎛️ Interface Principal

### 📱 **Aba Reconhecimento**
- **🎤 Iniciar Gravação**: Botão principal para começar
- **🛑 Parar**: Finaliza gravação
- **🧹 Limpar**: Remove resultados
- **📊 Status em Tempo Real**: 
  - Indicador de microfone
  - Barra de volume
  - Confiança percentual

### 📈 **Aba Histórico & Métricas**
- **📊 Gráficos**: Acurácia e tempo de processamento
- **📋 Lista Detalhada**: Todos os reconhecimentos
- **🔍 Filtros**: Por período (hoje, semana, mês, todos)

### 📄 **Aba Integração PDF**
- **📂 Seleção**: Choose PDF com receitas
- **🔍 Análise**: Extração automática de ingredientes
- **⚖️ Comparação**: Análise de similaridade com voz

## 🛠️ Dependências

### ✅ **Principais**
- `SpeechRecognition` - Reconhecimento de voz
- `tkinter` - Interface gráfica (incluído no Python)
- `matplotlib` - Gráficos e visualizações
- `PyPDF2` - Processamento de PDF
- `numpy` - Processamento numérico

### 🔊 **Audio**
- `pyaudio` - Captura de audio do microfone
- `wave` - Processamento de ondas de audio

### 🧠 **Opcionais (para melhor performance)**
- `pocketsphinx` - Reconhecimento offline
- `nltk` - Análise avançada de texto

## 🎯 Exemplos de Uso

### 🗣️ **Frases Reconhecidas**
```
✅ "Tenho tomate, cebola e alho"
✅ "Quero fazer algo com frango e batata"  
✅ "Ingredientes: ovos, leite e farinha"
✅ "Preciso de receitas com arroz e feijão"
```

### 📊 **Métricas Típicas**
- **Acurácia**: 85-95% (ambiente silencioso)
- **Tempo de Processamento**: 1-3 segundos
- **Idiomas Suportados**: Português BR (principal)

## 🔧 Solução de Problemas

### ❌ **Microfone não funciona**
```bash
# Windows: Verificar permissões
# Linux: sudo apt install portaudio19-dev
# macOS: brew install portaudio
```

### ❌ **PyAudio não instala**
```bash
# Windows: Instalar Microsoft C++ Build Tools
# Ou usar: pip install pipwin && pipwin install pyaudio
```

### ❌ **Baixa acurácia**
- Use ambiente silencioso
- Fale claramente e devagar
- Ajuste distância do microfone
- Verifique configurações de audio

## 📈 Roadmap Futuro

### 🔮 **Próximas Funcionalidades**
- [ ] Reconhecimento de múltiplos idiomas
- [ ] Integração com IA para correção automática
- [ ] Comandos de voz para navegação
- [ ] Treinamento personalizado de vocabulário
- [ ] Integração com assistentes virtuais

### 🌟 **Melhorias Planejadas**
- [ ] Interface mais moderna (tkinter → PyQt6)
- [ ] Suporte a arquivos de audio (MP3, WAV)
- [ ] Análise de sentimento da fala
- [ ] Reconhecimento de receitas por categoria

## 📞 Suporte

### 🐛 **Reportar Bugs**
- Abra uma issue no GitHub
- Inclua logs de erro
- Especifique sistema operacional

### 💡 **Sugestões**
- Funcionalidades desejadas
- Melhorias de interface
- Novos formatos de input

---

## 🎉 Conclusão

A **Interface de Voz Avançada** do Chef RAG v2 representa um salto qualitativo no reconhecimento de ingredientes por voz, oferecendo:

✨ **Precisão Superior** com múltiplas engines
📊 **Transparência Total** com métricas em tempo real  
🔄 **Integração Completa** com PDFs e histórico
🎯 **Experiência Intuitiva** com interface moderna

**Transforme sua experiência culinária com o poder da voz!** 🍳🎤