#!/usr/bin/env python3
"""
Interface de Voz Simplificada - Chef RAG v2
Versão que funciona apenas com tkinter (incluído no Python)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
from datetime import datetime
import json
import os
from typing import Optional, Dict, List

class SimpleVoiceInterface:
    """Interface simplificada para reconhecimento de voz e análise de ingredientes"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.recognition_history = self.load_history()
        self.current_result = None
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("🎤 Chef RAG - Interface de Voz")
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
        
        title_label = tk.Label(header_frame, text="🎤 Interface de Voz Avançada", 
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
        
        self.record_btn = ttk.Button(btn_frame, text="🎤 Simular Reconhecimento", 
                                   command=self.simulate_recognition)
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
    
    def simulate_recognition(self):
        """Simula reconhecimento de voz para demonstração"""
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
        self.status_label.config(text="🎤 Gravando...")
        self.record_btn.config(state='disabled')
        self.root.update()
        
        time.sleep(1)
        
        self.status_label.config(text="🧠 Processando...")
        self.root.update()
        
        time.sleep(example['processing_time'])
        
        # Mostrar resultados
        self.show_results(example)
        
        self.status_label.config(text="✅ Reconhecimento concluído")
        self.record_btn.config(state='normal')
        
        # Salvar resultado atual
        self.current_result = example.copy()
        self.current_result['timestamp'] = datetime.now()
    
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
        analysis = self.generate_analysis(result)
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
    
    def generate_analysis(self, result: Dict) -> str:
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
        """Salva resultado atual no histórico"""
        if self.current_result:
            self.recognition_history.append(self.current_result)
            self.save_history()
            self.update_history()
            messagebox.showinfo("Sucesso", "Resultado salvo no histórico!")
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
    
    def load_history(self) -> List[Dict]:
        """Carrega histórico do arquivo"""
        history_file = 'simple_voice_history.json'
        
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Converter timestamps
                for item in data:
                    if isinstance(item['timestamp'], str):
                        item['timestamp'] = datetime.fromisoformat(item['timestamp'])
                    
                return data
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
        
        return []
    
    def save_history(self):
        """Salva histórico no arquivo"""
        history_file = 'simple_voice_history.json'
        
        try:
            serializable_data = []
            for item in self.recognition_history:
                serializable_item = item.copy()
                serializable_item['timestamp'] = item['timestamp'].isoformat()
                serializable_data.append(serializable_item)
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def update_history(self):
        """Atualiza exibição do histórico"""
        # Limpar treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Adicionar itens (últimos primeiro)
        for result in reversed(self.recognition_history[-50:]):
            timestamp = result['timestamp'].strftime('%d/%m/%Y %H:%M')
            text_preview = result['text'][:30] + '...' if len(result['text']) > 30 else result['text']
            ingredients_preview = result['ingredients'][:30] + '...' if len(result['ingredients']) > 30 else result['ingredients']
            confidence = f"{int(result['confidence'] * 100)}%"
            
            self.history_tree.insert('', 0, values=(
                timestamp, text_preview, ingredients_preview, confidence
            ))
    
    def show_details(self, event):
        """Mostra detalhes do item selecionado"""
        selection = self.history_tree.selection()
        if selection:
            item_id = selection[0]
            item_index = self.history_tree.index(item_id)
            
            # Converter índice (lista reversa)
            actual_index = len(self.recognition_history) - 1 - item_index
            
            if 0 <= actual_index < len(self.recognition_history):
                result = self.recognition_history[actual_index]
                
                details = f"""Data/Hora: {result['timestamp'].strftime('%d/%m/%Y às %H:%M:%S')}
Texto Original: {result['text']}
Ingredientes: {result['ingredients']}
Confiança: {result['confidence'] * 100:.1f}%
Tempo de Processamento: {result['processing_time']:.1f}s

Análise:
{self.generate_analysis(result)}"""
                
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, details)
    
    def export_history(self):
        """Exporta histórico para arquivo"""
        if not self.recognition_history:
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
                    'total_records': len(self.recognition_history),
                    'records': []
                }
                
                for item in self.recognition_history:
                    export_item = item.copy()
                    export_item['timestamp'] = item['timestamp'].isoformat()
                    export_data['records'].append(export_item)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Sucesso", f"Histórico exportado para {filename}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {e}")
    
    def clear_history(self):
        """Limpa histórico"""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todo o histórico?"):
            self.recognition_history.clear()
            self.save_history()
            self.update_history()
            self.details_text.delete(1.0, tk.END)
            messagebox.showinfo("Sucesso", "Histórico limpo!")
    
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
        # Carregar histórico inicial
        self.update_history()
        
        # Mensagem de boas-vindas
        self.status_label.config(text="✨ Interface carregada! Use 'Simular Reconhecimento' ou 'Entrada Manual'")
        
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