#!/usr/bin/env python3
"""
Script para iniciar o sistema Chef RAG completo (API + Frontend)
"""

import subprocess
import time
import os
import sys
import threading
import webbrowser

def start_api():
    """Inicia a API Flask"""
    print("🚀 Iniciando API Flask...")
    try:
        # Ativar ambiente virtual e executar API
        if os.name == 'nt':  # Windows
            python_path = os.path.join("venv", "Scripts", "python.exe")
        else:  # Linux/Mac
            python_path = os.path.join("venv", "bin", "python")
        
        subprocess.run([python_path, "api.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar API: {e}")
    except KeyboardInterrupt:
        print("\n🛑 API encerrada pelo usuário")

def start_frontend():
    """Inicia o frontend React"""
    print("🌐 Iniciando Frontend React...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if not os.path.exists(frontend_dir):
        print("❌ Pasta frontend não encontrada!")
        return
    
    try:
        # Verificar se node_modules existe, se não, instalar dependências
        if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
            print("📦 Instalando dependências do frontend...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Iniciar servidor de desenvolvimento
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar frontend: {e}")
        print("💡 Certifique-se de que o Node.js está instalado!")
    except KeyboardInterrupt:
        print("\n🛑 Frontend encerrado pelo usuário")

def process_recipe_book():
    """Processa o livro de receitas via terminal"""
    print("📚 Processando livro de receitas...")
    try:
        # Ativar ambiente virtual e executar processamento
        if os.name == 'nt':  # Windows
            python_path = os.path.join("venv", "Scripts", "python.exe")
        else:  # Linux/Mac
            python_path = os.path.join("venv", "bin", "python")
        
        subprocess.run([python_path, "pdf_inge.py"], check=True)
        print("✅ Livro processado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao processar livro: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Processamento cancelado pelo usuário")

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    # Verificar Python
    try:
        import flask
        import flask_cors
        from core_logic import config, rag_system, database
        print("✅ Dependências Python OK")
    except ImportError as e:
        print(f"❌ Dependência Python faltando: {e}")
        print("Execute: pip install flask flask-cors")
        return False
    
    # Verificar Node.js
    try:
        result = subprocess.run(["node", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Node.js {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js não encontrado!")
        print("Baixe em: https://nodejs.org/")
        return False
    
    return True

def main():
    """Função principal"""
    print("🧑‍🍳 Chef RAG - Sistema Completo")
    print("=" * 40)
    
    if not check_dependencies():
        print("\n❌ Dependências não atendidas. Configure o ambiente primeiro.")
        return
    
    print("\nEscolha uma opção:")
    print("1. 🚀 Iniciar sistema completo (API + Frontend)")
    print("2. 📡 Apenas API (http://localhost:5000)")
    print("3. 🌐 Apenas Frontend (http://localhost:3000)")
    print("4. 🐍 Sistema Python original (terminal)")
    print("5. 📚 Processar livro de receitas (PDF)")
    print("6. ❌ Sair")
    
    choice = input("\n➤ Digite sua escolha (1-6): ").strip()
    
    if choice == "1":
        print("\n🚀 Iniciando sistema completo...")
        print("📡 API: http://localhost:5000")
        print("🌐 Frontend: http://localhost:3000")
        print("\n⏰ Aguarde alguns segundos para tudo inicializar...")
        
        # Iniciar API em thread separada
        api_thread = threading.Thread(target=start_api, daemon=True)
        api_thread.start()
        
        # Aguardar API inicializar
        time.sleep(3)
        
        # Abrir navegador
        try:
            webbrowser.open("http://localhost:3000")
        except:
            pass
        
        # Iniciar frontend (bloqueante)
        start_frontend()
        
    elif choice == "2":
        print("\n📡 Iniciando apenas a API...")
        start_api()
        
    elif choice == "3":
        print("\n🌐 Iniciando apenas o frontend...")
        print("⚠️  Certifique-se de que a API está rodando em http://localhost:5000")
        start_frontend()
        
    elif choice == "4":
        print("\n🐍 Iniciando sistema Python original...")
        from main import main as python_main
        python_main()
        
    elif choice == "5":
        print("\n📚 Processando livro de receitas...")
        process_recipe_book()
        
    elif choice == "6":
        print("\n👋 Até mais!")
        
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")