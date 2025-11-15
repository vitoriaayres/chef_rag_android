#!/usr/bin/env python3
"""
Script para iniciar tanto o backend Chef RAG quanto o app React Native
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class ChefRAGLauncher:
    def __init__(self):
        self.backend_process = None
        self.metro_process = None
        self.android_process = None
        self.base_path = Path(__file__).parent
        self.mobile_path = self.base_path / "android_rag_chef"
    
    def check_dependencies(self):
        """Verificar se todas as dependências estão instaladas"""
        print("🔍 Verificando dependências...")
        
        # Verificar Python
        try:
            import flask
            import flask_cors
            print("✅ Flask instalado")
        except ImportError:
            print("❌ Flask não encontrado. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
        
        # Verificar Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js {result.stdout.strip()} instalado")
            else:
                print("❌ Node.js não encontrado")
                return False
        except FileNotFoundError:
            print("❌ Node.js não encontrado")
            return False
        
        # Verificar React Native CLI
        try:
            result = subprocess.run(["npx", "react-native", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ React Native CLI disponível")
            else:
                print("❌ React Native CLI não encontrado")
        except FileNotFoundError:
            print("❌ React Native CLI não encontrado")
        
        # Verificar se node_modules existe
        if (self.mobile_path / "node_modules").exists():
            print("✅ Dependências React Native instaladas")
        else:
            print("❌ Dependências React Native não instaladas")
            print("📦 Instalando dependências...")
            os.chdir(self.mobile_path)
            subprocess.run(["npm", "install"])
            os.chdir(self.base_path)
        
        return True
    
    def start_backend(self):
        """Iniciar o backend Flask"""
        print("🚀 Iniciando backend Chef RAG...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "mobile_api.py"],
                cwd=self.base_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Thread para mostrar output do backend
            def show_backend_output():
                for line in iter(self.backend_process.stdout.readline, ''):
                    if line:
                        print(f"[BACKEND] {line.strip()}")
                        if "Running on" in line:
                            print("✅ Backend Flask iniciado com sucesso!")
            
            threading.Thread(target=show_backend_output, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return False
    
    def start_metro(self):
        """Iniciar o Metro bundler"""
        print("📱 Iniciando Metro bundler...")
        try:
            self.metro_process = subprocess.Popen(
                ["npx", "react-native", "start"],
                cwd=self.mobile_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Thread para mostrar output do Metro
            def show_metro_output():
                for line in iter(self.metro_process.stdout.readline, ''):
                    if line:
                        print(f"[METRO] {line.strip()}")
                        if "Loading dependency graph" in line or "Metro waiting on" in line:
                            print("✅ Metro bundler iniciado com sucesso!")
            
            threading.Thread(target=show_metro_output, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar Metro: {e}")
            return False
    
    def check_android_device(self):
        """Verificar se há dispositivo Android conectado ou emulador"""
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            devices = [line for line in result.stdout.split('\n') if 'device' in line and 'List' not in line]
            
            if devices:
                print(f"✅ {len(devices)} dispositivo(s) Android encontrado(s)")
                return True
            else:
                print("⚠️  Nenhum dispositivo Android encontrado")
                print("💡 Para testar:")
                print("   1. Conecte um dispositivo Android via USB")
                print("   2. Ou inicie um emulador Android")
                return False
                
        except FileNotFoundError:
            print("⚠️  ADB não encontrado - Android SDK não instalado")
            return False
    
    def start_android_app(self):
        """Iniciar o app no Android"""
        if not self.check_android_device():
            print("⏭️  Pulando inicialização do app Android")
            return False
        
        print("📱 Iniciando app no Android...")
        try:
            # Dar tempo para o Metro inicializar
            time.sleep(5)
            
            self.android_process = subprocess.Popen(
                ["npx", "react-native", "run-android"],
                cwd=self.mobile_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Thread para mostrar output do Android
            def show_android_output():
                for line in iter(self.android_process.stdout.readline, ''):
                    if line:
                        print(f"[ANDROID] {line.strip()}")
                        if "BUILD SUCCESSFUL" in line or "Installing APK" in line:
                            print("✅ App Android instalado com sucesso!")
            
            threading.Thread(target=show_android_output, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar app Android: {e}")
            return False
    
    def stop_all(self):
        """Parar todos os processos"""
        print("\n🛑 Parando todos os serviços...")
        
        if self.android_process:
            self.android_process.terminate()
            print("✅ App Android parado")
        
        if self.metro_process:
            self.metro_process.terminate()
            print("✅ Metro bundler parado")
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend Flask parado")
    
    def run(self):
        """Executar o sistema completo"""
        print("=" * 60)
        print("🧑‍🍳 CHEF RAG - Iniciando Sistema Completo")
        print("=" * 60)
        
        try:
            # Verificar dependências
            if not self.check_dependencies():
                print("❌ Dependências não atendidas")
                return
            
            print("\n📋 Ordem de inicialização:")
            print("1. 🐍 Backend Flask (mobile_api.py)")
            print("2. 📦 Metro Bundler (React Native)")
            print("3. 📱 App Android (se dispositivo disponível)")
            print()
            
            # Iniciar backend
            if not self.start_backend():
                return
            
            time.sleep(3)  # Aguardar backend inicializar
            
            # Iniciar Metro
            if not self.start_metro():
                return
            
            time.sleep(5)  # Aguardar Metro inicializar
            
            # Iniciar Android (opcional)
            self.start_android_app()
            
            print("\n" + "=" * 60)
            print("🎉 SISTEMA CHEF RAG INICIADO COM SUCESSO!")
            print("=" * 60)
            print("🌐 Backend API: http://localhost:5000")
            print("📱 Metro Bundler: http://localhost:8081")
            print("📖 Para testar a API: http://localhost:5000/api/health")
            print()
            print("⚡ Comandos úteis:")
            print("   Ctrl+C - Parar todos os serviços")
            print("   R - Recarregar app React Native")
            print("   D - Abrir menu de debug")
            print("=" * 60)
            
            # Manter o script rodando
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Parando sistema...")
                self.stop_all()
                
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            self.stop_all()

def main():
    launcher = ChefRAGLauncher()
    launcher.run()

if __name__ == "__main__":
    main()