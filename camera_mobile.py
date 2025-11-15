#!/usr/bin/env python3
"""
Chef RAG - Interface Mobile para Câmera
Permite usar a câmera do celular via navegador web
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import socket
import threading
import webbrowser
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import sys

# Para QR code simples
try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
    print("⚠️ qrcode não instalado. QR code não será gerado.")

# Adicionar o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Importar sistema RAG
rag_system = None
try:
    from core_logic import sistema_rag
    rag_system = RAGSystem()
    print("✅ Sistema RAG carregado com sucesso!")
except Exception as e:
    print(f"⚠️ Sistema RAG não disponível: {e}")
    print("🔄 Funcionando em modo demo")

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

@app.route('/')
def mobile_interface():
    """Interface principal para mobile"""
    return render_template('mobile_camera.html')

@app.route('/capture', methods=['POST'])
def capture_photo():
    """Processa foto capturada pelo celular"""
    try:
        # Verificar se há dados JSON
        if not request.json:
            return jsonify({'success': False, 'error': 'Dados JSON não recebidos'})
            
        # Recebe dados da imagem em base64
        image_data = request.json.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'Nenhuma imagem recebida'})
        
        # Remove o prefixo data:image/jpeg;base64,
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decodifica base64
        image_bytes = base64.b64decode(image_data)
        
        # Converte para imagem PIL
        image = Image.open(BytesIO(image_bytes))
        
        # Salva a imagem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mobile_capture_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Converte para RGB se necessário
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        image.save(filepath, 'JPEG', quality=90)
        print(f"📱 Imagem salva: {filename}")
        
        # Processa com o sistema RAG
        result = process_image_with_rag(filepath)
        
        return jsonify({
            'success': True,
            'result': result,
            'filename': filename
        })
        
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
        return jsonify({'success': False, 'error': str(e)})

def process_image_with_rag(image_path):
    """Processa imagem com sistema RAG"""
    try:
        if not rag_system:
            # Modo demo quando RAG não está disponível
            return {
                'ingredient': 'Demo - Tomate Cherry',
                'recipes': '📚 **DO SEU LIVRO DE RECEITAS:**\n\n🍅 **RECEITAS COM TOMATE CHERRY:**\n\n1. **Salada Caprese** - Página 45\nTomate cherry, mussarela de búfala, manjericão\n\n2. **Bruschetta de Tomate** - Página 67\nPão italiano, tomate cherry, alho, azeite\n\n3. **Massa ao Pomodoro** - Página 89\nMacarrão, tomate cherry, manjericão fresco',
                'count': 3
            }
        
        print(f"🔍 Analisando imagem: {image_path}")
        
        # Extrai ingredientes
        ingredient = sistema_rag.extract_ingredients_from_image(image_path)
        
        if "Erro" in ingredient or not ingredient:
            return {
                'ingredient': None,
                'recipes': None,
                'count': 0,
                'error': 'Ingrediente não identificado. Tente uma foto mais clara.'
            }
        
        print(f"✅ Ingrediente detectado: {ingredient}")
        
        # Busca receitas
        recipes = sistema_rag.find_recipes_by_ingredient(ingredient, image_path, "mobile")
        recipe_count = recipes.count("Página") if recipes else 0
        
        if not recipes or recipe_count == 0:
            return {
                'ingredient': ingredient,
                'recipes': None,
                'count': 0,
                'error': f'Nenhuma receita encontrada para {ingredient}'
            }
        
        return {
            'ingredient': ingredient,
            'recipes': recipes,
            'count': recipe_count
        }
        
    except Exception as e:
        print(f"❌ Erro no RAG: {e}")
        return {
            'ingredient': None,
            'recipes': None,
            'count': 0,
            'error': f'Erro no processamento: {str(e)}'
        }

@app.route('/history')
def get_history():
    """Retorna histórico de análises"""
    try:
        files = []
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                if filename.startswith('mobile_capture_'):
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    stat = os.stat(filepath)
                    files.append({
                        'filename': filename,
                        'timestamp': datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M"),
                        'size': f"{stat.st_size / 1024:.1f} KB"
                    })
        
        # Ordena por data (mais recente primeiro)
        files.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({'success': True, 'files': files[:10]})  # Últimas 10
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve arquivos uploadados"""
    return send_from_directory(UPLOAD_FOLDER, filename)

def generate_qr_code(url):
    """Gera QR code para acesso mobile"""
    if not QR_AVAILABLE:
        return None
        
    try:
        # Configuração simples do QR code
        qr = qrcode.QRCode(version=1)
        qr.add_data(url)
        qr.make()
        
        # Cria imagem do QR code
        img = qr.make_image()
        
        # Salva temporariamente
        qr_path = os.path.join(os.getcwd(), "qr_code_mobile.png")
        
        # Salva usando with open para garantir compatibilidade
        with open(qr_path, 'wb') as f:
            img.save(f, 'PNG')
        
        return qr_path
    except Exception as e:
        print(f"⚠️ Erro ao gerar QR code: {e}")
        return None

def show_qr_code_file(qr_path):
    """Tenta abrir o arquivo do QR code"""
    if not qr_path or not os.path.exists(qr_path):
        return False
        
    try:
        import subprocess
        import platform
        
        system = platform.system()
        if system == "Windows":
            subprocess.run(['start', qr_path], shell=True, check=False)
        elif system == "Darwin":  # macOS
            subprocess.run(['open', qr_path], check=False)
        elif system == "Linux":
            subprocess.run(['xdg-open', qr_path], check=False)
        return True
    except Exception:
        return False

def print_mobile_instructions(url):
    """Imprime instruções para acesso mobile com QR code"""
    print("\n" + "="*80)
    print("📱 CHEF RAG - CÂMERA MOBILE ATIVA")
    print("="*80)
    print(f"🌐 URL: {url}")
    print("="*80)
    
    # Gerar QR code se disponível
    if QR_AVAILABLE:
        qr_path = generate_qr_code(url)
        if qr_path:
            print("✅ QR CODE GERADO COM SUCESSO!")
            print(f"💾 Arquivo: {qr_path}")
            
            # Tenta abrir o arquivo
            if show_qr_code_file(qr_path):
                print("📱 QR code aberto automaticamente!")
            else:
                print("💡 Abra manualmente o arquivo: qr_code_mobile.png")
        else:
            print("⚠️ Erro ao gerar QR code")
    else:
        print("💡 Para QR code, instale: pip install qrcode[pil]")
    
    print("="*80)
    print("📱 COMO CONECTAR SEU CELULAR:")
    print("   1️⃣ PC e celular na MESMA REDE WiFi ✅")
    print("   2️⃣ ESCANEIE o QR code acima 📱")
    print(f"   3️⃣ OU digite no navegador: {url}")
    print("   4️⃣ Permita acesso à câmera 📷")
    print("   5️⃣ Aponte e capture ingredientes! 🥕")
    print("="*80)
    print("🔧 CONTROLES:")
    print("   • Mantenha este terminal ABERTO")
    print("   • Ctrl+C para encerrar")
    print("="*80)

def start_mobile_server(host='0.0.0.0', port=5001):
    """Inicia servidor mobile"""
    try:
        # Obtém IP local
        local_ip = get_local_ip()
        url = f"http://{local_ip}:{port}"
        
        print_mobile_instructions(url)
        
        print("🚀 Iniciando servidor Flask...")
        
        # Inicia servidor Flask
        app.run(host=host, port=port, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\n👋 Servidor mobile encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        print("💡 Verifique se a porta 5001 não está em uso")

if __name__ == "__main__":
    start_mobile_server()