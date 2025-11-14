#!/usr/bin/env python3
"""
Módulo de Reconhecimento de Voz para o Chef RAG
Permite entrada de ingredientes por comando de voz
"""

import speech_recognition as sr
import time
import threading
from typing import Optional, List

class VoiceRecognition:
    """
    Classe para gerenciar reconhecimento de voz
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.last_result = None
        
        # Configurações
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
    def check_microphone_available(self) -> bool:
        """Verifica se o microfone está disponível"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return True
        except Exception as e:
            print(f"❌ Erro ao acessar microfone: {e}")
            return False
    
    def recognize_ingredients(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Reconhece ingredientes por voz
        
        Args:
            timeout: Tempo limite para começar a falar
            phrase_time_limit: Tempo limite para terminar de falar
            
        Returns:
            String com ingredientes reconhecidos ou None se erro
        """
        if not self.microphone:
            if not self.check_microphone_available():
                return None
        
        try:
            print("🎤 Diga os ingredientes que você tem...")
            print("💡 Exemplo: 'Tenho tomate, cebola e alho'")
            
            with self.microphone as source:
                print("🔵 Ajustando para ruído ambiente...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("🟢 Pode falar agora!")
                
                # Captura o áudio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
            print("🧠 Processando fala...")
            
            # Tenta múltiplos serviços de reconhecimento
            result = None
            
            # 1. Tenta Google Web Speech API (melhor para português)
            try:
                result = self.recognizer.recognize_google(audio, language='pt-BR')
                print(f"✅ Google: '{result}'")
            except sr.UnknownValueError:
                print("⚠️ Google não conseguiu entender")
            except sr.RequestError as e:
                print(f"⚠️ Erro no Google Speech: {e}")
            
            # 2. Se Google falhou, tenta reconhecimento offline (se disponível)
            if not result:
                try:
                    result = self.recognizer.recognize_sphinx(audio)
                    print(f"✅ Sphinx (offline): '{result}'")
                except sr.UnknownValueError:
                    print("⚠️ Reconhecimento offline também falhou")
                except sr.RequestError:
                    print("⚠️ Reconhecimento offline não disponível")
                except Exception:
                    pass  # Sphinx pode não estar disponível
            
            if result:
                # Processa o resultado para extrair ingredientes
                ingredients = self._extract_ingredients_from_text(result)
                self.last_result = ingredients
                return ingredients
            else:
                print("❌ Nenhum serviço conseguiu reconhecer a fala")
                return None
                
        except sr.WaitTimeoutError:
            print("⏰ Timeout - nenhuma fala detectada")
            print("💡 Tente falar mais próximo do microfone")
            return None
        except Exception as e:
            print(f"❌ Erro durante reconhecimento: {e}")
            return None
    
    def _extract_ingredients_from_text(self, text: str) -> str:
        """
        Extrai e limpa ingredientes do texto reconhecido
        
        Args:
            text: Texto reconhecido pelo speech recognition
            
        Returns:
            String com ingredientes limpos e formatados
        """
        # Converte para minúsculas
        text = text.lower()
        
        # Remove palavras irrelevantes
        stop_words = [
            'tenho', 'eu', 'tenho', 'tem', 'temos', 'há', 'existe', 'existem',
            'aqui', 'na', 'no', 'da', 'do', 'de', 'em', 'com', 'para',
            'que', 'um', 'uma', 'uns', 'umas', 'o', 'a', 'os', 'as',
            'geladeira', 'cozinha', 'mesa', 'hoje', 'agora', 'disponível',
            'disponíveis', 'fresh', 'fresco', 'frescos', 'fresca', 'frescas'
        ]
        
        words = text.split()
        cleaned_words = [word for word in words if word not in stop_words]
        
        # Junta palavras novamente
        cleaned_text = ' '.join(cleaned_words)
        
        # Substitui conectores por vírgulas
        connectors = [' e ', ' mais ', ' também ', ' além de ', ' junto com ']
        for connector in connectors:
            cleaned_text = cleaned_text.replace(connector, ', ')
        
        # Remove vírgulas duplas e espaços extras
        cleaned_text = cleaned_text.replace(',,', ',')
        cleaned_text = ' '.join(cleaned_text.split())
        
        # Capitaliza primeiras letras
        ingredients_list = [ing.strip().title() for ing in cleaned_text.split(',') if ing.strip()]
        
        return ', '.join(ingredients_list)
    
    def continuous_listen(self, callback_function, stop_event):
        """
        Escuta continuamente por comandos de voz
        
        Args:
            callback_function: Função chamada quando ingredientes são reconhecidos
            stop_event: Threading event para parar a escuta
        """
        self.is_listening = True
        
        while not stop_event.is_set():
            try:
                ingredients = self.recognize_ingredients(timeout=1)
                if ingredients:
                    callback_function(ingredients)
                    
                time.sleep(0.1)  # Pequena pausa para evitar sobrecarga
                
            except Exception as e:
                print(f"⚠️ Erro na escuta contínua: {e}")
                time.sleep(1)
        
        self.is_listening = False
    
    def test_microphone(self) -> dict:
        """
        Testa o microfone e retorna informações de status
        
        Returns:
            Dicionário com informações do teste
        """
        result = {
            'available': False,
            'message': '',
            'details': {}
        }
        
        try:
            # Lista microfones disponíveis
            mic_list = sr.Microphone.list_microphone_names()
            result['details']['microphones'] = mic_list
            
            if not mic_list:
                result['message'] = 'Nenhum microfone encontrado'
                return result
            
            # Testa microfone padrão
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                result['details']['energy_threshold'] = self.recognizer.energy_threshold
            
            result['available'] = True
            result['message'] = f'Microfone funcionando! {len(mic_list)} dispositivo(s) encontrado(s)'
            
        except Exception as e:
            result['message'] = f'Erro ao testar microfone: {e}'
            
        return result

# Instância global
voice_recognition = VoiceRecognition()

def quick_voice_input() -> Optional[str]:
    """Função rápida para entrada de voz"""
    return voice_recognition.recognize_ingredients()

if __name__ == "__main__":
    # Teste do módulo
    print("🎤 Teste do Reconhecimento de Voz")
    print("=" * 40)
    
    # Testa microfone
    test_result = voice_recognition.test_microphone()
    print(f"Status: {test_result['message']}")
    
    if test_result['available']:
        print("\n🗣️ Teste de reconhecimento:")
        ingredients = voice_recognition.recognize_ingredients()
        
        if ingredients:
            print(f"✅ Ingredientes reconhecidos: {ingredients}")
        else:
            print("❌ Nenhum ingrediente reconhecido")
    
    print("=" * 40)