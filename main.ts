// The World — Saturday 21 November 2026 (Node 22, standard library only):
// the entry image is entry.png beside this file, and the program copies it
// to /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
// and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const out = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), out);

// Fail loudly if the copied image ever breaks the gate (at most 1 MiB).
const bytes = statSync(out).size;
if (bytes > 1048576) throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB limit`);
console.log(`wrote entry.png (${bytes} bytes)`);
