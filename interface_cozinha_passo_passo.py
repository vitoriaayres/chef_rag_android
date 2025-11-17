#!/usr/bin/env python3
"""
Interface de Cozinha Passo a Passo
Guia o usuário durante o processo de cozimento de uma receita específica
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
from datetime import datetime, timedelta
from core_logic.database import history_db

class InterfaceCozinhaPP:
    def __init__(self, dados_receita):
        """
        Inicializa a interface de cozinha com dados da receita
        
        Args:
            dados_receita (dict): Dados estruturados da receita
        """
        self.dados_receita = dados_receita
        self.root = tk.Tk()
        self.passo_atual = 0
        self.cronometros_ativos = {}
        self.janela_cronometro = None
        
        self.configurar_janela()
        self.criar_interface()
        
    def configurar_janela(self):
        """Configura a janela principal"""
        self.root.title(f"👨‍🍳 Cozinhando: {self.dados_receita['titulo']}")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        # Configurar grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Fontes
        self.font_title = font.Font(family="Arial", size=14, weight="bold")
        self.font_step = font.Font(family="Arial", size=12)
        self.font_button = font.Font(family="Arial", size=11, weight="bold")
        
    def criar_interface(self):
        """Cria todos os elementos da interface"""
        self.criar_cabecalho()
        self.criar_area_principal()
        
    def criar_cabecalho(self):
        """Cria o cabeçalho com informações da receita"""
        frame_header = tk.Frame(self.root, bg="#34495e", pady=10)
        frame_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,0))
        frame_header.grid_columnconfigure(1, weight=1)
        
        # Título da receita
        titulo = self.dados_receita['titulo'][:50] + "..." if len(self.dados_receita['titulo']) > 50 else self.dados_receita['titulo']
        tk.Label(frame_header, text=f"👨‍🍳 {titulo}", 
                font=self.font_title, fg="white", bg="#34495e").grid(row=0, column=0, columnspan=3, pady=(0,5))
        
        # Informações da receita
        tk.Label(frame_header, text=f"⏰ {self.dados_receita['tempo_preparo']}", 
                font=("Arial", 10), fg="#ecf0f1", bg="#34495e").grid(row=1, column=0, sticky="w", padx=(10,20))
        
        tk.Label(frame_header, text=f"🍽️ {self.dados_receita['porcoes']}", 
                font=("Arial", 10), fg="#ecf0f1", bg="#34495e").grid(row=1, column=1, sticky="w", padx=(0,20))
        
        tk.Label(frame_header, text=f"📊 Dificuldade: {self.dados_receita['dificuldade']}", 
                font=("Arial", 10), fg="#ecf0f1", bg="#34495e").grid(row=1, column=2, sticky="w")
        
    def criar_area_principal(self):
        """Cria a área principal com abas"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background="#34495e")
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Aba Ingredientes
        self.criar_aba_ingredientes()
        
        # Aba Passo a Passo
        self.criar_aba_passo_passo()
        
        # Aba Cronômetros
        self.criar_aba_cronometros()
        
    def criar_aba_ingredientes(self):
        """Cria a aba com lista de ingredientes"""
        frame_ingredientes = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(frame_ingredientes, text="📝 Ingredientes")
        
        # Título
        tk.Label(frame_ingredientes, text="📝 LISTA DE INGREDIENTES", 
                font=self.font_title, bg="#ecf0f1", fg="#2c3e50").pack(pady=20)
        
        # Frame scrollable para ingredientes
        canvas = tk.Canvas(frame_ingredientes, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(frame_ingredientes, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Lista de ingredientes com checkboxes
        self.ingredientes_vars = []
        for i, ingrediente in enumerate(self.dados_receita['ingredientes']):
            var = tk.BooleanVar()
            self.ingredientes_vars.append(var)
            
            frame_item = tk.Frame(scrollable_frame, bg="white", relief="raised", bd=1)
            frame_item.pack(fill="x", padx=20, pady=5)
            
            checkbox = tk.Checkbutton(frame_item, variable=var, text=f"✓ {ingrediente}", 
                                    font=self.font_step, bg="white", fg="#2c3e50",
                                    wraplength=600, justify="left", anchor="w")
            checkbox.pack(fill="x", padx=10, pady=8)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20,0), pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
    def criar_aba_passo_passo(self):
        """Cria a aba com instruções passo a passo"""
        frame_passos = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(frame_passos, text="👨‍🍳 Passo a Passo")
        
        # Título e contador
        frame_titulo = tk.Frame(frame_passos, bg="#ecf0f1")
        frame_titulo.pack(fill="x", pady=20)
        
        self.label_passo_titulo = tk.Label(frame_titulo, text=f"PASSO 1 DE {len(self.dados_receita['modo_preparo'])}", 
                                          font=self.font_title, bg="#ecf0f1", fg="#2c3e50")
        self.label_passo_titulo.pack()
        
        # Área do passo atual
        frame_passo_atual = tk.Frame(frame_passos, bg="white", relief="raised", bd=2)
        frame_passo_atual.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Texto do passo
        self.texto_passo = tk.Text(frame_passo_atual, wrap=tk.WORD, font=self.font_step, 
                                  bg="white", fg="#2c3e50", relief="flat", bd=10)
        self.texto_passo.pack(fill="both", expand=True)
        
        # Mostrar primeiro passo
        self.mostrar_passo_atual()
        
        # Botões de navegação
        frame_navegacao = tk.Frame(frame_passos, bg="#ecf0f1")
        frame_navegacao.pack(fill="x", pady=20)
        
        self.btn_anterior = tk.Button(frame_navegacao, text="⬅️ Passo Anterior", 
                                     command=self.passo_anterior, font=self.font_button,
                                     bg="#95a5a6", fg="white", relief="raised", bd=2)
        self.btn_anterior.pack(side="left", padx=(20,10))
        
        self.btn_proximo = tk.Button(frame_navegacao, text="➡️ Próximo Passo", 
                                    command=self.proximo_passo, font=self.font_button,
                                    bg="#3498db", fg="white", relief="raised", bd=2)
        self.btn_proximo.pack(side="right", padx=(10,20))
        
        self.btn_cronometro = tk.Button(frame_navegacao, text="⏰ Cronômetro", 
                                       command=self.abrir_cronometro, font=self.font_button,
                                       bg="#e74c3c", fg="white", relief="raised", bd=2)
        self.btn_cronometro.pack(side="right", padx=10)
        
        # Atualizar estado dos botões
        self.atualizar_botoes_navegacao()
        
    def criar_aba_cronometros(self):
        """Cria a aba para gerenciar cronômetros"""
        frame_cronometros = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(frame_cronometros, text="⏰ Cronômetros")
        
        tk.Label(frame_cronometros, text="⏰ CRONÔMETROS ATIVOS", 
                font=self.font_title, bg="#ecf0f1", fg="#2c3e50").pack(pady=20)
        
        # Frame para cronômetros
        self.frame_cronometros_lista = tk.Frame(frame_cronometros, bg="#ecf0f1")
        self.frame_cronometros_lista.pack(fill="both", expand=True, padx=20)
        
        # Adicionar cronômetro rápido
        frame_adicionar = tk.Frame(frame_cronometros, bg="#ecf0f1")
        frame_adicionar.pack(fill="x", padx=20, pady=20)
        
        tk.Label(frame_adicionar, text="⏱️ Novo cronômetro (minutos):", 
                font=self.font_step, bg="#ecf0f1", fg="#2c3e50").pack(side="left")
        
        self.entry_cronometro = tk.Entry(frame_adicionar, font=self.font_step, width=10)
        self.entry_cronometro.pack(side="left", padx=10)
        
        tk.Button(frame_adicionar, text="▶️ Iniciar", command=self.iniciar_cronometro,
                 font=self.font_button, bg="#27ae60", fg="white").pack(side="left", padx=5)
        
    def mostrar_passo_atual(self):
        """Mostra o passo atual na interface"""
        if not self.dados_receita['modo_preparo']:
            self.texto_passo.delete(1.0, tk.END)
            self.texto_passo.insert(tk.END, "❌ Nenhum passo encontrado nesta receita.")
            return
            
        passo_texto = self.dados_receita['modo_preparo'][self.passo_atual]
        
        # Atualizar título
        self.label_passo_titulo.config(text=f"PASSO {self.passo_atual + 1} DE {len(self.dados_receita['modo_preparo'])}")
        
        # Atualizar texto
        self.texto_passo.delete(1.0, tk.END)
        self.texto_passo.insert(tk.END, f"👨‍🍳 {passo_texto}")
        
        # Destacar palavras importantes
        self.destacar_palavras_importantes(passo_texto)
        
    def destacar_palavras_importantes(self, texto):
        """Destaca palavras importantes no passo atual"""
        palavras_tempo = ["minuto", "minutos", "hora", "horas", "segundo", "segundos"]
        palavras_acao = ["misture", "mexe", "doure", "frite", "cozinhe", "ferva", "tempere"]
        
        # Configurar tags
        self.texto_passo.tag_configure("tempo", foreground="#e74c3c", font=("Arial", 12, "bold"))
        self.texto_passo.tag_configure("acao", foreground="#27ae60", font=("Arial", 12, "bold"))
        
        texto_lower = texto.lower()
        
        # Destacar palavras de tempo
        for palavra in palavras_tempo:
            start = texto_lower.find(palavra)
            while start != -1:
                end = start + len(palavra)
                start_index = f"1.{start}"
                end_index = f"1.{end}"
                self.texto_passo.tag_add("tempo", start_index, end_index)
                start = texto_lower.find(palavra, end)
        
        # Destacar palavras de ação
        for palavra in palavras_acao:
            start = texto_lower.find(palavra)
            while start != -1:
                end = start + len(palavra)
                start_index = f"1.{start}"
                end_index = f"1.{end}"
                self.texto_passo.tag_add("acao", start_index, end_index)
                start = texto_lower.find(palavra, end)
    
    def proximo_passo(self):
        """Avança para o próximo passo"""
        if self.passo_atual < len(self.dados_receita['modo_preparo']) - 1:
            self.passo_atual += 1
            self.mostrar_passo_atual()
            self.atualizar_botoes_navegacao()
        else:
            self.finalizar_receita()
    
    def passo_anterior(self):
        """Volta ao passo anterior"""
        if self.passo_atual > 0:
            self.passo_atual -= 1
            self.mostrar_passo_atual()
            self.atualizar_botoes_navegacao()
    
    def atualizar_botoes_navegacao(self):
        """Atualiza o estado dos botões de navegação"""
        # Botão anterior
        if self.passo_atual == 0:
            self.btn_anterior.config(state="disabled", bg="#bdc3c7")
        else:
            self.btn_anterior.config(state="normal", bg="#95a5a6")
        
        # Botão próximo
        if self.passo_atual >= len(self.dados_receita['modo_preparo']) - 1:
            self.btn_proximo.config(text="🏁 Finalizar", bg="#e67e22")
        else:
            self.btn_proximo.config(text="➡️ Próximo Passo", bg="#3498db")
    
    def abrir_cronometro(self):
        """Abre janela de cronômetro para o passo atual"""
        try:
            from interface_cronometros_cozinha import iniciar_interface_cronometros
            iniciar_interface_cronometros()
        except ImportError:
            self.cronometro_simples()
    
    def cronometro_simples(self):
        """Cronômetro simples integrado"""
        if self.janela_cronometro:
            self.janela_cronometro.lift()
            return
            
        self.janela_cronometro = tk.Toplevel(self.root)
        self.janela_cronometro.title("⏰ Cronômetro")
        self.janela_cronometro.geometry("300x200")
        self.janela_cronometro.configure(bg="#2c3e50")
        
        tk.Label(self.janela_cronometro, text="⏰ Cronômetro Rápido", 
                font=self.font_title, fg="white", bg="#2c3e50").pack(pady=20)
        
        frame_tempo = tk.Frame(self.janela_cronometro, bg="#2c3e50")
        frame_tempo.pack(pady=20)
        
        tk.Label(frame_tempo, text="Minutos:", fg="white", bg="#2c3e50").pack(side="left")
        entry_minutos = tk.Entry(frame_tempo, width=10, font=self.font_step)
        entry_minutos.pack(side="left", padx=10)
        
        def iniciar_timer():
            try:
                minutos = int(entry_minutos.get())
                threading.Thread(target=self.executar_cronometro, args=(minutos,), daemon=True).start()
                if self.janela_cronometro:
                    self.janela_cronometro.destroy()
                    self.janela_cronometro = None
            except ValueError:
                messagebox.showerror("Erro", "Digite um número válido de minutos")
        
        tk.Button(frame_tempo, text="▶️ Iniciar", command=iniciar_timer,
                 font=self.font_button, bg="#27ae60", fg="white").pack(side="left", padx=10)
        
        self.janela_cronometro.protocol("WM_DELETE_WINDOW", lambda: setattr(self, 'janela_cronometro', None))
    
    def executar_cronometro(self, minutos):
        """Executa cronômetro em thread separada"""
        segundos_total = minutos * 60
        
        for i in range(segundos_total, -1, -1):
            mins, secs = divmod(i, 60)
            self.root.title(f"👨‍🍳 Cozinhando: {self.dados_receita['titulo']} - ⏰ {mins:02d}:{secs:02d}")
            time.sleep(1)
        
        # Cronômetro finalizado
        self.root.title(f"👨‍🍳 Cozinhando: {self.dados_receita['titulo']}")
        messagebox.showinfo("⏰ Tempo!", f"Cronômetro de {minutos} minutos finalizado!")
    
    def iniciar_cronometro(self):
        """Inicia novo cronômetro da aba"""
        try:
            minutos = int(self.entry_cronometro.get())
            if minutos <= 0:
                raise ValueError
                
            cronometro_id = f"cronometro_{len(self.cronometros_ativos) + 1}"
            
            # Adicionar à interface
            frame_cronometro = tk.Frame(self.frame_cronometros_lista, bg="white", relief="raised", bd=1)
            frame_cronometro.pack(fill="x", pady=5)
            
            label_cronometro = tk.Label(frame_cronometro, text=f"⏰ {minutos} minutos - Iniciando...", 
                                       font=self.font_step, bg="white")
            label_cronometro.pack(side="left", padx=10, pady=5)
            
            # Iniciar em thread
            threading.Thread(target=self.executar_cronometro_na_lista, 
                           args=(cronometro_id, minutos, label_cronometro, frame_cronometro), 
                           daemon=True).start()
            
            self.entry_cronometro.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido de minutos")
    
    def executar_cronometro_na_lista(self, cronometro_id, minutos, label, frame):
        """Executa cronômetro específico"""
        segundos_total = minutos * 60
        
        for i in range(segundos_total, -1, -1):
            mins, secs = divmod(i, 60)
            label.config(text=f"⏰ {mins:02d}:{secs:02d} restantes")
            time.sleep(1)
        
        # Cronômetro finalizado
        label.config(text="🔔 TEMPO! Finalizado", fg="#e74c3c")
        messagebox.showinfo("⏰ Cronômetro", f"Cronômetro de {minutos} minutos finalizado!")
    
    def finalizar_receita(self):
        """Finaliza o processo de cozimento"""
        resultado = messagebox.askyesno("🏁 Receita Finalizada!", 
                                       "Parabéns! Você completou a receita!\n\n🤔 Como ficou o resultado?\n\nClique 'Sim' se ficou boa ou 'Não' se quer tentar novamente.")
        
        if resultado:
            messagebox.showinfo("👨‍🍳 Sucesso!", "Que ótimo! Esperamos que você tenha se divertido cozinhando! 🎉")
        else:
            messagebox.showinfo("🔄 Tente Novamente", "Não desista! A prática leva à perfeição! 💪")
        
        # Salvar no histórico que a receita foi executada
        try:
            history_db.add_analysis(
                ingredient=self.dados_receita['titulo'],
                recipes_response=f"Receita executada: {self.dados_receita['titulo']}",
                source_mode="receita_executada"
            )
        except:
            pass
        
        self.root.quit()
    
    def executar(self):
        """Executa a interface"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Erro na interface de cozinha: {e}")
        finally:
            try:
                self.root.destroy()
            except:
                pass

def abrir_interface_cozinha(dados_receita):
    """Abre a interface de cozinha com os dados da receita"""
    try:
        print(f"🧑‍🍳 Abrindo interface de cozinha para: {dados_receita['titulo']}")
        interface = InterfaceCozinhaPP(dados_receita)
        interface.executar()
    except Exception as e:
        print(f"❌ Erro ao abrir interface de cozinha: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Dados de teste
    dados_teste = {
        'titulo': 'Receita de Teste',
        'ingredientes': ['1 xícara de farinha', '2 ovos', '1/2 xícara de leite'],
        'modo_preparo': [
            'Misture a farinha com os ovos',
            'Adicione o leite gradualmente', 
            'Cozinhe em fogo médio por 10 minutos'
        ],
        'tempo_preparo': '30 minutos',
        'porcoes': '4 porções',
        'dificuldade': 'Fácil',
        'texto_completo': 'Receita completa de teste'
    }
    
    abrir_interface_cozinha(dados_teste)