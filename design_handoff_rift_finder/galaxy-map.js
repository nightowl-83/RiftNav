(function () {
  if (customElements.get('galaxy-map')) return;
  const N = 48000, SHAPES = ['galaxy', 'rift', 'dig'];
  let seed = 7;
  const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
  const gauss = () => { const u = rnd() || 1e-6, v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(6.2831853 * v); };
  const ease = t => t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t);

  const P = {}, C = {}, PHASE = new Float32Array(N), DELAY = new Float32Array(N), CORE = new Uint8Array(N), CORELUM = new Float32Array(N), DIGC = new Uint8Array(N);
  for (let i = 0; i < N; i++) { PHASE[i] = rnd() * 6.2831853; DELAY[i] = rnd(); }

  // coreFrac: share of disc stars pulled into the central bulge
  function buildGalaxy(coreFrac) {
    seed = 7;
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      const o = i * 3; CORE[i] = 0; CORELUM[i] = 0;
      const halo = rnd() < 0.09, bulge = rnd() < coreFrac;
      if (halo) {
        const r = 1.2 + rnd() * 1.4, th = rnd() * 6.2831853, ph = Math.acos(2 * rnd() - 1);
        p[o] = r * Math.sin(ph) * Math.cos(th); p[o + 1] = r * Math.cos(ph) * 0.35; p[o + 2] = r * Math.sin(ph) * Math.sin(th);
        c[o] = 0.22; c[o + 1] = 0.3; c[o + 2] = 0.62; continue;
      }
      if (bulge) {
        const r = Math.pow(rnd(), 0.85) * 0.3, th = rnd() * 6.2831853, ph = Math.acos(2 * rnd() - 1);
        p[o] = r * Math.sin(ph) * Math.cos(th); p[o + 1] = r * Math.cos(ph) * 0.5; p[o + 2] = r * Math.sin(ph) * Math.sin(th);
        const k = Math.max(0, 1 - r / 0.3), j = gauss();
        c[o] = Math.max(0, Math.min(1, 0.07 + 0.15 * k * k + j * 0.06));
        c[o + 1] = Math.max(0, Math.min(1, 0.66 + 0.28 * k + j * 0.05));
        c[o + 2] = Math.max(0.86, Math.min(1, 1 - Math.abs(j) * 0.05));
        CORE[i] = 1; CORELUM[i] = Math.pow(k, 0.85); continue;
      }
      const r = Math.pow(rnd(), 0.72) * 1.05, arm = Math.floor(rnd() * 3);
      const ang = arm * 2.0944 + r * 3.4 + gauss() * (0.16 + 0.28 * r);
      const rr = r * (1 + gauss() * 0.04);
      p[o] = rr * Math.cos(ang); p[o + 1] = gauss() * 0.022 * (1.2 - r); p[o + 2] = rr * Math.sin(ang);
      if (r < 0.22) {
        const k = 1 - r / 0.22, j = gauss();
        c[o] = Math.max(0, Math.min(1, 0.07 + 0.14 * k * k + j * 0.07));
        c[o + 1] = Math.max(0, Math.min(1, 0.82 + 0.16 * k + j * 0.05));
        c[o + 2] = Math.max(0.84, Math.min(1, 1 - Math.abs(j) * 0.06));
        CORE[i] = 1; CORELUM[i] = Math.pow(k, 1.4) * 0.85;
      }
      else if (r < 0.4 && rnd() < 0.5) { const k = rnd(); c[o] = 0.42 + 0.24 * k; c[o + 1] = 0.84 + 0.12 * k; c[o + 2] = 1; CORELUM[i] = 0.16 * (1 - r / 0.4); }
      else if (rnd() < 0.09) { c[o] = 1; c[o + 1] = 0.22; c[o + 2] = 0.62; }
      else if (rnd() < 0.06) { c[o] = 0.18; c[o + 1] = 0.95; c[o + 2] = 1; }
      else if (rnd() < 0.04) { c[o] = 1; c[o + 1] = 0.58; c[o + 2] = 0.22; }
      else if (rnd() < 0.05) { c[o] = 0.35; c[o + 1] = 1; c[o + 2] = 0.5; }
      else if (rnd() < 0.26) { c[o] = 0.86; c[o + 1] = 0.93; c[o + 2] = 1; }
      else { const k = rnd(); c[o] = 0.24 + 0.28 * k; c[o + 1] = 0.44 + 0.26 * k; c[o + 2] = 1; }
    }
    P.galaxy = p; C.galaxy = c;
  }
  function buildRift() {
    seed = 99;
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3), R = 0.62;
    for (let i = 0; i < N; i++) {
      const o = i * 3;
      if (rnd() < 0.7) {
        const k = i + 0.5, ph = Math.acos(1 - 2 * k / N), th = 2.39996323 * k, jit = 1 + gauss() * 0.006;
        p[o] = R * jit * Math.sin(ph) * Math.cos(th); p[o + 1] = R * jit * Math.cos(ph); p[o + 2] = R * jit * Math.sin(ph) * Math.sin(th);
        const lat = Math.abs(Math.cos(ph)), ring = Math.abs(((ph * 8) % 3.14159) - 1.5708) < 0.06 ? 1 : 0;
        const b = 0.55 + 0.35 * ring + 0.1 * rnd();
        c[o] = 0.3 * b; c[o + 1] = 0.82 * b; c[o + 2] = 1 * b; if (lat > 0.97) { c[o] = 0.6; c[o + 1] = 0.95; c[o + 2] = 1; }
      } else {
        const t = (rnd() < 0.5 ? -1 : 1) * (0.55 + Math.pow(rnd(), 0.6) * 1.1);
        const cl = gauss() * (0.03 + 0.05 * Math.abs(t)), cl2 = gauss() * (0.03 + 0.05 * Math.abs(t));
        p[o] = t * 0.95 + cl * 0.4; p[o + 1] = t * 0.34 + cl; p[o + 2] = cl2;
        const b = 0.35 + 0.45 * rnd();
        c[o] = 0.35 * b; c[o + 1] = 0.85 * b; c[o + 2] = 1 * b;
      }
    }
    P.rift = p; C.rift = c;
  }
  function buildDig() {
    seed = 313;
    const p = new Float32Array(N * 3), c = new Float32Array(N * 3), R = 0.6;
    // fake elevation field over the sphere; contour bands are drawn where it crosses a level
    const elev = (x, y, z) => 0.5 * Math.sin(3.1 * x + 0.7) * Math.cos(2.7 * z) + 0.34 * Math.sin(4.3 * y + 1.9)
      + 0.22 * Math.sin(6.1 * z + x * 2.2) + 0.14 * Math.sin(8.7 * x * z + 1.3);
    const onSphere = () => { const u = rnd() * 6.2831853, v = 2 * rnd() - 1, r = Math.sqrt(1 - v * v); return [r * Math.cos(u), v, r * Math.sin(u)]; };
    for (let i = 0; i < N; i++) {
      const o = i * 3, contour = rnd() < 0.55;
      DIGC[i] = contour ? 1 : 0;
      let n = onSphere(), e = elev(n[0] * 2, n[1] * 2, n[2] * 2);
      if (contour) {
        for (let k = 0; k < 90; k++) {
          const f = (e * 7) - Math.floor(e * 7);
          if (f < 0.05 || f > 0.95) break;
          n = onSphere(); e = elev(n[0] * 2, n[1] * 2, n[2] * 2);
        }
      }
      const rr = R * (1 + e * 0.004);
      p[o] = n[0] * rr; p[o + 1] = n[1] * rr; p[o + 2] = n[2] * rr;
      const hi = (e + 1) * 0.5;
      if (contour) {
        const b = 0.9 + 0.35 * hi;
        c[o] = 0.34 * b; c[o + 1] = 1 * b; c[o + 2] = 0.94 * b;
        if (rnd() < 0.06) { c[o] = 1 * b; c[o + 1] = 0.78 * b; c[o + 2] = 0.42 * b; }
      } else {
        const b = 0.34 + 0.34 * hi + 0.12 * rnd();
        c[o] = 0.22 * b; c[o + 1] = 0.88 * b; c[o + 2] = 0.88 * b;
        if (rnd() < 0.03) { c[o] = 0.95 * b; c[o + 1] = 0.72 * b; c[o + 2] = 0.4 * b; }
      }
    }
    P.dig = p; C.dig = c;
  }

  // gaussian splat kernels (radius 1..5) for per-particle glow
  const KERNELS = [];
  for (let R = 1; R <= 16; R++) {
    const s2 = R * R * 0.16, k = [];
    for (let dy = -R; dy <= R; dy++) for (let dx = -R; dx <= R; dx++) {
      const d2 = dx * dx + dy * dy;
      if (d2 > R * R) continue;
      // heavy-tailed falloff: long diffuse skirt instead of a gaussian cutoff
      const w = Math.pow(1 / (1 + d2 / s2), 1.55);
      if (w > 0.004) k.push(dx, dy, w);
    }
    KERNELS.push(k);
  }

  const TONE_MAX = 7, TONE_N = 4096, TONE = new Uint8Array(TONE_N + 1);
  for (let i = 0; i <= TONE_N; i++) TONE[i] = Math.round(255 * (1 - Math.exp(-(i / TONE_N) * TONE_MAX)));
  const TONE_S = TONE_N / TONE_MAX;

  let coreFracBuilt = 0.3;
  buildGalaxy(coreFracBuilt); buildRift(); buildDig();

  // pitch: radians (π/2 = straight down), dist: perspective focal distance, ang: fixed yaw offset, zoom: scale, yOff: vertical centre shift (fraction of height), glow: core glow
  const CAM = {
    galaxy: { pitch: 0.5, dist: 2.6, ang: 0, zoom: 1.7, xOff: 0, yOff: -0.06, glow: 1.4 },
    rift: { pitch: 0.14, dist: 3.2, ang: 0, zoom: 0.86, xOff: 0, yOff: 0.06, glow: 0 },
    dig: { pitch: 0.34, dist: 5, ang: 0, zoom: 3.6, xOff: 0.34, yOff: 0.74, glow: 0 }
  };
  const KEYS = Object.keys(CAM.galaxy);

  function ambient(shape, i, ta, px, py, pz, out) {
    const ph = PHASE[i];
    if (shape === 'rift') {
      const br = 1 + 0.012 * Math.sin(ta * 0.00075), j = 0.006 * Math.sin(ta * 0.0011 + ph);
      out[0] = px * br + j * Math.cos(ph); out[1] = py * br + j * Math.sin(ph * 1.7); out[2] = pz * br + j * Math.sin(ph);
      return 0.82 + 0.18 * Math.sin(ta * 0.0016 + ph);
    }
    if (shape === 'dig') {
      const br = 1 + 0.0015 * Math.sin(ta * 0.0006 + ph);
      out[0] = px * br; out[1] = py * br; out[2] = pz * br;
      return 0.82 + 0.18 * Math.sin(ta * 0.0012 + ph);
    }
    out[0] = px; out[1] = py; out[2] = pz;
    return 0.86 + 0.14 * Math.sin(ta * 0.0013 + ph);
  }

  class GalaxyMap extends HTMLElement {
    static get observedAttributes() { return ['mode', 'speed', 'pitch', 'dist', 'ang', 'zoom', 'xoff', 'yoff', 'glow', 'core']; }
    constructor() {
      super();
      this._mode = 'galaxy'; this._speed = 1; this.ov = {};
      this.cur = new Float32Array(N * 3); this.curC = new Float32Array(N * 3);
      this.from = null; this.fromC = null; this.fromCam = null; this.fromShape = null; this.tStart = 0; this.dur = 2800;
      this.yaw = 0; this.ta = 0; this.last = 0; this.tmp = [0, 0, 0];
      this.cam = Object.assign({}, CAM.galaxy);
    }
    get mode() { return this._mode; } set mode(v) { this.setMode(v); }
    get speed() { return this._speed; } set speed(v) { const n = parseFloat(v); this._speed = isNaN(n) ? 1 : n; }
    setOv(k, v) { const n = parseFloat(v); if (isNaN(n)) delete this.ov[k]; else this.ov[k] = n; }
    set pitch(v) { this.setOv('pitch', v); } set dist(v) { this.setOv('dist', v); } set ang(v) { this.setOv('ang', v); }
    set zoom(v) { this.setOv('zoom', v); } set xoff(v) { this.setOv('xOff', v); } set yoff(v) { this.setOv('yOff', v); } set glow(v) { this.setOv('glow', v); }
    set core(v) { const n = parseFloat(v); if (!isNaN(n) && Math.abs(n - coreFracBuilt) > 1e-4) { coreFracBuilt = n; buildGalaxy(n); } }
    attributeChangedCallback(n, _o, v) { if (n === 'mode') this.setMode(v); else this[n] = v; }
    setMode(v) {
      v = SHAPES.includes(v) ? v : 'galaxy';
      if (v === this._mode) return;
      if (this.started) {
        this.from = Float32Array.from(this.cur); this.fromC = Float32Array.from(this.curC);
        this.fromCam = Object.assign({}, this.cam); this.fromShape = this._mode; this.tStart = performance.now();
      }
      this._mode = v;
    }
    connectedCallback() {
      this.style.display = 'block';
      this.style.cssText += ';position:fixed;inset:0;width:100vw;height:100vh';
      const c = this.canvas = document.createElement('canvas');
      c.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;display:block';
      this.appendChild(c); this.ctx = c.getContext('2d', { alpha: false });
      this.onWin = () => this.resize(); window.addEventListener('resize', this.onWin);
      this.resize(); this.started = true; this.last = performance.now();
      const loop = t => { this.raf = requestAnimationFrame(loop); this.frame(t); };
      this.raf = requestAnimationFrame(loop);
    }
    disconnectedCallback() { cancelAnimationFrame(this.raf); window.removeEventListener('resize', this.onWin); }
    resize() {
      const w = Math.max(1, window.innerWidth | 0), h = Math.max(1, window.innerHeight | 0);
      if (this.canvas.width !== w || this.canvas.height !== h) {
        this.canvas.width = w; this.canvas.height = h;
        this.img = this.ctx.createImageData(w, h); this.acc = new Float32Array(w * h * 3);
      }
    }
    frame(now) {
      const dt = Math.min(64, now - this.last); this.last = now;
      this.resize();
      const w = this.canvas.width, h = this.canvas.height; if (!this.img || w < 2) return;
      this.yaw += dt * 0.0000436 * this.speed; // 1 rev / 144 s at speed 1
      this.ta += dt;
      const shape = this._mode, pos = P[shape], col = C[shape];
      const tr = this.from ? Math.min(1, (now - this.tStart) / this.dur) : 1, gT = ease(tr);
      if (tr >= 1 && this.from) { this.from = null; this.fromC = null; this.fromCam = null; }
      const target = shape === 'galaxy' ? Object.assign({}, CAM.galaxy, this.ov) : Object.assign({}, CAM[shape], { xOff: CAM[shape].xOff + (this.ov.xOff || 0) }), fc = this.fromCam || target, cam = this.cam;
      for (const k of KEYS) cam[k] = fc[k] + (target[k] - fc[k]) * gT;
      const yawT = this.yaw + cam.ang;
      const cy = Math.cos(yawT), sy = Math.sin(yawT), cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch);
      const S = Math.min(w, h) * 0.46 * cam.zoom, cx = w * (0.5 + cam.xOff), cyy = h * (0.5 + cam.yOff), F = cam.dist;
      const cullBack = shape === 'dig' && !this.from, digSplat = shape === 'dig', glow = cam.glow, splat = shape === 'galaxy' ? glow * (1 - (this.from ? 1 - gT : 0)) : 0;
      const d = this.img.data, acc = this.acc; acc.fill(0);
      const cur = this.cur, curC = this.curC, from = this.from, fromC = this.fromC, tmp = this.tmp;
      for (let i = 0; i < N; i++) {
        const o = i * 3;
        let br = ambient(shape, i, this.ta, pos[o], pos[o + 1], pos[o + 2], tmp);
        let x = tmp[0], y = tmp[1], z = tmp[2], r = col[o], g = col[o + 1], b = col[o + 2];
        if (from) {
          const p = ease((tr - DELAY[i] * 0.4) / 0.6);
          x = from[o] + (x - from[o]) * p; y = from[o + 1] + (y - from[o + 1]) * p; z = from[o + 2] + (z - from[o + 2]) * p;
          r = fromC[o] + (r - fromC[o]) * p; g = fromC[o + 1] + (g - fromC[o + 1]) * p; b = fromC[o + 2] + (b - fromC[o + 2]) * p;
          br *= 1 + 0.9 * Math.sin(p * 3.14159);
        }
        cur[o] = x; cur[o + 1] = y; cur[o + 2] = z; curC[o] = r; curC[o + 1] = g; curC[o + 2] = b;
        const x1 = x * cy - z * sy, z1 = x * sy + z * cy;
        const y2 = y * cp - z1 * sp, z2 = y * sp + z1 * cp;
        if (cullBack && z2 > 0) continue;
        const s = F / (F + z2);
        const px = (cx + x1 * s * S) | 0, py = (cyy - y2 * s * S) | 0;
        if (px < 1 || py < 1 || px >= w - 1 || py >= h - 1) continue;
        const dim = shape === 'galaxy' ? 1 - 0.86 * CORELUM[i] : 1;
        const k = br * 1.15 * Math.min(1.3, s * s), q = (py * w + px) * 3, kd = k * dim;
        acc[q] += r * kd; acc[q + 1] += g * kd; acc[q + 2] += b * kd;
        if (digSplat && DIGC[i]) {
          const kk = k * 0.42, rr = r * kk, gg = g * kk, bb = b * kk, ww = w * 3;
          acc[q - 3] += rr; acc[q - 2] += gg; acc[q - 1] += bb; acc[q + 3] += rr; acc[q + 4] += gg; acc[q + 5] += bb;
          acc[q - ww] += rr; acc[q - ww + 1] += gg; acc[q - ww + 2] += bb; acc[q + ww] += rr; acc[q + ww + 1] += gg; acc[q + ww + 2] += bb;
        }
        const lum = splat > 0 ? CORELUM[i] : 0;
        if (lum > 0.02) {
          const R = 2 + Math.min(14, (lum * lum * 16) | 0), ker = KERNELS[R - 1];
          if (px > R && py > R && px < w - R - 1 && py < h - R - 1) {
            const amp = k * splat * (0.012 + 0.05 * lum * lum);
            for (let j = 0; j < ker.length; j += 3) {
              const wq = q + (ker[j + 1] * w + ker[j]) * 3, ww = ker[j + 2] * amp;
              acc[wq] += r * ww; acc[wq + 1] += g * ww; acc[wq + 2] += b * ww;
            }
          }
        }
      }
      const np = w * h;
      for (let i = 0, a = 0, o = 0; i < np; i++, a += 3, o += 4) {
        const ar = acc[a], ag = acc[a + 1], ab = acc[a + 2];
        if (ar === 0 && ag === 0 && ab === 0) { d[o] = 4; d[o + 1] = 5; d[o + 2] = 10; d[o + 3] = 255; continue; }
        d[o] = 4 + TONE[ar > 0 ? (ar < TONE_MAX ? (ar * TONE_S) | 0 : TONE_N) : 0];
        d[o + 1] = 5 + TONE[ag > 0 ? (ag < TONE_MAX ? (ag * TONE_S) | 0 : TONE_N) : 0];
        d[o + 2] = 10 + TONE[ab > 0 ? (ab < TONE_MAX ? (ab * TONE_S) | 0 : TONE_N) : 0];
        d[o + 3] = 255;
      }
      const ctx = this.ctx; ctx.putImageData(this.img, 0, 0);
      if (glow > 0.01) {
        const sq = 0.12 + 0.88 * Math.abs(Math.sin(cam.pitch)), a = Math.min(1, glow);
        ctx.globalCompositeOperation = 'lighter';
        // hue drawn from the actual star tones (pale blue-white core -> periwinkle -> indigo)
        const RAMP = [
          [0, 206, 226, 255], [0.18, 156, 194, 252], [0.42, 108, 152, 240],
          [0.68, 74, 110, 210], [1, 48, 74, 165]
        ];
        // core stars live inside world r ~0.3; keep the haze within 1.2x of that
        const rad = S * 0.36, gr = ctx.createRadialGradient(cx, cyy, 0, cx, cyy, rad);
        const STOPS = 96;
        for (let i = 0; i <= STOPS; i++) {
          const t = i / STOPS, u = 1 - t;
          let k = 1;
          while (k < RAMP.length - 1 && RAMP[k][0] < t) k++;
          const A = RAMP[k - 1], B = RAMP[k], f = (t - A[0]) / (B[0] - A[0] || 1), g = ease(f);
          const alpha = (0.16 * Math.pow(u, 3.2) + 0.1 * Math.pow(u, 1.9)) * ease(u * 3.2) * a;
          gr.addColorStop(t,
            'rgba(' + Math.round(A[1] + (B[1] - A[1]) * g) + ',' + Math.round(A[2] + (B[2] - A[2]) * g)
            + ',' + Math.round(A[3] + (B[3] - A[3]) * g) + ',' + alpha.toFixed(5) + ')');
        }
        gr.addColorStop(1, 'rgba(48,74,165,0)');
        try {
          ctx.fillStyle = gr; ctx.beginPath(); ctx.ellipse(cx, cyy, rad, rad * sq, 0, 0, 6.2831853); ctx.fill();
        } finally {
          ctx.globalCompositeOperation = 'source-over';
        }
      }
      const wR = (shape === 'rift' ? gT : 0) + (this.from && this.fromShape === 'rift' ? 1 - gT : 0);
      if (wR > 0.01) {
        const gr = ctx.createRadialGradient(cx, cyy, S * 0.3, cx, cyy, S * 0.95);
        gr.addColorStop(0, 'rgba(60,190,255,' + (0.16 * wR) + ')'); gr.addColorStop(1, 'rgba(60,190,255,0)');
        ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = gr; ctx.fillRect(0, 0, w, h); ctx.globalCompositeOperation = 'source-over';
      }
    }
  }
  customElements.define('galaxy-map', GalaxyMap);
})();
