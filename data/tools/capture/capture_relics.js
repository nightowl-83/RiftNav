// Capture the relic catalogue from https://stellaris.paradoxwikis.com/Relics.
//
// The wiki sits behind a browser challenge that blocks scripted API clients, so this runs
// in a normal browser tab: open any page on stellaris.paradoxwikis.com, paste this into the
// console, and save what `await captureRelics()` returns as data/tools/capture/relics.wiki.json.
// Parsing is deterministic: same revision in, same JSON out. Nothing is typed by hand.
async function captureRelics(page = 'Relics') {
  const res = await fetch(`/api.php?action=parse&page=${page}&prop=wikitext|revid&format=json`);
  const j = await res.json();
  const w = j.parse.wikitext['*'];
  const sha = [...new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(w)))]
    .map(b => b.toString(16).padStart(2, '0')).join('');

  // --- wikitext -> plain text ------------------------------------------------------
  // Innermost templates first, repeated until none are left, so nesting resolves cleanly.
  const TPL = {
    green: a => a[0], yellow: a => a[0], red: a => a[0], small: a => a[0],
    hover: a => a[0], tooltip: a => a[0], 'tooltip premade': a => a[0],
    'planet modifier': a => a[0], 'icon link': a => a[a.length - 1] || a[0],
    iconify: a => (a[2] ? a[2] + ' ' : '') + a[0],
    icon: a => '', 'icon split': a => '', expansion: a => '', Version: a => '',
    reward: a => a[1] || a[0], ICONNAME: a => a[0],
  };
  const templ = s => {
    let prev;
    do {
      prev = s;
      s = s.replace(/\{\{([^{}|]+)((?:\|[^{}]*)?)\}\}/g, (m, name, rest) => {
        const n = name.trim();
        const args = rest ? rest.slice(1).split('|').filter(a => !/^\s*(?:\d+px|w=|image=|link=|tech=)/.test(a)) : [];
        return TPL[n] ? TPL[n](args.map(a => a.trim())) : (args[0] || n);
      });
    } while (s !== prev);
    return s;
  };
  const clean = s => templ(s
      // conditions: "{{icon|no}}{{…}}" reads "not …", and a bare icon after "if" is the condition's name
      .replace(/\{\{icon\|no(?:\|[^{}]*)?\}\}(?=\s*\{\{)/g, 'not ')
      .replace(/\bif (not )?\{\{icon\|([^{}|]+)(?:\|[^{}]*)?\}\}/g, (m, n, x) => 'if ' + (n || '') + '{{ICONNAME|' + x.trim() + '}}')
      .replace(/\[\[File:[^\]]*\]\]/g, '')
      .replace(/<ref[^>]*\/>|<ref[^>]*>[\s\S]*?<\/ref>/gi, '')   // footnotes are commentary, not effects
      .replace(/<br\s*\/?>/gi, '; ').replace(/<[^>]+>/g, ''))
    .replace(/\[\[(?:[^|\]]*\|)?([^\]]*)\]\]/g, '$1')
    .replace(/'''?/g, '').replace(/\s+/g, ' ').replace(/^[\s;]+|[\s;]+$/g, '').trim();
  const items = cell => {
    const lines = cell.split('\n').map(l => l.trim()).filter(Boolean);
    const bullets = lines.filter(l => l.startsWith('*')).map(l => clean(l.replace(/^\*+/, '')));
    const plain = lines.filter(l => !l.startsWith('*')).map(clean).filter(Boolean);
    return plain.concat(bullets).filter(Boolean);
  };
  const icons = s => [...s.matchAll(/\{\{icon\|([^}|]+)/g)].map(m => m[1].trim());

  // --- walk sections and tables -------------------------------------------------------
  const out = [];
  let h2 = null, h3 = null, sectionDlc = [];
  const blocks = w.split(/^(==+)\s*([^=\n]+?)\s*\1\s*$/m);
  for (let b = 0; b < blocks.length; b++) {
    if (/^==+$/.test(blocks[b])) {
      if (blocks[b].length === 2) { h2 = blocks[b + 1]; h3 = null; } else h3 = blocks[b + 1];
      sectionDlc = [];
      b++; continue;
    }
    const text = blocks[b];
    const ex = [...text.matchAll(/\{\{expansion\|([^}|]+)/g)].map(m => m[1].trim());
    if (ex.length) sectionDlc = ex;
    for (const t of text.matchAll(/^\{\|[^\n]*\n([\s\S]*?)^\|\}/gm)) {
      const body = t[1];
      const headerPart = body.split(/^\|-/m)[0];
      const headers = headerPart.split('\n').filter(l => l.startsWith('!'))
        .map(l => l.replace(/^!\s*/, '').split('|').pop().trim());
      const rows = body.split(/^\|-.*$/m).slice(1);
      for (const row of rows) {
        const cells = []; let cur = null;
        for (const line of row.split('\n')) {
          if (/^\|(?![-}])/.test(line)) { if (cur !== null) cells.push(cur); cur = line.slice(1); }
          else if (cur !== null) cur += '\n' + line;
        }
        if (cur !== null) cells.push(cur);
        const c = cells.map(x => x.replace(/^\s*(?:style|class|width|rowspan|colspan)="?[^|"]*"?\s*\|(?!\|)/, ''));
        if (c.length < 5) continue;
        const col = h => { const i = headers.findIndex(x => x.toLowerCase() === h.toLowerCase()); return i < 0 ? null : c[i]; };
        const box = (col('Relic') || '').match(/\{\{iconbox\|([^|}]+)\|/);
        if (!box) continue;
        const costRaw = col('Triumph cost') || '';
        const cost = [...costRaw.matchAll(/\{\{icon\|([^}|]+)\}\}\s*([\d,]+)/g)]
          .map(m => ({ resource: m[1].trim(), amount: Number(m[2].replace(/,/g, '')) }));
        const cdRaw = col('Triumph cooldown') || '';
        const cd = cdRaw.match(/([\d,]+)\s*days/);
        const srcHeader = headers.find(h => /^(source|archaeological site|guardian|precursor|astral rift)$/i.test(h)) || null;
        const dlcCell = col('DLC');
        out.push({
          name: box[1].trim(),
          category: h2, subsection: h3,
          passive: items(col('Passive effect') || ''),
          triumph: items(col('Triumph effect') || ''),
          triumph_cost: cost,
          triumph_cooldown_days: cd ? Number(cd[1].replace(/,/g, '')) : null,
          activatable: !/\{\{icon\|no\}\}/.test(costRaw + cdRaw),
          source_kind: srcHeader ? srcHeader.toLowerCase() : null,
          source: srcHeader ? items(col(srcHeader)).join('; ') || null : null,
          score: (m => m ? Number(m[1].replace(/,/g, '')) : null)((col('Score') || '').match(/([\d,]+)/)),
          dlc_codes: dlcCell !== null ? icons(dlcCell) : sectionDlc.slice(),
        });
      }
    }
  }
  // DLC codes -> names, resolved by the wiki's own {{icon}} template rather than a hand-kept table
  const codes = [...new Set(out.flatMap(r => r.dlc_codes))].sort();
  const exp = await (await fetch('/api.php?action=expandtemplates&prop=wikitext&format=json&text='
    + encodeURIComponent(codes.map(c => `${c}=={{icon|${c}}}`).join('\n')))).json();
  const dlcNames = {};
  for (const line of exp.expandtemplates.wikitext.split('\n')) {
    const m = line.match(/^([^=]+)==\[\[File:([^|\]]+?)\.png/);
    if (m) dlcNames[m[1]] = m[2];
  }
  const ifDlc = t => t.replace(/\bif (not )?([a-z]{3})\)/g, (m, n, c) => dlcNames[c] ? `if ${n || ''}${dlcNames[c]})` : m);
  for (const r of out) {
    r.dlc = r.dlc_codes.map(c => dlcNames[c] || c);
    r.passive = r.passive.map(ifDlc); r.triumph = r.triumph.map(ifDlc);
  }
  // upgradeable relics repeat a name per stage (Celestial Chart x4); number the stages in page order
  const seen = {};
  for (const r of out) if (r.subsection) r.stage = (seen[r.subsection] = (seen[r.subsection] || 0) + 1);
  return { page, revid: j.parse.revid, wiki_version: (w.match(/\{\{Version\|([^}]+)\}\}/) || [])[1] || null,
           wikitext_sha256: sha, url: `https://stellaris.paradoxwikis.com/${page}`, dlc_names: dlcNames, relics: out };
}
