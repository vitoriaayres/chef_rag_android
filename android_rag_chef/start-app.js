const { spawn } = require('child_process');
const QRCode = require('qrcode');
const os = require('os');

// Função para obter IP local
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    return 'localhost';
}

async function startApp() {
    const localIP = getLocalIP();
    const port = 8081;
    const expUrl = `exp://${localIP}:${port}`;
    
    console.log('🚀 Chef RAG Mobile App');
    console.log('📱 Para testar no celular:');
    console.log('1. Baixe o app "Expo Go" na Play Store');
    console.log('2. Escaneie o QR code abaixo:');
    console.log('');
    
    try {
        const qrString = await QRCode.toString(expUrl, { type: 'terminal' });
        console.log(qrString);
    } catch (err) {
        console.log('QR Code não disponível, use este link:');
    }
    
    console.log('');
    console.log(`📋 Link direto: ${expUrl}`);
    console.log(`🌐 URL local: http://${localIP}:${port}`);
    console.log('');
    console.log('🔄 Iniciando Metro Bundler...');
    
    // Iniciar Metro
    const metro = spawn('npx', ['react-native', 'start', '--port', port.toString()], {
        stdio: 'inherit',
        shell: true
    });
    
    metro.on('close', (code) => {
        console.log(`Metro bundler fechado com código ${code}`);
    });
}

startApp().catch(console.error);