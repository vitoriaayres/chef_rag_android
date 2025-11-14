import sys
import time
import os 
from core_logic import config
from core_logic import rag_system
from core_logic.cleanup_manager import cleanup_manager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
class ImageHandler(FileSystemEventHandler):
    """
    Classe que manipula eventos de sistema de arquivos (novas imagens adicionadas)
    """
    def on_created(self, event):
        """
        Chamado quando um novo arquivo é criado na pasta
        """
        if event.is_directory:
            return
        
        file_path = event.src_path
        fili_name, file_ext = os.path.splitext(file_path)

        if file_ext.lower() in IMAGE_EXTENSIONS:
            print("\n================================")
            print(f"📸 Nova imagem detectada: {os.path.basename(file_path)}")
            
            # Registrar imagem para limpeza automática
            cleanup_manager.add_image_to_cleanup(file_path)

            ingredient = rag_system.extract_ingredients_from_image(file_path)

            if "Erro" in ingredient:
                print(f"❌ Falha ao extrair ingredientes: {ingredient}")
                return
            
            receitas = rag_system.find_recipes_by_ingredient(ingredient, file_path, "folder")

            print(f"✅ Sugestão de receita gerada com sucesso para o ingrediente: {ingredient}")
            print(receitas)
            print("================================\n")
            print(f"Aguardando novas imagens na pasta '{config.IMAGE_WATCH_FOLDER}'...")

def start_monitoring():
    """
    Inicia o monitoramento da pasta para novas imagens
    """
    if not os.path.exists(config.IMAGE_WATCH_FOLDER):
        print(f"Criando pasta de monitoramento: {config.IMAGE_WATCH_FOLDER}")
        os.makedirs(config.IMAGE_WATCH_FOLDER)

    path = config.IMAGE_WATCH_FOLDER
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print("=========================================")
    print("Agente inicializado")
    print("Coloque um arquivo .jpg ou .png na pasta abaixo para processá-lo:")
    print(f"📁 {config.IMAGE_WATCH_FOLDER}")
    print("Pressione Ctrl+C para sair.")
    print("============================================")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nServidor de monitoramento encerrado.")
    observer.join()

if __name__ == "__main__":
    if not config.GOOGLE_API_KEY:
        print("Erro: A chave da API do Google não está configurada. Por favor, defina GOOGLE_API_KEY no arquivo .env")
        sys.exit(1)
    start_monitoring()
