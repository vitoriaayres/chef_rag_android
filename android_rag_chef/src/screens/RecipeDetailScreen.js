import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { apiService } from '../services/APIService';

const RecipeDetailScreen = ({ route, navigation }) => {
  const { recipe } = route.params;
  const [detailedRecipe, setDetailedRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timers, setTimers] = useState([]);

  useEffect(() => {
    loadRecipeDetails();
    extractTimers();
  }, []);

  const loadRecipeDetails = async () => {
    try {
      if (recipe.id) {
        const details = await apiService.getRecipeDetails(recipe.id);
        setDetailedRecipe(details);
      } else {
        setDetailedRecipe(recipe);
      }
    } catch (error) {
      console.log('Erro ao carregar detalhes:', error);
      setDetailedRecipe(recipe);
    } finally {
      setLoading(false);
    }
  };

  const extractTimers = async () => {
    try {
      const recipeText = recipe.instructions || recipe.description || '';
      const extractedTimers = await apiService.getTimersFromRecipe(recipeText);
      setTimers(extractedTimers.timers || []);
    } catch (error) {
      console.log('Erro ao extrair timers:', error);
    }
  };

  const addToTimers = () => {
    if (timers.length > 0) {
      Alert.alert(
        'Adicionar Timers',
        `Foram encontrados ${timers.length} timers nesta receita. Deseja adicioná-los?`,
        [
          { text: 'Cancelar' },
          {
            text: 'Adicionar',
            onPress: () => {
              navigation.navigate('Timer', { timers });
              Alert.alert('Sucesso', 'Timers adicionados com sucesso!');
            },
          },
        ]
      );
    } else {
      Alert.alert('Info', 'Nenhum timer encontrado nesta receita.');
    }
  };

  const shareRecipe = () => {
    Alert.alert('Compartilhar', 'Funcionalidade de compartilhamento em desenvolvimento');
  };

  const favoriteRecipe = () => {
    Alert.alert('Favoritos', 'Receita adicionada aos favoritos!');
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text>Carregando detalhes...</Text>
      </View>
    );
  }

  const currentRecipe = detailedRecipe || recipe;

  return (
    <ScrollView style={styles.container}>
      {/* Recipe Header */}
      <View style={styles.header}>
        <Text style={styles.title}>{currentRecipe.title || currentRecipe.name}</Text>
        
        <View style={styles.stats}>
          <View style={styles.statItem}>
            <Icon name="schedule" size={20} color="#666" />
            <Text style={styles.statText}>{currentRecipe.cookTime || '30'} min</Text>
          </View>
          
          <View style={styles.statItem}>
            <Icon name="restaurant" size={20} color="#666" />
            <Text style={styles.statText}>{currentRecipe.difficulty || 'Fácil'}</Text>
          </View>
          
          <View style={styles.statItem}>
            <Icon name="people" size={20} color="#666" />
            <Text style={styles.statText}>{currentRecipe.servings || '4'} porções</Text>
          </View>
        </View>

        {/* Action Buttons */}
        <View style={styles.actionButtons}>
          <TouchableOpacity style={styles.actionButton} onPress={favoriteRecipe}>
            <Icon name="favorite-border" size={20} color="#FF6B35" />
            <Text style={styles.actionButtonText}>Favoritar</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton} onPress={addToTimers}>
            <Icon name="timer" size={20} color="#FF6B35" />
            <Text style={styles.actionButtonText}>Timers</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionButton} onPress={shareRecipe}>
            <Icon name="share" size={20} color="#FF6B35" />
            <Text style={styles.actionButtonText}>Compartilhar</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Ingredients */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Ingredientes</Text>
        {currentRecipe.ingredients ? (
          Array.isArray(currentRecipe.ingredients) ? (
            currentRecipe.ingredients.map((ingredient, index) => (
              <View key={index} style={styles.ingredientItem}>
                <Icon name="check-circle-outline" size={16} color="#4CAF50" />
                <Text style={styles.ingredientText}>{ingredient}</Text>
              </View>
            ))
          ) : (
            <Text style={styles.description}>{currentRecipe.ingredients}</Text>
          )
        ) : (
          <Text style={styles.description}>Ingredientes não disponíveis</Text>
        )}\n      </View>\n\n      {/* Instructions */}\n      <View style={styles.section}>\n        <Text style={styles.sectionTitle}>Modo de Preparo</Text>\n        {currentRecipe.instructions ? (\n          Array.isArray(currentRecipe.instructions) ? (\n            currentRecipe.instructions.map((step, index) => (\n              <View key={index} style={styles.instructionStep}>\n                <View style={styles.stepNumber}>\n                  <Text style={styles.stepNumberText}>{index + 1}</Text>\n                </View>\n                <Text style={styles.stepText}>{step}</Text>\n              </View>\n            ))\n          ) : (\n            <Text style={styles.description}>{currentRecipe.instructions}</Text>\n          )\n        ) : currentRecipe.description ? (\n          <Text style={styles.description}>{currentRecipe.description}</Text>\n        ) : (\n          <Text style={styles.description}>Instruções não disponíveis</Text>\n        )}\n      </View>\n\n      {/* Timers Found */}\n      {timers.length > 0 && (\n        <View style={styles.section}>\n          <Text style={styles.sectionTitle}>Timers Encontrados</Text>\n          {timers.map((timer, index) => (\n            <View key={index} style={styles.timerItem}>\n              <Icon name=\"timer\" size={16} color=\"#FF6B35\" />\n              <Text style={styles.timerText}>\n                {timer.label}: {timer.duration} minutos\n              </Text>\n            </View>\n          ))}\n        </View>\n      )}\n\n      {/* Tips */}\n      <View style={styles.section}>\n        <Text style={styles.sectionTitle}>Dicas do Chef</Text>\n        <View style={styles.tipItem}>\n          <Icon name=\"lightbulb-outline\" size={16} color=\"#FF6B35\" />\n          <Text style={styles.tipText}>\n            Para melhores resultados, prepare todos os ingredientes antes de começar a cozinhar.\n          </Text>\n        </View>\n      </View>\n    </ScrollView>\n  );\n};\n\nconst styles = StyleSheet.create({\n  container: {\n    flex: 1,\n    backgroundColor: '#f5f5f5',\n  },\n  loadingContainer: {\n    flex: 1,\n    justifyContent: 'center',\n    alignItems: 'center',\n  },\n  header: {\n    backgroundColor: '#fff',\n    padding: 20,\n    marginBottom: 10,\n  },\n  title: {\n    fontSize: 24,\n    fontWeight: 'bold',\n    color: '#333',\n    marginBottom: 15,\n  },\n  stats: {\n    flexDirection: 'row',\n    justifyContent: 'space-around',\n    marginBottom: 20,\n  },\n  statItem: {\n    alignItems: 'center',\n  },\n  statText: {\n    fontSize: 12,\n    color: '#666',\n    marginTop: 4,\n  },\n  actionButtons: {\n    flexDirection: 'row',\n    justifyContent: 'space-around',\n  },\n  actionButton: {\n    alignItems: 'center',\n    padding: 10,\n  },\n  actionButtonText: {\n    fontSize: 12,\n    color: '#FF6B35',\n    marginTop: 4,\n    fontWeight: '600',\n  },\n  section: {\n    backgroundColor: '#fff',\n    marginBottom: 10,\n    padding: 20,\n  },\n  sectionTitle: {\n    fontSize: 18,\n    fontWeight: 'bold',\n    color: '#333',\n    marginBottom: 15,\n  },\n  ingredientItem: {\n    flexDirection: 'row',\n    alignItems: 'center',\n    marginBottom: 8,\n  },\n  ingredientText: {\n    fontSize: 16,\n    color: '#333',\n    marginLeft: 10,\n    flex: 1,\n  },\n  instructionStep: {\n    flexDirection: 'row',\n    marginBottom: 15,\n    alignItems: 'flex-start',\n  },\n  stepNumber: {\n    width: 24,\n    height: 24,\n    borderRadius: 12,\n    backgroundColor: '#FF6B35',\n    justifyContent: 'center',\n    alignItems: 'center',\n    marginRight: 15,\n    marginTop: 2,\n  },\n  stepNumberText: {\n    color: '#fff',\n    fontSize: 12,\n    fontWeight: 'bold',\n  },\n  stepText: {\n    fontSize: 16,\n    color: '#333',\n    lineHeight: 24,\n    flex: 1,\n  },\n  description: {\n    fontSize: 16,\n    color: '#333',\n    lineHeight: 24,\n  },\n  timerItem: {\n    flexDirection: 'row',\n    alignItems: 'center',\n    marginBottom: 8,\n  },\n  timerText: {\n    fontSize: 14,\n    color: '#666',\n    marginLeft: 10,\n  },\n  tipItem: {\n    flexDirection: 'row',\n    alignItems: 'flex-start',\n  },\n  tipText: {\n    fontSize: 14,\n    color: '#666',\n    marginLeft: 10,\n    lineHeight: 20,\n    flex: 1,\n  },\n});\n\nexport default RecipeDetailScreen;