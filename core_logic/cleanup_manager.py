"""
Sistema de limpeza automática de imagens
"""

import os
import signal
import sys
import atexit
import glob
from pathlib import Path

class ImageCleanupManager:
    """Gerencia a limpeza automática de imagens quando o programa é encerrado"""
    
    def __init__(self, images_folder: str = "data/imagens"):
        self.images_folder = Path(images_folder)
        self.cleanup_enabled = True
        self.initial_images = set()
        
        # Registrar handlers de cleanup
        self._register_cleanup_handlers()
        
        # Registrar imagens existentes no início
        self._register_existing_images()
    
    def _register_existing_images(self):
        """Registra imagens que já existem na pasta"""
        if self.images_folder.exists():
            image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
            for extension in image_extensions:
                for img_path in self.images_folder.glob(extension):
                    self.initial_images.add(img_path.name)
            print(f"📁 Imagens registradas para limpeza: {len(self.initial_images)} arquivos")
    
    def _register_cleanup_handlers(self):
        """Registra handlers para diferentes tipos de encerramento"""
        # Handler para saída normal do programa
        atexit.register(self._cleanup_on_exit)
        
        # Handler para Ctrl+C (SIGINT)
        signal.signal(signal.SIGINT, self._cleanup_on_signal)
        
        # Handler para terminação (SIGTERM) - Windows
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self._cleanup_on_signal)
    
    def _cleanup_on_exit(self):
        """Executa limpeza na saída normal do programa"""
        if self.cleanup_enabled:
            self._perform_cleanup()
    
    def _cleanup_on_signal(self, signum, frame):
        """Executa limpeza quando recebe sinal de interrupção"""
        print(f"\n🛑 Recebido sinal {signum}, executando limpeza...")
        if self.cleanup_enabled:
            self._perform_cleanup()
        sys.exit(0)
    
    def _perform_cleanup(self):
        """Executa a limpeza das imagens"""
        try:
            if not self.images_folder.exists():
                return
            
            cleaned_count = 0
            image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
            
            print("🧹 Iniciando limpeza de imagens...")
            
            for extension in image_extensions:
                for img_path in self.images_folder.glob(extension):
                    try:
                        img_path.unlink()  # Remove o arquivo
                        cleaned_count += 1
                        print(f"  🗑️ Removido: {img_path.name}")
                    except Exception as e:
                        print(f"  ❌ Erro ao remover {img_path.name}: {e}")
            
            print(f"✅ Limpeza concluída: {cleaned_count} imagens removidas")
            
        except Exception as e:
            print(f"❌ Erro durante limpeza: {e}")
    
    def disable_cleanup(self):
        """Desabilita a limpeza automática"""
        self.cleanup_enabled = False
        print("🔒 Limpeza automática desabilitada")
    
    def enable_cleanup(self):
        """Habilita a limpeza automática"""
        self.cleanup_enabled = True
        print("🔓 Limpeza automática habilitada")
    
    def manual_cleanup(self):
        """Executa limpeza manual"""
        print("🧹 Executando limpeza manual...")
        self._perform_cleanup()
    
    def add_image_to_cleanup(self, image_path: str):
        """Adiciona uma imagem específica para limpeza"""
        image_name = Path(image_path).name
        if image_name not in self.initial_images:
            self.initial_images.add(image_name)
            print(f"📝 Imagem adicionada para limpeza: {image_name}")

# Instância global do gerenciador
cleanup_manager = ImageCleanupManager()

def setup_image_cleanup(images_folder: str = "data/imagens"):
    """Configura o sistema de limpeza de imagens"""
    global cleanup_manager
    cleanup_manager = ImageCleanupManager(images_folder)
    return cleanup_manager

def disable_image_cleanup():
    """Desabilita a limpeza automática de imagens"""
    cleanup_manager.disable_cleanup()

def enable_image_cleanup():
    """Habilita a limpeza automática de imagens"""
    cleanup_manager.enable_cleanup()

def manual_image_cleanup():
    """Executa limpeza manual de imagens"""
    cleanup_manager.manual_cleanup()