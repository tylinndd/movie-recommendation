import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const apiBase = (process.env.API_URL || '').replace(/\/$/, '');
const content = `// Generated at build time — do not edit manually on Vercel
window.API_BASE = ${JSON.stringify(apiBase)};
`;

fs.writeFileSync(path.join(root, 'static', 'config.js'), content);
console.log(
  apiBase
    ? `Wrote static/config.js → API_BASE = ${apiBase}`
    : 'Wrote static/config.js → API_BASE = "" (same-origin; set API_URL on Vercel)'
);
