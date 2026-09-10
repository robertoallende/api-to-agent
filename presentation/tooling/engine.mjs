// Custom Marp CLI engine that enables Shiki syntax highlighting.
//
// Shiki wraps every source line in a `<span class="line">` element, which lets
// us render line numbers with a pure-CSS counter (see the `style:` block in
// presentation.md). Marp CLI's default highlighter (highlight.js) does not
// produce per-line elements, so this engine is required for line numbers.
//
// Usage: marp --engine ./engine.mjs presentation.md -o presentation.html

import { Marp } from '@marp-team/marp-core'
import shiki from '@marp-team/marp-core/plugins/shiki'

export default (opts) => new Marp(opts).use(shiki())
