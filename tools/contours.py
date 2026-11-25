import numpy as np, sys, os
out = sys.argv[1]

def field(W, H, nx, ny, hills, seed, warp=0.0):
    rng = np.random.default_rng(seed)
    xs = np.linspace(0, W, nx); ys = np.linspace(0, H, ny)
    X, Y = np.meshgrid(xs, ys)
    Z = np.zeros_like(X)
    for (cx, cy, sx, sy, a) in hills:
        Z += a * np.exp(-(((X-cx)/sx)**2 + ((Y-cy)/sy)**2))
    for _ in range(6):
        fx, fy = rng.uniform(0.5, 3.0, 2) / max(W, H) * 2*np.pi
        ph = rng.uniform(0, 2*np.pi, 2)
        Z += rng.uniform(0.04, 0.12) * np.sin(X*fx + ph[0] + warp*np.sin(Y*fy*0.7)) * np.cos(Y*fy + ph[1])
    return xs, ys, Z

def march(xs, ys, Z, level):
    segs = []
    ny, nx = Z.shape
    def interp(p1, p2, v1, v2):
        t = (level - v1) / (v2 - v1) if v2 != v1 else 0.5
        return (p1[0] + t*(p2[0]-p1[0]), p1[1] + t*(p2[1]-p1[1]))
    for j in range(ny-1):
        for i in range(nx-1):
            v = [Z[j,i], Z[j,i+1], Z[j+1,i+1], Z[j+1,i]]
            p = [(xs[i],ys[j]), (xs[i+1],ys[j]), (xs[i+1],ys[j+1]), (xs[i],ys[j+1])]
            c = sum((1<<k) for k in range(4) if v[k] > level)
            if c in (0, 15): continue
            e = {}
            for k in range(4):
                a, b = k, (k+1) % 4
                if (v[a] > level) != (v[b] > level):
                    e[k] = interp(p[a], p[b], v[a], v[b])
            ks = sorted(e)
            if len(ks) == 2:
                segs.append((e[ks[0]], e[ks[1]]))
            elif len(ks) == 4:
                segs.append((e[0], e[1])); segs.append((e[2], e[3]))
    return segs

def join(segs):
    key = lambda p: (round(p[0], 3), round(p[1], 3))
    adj = {}
    for idx, (a, b) in enumerate(segs):
        adj.setdefault(key(a), []).append(idx); adj.setdefault(key(b), []).append(idx)
    used = [False]*len(segs); lines = []
    for s in range(len(segs)):
        if used[s]: continue
        used[s] = True
        line = [segs[s][0], segs[s][1]]
        for direction in (1, 0):
            while True:
                end = line[-1] if direction else line[0]
                nxt = None
                for idx in adj.get(key(end), []):
                    if not used[idx]: nxt = idx; break
                if nxt is None: break
                used[nxt] = True
                a, b = segs[nxt]
                pt = b if key(a) == key(end) else a
                if direction: line.append(pt)
                else: line.insert(0, pt)
        lines.append(line)
    return lines

def chaikin(pts, it=2):
    closed = abs(pts[0][0]-pts[-1][0]) < 1e-6 and abs(pts[0][1]-pts[-1][1]) < 1e-6
    for _ in range(it):
        q = [] if closed else [pts[0]]
        for i in range(len(pts)-1):
            (x0,y0),(x1,y1) = pts[i], pts[i+1]
            q += [(0.75*x0+0.25*x1, 0.75*y0+0.25*y1), (0.25*x0+0.75*x1, 0.25*y0+0.75*y1)]
        if closed: q.append(q[0])
        else: q.append(pts[-1])
        pts = q
    return pts

def svg(name, W, H, nx, ny, hills, seed, nlevels, stroke=1, index_every=5, warp=0.0, minlen=6):
    xs, ys, Z = field(W, H, nx, ny, hills, seed, warp)
    lo, hi = np.percentile(Z, 2), np.percentile(Z, 99.6)
    paths_minor, paths_major = [], []
    for n, lv in enumerate(np.linspace(lo, hi, nlevels)):
        for line in join(march(xs, ys, Z, lv)):
            if len(line) < minlen: continue
            pts = chaikin(line[::2] + ([line[-1]] if len(line)%2==0 else []), 1)
            d = "M" + " ".join(f"{x:.0f} {y:.0f}" for x, y in pts[::1])
            (paths_major if n % index_every == 0 else paths_minor).append(d)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round">'
         f'<path stroke-width="{stroke}" d="{" ".join(paths_minor)}"/>'
         f'<path stroke-width="{stroke*2.1:.2f}" d="{" ".join(paths_major)}"/></svg>')
    open(os.path.join(out, name), "w").write(s)
    print(name, len(s)//1024, "KB")

# Wide hero terrain: ridge on the right, basin left
svg("contours-hero.svg", 1600, 1000, 170, 106,
    [(1150, 380, 260, 200, 1.0), (1380, 620, 180, 160, 0.7), (820, 250, 200, 130, 0.45), (400, 760, 320, 180, -0.5), (250, 300, 160, 140, 0.35)],
    seed=7, nlevels=34, warp=0.8)
# Section texture: gentle, sparse
svg("contours-soft.svg", 1600, 900, 140, 80,
    [(400, 450, 380, 260, 0.8), (1250, 350, 300, 240, 0.6), (900, 800, 260, 160, -0.3)],
    seed=21, nlevels=22, warp=0.5)
# Single peak (for feature figures), echoes the logo's concentric summit
svg("contours-peak.svg", 800, 800, 120, 120,
    [(400, 380, 190, 170, 1.0), (520, 300, 90, 80, 0.35), (300, 520, 140, 90, 0.2)],
    seed=3, nlevels=20, warp=0.3, index_every=4)
