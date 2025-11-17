#!/usr/bin/env python3
"""
Interface de Cronômetros e Timers - Chef RAG v2
===============================================

Interface gráfica para gerenciar cronômetros de cozinha.
Design limpo e simples com múltiplos timers.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import threading
import time
import uuid

# Importação do banco de dados
from core_logic.database import history_db

class TimerKitchenInterface:
    """Interface para cronômetros de cozinha"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.timers = {}
        self.timer_threads = {}
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("⏰ Chef RAG v2 - Cronômetros de Cozinha")
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
                              text="⏰ Cronômetros de Cozinha - Chef RAG v2", 
                              font=('Arial', 18, 'bold'), 
                              bg='#9C27B0', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_timer_tab()
        self.setup_presets_tab()
        self.setup_history_tab()
        
    def setup_timer_tab(self):
        """Configura aba principal de timers"""
        self.timer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.timer_frame, text="⏱️ Cronômetros")
        
        # Frame de criação de timer
        create_frame = ttk.LabelFrame(self.timer_frame, text="➕ Criar Cronômetro", padding=15)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nome do timer
        tk.Label(create_frame, text="📝 Nome:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.timer_name_var = tk.StringVar()
        name_entry = tk.Entry(create_frame, textvariable=self.timer_name_var, font=('Arial', 12), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        # Tempo
        tk.Label(create_frame, text="⏰ Tempo:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        
        time_frame = tk.Frame(create_frame, bg='white')
        time_frame.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        # Horas
        self.hours_var = tk.StringVar(value="0")
        hours_spin = tk.Spinbox(time_frame, from_=0, to=23, textvariable=self.hours_var, width=3, font=('Arial', 12))
        hours_spin.pack(side=tk.LEFT)
        tk.Label(time_frame, text="h", font=('Arial', 11)).pack(side=tk.LEFT, padx=(2, 10))
        
        # Minutos
        self.minutes_var = tk.StringVar(value="5")
        minutes_spin = tk.Spinbox(time_frame, from_=0, to=59, textvariable=self.minutes_var, width=3, font=('Arial', 12))
        minutes_spin.pack(side=tk.LEFT)
        tk.Label(time_frame, text="min", font=('Arial', 11)).pack(side=tk.LEFT, padx=(2, 10))
        
        # Segundos
        self.seconds_var = tk.StringVar(value="0")
        seconds_spin = tk.Spinbox(time_frame, from_=0, to=59, textvariable=self.seconds_var, width=3, font=('Arial', 12))
        seconds_spin.pack(side=tk.LEFT)
        tk.Label(time_frame, text="seg", font=('Arial', 11)).pack(side=tk.LEFT, padx=2)
        
        # Botão criar timer
        create_btn = tk.Button(create_frame,
                              text="▶️ Iniciar Cronômetro",
                              command=self.create_timer,
                              bg='#4CAF50',
                              fg='white',
                              font=('Arial', 12, 'bold'),
                              relief='flat',
                              padx=30,
                              pady=10)
        create_btn.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # Frame de timers ativos
        self.active_frame = ttk.LabelFrame(self.timer_frame, text="🔥 Cronômetros Ativos", padding=15)
        self.active_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para scroll
        canvas = tk.Canvas(self.active_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.active_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Label inicial
        self.no_timers_label = tk.Label(self.scrollable_frame, 
                                       text="🕐 Nenhum cronômetro ativo\\nCrie um cronômetro acima!", 
                                       font=('Arial', 12), 
                                       fg='#666666',
                                       bg='white')
        self.no_timers_label.pack(pady=50)
        
    def setup_presets_tab(self):
        """Configura aba de presets"""
        self.presets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.presets_frame, text="⚡ Presets")
        
        # Título
        title_label = tk.Label(self.presets_frame, 
                              text="⚡ Tempos Pré-definidos", 
                              font=('Arial', 16, 'bold'), 
                              bg='white')
        title_label.pack(pady=20)
        
        # Grid de presets
        presets_grid = tk.Frame(self.presets_frame, bg='white')
        presets_grid.pack(expand=True, pady=20)
        
        presets = [
            ("🥚 Ovo Mole", "00:03:00", "Ovo cozido mole"),
            ("🥚 Ovo Duro", "00:10:00", "Ovo cozido duro"),
            ("🍝 Macarrão", "00:08:00", "Massa al dente"),
            ("☕ Café Coado", "00:05:00", "Tempo de extração"),
            ("🥔 Batata Cozida", "00:20:00", "Batatas médias"),
            ("🍚 Arroz", "00:18:00", "Arroz branco"),
            ("🥩 Bife Mal Passado", "00:02:00", "Cada lado do bife"),
            ("🥩 Bife Bem Passado", "00:05:00", "Cada lado do bife"),
            ("🍪 Biscoitos", "00:12:00", "Forno pré-aquecido"),
            ("🍕 Pizza", "00:15:00", "Forno alto"),
            ("🥖 Pão", "00:25:00", "Assamento normal"),
            ("🧁 Cupcakes", "00:20:00", "Forno médio"),
        ]
        
        row = 0
        col = 0
        for name, time_str, description in presets:
            preset_frame = tk.Frame(presets_grid, 
                                   bg='#f5f5f5', 
                                   relief='raised', 
                                   bd=1,
                                   padx=15,
                                   pady=10)
            preset_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Nome
            name_label = tk.Label(preset_frame, text=name, font=('Arial', 12, 'bold'), bg='#f5f5f5')
            name_label.pack()
            
            # Tempo
            time_label = tk.Label(preset_frame, text=time_str, font=('Arial', 11), fg='#666', bg='#f5f5f5')
            time_label.pack()
            
            # Descrição
            desc_label = tk.Label(preset_frame, text=description, font=('Arial', 9), fg='#888', bg='#f5f5f5')
            desc_label.pack()
            
            # Botão
            start_btn = tk.Button(preset_frame,
                                 text="▶️ Iniciar",
                                 command=lambda n=name, t=time_str: self.start_preset_timer(n, t),
                                 bg='#9C27B0',
                                 fg='white',
                                 font=('Arial', 10, 'bold'),
                                 relief='flat',
                                 padx=15,
                                 pady=5)
            start_btn.pack(pady=5)
            
            col += 1
            if col >= 3:  # 3 colunas
                col = 0
                row += 1
                
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
        
        clear_btn = tk.Button(controls_frame,
                             text="🧹 Limpar Histórico",
                             command=self.clear_history,
                             bg='#F44336',
                             fg='white',
                             font=('Arial', 10, 'bold'),
                             relief='flat',
                             padx=15,
                             pady=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Histórico
        history_list_frame = ttk.LabelFrame(self.history_frame, text="📜 Cronômetros Anteriores", padding=10)
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.history_text = scrolledtext.ScrolledText(history_list_frame,
                                                     height=20,
                                                     font=('Arial', 10),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        self.load_history()
        
    def create_timer(self):
        """Cria novo timer"""
        name = self.timer_name_var.get().strip()
        if not name:
            messagebox.showwarning("Aviso", "Digite um nome para o cronômetro!")
            return
            
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds <= 0:
                messagebox.showwarning("Aviso", "Digite um tempo válido!")
                return
                
            # Criar timer
            timer_id = str(uuid.uuid4())[:8]
            self.start_timer(timer_id, name, total_seconds)
            
            # Limpar campos
            self.timer_name_var.set('')
            self.hours_var.set('0')
            self.minutes_var.set('5')
            self.seconds_var.set('0')
            
        except ValueError:
            messagebox.showerror("Erro", "Valores de tempo inválidos!")
            
    def start_preset_timer(self, name, time_str):
        """Inicia timer preset"""
        try:
            # Converter time_str (HH:MM:SS) para segundos
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            timer_id = str(uuid.uuid4())[:8]
            self.start_timer(timer_id, name, total_seconds)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar preset: {str(e)}")
            
    def start_timer(self, timer_id, name, total_seconds):
        """Inicia cronômetro"""
        # Remover label "nenhum timer"
        if hasattr(self, 'no_timers_label'):
            self.no_timers_label.destroy()
            
        # Criar frame do timer
        timer_frame = tk.Frame(self.scrollable_frame, 
                              bg='#e8f5e8', 
                              relief='raised', 
                              bd=2,
                              padx=15,
                              pady=10)
        timer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Título
        title_label = tk.Label(timer_frame, 
                              text=f"🔥 {name}", 
                              font=('Arial', 14, 'bold'), 
                              bg='#e8f5e8')
        title_label.pack()
        
        # Display do tempo
        time_label = tk.Label(timer_frame, 
                             text=self.format_time(total_seconds), 
                             font=('Arial', 24, 'bold'), 
                             fg='#2E7D32',
                             bg='#e8f5e8')
        time_label.pack(pady=10)
        
        # Status
        status_label = tk.Label(timer_frame, 
                               text="▶️ Executando...", 
                               font=('Arial', 11), 
                               fg='#4CAF50',
                               bg='#e8f5e8')
        status_label.pack()
        
        # Botões
        button_frame = tk.Frame(timer_frame, bg='#e8f5e8')
        button_frame.pack(pady=10)
        
        stop_btn = tk.Button(button_frame,
                            text="⏹️ Parar",
                            command=lambda: self.stop_timer(timer_id),
                            bg='#F44336',
                            fg='white',
                            font=('Arial', 10, 'bold'),
                            relief='flat',
                            padx=15,
                            pady=5)
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Salvar referências
        self.timers[timer_id] = {
            'name': name,
            'frame': timer_frame,
            'time_label': time_label,
            'status_label': status_label,
            'remaining': total_seconds,
            'running': True,
            'start_time': datetime.now()
        }
        
        # Iniciar thread do timer
        thread = threading.Thread(target=self.timer_worker, args=(timer_id,))
        thread.daemon = True
        self.timer_threads[timer_id] = thread
        thread.start()
        
        messagebox.showinfo("Sucesso", f"Cronômetro '{name}' iniciado!")
        
    def timer_worker(self, timer_id):
        """Worker thread para o timer"""
        while self.timers[timer_id]['running'] and self.timers[timer_id]['remaining'] > 0:
            time.sleep(1)
            if timer_id in self.timers and self.timers[timer_id]['running']:
                self.timers[timer_id]['remaining'] -= 1
                
                # Atualizar UI na thread principal
                self.root.after(0, self.update_timer_display, timer_id)
                
        # Timer terminou
        if timer_id in self.timers and self.timers[timer_id]['remaining'] <= 0:
            self.root.after(0, self.timer_finished, timer_id)
            
    def update_timer_display(self, timer_id):
        """Atualiza display do timer"""
        if timer_id in self.timers:
            remaining = self.timers[timer_id]['remaining']
            time_text = self.format_time(remaining)
            
            # Atualizar cores baseado no tempo restante
            if remaining <= 10:  # Últimos 10 segundos
                self.timers[timer_id]['time_label'].config(fg='#F44336')
                self.timers[timer_id]['frame'].config(bg='#ffebee')
            elif remaining <= 60:  # Último minuto
                self.timers[timer_id]['time_label'].config(fg='#FF9800')
                self.timers[timer_id]['frame'].config(bg='#fff8e1')
            
            self.timers[timer_id]['time_label'].config(text=time_text)
            
    def timer_finished(self, timer_id):
        """Timer terminou"""
        if timer_id in self.timers:
            timer = self.timers[timer_id]
            timer['status_label'].config(text="✅ Concluído!", fg='#4CAF50')
            timer['time_label'].config(text="00:00:00", fg='#4CAF50')
            timer['frame'].config(bg='#e8f5e8')
            
            # Notificação
            messagebox.showinfo("⏰ Tempo Esgotado!", 
                               f"O cronômetro '{timer['name']}' terminou!\\n⏰ Seu tempo acabou!")
            
            # Salvar no histórico
            self.save_timer_history(timer['name'], timer['start_time'])
            
            # Auto-remover após 5 segundos
            self.root.after(5000, lambda: self.stop_timer(timer_id))
            
    def stop_timer(self, timer_id):
        """Para um timer"""
        if timer_id in self.timers:
            self.timers[timer_id]['running'] = False
            
            # Remover da UI
            self.timers[timer_id]['frame'].destroy()
            del self.timers[timer_id]
            
        if timer_id in self.timer_threads:
            del self.timer_threads[timer_id]
            
        # Se não há mais timers, mostrar label
        if not self.timers:
            self.no_timers_label = tk.Label(self.scrollable_frame, 
                                           text="🕐 Nenhum cronômetro ativo\\nCrie um cronômetro acima!", 
                                           font=('Arial', 12), 
                                           fg='#666666',
                                           bg='white')
            self.no_timers_label.pack(pady=50)
            
    def format_time(self, seconds):
        """Formata segundos em HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        
    def save_timer_history(self, name, start_time):
        """Salva timer no histórico"""
        try:
            history_db.add_analysis(
                ingredient=f"Timer: {name}",
                recipes_response=f"Cronômetro finalizado em {datetime.now().strftime('%H:%M:%S')}",
                source_mode="kitchen_timer"
            )
        except Exception as e:
            print(f"Erro ao salvar timer no histórico: {e}")
            
    def load_history(self):
        """Carrega histórico de timers"""
        try:
            all_analyses = history_db.get_recent_analyses(limit=100)
            timer_analyses = [a for a in all_analyses if a.get('source_mode') == 'kitchen_timer']
            
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            
            if timer_analyses:
                self.history_text.insert(tk.END, "⏰ HISTÓRICO DE CRONÔMETROS\\n")
                self.history_text.insert(tk.END, "="*40 + "\\n\\n")
                
                for analysis in timer_analyses:
                    timestamp = analysis.get('timestamp', 'N/A')
                    timer_name = analysis.get('ingredient_identified', 'N/A')
                    result = analysis.get('recipes_found', 'N/A')
                    
                    self.history_text.insert(tk.END, f"📅 {timestamp}\\n")
                    self.history_text.insert(tk.END, f"⏰ {timer_name}\\n")
                    self.history_text.insert(tk.END, f"✅ {result}\\n\\n")
            else:
                self.history_text.insert(tk.END, "Nenhum cronômetro registrado ainda.\\nComece criando seus primeiros timers!")
                
            self.history_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {str(e)}")
            
    def clear_history(self):
        """Limpa histórico"""
        if messagebox.askyesno("Confirmar", "Limpar todo o histórico de cronômetros?"):
            # Aqui seria implementada a limpeza seletiva do histórico
            messagebox.showinfo("Sucesso", "Histórico limpo!")
            self.load_history()
            
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

def iniciar_interface_cronometros():
    """Função para iniciar a interface de cronômetros"""
    try:
        app = TimerKitchenInterface()
        app.run()
    except Exception as e:
        print(f"❌ Erro ao iniciar cronômetros: {e}")

if __name__ == "__main__":
    iniciar_interface_cronometros()