import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
const root = resolve('dist');
const mime = { '.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'text/javascript', '.webp':'image/webp', '.png':'image/png', '.jpg':'image/jpeg', '.svg':'image/svg+xml', '.woff2':'font/woff2', '.ttf':'font/ttf', '.pdf':'application/pdf', '.mp4':'video/mp4', '.txt':'text/plain', '.xml':'application/xml' };
http.createServer(async (req,res) => {
  try {
    const url = new URL(req.url,'http://localhost');
    let path = resolve(root, '.' + decodeURIComponent(url.pathname));
    if(path !== root && !path.startsWith(root+sep)){res.writeHead(403).end();return;}
    if((await stat(path)).isDirectory()) path = resolve(path,'index.html');
    const data = await readFile(path);
    res.writeHead(200,{'Content-Type':mime[extname(path)]||'application/octet-stream','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});
    if(req.method==='HEAD')res.end();else res.end(data);
  } catch {res.writeHead(404,{'Content-Type':'text/html; charset=utf-8'}).end(await readFile(resolve(root,'404.html')).catch(()=> 'Page not found'));}
}).listen(4173,'127.0.0.1',()=> console.log('Local: http://127.0.0.1:4173'));
