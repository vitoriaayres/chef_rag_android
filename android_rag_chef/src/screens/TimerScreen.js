import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  Modal,
  TextInput,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import Sound from 'react-native-sound';

const TimerScreen = () => {
  const [timers, setTimers] = useState([]);
  const [showAddTimer, setShowAddTimer] = useState(false);
  const [newTimerMinutes, setNewTimerMinutes] = useState('');
  const [newTimerLabel, setNewTimerLabel] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      setTimers(prevTimers => 
        prevTimers.map(timer => {
          if (timer.isRunning && timer.timeLeft > 0) {
            const newTimeLeft = timer.timeLeft - 1;
            if (newTimeLeft === 0) {
              playAlarmSound();
              Alert.alert('⏰ Timer Finalizado!', `${timer.label} está pronto!`);
              return { ...timer, timeLeft: 0, isRunning: false };
            }
            return { ...timer, timeLeft: newTimeLeft };
          }
          return timer;
        })
      );
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const playAlarmSound = () => {
    // Implementar som de alarme
    console.log('🔔 Alarm sound!');
  };

  const addTimer = () => {
    const minutes = parseInt(newTimerMinutes);
    if (!minutes || minutes <= 0) {
      Alert.alert('Erro', 'Digite um tempo válido em minutos');
      return;
    }

    const newTimer = {
      id: Date.now().toString(),
      label: newTimerLabel || `Timer ${timers.length + 1}`,
      totalTime: minutes * 60,
      timeLeft: minutes * 60,
      isRunning: false,
    };

    setTimers([...timers, newTimer]);
    setNewTimerMinutes('');
    setNewTimerLabel('');
    setShowAddTimer(false);
  };

  const toggleTimer = (id) => {
    setTimers(prevTimers =>
      prevTimers.map(timer =>
        timer.id === id
          ? { ...timer, isRunning: !timer.isRunning }
          : timer
      )
    );
  };

  const resetTimer = (id) => {
    setTimers(prevTimers =>
      prevTimers.map(timer =>
        timer.id === id
          ? { ...timer, timeLeft: timer.totalTime, isRunning: false }
          : timer
      )
    );
  };

  const deleteTimer = (id) => {
    setTimers(prevTimers => prevTimers.filter(timer => timer.id !== id));
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getTimerColor = (timer) => {
    if (timer.timeLeft === 0) return '#FF3B30';
    if (timer.isRunning) return '#FF6B35';
    return '#666';
  };

  const addPresetTimer = (minutes, label) => {
    const newTimer = {
      id: Date.now().toString(),
      label,
      totalTime: minutes * 60,
      timeLeft: minutes * 60,
      isRunning: false,
    };
    setTimers([...timers, newTimer]);
  };

  const TimerCard = ({ timer }) => (
    <View style={styles.timerCard}>
      <View style={styles.timerHeader}>
        <Text style={styles.timerLabel}>{timer.label}</Text>
        <TouchableOpacity onPress={() => deleteTimer(timer.id)}>
          <Icon name="close" size={20} color="#666" />
        </TouchableOpacity>
      </View>
      
      <Text style={[styles.timerDisplay, { color: getTimerColor(timer) }]}>
        {formatTime(timer.timeLeft)}
      </Text>
      
      <View style={styles.timerControls}>
        <TouchableOpacity
          style={[styles.controlButton, styles.resetButton]}
          onPress={() => resetTimer(timer.id)}
        >
          <Icon name="refresh" size={20} color="#666" />
        </TouchableOpacity>
        
        <TouchableOpacity
          style={[
            styles.controlButton,
            styles.playButton,
            timer.isRunning && styles.pauseButton
          ]}
          onPress={() => toggleTimer(timer.id)}
        >
          <Icon
            name={timer.isRunning ? "pause" : "play-arrow"}
            size={24}
            color="#fff"
          />
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Preset Timers */}
      <View style={styles.presetsSection}>
        <Text style={styles.sectionTitle}>Timers Rápidos</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <TouchableOpacity
            style={styles.presetButton}
            onPress={() => addPresetTimer(5, 'Ovos Cozidos')}
          >
            <Icon name="schedule" size={20} color="#FF6B35" />
            <Text style={styles.presetText}>5 min</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={styles.presetButton}
            onPress={() => addPresetTimer(15, 'Massa')}
          >
            <Icon name="schedule" size={20} color="#FF6B35" />
            <Text style={styles.presetText}>15 min</Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={styles.presetButton}
            onPress={() => addPresetTimer(30, 'Assado')}
          >
            <Icon name="schedule" size={20} color="#FF6B35" />
            <Text style={styles.presetText}>30 min</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* Active Timers */}
      <ScrollView style={styles.timersContainer}>
        {timers.length > 0 ? (
          timers.map(timer => (
            <TimerCard key={timer.id} timer={timer} />
          ))
        ) : (
          <View style={styles.emptyState}>
            <Icon name="timer" size={60} color="#ccc" />
            <Text style={styles.emptyStateText}>Nenhum timer ativo</Text>
            <Text style={styles.emptyStateSubtext}>
              Crie um timer personalizado ou use os presets
            </Text>
          </View>
        )}
      </ScrollView>

      {/* Add Timer Button */}
      <TouchableOpacity
        style={styles.addButton}
        onPress={() => setShowAddTimer(true)}
      >
        <Icon name="add" size={30} color="#fff" />
      </TouchableOpacity>

      {/* Add Timer Modal */}
      <Modal visible={showAddTimer} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Novo Timer</Text>
            
            <TextInput
              style={styles.input}
              placeholder="Nome do timer (opcional)"
              value={newTimerLabel}
              onChangeText={setNewTimerLabel}
            />
            
            <TextInput
              style={styles.input}
              placeholder="Tempo em minutos"
              value={newTimerMinutes}
              onChangeText={setNewTimerMinutes}
              keyboardType="numeric"
            />
            
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.cancelButton]}
                onPress={() => setShowAddTimer(false)}
              >
                <Text style={styles.cancelButtonText}>Cancelar</Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.modalButton, styles.confirmButton]}
                onPress={addTimer}
              >
                <Text style={styles.confirmButtonText}>Criar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  presetsSection: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  presetButton: {
    alignItems: 'center',
    backgroundColor: '#f8f8f8',
    borderRadius: 10,
    padding: 15,
    marginRight: 10,
    minWidth: 80,
  },
  presetText: {
    marginTop: 5,
    fontSize: 12,
    color: '#666',
    fontWeight: '600',
  },
  timersContainer: {
    flex: 1,
    padding: 20,
  },
  timerCard: {
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  timerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  timerLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  timerDisplay: {
    fontSize: 48,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
    fontFamily: 'monospace',
  },
  timerControls: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  controlButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 10,
  },
  resetButton: {
    backgroundColor: '#f0f0f0',
  },
  playButton: {
    backgroundColor: '#FF6B35',
  },
  pauseButton: {
    backgroundColor: '#666',
  },
  emptyState: {
    alignItems: 'center',
    padding: 40,
  },
  emptyStateText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
    marginTop: 15,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    marginTop: 5,
  },
  addButton: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#FF6B35',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
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

export default TimerScreen;