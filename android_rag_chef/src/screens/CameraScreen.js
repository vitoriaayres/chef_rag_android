import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Image,
  Modal,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { launchCamera, launchImageLibrary } from 'react-native-image-picker';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { apiService } from '../services/APIService';

const { width, height } = Dimensions.get('window');

const CameraScreen = ({ navigation }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [showOptions, setShowOptions] = useState(false);

  const imagePickerOptions = {
    mediaType: 'photo',
    quality: 0.8,
    maxWidth: 1024,
    maxHeight: 1024,
    includeBase64: false,
  };

  const handleTakePhoto = () => {
    setShowOptions(false);
    launchCamera(imagePickerOptions, handleImageResponse);
  };

  const handleSelectFromGallery = () => {
    setShowOptions(false);
    launchImageLibrary(imagePickerOptions, handleImageResponse);
  };

  const handleImageResponse = (response) => {
    if (response.didCancel || response.error) {
      return;
    }

    if (response.assets && response.assets[0]) {
      setSelectedImage(response.assets[0]);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) {
      Alert.alert('Erro', 'Por favor, selecione uma imagem primeiro.');
      return;
    }

    setAnalyzing(true);
    try {
      const result = await apiService.analyzeImage(selectedImage.uri, {
        multipleIngredients: true,
      });

      Alert.alert(
        'Ingredientes Detectados',
        `Encontrados: ${result.ingredients.join(', ')}`,
        [
          {
            text: 'Ver Receitas',
            onPress: () => {
              navigation.navigate('Recipes', { 
                ingredients: result.ingredients 
              });
            },
          },
          { text: 'OK' },
        ]
      );
    } catch (error) {
      Alert.alert('Erro na Análise', error.message || 'Não foi possível analisar a imagem.');
    } finally {
      setAnalyzing(false);
    }
  };

  const resetImage = () => {
    setSelectedImage(null);
  };

  return (
    <View style={styles.container}>
      {selectedImage ? (
        <View style={styles.imageContainer}>
          <Image source={{ uri: selectedImage.uri }} style={styles.selectedImage} />
          
          <View style={styles.actionButtons}>
            <TouchableOpacity 
              style={[styles.actionButton, styles.resetButton]} 
              onPress={resetImage}
            >
              <Icon name="refresh" size={24} color="#fff" />
              <Text style={styles.buttonText}>Nova Foto</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={[styles.actionButton, styles.analyzeButton]} 
              onPress={analyzeImage}
              disabled={analyzing}
            >
              {analyzing ? (
                <ActivityIndicator color="#fff" size="small" />
              ) : (
                <Icon name="search" size={24} color="#fff" />
              )}
              <Text style={styles.buttonText}>
                {analyzing ? 'Analisando...' : 'Analisar'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      ) : (
        <View style={styles.cameraContainer}>
          <View style={styles.placeholder}>
            <Icon name="add-a-photo" size={80} color="#ccc" />
            <Text style={styles.placeholderText}>
              Capture ou selecione uma foto dos seus ingredientes
            </Text>
          </View>
          
          <TouchableOpacity 
            style={styles.captureButton}
            onPress={() => setShowOptions(true)}
          >
            <Icon name="camera-alt" size={30} color="#fff" />
          </TouchableOpacity>
        </View>
      )}

      {/* Modal de opções */}
      <Modal
        visible={showOptions}
        transparent
        animationType="slide"
        onRequestClose={() => setShowOptions(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Selecionar Imagem</Text>
            
            <TouchableOpacity 
              style={styles.modalButton}
              onPress={handleTakePhoto}
            >
              <Icon name="camera-alt" size={24} color="#FF6B35" />
              <Text style={styles.modalButtonText}>Tirar Foto</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={styles.modalButton}
              onPress={handleSelectFromGallery}
            >
              <Icon name="photo-library" size={24} color="#FF6B35" />
              <Text style={styles.modalButtonText}>Galeria</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={[styles.modalButton, styles.cancelButton]}
              onPress={() => setShowOptions(false)}
            >
              <Text style={styles.cancelButtonText}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  cameraContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  placeholder: {
    alignItems: 'center',
    marginBottom: 50,
  },
  placeholderText: {
    color: '#ccc',
    fontSize: 16,
    textAlign: 'center',
    marginTop: 20,
    lineHeight: 24,
  },
  captureButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#FF6B35',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  imageContainer: {
    flex: 1,
  },
  selectedImage: {
    flex: 1,
    width: width,
    resizeMode: 'contain',
  },
  actionButtons: {
    flexDirection: 'row',
    padding: 20,
    justifyContent: 'space-between',
    backgroundColor: 'rgba(0,0,0,0.7)',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 25,
    flex: 0.45,
    justifyContent: 'center',
  },
  resetButton: {
    backgroundColor: '#666',
  },
  analyzeButton: {
    backgroundColor: '#FF6B35',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 20,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  modalButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 15,
    paddingHorizontal: 20,
    marginBottom: 10,
    backgroundColor: '#f8f8f8',
    borderRadius: 10,
  },
  modalButtonText: {
    fontSize: 16,
    marginLeft: 15,
    color: '#333',
    fontWeight: '500',
  },
  cancelButton: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    marginTop: 10,
  },
  cancelButtonText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    width: '100%',
  },
});

export default CameraScreen;