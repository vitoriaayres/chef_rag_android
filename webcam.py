import cv2 
import os 
import time 
from core_logic import config 
from core_logic import rag_system

SNAPSHOT_INTERVAL = os.path.join(config.BASE_DIR, "..", "temp_snapshot.jpg")

def run_webcam_capture():
    """
    Inicia a webcam e escaneia ingredientes quando o usuário pressiona a tecla 'E'.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a webcam.")
        print("Verifique se a webcam está conectada corretamente e tente novamente.")
        return
    
    # Configurações da câmera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Força a criação da janela
    cv2.namedWindow("Webcam - RAG Ingredientes", cv2.WINDOW_AUTOSIZE)
        
    print("\n================================")
    print("RAG ATIVADO -- MODO WEBCAM")
    print("\n================================")
    print("Aponte o ingrediente para a câmera....")
    print("Pressione 'E' para escanear o ingrediente.")
    print("Pressione 'Q' para sair.")
    print("\n ---AGUARDANDO COMANDO-----")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro: Não foi possível capturar o quadro da webcam.")
            break
        
        color = (0, 255, 0)

        cv2.putText(frame, "Pressione 'E' para escanear o ingrediente", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, "Pressione 'Q' para sair", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("Webcam - RAG Ingredientes", frame)

        # Aumenta o tempo de espera para melhor captura de teclas
        key = cv2.waitKey(30) & 0xFF
        
        # Verifica se a janela ainda existe
        if cv2.getWindowProperty("Webcam - RAG Ingredientes", cv2.WND_PROP_VISIBLE) < 1:
            print("Janela foi fechada. Encerrando...")
            break
        
        if key == ord('q'):
            print("Encerrando a webcam...")
            break
            
        if key == ord('e'):
            print("\n ============================================")
            print("Imagem capturada. Processando o ingrediente...")

            cv2.imwrite(SNAPSHOT_INTERVAL, frame)
            ingredient = rag_system.extract_ingredients_from_image(SNAPSHOT_INTERVAL)

            if "Erro" in ingredient:
                print("Não foi possível identificar o ingrediente")
                continue
                
            recipes = rag_system.find_recipes_by_ingredient(ingredient, SNAPSHOT_INTERVAL, "webcam")
            
            if not recipes:
                print(f"Nenhuma receita encontrada com o ingrediente: {ingredient}")
                continue

            print("\n--- SUGESTÃO DO CHEF ---")
            print(recipes)
            print("=============================================")
            print("Aguardando próximo comando...")

    cap.release()
    cv2.destroyAllWindows()

    if os.path.exists(SNAPSHOT_INTERVAL):
        os.remove(SNAPSHOT_INTERVAL)

if __name__ == "__main__":
    run_webcam_capture()