#!/usr/bin/env python3
"""
Teste do Reconhecimento de Voz no Terminal
Permite testar a funcionalidade de voz de forma interativa
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core_logic.voice_recognition import voice_recognition
from core_logic import rag_system

def main():
    print("=" * 60)
    print("🎤 CHEF RAG - TESTE DE RECONHECIMENTO DE VOZ")
    print("=" * 60)
    print()
    
    # Testa se o microfone está disponível
    print("🔧 Verificando status do microfone...")
    test_result = voice_recognition.test_microphone()
    print(f"Status: {test_result['message']}")
    print()
    
    if test_result['available']:
        print("✅ Microfone funcionando!")
        
        if 'microphones' in test_result.get('details', {}):
            mics = test_result['details']['microphones']
            print(f"📱 Microfones encontrados: {len(mics)}")
            for i, mic in enumerate(mics[:3], 1):  # Mostra apenas os 3 primeiros
                print(f"   {i}. {mic}")
        print()
        
        # Loop principal de reconhecimento
        while True:
            print("-" * 50)
            print("Escolha uma opção:")
            print("1. 🎙️  Reconhecer ingredientes por voz")
            print("2. 🧠 Reconhecer + Buscar receitas")
            print("3. 🔧 Testar microfone novamente")
            print("4. ❌ Sair")
            print()
            
            choice = input("➤ Digite sua escolha (1-4): ").strip()
            print()
            
            if choice == "1":
                test_voice_recognition()
            elif choice == "2":
                test_voice_with_recipes()
            elif choice == "3":
                test_microphone_again()
            elif choice == "4":
                print("👋 Saindo do teste de voz...")
                break
            else:
                print("❌ Opção inválida! Escolha entre 1-4.")
    else:
        print("❌ Não foi possível usar o microfone.")
        print("💡 Verifique se:")
        print("   - O microfone está conectado")
        print("   - As permissões estão corretas")
        print("   - O pyaudio está instalado corretamente")

def test_voice_recognition():
    """Testa apenas o reconhecimento de voz"""
    print("🎤 TESTE DE RECONHECIMENTO DE VOZ")
    print("=" * 40)
    print()
    
    print("💡 Dicas para melhor reconhecimento:")
    print("   - Fale claramente e pausadamente")
    print("   - Evite ruídos de fundo")
    print("   - Diga 'Tenho [ingredientes]' ou apenas os ingredientes")
    print("   - Exemplo: 'Tenho tomate, cebola e alho'")
    print()
    
    input("Pressione ENTER para começar a gravação...")
    print()
    
    try:
        ingredients = voice_recognition.recognize_ingredients(timeout=8, phrase_time_limit=15)
        
        if ingredients:
            print("🎯 RESULTADO DO RECONHECIMENTO:")
            print(f"✅ Ingredientes: '{ingredients}'")
            print()
            
            # Mostra ingredientes separados
            if ',' in ingredients:
                ingredient_list = [ing.strip() for ing in ingredients.split(',')]
                print("📝 Ingredientes detectados:")
                for i, ing in enumerate(ingredient_list, 1):
                    print(f"   {i}. {ing}")
            
        else:
            print("❌ Não foi possível reconhecer ingredientes")
            print("💭 Possíveis causas:")
            print("   - Fala muito baixa ou rápida")
            print("   - Ruído de fundo")
            print("   - Timeout (não falou a tempo)")
            
    except Exception as e:
        print(f"❌ Erro durante reconhecimento: {e}")
    
    print()
    input("Pressione ENTER para continuar...")

def test_voice_with_recipes():
    """Testa reconhecimento + busca de receitas"""
    print("🎤🧠 RECONHECIMENTO + BUSCA DE RECEITAS")
    print("=" * 50)
    print()
    
    print("Este teste fará:")
    print("1. 🎙️  Reconhecer seus ingredientes por voz")
    print("2. 🔍 Buscar receitas no banco de dados")
    print("3. 🤖 Gerar sugestão do chef")
    print()
    
    input("Pressione ENTER para começar...")
    print()
    
    try:
        # Reconhecimento de voz
        ingredients = voice_recognition.recognize_ingredients(timeout=8, phrase_time_limit=15)
        
        if ingredients:
            print("✅ Ingredientes reconhecidos:", ingredients)
            print()
            
            # Busca receitas
            print("🔍 Buscando receitas...")
            recipes_response = rag_system.find_recipes_by_ingredient(
                ingredients, 
                source_mode='voice_terminal'
            )
            
            print()
            print("📋 SUGESTÕES DE RECEITAS:")
            print("=" * 40)
            print(recipes_response)
            
        else:
            print("❌ Não foi possível reconhecer ingredientes")
            
    except Exception as e:
        print(f"❌ Erro durante o processo: {e}")
    
    print()
    input("Pressione ENTER para continuar...")

def test_microphone_again():
    """Testa o microfone novamente"""
    print("🔧 TESTE DE MICROFONE")
    print("=" * 30)
    print()
    
    test_result = voice_recognition.test_microphone()
    
    print(f"Status: {test_result['message']}")
    print(f"Disponível: {'✅ Sim' if test_result['available'] else '❌ Não'}")
    
    if test_result['available'] and 'details' in test_result:
        details = test_result['details']
        
        if 'microphones' in details:
            print(f"Microfones: {len(details['microphones'])} encontrado(s)")
            
        if 'energy_threshold' in details:
            print(f"Threshold de energia: {details['energy_threshold']}")
    
    print()
    input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()