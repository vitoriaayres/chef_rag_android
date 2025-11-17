#!/usr/bin/env python3
"""
Interface Principal do Chef RAG - Sistema de Interfaces Gráficas Unificado
Centraliza todas as funcionalidades em interfaces visuais modernas
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from datetime import datetime
from pathlib import Path

class ChefRAGMainGUI:
    """Interface principal do Chef RAG com todas as funcionalidades"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_main_interface()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("🧑‍🍳 Chef RAG - Assistente Culinário Inteligente")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        self.root.eval('tk::PlaceWindow . center')
        
        # Ícone personalizado (se existir)
        try:
            self.root.iconbitmap("assets/chef_icon.ico")
        except:
            pass
            
    def setup_styles(self):
        """Configura estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botões principais
        style.configure('Main.TButton',
                       background='#4a9eff',
                       foreground='white',
                       font=('Segoe UI', 12, 'bold'),
                       padding=(20, 15))
        
        # Estilo para botões secundários
        style.configure('Secondary.TButton',
                       background='#6c757d',
                       foreground='white',
                       font=('Segoe UI', 10),
                       padding=(15, 10))
                       
        # Estilo para frames
        style.configure('Card.TFrame',
                       background='#2b2b2b',
                       relief='raised',
                       borderwidth=2)
        
    def create_main_interface(self):
        """Cria a interface principal"""
        # Header
        header_frame = tk.Frame(self.root, bg='#1a1a1a', height=100)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(header_frame, 
                              text="🧑‍🍳 Chef RAG - Seu Assistente Culinário Inteligente",
                              font=('Segoe UI', 24, 'bold'),
                              fg='#4a9eff',
                              bg='#1a1a1a')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(header_frame,
                                 text="🤖 Inteligência Artificial • 📚 Base de Receitas • 🎯 Análise Avançada",
                                 font=('Segoe UI', 12),
                                 fg='#cccccc',
                                 bg='#1a1a1a')
        subtitle_label.pack()
        
        # Container principal
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Grid de funcionalidades
        self.create_features_grid(main_container)
        
        # Status bar
        self.create_status_bar()
        
    def create_features_grid(self, parent):
        """Cria o grid com todas as funcionalidades"""
        # Frame para o grid
        grid_frame = tk.Frame(parent, bg='#1a1a1a')
        grid_frame.pack(fill='both', expand=True)
        
        # Configurar grid
        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
        for i in range(3):
            grid_frame.rowconfigure(i, weight=1)
        
        # Funcionalidades principais
        features = [
            {
                'title': '📷 Câmera do PC',
                'subtitle': 'Capture ingredientes em tempo real',
                'command': self.open_webcam_interface,
                'color': '#28a745'
            },
            {
                'title': '📱 Câmera Mobile',
                'subtitle': 'Use seu celular via QR Code',
                'command': self.open_mobile_interface,
                'color': '#17a2b8'
            },
            {
                'title': '🖼️ Enviar Foto',
                'subtitle': 'Analise fotos dos seus ingredientes',
                'command': self.open_photo_interface,
                'color': '#fd7e14'
            },
            {
                'title': '✍️ Digitar Ingredientes',
                'subtitle': 'Liste manualmente os ingredientes',
                'command': self.open_text_interface,
                'color': '#6f42c1'
            },
            {
                'title': '🎤 Reconhecimento de Voz',
                'subtitle': 'Fale seus ingredientes naturalmente',
                'command': self.open_voice_interface,
                'color': '#e83e8c'
            },
            {
                'title': '🥗 Filtros Especiais',
                'subtitle': 'Dietas específicas e restrições',
                'command': self.open_diet_interface,
                'color': '#20c997'
            },
            {
                'title': '⏰ Cronômetros',
                'subtitle': 'Gerencie tempos de cozimento',
                'command': self.open_timer_interface,
                'color': '#ffc107'
            },
            {
                'title': '📊 Histórico',
                'subtitle': 'Visualize suas receitas anteriores',
                'command': self.open_history_interface,
                'color': '#6610f2'
            },
            {
                'title': '👤 Meu Perfil',
                'subtitle': 'Preferências e configurações',
                'command': self.open_profile_interface,
                'color': '#dc3545'
            }
        ]
        
        # Criar cards
        for i, feature in enumerate(features):
            row = i // 3
            col = i % 3
            self.create_feature_card(grid_frame, feature, row, col)
            
    def create_feature_card(self, parent, feature, row, col):
        """Cria um card para uma funcionalidade"""
        # Frame do card
        card_frame = tk.Frame(parent, bg='#2b2b2b', relief='raised', bd=2)
        card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Hover effects
        def on_enter(event):
            card_frame.configure(bg='#3b3b3b')
            
        def on_leave(event):
            card_frame.configure(bg='#2b2b2b')
            
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)
        
        # Conteúdo do card
        title_label = tk.Label(card_frame,
                              text=feature['title'],
                              font=('Segoe UI', 16, 'bold'),
                              fg=feature['color'],
                              bg='#2b2b2b')
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(card_frame,
                                 text=feature['subtitle'],
                                 font=('Segoe UI', 10),
                                 fg='#cccccc',
                                 bg='#2b2b2b',
                                 wraplength=200)
        subtitle_label.pack(pady=(0, 15))
        
        # Botão
        open_btn = tk.Button(card_frame,
                            text="Abrir",
                            command=feature['command'],
                            bg=feature['color'],
                            fg='white',
                            font=('Segoe UI', 11, 'bold'),
                            relief='flat',
                            padx=30,
                            pady=10)
        open_btn.pack(pady=(0, 20))
        
        # Efeitos do botão
        def on_btn_enter(event):
            open_btn.configure(bg=self.lighten_color(feature['color']))
            
        def on_btn_leave(event):
            open_btn.configure(bg=feature['color'])
            
        open_btn.bind("<Enter>", on_btn_enter)
        open_btn.bind("<Leave>", on_btn_leave)
        
    def lighten_color(self, color):
        """Clareia uma cor hex"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter_rgb = tuple(min(255, c + 30) for c in rgb)
        return '#%02x%02x%02x' % lighter_rgb
        
    def create_status_bar(self):
        """Cria a barra de status"""
        status_frame = tk.Frame(self.root, bg='#1a1a1a')
        status_frame.pack(fill='x', side='bottom')
        
        self.status_label = tk.Label(status_frame,
                                   text="🟢 Sistema Pronto",
                                   font=('Segoe UI', 9),
                                   fg='#28a745',
                                   bg='#1a1a1a')
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Informações do sistema
        info_label = tk.Label(status_frame,
                             text=f"Chef RAG v2.0 | {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                             font=('Segoe UI', 9),
                             fg='#6c757d',
                             bg='#1a1a1a')
        info_label.pack(side='right', padx=10, pady=5)
        
    def update_status(self, message, color='#28a745'):
        """Atualiza a mensagem de status"""
        self.status_label.configure(text=message, fg=color)
        
    # Métodos para abrir interfaces específicas
    def open_webcam_interface(self):
        """Abre interface da webcam"""
        self.update_status("🔄 Iniciando câmera do PC...", '#17a2b8')
        threading.Thread(target=self._start_webcam, daemon=True).start()
        
    def _start_webcam(self):
        """Inicia webcam em thread separada"""
        try:
            from webcam import run_webcam_capture
            run_webcam_capture()
            self.update_status("✅ Câmera finalizada")
        except Exception as e:
            self.update_status(f"❌ Erro na câmera: {str(e)}", '#dc3545')
            
    def open_mobile_interface(self):
        """Abre interface mobile"""
        self.update_status("🔄 Iniciando servidor mobile...", '#17a2b8')
        threading.Thread(target=self._start_mobile, daemon=True).start()
        
    def _start_mobile(self):
        """Inicia servidor mobile"""
        try:
            from camera_mobile import start_mobile_server
            start_mobile_server()
            self.update_status("✅ Servidor mobile finalizado")
        except Exception as e:
            self.update_status(f"❌ Erro no mobile: {str(e)}", '#dc3545')
            
    def open_photo_interface(self):
        """Abre interface de upload de foto"""
        self.update_status("🔄 Abrindo seletor de arquivos...", '#17a2b8')
        
        file_path = filedialog.askopenfilename(
            title="Selecione uma foto dos ingredientes",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            threading.Thread(target=self._process_photo, args=(file_path,), daemon=True).start()
        else:
            self.update_status("🟡 Seleção cancelada", '#ffc107')
            
    def _process_photo(self, file_path):
        """Processa foto selecionada"""
        try:
            from core_logic.sistema_rag import extract_ingredients_from_image, find_recipes_by_ingredient
            
            self.update_status("🔍 Analisando imagem...", '#17a2b8')
            
            # Extrair ingredientes
            ingredientes = extract_ingredients_from_image(file_path)
            
            if "Erro" not in ingredientes:
                self.update_status("🔍 Buscando receitas...", '#17a2b8')
                
                # Buscar receitas
                receitas = find_recipes_by_ingredient(ingredientes, file_path, "upload")
                
                # Mostrar resultado
                self._show_recipe_results(ingredientes, receitas)
                self.update_status("✅ Análise concluída")
            else:
                messagebox.showerror("Erro", f"Não foi possível analisar a imagem: {ingredientes}")
                self.update_status("❌ Erro na análise", '#dc3545')
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar foto: {str(e)}")
            self.update_status(f"❌ Erro: {str(e)}", '#dc3545')
            
    def open_text_interface(self):
        """Abre interface de texto"""
        self.create_text_input_window()
        
    def create_text_input_window(self):
        """Cria janela para entrada de texto"""
        text_window = tk.Toplevel(self.root)
        text_window.title("✍️ Digitar Ingredientes")
        text_window.geometry("600x400")
        text_window.configure(bg='#2b2b2b')
        text_window.transient(self.root)
        text_window.grab_set()
        
        # Centralizar janela
        text_window.eval('tk::PlaceWindow . center')
        
        # Título
        title_label = tk.Label(text_window,
                              text="✍️ Digite seus ingredientes",
                              font=('Segoe UI', 18, 'bold'),
                              fg='#4a9eff',
                              bg='#2b2b2b')
        title_label.pack(pady=20)
        
        # Instruções
        instructions = tk.Label(text_window,
                               text="Digite os ingredientes separados por vírgula\nExemplo: tomate, cebola, alho, frango",
                               font=('Segoe UI', 10),
                               fg='#cccccc',
                               bg='#2b2b2b')
        instructions.pack(pady=10)
        
        # Campo de texto
        text_frame = tk.Frame(text_window, bg='#2b2b2b')
        text_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        text_entry = tk.Text(text_frame,
                            font=('Segoe UI', 12),
                            bg='#3b3b3b',
                            fg='white',
                            insertbackground='white',
                            relief='flat',
                            bd=10)
        text_entry.pack(fill='both', expand=True)
        
        # Botões
        button_frame = tk.Frame(text_window, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        def process_text():
            ingredientes = text_entry.get("1.0", tk.END).strip()
            if ingredientes:
                text_window.destroy()
                threading.Thread(target=self._process_text_ingredients, args=(ingredientes,), daemon=True).start()
            else:
                messagebox.showwarning("Aviso", "Por favor, digite os ingredientes")
                
        process_btn = tk.Button(button_frame,
                               text="🔍 Buscar Receitas",
                               command=process_text,
                               bg='#28a745',
                               fg='white',
                               font=('Segoe UI', 12, 'bold'),
                               padx=30,
                               pady=10)
        process_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(button_frame,
                              text="❌ Cancelar",
                              command=text_window.destroy,
                              bg='#dc3545',
                              fg='white',
                              font=('Segoe UI', 12),
                              padx=30,
                              pady=10)
        cancel_btn.pack(side='left', padx=10)
        
    def _process_text_ingredients(self, ingredientes_text):
        """Processa ingredientes digitados"""
        try:
            from sistema_busca_robusta import buscar_receitas_robusta
            
            self.update_status("🔍 Buscando receitas...", '#17a2b8')
            
            # Processar ingredientes
            ingredientes = [ing.strip() for ing in ingredientes_text.split(',') if ing.strip()]
            
            # Buscar receitas usando sistema robusto
            receitas_lista = buscar_receitas_robusta(ingredientes)
            
            # Converter lista em string para exibição
            receitas = "\n\n---\n\n".join(receitas_lista)
            
            # Mostrar resultado
            self._show_recipe_results(', '.join(ingredientes), receitas)
            self.update_status("✅ Busca concluída")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar receitas: {str(e)}")
            self.update_status(f"❌ Erro: {str(e)}", '#dc3545')
            
    def open_voice_interface(self):
        """Abre interface de reconhecimento de voz"""
        self.update_status("🔄 Iniciando reconhecimento de voz...", '#17a2b8')
        try:
            from reconhecimento_voz_grafico import VoiceInterfaceGUI
            voice_app = VoiceInterfaceGUI()
            voice_app.run()
            self.update_status("✅ Interface de voz finalizada")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir interface de voz: {str(e)}")
            self.update_status(f"❌ Erro na voz: {str(e)}", '#dc3545')
            
    def open_diet_interface(self):
        """Abre interface de filtros dietéticos"""
        messagebox.showinfo("Em Desenvolvimento", "🚧 Interface de filtros dietéticos em desenvolvimento")
        
    def open_timer_interface(self):
        """Abre interface de cronômetros"""
        messagebox.showinfo("Em Desenvolvimento", "🚧 Interface de cronômetros em desenvolvimento")
        
    def open_history_interface(self):
        """Abre interface de histórico"""
        self.update_status("🔄 Abrindo histórico...", '#17a2b8')
        try:
            from visualizador_historico import main as history_main
            history_main()
            self.update_status("✅ Histórico finalizado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir histórico: {str(e)}")
            self.update_status(f"❌ Erro no histórico: {str(e)}", '#dc3545')
            
    def open_profile_interface(self):
        """Abre interface de perfil"""
        messagebox.showinfo("Em Desenvolvimento", "🚧 Interface de perfil em desenvolvimento")
        
    def _show_recipe_results(self, ingredientes, receitas):
        """Mostra resultados das receitas em janela separada"""
        results_window = tk.Toplevel(self.root)
        results_window.title("🍽️ Receitas Encontradas")
        results_window.geometry("800x600")
        results_window.configure(bg='#2b2b2b')
        
        # Título
        title_label = tk.Label(results_window,
                              text=f"🍽️ Receitas para: {ingredientes}",
                              font=('Segoe UI', 16, 'bold'),
                              fg='#4a9eff',
                              bg='#2b2b2b')
        title_label.pack(pady=20)
        
        # Área de texto com scrollbar
        text_frame = tk.Frame(results_window, bg='#2b2b2b')
        text_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_area = tk.Text(text_frame,
                           yscrollcommand=scrollbar.set,
                           font=('Segoe UI', 11),
                           bg='#3b3b3b',
                           fg='white',
                           wrap='word',
                           state='normal')
        text_area.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=text_area.yview)
        
        # Inserir receitas
        if receitas:
            text_area.insert(tk.END, receitas)
        else:
            text_area.insert(tk.END, "❌ Nenhuma receita encontrada para os ingredientes especificados.\n\n💡 Dicas:\n• Tente ingredientes mais comuns\n• Verifique a ortografia\n• Use combinações diferentes")
            
        text_area.configure(state='disabled')
        
        # Botão fechar
        close_btn = tk.Button(results_window,
                             text="✅ Fechar",
                             command=results_window.destroy,
                             bg='#28a745',
                             fg='white',
                             font=('Segoe UI', 12, 'bold'),
                             padx=30,
                             pady=10)
        close_btn.pack(pady=20)
        
    def run(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()

if __name__ == "__main__":
    app = ChefRAGMainGUI()
    app.run()