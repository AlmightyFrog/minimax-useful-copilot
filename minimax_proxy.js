const http = require('http');
const https = require('https');

const PORT = process.env.MINIMAX_PROXY_PORT || 3333;
const API_KEY = process.env.MINIMAX_API_KEY;

if (!API_KEY) {
    console.error("ERROR: MINIMAX_API_KEY environment variable is not set!");
    process.exit(1);
}

http.createServer((req, res) => {
    let bodyCollector = [];
    req.on('data', (chunk) => bodyCollector.push(chunk));
    
    req.on('end', () => {
        const fullBody = Buffer.concat(bodyCollector).toString();
        
        console.log(`\n--- [ REQUEST: ${new Date().toLocaleTimeString()} ] ---`);
        console.log(`Path: ${req.url}`);

        const cleanHeaders = {
            'X-Api-Key': API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream',
            'Host': 'api.minimax.io'
        };

        const options = {
            hostname: 'api.minimax.io',
            path: req.url,
            method: 'POST',
            headers: cleanHeaders
        };

        const proxy = https.request(options, (targetRes) => {
            console.log(`Status from MiniMax: ${targetRes.statusCode}`);
            
            res.writeHead(targetRes.statusCode, {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            });

            targetRes.on('data', (chunk) => {
                res.write(chunk);
            });

            targetRes.on('end', () => {
                console.log("--- [ STREAM END ] ---");
                res.end();
            });
        });

        proxy.on('error', (e) => {
            console.error(`ERROR: Proxy error: ${e.message}`);
            res.end();
        });

        proxy.write(fullBody);
        proxy.end();
    });
}).listen(PORT, () => {
    console.log("========================================");
    console.log(`MiniMax Proxy active on port ${PORT}`);
    console.log(`Key loaded: ${API_KEY.substring(0, 6)}...`);
    console.log("========================================");
});
