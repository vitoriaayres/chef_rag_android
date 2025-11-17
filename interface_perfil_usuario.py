#!/usr/bin/env python3
"""
Interface de Perfil do Usuário - Chef RAG v2
============================================

Interface gráfica para gerenciamento de perfil e configurações do usuário.
Design limpo e simples com histórico integrado, seguindo o padrão da interface de voz.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
import uuid

# Importação do banco de dados
from core_logic.database import history_db

class UserProfileInterface:
    """Interface para gerenciamento de perfil do usuário"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.load_profile()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("👤 Chef RAG v2 - Meu Perfil")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#9C27B0', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="👤 Meu Perfil - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#9C27B0', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_profile_tab()
        self.setup_stats_tab()
        self.setup_ratings_tab()
        
    def setup_profile_tab(self):
        """Configura aba de perfil"""
        self.profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.profile_frame, text="👤 Perfil")
        
        # Frame de informações básicas
        basic_frame = ttk.LabelFrame(self.profile_frame, text="📋 Informações Básicas", padding=15)
        basic_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nome
        tk.Label(basic_frame, text="Nome:", font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(basic_frame, textvariable=self.name_var, font=('Arial', 11), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        # Nível de habilidade
        tk.Label(basic_frame, text="Nível:", font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.skill_var = tk.StringVar()
        skill_combo = ttk.Combobox(basic_frame, textvariable=self.skill_var, 
                                  values=['iniciante', 'intermediário', 'avançado', 'profissional'],
                                  font=('Arial', 11), width=27)
        skill_combo.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        # Tempo preferido de cozimento
        tk.Label(basic_frame, text="Tempo preferido (min):", font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        self.time_var = tk.StringVar()
        time_entry = tk.Entry(basic_frame, textvariable=self.time_var, font=('Arial', 11), width=30)
        time_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Frame de preferências
        pref_frame = ttk.LabelFrame(self.profile_frame, text="🍽️ Preferências Alimentares", padding=15)
        pref_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Restrições dietéticas
        tk.Label(pref_frame, text="Restrições Dietéticas:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 5))
        
        restrictions_frame = tk.Frame(pref_frame, bg='white')
        restrictions_frame.pack(fill=tk.X, pady=5)
        
        self.restrictions_vars = {}
        restrictions = ['Vegetariano', 'Vegano', 'Sem Glúten', 'Sem Lactose', 'Low Carb', 'Cetogênica']
        
        for i, restriction in enumerate(restrictions):
            var = tk.BooleanVar()
            self.restrictions_vars[restriction.lower()] = var
            cb = tk.Checkbutton(restrictions_frame, text=restriction, variable=var, 
                               font=('Arial', 10), bg='white')
            cb.grid(row=i//3, column=i%3, sticky='w', padx=10, pady=2)
        
        # Alergias
        tk.Label(pref_frame, text="Alergias:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(15, 5))
        self.allergies_text = tk.Text(pref_frame, height=3, font=('Arial', 10))
        self.allergies_text.pack(fill=tk.X, pady=5)
        
        # Cozinhas favoritas
        tk.Label(pref_frame, text="Cozinhas Favoritas:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(15, 5))
        self.cuisines_text = tk.Text(pref_frame, height=3, font=('Arial', 10))
        self.cuisines_text.pack(fill=tk.X, pady=5)
        
        # Botões
        button_frame = tk.Frame(self.profile_frame, bg='white')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        save_btn = tk.Button(button_frame,
                            text="💾 Salvar Perfil",
                            command=self.save_profile,
                            bg='#4CAF50',
                            fg='white',
                            font=('Arial', 12, 'bold'),
                            relief='flat',
                            padx=30,
                            pady=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(button_frame,
                             text="🔄 Recarregar",
                             command=self.load_profile,
                             bg='#2196F3',
                             fg='white',
                             font=('Arial', 12, 'bold'),
                             relief='flat',
                             padx=30,
                             pady=10)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
    def setup_stats_tab(self):
        """Configura aba de estatísticas"""
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="📊 Estatísticas")
        
        # Frame de estatísticas gerais
        general_stats_frame = ttk.LabelFrame(self.stats_frame, text="📈 Estatísticas Gerais", padding=15)
        general_stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Labels para estatísticas
        self.total_analyses_label = tk.Label(general_stats_frame, text="Total de análises: -", 
                                           font=('Arial', 12), anchor='w')
        self.total_analyses_label.pack(fill=tk.X, pady=5)
        
        self.successful_analyses_label = tk.Label(general_stats_frame, text="Análises bem-sucedidas: -", 
                                                font=('Arial', 12), anchor='w')
        self.successful_analyses_label.pack(fill=tk.X, pady=5)
        
        self.webcam_analyses_label = tk.Label(general_stats_frame, text="Análises por webcam: -", 
                                            font=('Arial', 12), anchor='w')
        self.webcam_analyses_label.pack(fill=tk.X, pady=5)
        
        self.last_updated_label = tk.Label(general_stats_frame, text="Última atualização: -", 
                                         font=('Arial', 12), anchor='w')
        self.last_updated_label.pack(fill=tk.X, pady=5)
        
        # Frame de ingredientes favoritos
        ingredients_frame = ttk.LabelFrame(self.stats_frame, text="🥬 Ingredientes Mais Usados", padding=15)
        ingredients_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de ingredientes
        self.ingredients_text = scrolledtext.ScrolledText(ingredients_frame,
                                                         height=10,
                                                         font=('Arial', 10),
                                                         wrap=tk.WORD,
                                                         state=tk.DISABLED)
        self.ingredients_text.pack(fill=tk.BOTH, expand=True)
        
        # Botão atualizar
        refresh_btn = tk.Button(self.stats_frame,
                               text="🔄 Atualizar Estatísticas",
                               command=self.load_statistics,
                               bg='#2196F3',
                               fg='white',
                               font=('Arial', 11, 'bold'),
                               relief='flat',
                               padx=20,
                               pady=8)
        refresh_btn.pack(pady=10)
        
    def setup_ratings_tab(self):
        """Configura aba de avaliações"""
        self.ratings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ratings_frame, text="⭐ Avaliações")
        
        # Frame de nova avaliação
        new_rating_frame = ttk.LabelFrame(self.ratings_frame, text="➕ Nova Avaliação", padding=15)
        new_rating_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nome da receita
        tk.Label(new_rating_frame, text="Nome da Receita:", font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.recipe_name_var = tk.StringVar()
        recipe_entry = tk.Entry(new_rating_frame, textvariable=self.recipe_name_var, font=('Arial', 11), width=40)
        recipe_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        # Avaliação (estrelas)
        tk.Label(new_rating_frame, text="Avaliação:", font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.rating_var = tk.StringVar()
        rating_combo = ttk.Combobox(new_rating_frame, textvariable=self.rating_var, 
                                   values=['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
                                   font=('Arial', 11), width=37)
        rating_combo.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        # Comentário
        tk.Label(new_rating_frame, text="Comentário:", font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='nw', pady=5)
        self.comment_text = tk.Text(new_rating_frame, height=3, width=40, font=('Arial', 10))
        self.comment_text.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Botão adicionar
        add_rating_btn = tk.Button(new_rating_frame,
                                  text="➕ Adicionar Avaliação",
                                  command=self.add_rating,
                                  bg='#FF9800',
                                  fg='white',
                                  font=('Arial', 11, 'bold'),
                                  relief='flat',
                                  padx=20,
                                  pady=8)
        add_rating_btn.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        # Frame de avaliações existentes
        ratings_list_frame = ttk.LabelFrame(self.ratings_frame, text="📝 Suas Avaliações", padding=15)
        ratings_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de avaliações
        self.ratings_text = scrolledtext.ScrolledText(ratings_list_frame,
                                                     height=12,
                                                     font=('Arial', 10),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.ratings_text.pack(fill=tk.BOTH, expand=True)
        
        # Carregar dados iniciais
        self.load_statistics()
        self.load_ratings()
        
    def load_profile(self):
        """Carrega perfil do banco de dados"""
        try:
            profile = history_db.get_user_profile()
            
            # Carregar informações básicas
            self.name_var.set(profile.get('name', ''))
            self.skill_var.set(profile.get('skill_level', 'iniciante'))
            self.time_var.set(str(profile.get('preferred_cooking_time', 60)))
            
            # Carregar restrições dietéticas
            restrictions_str = profile.get('dietary_restrictions', '[]')
            try:
                restrictions = json.loads(restrictions_str) if restrictions_str != '[]' else []
                for restriction, var in self.restrictions_vars.items():
                    var.set(restriction in [r.lower() for r in restrictions])
            except:
                pass
            
            # Carregar alergias
            allergies_str = profile.get('allergies', '[]')
            try:
                allergies = json.loads(allergies_str) if allergies_str != '[]' else []
                self.allergies_text.delete(1.0, tk.END)
                self.allergies_text.insert(tk.END, ', '.join(allergies))
            except:
                pass
            
            # Carregar cozinhas favoritas
            cuisines_str = profile.get('favorite_cuisines', '[]')
            try:
                cuisines = json.loads(cuisines_str) if cuisines_str != '[]' else []
                self.cuisines_text.delete(1.0, tk.END)
                self.cuisines_text.insert(tk.END, ', '.join(cuisines))
            except:
                pass
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar perfil: {str(e)}")
            
    def save_profile(self):
        """Salva perfil no banco de dados"""
        try:
            # Coletar restrições selecionadas
            selected_restrictions = [name for name, var in self.restrictions_vars.items() if var.get()]
            
            # Coletar alergias
            allergies_text = self.allergies_text.get(1.0, tk.END).strip()
            allergies = [a.strip() for a in allergies_text.split(',') if a.strip()]
            
            # Coletar cozinhas
            cuisines_text = self.cuisines_text.get(1.0, tk.END).strip()
            cuisines = [c.strip() for c in cuisines_text.split(',') if c.strip()]
            
            # Atualizar perfil
            history_db.update_user_profile(
                name=self.name_var.get(),
                skill_level=self.skill_var.get(),
                dietary_restrictions=json.dumps(selected_restrictions),
                allergies=json.dumps(allergies),
                favorite_cuisines=json.dumps(cuisines),
                preferred_cooking_time=int(self.time_var.get()) if self.time_var.get().isdigit() else 60
            )
            
            messagebox.showinfo("Sucesso", "Perfil salvo com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar perfil: {str(e)}")
            
    def load_statistics(self):
        """Carrega estatísticas do banco de dados"""
        try:
            stats = history_db.get_statistics()
            
            self.total_analyses_label.config(text=f"Total de análises: {stats.get('total_analyses', 0)}")
            self.successful_analyses_label.config(text=f"Análises bem-sucedidas: {stats.get('successful_analyses', 0)}")
            self.webcam_analyses_label.config(text=f"Análises por webcam: {stats.get('webcam_analyses', 0)}")
            self.last_updated_label.config(text=f"Última atualização: {stats.get('last_updated', 'N/A')}")
            
            # Carregar ingredientes mais usados
            ingredients = history_db.get_all_ingredients()
            
            self.ingredients_text.config(state=tk.NORMAL)
            self.ingredients_text.delete(1.0, tk.END)
            
            if ingredients:
                self.ingredients_text.insert(tk.END, "🥬 INGREDIENTES MAIS ANALISADOS:\n\n")
                for i, ingredient in enumerate(ingredients[:20], 1):  # Top 20
                    count = history_db.get_ingredient_count(ingredient)
                    self.ingredients_text.insert(tk.END, f"{i}. {ingredient.title()} - {count} vezes\n")
            else:
                self.ingredients_text.insert(tk.END, "Nenhum ingrediente analisado ainda.\nComece usando o sistema para ver suas estatísticas!")
                
            self.ingredients_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar estatísticas: {str(e)}")
            
    def load_ratings(self):
        """Carrega avaliações do banco de dados"""
        try:
            ratings = history_db.get_user_recipe_ratings(limit=50)
            
            self.ratings_text.config(state=tk.NORMAL)
            self.ratings_text.delete(1.0, tk.END)
            
            if ratings:
                for rating in ratings:
                    stars = "⭐" * int(rating.get('rating', 0))
                    self.ratings_text.insert(tk.END, f"🍽️ {rating.get('recipe_name', 'N/A')}\n")
                    self.ratings_text.insert(tk.END, f"   {stars} ({rating.get('rating', 0)}/5)\n")
                    if rating.get('comment'):
                        self.ratings_text.insert(tk.END, f"   💬 {rating['comment']}\n")
                    self.ratings_text.insert(tk.END, f"   📅 {rating.get('created_at', 'N/A')}\n\n")
            else:
                self.ratings_text.insert(tk.END, "Você ainda não avaliou nenhuma receita.\nExperimente algumas receitas e avalie-as!")
                
            self.ratings_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar avaliações: {str(e)}")
            
    def add_rating(self):
        """Adiciona nova avaliação"""
        recipe_name = self.recipe_name_var.get().strip()
        rating_text = self.rating_var.get()
        comment = self.comment_text.get(1.0, tk.END).strip()
        
        if not recipe_name:
            messagebox.showwarning("Aviso", "Digite o nome da receita")
            return
            
        if not rating_text:
            messagebox.showwarning("Aviso", "Selecione uma avaliação")
            return
            
        try:
            # Converter estrelas em número
            rating_num = len([c for c in rating_text if c == '⭐'])
            
            # Adicionar no banco
            history_db.add_recipe_rating(
                recipe_name=recipe_name,
                rating=rating_num,
                comment=comment if comment else None
            )
            
            # Limpar campos
            self.recipe_name_var.set('')
            self.rating_var.set('')
            self.comment_text.delete(1.0, tk.END)
            
            # Recarregar lista
            self.load_ratings()
            
            messagebox.showinfo("Sucesso", "Avaliação adicionada com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar avaliação: {str(e)}")
            
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

if __name__ == "__main__":
    app = UserProfileInterface()
    app.run()