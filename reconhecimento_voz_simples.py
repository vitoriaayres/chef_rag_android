#!/usr/bin/env python3
"""
Interface Simplificada de Reconhecimento de Voz - Chef RAG v2
=============================================================

Interface gráfica completa para reconhecimento de voz com histórico
persistente no banco de dados e análise avançada de ingredientes.

Funcionalidades principais:
🎤 Reconhecimento de voz real (Google Speech API)
✍️ Entrada manual como alternativa
📊 Histórico completo no banco SQLite
📈 Estatísticas detalhadas de uso
🔍 Análise e comparação de textos
💾 Exportação completa de dados
🔄 Sistema de fallback inteligente

⚡ Versão otimizada que funciona apenas com tkinter como dependência base,
com reconhecimento real quando as bibliotecas de voz estão disponíveis.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
from datetime import datetime
import json
import os
from typing import Optional, Dict, List
import uuid

# Importação do banco de dados
from core_logic.database import history_db

# Importações para reconhecimento de voz
try:
    import speech_recognition as sr
    import pyaudio
    VOICE_AVAILABLE = True
except ImportError as e:
    sr = None
    pyaudio = None
    VOICE_AVAILABLE = False
    print(f"⚠️ Dependências de voz não encontradas: {e}. Usando modo simulação.")

class SimpleVoiceInterface:
    """Interface simplificada para reconhecimento de voz e análise de ingredientes"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.current_result = None
        self.session_id = str(uuid.uuid4())  # ID único para esta sessão
        
        # Configurar reconhecimento de voz
        if VOICE_AVAILABLE and sr:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            # Ajustar para ruído ambiente
            self.adjust_for_ambient_noise()
        else:
            self.recognizer = None
            self.microphone = None
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("🎤 Chef RAG v2 - Interface de Voz Inteligente")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        
        # Centralizar janela
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#2196F3', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🎤 Interface de Voz Inteligente - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), bg='#2196F3', fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_main_tab()
        self.setup_history_tab()
        self.setup_analysis_tab()
        
    def setup_main_tab(self):
        """Configura aba principal"""
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="🎤 Reconhecimento")
        
        # Frame de controles
        controls_frame = ttk.LabelFrame(self.main_frame, text="🎛️ Controles", padding=15)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(controls_frame)
        btn_frame.pack(fill=tk.X)
        
        voice_text = "🎤 Reconhecimento de Voz" if VOICE_AVAILABLE else "🎤 Simular Reconhecimento"
        self.record_btn = ttk.Button(btn_frame, text=voice_text, 
                                   command=self.start_voice_recognition)
        self.record_btn.pack(side=tk.LEFT, padx=5)
        
        self.input_btn = ttk.Button(btn_frame, text="✍️ Entrada Manual", 
                                  command=self.manual_input)
        self.input_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="🧹 Limpar", 
                                  command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        status_frame = ttk.LabelFrame(self.main_frame, text="📊 Status", padding=15)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Pronto para reconhecimento de voz", 
                                    font=('Arial', 10))
        self.status_label.pack()
        
        # Métricas
        metrics_frame = ttk.Frame(status_frame)
        metrics_frame.pack(fill=tk.X, pady=5)
        
        self.accuracy_label = ttk.Label(metrics_frame, text="Acurácia: --", font=('Arial', 10))
        self.accuracy_label.pack(side=tk.LEFT)
        
        self.time_label = ttk.Label(metrics_frame, text="Tempo: --", font=('Arial', 10))
        self.time_label.pack(side=tk.LEFT, padx=(20,0))
        
        self.confidence_label = ttk.Label(metrics_frame, text="Confiança: --", font=('Arial', 10))
        self.confidence_label.pack(side=tk.LEFT, padx=(20,0))
        
        # Resultados
        results_frame = ttk.LabelFrame(self.main_frame, text="📝 Resultados", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Texto original
        ttk.Label(results_frame, text="Texto Reconhecido:").pack(anchor=tk.W)
        self.original_text = tk.Text(results_frame, height=4, font=('Consolas', 10))
        self.original_text.pack(fill=tk.X, pady=5)
        
        # Ingredientes
        ttk.Label(results_frame, text="Ingredientes Identificados:").pack(anchor=tk.W, pady=(10,0))
        self.ingredients_text = tk.Text(results_frame, height=3, font=('Consolas', 10, 'bold'))
        self.ingredients_text.pack(fill=tk.X, pady=5)
        
        # Análise
        ttk.Label(results_frame, text="Análise:").pack(anchor=tk.W, pady=(10,0))
        self.analysis_text = tk.Text(results_frame, height=3, font=('Consolas', 10))
        self.analysis_text.pack(fill=tk.X, pady=5)
        
        # Botões de ação
        action_frame = ttk.Frame(results_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        self.save_btn = ttk.Button(action_frame, text="💾 Salvar Resultado", 
                                 command=self.save_result)
        self.save_btn.pack(side=tk.LEFT)
        
        self.search_btn = ttk.Button(action_frame, text="🔍 Buscar Receitas", 
                                   command=self.search_recipes)
        self.search_btn.pack(side=tk.LEFT, padx=(10,0))
    
    def setup_history_tab(self):
        """Configura aba de histórico"""
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📊 Histórico")
        
        # Controles
        controls_frame = ttk.Frame(self.history_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls_frame, text="🔄 Atualizar", 
                 command=self.update_history).pack(side=tk.LEFT)
        
        ttk.Button(controls_frame, text="📊 Exportar", 
                 command=self.export_history).pack(side=tk.LEFT, padx=(10,0))
        
        ttk.Button(controls_frame, text="🧹 Limpar Histórico", 
                 command=self.clear_history).pack(side=tk.LEFT, padx=(10,0))
        
        # Lista do histórico
        history_list_frame = ttk.LabelFrame(self.history_frame, text="📋 Histórico de Reconhecimentos", padding=10)
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('Data/Hora', 'Texto', 'Ingredientes', 'Acurácia')
        self.history_tree = ttk.Treeview(history_list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Detalhes do item selecionado
        details_frame = ttk.LabelFrame(self.history_frame, text="📄 Detalhes", padding=10)
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.details_text = tk.Text(details_frame, height=5, font=('Consolas', 9))
        self.details_text.pack(fill=tk.X)
        
        # Bind para mostrar detalhes
        self.history_tree.bind('<<TreeviewSelect>>', self.show_details)
        
    def setup_analysis_tab(self):
        """Configura aba de análise"""
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="📄 Análise")
        
        # Upload de arquivo
        upload_frame = ttk.LabelFrame(self.analysis_frame, text="📁 Analisar Texto", padding=15)
        upload_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Entrada de texto
        ttk.Label(upload_frame, text="Cole ou digite o texto para análise:").pack(anchor=tk.W)
        
        self.analysis_input = tk.Text(upload_frame, height=8, font=('Consolas', 10))
        self.analysis_input.pack(fill=tk.X, pady=5)
        
        btn_frame = ttk.Frame(upload_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="📂 Carregar Arquivo", 
                 command=self.load_text_file).pack(side=tk.LEFT)
        
        ttk.Button(btn_frame, text="🔍 Analisar", 
                 command=self.analyze_text).pack(side=tk.LEFT, padx=(10,0))
        
        # Resultados da análise
        analysis_results_frame = ttk.LabelFrame(self.analysis_frame, text="📊 Resultados da Análise", padding=15)
        analysis_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.analysis_output = tk.Text(analysis_results_frame, height=12, font=('Consolas', 10))
        self.analysis_output.pack(fill=tk.BOTH, expand=True)
        
        # Comparação
        compare_frame = ttk.LabelFrame(self.analysis_frame, text="⚖️ Comparação", padding=15)
        compare_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(compare_frame, text="🔄 Comparar com Último Reconhecimento", 
                 command=self.compare_with_last).pack()
    
    def adjust_for_ambient_noise(self):
        """Ajusta o reconhecedor para o ruído ambiente"""
        if not VOICE_AVAILABLE:
            return
            
        try:
            with self.microphone as source:
                self.status_label.config(text="🔧 Calibrando microfone...")
                self.root.update()
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.status_label.config(text="✅ Microfone calibrado")
        except Exception as e:
            self.status_label.config(text=f"❌ Erro na calibração: {str(e)}")
            print(f"Erro na calibração do microfone: {e}")
    
    def start_voice_recognition(self):
        """Inicia reconhecimento de voz real ou simulação"""
        if VOICE_AVAILABLE and self.recognizer and self.microphone:
            self.real_voice_recognition()
        else:
            self.simulate_recognition()
    
    def real_voice_recognition(self):
        """Reconhecimento de voz real usando microfone"""
        start_time = time.time()
        
        try:
            # Desabilitar botão
            self.record_btn.config(state='disabled')
            self.status_label.config(text="🎤 Fale agora... (5 segundos)")
            self.root.update()
            
            # Capturar áudio
            with self.microphone as source:
                # Ouvir por até 5 segundos
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
            self.status_label.config(text="🧠 Processando fala...")
            self.root.update()
            
            # Reconhecimento usando Google (gratuito)
            recognition_engine = 'google'
            try:
                text = self.recognizer.recognize_google(audio, language='pt-BR')
                confidence = 0.9  # Google não retorna confiança, estimamos alta
            except sr.UnknownValueError:
                # Tentar com Sphinx offline se falhar
                try:
                    recognition_engine = 'sphinx'
                    text = self.recognizer.recognize_sphinx(audio, language='pt-BR')
                    confidence = 0.7  # Sphinx tem menor precisão
                except:
                    raise sr.UnknownValueError("Não consegui entender o áudio")
            
            processing_time = time.time() - start_time
            
            # Processar resultado
            result = {
                'text': text,
                'ingredients': self.extract_ingredients(text),
                'confidence': confidence,
                'processing_time': processing_time
            }
            
            # Mostrar resultados
            self.show_results(result)
            self.status_label.config(text="✅ Reconhecimento concluído com sucesso!")
            
            # Salvar resultado
            self.current_result = result.copy()
            self.current_result['timestamp'] = datetime.now()
            self.current_result['engine'] = recognition_engine
            
            # Salvar automaticamente no banco
            try:
                voice_id = history_db.save_voice_recognition(
                    text_recognized=result['text'],
                    ingredients_extracted=result['ingredients'],
                    confidence_level=result['confidence'],
                    processing_time=result['processing_time'],
                    recognition_engine=recognition_engine,
                    was_manual_input=False,
                    session_id=self.session_id
                )
                self.update_history()  # Atualizar exibição
            except Exception as e:
                print(f"Erro ao salvar no banco: {e}")
            
        except sr.WaitTimeoutError:
            self.status_label.config(text="⏰ Timeout - Nenhum áudio detectado")
            messagebox.showwarning("Timeout", "Não detectei nenhuma fala. Tente novamente.")
            
        except sr.UnknownValueError:
            self.status_label.config(text="❓ Não consegui entender a fala")
            messagebox.showwarning("Não compreendido", 
                                 "Não consegui entender o que foi dito.\nTente falar mais claramente.")
            
        except sr.RequestError as e:
            self.status_label.config(text="🌐 Erro de conexão com serviço de reconhecimento")
            messagebox.showerror("Erro de Rede", 
                               f"Erro ao conectar com serviço de reconhecimento:\n{e}")
            
        except Exception as e:
            self.status_label.config(text="❌ Erro no reconhecimento de voz")
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
            
        finally:
            # Re-habilitar botão
            self.record_btn.config(state='normal')
    
    def simulate_recognition(self):
        """Simula reconhecimento de voz para demonstração (fallback)"""
        examples = [
            {
                'text': 'Tenho tomate, cebola, alho e azeite na cozinha',
                'ingredients': 'Tomate, Cebola, Alho, Azeite',
                'confidence': 0.92,
                'processing_time': 1.8
            },
            {
                'text': 'Quero fazer algo com frango, batata e cenoura',
                'ingredients': 'Frango, Batata, Cenoura',
                'confidence': 0.87,
                'processing_time': 2.1
            },
            {
                'text': 'Ingredientes disponíveis ovos leite farinha açúcar',
                'ingredients': 'Ovos, Leite, Farinha, Açúcar',
                'confidence': 0.95,
                'processing_time': 1.5
            }
        ]
        
        import random
        example = random.choice(examples)
        
        # Simular processamento
        self.status_label.config(text="🎭 Simulando gravação...")
        self.record_btn.config(state='disabled')
        self.root.update()
        
        time.sleep(1)
        
        self.status_label.config(text="🎭 Simulando processamento...")
        self.root.update()
        
        time.sleep(example['processing_time'])
        
        # Mostrar resultados
        self.show_results(example)
        
        self.status_label.config(text="✅ Simulação concluída (modo demonstração)")
        self.record_btn.config(state='normal')
        
        # Salvar resultado atual
        self.current_result = example.copy()
        self.current_result['timestamp'] = datetime.now()
        self.current_result['engine'] = 'simulation'
        
        # Salvar automaticamente no banco
        try:
            voice_id = history_db.save_voice_recognition(
                text_recognized=example['text'],
                ingredients_extracted=example['ingredients'],
                confidence_level=example['confidence'],
                processing_time=example['processing_time'],
                recognition_engine='simulation',
                was_manual_input=False,
                session_id=self.session_id
            )
            self.update_history()  # Atualizar exibição
        except Exception as e:
            print(f"Erro ao salvar simulação no banco: {e}")
    
    def manual_input(self):
        """Permite entrada manual de texto"""
        dialog = tk.Toplevel(self.root)
        dialog.title("✍️ Entrada Manual")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        ttk.Label(dialog, text="Digite o texto dos ingredientes:").pack(pady=10)
        
        text_input = tk.Text(dialog, height=8, font=('Consolas', 11))
        text_input.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def process_manual_input():
            text = text_input.get(1.0, tk.END).strip()
            if text:
                result = {
                    'text': text,
                    'ingredients': self.extract_ingredients(text),
                    'confidence': 1.0,  # Manual = 100% confiança
                    'processing_time': 0.0
                }
                
                self.show_results(result)
                self.current_result = result.copy()
                self.current_result['timestamp'] = datetime.now()
                self.current_result['engine'] = 'manual'
                
                # Salvar automaticamente no banco
                try:
                    voice_id = history_db.save_voice_recognition(
                        text_recognized=result['text'],
                        ingredients_extracted=result['ingredients'],
                        confidence_level=result['confidence'],
                        processing_time=result['processing_time'],
                        recognition_engine='manual',
                        was_manual_input=True,
                        session_id=self.session_id
                    )
                    self.update_history()  # Atualizar exibição
                except Exception as e:
                    print(f"Erro ao salvar entrada manual no banco: {e}")
                
                dialog.destroy()
            else:
                messagebox.showwarning("Aviso", "Digite algum texto!")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="✅ Processar", command=process_manual_input).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        text_input.focus_set()
    
    def show_results(self, result: Dict):
        """Mostra resultados na interface"""
        # Limpar campos
        self.original_text.delete(1.0, tk.END)
        self.ingredients_text.delete(1.0, tk.END)
        self.analysis_text.delete(1.0, tk.END)
        
        # Preencher com novos dados
        self.original_text.insert(tk.END, result['text'])
        self.ingredients_text.insert(tk.END, result['ingredients'])
        
        # Análise
        analysis = self.generate_analysis_from_record({
            'text': result['text'],
            'ingredients': result['ingredients'], 
            'confidence': result['confidence']
        })
        self.analysis_text.insert(tk.END, analysis)
        
        # Métricas
        confidence_percent = int(result['confidence'] * 100)
        self.accuracy_label.config(text=f"Acurácia: {confidence_percent}%")
        self.time_label.config(text=f"Tempo: {result['processing_time']:.1f}s")
        self.confidence_label.config(text=f"Confiança: {confidence_percent}%")
    
    def extract_ingredients(self, text: str) -> str:
        """Extrai ingredientes do texto"""
        known_ingredients = [
            'tomate', 'cebola', 'alho', 'ovo', 'ovos', 'frango', 'carne', 'peixe',
            'batata', 'cenoura', 'brócolis', 'arroz', 'feijão', 'macarrão',
            'queijo', 'leite', 'manteiga', 'azeite', 'sal', 'pimenta',
            'açúcar', 'farinha', 'óleo', 'vinagre', 'limão', 'banana',
            'maçã', 'pera', 'uva', 'laranja', 'abacaxi', 'melancia',
            'alface', 'pepino', 'pimentão', 'berinjela', 'linguiça',
            'bacon', 'presunto', 'mussarela', 'ricota'
        ]
        
        text_lower = text.lower()
        found_ingredients = []
        
        for ingredient in known_ingredients:
            if ingredient in text_lower:
                found_ingredients.append(ingredient.title())
        
        # Remover duplicatas
        unique_ingredients = []
        for ing in found_ingredients:
            if ing not in unique_ingredients:
                unique_ingredients.append(ing)
        
        return ', '.join(unique_ingredients) if unique_ingredients else 'Nenhum ingrediente conhecido identificado'
    
    def generate_analysis_from_record(self, record: Dict) -> str:
        """Gera análise a partir de um registro do banco"""
        text = record['text']
        ingredients = record['ingredients']
        confidence = record['confidence']
        
        analysis = f"""Palavras detectadas: {len(text.split())}
Ingredientes encontrados: {len(ingredients.split(', ')) if ingredients and ingredients != 'Nenhum ingrediente conhecido identificado' else 0}
Nível de confiança: {confidence * 100:.1f}%
Qualidade: {'Excelente' if confidence > 0.9 else 'Boa' if confidence > 0.7 else 'Regular'}

Sugestão: {'Buscar receitas imediatamente' if confidence > 0.8 else 'Verificar ingredientes identificados'}"""
        
        return analysis
        """Gera análise do reconhecimento"""
        text = result['text']
        ingredients = result['ingredients']
        confidence = result['confidence']
        
        analysis = f"""Palavras detectadas: {len(text.split())}
Ingredientes encontrados: {len(ingredients.split(', ')) if ingredients != 'Nenhum ingrediente conhecido identificado' else 0}
Nível de confiança: {confidence * 100:.1f}%
Qualidade: {'Excelente' if confidence > 0.9 else 'Boa' if confidence > 0.7 else 'Regular'}

Sugestão: {'Buscar receitas imediatamente' if confidence > 0.8 else 'Verificar ingredientes identificados'}"""
        
        return analysis
    
    def save_result(self):
        """Salva resultado atual no banco de dados"""
        if self.current_result:
            try:
                # Determinar se foi entrada manual
                was_manual = self.current_result.get('engine') == 'manual'
                
                # Salvar no banco de dados
                voice_id = history_db.save_voice_recognition(
                    text_recognized=self.current_result['text'],
                    ingredients_extracted=self.current_result['ingredients'],
                    confidence_level=self.current_result['confidence'],
                    processing_time=self.current_result['processing_time'],
                    recognition_engine=self.current_result.get('engine', 'google'),
                    was_manual_input=was_manual,
                    session_id=self.session_id
                )
                
                self.update_history()
                messagebox.showinfo("Sucesso", f"Resultado salvo no banco de dados (ID: {voice_id})!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")
        else:
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar!")
    
    def search_recipes(self):
        """Simula busca de receitas"""
        if self.current_result:
            ingredients = self.current_result['ingredients']
            messagebox.showinfo("Busca de Receitas", 
                              f"Buscando receitas para: {ingredients}\n\n" +
                              "Esta funcionalidade seria integrada com o sistema principal do Chef RAG.")
        else:
            messagebox.showwarning("Aviso", "Nenhum ingrediente para buscar!")
    
    def clear_results(self):
        """Limpa resultados"""
        self.original_text.delete(1.0, tk.END)
        self.ingredients_text.delete(1.0, tk.END)
        self.analysis_text.delete(1.0, tk.END)
        
        self.accuracy_label.config(text="Acurácia: --")
        self.time_label.config(text="Tempo: --")
        self.confidence_label.config(text="Confiança: --")
        
        self.current_result = None
        self.status_label.config(text="Pronto para reconhecimento de voz")
    
    def update_history(self):
        """Atualiza exibição do histórico do banco de dados"""
        try:
            # Limpar treeview
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Buscar histórico do banco
            history_records = history_db.get_voice_recognition_history(limit=50)
            
            # Adicionar itens
            for i, record in enumerate(history_records):
                # Parse do timestamp
                try:
                    timestamp_obj = datetime.fromisoformat(record['timestamp'])
                    timestamp_str = timestamp_obj.strftime('%d/%m/%Y %H:%M')
                except:
                    timestamp_str = record['timestamp'][:16]  # Fallback
                
                text_preview = record['text'][:30] + '...' if len(record['text']) > 30 else record['text']
                ingredients_preview = record['ingredients'][:30] + '...' if len(record['ingredients']) > 30 else record['ingredients']
                confidence = f"{int(record['confidence'] * 100)}%" if record['confidence'] else "N/A"
                
                # Adicionar ícone para entrada manual
                if record['manual']:
                    text_preview = "✍️ " + text_preview
                else:
                    text_preview = "🎤 " + text_preview
                
                self.history_tree.insert('', 'end', values=(
                    timestamp_str, text_preview, ingredients_preview, confidence
                ), tags=(str(i),))
            
            # Atualizar status
            total_records = len(history_records)
            stats = history_db.get_voice_recognition_stats()
            
            self.status_label.config(
                text=f"✨ Histórico carregado: {total_records} registros (Total: {stats['total_recognitions']})"
            )
            
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar histórico do banco: {e}")
    
    def show_details(self, event):
        """Mostra detalhes do item selecionado do banco de dados"""
        selection = self.history_tree.selection()
        if selection:
            try:
                item_id = selection[0]
                item_index = int(self.history_tree.item(item_id, 'tags')[0])
                
                # Buscar histórico novamente para garantir sincronização
                history_records = history_db.get_voice_recognition_history(limit=50)
                
                if 0 <= item_index < len(history_records):
                    record = history_records[item_index]
                    
                    # Parse do timestamp
                    try:
                        timestamp_obj = datetime.fromisoformat(record['timestamp'])
                        timestamp_str = timestamp_obj.strftime('%d/%m/%Y às %H:%M:%S')
                    except:
                        timestamp_str = record['timestamp']
                    
                    # Tipo de entrada
                    input_type = "✍️ Entrada Manual" if record['manual'] else f"🎤 {record['engine'].title()}"
                    
                    details = f"""Data/Hora: {timestamp_str}
Tipo: {input_type}
Sessão: {record['session_id'][:8]}...
ID do Banco: {record['id']}

Texto Original: {record['text']}
Ingredientes: {record['ingredients']}
Confiança: {record['confidence'] * 100:.1f}%
Tempo de Processamento: {record['processing_time']:.1f}s

Análise:
{self.generate_analysis_from_record(record)}"""
                    
                    self.details_text.delete(1.0, tk.END)
                    self.details_text.insert(tk.END, details)
                    
            except Exception as e:
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, f"Erro ao carregar detalhes: {e}")
    
    def export_history(self):
        """Exporta histórico do banco de dados para arquivo"""
        try:
            history_records = history_db.get_voice_recognition_history(limit=1000)
            
            if not history_records:
                messagebox.showwarning("Aviso", "Histórico vazio!")
                return
            
            filename = filedialog.asksaveasfilename(
                title="Exportar Histórico",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                try:
                    export_data = {
                        'exported_at': datetime.now().isoformat(),
                        'total_records': len(history_records),
                        'session_id': self.session_id,
                        'statistics': history_db.get_voice_recognition_stats(),
                        'records': history_records
                    }
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(export_data, f, ensure_ascii=False, indent=2)
                    
                    messagebox.showinfo("Sucesso", f"Histórico exportado para {filename}")
                    
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao exportar: {e}")
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar histórico: {e}")
    
    def clear_history(self):
        """Limpa histórico do banco de dados"""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todo o histórico do banco de dados?"):
            try:
                deleted_count = history_db.delete_voice_recognition_history()
                self.update_history()
                self.details_text.delete(1.0, tk.END)
                messagebox.showinfo("Sucesso", f"Histórico limpo! {deleted_count} registros removidos.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar histórico: {e}")
    
    def load_text_file(self):
        """Carrega arquivo de texto para análise"""
        filename = filedialog.askopenfilename(
            title="Selecionar Arquivo de Texto",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.analysis_input.delete(1.0, tk.END)
                self.analysis_input.insert(tk.END, content)
                
                messagebox.showinfo("Sucesso", f"Arquivo carregado: {filename}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}")
    
    def analyze_text(self):
        """Analisa texto inserido"""
        text = self.analysis_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Aviso", "Insira texto para análise!")
            return
        
        # Extrair ingredientes
        ingredients = self.extract_ingredients(text)
        
        # Estatísticas
        words = len(text.split())
        chars = len(text)
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        # Análise
        analysis_result = f"""📊 ANÁLISE COMPLETA DO TEXTO
{'='*50}

📝 ESTATÍSTICAS:
• Total de palavras: {words}
• Total de caracteres: {chars}
• Sentenças aproximadas: {sentences}
• Tamanho médio das palavras: {chars/words:.1f} caracteres

🥬 INGREDIENTES ENCONTRADOS:
{ingredients}

📈 ANÁLISE DETALHADA:
• Densidade de ingredientes: {len(ingredients.split(', '))/words*100 if ingredients != 'Nenhum ingrediente conhecido identificado' else 0:.1f}% das palavras
• Tipo de texto: {'Receita/Ingredientes' if 'Tenho' in text or 'ingredientes' in text.lower() else 'Texto geral'}
• Complexidade: {'Simples' if words < 20 else 'Média' if words < 50 else 'Complexa'}

💡 RECOMENDAÇÕES:
{self.get_recommendations(text, ingredients)}"""
        
        self.analysis_output.delete(1.0, tk.END)
        self.analysis_output.insert(tk.END, analysis_result)
    
    def get_recommendations(self, text: str, ingredients: str) -> str:
        """Gera recomendações baseadas na análise"""
        if ingredients == 'Nenhum ingrediente conhecido identificado':
            return "• Tente usar nomes mais específicos de ingredientes\n• Verifique a ortografia\n• Use termos em português"
        
        ingredient_count = len(ingredients.split(', '))
        
        if ingredient_count == 1:
            return "• Adicione mais ingredientes para receitas completas\n• Considere complementos como temperos\n• Pense em proteínas ou carboidratos"
        elif ingredient_count <= 3:
            return "• Bom número de ingredientes para receitas simples\n• Considere adicionar temperos\n• Verifique se tem todos os básicos"
        else:
            return "• Excelente variedade de ingredientes\n• Ideal para receitas elaboradas\n• Considere organizar por categoria"
    
    def compare_with_last(self):
        """Compara análise atual com último reconhecimento"""
        text = self.analysis_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Aviso", "Insira texto para comparação!")
            return
        
        if not self.current_result:
            messagebox.showwarning("Aviso", "Faça um reconhecimento primeiro!")
            return
        
        # Análise do texto atual
        current_ingredients = self.extract_ingredients(text)
        last_ingredients = self.current_result['ingredients']
        
        # Comparação
        current_set = set(current_ingredients.lower().split(', '))
        last_set = set(last_ingredients.lower().split(', '))
        
        intersection = current_set.intersection(last_set)
        union = current_set.union(last_set)
        
        similarity = len(intersection) / len(union) if union else 0
        
        comparison_result = f"""⚖️ COMPARAÇÃO DETALHADA
{'='*40}

📄 TEXTO ATUAL:
• Ingredientes: {current_ingredients}

🎤 ÚLTIMO RECONHECIMENTO:
• Ingredientes: {last_ingredients}
• Data: {self.current_result['timestamp'].strftime('%d/%m/%Y %H:%M')}

📊 ANÁLISE:
• Em comum: {', '.join(intersection) if intersection else 'Nenhum'}
• Apenas no texto: {', '.join(current_set - last_set) if current_set - last_set else 'Nenhum'}
• Apenas no reconhecimento: {', '.join(last_set - current_set) if last_set - current_set else 'Nenhum'}
• Similaridade: {similarity:.1%}

🎯 CONCLUSÃO:
{self.get_similarity_conclusion(similarity)}"""
        
        # Mostrar em dialog
        self.show_comparison_dialog(comparison_result)
    
    def get_similarity_conclusion(self, similarity: float) -> str:
        """Gera conclusão baseada na similaridade"""
        if similarity > 0.8:
            return "🎉 Alta compatibilidade! Os ingredientes são muito similares."
        elif similarity > 0.5:
            return "✅ Boa compatibilidade. Há sobreposição significativa."
        elif similarity > 0.2:
            return "⚠️ Compatibilidade moderada. Alguns ingredientes em comum."
        else:
            return "❌ Baixa compatibilidade. Ingredientes muito diferentes."
    
    def show_comparison_dialog(self, comparison_text: str):
        """Mostra resultado da comparação em dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚖️ Resultado da Comparação")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centralizar
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 100, self.root.winfo_rooty() + 50))
        
        # Texto da comparação
        text_widget = tk.Text(dialog, font=('Consolas', 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget.insert(tk.END, comparison_text)
        text_widget.config(state=tk.DISABLED)
        
        # Botão fechar
        ttk.Button(dialog, text="✅ Fechar", command=dialog.destroy).pack(pady=10)
    
    def run(self):
        """Executa a interface"""
        try:
            # Carregar histórico inicial do banco
            self.update_history()
            
            # Buscar estatísticas
            stats = history_db.get_voice_recognition_stats()
            
            # Mensagem de boas-vindas com estatísticas
            welcome_msg = f"✨ Interface carregada! Total de reconhecimentos: {stats['total_recognitions']}"
            if stats['total_recognitions'] > 0:
                welcome_msg += f" (Confiança média: {stats['avg_confidence']:.1%})"
            
            self.status_label.config(text=welcome_msg)
            
        except Exception as e:
            print(f"Erro ao carregar dados iniciais: {e}")
            self.status_label.config(text="✨ Interface carregada! Use 'Reconhecimento de Voz' ou 'Entrada Manual'")
        
        # Iniciar loop principal
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        print("🚀 Iniciando Interface de Voz Simplificada...")
        app = SimpleVoiceInterface()
        app.run()
    except Exception as e:
        print(f"Erro ao iniciar: {e}")
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()