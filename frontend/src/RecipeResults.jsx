import React, { useState, useEffect } from 'react';
import RecipeRating from './RecipeRating';

const RecipeResults = ({ result, onBack }) => {
  const [extractedRecipes, setExtractedRecipes] = useState([]);
  const [showRating, setShowRating] = useState(false);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (result?.recipes) {
      extractRecipesFromResponse();
    }
  }, [result]);

  const extractRecipesFromResponse = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/recipes/extract-for-rating', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          recipes_response: result.recipes
        })
      });

      const data = await response.json();

      if (data.success) {
        setExtractedRecipes(data.recipes);
      }
    } catch (error) {
      console.error('Erro ao extrair receitas:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRate = (recipe) => {
    setSelectedRecipe(recipe);
    setShowRating(true);
  };

  const handleRatingSubmitted = (recipe, newSummary) => {
    // Atualiza o resumo de avaliações da receita
    setExtractedRecipes(prev => 
      prev.map(r => 
        r.id === recipe.id 
          ? { ...r, rating_summary: newSummary }
          : r
      )
    );
  };

  const formatIngredient = (ingredient) => {
    if (typeof ingredient === 'string' && ingredient.includes(',')) {
      return ingredient.split(',').map(ing => ing.trim()).join(', ');
    }
    return ingredient;
  };

  return (
    <div className="recipe-results-container">
      <div className="results-header">
        <h3>🍽️ Resultados da Análise</h3>
        <div className="result-info">
          <span className="ingredient-tag">
            📍 {formatIngredient(result.ingredient)}
          </span>
          {result.processing_time && (
            <span className="time-tag">
              ⏱️ {result.processing_time}s
            </span>
          )}
          {result.source && (
            <span className="source-tag">
              📡 {result.source === 'voice_recognition' ? 'Voz' : result.source}
            </span>
          )}
        </div>
      </div>

      {isLoading ? (
        <div className="loading-recipes">
          <div className="loading-spinner"></div>
          <p>Processando receitas...</p>
        </div>
      ) : (
        <>
          <div className="recipes-content">
            <div className="raw-response">
              <div dangerouslySetInnerHTML={{ 
                __html: result.recipes.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
              }} />
            </div>

            {extractedRecipes.length > 0 && (
              <div className="extracted-recipes">
                <h4>📋 Receitas Encontradas</h4>
                <div className="recipes-grid">
                  {extractedRecipes.map((recipe) => (
                    <div key={recipe.id} className="recipe-card">
                      <div className="recipe-header">
                        <h5>{recipe.name}</h5>
                        <span className="page-badge">Pág. {recipe.page}</span>
                      </div>
                      
                      {recipe.description && (
                        <p className="recipe-description">{recipe.description}</p>
                      )}
                      
                      <div className="recipe-rating-info">
                        {recipe.rating_summary.total_ratings > 0 ? (
                          <div className="rating-display">
                            <span className="stars">{recipe.rating_summary.stars_display}</span>
                            <span className="rating-text">
                              {recipe.rating_summary.average_rating}/5 
                              ({recipe.rating_summary.total_ratings} avaliações)
                            </span>
                            <span className="positive-rate">
                              👍 {recipe.rating_summary.positive_percentage}%
                            </span>
                          </div>
                        ) : (
                          <div className="no-ratings">
                            <span>⭐ Sem avaliações ainda</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="recipe-actions">
                        <button 
                          className="rate-btn"
                          onClick={() => handleRate(recipe)}
                        >
                          ⭐ Avaliar Receita
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </>
      )}

      <div className="results-actions">
        <button className="back-btn" onClick={onBack}>
          ⬅️ Nova Análise
        </button>
      </div>

      {/* Modal de Avaliação */}
      {showRating && selectedRecipe && (
        <RecipeRating
          recipe={selectedRecipe}
          onRate={handleRatingSubmitted}
          onClose={() => setShowRating(false)}
        />
      )}
    </div>
  );
};

export default RecipeResults;