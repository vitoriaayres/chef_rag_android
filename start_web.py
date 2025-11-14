#!/usr/bin/env python3
"""
Chef RAG - Iniciador Web Completo
Inicia tanto a API quanto o frontend automaticamente
"""

import os
import sys
import subprocess
import threading
import time
import signal

def start_api():
    """Inicia o servidor da API Flask"""
    print("🔧 Iniciando API Flask...")
    python_path = "c:/Users/Interfocus/Desktop/projetos_pessoais/chef_rag_v2/venv/Scripts/python.exe"
    
    try:
        subprocess.run([python_path, "api.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar API")
    except KeyboardInterrupt:
        print("⏹️  API finalizada")

def start_frontend():
    """Inicia o servidor do frontend React"""
    print("🔧 Iniciando Frontend React...")
    
    # Verifica se npm está disponível
    try:
        subprocess.run(["npm", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ NPM não encontrado! Instale o Node.js primeiro.")
        print("💡 Baixe em: https://nodejs.org/")
        return
    
    # Salva o diretório atual
    original_dir = os.getcwd()
    
    try:
        # Muda para o diretório frontend e executa npm run dev
        frontend_dir = os.path.join(original_dir, "frontend")
        os.chdir(frontend_dir)
        print("📦 Verificando dependências...")
        
        # Verifica se node_modules existe
        if not os.path.exists("node_modules"):
            print("📥 Instalando dependências...")
            subprocess.run(["npm", "install"], check=True)
        
        subprocess.run(["npm", "run", "dev"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar Frontend")
    except KeyboardInterrupt:
        print("⏹️  Frontend finalizado")
    finally:
        # Restaura o diretório original
        os.chdir(original_dir)

def main():
    """Inicia ambos os servidores"""
    print("🚀 CHEF RAG - Modo Web Completo")
    print("=" * 50)
    print("🔄 Iniciando API e Frontend simultaneamente...")
    print()
    
    # Inicia a API em uma thread separada
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Aguarda um pouco para a API iniciar
    print("⏳ Aguardando API inicializar...")
    time.sleep(3)
    
    print()
    print("✅ Servidores em execução:")
    print("📡 API: http://localhost:5000")
    print("🎯 Frontend: http://localhost:3000")
    print()
    print("💡 Abra http://localhost:3000 no seu navegador!")
    print("⚠️  Para parar, pressione Ctrl+C")
    print("=" * 50)
    print()
    
    try:
        # Inicia o frontend (processo principal)
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Parando servidores...")
        sys.exit(0)

if __name__ == "__main__":
    main()