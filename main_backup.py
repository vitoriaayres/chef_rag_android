#!/usr/bin/env python3
"""
Sistema Chef RAG v2 - Sistema Avançado de Análise de Ingredientes e Sugestão de Receitas

NOVA VERSÃO COM INTERFACE GRÁFICA COMPLETA!
Todas as funcionalidades agora possuem interfaces visuais modernas e intuitivas.

Funcionalidades:
1. Webcam - Interface gráfica para captura em tempo real
2. Mobile - Interface para conexão com dispositivos móveis  
3. Upload - Interface para análise de fotos salvas
4. Texto - Interface para entrada manual de ingredientes
5. Voz - Interface avançada de reconhecimento de voz
6. Histórico - Visualização gráfica de dados e estatísticas
7. Filtros - Interface para dietas especiais
8. Cronômetros - Interface para gerenciamento de tempo
9. Perfil - Interface de configurações do usuário

Versão: 2.0 - Novembro 2025
Desenvolvido com LangChain, ChromaDB e OpenAI
Interface moderna com Tkinter
"""

import sys
import os

def main():
    """Função principal - inicia interface gráfica"""
    try:
        print("🚀 Iniciando Chef RAG - Interface Gráfica...")
        print("✨ Carregando sistema de inteligência artificial...")
        
        # Importar e executar interface principal
        from interface_principal_chef import ChefRAGMainGUI
        
        print("🎨 Abrindo interface principal...")
        app = ChefRAGMainGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Erro ao importar interface: {e}")
        print("💡 Verifique se todas as dependências estão instaladas:")
        print("   pip install tkinter matplotlib")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("💡 Tente executar novamente ou verifique os logs")
        sys.exit(1)
        
    print("\n👋 Chef RAG finalizado. Até logo!")

if __name__ == "__main__":
    main()