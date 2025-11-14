#!/usr/bin/env python3
"""
Chef RAG - Launcher Principal
Permite ao usuário escolher entre modo terminal ou web
"""

import os
import sys
import subprocess

def print_banner():
    """Exibe o banner do sistema"""
    print("=" * 60)
    print("🍽️  CHEF RAG - Sistema de Análise de Ingredientes")
    print("=" * 60)
    print()

def show_menu():
    """Exibe o menu de opções"""
    print("Escolha como você quer usar o sistema:")
    print()
    print("1️⃣  Terminal (IDE) - Interface de linha de comando")
    print("   • Rápido e direto")
    print("   • Ideal para desenvolvedores")
    print("   • Funciona diretamente na IDE")
    print()
    print("2️⃣  Web Browser (localhost) - Interface web moderna")
    print("   • Interface gráfica completa")
    print("   • Webcam integrada")
    print("   • Gerenciamento de livros")
    print("   • Acesso via http://localhost:5000")
    print()
    print("0️⃣  Sair")
    print()

def run_terminal_mode():
    """Executa o modo terminal"""
    print("🖥️  Iniciando modo TERMINAL...")
    print("=" * 40)
    
    # Caminho para o Python do ambiente virtual
    python_path = "c:/Users/Interfocus/Desktop/projetos_pessoais/chef_rag_v2/venv/Scripts/python.exe"
    
    try:
        # Executa o main.py que é a interface de terminal
        subprocess.run([python_path, "main.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar o modo terminal")
    except KeyboardInterrupt:
        print("\n👋 Modo terminal finalizado pelo usuário")

def run_web_mode():
    """Executa o modo web"""
    print("🌐 Iniciando modo WEB...")
    print("=" * 40)
    print("🚀 Iniciando servidores...")
    print("📡 API: http://localhost:5000")
    print("🎯 Frontend: http://localhost:3000")
    print()
    print("💡 Dica: Abra duas abas no seu navegador:")
    print("   • API Health: http://localhost:5000/api/health")
    print("   • Interface Principal: http://localhost:3000")
    print()
    print("⚠️  Para parar os servidores, pressione Ctrl+C")
    print("=" * 40)
    
    # Caminho para o Python do ambiente virtual
    python_path = "c:/Users/Interfocus/Desktop/projetos_pessoais/chef_rag_v2/venv/Scripts/python.exe"
    
    try:
        # Executa o script que inicia API + Frontend
        subprocess.run([python_path, "start_web.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o servidor web: {e}")
        print("💡 Verifique se o Node.js está instalado")
    except KeyboardInterrupt:
        print("\n👋 Servidores web finalizados pelo usuário")

def main():
    """Função principal do launcher"""
    while True:
        print_banner()
        show_menu()
        
        try:
            choice = input("Digite sua escolha (1, 2 ou 0): ").strip()
            print()
            
            if choice == "1":
                run_terminal_mode()
                input("\nPressione Enter para voltar ao menu...")
                
            elif choice == "2":
                run_web_mode()
                input("\nPressione Enter para voltar ao menu...")
                
            elif choice == "0":
                print("👋 Obrigado por usar o Chef RAG!")
                break
                
            else:
                print("❌ Opção inválida! Digite 1, 2 ou 0.")
                input("Pressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Chef RAG finalizado pelo usuário!")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()