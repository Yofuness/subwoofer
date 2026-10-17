#!/usr/bin/env python3
"""Dimensioned drawings of the FINAL box (34 x 15.5), geometry taken from box_cad.py.

    python3 box_drawing.py   -> cad/box_v4_34x15.5in_ortho.{png,pdf}  (3rd-angle: front, top, right side)
                                cad/box_v4_34x15.5in_parts.{png,pdf}  (every cut part, dimensioned)
Inches as fractions (nearest 1/16, +/- flags >= 1/64 rounding). Hidden edges dashed. Front view = trunk-lid side, x = 0 at the port-mouth end (left).
"""
import importlib.util, math, os, re
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

W, H_BOX = 34.0, 15.5
os.environ['BOX_H'] = str(H_BOX)
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('box_geom', os.path.join(here, 'box_cad.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)   # module name != box_cad, so main() doesn't run
g.CW = round(16 / g.CH, 2)                                              # 16 in^2 slot, as main() picks at 34"
d = g.design(W)
T, H, CH, CW, TH = g.T, g.H, g.CH, g.CW, g.TH
XE, DX, DZ = d['port_L'], d['drv_x'], g.DRV_Z
yo, yi = g.yo, g.yi
DIM, HID, LW = '#1f4e9e', '0.35', 1.1
FS = 6.5

# ---------------------------------------------------------------- drawing helpers
def line(ax, pts, hidden=False, close=False, c='k', lw=LW):
    pts = list(pts) + ([pts[0]] if close else [])
    ax.plot(*zip(*pts), color=HID if hidden else c, lw=0.8 if hidden else lw, ls=(0, (4, 2)) if hidden else '-')

def dim(ax, a, b, off, txt=None, fs=FS):
    """Aligned dimension a->b, dimension line offset `off` along the left normal of a->b."""
    (x1, y1), (x2, y2) = a, b
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = -uy, ux
    s = 1 if off >= 0 else -1
    p, q = (x1 + nx*off, y1 + ny*off), (x2 + nx*off, y2 + ny*off)
    for (px, py), (ex, ey) in ((a, p), (b, q)):
        ax.plot([px + nx*0.25*s, ex + nx*0.35*s], [py + ny*0.25*s, ey + ny*0.35*s], color=DIM, lw=0.5)
    ax.annotate('', p, q, arrowprops=dict(arrowstyle='<|-|>', color=DIM, lw=0.6, mutation_scale=6, shrinkA=0, shrinkB=0))
    ang = math.degrees(math.atan2(uy, ux))
    if ang > 90.1 or ang < -89.9: ang -= 180
    t = txt or f'{fr(L)}'
    ax.text((p[0]+q[0])/2 + nx*0.45*s, (p[1]+q[1])/2 + ny*0.45*s, t, rotation=ang, color=DIM, fontsize=fs,
            ha='center', va='center', bbox=dict(fc='white', ec='none', pad=0.3))

def fr(v, den=16):
    """Inches as a fraction to the nearest 1/16, with + / - if the true value is >= 1/64 off."""
    n = round(v * den); err = v - n / den
    w, r = divmod(abs(n), den); dd = den
    while r and r % 2 == 0: r //= 2; dd //= 2
    s = ('-' if n < 0 else '') + (f'{w} {r}/{dd}' if w and r else f'{r}/{dd}' if r else f'{w}') + '"'
    return s + ('+' if err >= 1/64 else '−' if err <= -1/64 else '')

def F(text):
    """Convert the decimal inch numbers (2+ decimals) in a note to fractions."""
    return re.sub(r'\d+\.\d{2,}', lambda m: fr(float(m.group())), text)

def note(ax, xy, xyt, txt, fs=FS):
    ax.annotate(txt, xy, xyt, color=DIM, fontsize=fs, ha='left', va='center',
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=0.5, mutation_scale=6))

def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

def setup(ax, title):
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=11, loc='left')

# ---------------------------------------------------------------- orthographic sheet
def ortho():
    fig, ax = plt.subplots(figsize=(17, 11))
    setup(ax, f'Sub box v4 FINAL: {fr(W)} W x {fr(H)} H x {fr(g.D_BOT)}/{fr(g.D_TOP)} D, net {d["net_L"]:.1f} L, '
              f'fb {g.FB:g} Hz   (3rd-angle projection, 3/4" MDF)')
    tz = (g.TERM[1] / 2) * math.cos(TH)                     # half-height of the cup hole, projected vertically
    cz0, cz1 = g.TERM_Z - tz, g.TERM_Z + tz
    cx0, cx1 = W/2 - g.TERM[0]/2, W/2 + g.TERM[0]/2
    bx0, bx1, bz0, bz1 = g.BRACE_X, g.BRACE_X + T, g.BRACE_Z, g.BRACE_Z + g.BRACE_H

    # ---- FRONT view (x, z)
    line(ax, rect(0, 0, W, H), close=True, lw=1.5)
    line(ax, rect(T, T, T + CW, T + CH), close=True)                                   # port mouth
    ax.add_patch(Circle((DX, DZ), g.DRV_CUT/2, fill=False, lw=LW))
    ax.add_patch(Circle((DX, DZ), g.DRV_OD/2, fill=False, lw=0.6, ls=':', color='0.5'))
    line(ax, rect(T, T, W - T, H - T), hidden=True, close=True)                         # inner faces
    line(ax, [(T + CW, T + CH), (XE, T + CH), (XE, T), (T + CW, T)], hidden=True)        # slot beyond the mouth
    line(ax, [(T, T + CH + T), (XE, T + CH + T), (XE, T + CH)], hidden=True)             # shelf top
    line(ax, rect(bx0, bz0, bx1, bz1), hidden=True, close=True)                         # brace
    line(ax, rect(cx0, cz0, cx1, cz1), hidden=True, close=True)                         # terminal cup (back)
    ax.text(W/2, -0.9, 'FRONT (trunk-lid side)', ha='center', fontsize=9, weight='bold')
    dim(ax, (0, H), (W, H), 1.2)
    dim(ax, (0, 0), (0, H), 1.6)
    dim(ax, (0, 0), (DX, 0), -2.2, f'{fr(DX)} driver C/L')
    dim(ax, (W, 0), (W, DZ), -1.4, f'{fr(DZ)}')
    dim(ax, (T, T), (T + CW, T), -1.1, f'mouth {fr(CW)}')
    dim(ax, (0, T), (0, T + CH), 0.7, f'{fr(CH)}', fs=5.5)
    dim(ax, (0, 0), (XE, 0), -3.4, f'port length {fr(XE)} (to open end, hidden)')
    note(ax, (DX + g.DRV_CUT/2*0.71, DZ + g.DRV_CUT/2*0.71), (DX + 6.6, DZ + 4.4),
         f'⌀{fr(g.DRV_CUT)} cutout\n(⌀{fr(g.DRV_OD)} frame, dotted)')
    note(ax, (bx1, (bz0 + bz1)/2), (1.2, 11.0), f'brace x {fr(bx0)}-{fr(bx1)}, z {fr(bz0)}-{fr(bz1)}')
    note(ax, (cx0, cz1), (1.2, 13.8), f'terminal cup on BACK, {fr(g.TERM[0])} x {fr(g.TERM[1])} centred x {fr(W/2)}, z {fr(g.TERM_Z)}')
    ax.text(0.9, 4.0, f'clearance cutout↔shelf / top: {fr(((H - T) - (T + CH + T) - g.DRV_CUT)/2)}', fontsize=FS, color=DIM)

    # ---- TOP view (x, y) above the front view, front edge nearest it
    oy = H + 6.0
    T_ = lambda x, y: (x, oy + y)
    line(ax, [T_(0, 0), T_(W, 0), T_(W, g.D_BOT), T_(0, g.D_BOT)], close=True, lw=1.5)
    line(ax, [T_(0, g.D_TOP), T_(W, g.D_TOP)])                                          # top-panel back edge / slope start
    line(ax, [T_(T, T), T_(W - T, T)], hidden=True)
    line(ax, [T_(T, T), T_(T, yi(T)), ], hidden=True); line(ax, [T_(W - T, T), T_(W - T, yi(T))], hidden=True)
    line(ax, [T_(T, T + CW + T), T_(XE, T + CW + T), T_(XE, T)], hidden=True)          # shelf / divider footprint
    line(ax, [T_(T, T + CW), T_(XE, T + CW)], hidden=True)
    line(ax, [T_(bx0, T), T_(bx0, yi(bz1)), T_(bx1, yi(bz1)), T_(bx1, T)], hidden=True)
    line(ax, [T_(cx0, yo(cz1)), T_(cx1, yo(cz1)), T_(cx1, yo(cz0)), T_(cx0, yo(cz0))], close=True)   # cup on the slope
    line(ax, [T_(T, 0), T_(T, T)], hidden=True); line(ax, [T_(T + CW, 0), T_(T + CW, T)], hidden=True)        # mouth through the baffle
    line(ax, [T_(DX - g.DRV_CUT/2, 0), T_(DX - g.DRV_CUT/2, T)], hidden=True)                                    # driver cutout
    line(ax, [T_(DX + g.DRV_CUT/2, 0), T_(DX + g.DRV_CUT/2, T)], hidden=True)
    line(ax, [T_(T, yi(H - T)), T_(W - T, yi(H - T))], hidden=True)                                             # back inner face at the top panel
    line(ax, [T_(T, yi(T)), T_(W - T, yi(T))], hidden=True)                                                     # back inner face at the floor
    line(ax, [T_(T, g.D_TOP - T*math.tan(TH)), T_(W - T, g.D_TOP - T*math.tan(TH))], hidden=True)              # top panel underside edge
    line(ax, [T_(0, yo(T)), T_(W, yo(T))], hidden=True)                                                          # bottom panel / back joint
    for xx in (cx0, cx1):                                                                                         # cup hole walls through the back
        line(ax, [T_(xx, yo(cz0)), T_(xx, yo(cz0) - T*math.cos(TH))], hidden=True)
    ax.text(W/2, oy - 1.0, 'TOP', ha='center', fontsize=9, weight='bold')
    ax.text(W/2, oy + (g.D_TOP + g.D_BOT)/2 + 1.9, 'sloped back (25.1°) seen from above', ha='center', fontsize=FS, color='0.3')
    dim(ax, T_(W, 0), T_(W, g.D_TOP), -1.3, f'{fr(g.D_TOP)} top')
    dim(ax, T_(W, 0), T_(W, g.D_BOT), -3.0, f'{fr(g.D_BOT)} floor')
    dim(ax, T_(0, T), T_(0, T + CW), 1.0, f'slot {fr(CW)}')
    dim(ax, T_(0, 0), T_(0, T + CW + T), 2.3, f'shelf {fr(CW + T)}')
    dim(ax, T_(T, g.D_BOT), T_(XE, g.D_BOT), 1.0, f'shelf + divider {fr(XE - T)} (from inside of end)')
    dim(ax, T_(XE, g.D_BOT), T_(W - T, g.D_BOT), 1.0, f'{fr(W - T - XE)} gap', fs=5.5)
    dim(ax, T_(0, g.D_BOT), T_(W, g.D_BOT), 2.6)

    # ---- RIGHT SIDE view (y, z), seen from the x = W end, front face nearest the front view
    ox = W + 8.0
    S = lambda y, z: (ox + y, z)
    line(ax, [S(0, 0), S(g.D_BOT, 0), S(g.D_TOP, H), S(0, H)], close=True, lw=1.5)
    line(ax, [S(T, T), S(yi(T), T), S(yi(H - T), H - T), S(T, H - T)], hidden=True, close=True)
    line(ax, [S(T, T + CH), S(T + CW, T + CH), S(T + CW, T)], hidden=True)                   # slot section
    line(ax, [S(T, T + CH + T), S(T + CW + T, T + CH + T), S(T + CW + T, T)], hidden=True)   # shelf + divider
    line(ax, [S(T, bz0), S(yi(bz0), bz0)], hidden=True); line(ax, [S(T, bz1), S(yi(bz1), bz1)], hidden=True)
    n_, u_ = (math.cos(TH), math.sin(TH)), (-math.sin(TH), math.cos(TH))                 # back-face normal / along-slope
    oc = (yo(g.TERM_Z), g.TERM_Z); hh = g.TERM[1] / 2
    cup = [(oc[0] + a*u_[0] - b*n_[0], oc[1] + a*u_[1] - b*n_[1]) for a, b in ((-hh, 0), (-hh, T), (hh, T), (hh, 0))]
    line(ax, [S(*p) for p in cup], hidden=True)                                            # cup hole through the back
    line(ax, [S(0, DZ - g.DRV_CUT/2), S(T, DZ - g.DRV_CUT/2)], hidden=True)                # driver cutout through the baffle
    line(ax, [S(0, DZ + g.DRV_CUT/2), S(T, DZ + g.DRV_CUT/2)], hidden=True)
    line(ax, [S(0, T + CH), S(T, T + CH)], hidden=True)                                    # mouth through the baffle
    line(ax, [S(0, T), S(T, T)], hidden=True); line(ax, [S(0, H - T), S(T, H - T)], hidden=True)   # top/bottom vs baffle joints
    line(ax, [S(yi(0), 0), S(yi(T), T)], hidden=True)                                      # bottom-panel bevel against the back
    line(ax, [S(yi(H - T), H - T), S(yi(H), H)], hidden=True)                              # top-panel bevel against the back
    line(ax, [S(T, bz0), S(T, bz1)], hidden=True); line(ax, [S(yi(bz0), bz0), S(yi(bz1), bz1)], hidden=True)   # brace ends
    ax.text(ox + g.D_BOT/2, -0.9, 'RIGHT SIDE (driver end)', ha='center', fontsize=9, weight='bold')
    dim(ax, S(0, 0), S(g.D_BOT, 0), -1.2)
    dim(ax, S(0, H), S(g.D_TOP, H), 1.0)
    dim(ax, S(g.D_BOT, 0), S(g.D_TOP, H), -1.2, f'back {fr(math.hypot(g.D_BOT - g.D_TOP, H))}')
    dim(ax, S(g.D_BOT + 2.3, 0), S(g.D_BOT + 2.3, g.TERM_Z), -0.01, f'cup C/L {fr(g.TERM_Z)}')
    ax.add_patch(Arc(S(g.D_TOP, H), 5, 5, theta1=270, theta2=270 + math.degrees(TH), color=DIM, lw=0.6))
    ax.plot([ox + g.D_TOP, ox + g.D_TOP], [H, H - 3.0], color=DIM, lw=0.5)
    ax.text(ox + g.D_TOP + 0.55, H - 3.4, f'{math.degrees(TH):.1f}°', color=DIM, fontsize=FS)
    note(ax, S(T + CW/2, T + CH/2), S(5.0, 6.0), f'slot {fr(CH)} x {fr(CW)} = {CH*CW:.1f} in²')
    note(ax, S(T + CW/2, T + CH + T/2), S(8.0, 4.4), f'shelf {fr(T)}, divider {fr(T)}')

    # ---- notes
    nx, ny = W + 8.0, H + 6.0
    lines = ['Dimensions in inches, nearest 1/16. Suffix + = a hair over (≥1/64), − = a hair under.',
             f'Net {d["net_L"]:.1f} L (gross {d["gross_L"]:.1f} L), port {CH*CW:.1f} in² x {fr(XE)} centre-line, fb {g.FB:g} Hz',
             'Construction: front and back full width/height; top & bottom between them;',
             '  ends inset between all four. All panels 3/4" MDF. Every bevel is 25.1° (blade tilt).',
             'Port: floor slot along the width; mouth through the baffle, 90° bend behind it.',
             '  1" of port length ≈ 0.36 Hz. Build as drawn, measure fb, trim.',
             f'Brace: 3/4 x {fr(g.BRACE_H)} front→back, back end cut to the slope.',
             'Terminal cup: back panel, hole square to the slope; size to the real cup.']
    for i, s in enumerate(lines):
        ax.text(nx, ny + 15.5 - i*1.25, s, fontsize=7.5, family='monospace')
    ax.set_xlim(-5, ox + g.D_BOT + 6); ax.set_ylim(-5, oy + g.D_BOT + 5)
    return fig

# ---------------------------------------------------------------- parts sheet
def parts():
    P = g.panels(d)
    fig, ax = plt.subplots(figsize=(14, 17))
    setup(ax, 'Cut parts, 3/4" MDF, inches to the nearest 1/16 (+ / − = a hair over / under). Polygons are the larger face; dashed green = bevel edge on the other face')
    col1, col2 = ['FRONT baffle', 'BACK', 'BOTTOM', 'TOP'], ['END', 'PORT SHELF', 'PORT DIVIDER', 'BRACE']
    for col, x0 in ((col1, 0.0), (col2, W + 12.0)):
        y = 0.0
        for name in col:
            nm, qty, poly, bevel, holes, nt = next(p for p in P if p[0] == name)
            pw, ph = max(u for u, _ in poly), max(v for _, v in poly)
            y -= ph
            Q = [(x0 + u, y + v) for u, v in poly]
            line(ax, Q, close=True, lw=1.4)
            ax.text(x0, y + ph + 3.2, f'{nm} x{qty}', fontsize=9, weight='bold')
            ax.text(x0, y + ph + 2.3, F(nt), fontsize=6, color='0.3')
            dim(ax, (x0, y), (x0 + pw, y), -1.1)
            dim(ax, (x0, y), (x0, y + ph), 1.1 if ph > 3 else 1.6)
            if name in ('END', 'BRACE'):                                         # non-rectangular: top edge too
                tw = poly[2][0]
                dim(ax, (x0, y + ph), (x0 + tw, y + ph), 0.9)
            if bevel:
                line(ax, [(x0, y + bevel[1]), (x0 + pw, y + bevel[1])], c='g', lw=0.7)
                ax.plot([x0, x0 + pw], [y + bevel[1]] * 2, color='g', lw=0.8, ls=(0, (4, 2)))
                dim(ax, (x0 + pw, y), (x0 + pw, y + bevel[1]), -1.1, f'{fr(bevel[1])} top face')
            k = 0
            for h in holes:
                if h[0] == 'rect':
                    _, u0, v0, u1, v1, lab = h
                    line(ax, rect(x0 + u0, y + v0, x0 + u1, y + v1), close=True, c='r')
                    ax.text(x0 + (u0 + u1)/2, y + v1 + 0.5, f'{lab}  {fr(u1-u0)} x {fr(v1-v0)}', fontsize=FS, color='r', ha='center')
                    dim(ax, (x0, y + v1 + 1.6 + k), (x0 + u0, y + v1 + 1.6 + k), 0.0001, f'{fr(u0)}', fs=5.5)
                    dim(ax, (x0 + u1 + 0.8, y), (x0 + u1 + 0.8, y + v0), -0.0001, f'{fr(v0)}', fs=5.5)
                else:
                    _, cu, cv, r, lab = h
                    ax.add_patch(Circle((x0 + cu, y + cv), r, fill=False, color='r', lw=1))
                    ax.plot([x0 + cu - 0.4, x0 + cu + 0.4], [y + cv]*2, 'r', lw=0.5); ax.plot([x0 + cu]*2, [y + cv - 0.4, y + cv + 0.4], 'r', lw=0.5)
                    dim(ax, (x0, y + cv), (x0 + cu, y + cv), 0.0001, f'{fr(cu)}', fs=5.5)
                    dim(ax, (x0 + cu, y), (x0 + cu, y + cv), -0.0001, f'{fr(cv)}', fs=5.5)
                    ax.text(x0 + cu + r*0.75, y + cv + r*0.75, f'⌀{fr(2*r)}', color='r', fontsize=FS)
                k += 1
            y -= 6.5
    ax.autoscale(); ax.margins(0.03)
    return fig

if __name__ == '__main__':
    stem = os.path.join(here, 'cad', f'box_v4_{W:g}x{H_BOX:g}in')
    for fn, f in (('_ortho', ortho), ('_parts', parts)):
        fig = f()
        for ext in ('png', 'pdf'):
            fig.savefig(stem + fn + '.' + ext, dpi=170 if ext == 'png' else None, bbox_inches='tight')
        print('wrote', stem + fn + '.png/.pdf')
