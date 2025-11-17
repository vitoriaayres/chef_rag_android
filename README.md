# 🧑‍🍳 Chef RAG - Assistente Culinário Inteligente

Sistema de recomendação de receitas baseado em IA que utiliza RAG (Retrieval-Augmented Generation) para sugerir receitas com base nos ingredientes disponíveis.

## ✨ Funcionalidades Principais

- 📷 **Análise por Câmera**: Detecta ingredientes via webcam usando YOLO
- 📱 **Versão Mobile**: Interface mobile com QR Code
- 🖼️ **Upload de Fotos**: Analisa ingredientes em fotos enviadas
- ✍️ **Entrada Manual**: Digite os ingredientes disponíveis
- 🎤 **Reconhecimento de Voz**: Fale os ingredientes
- 🥗 **Filtros Dietéticos**: Filtra por restrições alimentares
- ⚖️ **Calculadora de Calorias**: Calcula valor nutricional
- 🚫 **Verificador de Alergias**: Identifica possíveis alérgenos
- ⏰ **Cronômetros**: Gerencia tempos de preparo

## 🎯 Diferenciais

- **Foco 100% no Passo a Passo**: Prioriza instruções detalhadas de preparo
- **Sistema CSV de Alta Precisão**: Base de dados estruturada com receitas brasileiras
- **Interface Gráfica Interativa**: Modo passo a passo visual
- **Busca Inteligente**: Compatibilidade por percentual de ingredientes
- **Múltiplas Formas de Entrada**: Câmera, voz, texto, foto

## 🚀 Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/vitoriaayres/chef_rag_android.git
cd chef_rag_android
```

2. **Crie um ambiente virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**:
Crie um arquivo `.env` com sua chave da OpenAI:
```
OPENAI_API_KEY=sua_chave_aqui
```

## 🎮 Como Usar

### Executar o Sistema Principal
```bash
python main.py
```

### Testar Funcionalidades Específicas
```bash
# Testar sistema de busca
python sistema_busca_csv.py

# Testar webcam com YOLO
python webcam.py

# Análise de fotos
python interface_upload_foto.py
```

## 📁 Estrutura do Projeto

```
chef_rag_v2/
├── main.py                        # Interface principal
├── sistema_busca_csv.py           # Sistema de busca por CSV
├── receitas_estruturadas.csv      # Base de dados de receitas
├── webcam.py                      # Análise por câmera
├── webcam_yolo.py                # YOLO para detecção de ingredientes
├── core_logic/                    # Lógica principal do RAG
│   ├── sistema_rag.py            # Engine principal
│   ├── processamento_imagem.py   # Análise de imagens
│   └── gerenciamento_dados.py    # Gestão de dados
├── interface_*.py                 # Interfaces específicas
├── reconhecimento_voz_*.py       # Sistema de voz
├── camera_mobile.py              # Servidor mobile
├── requirements.txt              # Dependências
└── README.md                     # Este arquivo
```

## 🧠 Como Funciona

1. **Entrada de Dados**: O usuário fornece ingredientes via câmera, voz, texto ou foto
2. **Processamento IA**: O sistema analisa e identifica ingredientes usando modelos de IA
3. **Busca Inteligente**: Algoritmo busca receitas compatíveis no banco de dados CSV
4. **Ranqueamento**: Receitas são ordenadas por compatibilidade percentual
5. **Apresentação**: Foco principal no passo a passo detalhado de preparo
6. **Interface Interativa**: Opção de interface gráfica para acompanhar o preparo

## 📊 Base de Dados

- **12+ receitas estruturadas** com ingredientes, modo de preparo, tempo e dificuldade
- **Sistema de compatibilidade** que calcula percentual de match
- **Receitas brasileiras** com ingredientes locais
- **Categorias diversas**: doces, salgados, bebidas, pratos principais

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **OpenAI GPT** para análise de ingredientes
- **LangChain** para RAG
- **YOLO v8** para detecção de objetos
- **OpenCV** para processamento de imagem
- **Tkinter** para interface gráfica
- **Flask** para servidor mobile
- **SpeechRecognition** para entrada por voz

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autores

- **Chef RAG Team** - Desenvolvimento inicial
- **Vitória Ayres** - Repositório GitHub

---

💡 **Dica**: Para melhor experiência, use em ambiente com boa iluminação para análise por câmera!