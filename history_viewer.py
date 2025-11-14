#!/usr/bin/env python3
"""
Script para visualizar e gerenciar o histórico de análises de ingredientes
"""

import sys
import os
from core_logic.database import history_db

def show_menu():
    """Exibe o menu de opções do histórico"""
    print("\n" + "="*50)
    print("📊 HISTÓRICO DE ANÁLISES - Chef RAG")
    print("="*50)
    print("1. 📈 Mostrar resumo estatístico")
    print("2. 🕐 Análises recentes")
    print("3. 🔍 Buscar por ingrediente")
    print("4. 🥕 Listar todos os ingredientes")
    print("5. 📤 Exportar histórico (JSON)")
    print("6. 🗑️  Limpar base de dados")
    print("7. ❌ Voltar")
    print("="*50)

def show_recent_analyses():
    """Mostra as análises mais recentes"""
    print("\n🕐 ANÁLISES RECENTES:")
    print("-" * 80)
    
    analyses = history_db.get_recent_analyses(20)
    
    if not analyses:
        print("Nenhuma análise encontrada.")
        return
    
    for analysis in analyses:
        timestamp, image_name, ingredient, suggestion, mode, proc_time = analysis
        
        # Formata timestamp
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%d/%m/%Y %H:%M:%S")
        
        mode_icon = "📷" if mode == "webcam" else "📁"
        
        print(f"\n{mode_icon} {time_str} - {ingredient}")
        if image_name:
            print(f"   📸 Arquivo: {image_name}")
        print(f"   ⏱️  Tempo: {proc_time:.2f}s")
        
        if suggestion and len(suggestion) > 100:
            print(f"   💡 Resposta: {suggestion[:100]}...")
        elif suggestion:
            print(f"   💡 Resposta: {suggestion}")
    
    print("-" * 80)

def search_ingredient():
    """Busca análises por ingrediente"""
    ingredient = input("\n🔍 Digite o nome do ingrediente: ").strip()
    
    if not ingredient:
        print("❌ Nome inválido.")
        return
    
    results = history_db.search_by_ingredient(ingredient)
    
    if not results:
        print(f"❌ Nenhuma análise encontrada para '{ingredient}'.")
        return
    
    print(f"\n🔍 RESULTADOS PARA '{ingredient.upper()}':")
    print("-" * 60)
    
    for result in results:
        timestamp, image_name, suggestion, mode = result
        
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp)
        time_str = dt.strftime("%d/%m/%Y %H:%M")
        
        mode_icon = "📷" if mode == "webcam" else "📁"
        
        print(f"\n{mode_icon} {time_str}")
        if image_name:
            print(f"   📸 {image_name}")
        
        if suggestion:
            # Mostra primeiras linhas da sugestão
            lines = suggestion.split('\n')[:3]
            for line in lines:
                if line.strip():
                    print(f"   💡 {line.strip()}")
    
    print("-" * 60)

def list_all_ingredients():
    """Lista todos os ingredientes únicos"""
    ingredients = history_db.get_all_ingredients()
    
    if not ingredients:
        print("❌ Nenhum ingrediente encontrado.")
        return
    
    print("\n🥕 TODOS OS INGREDIENTES ANALISADOS:")
    print("-" * 40)
    
    for i, (ingredient, count) in enumerate(ingredients, 1):
        print(f"{i:2d}. {ingredient} ({count} análise{'s' if count > 1 else ''})")
    
    print("-" * 40)
    print(f"📊 Total: {len(ingredients)} ingredientes únicos")

def export_history():
    """Exporta o histórico para JSON"""
    print("\n📤 Exportando histórico...")
    
    try:
        output_file = history_db.export_history_to_json()
        print(f"✅ Histórico exportado com sucesso!")
        print(f"📁 Arquivo: {output_file}")
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")

def clear_database():
    """Limpa toda a base de dados (com confirmação)"""
    print("\n⚠️  ATENÇÃO: Esta ação irá apagar TODO o histórico!")
    confirm = input("Digite 'CONFIRMAR' para prosseguir: ").strip()
    
    if confirm != "CONFIRMAR":
        print("❌ Operação cancelada.")
        return
    
    try:
        import sqlite3
        with sqlite3.connect(history_db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM ingredient_history')
            cursor.execute('DELETE FROM statistics')
            cursor.execute('''
                INSERT INTO statistics (total_analyses, webcam_analyses, folder_analyses, 
                                      successful_analyses, failed_analyses, last_updated)
                VALUES (0, 0, 0, 0, 0, datetime('now'))
            ''')
            conn.commit()
        
        print("✅ Base de dados limpa com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao limpar base: {e}")

def main():
    """Função principal"""
    while True:
        try:
            show_menu()
            choice = input("➤ Escolha uma opção (1-7): ").strip()
            
            if choice == "1":
                history_db.show_summary()
            elif choice == "2":
                show_recent_analyses()
            elif choice == "3":
                search_ingredient()
            elif choice == "4":
                list_all_ingredients()
            elif choice == "5":
                export_history()
            elif choice == "6":
                clear_database()
            elif choice == "7":
                break
            else:
                print("❌ Opção inválida!")
            
            input("\nPressione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Saindo...")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()