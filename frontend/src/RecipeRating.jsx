import React, { useState } from 'react';

const RecipeRating = ({ recipe, onRate, onClose }) => {
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [cookingTime, setCookingTime] = useState('');
  const [difficulty, setDifficulty] = useState('medio');
  const [wouldCookAgain, setWouldCookAgain] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (rating === 0) {
      alert('Por favor, selecione uma avaliação de 1 a 5 estrelas');
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:5000/api/recipes/quick-rate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          recipe_name: recipe.name,
          recipe_page: recipe.page,
          rating: rating,
          comment: comment,
          cooking_time_actual: cookingTime ? parseInt(cookingTime) : null,
          difficulty_perceived: difficulty,
          would_cook_again: wouldCookAgain
        })
      });

      const data = await response.json();

      if (data.success) {
        onRate(recipe, data.new_rating_summary);
        alert('✅ Avaliação enviada com sucesso!');
        onClose();
      } else {
        alert('Erro: ' + data.error);
      }
    } catch (error) {
      alert('Erro ao enviar avaliação: ' + error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStars = () => {
    return (
      <div className="stars-input">
        {[1, 2, 3, 4, 5].map(star => (
          <button
            key={star}
            className={`star-button ${rating >= star ? 'filled' : ''}`}
            onClick={() => setRating(star)}
            type="button"
          >
            {rating >= star ? '⭐' : '☆'}
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="rating-overlay">
      <div className="rating-modal">
        <div className="rating-header">
          <h3>⭐ Avaliar Receita</h3>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="rating-content">
          <div className="recipe-info">
            <h4>📋 {recipe.name}</h4>
            <p>📖 Página {recipe.page}</p>
            {recipe.description && (
              <p className="recipe-description">{recipe.description}</p>
            )}
          </div>

          <div className="rating-form">
            <div className="form-group">
              <label><strong>Sua avaliação:</strong></label>
              {renderStars()}
              <div className="rating-labels">
                <span>Ruim</span>
                <span>Excelente</span>
              </div>
            </div>

            <div className="form-group">
              <label>Comentário (opcional):</label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Como foi a experiência? A receita ficou boa? Alguma dica?"
                rows="3"
              />
            </div>

            <div className="form-row">
              <div className="form-group half">
                <label>Tempo de preparo real (min):</label>
                <input
                  type="number"
                  value={cookingTime}
                  onChange={(e) => setCookingTime(e.target.value)}
                  placeholder="Ex: 45"
                  min="1"
                  max="300"
                />
              </div>

              <div className="form-group half">
                <label>Dificuldade percebida:</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                >
                  <option value="facil">😊 Fácil</option>
                  <option value="medio">🤔 Médio</option>
                  <option value="dificil">😅 Difícil</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={wouldCookAgain}
                  onChange={(e) => setWouldCookAgain(e.target.checked)}
                />
                <span>👨‍🍳 Faria esta receita novamente</span>
              </label>
            </div>
          </div>
        </div>

        <div className="rating-actions">
          <button 
            className="submit-btn" 
            onClick={handleSubmit}
            disabled={isSubmitting || rating === 0}
          >
            {isSubmitting ? '⏳ Enviando...' : '⭐ Enviar Avaliação'}
          </button>
          <button className="cancel-btn" onClick={onClose}>
            ❌ Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecipeRating;