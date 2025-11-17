#!/usr/bin/env python3
"""
Instalador de Dependências para Sistema de Agentes - Chef RAG v2
================================================================

Script para instalar as dependências necessárias para o sistema de agentes
e monitoramento com LangSmith.

Execução:
python scripts/instalar_dependencias_agentes.py
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala um pacote Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}")
        return False

def main():
    """Função principal"""
    print("🔧 Chef RAG v2 - Instalador de Dependências para Agentes")
    print("=" * 60)
    
    # Lista de pacotes necessários para o sistema de agentes
    packages = [
        "langchain>=0.1.0",
        "langchain-openai>=0.1.0", 
        "langchain-core>=0.1.0",
        "langsmith>=0.1.0",
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
        "requests>=2.31.0"
    ]
    
    print("📦 Instalando dependências para sistema de agentes...")
    print()
    
    success_count = 0
    for package in packages:
        print(f"📥 Instalando {package}...")
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"📊 Resultado: {success_count}/{len(packages)} pacotes instalados com sucesso")
    
    if success_count == len(packages):
        print("🎉 Todas as dependências foram instaladas!")
        print()
        print("🔧 Próximos passos:")
        print("1. Configure seu .env com LANGCHAIN_API_KEY (opcional)")
        print("2. Execute: python main.py")
        print("3. Escolha opção 13 para abrir o Dashboard de Monitoramento")
        print()
        print("📖 Para configurar LangSmith:")
        print("   - Registre-se em: https://smith.langchain.com/")
        print("   - Obtenha sua API key")
        print("   - Adicione LANGCHAIN_API_KEY=sua_key no arquivo .env")
    else:
        print("⚠️ Algumas dependências falharam ao instalar.")
        print("Tente executar manualmente:")
        for package in packages:
            print(f"   pip install {package}")
    
    print()
    input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()