import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'fs'; import path from 'path';
const [,, propsFile, out, framesArg] = process.argv;
const inputProps = JSON.parse(fs.readFileSync(propsFile, 'utf8'));
const browserExecutable = process.env.CHROME;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve('public')});
const composition = await selectComposition({serveUrl, id: 'Criativo', inputProps, browserExecutable});
const opts = {composition, serveUrl, codec: 'h264', scale: Number(process.env.SCALE || 1), outputLocation: out, inputProps, browserExecutable, concurrency: 2, crf: 20,
  audioBitrate: '192k', chromiumOptions: {gl: 'swangle'}, timeoutInMilliseconds: 120000,
  onProgress: ({progress}) => { if (Math.round(progress*100)%10===0) process.stdout.write(`\r${Math.round(progress*100)}%`); }};
if (framesArg) { const [a,b] = framesArg.split('-').map(Number); opts.frameRange = [a,b]; }
await renderMedia(opts);
console.log('\nOK', out);
