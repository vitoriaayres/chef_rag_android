#!/usr/bin/env python3
"""
Script para verificar o status da API Key da OpenAI
Verifica se a chave está ativa e quanto tempo falta para usar
"""
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

def test_openai_api_status():
    print("🔍 VERIFICANDO STATUS DA API KEY DA OPENAI")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada no arquivo .env")
        print("📝 Crie um arquivo .env na raiz do projeto com:")
        print("OPENAI_API_KEY=sua_chave_aqui")
        return False
    
    print(f"🔑 API Key encontrada: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # Tentar importar e testar OpenAI
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        print("🧪 Testando conexão com OpenAI...")
        
        # Teste simples e rápido
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Responda apenas: OK"}],
            max_tokens=5
        )
        
        print("✅ API Key ATIVA e funcionando!")
        print(f"📝 Resposta de teste: {response.choices[0].message.content}")
        print(f"⏰ Testado em: {datetime.now().strftime('%H:%M:%S')}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erro ao testar API Key: {error_msg}")
        
        # Verificar tipos específicos de erro
        if "rate_limit" in error_msg.lower():
            print("⏳ Erro de Rate Limit - Você atingiu o limite de uso")
            print("🕐 Aguarde alguns minutos e tente novamente")
            
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
            print("💳 Erro de Billing/Quota - Verifique sua conta OpenAI")
            print("🌐 Acesse: https://platform.openai.com/account/billing")
            
        elif "invalid" in error_msg.lower() or "unauthorized" in error_msg.lower():
            print("🔑 API Key inválida ou não autorizada")
            print("🌐 Verifique em: https://platform.openai.com/api-keys")
            
        elif "You exceeded your current quota" in error_msg:
            print("💸 Quota excedida - Você precisa adicionar créditos")
            print("🌐 Acesse: https://platform.openai.com/account/billing")
            
        # Tentar estimar tempo baseado na mensagem de erro
        try:
            if "try again in" in error_msg.lower():
                # Extrair tempo da mensagem de erro
                import re
                time_match = re.search(r'try again in (\d+)([hms])', error_msg.lower())
                if time_match:
                    amount = int(time_match.group(1))
                    unit = time_match.group(2)
                    
                    if unit == 'h':
                        wait_minutes = amount * 60
                        wait_text = f"{amount} hora(s)"
                    elif unit == 'm':
                        wait_minutes = amount
                        wait_text = f"{amount} minuto(s)"
                    elif unit == 's':
                        wait_minutes = amount / 60
                        wait_text = f"{amount} segundo(s)"
                    
                    available_time = datetime.now() + timedelta(minutes=wait_minutes)
                    print(f"⏰ Tempo de espera: {wait_text}")
                    print(f"🕐 Disponível às: {available_time.strftime('%H:%M:%S')}")
                    
        except Exception:
            pass
            
        return False

def check_env_file():
    """Verifica se existe arquivo .env"""
    if os.path.exists(".env"):
        print("📁 Arquivo .env encontrado")
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                print("✅ OPENAI_API_KEY configurada no .env")
            else:
                print("❌ OPENAI_API_KEY não encontrada no .env")
    else:
        print("❌ Arquivo .env não encontrado")
        print("📝 Crie um arquivo .env com:")
        print("OPENAI_API_KEY=sua_chave_da_openai")
        print("GOOGLE_API_KEY=sua_chave_do_google")

if __name__ == "__main__":
    print("🤖 CHECKER DE STATUS - API OPENAI")
    print("=" * 40)
    
    # Verificar arquivo .env
    check_env_file()
    print()
    
    # Testar API
    success = test_openai_api_status()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUA API KEY ESTÁ FUNCIONANDO!")
        print("🚀 Pode usar o Chef RAG com OpenAI!")
    else:
        print("⏳ API Key não disponível no momento")
        print("🔄 Execute novamente para verificar status")
        print("\n💡 DICA: Use o Google Gemini enquanto espera:")
        print("   - Configure GOOGLE_API_KEY no .env")
        print("   - O sistema já suporta Google Gemini!")