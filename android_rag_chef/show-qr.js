const qrcode = require('qrcode');
const { networkInterfaces } = require('os');

async function showQRCode() {
    console.log('\n🚀 Chef RAG Mobile App');
    console.log('📱 Para testar no celular com Expo Go:\n');

    // Obter IP local
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
    
    console.log('📋 Link direto:', expURL);
    console.log('🌐 URL web:', `http://${localIP}:8081\n`);

    try {
        console.log('📱 QR Code para escanear no Expo Go:');
        const qrString = await qrcode.toString(expURL, { 
            type: 'terminal', 
            small: false,
            margin: 1 
        });
        console.log(qrString);
        
        console.log('\n📖 Instruções:');
        console.log('1. Baixe "Expo Go" na Play Store');
        console.log('2. Abra o Expo Go');
        console.log('3. Escaneie o QR code acima');
        console.log('4. Aguarde carregar o app');
        
        console.log('\n🔄 Agora execute em outro terminal: npm start');
        
    } catch (err) {
        console.log('❌ Erro ao gerar QR code:', err.message);
        console.log('📋 Use o link direto no Expo Go:', expURL);
    }
}

showQRCode();