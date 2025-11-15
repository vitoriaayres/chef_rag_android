const { execSync } = require('child_process');
const qrcode = require('qrcode');

async function startApp() {
    console.log('🚀 Chef RAG Mobile App');
    console.log('📱 Para testar no celular:');
    console.log('1. Baixe o app "Expo Go" na Play Store');
    console.log('2. Use um dos métodos abaixo:\n');

    // Obter IP local
    const { networkInterfaces } = require('os');
    const nets = networkInterfaces();
    let localIP = 'localhost';
    
    for (const name of Object.keys(nets)) {
        for (const net of nets[name]) {
            if (net.family === 'IPv4' && !net.internal) {
                localIP = net.address;
                break;
            }
        }
    }

    const expURL = `exp://${localIP}:8081`;
    const webURL = `http://${localIP}:8081`;

    console.log('📋 URLs para testar:');
    console.log(`   Expo Go: ${expURL}`);
    console.log(`   Web: ${webURL}\n`);

    try {
        console.log('📱 QR Code para Expo Go:');
        const qrString = await qrcode.toString(expURL, { type: 'terminal', small: true });
        console.log(qrString);
    } catch (err) {
        console.log('❌ Não foi possível gerar QR code:', err.message);
        console.log('📋 Use o link direto:', expURL);
    }

    console.log('🔄 Iniciando React Native Metro...');
    
    try {
        execSync('npm start', { stdio: 'inherit' });
    } catch (error) {
        console.log('❌ Erro ao iniciar Metro:', error.message);
    }
}

startApp();