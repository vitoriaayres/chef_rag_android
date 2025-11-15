# Chef RAG Mobile - Script de Inicialização
# Este script inicia tanto o backend da API quanto o Metro bundler do React Native

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Chef RAG Mobile - Iniciando Sistema" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Diretório base do projeto
$baseDir = "C:\Users\Interfocus\Desktop\projetos_pessoais\chef_rag_v2"
$reactNativeDir = Join-Path $baseDir "android_rag_chef"

# Verificar se os diretórios existem
if (!(Test-Path $baseDir)) {
    Write-Host "❌ Erro: Diretório base não encontrado: $baseDir" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $reactNativeDir)) {
    Write-Host "❌ Erro: Diretório React Native não encontrado: $reactNativeDir" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Iniciando API Backend..." -ForegroundColor Green
# Iniciar a API em background
Set-Location $baseDir
$apiProcess = Start-Process -FilePath "python" -ArgumentList "mobile_api.py" -PassThru -WindowStyle Normal

Write-Host "⏳ Aguardando API inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Testar se a API está funcionando
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API Backend iniciada com sucesso!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  API pode estar iniciando ainda... continuando..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📱 Iniciando Metro Bundler..." -ForegroundColor Green
Set-Location $reactNativeDir

# Iniciar Metro em background
$metroProcess = Start-Process -FilePath "npm" -ArgumentList "start" -PassThru -WindowStyle Normal

Write-Host ""
Write-Host "✅ Ambos os serviços foram iniciados!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Status dos Processos:" -ForegroundColor Cyan
Write-Host "- API Backend PID: $($apiProcess.Id)" -ForegroundColor White
Write-Host "- Metro Bundler PID: $($metroProcess.Id)" -ForegroundColor White
Write-Host ""
Write-Host "🔗 URLs Importantes:" -ForegroundColor Cyan
Write-Host "- API Health Check: http://localhost:5000/api/health" -ForegroundColor White
Write-Host "- Metro Bundler: http://localhost:8081" -ForegroundColor White
Write-Host ""
Write-Host "🛠️  Para desenvolvimento:" -ForegroundColor Cyan
Write-Host "1. Abra um emulador Android ou conecte um dispositivo" -ForegroundColor White
Write-Host "2. Execute 'npm run android' no diretório android_rag_chef" -ForegroundColor White
Write-Host "3. Use 'r' no Metro para reload, 'd' para developer menu" -ForegroundColor White
Write-Host ""
Write-Host "Para parar os serviços, feche as janelas ou use Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Manter o script aberto
Write-Host "Pressione qualquer tecla para finalizar e fechar os serviços..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Finalizar processos se ainda estiverem rodando
if (!$apiProcess.HasExited) {
    Write-Host "🛑 Finalizando API Backend..." -ForegroundColor Yellow
    Stop-Process -Id $apiProcess.Id -Force -ErrorAction SilentlyContinue
}

if (!$metroProcess.HasExited) {
    Write-Host "🛑 Finalizando Metro Bundler..." -ForegroundColor Yellow
    Stop-Process -Id $metroProcess.Id -Force -ErrorAction SilentlyContinue
}

Write-Host "✅ Serviços finalizados!" -ForegroundColor Green