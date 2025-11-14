import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Image,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { apiService } from '../services/APIService';

const HomeScreen = ({ navigation }) => {
  const [recentRecipes, setRecentRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRecentData();
  }, []);

  const loadRecentData = async () => {
    try {
      const history = await apiService.getAnalysisHistory();
      setRecentRecipes(history.slice(0, 3)); // Últimas 3 análises
    } catch (error) {
      console.log('Erro ao carregar dados recentes:', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAction = (action) => {
    switch (action) {
      case 'camera':
        navigation.navigate('Camera');
        break;
      case 'voice':
        // Implementar reconhecimento de voz
        Alert.alert('Reconhecimento de Voz', 'Funcionalidade em desenvolvimento');
        break;
      case 'recipes':
        navigation.navigate('Recipes');
        break;
      case 'timer':
        navigation.navigate('Timer');
        break;
      default:
        break;
    }
  };

  const QuickActionButton = ({ icon, title, action, color = '#FF6B35' }) => (
    <TouchableOpacity
      style={[styles.quickActionButton, { backgroundColor: color }]}
      onPress={() => handleQuickAction(action)}>
      <Icon name={icon} size={30} color="#fff" />
      <Text style={styles.quickActionText}>{title}</Text>
    </TouchableOpacity>
  );

  const RecentRecipeCard = ({ recipe }) => (
    <TouchableOpacity style={styles.recipeCard}>
      <View style={styles.recipeInfo}>
        <Text style={styles.recipeTitle}>{recipe.ingredient}</Text>
        <Text style={styles.recipeSubtitle}>
          Analisado em {new Date(recipe.timestamp).toLocaleDateString()}
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <ScrollView style={styles.container}>
      {/* Header Welcome */}
      <View style={styles.welcomeSection}>
        <Text style={styles.welcomeTitle}>Olá! 👋</Text>
        <Text style={styles.welcomeSubtitle}>
          Que tal descobrir uma receita incrível hoje?
        </Text>
      </View>

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Ações Rápidas</Text>
        <View style={styles.quickActionsGrid}>
          <QuickActionButton
            icon="camera-alt"
            title="Capturar"
            action="camera"
            color="#FF6B35"
          />
          <QuickActionButton
            icon="mic"
            title="Voz"
            action="voice"
            color="#4CAF50"
          />
          <QuickActionButton
            icon="restaurant"
            title="Receitas"
            action="recipes"
            color="#2196F3"
          />
          <QuickActionButton
            icon="timer"
            title="Timer"
            action="timer"
            color="#9C27B0"
          />
        </View>
      </View>

      {/* Recent Analysis */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Análises Recentes</Text>
        {loading ? (
          <View style={styles.loadingContainer}>
            <Text style={styles.loadingText}>Carregando...</Text>
          </View>
        ) : recentRecipes.length > 0 ? (
          recentRecipes.map((recipe, index) => (
            <RecentRecipeCard key={index} recipe={recipe} />
          ))
        ) : (
          <View style={styles.emptyState}>
            <Icon name="restaurant" size={50} color="#ccc" />
            <Text style={styles.emptyStateText}>
              Nenhuma análise recente
            </Text>
            <Text style={styles.emptyStateSubtext}>
              Comece capturando uma imagem dos seus ingredientes!
            </Text>
          </View>
        )}
      </View>

      {/* Tips Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Dicas do Chef</Text>
        <View style={styles.tipCard}>
          <Icon name="lightbulb-outline" size={24} color="#FF6B35" />
          <Text style={styles.tipText}>
            Para melhores resultados, fotografe os ingredientes com boa iluminação
            e fundo claro.
          </Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  welcomeSection: {
    backgroundColor: '#FF6B35',
    padding: 20,
    paddingTop: 40,
  },
  welcomeTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  welcomeSubtitle: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  quickActionButton: {
    width: '48%',
    aspectRatio: 1,
    borderRadius: 15,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  quickActionText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    marginTop: 8,
  },
  recipeCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  recipeInfo: {
    flex: 1,
  },
  recipeTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  recipeSubtitle: {
    fontSize: 14,
    color: '#666',
  },
  loadingContainer: {
    padding: 20,
    alignItems: 'center',
  },
  loadingText: {
    color: '#666',
    fontSize: 16,
  },
  emptyState: {
    alignItems: 'center',
    padding: 30,
  },
  emptyStateText: {
    fontSize: 18,
    color: '#666',
    marginTop: 10,
    fontWeight: '600',
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    marginTop: 5,
  },
  tipCard: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    flexDirection: 'row',
    alignItems: 'flex-start',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  tipText: {
    flex: 1,
    fontSize: 14,
    color: '#666',
    marginLeft: 10,
    lineHeight: 20,
  },
});

export default HomeScreen;