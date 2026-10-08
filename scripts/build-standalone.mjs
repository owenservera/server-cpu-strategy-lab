import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
const [html,css,data,economics,app]=await Promise.all(['index.html','styles.css','data.js','economics.js','app.js'].map(file=>readFile(resolve(root,file),'utf8')));
const dataInline=data.replace(/\bexport\s+(?=const\s)/g,'');
const economicsInline=economics.replace(/\bexport\s+(?=function\s)/g,'');
const appInline=app.replace(/^import\s+.*?;\s*$/gm,'');
const output=html.replace('<link rel="stylesheet" href="./styles.css" />',`<style>\n${css}\n</style>`)
 .replace('<script type="module" src="./app.js"></script>',`<script>\n${dataInline}\n${economicsInline}\n${appInline}\n</script>`)
 .replace('<link rel="icon" href="./assets/favicon.svg" type="image/svg+xml" />','');
const location=process.argv[2]||resolve(root,'standalone.html');
await writeFile(location,output,'utf8');
console.log(`Created standalone browser-ready dashboard: ${location}`);