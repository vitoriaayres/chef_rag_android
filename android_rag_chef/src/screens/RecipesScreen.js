import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { apiService } from '../services/APIService';

const RecipesScreen = ({ navigation, route }) => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    vegetarian: false,
    vegan: false,
    glutenFree: false,
    lowCarb: false,
  });

  useEffect(() => {
    // Se vieram ingredientes da análise da câmera
    if (route.params?.ingredients) {
      searchRecipesByIngredients(route.params.ingredients);
    }
  }, [route.params]);

  const searchRecipesByIngredients = async (ingredients) => {
    setLoading(true);
    try {
      const ingredientString = Array.isArray(ingredients) 
        ? ingredients.join(', ') 
        : ingredients;
      
      const result = await apiService.getRecipesByIngredient(ingredientString, filters);
      setRecipes(result.recipes || []);
    } catch (error) {
      Alert.alert('Erro', error.message || 'Não foi possível carregar as receitas');
    } finally {
      setLoading(false);
    }
  };

  const searchRecipes = async () => {
    if (!searchTerm.trim()) {
      Alert.alert('Aviso', 'Digite um ingrediente para buscar receitas');
      return;
    }
    
    await searchRecipesByIngredients(searchTerm);
  };

  const toggleFilter = (filterName) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: !prev[filterName]
    }));
  };

  const applyFilters = async () => {
    if (recipes.length > 0) {
      setLoading(true);
      try {
        const result = await apiService.getRecipesWithFilters(filters);
        setRecipes(result.recipes || []);
      } catch (error) {
        Alert.alert('Erro', error.message || 'Não foi possível aplicar filtros');
      } finally {
        setLoading(false);
      }
    }
  };

  const FilterButton = ({ label, filterKey, icon }) => (
    <TouchableOpacity
      style={[
        styles.filterButton,
        filters[filterKey] && styles.filterButtonActive
      ]}
      onPress={() => toggleFilter(filterKey)}
    >
      <Icon 
        name={icon} 
        size={16} 
        color={filters[filterKey] ? '#fff' : '#666'} 
      />
      <Text style={[
        styles.filterButtonText,
        filters[filterKey] && styles.filterButtonTextActive
      ]}>
        {label}
      </Text>
    </TouchableOpacity>
  );

  const RecipeCard = ({ recipe }) => (
    <TouchableOpacity
      style={styles.recipeCard}
      onPress={() => navigation.navigate('RecipeDetail', { recipe })}
    >
      <View style={styles.recipeContent}>
        <Text style={styles.recipeTitle}>{recipe.title || recipe.name}</Text>
        <Text style={styles.recipeDescription} numberOfLines={2}>
          {recipe.description || recipe.ingredients}
        </Text>
        
        <View style={styles.recipeFooter}>
          <View style={styles.recipeStats}>
            <Icon name="schedule" size={16} color="#666" />
            <Text style={styles.recipeStatText}>
              {recipe.cookTime || '30'} min
            </Text>
          </View>
          
          <View style={styles.recipeStats}>
            <Icon name="restaurant" size={16} color="#666" />
            <Text style={styles.recipeStatText}>
              {recipe.difficulty || 'Fácil'}
            </Text>
          </View>
        </View>
      </View>
      
      <Icon name="chevron-right" size={24} color="#ccc" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <View style={styles.searchBar}>
          <Icon name="search" size={24} color="#666" />
          <TextInput
            style={styles.searchInput}
            placeholder="Buscar receitas por ingrediente..."
            value={searchTerm}
            onChangeText={setSearchTerm}
            onSubmitEditing={searchRecipes}
          />
          {searchTerm.length > 0 && (
            <TouchableOpacity onPress={() => setSearchTerm('')}>
              <Icon name="clear" size={20} color="#666" />
            </TouchableOpacity>
          )}
        </View>
        
        <TouchableOpacity style={styles.searchButton} onPress={searchRecipes}>
          <Icon name="search" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Filters */}
      <ScrollView horizontal style={styles.filtersContainer} showsHorizontalScrollIndicator={false}>
        <FilterButton label="Vegetariano" filterKey="vegetarian" icon="eco" />
        <FilterButton label="Vegano" filterKey="vegan" icon="nature" />
        <FilterButton label="Sem Glúten" filterKey="glutenFree" icon="no-food" />
        <FilterButton label="Low Carb" filterKey="lowCarb" icon="trending-down" />
        
        <TouchableOpacity style={styles.applyFiltersButton} onPress={applyFilters}>
          <Icon name="tune" size={16} color="#FF6B35" />
          <Text style={styles.applyFiltersText}>Aplicar</Text>
        </TouchableOpacity>
      </ScrollView>

      {/* Recipes List */}
      <ScrollView style={styles.recipesContainer}>
        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#FF6B35" />
            <Text style={styles.loadingText}>Buscando receitas...</Text>
          </View>
        ) : recipes.length > 0 ? (
          recipes.map((recipe, index) => (
            <RecipeCard key={index} recipe={recipe} />
          ))
        ) : (
          <View style={styles.emptyState}>
            <Icon name="restaurant" size={60} color="#ccc" />
            <Text style={styles.emptyStateTitle}>Nenhuma receita encontrada</Text>
            <Text style={styles.emptyStateText}>
              Tente buscar por um ingrediente ou use a câmera para analisar seus ingredientes
            </Text>
            
            <TouchableOpacity
              style={styles.cameraButton}
              onPress={() => navigation.navigate('Camera')}
            >
              <Icon name="camera-alt" size={20} color="#fff" />
              <Text style={styles.cameraButtonText}>Usar Câmera</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  searchContainer: {
    flexDirection: 'row',
    padding: 15,
    backgroundColor: '#fff',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  searchBar: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8f8f8',
    borderRadius: 25,
    paddingHorizontal: 15,
    marginRight: 10,
  },
  searchInput: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 10,
    fontSize: 16,
    color: '#333',
  },
  searchButton: {
    backgroundColor: '#FF6B35',
    borderRadius: 25,
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  filtersContainer: {
    backgroundColor: '#fff',
    paddingVertical: 10,
    paddingHorizontal: 15,
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    marginRight: 10,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  filterButtonActive: {
    backgroundColor: '#FF6B35',
    borderColor: '#FF6B35',
  },
  filterButtonText: {
    marginLeft: 6,
    fontSize: 14,
    color: '#666',
  },
  filterButtonTextActive: {
    color: '#fff',
  },
  applyFiltersButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#FF6B35',
  },
  applyFiltersText: {
    marginLeft: 6,
    fontSize: 14,
    color: '#FF6B35',
    fontWeight: '600',
  },
  recipesContainer: {
    flex: 1,
    padding: 15,
  },
  recipeCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 12,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  recipeContent: {
    flex: 1,
  },
  recipeTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 6,
  },
  recipeDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 10,
  },
  recipeFooter: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  recipeStats: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 20,
  },
  recipeStatText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 40,
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  emptyState: {
    alignItems: 'center',
    padding: 40,
  },
  emptyStateTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 15,
    marginBottom: 10,
  },
  emptyStateText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 25,
  },
  cameraButton: {
    backgroundColor: '#FF6B35',
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 25,
  },
  cameraButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
});

export default RecipesScreen;