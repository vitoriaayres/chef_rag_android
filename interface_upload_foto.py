#!/usr/bin/env python3
"""
Interface de Upload de Fotos - Chef RAG v2
==========================================

Interface gráfica para análise de fotos de ingredientes usando IA.
Design limpo e simples com histórico integrado.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
from datetime import datetime
import uuid

# Importação do banco de dados
from core_logic.database import history_db

class PhotoAnalysisInterface:
    """Interface para análise de fotos de ingredientes"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.current_result = None
        self.session_id = str(uuid.uuid4())
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("📸 Chef RAG v2 - Análise de Fotos")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#FF9800', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="📸 Análise de Fotos - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#FF9800', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_main_tab()
        self.setup_history_tab()
        
    def setup_main_tab(self):
        """Configura aba principal"""
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="📸 Upload")
        
        # Frame de upload
        upload_frame = ttk.LabelFrame(self.main_frame, text="📁 Selecionar Foto", padding=15)
        upload_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Instruções
        instructions = tk.Label(upload_frame, 
                               text="Selecione uma foto dos seus ingredientes para análise com IA",
                               font=('Arial', 11),
                               wraplength=400,
                               justify='center')
        instructions.pack(pady=(0, 15))
        
        # Botão de upload
        self.upload_btn = tk.Button(upload_frame,
                                   text="📁 Escolher Foto",
                                   command=self.select_photo,
                                   bg='#4CAF50',
                                   fg='white',
                                   font=('Arial', 12, 'bold'),
                                   padx=20,
                                   pady=10,
                                   relief='flat')
        self.upload_btn.pack(pady=10)
        
        # Status
        status_frame = ttk.LabelFrame(self.main_frame, text="📊 Status", padding=15)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, 
                                    text="🔵 Pronto para upload",
                                    font=('Arial', 11),
                                    fg='#2196F3')
        self.status_label.pack()
        
        # Resultados
        results_frame = ttk.LabelFrame(self.main_frame, text="📋 Resultados", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     height=15,
                                                     font=('Arial', 10),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_history_tab(self):
        """Configura aba de histórico"""
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📊 Histórico")
        
        # Controles
        controls_frame = ttk.LabelFrame(self.history_frame, text="🔧 Controles", padding=10)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        refresh_btn = tk.Button(controls_frame,
                               text="🔄 Atualizar",
                               command=self.load_history,
                               bg='#2196F3',
                               fg='white',
                               font=('Arial', 10, 'bold'),
                               relief='flat',
                               padx=15,
                               pady=5)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de histórico
        history_list_frame = ttk.LabelFrame(self.history_frame, text="📜 Análises Anteriores", padding=10)
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ('data', 'arquivo', 'ingredientes')
        self.history_tree = ttk.Treeview(history_list_frame, columns=columns, show='tree headings')
        
        self.history_tree.heading('#0', text='ID')
        self.history_tree.heading('data', text='Data/Hora')
        self.history_tree.heading('arquivo', text='Arquivo')
        self.history_tree.heading('ingredientes', text='Ingredientes')
        
        self.history_tree.column('#0', width=50)
        self.history_tree.column('data', width=150)
        self.history_tree.column('arquivo', width=200)
        self.history_tree.column('ingredientes', width=300)
        
        tree_scroll = ttk.Scrollbar(history_list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_history()
        
    def select_photo(self):
        """Seleciona e processa uma foto"""
        file_path = filedialog.askopenfilename(
            title="Selecione uma foto dos ingredientes",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            self.update_status("🔄 Analisando foto...", '#FF9800')
            threading.Thread(target=self.process_photo, args=(file_path,), daemon=True).start()
        else:
            self.update_status("🔵 Seleção cancelada", '#2196F3')
            
    def process_photo(self, file_path):
        """Processa a foto selecionada"""
        try:
            from core_logic.sistema_rag import extract_ingredients_from_image, find_recipes_by_ingredient
            
            self.root.after(0, lambda: self.update_status("🤖 Identificando ingredientes...", '#FF9800'))
            
            ingredientes = extract_ingredients_from_image(file_path)
            
            if "Erro" not in ingredientes:
                # Buscar receitas primeiro (em background)
                receitas = find_recipes_by_ingredient(ingredientes, file_path, "upload")
                
                # Mostrar animação de sucesso e depois fechar
                self.root.after(0, lambda: self.mostrar_animacao_sucesso(ingredientes, file_path, receitas))
                
            else:
                error_msg = f"❌ Erro ao analisar imagem: {ingredientes}"
                self.root.after(0, lambda: self.show_results(error_msg))
                self.root.after(0, lambda: self.update_status("❌ Erro na análise", '#F44336'))
                self.root.after(0, lambda: self.update_status("❌ Erro na análise", '#F44336'))
                
        except Exception as e:
            error_msg = f"❌ Erro inesperado: {str(e)}"
            self.root.after(0, lambda: self.show_results(error_msg))
            self.root.after(0, lambda: self.update_status("❌ Erro no processamento", '#F44336'))
            
    def show_results(self, text):
        """Mostra resultados na área de texto"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        self.results_text.config(state=tk.DISABLED)
        
    def mostrar_animacao_sucesso(self, ingredientes, file_path, receitas):
        """Mostra animação de sucesso e fecha a interface"""
        # Limpar interface
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar nova interface de sucesso
        self.root.configure(bg='#4CAF50')
        
        # Frame central
        center_frame = tk.Frame(self.root, bg='#4CAF50')
        center_frame.pack(expand=True, fill=tk.BOTH)
        
        # Ícone de sucesso grande
        success_icon = tk.Label(center_frame, 
                               text="✅", 
                               font=('Arial', 72), 
                               bg='#4CAF50', 
                               fg='white')
        success_icon.pack(pady=(100, 20))
        
        # Texto "OKAY!"
        okay_label = tk.Label(center_frame, 
                            text="OKAY!", 
                            font=('Arial', 32, 'bold'), 
                            bg='#4CAF50', 
                            fg='white')
        okay_label.pack(pady=10)
        
        # Ingredientes identificados
        ingredients_label = tk.Label(center_frame, 
                                    text=f"Ingredientes: {ingredientes}", 
                                    font=('Arial', 12), 
                                    bg='#4CAF50', 
                                    fg='white',
                                    wraplength=400)
        ingredients_label.pack(pady=10)
        
        # Status
        status_label = tk.Label(center_frame, 
                              text="📺 Receitas mostradas no terminal!", 
                              font=('Arial', 14, 'bold'), 
                              bg='#4CAF50', 
                              fg='white')
        status_label.pack(pady=20)
        
        # Mostrar receitas no terminal
        self.mostrar_receitas_no_terminal(ingredientes, file_path, receitas)
        
        # Fechar automaticamente após 2.5 segundos
        self.root.after(2500, self.fechar_interface)
    
    def mostrar_receitas_no_terminal(self, ingredientes, file_path, receitas):
        """Mostra receitas no terminal"""
        print(f"\n{'='*60}")
        print("📷 ANÁLISE DE IMAGEM CONCLUÍDA")
        print("="*60)
        print(f"📁 Arquivo: {os.path.basename(file_path)}")
        print(f"🥬 Ingredientes identificados: {ingredientes}")
        print(f"{'='*60}")
        
        if receitas:
            print("\n🍽️ RECEITAS SUGERIDAS:")
            print("="*60)
            print(receitas)
            print("="*60)
        else:
            print("\n❌ Nenhuma receita encontrada para estes ingredientes.")
        
        # Salvar no histórico
        try:
            from core_logic.database import HistoryDB
            history_db = HistoryDB()
            history_db.add_analysis(
                ingredient=ingredientes,
                recipes_response="Receitas mostradas no terminal" if receitas else "Nenhuma receita encontrada",
                image_path=file_path,
                source_mode="upload_photo"
            )
        except:
            pass  # Ignorar erros
    
    def fechar_interface(self):
        """Fecha a interface"""
        try:
            self.root.destroy()
        except:
            pass
        
    def update_status(self, message, color='#2196F3'):
        """Atualiza mensagem de status"""
        self.status_label.config(text=message, fg=color)
        
    def load_history(self):
        """Carrega histórico do banco de dados"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        try:
            history_data = history_db.get_recent_analyses(limit=50)
            
            for i, entry in enumerate(history_data, 1):
                try:
                    dt = datetime.fromisoformat(entry['timestamp'])
                    formatted_date = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    formatted_date = entry['timestamp']
                
                input_file = entry.get('input_file', 'N/A')
                if input_file != 'N/A' and os.path.exists(input_file):
                    filename = os.path.basename(input_file)
                else:
                    filename = 'N/A'
                
                ingredients = entry.get('ingredients', 'N/A')
                if len(ingredients) > 50:
                    ingredients = ingredients[:50] + '...'
                
                self.history_tree.insert('', tk.END, 
                                        text=str(i),
                                        values=(formatted_date, filename, ingredients))
                                        
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

if __name__ == "__main__":
    app = PhotoAnalysisInterface()
    app.run()