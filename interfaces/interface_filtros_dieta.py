#!/usr/bin/env python3
"""
Interface de Filtros Dietéticos - Chef RAG v2
=============================================

Interface gráfica para filtrar receitas por dietas especiais.
Design limpo e simples com histórico integrado.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import uuid

# Importação do banco de dados e sistema RAG
from core_logic.database import history_db

try:
    from sistema_busca_robusta import buscar_receitas_robusta
except ImportError:
    buscar_receitas_robusta = None

class DietFilterInterface:
    """Interface para filtros dietéticos"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("🥗 Chef RAG v2 - Filtros Dietéticos")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#4CAF50', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🥗 Filtros Dietéticos - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#4CAF50', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_filter_tab()
        self.setup_results_tab()
        
    def setup_filter_tab(self):
        """Configura aba de filtros"""
        self.filter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.filter_frame, text="🔍 Filtrar")
        
        # Frame de seleção de dietas
        diet_frame = ttk.LabelFrame(self.filter_frame, text="🍽️ Selecione as Dietas", padding=15)
        diet_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Checkboxes para dietas
        self.diet_vars = {}
        diets = [
            ('vegetariana', 'Vegetariana', '🌱'),
            ('vegana', 'Vegana', '🌿'),
            ('sem_gluten', 'Sem Glúten', '🌾'),
            ('sem_lactose', 'Sem Lactose', '🥛'),
            ('low_carb', 'Low Carb', '🥩'),
            ('cetogenica', 'Cetogênica', '🧈'),
            ('mediterranea', 'Mediterrânea', '🫒'),
            ('paleo', 'Paleo', '🦣'),
        ]
        
        for i, (key, name, emoji) in enumerate(diets):
            var = tk.BooleanVar()
            self.diet_vars[key] = var
            
            frame = tk.Frame(diet_frame, bg='white')
            frame.grid(row=i//2, column=i%2, sticky='w', padx=20, pady=8)
            
            cb = tk.Checkbutton(frame, text=f"{emoji} {name}", variable=var, 
                               font=('Arial', 12), bg='white')
            cb.pack(side=tk.LEFT)
        
        # Frame de filtros adicionais
        additional_frame = ttk.LabelFrame(self.filter_frame, text="⚙️ Filtros Adicionais", padding=15)
        additional_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Tempo máximo de preparo
        time_frame = tk.Frame(additional_frame, bg='white')
        time_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(time_frame, text="⏱️ Tempo máximo (minutos):", font=('Arial', 11, 'bold'), bg='white').pack(side=tk.LEFT)
        self.max_time_var = tk.StringVar(value="60")
        time_entry = tk.Entry(time_frame, textvariable=self.max_time_var, font=('Arial', 11), width=10)
        time_entry.pack(side=tk.LEFT, padx=10)
        
        # Dificuldade
        difficulty_frame = tk.Frame(additional_frame, bg='white')
        difficulty_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(difficulty_frame, text="📊 Dificuldade máxima:", font=('Arial', 11, 'bold'), bg='white').pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="intermediário")
        difficulty_combo = ttk.Combobox(difficulty_frame, textvariable=self.difficulty_var,
                                       values=['iniciante', 'intermediário', 'avançado'],
                                       font=('Arial', 11), width=15)
        difficulty_combo.pack(side=tk.LEFT, padx=10)
        
        # Botões
        button_frame = tk.Frame(self.filter_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        search_btn = tk.Button(button_frame,
                              text="🔍 Buscar Receitas",
                              command=self.search_recipes,
                              bg='#4CAF50',
                              fg='white',
                              font=('Arial', 12, 'bold'),
                              relief='flat',
                              padx=30,
                              pady=10)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame,
                             text="🧹 Limpar Filtros",
                             command=self.clear_filters,
                             bg='#FF9800',
                             fg='white',
                             font=('Arial', 12, 'bold'),
                             relief='flat',
                             padx=30,
                             pady=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = tk.Label(self.filter_frame, 
                                    text="🔵 Selecione os filtros e clique em Buscar",
                                    font=('Arial', 11),
                                    fg='#2196F3',
                                    bg='white')
        self.status_label.pack(pady=10)
        
    def setup_results_tab(self):
        """Configura aba de resultados"""
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="📋 Resultados")
        
        # Frame de informações
        info_frame = ttk.LabelFrame(self.results_frame, text="📊 Informações da Busca", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.search_info_label = tk.Label(info_frame, 
                                         text="Nenhuma busca realizada ainda",
                                         font=('Arial', 11),
                                         anchor='w')
        self.search_info_label.pack(fill=tk.X)
        
        # Frame de resultados
        results_list_frame = ttk.LabelFrame(self.results_frame, text="🍽️ Receitas Encontradas", padding=10)
        results_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de resultados
        self.results_text = scrolledtext.ScrolledText(results_list_frame,
                                                     height=20,
                                                     font=('Arial', 10),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        action_frame = tk.Frame(self.results_frame, bg='white')
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        export_btn = tk.Button(action_frame,
                              text="💾 Exportar Resultados",
                              command=self.export_results,
                              bg='#2196F3',
                              fg='white',
                              font=('Arial', 11, 'bold'),
                              relief='flat',
                              padx=20,
                              pady=8)
        export_btn.pack(side=tk.LEFT, padx=5)
        
    def search_recipes(self):
        """Busca receitas baseado nos filtros selecionados"""
        try:
            # Coletar filtros selecionados
            selected_diets = [diet for diet, var in self.diet_vars.items() if var.get()]
            
            if not selected_diets:
                messagebox.showwarning("Aviso", "Selecione pelo menos uma dieta!")
                return
            
            self.update_status("🔄 Buscando receitas...", '#FF9800')
            
            # Primeiro tentar buscar no histórico
            recipes = []
            try:
                filters = {diet: True for diet in selected_diets}
                recipes = history_db.get_recipes_by_dietary_filter(filters)
            except:
                recipes = []
            
            # Se não encontrar receitas salvas, usar sistema robusto
            if not recipes and buscar_receitas_robusta:
                try:
                    # Criar ingredientes típicos para as dietas selecionadas
                    diet_ingredients = self.get_ingredients_for_diets(selected_diets)
                    
                    # Gerar receitas usando sistema robusto
                    print(f"🧠 Buscando receitas {', '.join(selected_diets)} com sistema robusto...")
                    
                    ai_recipes = buscar_receitas_robusta(diet_ingredients)
                    
                    if ai_recipes:
                        # Converter resposta em formato de receitas
                        recipes = []
                        for i, recipe_text in enumerate(ai_recipes, 1):
                            recipe = {
                                'recipe_name': f"Receita {', '.join([d.replace('_', ' ').title() for d in selected_diets])} #{i}",
                                'description': recipe_text[:200] + "..." if len(recipe_text) > 200 else recipe_text,
                                'full_text': recipe_text,
                                'dietary_properties': {diet: True for diet in selected_diets}
                            }
                            recipes.append(recipe)
                        
                except Exception as e:
                    print(f"Erro ao buscar receitas: {e}")
                    # Criar receita básica como fallback
                    diet_description = ", ".join([d.replace('_', ' ').title() for d in selected_diets])
                    fallback_recipe = {
                        'recipe_name': f"Sugestão {diet_description}",
                        'description': f"Receita básica seguindo dieta {diet_description}",
                        'full_text': f"Aqui está uma sugestão para dieta {diet_description}. Consulte um nutricionista para receitas específicas.",
                        'dietary_properties': {diet: True for diet in selected_diets}
                    }
                    recipes = [fallback_recipe]
            
            # Mostrar resultados
            self.show_results(selected_diets, recipes)
            
            # Atualizar informações da busca
            search_info = f"Filtros: {', '.join([d.replace('_', ' ').title() for d in selected_diets])}"
            search_info += f" | Tempo máx: {self.max_time_var.get()}min"
            search_info += f" | Dificuldade: {self.difficulty_var.get()}"
            search_info += f" | Encontradas: {len(recipes)} receitas"
            
            self.search_info_label.config(text=search_info)
            
            # Mudar para aba de resultados
            self.notebook.select(1)
            
            self.update_status("✅ Busca concluída!", '#4CAF50')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar receitas: {str(e)}")
            self.update_status("❌ Erro na busca", '#F44336')
            
    def get_ingredients_for_diets(self, selected_diets):
        """Retorna ingredientes típicos para as dietas selecionadas"""
        diet_ingredients_map = {
            'vegetariana': ['tofu', 'cogumelos', 'queijo', 'ovos', 'verduras'],
            'vegana': ['lentilha', 'grão de bico', 'quinoa', 'castanhas', 'vegetais'],
            'sem_gluten': ['arroz', 'quinoa', 'batata', 'legumes', 'carne'],
            'cetogenica': ['abacate', 'azeite', 'carne', 'peixe', 'queijo'],
            'paleo': ['carne', 'peixe', 'vegetais', 'frutas', 'castanhas'],
            'low_carb': ['frango', 'ovos', 'verduras', 'azeite', 'peixes'],
            'mediterranea': ['azeite', 'peixe', 'vegetais', 'frutas', 'grãos'],
            'dash': ['vegetais', 'frutas', 'grãos integrais', 'peixe', 'frango']
        }
        
        # Combinar ingredientes das dietas selecionadas
        all_ingredients = set()
        for diet in selected_diets:
            if diet in diet_ingredients_map:
                all_ingredients.update(diet_ingredients_map[diet])
        
        # Retornar alguns ingredientes principais
        return list(all_ingredients)[:5]
    
    def parse_ai_recipes(self, ai_response, selected_diets):
        """Converte resposta da IA em lista de receitas"""
        try:
            recipes = []
            
            # Dividir a resposta em receitas individuais
            recipe_sections = ai_response.split('Receita')
            
            for i, section in enumerate(recipe_sections[1:], 1):  # Pular primeira seção vazia
                if section.strip():
                    recipe = {
                        'recipe_name': f"Receita {', '.join([d.replace('_', ' ').title() for d in selected_diets])} #{i}",
                        'description': section.strip()[:200] + "...",
                        'full_text': section.strip(),
                        'dietary_properties': {diet: True for diet in selected_diets}
                    }
                    recipes.append(recipe)
            
            # Se não conseguir dividir, criar uma receita única
            if not recipes:
                recipes = [{
                    'recipe_name': f"Receita {', '.join([d.replace('_', ' ').title() for d in selected_diets])}",
                    'description': ai_response[:200] + "...",
                    'full_text': ai_response,
                    'dietary_properties': {diet: True for diet in selected_diets}
                }]
            
            return recipes[:3]  # Máximo 3 receitas
            
        except Exception as e:
            print(f"Erro ao processar receitas da IA: {e}")
            return []
            
    def show_results(self, selected_diets, recipes):
        """Mostra resultados da busca"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if recipes:
            self.results_text.insert(tk.END, f"🥗 RECEITAS ENCONTRADAS ({len(recipes)}):\n")
            self.results_text.insert(tk.END, "="*60 + "\n\n")
            
            for i, recipe in enumerate(recipes, 1):
                self.results_text.insert(tk.END, f"{i}. 🍽️ {recipe.get('recipe_name', 'Receita sem nome')}\n")
                
                if recipe.get('description'):
                    self.results_text.insert(tk.END, f"   📝 {recipe['description']}\n")
                
                # Mostrar propriedades dietéticas
                diet_props = []
                for diet in selected_diets:
                    if recipe.get(f'is_{diet}'):
                        diet_props.append(diet.replace('_', ' ').title())
                
                if diet_props:
                    self.results_text.insert(tk.END, f"   🏷️ {', '.join(diet_props)}\n")
                
                if recipe.get('cooking_time'):
                    self.results_text.insert(tk.END, f"   ⏱️ Tempo: {recipe['cooking_time']} min\n")
                
                self.results_text.insert(tk.END, "\n")
            
            # Adicionar opção para cozinhar
            self.results_text.insert(tk.END, "👨‍🍳 BORA COZINHAR? Digite o número da receita que você gostou!\n\n")
            
            # Criar botões para seleção de receita
            self.create_recipe_selection_buttons(recipes)
            
        else:
            self.results_text.insert(tk.END, "❌ NENHUMA RECEITA ENCONTRADA\n\n")
            self.results_text.insert(tk.END, "💡 DICAS:\n")
            self.results_text.insert(tk.END, "• Tente filtros menos restritivos\n")
            self.results_text.insert(tk.END, "• Use o sistema para analisar mais ingredientes\n")
            self.results_text.insert(tk.END, "• Receitas dietéticas são adicionadas automaticamente\n")
            self.results_text.insert(tk.END, "  quando você usa outras funcionalidades do Chef RAG\n")
        
        self.results_text.config(state=tk.DISABLED)
        
        # Salvar busca no histórico
        try:
            search_data = {
                'session_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'method': 'diet_filter',
                'filters': selected_diets,
                'results_count': len(recipes),
                'success': len(recipes) > 0
            }
            
            history_db.add_analysis(
                ingredient=f"Filtros: {', '.join(selected_diets)}",
                recipes_response=f"{len(recipes)} receitas encontradas",
                source_mode="diet_filter"
            )
        except:
            pass
    
    def create_recipe_selection_buttons(self, recipes):
        """Cria botões para seleção de receitas para cozinhar"""
        # Remover botões anteriores se existirem
        if hasattr(self, 'recipe_buttons_frame'):
            self.recipe_buttons_frame.destroy()
        
        self.recipe_buttons_frame = tk.Frame(self.root, bg='#f5f5f5')
        self.recipe_buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(self.recipe_buttons_frame, text="👨‍🍳 Escolha uma receita para cozinhar:", 
                font=('Arial', 12, 'bold'), bg='#f5f5f5').pack(pady=5)
        
        buttons_frame = tk.Frame(self.recipe_buttons_frame, bg='#f5f5f5')
        buttons_frame.pack(pady=5)
        
        for i, recipe in enumerate(recipes, 1):
            btn = tk.Button(buttons_frame, 
                           text=f"🍽️ Receita {i}",
                           font=('Arial', 10, 'bold'),
                           bg='#4CAF50', fg='white',
                           width=15, height=2,
                           command=lambda r=recipe: self.start_cooking(r))
            btn.pack(side=tk.LEFT, padx=5)
    
    def start_cooking(self, recipe):
        """Inicia o processo de cozimento para receita selecionada"""
        try:
            print(f"🧑‍🍳 Preparando para cozinhar: {recipe.get('recipe_name', 'Receita')}")
            
            # Processar dados da receita
            from sistema_hibrido_json_pdf import extrair_dados_receita_json
            from sistema_busca_robusta import processar_receita_para_cozinha
            
            # Extrair texto completo da receita
            receita_texto = recipe.get('full_text', recipe.get('description', ''))
            
            # Processar para interface de cozinha  
            # Convertendo texto para formato JSON para extração
            dados_basicos = {
                "nome": "Receita Encontrada",
                "ingredientes": [],
                "modo_preparo": []
            }
            dados_receita = extrair_dados_receita_json(dados_basicos)
            dados_receita['titulo'] = recipe.get('recipe_name', 'Receita Selecionada')
            
            # Abrir interface de cozinha
            from interface_cozinha_passo_passo import abrir_interface_cozinha
            abrir_interface_cozinha(dados_receita)
            
            # Fechar esta janela
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir interface de cozinha: {e}")
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            
    def clear_filters(self):
        """Limpa todos os filtros"""
        for var in self.diet_vars.values():
            var.set(False)
        self.max_time_var.set("60")
        self.difficulty_var.set("intermediário")
        self.update_status("🔵 Filtros limpos", '#2196F3')
        
    def export_results(self):
        """Exporta resultados para arquivo"""
        try:
            from tkinter import filedialog
            
            file_path = filedialog.asksaveasfilename(
                title="Salvar resultados",
                defaultextension=".txt",
                filetypes=[("Texto", "*.txt"), ("Todos os arquivos", "*.*")]
            )
            
            if file_path:
                content = self.results_text.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"FILTROS DIETÉTICOS - CHEF RAG v2\n")
                    f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                    f.write("="*60 + "\n\n")
                    f.write(content)
                
                messagebox.showinfo("Sucesso", f"Resultados exportados para:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
            
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
    app = DietFilterInterface()
    app.run()