import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(fileURLToPath(new URL('.', import.meta.url)));
const port = Number(process.env.PORT || 4173);
const mime = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.json':'application/json'};
const server = createServer(async(req,res)=>{
  try {
    const requested = decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const path = resolve(root, '.'+requested, requested.endsWith('/')?'index.html':'');
    if(path!==root && !path.startsWith(root+sep)) {res.writeHead(403);res.end('Forbidden');return;}
    if((await stat(path)).isDirectory()) {res.writeHead(403);res.end('Forbidden');return;}
    const body = await readFile(path);
    res.writeHead(200, {'Content-Type': mime[extname(path)]||'application/octet-stream','X-Content-Type-Options':'nosniff','Cache-Control':'no-cache'});
    res.end(body);
  }catch(err){res.writeHead(404);res.end('Not found');}
});
server.listen(port,'127.0.0.1',()=>console.log(`Server CPU Strategy Lab → http://127.0.0.1:${port}`));