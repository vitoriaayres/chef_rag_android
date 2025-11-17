#!/usr/bin/env python3
"""
Script de Instalação para Interface de Voz Avançada - Chef RAG v2
Instala todas as dependências necessárias para o reconhecimento de voz
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala um pacote Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {package}: {e}")
        return False

def check_package(package_name, import_name=None):
    """Verifica se um pacote está instalado"""
    if not import_name:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def install_voice_dependencies():
    """Instala todas as dependências para reconhecimento de voz"""
    
    print("🎤 INSTALAÇÃO DE DEPENDÊNCIAS - INTERFACE DE VOZ AVANÇADA")
    print("="*60)
    print()
    
    # Lista de dependências
    dependencies = [
        ("SpeechRecognition", "speech_recognition"),
        ("matplotlib", "matplotlib"),
        ("PyPDF2", "PyPDF2"),
        ("numpy", "numpy"),
        ("nltk", "nltk"),
    ]
    
    # Dependências específicas para Windows
    if sys.platform.startswith('win'):
        dependencies.append(("pyaudio", "pyaudio"))
    else:
        print("⚠️ Para Linux/Mac, você pode precisar instalar PortAudio:")
        print("   Ubuntu/Debian: sudo apt install portaudio19-dev")
        print("   macOS: brew install portaudio")
        dependencies.append(("pyaudio", "pyaudio"))
    
    installed = 0
    failed = 0
    
    print("🔍 Verificando dependências existentes...")
    print()
    
    for package, import_name in dependencies:
        print(f"📦 Verificando {package}...", end=" ")
        
        if check_package(package, import_name):
            print("✅ Já instalado")
            installed += 1
        else:
            print("❌ Não encontrado - instalando...")
            
            if install_package(package):
                print(f"✅ {package} instalado com sucesso!")
                installed += 1
            else:
                print(f"❌ Falha ao instalar {package}")
                failed += 1
        
        print()
    
    # Dependências opcionais para melhor reconhecimento offline
    optional_deps = [
        ("pocketsphinx", "pocketsphinx"),
    ]
    
    print("\n🔧 Instalando dependências opcionais para reconhecimento offline...")
    
    for package, import_name in optional_deps:
        print(f"📦 Tentando instalar {package}...", end=" ")
        
        if check_package(package, import_name):
            print("✅ Já instalado")
        elif install_package(package):
            print("✅ Instalado!")
        else:
            print("⚠️ Falha (opcional - sistema funcionará sem)")
    
    # Baixar modelos NLTK necessários
    try:
        import nltk
        print("\n📚 Baixando modelos NLTK...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ Modelos NLTK baixados!")
    except:
        print("⚠️ Não foi possível baixar modelos NLTK")
    
    # Relatório final
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE INSTALAÇÃO")
    print("="*60)
    print(f"✅ Pacotes instalados com sucesso: {installed}")
    print(f"❌ Pacotes com falha: {failed}")
    
    if failed == 0:
        print("\n🎉 TODAS AS DEPENDÊNCIAS INSTALADAS COM SUCESSO!")
        print("🚀 Agora você pode usar a interface de voz avançada!")
        print()
        print("💡 Para testar, execute: python main.py")
        print("   Depois escolha a opção 5 (Interface de Voz Avançada)")
        
        return True
    else:
        print(f"\n⚠️ ALGUMAS DEPENDÊNCIAS FALHARAM ({failed} de {len(dependencies)})")
        print("🔧 Soluções:")
        print("   1. Execute como administrador")
        print("   2. Atualize o pip: python -m pip install --upgrade pip")
        print("   3. Use um ambiente virtual")
        print("   4. No Windows, instale Microsoft C++ Build Tools")
        
        return False

def test_installation():
    """Testa se a instalação funcionou"""
    print("\n🧪 TESTANDO INSTALAÇÃO...")
    print("-" * 40)
    
    tests = [
        ("tkinter", "Interface gráfica"),
        ("speech_recognition", "Reconhecimento de voz"),
        ("matplotlib", "Gráficos"),
        ("PyPDF2", "Processamento PDF"),
        ("numpy", "Processamento numérico"),
    ]
    
    all_ok = True
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"✅ {description} - OK")
        except ImportError:
            print(f"❌ {description} - FALHOU")
            all_ok = False
    
    # Teste específico para pyaudio
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        p.terminate()
        print("✅ Sistema de audio - OK")
    except Exception as e:
        print(f"⚠️ Sistema de audio - ATENÇÃO: {e}")
        print("   Microfone pode não funcionar corretamente")
    
    if all_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("🚀 Interface de voz está pronta para uso!")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Verifique as dependências que falharam")
    
    return all_ok

def main():
    """Função principal"""
    print("🎤 Chef RAG v2 - Instalador de Dependências de Voz")
    print("=" * 50)
    print()
    
    # Verificar versão do Python
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ é necessário!")
        print(f"Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    print()
    
    # Instalar dependências
    success = install_voice_dependencies()
    
    if success:
        # Testar instalação
        test_installation()
        
        print("\n" + "="*50)
        print("✨ INSTALAÇÃO CONCLUÍDA!")
        print("="*50)
        print("🎤 A Interface de Voz Avançada está pronta!")
        print()
        print("🚀 Funcionalidades disponíveis:")
        print("   • Reconhecimento de voz em tempo real")
        print("   • Métricas de acurácia visual")
        print("   • Comparação de ingredientes com PDF")
        print("   • Histórico detalhado de reconhecimentos")
        print("   • Múltiplas engines de reconhecimento")
        print()
        print("💡 Execute 'python main.py' e escolha opção 5!")
        
    else:
        print("\n❌ Instalação não foi concluída com sucesso")
        print("🔧 Consulte as mensagens de erro acima")

if __name__ == "__main__":
    main()
    input("\nPressione ENTER para sair...")