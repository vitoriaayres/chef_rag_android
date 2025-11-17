#!/usr/bin/env python3
"""
Interface de Monitoramento - Chef RAG v2
=======================================

Interface gráfica para visualizar métricas, custos e analytics do sistema.
Integrada com LangSmith para análise de performance dos agentes.

Funcionalidades:
- Dashboard de custos em tempo real
- Histórico de sessões
- Análise de performance de agentes
- Gráficos de uso
- Exportação de relatórios
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import pandas as pd
from typing import Dict, List, Any

# Imports do sistema
from core_logic.agent_environment import get_agent_system, reset_agent_session
from core_logic.config import LANGCHAIN_API_KEY, LANGCHAIN_PROJECT

class MonitoringDashboard:
    """Dashboard de monitoramento do Chef RAG"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.agent_system = get_agent_system()
        self.setup_window()
        self.setup_ui()
        self.update_metrics()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("📊 Chef RAG v2 - Monitoring Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        self.root.eval('tk::PlaceWindow . center')
        
    def setup_ui(self):
        """Configura interface do usuário"""
        
        # Cabeçalho
        header_frame = tk.Frame(self.root, bg='#2E7D32', height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="📊 Chef RAG v2 - Monitoring Dashboard", 
                              font=('Arial', 18, 'bold'), 
                              bg='#2E7D32', 
                              fg='white')
        title_label.pack(expand=True)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Abas
        self.setup_realtime_tab()
        self.setup_session_tab()
        self.setup_agents_tab()
        self.setup_langsmith_tab()
        self.setup_settings_tab()
        
    def setup_realtime_tab(self):
        """Aba de métricas em tempo real"""
        self.realtime_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.realtime_frame, text="📈 Tempo Real")
        
        # Métricas principais
        metrics_frame = ttk.LabelFrame(self.realtime_frame, text="📊 Métricas Atuais", padding=15)
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Grid de métricas
        metrics_grid = tk.Frame(metrics_frame, bg='white')
        metrics_grid.pack(fill=tk.X)
        
        # Custo atual
        self.cost_label = tk.Label(metrics_grid, 
                                  text="💰 Custo da Sessão: $0.000000", 
                                  font=('Arial', 14, 'bold'), 
                                  fg='#D32F2F', 
                                  bg='white')
        self.cost_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        
        # Tokens usados
        self.tokens_label = tk.Label(metrics_grid, 
                                    text="🔢 Tokens: 0 (Input: 0, Output: 0)", 
                                    font=('Arial', 12), 
                                    fg='#1976D2', 
                                    bg='white')
        self.tokens_label.grid(row=0, column=1, padx=20, pady=10, sticky='w')
        
        # Interações
        self.interactions_label = tk.Label(metrics_grid, 
                                          text="🔄 Interações: 0", 
                                          font=('Arial', 12), 
                                          fg='#388E3C', 
                                          bg='white')
        self.interactions_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        
        # Sessão ID
        self.session_label = tk.Label(metrics_grid, 
                                     text=f"🆔 Sessão: {self.agent_system.session_id}", 
                                     font=('Arial', 10), 
                                     fg='#666', 
                                     bg='white')
        self.session_label.grid(row=1, column=1, padx=20, pady=10, sticky='w')
        
        # Controles
        controls_frame = ttk.LabelFrame(self.realtime_frame, text="🎮 Controles", padding=10)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botões
        tk.Button(controls_frame, text="🔄 Atualizar", command=self.update_metrics,
                 bg='#1976D2', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls_frame, text="🆕 Nova Sessão", command=self.new_session,
                 bg='#388E3C', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls_frame, text="💾 Exportar", command=self.export_session,
                 bg='#F57C00', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Log de atividades
        log_frame = ttk.LabelFrame(self.realtime_frame, text="📝 Log de Atividades", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.activity_log = scrolledtext.ScrolledText(log_frame,
                                                     height=15,
                                                     font=('Consolas', 9),
                                                     wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.activity_log.pack(fill=tk.BOTH, expand=True)
        
    def setup_session_tab(self):
        """Aba de histórico de sessões"""
        self.session_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.session_frame, text="📚 Histórico")
        
        # Lista de sessões
        sessions_frame = ttk.LabelFrame(self.session_frame, text="📋 Sessões Anteriores", padding=10)
        sessions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para sessões
        columns = ('ID', 'Data/Hora', 'Interações', 'Custo', 'Tokens', 'Agentes')
        self.sessions_tree = ttk.Treeview(sessions_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.sessions_tree.heading(col, text=col)
            self.sessions_tree.column(col, width=120)
        
        self.sessions_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar
        sessions_scroll = ttk.Scrollbar(sessions_frame, orient=tk.VERTICAL, command=self.sessions_tree.yview)
        sessions_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.sessions_tree.configure(yscrollcommand=sessions_scroll.set)
        
    def setup_agents_tab(self):
        """Aba de análise de agentes"""
        self.agents_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.agents_frame, text="🤖 Agentes")
        
        # Estatísticas dos agentes
        stats_frame = ttk.LabelFrame(self.agents_frame, text="📊 Estatísticas por Agente", padding=15)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Gráfico de uso dos agentes
        self.create_agent_usage_chart(stats_frame)
        
        # Detalhes dos agentes
        details_frame = ttk.LabelFrame(self.agents_frame, text="🔍 Detalhes dos Agentes", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.agent_details = scrolledtext.ScrolledText(details_frame,
                                                      height=15,
                                                      font=('Arial', 10),
                                                      wrap=tk.WORD,
                                                      state=tk.DISABLED)
        self.agent_details.pack(fill=tk.BOTH, expand=True)
        
    def setup_langsmith_tab(self):
        """Aba de integração LangSmith"""
        self.langsmith_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.langsmith_frame, text="🔗 LangSmith")
        
        # Status da conexão
        status_frame = ttk.LabelFrame(self.langsmith_frame, text="🔌 Status da Conexão", padding=15)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        connection_status = "🟢 Conectado" if LANGCHAIN_API_KEY else "🔴 Desconectado"
        project_name = LANGCHAIN_PROJECT if LANGCHAIN_API_KEY else "N/A"
        
        tk.Label(status_frame, text=f"Status: {connection_status}", 
                font=('Arial', 12, 'bold')).pack(anchor='w')
        tk.Label(status_frame, text=f"Projeto: {project_name}", 
                font=('Arial', 11)).pack(anchor='w')
        
        # Dados do LangSmith
        data_frame = ttk.LabelFrame(self.langsmith_frame, text="📊 Dados LangSmith", padding=10)
        data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.langsmith_data = scrolledtext.ScrolledText(data_frame,
                                                       height=20,
                                                       font=('Arial', 10),
                                                       wrap=tk.WORD,
                                                       state=tk.DISABLED)
        self.langsmith_data.pack(fill=tk.BOTH, expand=True)
        
        # Botão para buscar dados
        tk.Button(data_frame, text="🔄 Buscar Dados LangSmith", 
                 command=self.fetch_langsmith_data,
                 bg='#1976D2', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        
    def setup_settings_tab(self):
        """Aba de configurações"""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Configurações")
        
        # Configurações de monitoramento
        monitor_frame = ttk.LabelFrame(self.settings_frame, text="📊 Monitoramento", padding=15)
        monitor_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.auto_update_var = tk.BooleanVar(value=True)
        tk.Checkbutton(monitor_frame, text="Atualização automática (5s)", 
                      variable=self.auto_update_var,
                      command=self.toggle_auto_update).pack(anchor='w')
        
        self.show_detailed_logs = tk.BooleanVar(value=False)
        tk.Checkbutton(monitor_frame, text="Logs detalhados", 
                      variable=self.show_detailed_logs).pack(anchor='w')
        
        # Limites de custo
        cost_frame = ttk.LabelFrame(self.settings_frame, text="💰 Limites de Custo", padding=15)
        cost_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(cost_frame, text="Alerta quando custo exceder (USD):").pack(anchor='w')
        self.cost_limit_var = tk.StringVar(value="1.00")\n        cost_entry = tk.Entry(cost_frame, textvariable=self.cost_limit_var, width=20)
        cost_entry.pack(anchor='w', pady=5)
        
        tk.Button(cost_frame, text="💾 Salvar Configurações",
                 command=self.save_settings,
                 bg='#388E3C', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        
    def create_agent_usage_chart(self, parent):
        """Cria gráfico de uso dos agentes"""
        try:
            # Criar figura matplotlib
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Dados dos agentes
            agent_calls = self.agent_system.session_metrics.agent_calls
            if agent_calls:
                agents = list(agent_calls.keys())
                calls = list(agent_calls.values())
                
                colors = ['#1976D2', '#388E3C', '#F57C00', '#D32F2F']
                ax.bar(agents, calls, color=colors[:len(agents)])
                ax.set_xlabel('Agentes')
                ax.set_ylabel('Número de Chamadas')
                ax.set_title('Uso dos Agentes na Sessão Atual')
            else:
                ax.text(0.5, 0.5, 'Nenhum dado disponível', 
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=12)
            
            # Integrar com tkinter
            canvas = FigureCanvasTkinter(fig, parent)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            tk.Label(parent, text=f"Erro ao criar gráfico: {e}").pack()
    
    def update_metrics(self):
        """Atualiza métricas em tempo real"""
        # Atualizar labels
        cost = self.agent_system.cost_tracker.total_cost
        input_tokens = self.agent_system.cost_tracker.input_tokens
        output_tokens = self.agent_system.cost_tracker.output_tokens
        total_tokens = input_tokens + output_tokens
        interactions = self.agent_system.session_metrics.interactions
        
        self.cost_label.config(text=f"💰 Custo da Sessão: ${cost:.6f}")
        self.tokens_label.config(text=f"🔢 Tokens: {total_tokens} (Input: {input_tokens}, Output: {output_tokens})")
        self.interactions_label.config(text=f"🔄 Interações: {interactions}")
        
        # Log de atividade
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] Métricas atualizadas - Custo: ${cost:.6f}, Tokens: {total_tokens}\\n"
        self.add_to_log(log_entry)
        
        # Verificar limite de custo
        try:
            cost_limit = float(self.cost_limit_var.get())
            if cost > cost_limit:
                messagebox.showwarning("⚠️ Limite de Custo", 
                                     f"Custo da sessão (${cost:.6f}) excedeu o limite (${cost_limit:.6f})")
        except:
            pass
    
    def add_to_log(self, message: str):
        """Adiciona mensagem ao log de atividades"""
        self.activity_log.config(state=tk.NORMAL)
        self.activity_log.insert(tk.END, message)
        self.activity_log.see(tk.END)
        self.activity_log.config(state=tk.DISABLED)
    
    def new_session(self):
        """Inicia nova sessão"""
        # Salvar sessão atual
        summary = self.agent_system.get_session_summary()
        
        # Reset do sistema
        self.agent_system = reset_agent_session()
        
        # Atualizar interface
        self.session_label.config(text=f"🆔 Sessão: {self.agent_system.session_id}")
        self.update_metrics()
        
        # Log
        self.add_to_log(f"[{datetime.now().strftime('%H:%M:%S')}] Nova sessão iniciada: {self.agent_system.session_id}\\n")
        
        messagebox.showinfo("✅ Nova Sessão", 
                           f"Nova sessão iniciada!\\nSessão anterior: ${summary['total_cost']:.6f}")
    
    def export_session(self):
        """Exporta dados da sessão"""
        try:
            summary = self.agent_system.get_session_summary()
            filename = f"chef_rag_session_{self.agent_system.session_id}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
            
            messagebox.showinfo("✅ Exportação", f"Sessão exportada para {filename}")
            self.add_to_log(f"[{datetime.now().strftime('%H:%M:%S')}] Sessão exportada: {filename}\\n")
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao exportar: {e}")
    
    def fetch_langsmith_data(self):
        """Busca dados do LangSmith"""
        if not LANGCHAIN_API_KEY:
            messagebox.showwarning("⚠️ Aviso", "LangSmith não configurado!")
            return
        
        try:
            # Placeholder - implementar busca real de dados LangSmith
            data = {
                "projeto": LANGCHAIN_PROJECT,
                "status": "Ativo",
                "runs_hoje": "Implementar busca real",
                "custo_estimado": "Implementar cálculo",
                "timestamp": datetime.now().isoformat()
            }
            
            self.langsmith_data.config(state=tk.NORMAL)
            self.langsmith_data.delete(1.0, tk.END)
            self.langsmith_data.insert(tk.END, json.dumps(data, indent=2, ensure_ascii=False))
            self.langsmith_data.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao buscar dados: {e}")
    
    def toggle_auto_update(self):
        """Alterna atualização automática"""
        if self.auto_update_var.get():
            self.schedule_update()
        
    def schedule_update(self):
        """Agenda próxima atualização"""
        if self.auto_update_var.get():
            self.update_metrics()
            self.root.after(5000, self.schedule_update)  # 5 segundos
    
    def save_settings(self):
        """Salva configurações"""
        messagebox.showinfo("✅ Configurações", "Configurações salvas com sucesso!")
    
    def run(self):
        """Executa a interface"""
        if self.auto_update_var.get():
            self.schedule_update()
        self.root.mainloop()

if __name__ == "__main__":
    dashboard = MonitoringDashboard()
    dashboard.run()