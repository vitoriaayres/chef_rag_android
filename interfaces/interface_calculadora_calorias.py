#!/usr/bin/env python3
"""
Interface de Calculadora de Calorias - Chef RAG v2
==================================================

Interface gráfica para calcular calorias de ingredientes.
Design limpo e simples com base de dados nutricional.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import re

# Importação do banco de dados
from core_logic.database import history_db

class CalorieCalculatorInterface:
    """Interface para cálculo de calorias """
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_calorie_database()
        self.setup_ui()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("⚖️ Chef RAG v2 - Calculadora de Calorias")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#FF5722', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="⚖️ Calculadora de Calorias - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#FF5722', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_calculator_tab()
        self.setup_database_tab()
        self.setup_history_tab()
        self.setup_credits_tab()
        
    def setup_calculator_tab(self):
        """Configura aba da calculadora"""
        self.calculator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calculator_frame, text="🧮 Calculadora")
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(self.calculator_frame, text="📝 Ingredientes", padding=15)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Campo de ingredientes
        tk.Label(input_frame, text="🥬 Digite os ingredientes (separados por vírgula):", 
                font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        tk.Label(input_frame, text="💡 Exemplo: 200g arroz, 150g frango, 1 tomate", 
                font=('Arial', 10), fg='#666666').pack(anchor='w', pady=(0, 10))
        
        self.ingredients_text = tk.Text(input_frame, height=5, font=('Arial', 11), width=70)
        self.ingredients_text.pack(fill=tk.X, pady=5)
        
        # Botões
        button_frame = tk.Frame(input_frame, bg='white')
        button_frame.pack(pady=10)
        
        calc_btn = tk.Button(button_frame,
                            text="🧮 Calcular Calorias",
                            command=self.calculate_calories,
                            bg='#4CAF50',
                            fg='white',
                            font=('Arial', 12, 'bold'),
                            relief='flat',
                            padx=30,
                            pady=10)
        calc_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame,
                             text="🧹 Limpar",
                             command=self.clear_input,
                             bg='#FF9800',
                             fg='white',
                             font=('Arial', 12, 'bold'),
                             relief='flat',
                             padx=30,
                             pady=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de resultados
        results_frame = ttk.LabelFrame(self.calculator_frame, text="📊 Análise Nutricional", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de resultados
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     height=15,
                                                     font=('Arial', 11),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status
        self.status_label = tk.Label(self.calculator_frame, 
                                    text="🔵 Digite ingredientes e suas quantidades",
                                    font=('Arial', 11),
                                    fg='#2196F3',
                                    bg='white')
        self.status_label.pack(pady=10)
        
    def setup_database_tab(self):
        """Configura aba da base de dados"""
        self.database_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.database_frame, text="📚 Base de Dados")
        
        # Frame de busca
        search_frame = ttk.LabelFrame(self.database_frame, text="🔍 Buscar Ingrediente", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        search_input_frame = tk.Frame(search_frame, bg='white')
        search_input_frame.pack(fill=tk.X)
        
        tk.Label(search_input_frame, text="Buscar:", font=('Arial', 11, 'bold'), bg='white').pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_input_frame, textvariable=self.search_var, font=('Arial', 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=10)
        
        search_btn = tk.Button(search_input_frame,
                              text="🔍 Buscar",
                              command=self.search_ingredient,
                              bg='#2196F3',
                              fg='white',
                              font=('Arial', 10, 'bold'),
                              relief='flat',
                              padx=15,
                              pady=5)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame da tabela
        table_frame = ttk.LabelFrame(self.database_frame, text="📋 Tabela Calórica (por 100g)", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ('ingrediente', 'calorias', 'proteinas', 'carboidratos', 'gorduras')
        self.ingredients_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        self.ingredients_tree.heading('ingrediente', text='Ingrediente')
        self.ingredients_tree.heading('calorias', text='Calorias (kcal)')
        self.ingredients_tree.heading('proteinas', text='Proteínas (g)')
        self.ingredients_tree.heading('carboidratos', text='Carboidratos (g)')
        self.ingredients_tree.heading('gorduras', text='Gorduras (g)')
        
        self.ingredients_tree.column('ingrediente', width=200)
        self.ingredients_tree.column('calorias', width=120)
        self.ingredients_tree.column('proteinas', width=120)
        self.ingredients_tree.column('carboidratos', width=120)
        self.ingredients_tree.column('gorduras', width=120)
        
        # Scrollbar
        tree_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.ingredients_tree.yview)
        self.ingredients_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.ingredients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Carregar dados iniciais
        self.load_ingredients_table()
        
    def setup_history_tab(self):
        """Configura aba de histórico"""
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📊 Histórico")
        
        # Controles
        controls_frame = ttk.LabelFrame(self.history_frame, text="🔧 Controles", padding=10)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        refresh_btn = tk.Button(controls_frame,
                               text="🔄 Atualizar",
                               command=self.load_calculation_history,
                               bg='#2196F3',
                               fg='white',
                               font=('Arial', 10, 'bold'),
                               relief='flat',
                               padx=15,
                               pady=5)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Histórico
        history_list_frame = ttk.LabelFrame(self.history_frame, text="📜 Cálculos Anteriores", padding=10)
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(history_list_frame,
                                                     height=20,
                                                     font=('Arial', 10),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        self.load_calculation_history()
        
    def setup_credits_tab(self):
        """Configura aba de créditos"""
        self.credits_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.credits_frame, text="🎆 Créditos")
        
        # Frame principal dos créditos
        main_credits_frame = tk.Frame(self.credits_frame, bg='white', padx=20, pady=20)
        main_credits_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(main_credits_frame, 
                              text="🧑‍🍳 Chef RAG - Créditos", 
                              font=('Arial', 20, 'bold'), 
                              fg='#FF5722', 
                              bg='white')
        title_label.pack(pady=(0, 20))
        
        # Separator
        separator = tk.Frame(main_credits_frame, height=2, bg='#FF5722')
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # Desenvolvido por
        dev_frame = tk.Frame(main_credits_frame, bg='white')
        dev_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(dev_frame, 
                text="📋 DESENVOLVIDO POR:", 
                font=('Arial', 14, 'bold'), 
                fg='#333', 
                bg='white').pack(anchor='w')
        
        tk.Label(dev_frame, 
                text="   • Vitória Ayres", 
                font=('Arial', 12), 
                fg='#666', 
                bg='white').pack(anchor='w', padx=(20, 0))
        
        # Tecnologias
        tech_frame = tk.Frame(main_credits_frame, bg='white')
        tech_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(tech_frame, 
                text="🛠️ TECNOLOGIAS ENVOLVIDAS:", 
                font=('Arial', 14, 'bold'), 
                fg='#333', 
                bg='white').pack(anchor='w')
        
        tecnologias = [
            "Python", "LangChain", "ChromaDB", "OpenCV", 
            "YOLO", "Tkinter", "SQLite", "Pandas", 
            "Speech Recognition", "Flask", "RAG"
        ]
        
        tech_row = None
        for i, tech in enumerate(tecnologias):
            if i % 2 == 0:  # Criar nova linha a cada 2 itens
                tech_row = tk.Frame(tech_frame, bg='white')
                tech_row.pack(fill=tk.X, padx=(20, 0))
            
            if tech_row:
                tk.Label(tech_row, 
                        text=f"• {tech}", 
                        font=('Arial', 11), 
                        fg='#666', 
                        bg='white').pack(side=tk.LEFT, padx=(0, 20))
        
        # Funcionalidades
        func_frame = tk.Frame(main_credits_frame, bg='white')
        func_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(func_frame, 
                text="🎯 FUNCIONALIDADES:", 
                font=('Arial', 14, 'bold'), 
                fg='#333', 
                bg='white').pack(anchor='w')
        
        funcionalidades = [
            "Reconhecimento de ingredientes por imagem",
            "Reconhecimento de voz",
            "Sistema de busca inteligente",
            "Filtros dietéticos",
            "Calculadora de calorias",
            "Verificador de alergias",
            "Cronômetros de cozinha",
            "Interface mobile"
        ]
        
        for func in funcionalidades:
            tk.Label(func_frame, 
                    text=f"   • {func}", 
                    font=('Arial', 11), 
                    fg='#666', 
                    bg='white').pack(anchor='w', padx=(20, 0))
        
        # Rodapé
        footer_frame = tk.Frame(main_credits_frame, bg='white')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(30, 0))
        
        separator2 = tk.Frame(footer_frame, height=1, bg='#DDD')
        separator2.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(footer_frame, 
                text="Chef RAG v2 - Sistema de Assistência Culinária Inteligente", 
                font=('Arial', 10, 'italic'), 
                fg='#999', 
                bg='white').pack()
        
    def setup_calorie_database(self):
        """Configura base de dados de calorias"""
        self.calorie_db = {
            'arroz': {'calorias': 130, 'proteinas': 2.7, 'carboidratos': 28, 'gorduras': 0.3},
            'feijao': {'calorias': 91, 'proteinas': 6.0, 'carboidratos': 16, 'gorduras': 0.5},
            'frango': {'calorias': 165, 'proteinas': 31, 'carboidratos': 0, 'gorduras': 3.6},
            'carne bovina': {'calorias': 250, 'proteinas': 26, 'carboidratos': 0, 'gorduras': 15},
            'ovo': {'calorias': 155, 'proteinas': 13, 'carboidratos': 1.1, 'gorduras': 11},
            'leite': {'calorias': 42, 'proteinas': 3.4, 'carboidratos': 5, 'gorduras': 1},
            'tomate': {'calorias': 18, 'proteinas': 0.9, 'carboidratos': 3.9, 'gorduras': 0.2},
            'cebola': {'calorias': 40, 'proteinas': 1.1, 'carboidratos': 9.3, 'gorduras': 0.1},
            'batata': {'calorias': 77, 'proteinas': 2, 'carboidratos': 17, 'gorduras': 0.1},
            'banana': {'calorias': 89, 'proteinas': 1.1, 'carboidratos': 23, 'gorduras': 0.3},
            'maça': {'calorias': 52, 'proteinas': 0.3, 'carboidratos': 14, 'gorduras': 0.2},
            'pao': {'calorias': 265, 'proteinas': 9, 'carboidratos': 49, 'gorduras': 3.2},
        }
        
    def calculate_calories(self):
        """Calcula calorias dos ingredientes informados"""
        ingredients_text = self.ingredients_text.get(1.0, tk.END).strip()
        
        if not ingredients_text:
            messagebox.showwarning("Aviso", "Digite os ingredientes!")
            return
            
        try:
            self.update_status("🧮 Calculando calorias...", '#FF9800')
            
            # Processar ingredientes
            ingredients_list = [ing.strip() for ing in ingredients_text.split(',') if ing.strip()]
            
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fat = 0
            
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            
            self.results_text.insert(tk.END, "🧮 ANÁLISE CALÓRICA DETALHADA\n")
            self.results_text.insert(tk.END, "="*50 + "\n\n")
            
            for ingredient in ingredients_list:
                calories, protein, carbs, fat, details_text = self.analyze_ingredient(ingredient)
                
                total_calories += calories
                total_protein += protein
                total_carbs += carbs
                total_fat += fat
                
                self.results_text.insert(tk.END, details_text + "\n")
            
            # Resumo total
            self.results_text.insert(tk.END, "\n" + "="*50 + "\n")
            self.results_text.insert(tk.END, "📊 RESUMO NUTRICIONAL TOTAL:\n")
            self.results_text.insert(tk.END, f"🔥 Calorias: {total_calories:.0f} kcal\n")
            self.results_text.insert(tk.END, f"🥩 Proteínas: {total_protein:.1f}g\n")
            self.results_text.insert(tk.END, f"🍞 Carboidratos: {total_carbs:.1f}g\n")
            self.results_text.insert(tk.END, f"🧈 Gorduras: {total_fat:.1f}g\n\n")
            
            # Classificação
            self.results_text.insert(tk.END, self.get_calorie_classification(total_calories))
            
            self.results_text.config(state=tk.DISABLED)
            
            # Salvar no histórico
            self.save_calculation(ingredients_text, total_calories)
            
            self.update_status("✅ Cálculo concluído!", '#4CAF50')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
            self.update_status("❌ Erro no cálculo", '#F44336')
            
    def analyze_ingredient(self, ingredient_text):
        """Analisa um ingrediente específico"""
        # Extrair quantidade e nome
        quantity = 100  # padrão
        ingredient_name = ingredient_text.lower().strip()
        
        # Tentar extrair quantidade
        quantity_match = re.search(r'(\d+)\s*(g|kg|ml|l)?', ingredient_text.lower())
        if quantity_match:
            quantity_value = int(quantity_match.group(1))
            unit = quantity_match.group(2)
            
            # Converter para gramas
            if unit == 'kg':
                quantity = quantity_value * 1000
            elif unit in ['ml', 'l']:
                quantity = quantity_value * (1000 if unit == 'l' else 1)
            else:
                quantity = quantity_value
            
            # Remover quantidade do nome
            ingredient_name = re.sub(r'\d+\s*(g|kg|ml|l)?', '', ingredient_name).strip()
        
        # Buscar no banco de dados
        nutrition_info = None
        found_key = None
        
        # Busca exata primeiro
        if ingredient_name in self.calorie_db:
            nutrition_info = self.calorie_db[ingredient_name]
            found_key = ingredient_name
        else:
            # Busca aproximada
            for key, info in self.calorie_db.items():
                if key in ingredient_name or ingredient_name in key:
                    nutrition_info = info
                    found_key = key
                    break
        
        if not nutrition_info:
            # Valor estimado para ingredientes não encontrados
            nutrition_info = {'calorias': 50, 'proteinas': 2, 'carboidratos': 10, 'gorduras': 1}
            found_text = " (estimativa)"
        else:
            found_text = f" (como '{found_key}')" if found_key != ingredient_name else ""
        
        # Calcular proporcionalmente
        factor = quantity / 100
        calories = nutrition_info['calorias'] * factor
        protein = nutrition_info['proteinas'] * factor
        carbs = nutrition_info['carboidratos'] * factor
        fat = nutrition_info['gorduras'] * factor
        
        details_text = f"🔸 {ingredient_name.title()} ({quantity}g){found_text}:\n"
        details_text += f"   🔥 {calories:.0f} kcal | 🥩 {protein:.1f}g prot | 🍞 {carbs:.1f}g carb | 🧈 {fat:.1f}g gord"
        
        return calories, protein, carbs, fat, details_text
        
    def get_calorie_classification(self, total_calories):
        """Classifica o prato baseado nas calorias"""
        classification = "\n🏷️ CLASSIFICAÇÃO DO PRATO:\n"
        
        if total_calories < 200:
            classification += "🟢 Lanche Leve\n"
            classification += "💡 Ideal para lanches entre refeições\n"
        elif total_calories < 400:
            classification += "🟡 Refeição Leve\n"
            classification += "💡 Boa opção para café da manhã ou jantar\n"
        elif total_calories < 700:
            classification += "🟠 Refeição Moderada\n"
            classification += "💡 Adequada para almoço ou após exercícios\n"
        else:
            classification += "🔴 Refeição Calórica\n"
            classification += "💡 Refeição completa, considere porções menores\n"
        
        return classification
        
    def search_ingredient(self):
        """Busca ingrediente na base de dados"""
        search_term = self.search_var.get().lower().strip()
        
        if not search_term:
            self.load_ingredients_table()
            return
            
        # Filtrar ingredientes
        filtered_ingredients = {}
        for name, info in self.calorie_db.items():
            if search_term in name.lower():
                filtered_ingredients[name] = info
        
        # Atualizar tabela
        self.load_ingredients_table(filtered_ingredients)
        
    def load_ingredients_table(self, ingredients_dict=None):
        """Carrega tabela de ingredientes"""
        # Limpar tabela
        for item in self.ingredients_tree.get_children():
            self.ingredients_tree.delete(item)
        
        # Usar dicionário fornecido ou completo
        ingredients = ingredients_dict if ingredients_dict else self.calorie_db
        
        # Adicionar ingredientes ordenados
        for name in sorted(ingredients.keys()):
            info = ingredients[name]
            self.ingredients_tree.insert('', tk.END, values=(
                name.title(),
                f"{info['calorias']:.0f}",
                f"{info['proteinas']:.1f}",
                f"{info['carboidratos']:.1f}",
                f"{info['gorduras']:.1f}"
            ))
    
    def save_calculation(self, ingredients_text, total_calories):
        """Salva cálculo no histórico"""
        try:
            history_db.add_analysis(
                ingredient=f"Cálculo: {ingredients_text[:50]}...",
                recipes_response=f"Total: {total_calories:.0f} kcal",
                source_mode="calorie_calculation"
            )
        except Exception as e:
            print(f"Erro ao salvar no histórico: {e}")
            
    def load_calculation_history(self):
        """Carrega histórico de cálculos"""
        try:
            all_analyses = history_db.get_recent_analyses(limit=50)
            calorie_analyses = [a for a in all_analyses if a.get('source_mode') == 'calorie_calculation']
            
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            
            if calorie_analyses:
                self.history_text.insert(tk.END, "📊 HISTÓRICO DE CÁLCULOS\n")
                self.history_text.insert(tk.END, "="*40 + "\n\n")
                
                for analysis in calorie_analyses:
                    timestamp = analysis.get('timestamp', 'N/A')
                    ingredient = analysis.get('ingredient_identified', 'N/A')
                    result = analysis.get('recipes_found', 'N/A')
                    
                    self.history_text.insert(tk.END, f"📅 {timestamp}\n")
                    self.history_text.insert(tk.END, f"🥬 {ingredient}\n")
                    self.history_text.insert(tk.END, f"📊 {result}\n\n")
            else:
                self.history_text.insert(tk.END, "Nenhum cálculo realizado ainda.\nComece calculando as calorias!")
                
            self.history_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {str(e)}")
            
    def clear_input(self):
        """Limpa campo de entrada"""
        self.ingredients_text.delete(1.0, tk.END)
        self.update_status("🔵 Campo limpo", '#2196F3')
        
    def update_status(self, message, color='#2196F3'):
        """Atualiza mensagem de status"""
        self.status_label.config(text=message, fg=color)
        
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

if __name__ == "__main__":
    app = CalorieCalculatorInterface()
    app.run()