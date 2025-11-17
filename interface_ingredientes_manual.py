#!/usr/bin/env python3
"""
Interface para Digitação Manual de Ingredientes - Chef RAG v2
============================================================

Interface simples e limpa para entrada manual de ingredientes.
Suporte para busca conjunta com vírgulas.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from datetime import datetime
import uuid

# Importação do banco de dados
from core_logic.database import history_db

class ManualIngredientsInterface:
    """Interface para entrada manual de ingredientes"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.current_result = None
        self.session_id = str(uuid.uuid4())
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("✍️ Chef RAG v2 - Entrada Manual")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#4CAF50', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="✍️ Entrada Manual - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#4CAF50', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instruções
        instructions_label = tk.Label(main_frame, 
                                    text="📝 Digite os ingredientes que você tem:", 
                                    font=('Arial', 12, 'bold'), 
                                    bg='white', 
                                    fg='#333')
        instructions_label.pack(pady=(0, 5))
        
        tip_label = tk.Label(main_frame, 
                           text="💡 Dica: Use vírgulas para buscar receitas que usem esses ingredientes JUNTOS\n" +
                                "Exemplo: 'chocolate, leite, açúcar' → receitas que usam os 3 ingredientes", 
                           font=('Arial', 9), 
                           bg='white', 
                           fg='#666')
        tip_label.pack(pady=(0, 15))
        
        # Campo de entrada
        entry_frame = tk.Frame(main_frame, bg='white')
        entry_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.ingredients_entry = tk.Entry(entry_frame, 
                                        font=('Arial', 12), 
                                        bg='#f5f5f5', 
                                        relief=tk.FLAT, 
                                        bd=10)
        self.ingredients_entry.pack(fill=tk.X, pady=5, ipady=8)
        self.ingredients_entry.bind('<Return>', self.search_recipes)
        self.ingredients_entry.focus()
        
        # Botão de busca
        search_button = tk.Button(entry_frame, 
                                text="🔍 Buscar Receitas", 
                                font=('Arial', 12, 'bold'), 
                                bg='#4CAF50', 
                                fg='white', 
                                relief=tk.FLAT, 
                                padx=20, 
                                pady=10,
                                command=self.search_recipes)
        search_button.pack(pady=10)
        
        # Status
        self.status_label = tk.Label(main_frame, 
                                   text="⚪ Digite ingredientes e pressione Enter ou clique em Buscar", 
                                   font=('Arial', 10), 
                                   bg='white', 
                                   fg='#666')
        self.status_label.pack(pady=(0, 10))
        
        # Área de resultado
        result_frame = tk.Frame(main_frame, bg='white')
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        result_label = tk.Label(result_frame, 
                              text="📋 Resultado da Busca:", 
                              font=('Arial', 12, 'bold'), 
                              bg='white', 
                              fg='#333')
        result_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(result_frame, 
                                                   wrap=tk.WORD, 
                                                   height=20, 
                                                   font=('Consolas', 10), 
                                                   bg='#f8f8f8', 
                                                   relief=tk.FLAT, 
                                                   bd=10)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        action_frame = tk.Frame(main_frame, bg='white')
        action_frame.pack(fill=tk.X, pady=15)
        
        copy_button = tk.Button(action_frame, 
                              text="📋 Copiar Resultado", 
                              font=('Arial', 10), 
                              bg='#2196F3', 
                              fg='white', 
                              relief=tk.FLAT, 
                              padx=15, 
                              pady=5,
                              command=self.copy_result)
        copy_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cook_button = tk.Button(action_frame, 
                              text="👨‍🍳 Ir para Cozinha", 
                              font=('Arial', 10), 
                              bg='#FF9800', 
                              fg='white', 
                              relief=tk.FLAT, 
                              padx=15, 
                              pady=5,
                              command=self.open_kitchen)
        cook_button.pack(side=tk.LEFT)
        
    def search_recipes(self, event=None):
        """Busca receitas pelos ingredientes digitados"""
        ingredients = self.ingredients_entry.get().strip()
        
        if not ingredients:
            messagebox.showwarning("Atenção", "Digite pelo menos um ingrediente!")
            return
        
        # Atualiza status
        self.update_status("🔄 Buscando receitas...", '#FF9800')
        self.result_text.delete(1.0, tk.END)
        
        # Inicia busca em thread separada
        threading.Thread(target=self.process_ingredients, args=(ingredients,), daemon=True).start()
        
    def process_ingredients(self, ingredients):
        """Processa os ingredientes e busca receitas"""
        try:
            from core_logic.sistema_rag import find_recipes_by_ingredient
            
            self.root.after(0, lambda: self.update_status("🔍 Analisando ingredientes...", '#FF9800'))
            
            # Determina tipo de busca baseado em vírgulas
            if ',' in ingredients:
                search_type = "CONJUNTA (receitas que usam esses ingredientes juntos)"
                ingredients_list = [ing.strip() for ing in ingredients.split(',')]
                ingredients_display = f"{len(ingredients_list)} ingredientes: {', '.join(ingredients_list)}"
            else:
                search_type = "INDIVIDUAL"
                ingredients_display = ingredients
            
            # Busca receitas
            recipes = find_recipes_by_ingredient(ingredients, None, "manual_entry")
            
            # Formata resultado
            resultado = f"🔍 BUSCA: {search_type}\n"
            resultado += f"📝 INGREDIENTES: {ingredients_display}\n"
            resultado += f"⏰ HORÁRIO: {datetime.now().strftime('%H:%M:%S')}\n"
            resultado += "="*60 + "\n\n"
            resultado += recipes
            
            # Atualiza interface
            self.current_result = resultado
            self.root.after(0, lambda: self.display_result(resultado))
            
            # Salvar no histórico
            history_db.add_analysis(
                ingredient=ingredients,
                recipes_response=recipes[:500] + "..." if len(recipes) > 500 else recipes,
                image_path=None,
                source_mode="manual_entry"
            )
            
        except Exception as e:
            error_msg = f"❌ Erro ao buscar receitas: {e}"
            self.root.after(0, lambda: self.display_result(error_msg))
            self.root.after(0, lambda: self.update_status("❌ Erro na busca", '#f44336'))
            
    def display_result(self, result):
        """Exibe o resultado na área de texto"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result)
        self.update_status("✅ Busca concluída!", '#4CAF50')
        
    def update_status(self, message, color='#666'):
        """Atualiza o status da interface"""
        self.status_label.config(text=message, fg=color)
        
    def copy_result(self):
        """Copia o resultado para a área de transferência"""
        if self.current_result:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_result)
            self.update_status("📋 Resultado copiado!", '#4CAF50')
        else:
            messagebox.showinfo("Informação", "Nenhum resultado para copiar!")
            
    def open_kitchen(self):
        """Abre a interface de cozinha passo a passo"""
        try:
            import subprocess
            subprocess.Popen(["python", "interface_cozinha_passo_passo.py"])
            self.update_status("👨‍🍳 Interface de cozinha aberta!", '#4CAF50')
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a cozinha: {e}")
            
    def run(self):
        """Executa a interface"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

def main():
    """Função principal"""
    app = ManualIngredientsInterface()
    app.run()

if __name__ == "__main__":
    main()