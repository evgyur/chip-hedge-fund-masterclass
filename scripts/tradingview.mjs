#!/usr/bin/env node
/* Workshop transport: one pinned local server, forced read-only. No config writer. */
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
if(Number(process.versions.node.split('.')[0])<24){console.error('TradingView Chip requires Node.js 24+');process.exit(2)}
const runtime=process.env.TV_DATA_DIR;
if(!runtime||!path.isAbsolute(runtime)){console.error('Set TV_DATA_DIR to a private absolute directory outside this repository');process.exit(2)}
// Resolve existing ancestors so a symlink cannot route runtime back into published source.
function physical(p){let suffix=[];while(!fs.existsSync(p)){suffix.unshift(path.basename(p));const parent=path.dirname(p);if(parent===p)break;p=parent}return path.resolve(fs.realpathSync(p),...suffix)}
const realRoot=fs.realpathSync(root),realRuntime=physical(path.resolve(runtime));
if(realRuntime===realRoot||realRuntime.startsWith(realRoot+path.sep)){console.error('Runtime must stay outside the repository');process.exit(2)}
const child=spawn(process.execPath,[path.join(root,'vendor/tradingview-chip/src/server.mjs')],{stdio:'inherit',env:{...process.env,TV_READONLY:'1',TV_ENABLE_GENERIC_UI:'0',TV_DATA_DIR:realRuntime}});
child.on('error',()=>{console.error('Could not launch pinned TradingView server');process.exit(2)});
child.on('exit',(code,signal)=>{if(signal){process.exitCode=1}else process.exitCode=code??1});
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>child.kill(signal));
