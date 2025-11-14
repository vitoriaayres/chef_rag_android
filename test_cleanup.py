#!/usr/bin/env python3
"""
Teste do sistema de limpeza automática
"""

import os
import time
import shutil
from pathlib import Path
from core_logic.cleanup_manager import setup_image_cleanup, manual_image_cleanup

def test_cleanup_system():
    """Testa o sistema de limpeza automática"""
    
    print("🧪 TESTE DO SISTEMA DE LIMPEZA AUTOMÁTICA")
    print("=" * 50)
    
    # Configurar sistema de limpeza
    cleanup_manager = setup_image_cleanup()
    
    # Pasta de imagens
    images_folder = Path("data/imagens")
    
    # Verificar imagens atuais
    print(f"\n📁 Verificando pasta: {images_folder}")
    if images_folder.exists():
        current_images = list(images_folder.glob("*.jpg")) + list(images_folder.glob("*.png"))
        print(f"📊 Imagens atuais: {len(current_images)}")
        for img in current_images:
            print(f"  - {img.name}")
    else:
        print("❌ Pasta de imagens não encontrada!")
        return
    
    # Opções do teste
    print(f"\n🔧 OPÇÕES DE TESTE:")
    print("1. Executar limpeza manual agora")
    print("2. Sair (limpeza automática ao encerrar)")
    print("3. Desabilitar limpeza e sair")
    
    while True:
        try:
            choice = input("\n➤ Escolha (1-3): ").strip()
            
            if choice == "1":
                print("\n🧹 Executando limpeza manual...")
                manual_image_cleanup()
                break
                
            elif choice == "2":
                print("\n✅ Saindo... (limpeza automática será executada)")
                break
                
            elif choice == "3":
                print("\n🔒 Desabilitando limpeza automática...")
                cleanup_manager.disable_cleanup()
                print("✅ Saindo sem limpeza")
                break
                
            else:
                print("❌ Opção inválida! Escolha 1-3.")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Interrompido pelo usuário (limpeza automática será executada)")
            break

if __name__ == "__main__":
    test_cleanup_system()