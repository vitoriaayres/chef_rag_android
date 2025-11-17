import cv2 
import os 
import time 
import threading
import numpy as np
from datetime import datetime
from core_logic import config 
from core_logic import sistema_rag

SNAPSHOT_INTERVAL = os.path.join(config.BASE_DIR, "..", "temp_snapshot.jpg")

def draw_modern_interface(frame, status="pronto", ingredient=None, recipe_count=0, rotation_angle=0):
    """Desenha uma interface moderna e informativa na webcam"""
    height, width = frame.shape[:2]
    
    # Cores modernas
    primary_color = (67, 126, 235)  # Azul moderno
    success_color = (46, 204, 113)  # Verde
    warning_color = (241, 196, 15)  # Amarelo
    danger_color = (231, 76, 60)    # Vermelho
    dark_overlay = (30, 30, 30)     # Cinza escuro
    
    # Overlay semi-transparente no topo
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, 120), dark_overlay, -1)
    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
    
    # Título principal
    title = "CHEF RAG - Webcam Inteligente"
    cv2.putText(frame, title, (20, 35), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
    
    # Data e hora
    now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    cv2.putText(frame, now, (width - 250, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    # Indicador de rotação (se houver)
    if rotation_angle > 0:
        rotation_text = f"🔄 Rotação: {rotation_angle}°"
        cv2.putText(frame, rotation_text, (width - 250, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    
    # Status indicator
    if status == "ready":
        status_color = primary_color
        status_text = "Pronto para escanear"
        status_icon = "●"
    elif status == "scanning":
        status_color = warning_color
        status_text = "Analisando ingrediente..."
        status_icon = "⚡"
    elif status == "success":
        status_color = success_color
        status_text = f"Encontrado: {ingredient}"
        status_icon = "✓"
    elif status == "error":
        status_color = danger_color
        status_text = "Erro na análise"
        status_icon = "✗"
    
    # Desenha status
    cv2.putText(frame, status_icon, (25, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
    cv2.putText(frame, status_text, (55, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Contador de receitas (se houver)
    if recipe_count > 0:
        recipe_text = f"📚 {recipe_count} receitas encontradas"
        cv2.putText(frame, recipe_text, (55, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, success_color, 1)
    
    # Overlay de instruções no rodapé
    footer_overlay = frame.copy()
    cv2.rectangle(footer_overlay, (0, height-80), (width, height), dark_overlay, -1)
    cv2.addWeighted(footer_overlay, 0.7, frame, 0.3, 0, frame)
    
    # Instruções
    instructions = [
        "Pressione 'E' para escanear ingrediente",
        "Pressione 'R' para rotacionar imagem",
        "Pressione 'H' para histórico",
        "Pressione 'Q' para sair"
    ]
    
    y_start = height - 65
    for i, instruction in enumerate(instructions):
        cv2.putText(frame, instruction, (20, y_start + i * 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Frame de captura (área de foco)
    margin = 80
    cv2.rectangle(frame, (margin, margin + 120), (width - margin, height - margin - 80), primary_color, 2)
    cv2.putText(frame, "Área de captura", (margin + 10, margin + 140), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, primary_color, 1)
    
    return frame

def show_analysis_popup(frame, ingredient, recipes):
    """Mostra popup com resultado da análise"""
    height, width = frame.shape[:2]
    
    # Criar overlay escuro
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Popup central
    popup_w, popup_h = 500, 300
    popup_x = (width - popup_w) // 2
    popup_y = (height - popup_h) // 2
    
    # Fundo do popup
    cv2.rectangle(frame, (popup_x, popup_y), (popup_x + popup_w, popup_y + popup_h), (40, 40, 40), -1)
    cv2.rectangle(frame, (popup_x, popup_y), (popup_x + popup_w, popup_y + popup_h), (67, 126, 235), 3)
    
    # Título do popup
    cv2.putText(frame, "Análise Concluída!", (popup_x + 20, popup_y + 40), 
               cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    
    # Ingrediente encontrado
    cv2.putText(frame, f"Ingrediente: {ingredient}", (popup_x + 20, popup_y + 80), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (46, 204, 113), 2)
    
    # Número de receitas
    cv2.putText(frame, f"Receitas encontradas: {recipe_count}", (popup_x + 20, popup_y + 110), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (241, 196, 15), 1)
    
    # Instruções
    instructions = [
        "• Verifique o terminal para escolher a receita",
        "• Digite o número da receita desejada",
        "• Pressione 0 para continuar capturando",
        "• Pressione 'Q' para sair"
    ]
    
    for i, instruction in enumerate(instructions):
        cv2.putText(frame, instruction, (popup_x + 20, popup_y + 150 + i * 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    return frame

def initialize_camera_fast():
    """Inicialização otimizada da câmera"""
    print("🔄 Inicializando câmera...")
    
    # Tenta diferentes backends para inicialização mais rápida
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
    
    for backend in backends:
        try:
            cap = cv2.VideoCapture(0, backend)
            if cap.isOpened():
                # Configurações otimizadas
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                cap.set(cv2.CAP_PROP_FPS, 30)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduz buffer para menos delay
                
                # Testa se consegue capturar um frame
                ret, frame = cap.read()
                if ret:
                    print("✅ Câmera inicializada em alta resolução!")
                    return cap
                    
        except Exception:
            continue
    
    print("❌ Erro: Câmera não encontrada!")
    return None

def run_webcam_capture():
    """
    Inicia a webcam otimizada com interface moderna
    """
    # Inicialização rápida
    cap = initialize_camera_fast()
    if not cap:
        print("❌ Não foi possível acessar a webcam.")
        print("💡 Verifique se a webcam está conectada.")
        input("Pressione ENTER para voltar...")
        return
    
    # Criar janela com tamanho fixo
    window_name = "Chef RAG - Webcam Inteligente"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)
    
    print("\n" + "="*60)
    print("📷 CHEF RAG - WEBCAM MODERNA ATIVADA")
    print("="*60)
    print("🎯 Interface moderna carregada")
    print("📹 Resolução: 1280x720")
    print("⚡ FPS otimizado para performance")
    print("🎨 UI redesenhada com elementos visuais")
    print("="*60)
    print("💡 DICAS:")
    print("   • Posicione ingredientes na área de captura")
    print("   • Use boa iluminação para melhores resultados")
    print("   • Pressione 'E' quando estiver pronto")
    print("   • Pressione 'R' para rotacionar imagem")
    print("="*60)

    frame_count = 0
    status = "ready"
    last_ingredient = None
    recipe_count = 0
    show_popup = False
    popup_timer = 0
    rotation_angle = 0  # 0, 90, 180, 270
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Erro na captura. Reconectando...")
            break
        
        # Aplicar rotação se necessário
        if rotation_angle == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotation_angle == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotation_angle == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # Otimização: processa apenas alguns frames
        frame_count += 1
        
        # Aplica filtros para melhorar qualidade
        if frame_count % 2 == 0:
            frame = cv2.bilateralFilter(frame, 9, 75, 75)  # Suaviza a imagem
        
        # Se está mostrando popup
        if show_popup:
            frame = show_analysis_popup(frame, last_ingredient, "receitas encontradas")
            popup_timer += 1
            if popup_timer > 90:  # 3 segundos a 30fps
                show_popup = False
                popup_timer = 0
                status = "ready"
        else:
            # Interface normal
            frame = draw_modern_interface(frame, status, last_ingredient, recipe_count, rotation_angle)

        cv2.imshow(window_name, frame)

        # Captura de teclas com menor delay
        key = cv2.waitKey(1) & 0xFF
        
        # Verifica se a janela ainda existe
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            print("👋 Janela fechada. Encerrando...")
            break
        
        if key == ord('q'):
            print("👋 Encerrando webcam...")
            break
            
        elif key == ord('r'):
            rotation_angle = (rotation_angle + 90) % 360
            print(f"🔄 Rotação: {rotation_angle}°")
            
        elif key == ord('e'):
            status = "scanning"
            print("\n🔍 ANÁLISE INICIADA")
            print("=" * 30)
            print("📸 Capturando imagem...")

            cv2.imwrite(SNAPSHOT_INTERVAL, frame)
            
            print("🧠 Processando com IA...")
            ingredient = sistema_rag.extract_ingredients_from_image(SNAPSHOT_INTERVAL)

            if "Erro" in ingredient:
                print("❌ Ingrediente não identificado")
                print("💡 Tente uma imagem mais clara")
                status = "error"
                time.sleep(1)
                continue
                
            print(f"✅ Detectado: {ingredient}")
            print("🔍 Buscando receitas na base...")
            last_ingredient = ingredient
            status = "success"
            
            # Usar sistema CSV para buscar receitas
            try:
                from main import extrair_receitas_csv
                receitas = extrair_receitas_csv(ingredient)
                
                if receitas:
                    recipe_count = len(receitas)
                    print(f"\n🍽️ {recipe_count} RECEITAS ENCONTRADAS:")
                    print("="*70)
                    
                    # Mostrar receitas com detalhes
                    for i, receita in enumerate(receitas[:5], 1):
                        print(f"\n{i}. 📋 {receita['titulo']}")
                        print(f"   📊 Compatibilidade: {receita['score']:.1f}%")
                        print(f"   📂 {receita['categoria']} | ⏰ {receita['tempo_preparo']}")
                        print(f"   🥬 Ingredientes: {receita['ingredientes_busca']}")
                        
                        # Preview do preparo
                        modo_preview = receita['modo_preparo'].split(' | ')[:2]
                        print(f"   👨‍🍳 Preview: {' | '.join(modo_preview)}")
                        if len(receita['modo_preparo'].split(' | ')) > 2:
                            print(f"   ... e mais {len(receita['modo_preparo'].split(' | ')) - 2} passos")
                    
                    print("="*70)
                    show_popup = True
                    popup_timer = 0
                    
                    # Iniciar thread para seleção de receita
                    import threading
                    threading.Thread(target=webcam_recipe_selection, args=(receitas,)).start()
                    
                else:
                    print("❌ Nenhuma receita encontrada")
                    recipe_count = 0
                    status = "error"
                    
            except Exception as e:
                print(f"❌ Erro na busca: {e}")
                # Fallback para sistema antigo
                recipes = sistema_rag.find_recipes_by_ingredient(ingredient, SNAPSHOT_INTERVAL, "webcam")
                recipe_count = recipes.count("Página") if recipes else 0
                
                if not recipes:
                    print(f"❌ Nenhuma receita encontrada para: {ingredient}")
                    status = "error"
                    recipe_count = 0
                else:
                    print("\n🍽️ RECEITAS ENCONTRADAS:")
                    print("=" * 50)
                    print(recipes)
                    print("=" * 50)
                    show_popup = True
                    popup_timer = 0
            
            print("📷 Pronto para próxima captura...")
            
        elif key == ord('h'):
            print("\n📊 ABRINDO HISTÓRICO...")
            # Aqui poderia chamar o visualizador de histórico
            try:
                from visualizador_historico import main as history_main
                history_main()
            except:
                print("❌ Histórico não disponível")

def webcam_recipe_selection(receitas):
    """Thread separada para seleção de receita na webcam"""
    try:
        print(f"\n🎯 ESCOLHA SUA RECEITA:")
        print("-" * 40)
        
        while True:
            escolha = input(f"👨‍🍳 Digite o número da receita (1-{min(5, len(receitas))}) ou 0 para continuar: ").strip()
            
            if escolha == "0":
                print("📷 Continuando captura...")
                break
            
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(receitas[:5]):
                    receita_escolhida = receitas[idx]
                    
                    # Mostrar receita completa
                    from main import mostrar_modo_preparo_csv
                    mostrar_modo_preparo_csv(receita_escolhida)
                    break
                else:
                    print(f"❌ Digite um número entre 1 e {min(5, len(receitas))}")
            except ValueError:
                print("❌ Digite apenas números")
                
    except Exception as e:
        print(f"❌ Erro na seleção: {e}")

    # Limpeza otimizada
    cap.release()
    cv2.destroyAllWindows()
    
    # Remove arquivo temporário
    if os.path.exists(SNAPSHOT_INTERVAL):
        os.remove(SNAPSHOT_INTERVAL)
        
    print("🧹 Limpeza concluída!")
    print("👋 Webcam moderna encerrada!")

if __name__ == "__main__":
    run_webcam_capture()