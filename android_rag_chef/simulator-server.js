const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const port = 3000;

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    let pathname = parsedUrl.pathname;
    
    // Se for a raiz, serve o arquivo HTML
    if (pathname === '/') {
        pathname = '/android-simulator.html';
    }
    
    const filePath = path.join(__dirname, pathname);
    
    // Verificar se o arquivo existe
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
            res.writeHead(404, {'Content-Type': 'text/plain'});
            res.end('Arquivo não encontrado');
            return;
        }
        
        // Determinar content-type
        const ext = path.extname(filePath).toLowerCase();
        const contentTypes = {
            '.html': 'text/html',
            '.js': 'text/javascript',
            '.css': 'text/css',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg'
        };
        
        const contentType = contentTypes[ext] || 'text/plain';
        
        // Ler e servir arquivo
        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(500, {'Content-Type': 'text/plain'});
                res.end('Erro interno do servidor');
                return;
            }
            
            res.writeHead(200, {
                'Content-Type': contentType,
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'
            });
            res.end(data);
        });
    });
});

server.listen(port, () => {
    console.log(`🚀 Simulador Android disponível em: http://localhost:${port}`);
    console.log('📱 Abra este link no VS Code Simple Browser');
});