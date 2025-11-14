import React, { useState, useEffect } from 'react';

const UserProfile = ({ onClose }) => {
  const [profile, setProfile] = useState({
    name: '',
    skill_level: 'iniciante',
    dietary_restrictions: [],
    favorite_cuisines: [],
    allergies: [],
    cooking_equipment: [],
    preferred_cooking_time: 60,
    budget_preference: 'medio',
    health_goals: []
  });
  
  const [ratings, setRatings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    loadUserProfile();
    loadUserRatings();
  }, []);

  const loadUserProfile = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/user/profile');
      const data = await response.json();
      
      if (data.success && data.profile) {
        setProfile(data.profile);
      }
    } catch (error) {
      console.error('Erro ao carregar perfil:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadUserRatings = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/user/recipe-ratings?limit=5');
      const data = await response.json();
      
      if (data.success) {
        setRatings(data.ratings);
      }
    } catch (error) {
      console.error('Erro ao carregar avaliações:', error);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const response = await fetch('http://localhost:5000/api/user/profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profile)
      });

      const data = await response.json();
      
      if (data.success) {
        alert('Perfil salvo com sucesso!');
      } else {
        alert('Erro ao salvar perfil: ' + data.error);
      }
    } catch (error) {
      alert('Erro ao salvar perfil: ' + error.message);
    } finally {
      setIsSaving(false);
    }
  };

  const handleArrayFieldChange = (field, value) => {
    setProfile(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  const skillLevels = [
    { value: 'iniciante', label: '👶 Iniciante' },
    { value: 'intermediario', label: '👨‍🍳 Intermediário' },
    { value: 'avancado', label: '🧑‍🍳 Avançado' },
    { value: 'profissional', label: '👨‍🚀 Profissional' }
  ];

  const dietaryOptions = [
    'Vegetariano', 'Vegano', 'Sem Glúten', 'Sem Lactose', 
    'Low Carb', 'Keto', 'Diabético', 'Hipertensão'
  ];

  const cuisineOptions = [
    'Brasileira', 'Italiana', 'Japonesa', 'Chinesa', 
    'Mexicana', 'Indiana', 'Francesa', 'Mediterrânea'
  ];

  const equipmentOptions = [
    'Forno', 'Microondas', 'Fogão', 'Air Fryer', 
    'Panela de Pressão', 'Liquidificador', 'Batedeira', 'Grill'
  ];

  const budgetOptions = [
    { value: 'baixo', label: '💰 Econômico' },
    { value: 'medio', label: '💰💰 Moderado' },
    { value: 'alto', label: '💰💰💰 Premium' }
  ];

  if (isLoading) {
    return (
      <div className="profile-overlay">
        <div className="profile-modal">
          <div className="loading">Carregando perfil...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-overlay">
      <div className="profile-modal">
        <div className="profile-header">
          <h2>👤 Meu Perfil Culinário</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="profile-tabs">
          <button 
            className={activeTab === 'profile' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('profile')}
          >
            📝 Perfil
          </button>
          <button 
            className={activeTab === 'ratings' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('ratings')}
          >
            ⭐ Minhas Avaliações
          </button>
        </div>

        {activeTab === 'profile' && (
          <div className="profile-content">
            <div className="form-group">
              <label>Nome:</label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({...profile, name: e.target.value})}
                placeholder="Seu nome"
              />
            </div>

            <div className="form-group">
              <label>Nível Culinário:</label>
              <select
                value={profile.skill_level}
                onChange={(e) => setProfile({...profile, skill_level: e.target.value})}
              >
                {skillLevels.map(level => (
                  <option key={level.value} value={level.value}>
                    {level.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Tempo de Cozinha (minutos):</label>
              <input
                type="range"
                min="15"
                max="180"
                value={profile.preferred_cooking_time}
                onChange={(e) => setProfile({...profile, preferred_cooking_time: parseInt(e.target.value)})}
              />
              <span>{profile.preferred_cooking_time} min</span>
            </div>

            <div className="form-group">
              <label>Orçamento:</label>
              <select
                value={profile.budget_preference}
                onChange={(e) => setProfile({...profile, budget_preference: e.target.value})}
              >
                {budgetOptions.map(budget => (
                  <option key={budget.value} value={budget.value}>
                    {budget.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Restrições Alimentares:</label>
              <div className="checkbox-grid">
                {dietaryOptions.map(option => (
                  <label key={option} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={profile.dietary_restrictions.includes(option)}
                      onChange={() => handleArrayFieldChange('dietary_restrictions', option)}
                    />
                    {option}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Cozinhas Favoritas:</label>
              <div className="checkbox-grid">
                {cuisineOptions.map(option => (
                  <label key={option} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={profile.favorite_cuisines.includes(option)}
                      onChange={() => handleArrayFieldChange('favorite_cuisines', option)}
                    />
                    {option}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Equipamentos Disponíveis:</label>
              <div className="checkbox-grid">
                {equipmentOptions.map(option => (
                  <label key={option} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={profile.cooking_equipment.includes(option)}
                      onChange={() => handleArrayFieldChange('cooking_equipment', option)}
                    />
                    {option}
                  </label>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ratings' && (
          <div className="ratings-content">
            <h3>🌟 Últimas Avaliações</h3>
            {ratings.length === 0 ? (
              <p>Você ainda não avaliou nenhuma receita.</p>
            ) : (
              <div className="ratings-list">
                {ratings.map((rating, index) => (
                  <div key={index} className="rating-item">
                    <div className="rating-header">
                      <strong>{rating.recipe_name}</strong>
                      <div className="stars">
                        {'⭐'.repeat(rating.rating)}
                      </div>
                    </div>
                    {rating.comment && (
                      <p className="rating-comment">"{rating.comment}"</p>
                    )}
                    <small>{new Date(rating.created_at).toLocaleDateString()}</small>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="profile-actions">
          <button 
            className="save-btn" 
            onClick={handleSave}
            disabled={isSaving}
          >
            {isSaving ? 'Salvando...' : '💾 Salvar Perfil'}
          </button>
          <button className="cancel-btn" onClick={onClose}>
            ❌ Cancelar
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;