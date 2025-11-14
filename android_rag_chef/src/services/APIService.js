import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Configure base URL - ajuste conforme seu backend
const BASE_URL = 'http://localhost:5000'; // Para desenvolvimento local
// const BASE_URL = 'http://10.0.2.2:5000'; // Para emulador Android
// const BASE_URL = 'https://sua-api.herokuapp.com'; // Para produção

class APIService {
  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para adicionar token de autenticação
    this.client.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('userToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }

  // Análise de imagem
  async analyzeImage(imageUri, options = {}) {
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: imageUri,
        type: 'image/jpeg',
        name: 'ingredient.jpg',
      });

      if (options.multipleIngredients) {
        formData.append('multiple_ingredients', 'true');
      }

      const response = await this.client.post('/api/analyze-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      console.error('Erro na análise de imagem:', error);
      throw this.handleError(error);
    }
  }

  // Buscar receitas por ingrediente
  async getRecipesByIngredient(ingredient, filters = {}) {
    try {
      const params = {
        ingredient,
        ...filters,
      };

      const response = await this.client.get('/api/recipes/search', { params });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar receitas:', error);
      throw this.handleError(error);
    }
  }

  // Obter detalhes de uma receita
  async getRecipeDetails(recipeId) {
    try {
      const response = await this.client.get(`/api/recipes/${recipeId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao obter detalhes da receita:', error);
      throw this.handleError(error);
    }
  }

  // Reconhecimento de voz
  async processVoiceInput(audioData) {
    try {
      const formData = new FormData();
      formData.append('audio', {
        uri: audioData.uri,
        type: 'audio/mp4',
        name: 'voice.mp4',
      });

      const response = await this.client.post('/api/voice/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      console.error('Erro no processamento de voz:', error);
      throw this.handleError(error);
    }
  }

  // Gerenciamento de perfil
  async getUserProfile() {
    try {
      const response = await this.client.get('/api/profile');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter perfil:', error);
      throw this.handleError(error);
    }
  }

  async updateUserProfile(profileData) {
    try {
      const response = await this.client.put('/api/profile', profileData);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      throw this.handleError(error);
    }
  }

  // Histórico
  async getAnalysisHistory() {
    try {
      const response = await this.client.get('/api/history');
      return response.data;
    } catch (error) {
      console.error('Erro ao obter histórico:', error);
      throw this.handleError(error);
    }
  }

  // Filtros alimentares
  async getRecipesWithFilters(filters) {
    try {
      const response = await this.client.post('/api/recipes/filters', filters);
      return response.data;
    } catch (error) {
      console.error('Erro ao aplicar filtros:', error);
      throw this.handleError(error);
    }
  }

  // Timers
  async getTimersFromRecipe(recipeText) {
    try {
      const response = await this.client.post('/api/timers/extract', {
        recipe_text: recipeText,
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao extrair timers:', error);
      throw this.handleError(error);
    }
  }

  // Tratamento de erros
  handleError(error) {
    if (error.response) {
      // Erro HTTP
      return {
        message: error.response.data.message || 'Erro no servidor',
        status: error.response.status,
        data: error.response.data,
      };
    } else if (error.request) {
      // Erro de rede
      return {
        message: 'Erro de conexão. Verifique sua internet.',
        status: 0,
        data: null,
      };
    } else {
      // Outro erro
      return {
        message: error.message || 'Erro desconhecido',
        status: -1,
        data: null,
      };
    }
  }

  // Utilitário para verificar conectividade
  async checkConnection() {
    try {
      const response = await this.client.get('/api/health');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
}

// Exportar instância singleton
export const apiService = new APIService();
export { APIService };