# Chef RAG Mobile

Um aplicativo móvel React Native para o sistema Chef RAG - sugestões inteligentes de receitas baseadas em análise de ingredientes.

## 📱 Funcionalidades

- **Captura de Ingredientes**: Use a câmera para fotografar ingredientes e obter análises automáticas
- **Sugestões de Receitas**: Receba receitas personalizadas baseadas nos ingredientes detectados
- **Timers Integrados**: Cronômetros automáticos extraídos das receitas
- **Perfil Personalizado**: Configure restrições alimentares e preferências culinárias
- **Reconhecimento de Voz**: Entrada de ingredientes por comando de voz (em desenvolvimento)

## 🛠️ Tecnologias

- **React Native** - Framework principal para desenvolvimento cross-platform
- **React Navigation** - Navegação entre telas
- **React Native Camera/Image Picker** - Captura e seleção de imagens
- **React Native Voice** - Reconhecimento de voz
- **AsyncStorage** - Armazenamento local de dados
- **Axios** - Cliente HTTP para comunicação com API
- **React Native Vector Icons** - Ícones customizáveis

## 🚀 Configuração do Ambiente

### Pré-requisitos

1. **Node.js** (v16 ou superior)
2. **React Native CLI**
3. **Android Studio** (para desenvolvimento Android)
4. **Xcode** (para desenvolvimento iOS - apenas macOS)

### Instalação

```bash
# Instalar dependências
npm install

# Para iOS (apenas macOS)
cd ios && pod install && cd ..

# Executar no Android
npm run android

# Executar no iOS
npm run ios

# Iniciar o Metro Bundler
npm start
```

## 📂 Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
├── screens/            # Telas do aplicativo
│   ├── HomeScreen.js   # Tela inicial
│   ├── CameraScreen.js # Captura de imagens
│   ├── RecipesScreen.js # Lista de receitas
│   ├── TimerScreen.js  # Gerenciador de timers
│   ├── ProfileScreen.js # Configurações do usuário
│   └── RecipeDetailScreen.js # Detalhes da receita
├── services/           # Serviços de API
│   └── APIService.js   # Cliente para comunicação com backend
├── utils/              # Funções utilitárias
└── App.js             # Componente principal
```

## 🔧 Configuração da API

Edite o arquivo `src/services/APIService.js` para configurar a URL do seu backend:

```javascript
const BASE_URL = 'http://localhost:5000'; // Para desenvolvimento local
// const BASE_URL = 'http://10.0.2.2:5000'; // Para emulador Android
// const BASE_URL = 'https://sua-api.herokuapp.com'; // Para produção
```

## 📱 Recursos por Tela

### Home Screen
- Ações rápidas (câmera, voz, receitas, timer)
- Histórico de análises recentes
- Dicas do chef

### Camera Screen
- Captura via câmera ou galeria
- Preview da imagem selecionada
- Análise automática de ingredientes

### Recipes Screen
- Lista de receitas filtráveis
- Busca por ingredientes
- Filtros dietéticos (vegetariano, vegano, sem glúten, etc.)

### Timer Screen
- Múltiplos timers simultâneos
- Timers pré-definidos (5, 15, 30 min)
- Timers customizáveis
- Notificações sonoras

### Profile Screen
- Configuração de restrições alimentares
- Nível culinário (iniciante, intermediário, avançado)
- Preferências pessoais
- Sincronização com servidor

## 🔒 Permissões

O app requer as seguintes permissões:

- **Câmera**: Para captura de fotos dos ingredientes
- **Galeria**: Para seleção de imagens existentes
- **Microfone**: Para reconhecimento de voz (futuro)
- **Internet**: Para comunicação com a API

## 🤝 Backend Integration

Este app se conecta com a API Flask do Chef RAG. Certifique-se de que o backend esteja rodando antes de usar o aplicativo.

Endpoints utilizados:
- `POST /api/analyze-image` - Análise de ingredientes
- `GET /api/recipes/search` - Busca de receitas
- `GET /api/recipes/{id}` - Detalhes da receita
- `POST /api/timers/extract` - Extração de timers
- `GET/PUT /api/profile` - Gerenciamento de perfil

## 📄 Licença

Este projeto é parte do sistema Chef RAG e está em desenvolvimento.

## 🐛 Problemas Conhecidos

- Reconhecimento de voz ainda em desenvolvimento
- Temas escuros não implementados
- Push notifications não configuradas

## 🔮 Próximas Funcionalidades

- [ ] Reconhecimento de voz completo
- [ ] Modo offline para receitas favoritas
- [ ] Compartilhamento social de receitas
- [ ] Modo escuro
- [ ] Notificações push para timers
- [ ] Sincronização entre dispositivos