#!/usr/bin/env python3
"""
Script de Limpeza Automática - Chef RAG v2
Remove arquivos desnecessários mantendo apenas o essencial
"""

import os
import shutil
from pathlib import Path

def criar_backup():
    """Cria backup dos arquivos que serão removidos"""
    backup_dir = Path("backup_arquivos_removidos")
    backup_dir.mkdir(exist_ok=True)
    
    print("📦 Criando backup dos arquivos que serão removidos...")
    return backup_dir

def limpar_arquivos():
    """Remove arquivos desnecessários"""
    
    # Arquivos a serem removidos
    arquivos_para_remover = [
        # APIs redundantes
        "api.py",
        "api_simple.py", 
        "mobile_api.py",
        
        # Scripts alternativos
        "launcher.py",
        "start.py",
        "start_web.py", 
        "main_new.py",
        "run_chef_rag_mobile.py",
        "start_chef_rag_mobile.bat",
        "Start-ChefRagMobile.ps1",
        
        # Sistemas antigos/experimentais
        "monitor.py",
        "ingredientes_opt.py",
        "lista_ingr.py",
        "pdf_inge.py",
        
        # Testes
        "test_cleanup.py",
        "test_langchain.py", 
        "test_openai_status.py",
        "test_smart_systems.py",
        "test_voice.py",
        
        # Scripts de análise temporários
        "analisar_dependencias.py",
        "arquivos_nao_utilizados.txt",
        "analise_arquivos.md",
        
        # Arquivo temporário
        "web_simple.html"
    ]
    
    backup_dir = criar_backup()
    removidos = []
    mantidos = []
    
    for arquivo in arquivos_para_remover:
        arquivo_path = Path(arquivo)
        
        if arquivo_path.exists():
            # Fazer backup
            backup_path = backup_dir / arquivo
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(arquivo_path, backup_path)
                os.remove(arquivo_path)
                removidos.append(arquivo)
                print(f"🗑️  Removido: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao remover {arquivo}: {e}")
                mantidos.append(arquivo)
        else:
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
    
    return removidos, mantidos, backup_dir

def limpar_diretorios_desnecessarios():
    """Remove diretórios desnecessários"""
    
    # Diretórios que podem ser limpos
    dirs_para_verificar = [
        "__pycache__",
        "temp_uploads",
        ".pytest_cache"
    ]
    
    removidos = []
    
    for dir_name in dirs_para_verificar:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            try:
                shutil.rmtree(dir_path)
                removidos.append(dir_name)
                print(f"📁 Diretório removido: {dir_name}")
            except Exception as e:
                print(f"❌ Erro ao remover diretório {dir_name}: {e}")
    
    return removidos

def calcular_economia(removidos):
    """Calcula a economia de espaço"""
    backup_dir = Path("backup_arquivos_removidos")
    total_size = 0
    
    for arquivo in removidos:
        backup_file = backup_dir / arquivo
        if backup_file.exists():
            total_size += backup_file.stat().st_size
    
    return total_size / 1024  # KB

def verificar_sistema():
    """Verifica se o sistema principal ainda funciona"""
    try:
        print("\n🔍 Verificando integridade do sistema...")
        
        # Testar import do main
        import main
        print("✅ main.py - OK")
        
        # Testar core_logic
        from core_logic import config, rag_system, database
        print("✅ core_logic - OK")
        
        print("🎉 Sistema íntegro após limpeza!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema após limpeza: {e}")
        return False

def main():
    print("🧹 CHEF RAG v2 - LIMPEZA AUTOMÁTICA")
    print("="*50)
    
    print("\n📋 Este script irá remover arquivos desnecessários:")
    print("  • APIs redundantes")
    print("  • Scripts alternativos")  
    print("  • Sistemas experimentais")
    print("  • Arquivos de teste")
    print("  • Caches temporários")
    
    print(f"\n⚠️  Um backup será criado antes da remoção")
    print(f"📁 Localização: ./backup_arquivos_removidos/")
    
    resposta = input(f"\n❓ Continuar com a limpeza? (s/n): ").lower().strip()
    
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("❌ Limpeza cancelada!")
        return
    
    print(f"\n🚀 Iniciando limpeza...")
    
    # Limpar arquivos
    removidos, mantidos, backup_dir = limpar_arquivos()
    
    # Limpar diretórios
    dirs_removidos = limpar_diretorios_desnecessarios()
    
    # Calcular economia
    economia_kb = calcular_economia(removidos)
    
    # Verificar sistema
    sistema_ok = verificar_sistema()
    
    # Relatório final
    print(f"\n" + "="*50)
    print("📊 RELATÓRIO DE LIMPEZA")
    print("="*50)
    print(f"🗑️  Arquivos removidos: {len(removidos)}")
    print(f"📁 Diretórios removidos: {len(dirs_removidos)}")
    print(f"💾 Espaço economizado: {economia_kb:.1f}KB")
    print(f"📦 Backup criado em: {backup_dir}")
    print(f"✅ Sistema íntegro: {'Sim' if sistema_ok else 'ATENÇÃO: Problemas detectados'}")
    
    if removidos:
        print(f"\n📝 Arquivos removidos:")
        for arquivo in removidos:
            print(f"  • {arquivo}")
    
    if mantidos:
        print(f"\n⚠️  Arquivos que não puderam ser removidos:")
        for arquivo in mantidos:
            print(f"  • {arquivo}")
    
    print(f"\n🎉 Limpeza concluída!")
    print(f"💡 Para desfazer, restaure os arquivos do backup")

if __name__ == "__main__":
    main()