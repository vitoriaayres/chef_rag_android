#!/usr/bin/env python3
"""
Sistema Chef RAG v2 - Sistema Avançado de Análise de Ingredientes e Sugestão de Receitas

Menu no terminal com interfaces gráficas para cada opção:
1. Webcam - Interface gráfica para captura em tempo real
2. Câmera Mobile - Interface para QR Code e conexão
3. Upload de Foto - Interface para análise de imagens
4. Digitar Ingredientes - Interface para entrada manual
5. Reconhecimento de Voz - Interface avançada com histórico
6. Visualizar Histórico - Interface de análise de dados

Versão: 2.0 - Novembro 2025
Desenvolvido com LangChain, ChromaDB e OpenAI
"""

import sys
import os

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Exibe o menu principal do sistema"""
    limpar_tela()
    print("\n" + "="*70)
    print("🧑‍🍳  CHEF RAG - Seu Assistente Culinário Inteligente")
    print("="*70)
    print("🤖 Inteligência Artificial  |  📚 Base de Receitas  |  🎯 Análise Avançada")
    print("="*70)
    
    print("\n📸  COMO VOCÊ QUER ENCONTRAR RECEITAS HOJE?")
    print()
    print("   1. 📷 Usar Câmera do Computador")
    print("   2. 📱 Usar Câmera do Celular (QR Code)")
    print("   3. 🖼️  Enviar Foto dos Ingredientes") 
    print("   4. ✍️  Digitar os Ingredientes")
    print("   5. 🎤 Reconhecimento de Voz")
    print()
    print("🔧  OUTRAS OPÇÕES:")
    print()
    print("   6. 📊 Ver Histórico de Receitas")
    print("   7. ❌ Sair do Sistema")
    print()
    print("="*70)

def usar_camera_pc():
    """Executa a interface da câmera do computador"""
    try:
        print("\n📷 Abrindo interface da câmera...")
        from webcam import run_webcam_capture
        run_webcam_capture()
    except ImportError:
        print("❌ Sistema de câmera não encontrado")
        print("💡 Verifique se a webcam está conectada")
    except Exception as e:
        print(f"❌ Erro na câmera: {e}")
        input("\nPressione ENTER para continuar...")

def usar_camera_celular():
    """Executa a interface da câmera do celular"""
    try:
        print("\n📱 Abrindo servidor para celular...")
        from camera_mobile import start_mobile_server
        start_mobile_server()
    except ImportError:
        print("❌ Sistema mobile não encontrado")
        print("💡 Execute: pip install flask qrcode pillow")
    except Exception as e:
        print(f"❌ Erro no servidor mobile: {e}")
        input("\nPressione ENTER para continuar...")

def enviar_foto_ingredientes():
    """Abre interface para upload de fotos"""
    try:
        print("\n📸 Abrindo interface de upload de fotos...")
        from interface_upload_foto import PhotoAnalysisInterface
        app = PhotoAnalysisInterface()
        app.run()
        print("✅ Interface de fotos finalizada!")
    except ImportError as e:
        print(f"❌ Erro ao importar interface de fotos: {e}")
        print("💡 Verifique se todas as dependências estão instaladas")
    except Exception as e:
        print(f"❌ Erro na interface de fotos: {e}")
        input("\nPressione ENTER para continuar...")

def digitar_ingredientes():
    """Abre interface para entrada manual de ingredientes"""
    try:
        print("\n✍️ Abrindo interface de entrada manual...")
        from interface_ingredientes_manual import ManualIngredientsInterface
        app = ManualIngredientsInterface()
        app.run()
        print("✅ Interface de entrada manual finalizada!")
    except ImportError as e:
        print(f"❌ Erro ao importar interface manual: {e}")
        print("💡 Verifique se o arquivo interface_ingredientes_manual.py existe")
    except Exception as e:
        print(f"❌ Erro na interface manual: {e}")
        input("\nPressione ENTER para continuar...")

def falar_ingredientes():
    """Abre a interface de reconhecimento de voz"""
    try:
        print("\n🎤 Abrindo interface de reconhecimento de voz...")
        from reconhecimento_voz_simples import SimpleVoiceInterface
        app = SimpleVoiceInterface()
        app.run()
        print("✅ Interface de voz finalizada!")
    except ImportError as e:
        print(f"❌ Erro ao importar interface de voz: {e}")
        print("💡 Execute: python instalar_dependencias_voz.py")
    except Exception as e:
        print(f"❌ Erro na interface de voz: {e}")
        input("\nPressione ENTER para continuar...")

def executar_historico():
    """Executa o visualizador de histórico"""
    try:
        print("\n📊 Abrindo visualizador de histórico...")
        from visualizador_historico import main as history_main
        history_main()
        print("✅ Histórico finalizado!")
    except ImportError:
        print("❌ Sistema de histórico não encontrado")
    except Exception as e:
        print(f"❌ Erro ao abrir histórico: {e}")
        input("\nPressione ENTER para continuar...")

def main():
    """Função principal - loop do menu"""
    while True:
        try:
            mostrar_menu()
            opcao = input("\n🎯 Digite sua escolha (1-7): ").strip()
            
            if opcao == "1":
                usar_camera_pc()
            elif opcao == "2":
                usar_camera_celular()
            elif opcao == "3":
                enviar_foto_ingredientes()
            elif opcao == "4":
                digitar_ingredientes()
            elif opcao == "5":
                falar_ingredientes()
            elif opcao == "6":
                executar_historico()
            elif opcao == "7":
                print("\n👋 Obrigado por usar o Chef RAG!")
                print("🍽️ Bom apetite e até a próxima!")
                break
            else:
                print("\n❌ Opção inválida! Digite um número de 1 a 7.")
                input("Pressione ENTER para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo do Chef RAG...")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()