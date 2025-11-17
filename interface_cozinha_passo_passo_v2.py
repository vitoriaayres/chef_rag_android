#!/usr/bin/env python3
"""
Interface Gráfica Passo a Passo - Chef RAG v2
=============================================

Interface gráfica para mostrar receitas passo a passo com todas as informações.
Similar ao reconhecimento de voz, com design limpo e informações completas.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, List
import threading

class InterfacePassoAPasso:
    """Interface gráfica para mostrar receitas passo a passo"""
    
    def __init__(self, receitas_lista: List[Dict] = None):
        self.root = tk.Tk()
        self.receitas_lista = receitas_lista or []
        self.receita_atual = None
        self.passo_atual = 0
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("👨‍🍳 Chef RAG v2 - Cozinha Passo a Passo")
        self.root.geometry("1000x700")
        self.root.configure(bg='white')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#FF5722', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="👨‍🍳 Cozinha Passo a Passo - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#FF5722', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if self.receitas_lista:
            self.criar_interface_selecao(main_frame)
        else:
            self.criar_interface_busca(main_frame)
    
    def criar_interface_busca(self, parent):
        """Cria interface para buscar receitas"""
        # Instruções
        instructions_label = tk.Label(parent, 
                                    text="🔍 Buscar Receitas para Cozinhar:", 
                                    font=('Arial', 14, 'bold'), 
                                    bg='white', 
                                    fg='#333')
        instructions_label.pack(pady=(0, 5))
        
        tip_label = tk.Label(parent, 
                           text="💡 Use vírgulas para busca conjunta: 'chocolate, leite, açúcar'", 
                           font=('Arial', 10), 
                           bg='white', 
                           fg='#666')
        tip_label.pack(pady=(0, 15))
        
        # Campo de busca
        self.search_entry = tk.Entry(parent, font=('Arial', 12), bg='#f5f5f5', relief=tk.FLAT, bd=10)
        self.search_entry.pack(fill=tk.X, pady=5, ipady=8)
        self.search_entry.bind('<Return>', self.buscar_receitas)
        
        # Botão de busca
        search_button = tk.Button(parent, 
                                text="🔍 Buscar Receitas", 
                                font=('Arial', 12, 'bold'), 
                                bg='#FF5722', 
                                fg='white', 
                                relief=tk.FLAT, 
                                padx=20, 
                                pady=10,
                                command=self.buscar_receitas)
        search_button.pack(pady=10)
        
        # Área de resultado
        self.result_frame = tk.Frame(parent, bg='white')
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
    def criar_interface_selecao(self, parent):
        """Cria interface para seleção de receitas"""
        # Título
        title_label = tk.Label(parent, 
                             text="🍽️ Escolha uma receita para cozinhar:", 
                             font=('Arial', 14, 'bold'), 
                             bg='white', 
                             fg='#333')
        title_label.pack(pady=(0, 15))
        
        # Lista de receitas
        self.recipe_listbox = tk.Listbox(parent, 
                                        font=('Arial', 12), 
                                        height=8,
                                        bg='#f8f8f8',
                                        selectbackground='#FF5722',
                                        selectforeground='white')
        self.recipe_listbox.pack(fill=tk.X, pady=10)
        
        for i, receita in enumerate(self.receitas_lista):
            nome = receita.get('nome', f'Receita {i+1}')
            self.recipe_listbox.insert(tk.END, f"{i+1}. {nome}")
        
        # Botão para cozinhar
        cook_button = tk.Button(parent, 
                              text="👨‍🍳 Começar a Cozinhar!", 
                              font=('Arial', 12, 'bold'), 
                              bg='#4CAF50', 
                              fg='white', 
                              relief=tk.FLAT, 
                              padx=20, 
                              pady=10,
                              command=self.iniciar_cozinha)
        cook_button.pack(pady=15)
    
    def buscar_receitas(self, event=None):
        """Busca receitas pelos ingredientes"""
        ingredientes = self.search_entry.get().strip()
        if not ingredientes:
            messagebox.showwarning("Atenção", "Digite ingredientes para buscar!")
            return
            
        # Buscar em thread separada
        threading.Thread(target=self.processar_busca, args=(ingredientes,), daemon=True).start()
    
    def processar_busca(self, ingredientes):
        """Processa busca de receitas"""
        try:
            from core_logic.sistema_rag import find_recipes_by_ingredient
            
            receitas_texto = find_recipes_by_ingredient(ingredientes, None, "interface_grafica")
            
            # Converter para lista de receitas
            from main import extrair_receitas_do_texto
            self.receitas_lista = extrair_receitas_do_texto(receitas_texto)
            
            # Atualizar interface na thread principal
            self.root.after(0, self.mostrar_receitas_encontradas)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar receitas: {e}")
    
    def mostrar_receitas_encontradas(self):
        """Mostra as receitas encontradas"""
        # Limpar frame anterior
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        if not self.receitas_lista:
            no_recipes_label = tk.Label(self.result_frame, 
                                      text="❌ Nenhuma receita encontrada", 
                                      font=('Arial', 12), 
                                      bg='white', 
                                      fg='#f44336')
            no_recipes_label.pack(pady=20)
            return
        
        # Criar lista de seleção
        title_label = tk.Label(self.result_frame, 
                             text="🍽️ Receitas Encontradas:", 
                             font=('Arial', 12, 'bold'), 
                             bg='white', 
                             fg='#333')
        title_label.pack(pady=(0, 10))
        
        self.recipe_listbox = tk.Listbox(self.result_frame, 
                                        font=('Arial', 11), 
                                        height=6,
                                        bg='#f8f8f8')
        self.recipe_listbox.pack(fill=tk.X, pady=5)
        
        for i, receita in enumerate(self.receitas_lista):
            nome = receita.get('nome', f'Receita {i+1}')
            self.recipe_listbox.insert(tk.END, f"{i+1}. {nome}")
        
        # Botão para cozinhar
        cook_button = tk.Button(self.result_frame, 
                              text="👨‍🍳 Começar a Cozinhar!", 
                              font=('Arial', 11, 'bold'), 
                              bg='#4CAF50', 
                              fg='white', 
                              relief=tk.FLAT,
                              command=self.iniciar_cozinha)
        cook_button.pack(pady=10)
    
    def iniciar_cozinha(self):
        """Inicia a interface de cozinha passo a passo"""
        if not hasattr(self, 'recipe_listbox') or not self.recipe_listbox.curselection():
            messagebox.showwarning("Atenção", "Selecione uma receita!")
            return
            
        indice = self.recipe_listbox.curselection()[0]
        self.receita_atual = self.receitas_lista[indice]
        self.criar_interface_cozinha()
    
    def criar_interface_cozinha(self):
        """Cria interface de cozinha passo a passo"""
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        nome_receita = self.receita_atual.get('nome', 'Receita')
        
        # Novo cabeçalho
        header_frame = tk.Frame(self.root, bg='#4CAF50', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text=f"👨‍🍳 Cozinhando: {nome_receita}", 
                              font=('Arial', 16, 'bold'), 
                              bg='#4CAF50', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba Ingredientes
        self.criar_aba_ingredientes(notebook)
        
        # Aba Modo de Preparo
        self.criar_aba_preparo(notebook)
        
        # Aba Informações
        self.criar_aba_informacoes(notebook)
    
    def criar_aba_ingredientes(self, notebook):
        """Cria aba com ingredientes"""
        frame = tk.Frame(notebook, bg='white')
        notebook.add(frame, text='🥬 Ingredientes')
        
        # Extrair ingredientes do texto
        texto = self.receita_atual.get('texto_completo', '')
        ingredientes = self.extrair_ingredientes(texto)
        
        # Título
        title_label = tk.Label(frame, 
                             text="🥬 INGREDIENTES NECESSÁRIOS:", 
                             font=('Arial', 14, 'bold'), 
                             bg='white', 
                             fg='#333')
        title_label.pack(pady=10)
        
        # Lista com checkboxes
        self.ingredientes_vars = []
        
        canvas = tk.Canvas(frame, bg='white')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        for i, ingrediente in enumerate(ingredientes):
            var = tk.BooleanVar()
            self.ingredientes_vars.append(var)
            
            cb = tk.Checkbutton(scrollable_frame, 
                               text=f"{i+1}. {ingrediente}", 
                               variable=var,
                               font=('Arial', 11),
                               bg='white',
                               anchor='w')
            cb.pack(fill=tk.X, padx=20, pady=2)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
    
    def criar_aba_preparo(self, notebook):
        """Cria aba com modo de preparo"""
        frame = tk.Frame(notebook, bg='white')
        notebook.add(frame, text='👨‍🍳 Preparo')
        
        # Extrair passos
        texto = self.receita_atual.get('texto_completo', '')
        passos = self.extrair_modo_preparo(texto)
        
        # Área de texto com scroll
        text_area = scrolledtext.ScrolledText(frame, 
                                            wrap=tk.WORD, 
                                            font=('Arial', 12), 
                                            bg='#f8f8f8',
                                            padx=15,
                                            pady=15)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Inserir conteúdo formatado
        text_area.insert(tk.END, "👨‍🍳 MODO DE PREPARO:\n\n")
        
        for i, passo in enumerate(passos, 1):
            text_area.insert(tk.END, f"PASSO {i}:\n{passo}\n\n")
        
        text_area.config(state=tk.DISABLED)  # Somente leitura
    
    def criar_aba_informacoes(self, notebook):
        """Cria aba com informações adicionais"""
        frame = tk.Frame(notebook, bg='white')
        notebook.add(frame, text='📊 Informações')
        
        # Área de texto
        text_area = scrolledtext.ScrolledText(frame, 
                                            wrap=tk.WORD, 
                                            font=('Arial', 11), 
                                            bg='#f8f8f8')
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Mostrar texto completo da receita
        texto_completo = self.receita_atual.get('texto_completo', '')
        text_area.insert(tk.END, texto_completo)
        text_area.config(state=tk.DISABLED)
    
    def extrair_ingredientes(self, texto):
        """Extrai lista de ingredientes do texto"""
        import re
        ingredientes = []
        
        linhas = texto.split('\\n')
        capturando = False
        
        for linha in linhas:
            linha = linha.strip()
            if 'INGREDIENTES' in linha.upper():
                capturando = True
                continue
            elif any(palavra in linha.upper() for palavra in ['MODO', 'PREPARO']):
                break
            elif capturando and linha.startswith('-'):
                ingredientes.append(linha[1:].strip())
        
        return ingredientes if ingredientes else ['Ingredientes não especificados']
    
    def extrair_modo_preparo(self, texto):
        """Extrai passos do modo de preparo"""
        import re
        passos = []
        
        linhas = texto.split('\\n')
        capturando = False
        
        for linha in linhas:
            linha = linha.strip()
            if any(palavra in linha.upper() for palavra in ['MODO', 'PREPARO']):
                capturando = True
                continue
            elif capturando and linha and linha[0].isdigit():
                passo = re.sub(r'^\\d+\\.\\s*', '', linha)
                passos.append(passo)
        
        return passos if passos else ['Modo de preparo não especificado']
    
    def run(self):
        """Executa a interface"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass

def abrir_interface_passo_a_passo(receitas_lista=None):
    """Função para abrir a interface de fora"""
    app = InterfacePassoAPasso(receitas_lista)
    app.run()

if __name__ == "__main__":
    abrir_interface_passo_a_passo()