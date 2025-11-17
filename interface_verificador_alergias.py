#!/usr/bin/env python3
"""
Interface de Verificação de Alergias - Chef RAG v2
==================================================

Interface gráfica para verificar alergias em receitas.
Design limpo e simples com histórico integrado.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import uuid

# Importação do banco de dados
from core_logic.database import history_db

class AllergyCheckerInterface:
    """Interface para verificação de alergias"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.setup_allergen_database()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("🚫 Chef RAG v2 - Verificador de Alergias")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#F44336', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🚫 Verificador de Alergias - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#F44336', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_checker_tab()
        self.setup_allergens_tab()
        self.setup_history_tab()
        
    def setup_checker_tab(self):
        """Configura aba do verificador"""
        self.checker_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.checker_frame, text="🔍 Verificar")
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(self.checker_frame, text="📝 Informações", padding=15)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Alergia
        tk.Label(input_frame, text="🚨 Sua Alergia:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.allergy_var = tk.StringVar()
        allergy_combo = ttk.Combobox(input_frame, textvariable=self.allergy_var,
                                    values=['Amendoim', 'Nozes', 'Leite/Lactose', 'Ovos', 
                                           'Glúten', 'Frutos do Mar', 'Soja', 'Outros'],
                                    font=('Arial', 12), width=30)
        allergy_combo.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        # Receita/Ingredientes
        tk.Label(input_frame, text="🍽️ Receita/Ingredientes:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky='nw', pady=5)
        self.recipe_text = tk.Text(input_frame, height=5, font=('Arial', 11), width=50)
        self.recipe_text.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        # Botões
        button_frame = tk.Frame(input_frame, bg='white')
        button_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        check_btn = tk.Button(button_frame,
                             text="🔍 Verificar Segurança",
                             command=self.check_allergy,
                             bg='#4CAF50',
                             fg='white',
                             font=('Arial', 12, 'bold'),
                             relief='flat',
                             padx=30,
                             pady=10)
        check_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame,
                             text="🧹 Limpar",
                             command=self.clear_fields,
                             bg='#FF9800',
                             fg='white',
                             font=('Arial', 12, 'bold'),
                             relief='flat',
                             padx=30,
                             pady=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de resultados
        results_frame = ttk.LabelFrame(self.checker_frame, text="⚠️ Resultado da Análise", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de resultados
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                     height=15,
                                                     font=('Arial', 11),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Status
        self.status_label = tk.Label(self.checker_frame, 
                                    text="🔵 Selecione sua alergia e digite a receita",
                                    font=('Arial', 11),
                                    fg='#2196F3',
                                    bg='white')
        self.status_label.pack(pady=10)
        
    def setup_allergens_tab(self):
        """Configura aba de alérgenos"""
        self.allergens_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.allergens_frame, text="📚 Base de Alérgenos")
        
        # Frame de informações
        info_frame = ttk.LabelFrame(self.allergens_frame, text="📖 Alérgenos Comuns", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto informativo
        self.allergens_info_text = scrolledtext.ScrolledText(info_frame,
                                                            height=25,
                                                            font=('Arial', 10),
                                                            wrap=tk.WORD,
                                                            state=tk.DISABLED)
        self.allergens_info_text.pack(fill=tk.BOTH, expand=True)
        
        self.load_allergens_info()
        
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
        
        # Histórico
        history_list_frame = ttk.LabelFrame(self.history_frame, text="📜 Verificações Anteriores", padding=10)
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(history_list_frame,
                                                     height=20,
                                                     font=('Arial', 10),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        self.load_history()
        
    def setup_allergen_database(self):
        """Configura base de alérgenos"""
        self.allergens_db = {
            'amendoim': {
                'ingredients': ['amendoim', 'pasta de amendoim', 'óleo de amendoim', 'manteiga de amendoim'],
                'hidden_sources': ['alguns óleos vegetais', 'molhos asiáticos', 'doces industrializados'],
                'severity': 'ALTA',
                'description': 'Uma das alergias mais graves e comuns'
            },
            'nozes': {
                'ingredients': ['nozes', 'castanha', 'amêndoa', 'avelã', 'pistache', 'caju', 'macadâmia'],
                'hidden_sources': ['farinhas especiais', 'granolas', 'chocolates', 'sorvetes'],
                'severity': 'ALTA',
                'description': 'Inclui todas as castanhas e nozes de árvore'
            },
            'leite': {
                'ingredients': ['leite', 'queijo', 'iogurte', 'manteiga', 'creme de leite', 'lactose', 
                               'caseína', 'soro de leite'],
                'hidden_sources': ['pães', 'biscoitos', 'molhos', 'embutidos', 'chocolate ao leite'],
                'severity': 'MODERADA',
                'description': 'Inclui lactose e proteínas do leite'
            },
            'ovos': {
                'ingredients': ['ovo', 'clara', 'gema', 'maionese', 'albumina'],
                'hidden_sources': ['massas', 'pães', 'bolos', 'sorvetes', 'alguns vinhos'],
                'severity': 'MODERADA',
                'description': 'Comum em produtos de panificação'
            },
            'glúten': {
                'ingredients': ['trigo', 'farinha', 'pão', 'macarrão', 'massa', 'centeio', 'cevada', 
                               'aveia contaminada'],
                'hidden_sources': ['molho de soja', 'temperos prontos', 'cerveja', 'embutidos'],
                'severity': 'MODERADA',
                'description': 'Proteína encontrada em cereais'
            },
            'frutos do mar': {
                'ingredients': ['camarão', 'peixe', 'salmão', 'atum', 'sardinha', 'marisco', 'lula', 
                               'polvo', 'caranguejo', 'lagosta'],
                'hidden_sources': ['molhos de peixe', 'caldos', 'gelatinas', 'suplementos de ômega-3'],
                'severity': 'ALTA',
                'description': 'Inclui peixes e crustáceos'
            },
            'soja': {
                'ingredients': ['soja', 'molho de soja', 'tofu', 'tempeh', 'miso', 'edamame', 'lecitina de soja'],
                'hidden_sources': ['óleos vegetais', 'chocolates', 'pães', 'emulsificantes'],
                'severity': 'MODERADA',
                'description': 'Muito comum como aditivo alimentar'
            }
        }
        
    def check_allergy(self):
        """Verifica alergias na receita"""
        allergy = self.allergy_var.get().lower().strip()
        recipe = self.recipe_text.get(1.0, tk.END).strip().lower()
        
        if not allergy or not recipe:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
            
        try:
            self.update_status("🔄 Analisando segurança...", '#FF9800')
            
            # Buscar alérgeno na base
            allergen_key = None
            for key in self.allergens_db.keys():
                if key in allergy or allergy in key:
                    allergen_key = key
                    break
            
            if not allergen_key and 'lactose' in allergy:
                allergen_key = 'leite'
                
            if not allergen_key:
                allergen_key = 'outros'
                
            # Analisar receita
            risk_found = False
            dangerous_ingredients = []
            
            if allergen_key != 'outros' and allergen_key in self.allergens_db:
                allergen_data = self.allergens_db[allergen_key]
                
                # Verificar ingredientes diretos
                for ingredient in allergen_data['ingredients']:
                    if ingredient in recipe:
                        risk_found = True
                        dangerous_ingredients.append(ingredient)
                
                # Verificar fontes ocultas
                for source in allergen_data['hidden_sources']:
                    if source in recipe:
                        risk_found = True
                        dangerous_ingredients.append(f"{source} (fonte oculta)")
            
            # Mostrar resultado
            self.show_allergy_result(allergy, recipe, risk_found, dangerous_ingredients, allergen_key)
            
            # Salvar no histórico
            self.save_check(allergy, recipe, risk_found)
            
            self.update_status("✅ Análise concluída!", '#4CAF50')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na verificação: {str(e)}")
            self.update_status("❌ Erro na análise", '#F44336')
            
    def show_allergy_result(self, allergy, recipe, risk_found, dangerous_ingredients, allergen_key):
        """Mostra resultado da verificação"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "🚫 ANÁLISE DE SEGURANÇA ALIMENTAR\\n")
        self.results_text.insert(tk.END, "="*50 + "\\n\\n")
        
        self.results_text.insert(tk.END, f"🚨 Alergia: {allergy.title()}\\n")
        self.results_text.insert(tk.END, f"🍽️ Receita analisada: {recipe[:100]}...\\n\\n")
        
        if risk_found:
            self.results_text.insert(tk.END, "🔴 ATENÇÃO - RISCO DE ALERGIA DETECTADO!\\n\\n")
            self.results_text.insert(tk.END, "⚠️ Ingredientes problemáticos encontrados:\\n")
            for ingredient in dangerous_ingredients:
                self.results_text.insert(tk.END, f"   • {ingredient.title()}\\n")
            self.results_text.insert(tk.END, f"\\n🚨 NÃO RECOMENDADO para pessoas com alergia a {allergy}\\n")
            self.results_text.insert(tk.END, "\\n🛡️ RECOMENDAÇÕES:\\n")
            self.results_text.insert(tk.END, "   • Evite completamente este prato\\n")
            self.results_text.insert(tk.END, "   • Verifique todos os rótulos dos ingredientes\\n")
            self.results_text.insert(tk.END, "   • Considere alternativas seguras\\n")
        else:
            self.results_text.insert(tk.END, "🟢 RECEITA APARENTEMENTE SEGURA\\n\\n")
            self.results_text.insert(tk.END, f"✅ Nenhum ingrediente relacionado a {allergy} foi detectado\\n")
            self.results_text.insert(tk.END, "\\n⚠️ IMPORTANTE:\\n")
            self.results_text.insert(tk.END, "   • Sempre verifique rótulos de produtos industrializados\\n")
            self.results_text.insert(tk.END, "   • Cuidado com contaminação cruzada na cozinha\\n")
            self.results_text.insert(tk.END, "   • Em caso de dúvida, consulte um profissional\\n")
        
        # Informações adicionais sobre o alérgeno
        if allergen_key in self.allergens_db:
            allergen_data = self.allergens_db[allergen_key]
            self.results_text.insert(tk.END, f"\\n📚 SOBRE A ALERGIA A {allergy.upper()}:\\n")
            self.results_text.insert(tk.END, f"   📝 {allergen_data['description']}\\n")
            self.results_text.insert(tk.END, f"   ⚡ Gravidade: {allergen_data['severity']}\\n")
        
        self.results_text.insert(tk.END, "\\n" + "="*50)
        
        self.results_text.config(state=tk.DISABLED)
        
    def load_allergens_info(self):
        """Carrega informações sobre alérgenos"""
        self.allergens_info_text.config(state=tk.NORMAL)
        self.allergens_info_text.delete(1.0, tk.END)
        
        self.allergens_info_text.insert(tk.END, "📚 GUIA COMPLETO DE ALÉRGENOS ALIMENTARES\\n")
        self.allergens_info_text.insert(tk.END, "="*60 + "\\n\\n")
        
        for allergen, data in self.allergens_db.items():
            self.allergens_info_text.insert(tk.END, f"🚨 {allergen.upper()}\\n")
            self.allergens_info_text.insert(tk.END, f"📝 {data['description']}\\n")
            self.allergens_info_text.insert(tk.END, f"⚡ Gravidade: {data['severity']}\\n")
            
            self.allergens_info_text.insert(tk.END, "\\n🔸 Ingredientes diretos:\\n")
            for ingredient in data['ingredients']:
                self.allergens_info_text.insert(tk.END, f"   • {ingredient.title()}\\n")
            
            self.allergens_info_text.insert(tk.END, "\\n🔸 Fontes ocultas:\\n")
            for source in data['hidden_sources']:
                self.allergens_info_text.insert(tk.END, f"   • {source.title()}\\n")
            
            self.allergens_info_text.insert(tk.END, "\\n" + "-"*40 + "\\n\\n")
        
        self.allergens_info_text.insert(tk.END, "⚠️ DICAS IMPORTANTES:\\n")
        self.allergens_info_text.insert(tk.END, "• Sempre leia rótulos completos\\n")
        self.allergens_info_text.insert(tk.END, "• Cuidado com contaminação cruzada\\n")
        self.allergens_info_text.insert(tk.END, "• Em caso de dúvida, não consuma\\n")
        self.allergens_info_text.insert(tk.END, "• Consulte sempre um alergologista\\n")
        
        self.allergens_info_text.config(state=tk.DISABLED)
        
    def save_check(self, allergy, recipe, risk_found):
        """Salva verificação no histórico"""
        try:
            result = "RISCO DETECTADO" if risk_found else "SEGURA"
            
            history_db.add_analysis(
                ingredient=f"Alergia: {allergy}",
                recipes_response=f"Receita verificada - {result}",
                source_mode="allergy_check"
            )
        except Exception as e:
            print(f"Erro ao salvar no histórico: {e}")
            
    def load_history(self):
        """Carrega histórico de verificações"""
        try:
            all_analyses = history_db.get_recent_analyses(limit=100)
            allergy_analyses = [a for a in all_analyses if a.get('source_mode') == 'allergy_check']
            
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            
            if allergy_analyses:
                self.history_text.insert(tk.END, "🚫 HISTÓRICO DE VERIFICAÇÕES DE ALERGIAS\\n")
                self.history_text.insert(tk.END, "="*50 + "\\n\\n")
                
                for analysis in allergy_analyses:
                    timestamp = analysis.get('timestamp', 'N/A')
                    ingredient = analysis.get('ingredient_identified', 'N/A')
                    result = analysis.get('recipes_found', 'N/A')
                    
                    self.history_text.insert(tk.END, f"📅 {timestamp}\\n")
                    self.history_text.insert(tk.END, f"🚨 {ingredient}\\n")
                    self.history_text.insert(tk.END, f"📊 {result}\\n\\n")
            else:
                self.history_text.insert(tk.END, "Nenhuma verificação realizada ainda.\\nComece verificando a segurança das suas receitas!")
                
            self.history_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {str(e)}")
            
    def clear_fields(self):
        """Limpa campos de entrada"""
        self.allergy_var.set('')
        self.recipe_text.delete(1.0, tk.END)
        self.update_status("🔵 Campos limpos", '#2196F3')
        
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
    app = AllergyCheckerInterface()
    app.run()