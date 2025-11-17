#!/usr/bin/env python3
"""
Webcam Inteligente com YOLO para Detecção Múltipla de Ingredientes
Sistema de Análise de Comida em Tempo Real
"""

import cv2
import os
import time
import threading
import numpy as np
from datetime import datetime
import torch
from pathlib import Path

# Imports do projeto
from core_logic import config
from core_logic import sistema_rag

class FoodDetectionWebcam:
    def __init__(self):
        self.snapshot_path = os.path.join(config.BASE_DIR, "..", "temp_snapshot.jpg")
        self.status = "ready"
        self.last_ingredients = []
        self.recipe_count = 0
        self.show_popup = False
        self.popup_timer = 0
        self.rotation_angle = 0
        self.cap = None
        
        # YOLO setup
        self.setup_yolo()
        
    def setup_yolo(self):
        """Configura o modelo YOLO para detecção de comida"""
        try:
            print("🔄 Carregando modelo YOLO...")
            
            # Tentar carregar YOLOv8 otimizado para comida
            try:
                from ultralytics import YOLO
                
                # Usar modelo pré-treinado COCO que inclui muitas comidas
                self.yolo_model = YOLO('yolov8n.pt')  # Nano version para velocidade
                
                # Classes de comida do COCO dataset
                self.food_classes = {
                    47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli',
                    51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut',
                    55: 'cake', 56: 'banana', 57: 'rice'
                }
                
                # Tradução para português
                self.food_translation = {
                    'apple': 'maçã', 'sandwich': 'sanduíche', 'orange': 'laranja',
                    'broccoli': 'brócolis', 'carrot': 'cenoura', 'hot dog': 'cachorro quente',
                    'pizza': 'pizza', 'donut': 'rosquinha', 'cake': 'bolo',
                    'banana': 'banana', 'rice': 'arroz'
                }
                
                self.use_yolo = True
                print("✅ YOLO carregado com sucesso!")
                
            except Exception as e:
                print(f"⚠️ YOLO não disponível: {e}")
                self.use_yolo = False
                
        except Exception as e:
            print(f"❌ Erro ao configurar YOLO: {e}")
            self.use_yolo = False
    
    def detect_food_with_yolo(self, frame):
        """Detecta múltiplos alimentos usando YOLO"""
        if not self.use_yolo:
            return []
        
        try:
            # Detectar objetos
            results = self.yolo_model(frame, verbose=False)
            detected_foods = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Extrair informações
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        
                        # Verificar se é comida e confiança alta
                        if class_id in self.food_classes and confidence > 0.5:
                            food_name = self.food_classes[class_id]
                            food_portuguese = self.food_translation.get(food_name, food_name)
                            
                            # Coordenadas da caixa
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            
                            detected_foods.append({
                                'name': food_portuguese,
                                'confidence': confidence,
                                'bbox': (int(x1), int(y1), int(x2), int(y2))
                            })
            
            return detected_foods
            
        except Exception as e:
            print(f"❌ Erro na detecção YOLO: {e}")
            return []
    
    def draw_food_detections(self, frame, detections):
        """Desenha as detecções na tela"""
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            name = detection['name']
            confidence = detection['confidence']
            
            # Desenhar caixa
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Label
            label = f"{name} ({confidence:.1%})"
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def draw_modern_interface(self, frame):
        """Desenha interface moderna na webcam"""
        height, width = frame.shape[:2]
        
        # Cores modernas
        primary_color = (67, 126, 235)  # Azul
        success_color = (46, 204, 113)  # Verde
        warning_color = (241, 196, 15)  # Amarelo
        danger_color = (231, 76, 60)    # Vermelho
        dark_overlay = (30, 30, 30)     # Cinza escuro
        
        # Overlay semi-transparente no topo
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 120), dark_overlay, -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Título principal
        title = "CHEF RAG - Detecção Inteligente de Comida"
        cv2.putText(frame, title, (20, 35), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
        
        # Data e hora
        now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        cv2.putText(frame, now, (width - 280, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Status indicator
        if self.status == "ready":
            status_color = primary_color
            status_text = "Pronto para detectar ingredientes"
            status_icon = "●"
        elif self.status == "scanning":
            status_color = warning_color
            status_text = "Analisando ingredientes..."
            status_icon = "⚡"
        elif self.status == "success":
            status_color = success_color
            status_text = f"Detectados {len(self.last_ingredients)} ingredientes"
            status_icon = "✓"
        elif self.status == "error":
            status_color = danger_color
            status_text = "Nenhum ingrediente detectado"
            status_icon = "✗"
        
        # Desenhar status
        cv2.putText(frame, f"{status_icon} {status_text}", (20, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        # Instruções
        instructions = [
            "E - Escanear ingredientes | Q - Sair | R - Rotacionar | H - Histórico"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (20, 90 + i * 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Mostrar ingredientes detectados
        if self.last_ingredients:
            cv2.putText(frame, f"Ingredientes: {', '.join(self.last_ingredients)}", 
                       (20, height - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, success_color, 2)
        
        return frame
    
    def show_results_popup(self, frame):
        """Mostra popup com resultados"""
        height, width = frame.shape[:2]
        
        # Overlay escuro
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Popup central
        popup_w, popup_h = 600, 400
        popup_x = (width - popup_w) // 2
        popup_y = (height - popup_h) // 2
        
        # Fundo do popup
        cv2.rectangle(frame, (popup_x, popup_y), (popup_x + popup_w, popup_y + popup_h), (40, 40, 40), -1)
        cv2.rectangle(frame, (popup_x, popup_y), (popup_x + popup_w, popup_y + popup_h), (67, 126, 235), 3)
        
        # Título
        cv2.putText(frame, "Ingredientes Detectados!", (popup_x + 20, popup_y + 40), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
        
        # Lista de ingredientes
        if self.last_ingredients:
            cv2.putText(frame, "Encontrados:", (popup_x + 20, popup_y + 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (46, 204, 113), 2)
            
            for i, ingredient in enumerate(self.last_ingredients[:5]):  # Máximo 5
                cv2.putText(frame, f"• {ingredient}", (popup_x + 40, popup_y + 110 + i * 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Número de receitas
        cv2.putText(frame, f"Receitas encontradas: {self.recipe_count}", 
                   (popup_x + 20, popup_y + 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (241, 196, 15), 1)
        
        # Instruções
        instructions = [
            "• Verifique o terminal para escolher a receita",
            "• Pressione qualquer tecla para continuar",
            "• Pressione 'Q' para sair"
        ]
        
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (popup_x + 20, popup_y + 290 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        return frame
    
    def initialize_camera(self):
        """Inicializa a câmera"""
        print("🔄 Inicializando câmera...")
        
        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
        
        for backend in backends:
            try:
                self.cap = cv2.VideoCapture(0, backend)
                if self.cap.isOpened():
                    # Configurações otimizadas
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    
                    print(f"✅ Câmera inicializada com backend: {backend}")
                    return True
            except Exception as e:
                print(f"❌ Erro com backend {backend}: {e}")
        
        return False
    
    def process_detection_results(self, ingredients_list):
        """Processa resultados e busca receitas"""
        if not ingredients_list:
            print("❌ Nenhum ingrediente detectado")
            self.status = "error"
            return
        
        # Usar sistema CSV para buscar receitas
        ingredients_str = ", ".join(ingredients_list)
        print(f"🔍 Buscando receitas para: {ingredients_str}")
        
        try:
            # Importar sistema de busca CSV
            from main import extrair_receitas_csv
            receitas = extrair_receitas_csv(ingredients_str)
            
            if receitas:
                self.recipe_count = len(receitas)
                print(f"\n🍽️ {self.recipe_count} RECEITAS ENCONTRADAS:")
                print("="*70)
                
                # Mostrar receitas com opção de seleção
                for i, receita in enumerate(receitas[:5], 1):
                    print(f"\n{i}. 📋 {receita['titulo']}")
                    print(f"   📊 Compatibilidade: {receita['score']:.1f}%")
                    print(f"   📂 {receita['categoria']} | ⏰ {receita['tempo_preparo']}")
                    print(f"   🥬 {receita['ingredientes_busca']}")
                
                print("="*70)
                print("🎯 ESCOLHA SUA RECEITA NO TERMINAL ABAIXO:")
                
                # Thread para seleção de receita
                threading.Thread(target=self.recipe_selection_thread, args=(receitas,)).start()
                
            else:
                self.recipe_count = 0
                print("❌ Nenhuma receita encontrada")
                
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            self.status = "error"
    
    def recipe_selection_thread(self, receitas):
        """Thread para seleção de receita pelo usuário"""
        try:
            while True:
                escolha = input(f"\n👨‍🍳 Escolha uma receita (1-{min(5, len(receitas))}) ou 0 para continuar: ").strip()
                
                if escolha == "0":
                    break
                
                try:
                    idx = int(escolha) - 1
                    if 0 <= idx < len(receitas[:5]):
                        receita_escolhida = receitas[idx]
                        
                        # Importar e mostrar receita completa
                        from main import mostrar_modo_preparo_csv
                        mostrar_modo_preparo_csv(receita_escolhida)
                        break
                    else:
                        print(f"❌ Escolha entre 1 e {min(5, len(receitas))}")
                except ValueError:
                    print("❌ Digite apenas números")
                    
        except Exception as e:
            print(f"❌ Erro na seleção: {e}")
    
    def run(self):
        """Loop principal da webcam"""
        if not self.initialize_camera():
            print("❌ Falha na inicialização da câmera")
            return
        
        print("🚀 Webcam iniciada! Pressione 'E' para detectar ingredientes")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Aplicar rotação se necessário
            if self.rotation_angle > 0:
                center = (frame.shape[1]//2, frame.shape[0]//2)
                rotation_matrix = cv2.getRotationMatrix2D(center, self.rotation_angle, 1.0)
                frame = cv2.warpAffine(frame, rotation_matrix, (frame.shape[1], frame.shape[0]))
            
            # Detectar comida com YOLO em tempo real (opcional)
            if self.use_yolo and self.status == "ready":
                detections = self.detect_food_with_yolo(frame)
                if detections:
                    frame = self.draw_food_detections(frame, detections)
            
            # Desenhar interface
            frame = self.draw_modern_interface(frame)
            
            # Mostrar popup se necessário
            if self.show_popup:
                frame = self.show_results_popup(frame)
                self.popup_timer += 1
                if self.popup_timer > 300:  # 10 segundos a 30fps
                    self.show_popup = False
                    self.popup_timer = 0
                    self.status = "ready"
            
            cv2.imshow('Chef RAG - Detecção de Ingredientes', frame)
            
            # Controles
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("👋 Encerrando webcam...")
                break
                
            elif key == ord('r'):
                self.rotation_angle = (self.rotation_angle + 90) % 360
                print(f"🔄 Rotação: {self.rotation_angle}°")
                
            elif key == ord('e'):
                self.capture_and_analyze(frame)
                
            elif key == ord('h'):
                self.show_history()
                
            elif self.show_popup and key != 255:
                self.show_popup = False
                self.popup_timer = 0
                self.status = "ready"
        
        self.cleanup()
    
    def capture_and_analyze(self, frame):
        """Captura frame e analisa ingredientes"""
        self.status = "scanning"
        print("\n🔍 ANÁLISE INICIADA")
        print("=" * 50)
        
        # Salvar frame
        cv2.imwrite(self.snapshot_path, frame)
        print("📸 Imagem capturada")
        
        # Detectar com YOLO primeiro
        ingredients_yolo = []
        if self.use_yolo:
            print("🤖 Detectando com YOLO...")
            detections = self.detect_food_with_yolo(frame)
            ingredients_yolo = [d['name'] for d in detections]
        
        # Detectar com sistema original também
        print("🧠 Analisando com IA...")
        try:
            ingredient_ai = sistema_rag.extract_ingredients_from_image(self.snapshot_path)
            if "Erro" not in ingredient_ai:
                ingredients_yolo.append(ingredient_ai)
        except:
            pass
        
        # Combinar resultados
        self.last_ingredients = list(set(ingredients_yolo))  # Remove duplicatas
        
        if self.last_ingredients:
            print(f"✅ Detectados: {', '.join(self.last_ingredients)}")
            self.status = "success"
            self.show_popup = True
            self.popup_timer = 0
            
            # Processar resultados
            self.process_detection_results(self.last_ingredients)
        else:
            print("❌ Nenhum ingrediente detectado")
            self.status = "error"
            time.sleep(1)
    
    def show_history(self):
        """Mostra histórico"""
        print("\n📊 ABRINDO HISTÓRICO...")
        try:
            from visualizador_historico import main as history_main
            history_main()
        except:
            print("❌ Histórico não disponível")
    
    def cleanup(self):
        """Limpeza de recursos"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        if os.path.exists(self.snapshot_path):
            os.remove(self.snapshot_path)
        
        print("🧹 Recursos liberados!")

def run_food_detection_webcam():
    """Função principal para executar a webcam"""
    webcam = FoodDetectionWebcam()
    webcam.run()

if __name__ == "__main__":
    run_food_detection_webcam()