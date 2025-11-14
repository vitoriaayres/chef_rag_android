import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Switch,
  Alert,
  Modal,
  TextInput,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiService } from '../services/APIService';

const ProfileScreen = () => {
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    dietaryRestrictions: {
      vegetarian: false,
      vegan: false,
      glutenFree: false,
      lowCarb: false,
      diabetic: false,
    },
    culinaryLevel: 'beginner', // beginner, intermediate, advanced
    preferences: {
      spicyFood: false,
      seafood: true,
      dairy: true,
    },
  });
  const [showEditModal, setShowEditModal] = useState(false);
  const [tempProfile, setTempProfile] = useState({});

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const savedProfile = await AsyncStorage.getItem('userProfile');
      if (savedProfile) {
        setProfile(JSON.parse(savedProfile));
      }
    } catch (error) {
      console.log('Erro ao carregar perfil:', error);
    }
  };

  const saveProfile = async (newProfile) => {
    try {
      await AsyncStorage.setItem('userProfile', JSON.stringify(newProfile));
      setProfile(newProfile);
      
      // Sincronizar com o servidor
      await apiService.updateUserProfile(newProfile);
      
      Alert.alert('Sucesso', 'Perfil atualizado com sucesso!');
    } catch (error) {
      console.log('Erro ao salvar perfil:', error);
      Alert.alert('Erro', 'Não foi possível salvar o perfil');
    }
  };

  const toggleRestriction = (restriction) => {
    setProfile(prev => ({
      ...prev,
      dietaryRestrictions: {
        ...prev.dietaryRestrictions,
        [restriction]: !prev.dietaryRestrictions[restriction],
      },
    }));
  };

  const togglePreference = (preference) => {
    setProfile(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [preference]: !prev.preferences[preference],
      },
    }));
  };

  const handleEditProfile = () => {
    setTempProfile({ ...profile });
    setShowEditModal(true);
  };

  const saveEditedProfile = () => {
    saveProfile(tempProfile);
    setShowEditModal(false);
  };

  const clearData = () => {
    Alert.alert(
      'Limpar Dados',
      'Tem certeza que deseja limpar todos os dados do aplicativo?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Limpar',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.clear();
              setProfile({
                name: '',
                email: '',
                dietaryRestrictions: {
                  vegetarian: false,
                  vegan: false,
                  glutenFree: false,
                  lowCarb: false,
                  diabetic: false,
                },
                culinaryLevel: 'beginner',
                preferences: {
                  spicyFood: false,
                  seafood: true,
                  dairy: true,
                },
              });
              Alert.alert('Sucesso', 'Dados limpos com sucesso!');
            } catch (error) {
              Alert.alert('Erro', 'Não foi possível limpar os dados');
            }
          },
        },
      ]
    );
  };

  const RestrictionToggle = ({ label, value, onToggle, icon }) => (
    <View style={styles.toggleRow}>
      <View style={styles.toggleLabel}>
        <Icon name={icon} size={20} color="#666" />
        <Text style={styles.toggleText}>{label}</Text>
      </View>
      <Switch
        value={value}
        onValueChange={onToggle}
        trackColor={{ false: '#ccc', true: '#FF6B35' }}
        thumbColor={value ? '#fff' : '#f4f3f4'}
      />
    </View>
  );

  const LevelButton = ({ level, label, isSelected, onPress }) => (
    <TouchableOpacity
      style={[
        styles.levelButton,
        isSelected && styles.levelButtonSelected,
      ]}
      onPress={onPress}
    >
      <Text
        style={[
          styles.levelButtonText,
          isSelected && styles.levelButtonTextSelected,
        ]}
      >
        {label}
      </Text>
    </TouchableOpacity>
  );

  return (
    <ScrollView style={styles.container}>
      {/* Profile Header */}
      <View style={styles.header}>
        <View style={styles.avatarContainer}>
          <Icon name="person" size={60} color="#fff" />
        </View>
        <Text style={styles.userName}>
          {profile.name || 'Usuário'}
        </Text>
        <Text style={styles.userEmail}>
          {profile.email || 'Adicione seu email'}
        </Text>
        <TouchableOpacity style={styles.editButton} onPress={handleEditProfile}>
          <Icon name="edit" size={16} color="#FF6B35" />
          <Text style={styles.editButtonText}>Editar</Text>
        </TouchableOpacity>
      </View>

      {/* Dietary Restrictions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Restrições Alimentares</Text>
        <RestrictionToggle
          label="Vegetariano"
          value={profile.dietaryRestrictions.vegetarian}
          onToggle={() => toggleRestriction('vegetarian')}
          icon="eco"
        />
        <RestrictionToggle
          label="Vegano"
          value={profile.dietaryRestrictions.vegan}
          onToggle={() => toggleRestriction('vegan')}
          icon="nature"
        />
        <RestrictionToggle
          label="Sem Glúten"
          value={profile.dietaryRestrictions.glutenFree}
          onToggle={() => toggleRestriction('glutenFree')}
          icon="no-food"
        />
        <RestrictionToggle
          label="Low Carb"
          value={profile.dietaryRestrictions.lowCarb}
          onToggle={() => toggleRestriction('lowCarb')}
          icon="trending-down"
        />
        <RestrictionToggle
          label="Diabético"
          value={profile.dietaryRestrictions.diabetic}
          onToggle={() => toggleRestriction('diabetic')}
          icon="local-hospital"
        />
      </View>

      {/* Culinary Level */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Nível Culinário</Text>
        <View style={styles.levelContainer}>
          <LevelButton
            level="beginner"
            label="Iniciante"
            isSelected={profile.culinaryLevel === 'beginner'}
            onPress={() => setProfile(prev => ({ ...prev, culinaryLevel: 'beginner' }))}
          />
          <LevelButton
            level="intermediate"
            label="Intermediário"
            isSelected={profile.culinaryLevel === 'intermediate'}
            onPress={() => setProfile(prev => ({ ...prev, culinaryLevel: 'intermediate' }))}
          />
          <LevelButton
            level="advanced"
            label="Avançado"
            isSelected={profile.culinaryLevel === 'advanced'}
            onPress={() => setProfile(prev => ({ ...prev, culinaryLevel: 'advanced' }))}
          />
        </View>
      </View>

      {/* Preferences */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Preferências</Text>
        <RestrictionToggle
          label="Comida Apimentada"
          value={profile.preferences.spicyFood}
          onToggle={() => togglePreference('spicyFood')}
          icon="whatshot"
        />
        <RestrictionToggle
          label="Frutos do Mar"
          value={profile.preferences.seafood}
          onToggle={() => togglePreference('seafood')}
          icon="set-meal"
        />
        <RestrictionToggle
          label="Laticínios"
          value={profile.preferences.dairy}
          onToggle={() => togglePreference('dairy')}
          icon="local-drink"
        />
      </View>

      {/* Actions */}
      <View style={styles.section}>
        <TouchableOpacity style={styles.saveButton} onPress={() => saveProfile(profile)}>
          <Icon name="save" size={20} color="#fff" />
          <Text style={styles.saveButtonText}>Salvar Preferências</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.clearButton} onPress={clearData}>
          <Icon name="clear-all" size={20} color="#FF3B30" />
          <Text style={styles.clearButtonText}>Limpar Todos os Dados</Text>
        </TouchableOpacity>
      </View>

      {/* Edit Profile Modal */}
      <Modal visible={showEditModal} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Editar Perfil</Text>
            
            <TextInput
              style={styles.input}
              placeholder="Nome"
              value={tempProfile.name}
              onChangeText={(text) =>
                setTempProfile(prev => ({ ...prev, name: text }))
              }
            />
            
            <TextInput
              style={styles.input}
              placeholder="Email"
              value={tempProfile.email}
              onChangeText={(text) =>
                setTempProfile(prev => ({ ...prev, email: text }))
              }
              keyboardType="email-address"
            />
            
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.cancelButton]}
                onPress={() => setShowEditModal(false)}
              >
                <Text style={styles.cancelButtonText}>Cancelar</Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.modalButton, styles.confirmButton]}
                onPress={saveEditedProfile}
              >
                <Text style={styles.confirmButtonText}>Salvar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#FF6B35',
    alignItems: 'center',
    paddingVertical: 30,
    paddingHorizontal: 20,
  },
  avatarContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  userEmail: {
    fontSize: 16,
    color: 'rgba(255,255,255,0.8)',
    marginBottom: 15,
  },
  editButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
  },
  editButtonText: {
    color: '#FF6B35',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 5,
  },
  section: {
    backgroundColor: '#fff',
    margin: 15,
    borderRadius: 12,
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  toggleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  toggleLabel: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  toggleText: {
    fontSize: 16,
    color: '#333',
    marginLeft: 10,
  },
  levelContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  levelButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 8,
    marginHorizontal: 4,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  levelButtonSelected: {
    backgroundColor: '#FF6B35',
    borderColor: '#FF6B35',
  },
  levelButtonText: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
  },
  levelButtonTextSelected: {
    color: '#fff',
    fontWeight: '600',
  },
  saveButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FF6B35',
    paddingVertical: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  clearButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f8f8f8',
    paddingVertical: 15,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#FF3B30',
  },
  clearButtonText: {
    color: '#FF3B30',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 20,
    width: '80%',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    padding: 15,
    fontSize: 16,
    marginBottom: 15,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  modalButton: {
    flex: 0.45,
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#f0f0f0',
  },
  confirmButton: {
    backgroundColor: '#FF6B35',
  },
  cancelButtonText: {
    color: '#666',
    fontSize: 16,
    fontWeight: '600',
  },
  confirmButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default ProfileScreen;