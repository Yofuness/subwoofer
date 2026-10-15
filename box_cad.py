#!/usr/bin/env python3
"""Layout v4 ported box (22 Hz): geometry, net volume, port length, DXF cut sheet.

    python3 box_cad.py [width_in]                 -> prints dims, writes cad/box_v4_<W>in.dxf
    freecadcmd box_cad.py  (env BOX_W=38.5)       -> also writes cad/box_v4_<W>in.FCStd + .step

Coordinates (inches): x = width (x=0 is the port-mouth end, left when you face the driver),
y = depth from the front face toward the seatback, z = up. 3/4" MDF everywhere.
Construction: front and back run full width and full height, top/bottom sit between them,
the ends are inset between all four. Every bevel is 25.1 deg (blade tilt).
"""
import math, os, sys

# ---------------------------------------------------------------- parameters
T = 0.75                        # MDF thickness
H, D_BOT, D_TOP = 16.0, 18.0, 10.5
CH, CW = 1.75, 10.25            # port slot: height x depth (y), 17.94 in^2
FB = 22.0                       # tuning
DRV_CUT, DRV_OD = 11.14, 12.4   # TS-W304R baffle cutout / frame OD
DRV_DISP_L = 1.66
DRV_Z = 9.25                    # driver centre height (outer); 0.43" clear of shelf and top
BRACE_X, BRACE_Z, BRACE_H = 11.25, 8.25, 1.5   # 3/4" brace, front->back
TERM = (3.0, 3.0)               # terminal-cup hole placeholder, measure the old cup
C = 343.0
IN3_L = 0.016387064

TAN = (D_BOT - D_TOP) / H
TH = math.atan(TAN)
DT = T / math.cos(TH)           # horizontal thickness of the sloped back

def yo(z): return D_BOT - z * TAN          # outer back face
def yi(z): return D_BOT - DT - z * TAN     # inner back face

def design(W):
    gross = (W - 2*T) * (H - 2*T) * (yi(H/2) - T)          # inner trapezoid prism, in^3
    brace = T * BRACE_H * (yi(BRACE_Z + BRACE_H/2) - T)
    area = CH * CW
    r = math.sqrt(area / math.pi)
    xe = 27.0
    for _ in range(50):                                     # port volume depends on its length
        port_block = (CW + T) * (CH + T) * (xe - T)         # slot air + divider + shelf
        net_in3 = gross - brace - port_block - DRV_DISP_L / IN3_L
        vb = net_in3 * IN3_L * 1e-3                         # m^3
        L = area * 0.0254**2 * C**2 / ((2*math.pi*FB)**2 * vb) / 0.0254 - 0.732 * r
        xe = L          # mouth via a square bend: centre-line length = xe (see box-designs.md)
    drv_x = (T + CW + T + W) / 2 if W >= 34 else W - T - DRV_OD/2 - 0.5
    return dict(W=W, gross_L=gross*IN3_L, net_L=net_in3*IN3_L, port_L=xe, area=area,
                slack=(W - T) - xe, drv_x=drv_x, brace_len=yi(BRACE_Z + BRACE_H/2) - T)

# ---------------------------------------------------------------- panels (2D cut shapes)
def panels(d):
    W, xe = d['W'], d['port_L']
    b = T * TAN                                             # bevel offset across one thickness
    P = []
    # name, qty, polygon (u,v) of the larger face, dashed bevel line or None, holes, note
    front_holes = [('rect', T, T, T + CW, T + CH, 'port mouth'),
                   ('circle', d['drv_x'], DRV_Z, DRV_CUT/2, 'driver cutout 11.14"'),
                   ('rect', W - T - 1.0 - TERM[0], H - T - 1.0 - TERM[1], W - T - 1.0, H - T - 1.0, 'terminal cup (size to your cup)')]
    P.append(('FRONT baffle', 1, [(0,0),(W,0),(W,H),(0,H)], None, front_holes,
              f'{W:.3f} x {H:.3f}  drawn as seen from OUTSIDE (trunk-lid side)'))
    bl = math.hypot(D_BOT - D_TOP, H)
    P.append(('BACK', 1, [(0,0),(W,0),(W,bl),(0,bl)], None, [],
              f'{W:.3f} x {bl:.3f}  both long edges bevel 25.1 deg, parallel (ends horizontal)'))
    bd = yi(0) - T
    P.append(('BOTTOM', 1, [(0,0),(W,0),(W,bd),(0,bd)], ('h', bd - b), [],
              f'{W:.3f} x {bd:.3f} (underside); back edge bevel 25.1 deg -> {bd-b:.3f} on top'))
    td = yi(H - T) - T
    P.append(('TOP', 1, [(0,0),(W,0),(W,td),(0,td)], ('h', td - b), [],
              f'{W:.3f} x {td:.3f} (underside); back edge bevel 25.1 deg -> {td-b:.3f} on top'))
    ib, it = yi(T) - T, yi(H - T) - T
    P.append(('END', 2, [(0,0),(ib,0),(it,H-2*T),(0,H-2*T)], None, [],
              f'trapezoid {H-2*T:.3f} tall, {ib:.3f} bottom, {it:.3f} top (square cuts)'))
    P.append(('PORT SHELF', 1, [(0,0),(xe-T,0),(xe-T,CW+T),(0,CW+T)], None, [],
              f'{xe-T:.3f} x {CW+T:.3f}'))
    P.append(('PORT DIVIDER', 1, [(0,0),(xe-T,0),(xe-T,CH),(0,CH)], None, [],
              f'{xe-T:.3f} x {CH:.3f}'))
    bl2 = d['brace_len']
    P.append(('BRACE', 1, [(0,0),(bl2 + BRACE_H/2*TAN,0),(bl2 - BRACE_H/2*TAN,BRACE_H),(0,BRACE_H)], None, [],
              f'{BRACE_H} x ~{bl2:.2f}, back end cut 25.1 deg to the slope'))
    return P

# ---------------------------------------------------------------- minimal R12 DXF writer (mm)
class DXF:
    def __init__(s): s.e = []
    def _p(s, *kv): s.e += [str(x) for x in kv]
    def line(s, a, b, layer='CUT', ltype=None):
        s._p(0,'LINE',8,layer, *( (6,ltype) if ltype else ()), 10,a[0]*25.4,20,a[1]*25.4,30,0,11,b[0]*25.4,21,b[1]*25.4,31,0)
    def poly(s, pts, layer='CUT', ltype=None):
        for i in range(len(pts)): s.line(pts[i], pts[(i+1) % len(pts)], layer, ltype)
    def circle(s, c, r, layer='CUT'):
        s._p(0,'CIRCLE',8,layer,10,c[0]*25.4,20,c[1]*25.4,30,0,40,r*25.4)
    def text(s, p, h, txt, layer='TEXT'):
        s._p(0,'TEXT',8,layer,10,p[0]*25.4,20,p[1]*25.4,30,0,40,h*25.4,1,txt)
    def save(s, fn):
        hdr = ['0','SECTION','2','HEADER','9','$ACADVER','1','AC1009','9','$INSUNITS','70','4','0','ENDSEC',
               '0','SECTION','2','TABLES','0','TABLE','2','LTYPE','70','2',
               '0','LTYPE','2','CONTINUOUS','70','0','3','Solid','72','65','73','0','40','0.0',
               '0','LTYPE','2','DASHED','70','0','3','Dashed','72','65','73','2','40','9.0','49','6.0','49','-3.0',
               '0','ENDTAB','0','TABLE','2','LAYER','70','5']
        for name, col in [('CUT',7),('BEVEL',3),('HOLES',1),('TEXT',5),('SHEET',8)]:
            hdr += ['0','LAYER','2',name,'70','0','62',str(col),'6','CONTINUOUS']
        hdr += ['0','ENDTAB','0','ENDSEC','0','SECTION','2','ENTITIES']
        with open(fn, 'w') as f:
            f.write('\n'.join(hdr + s.e + ['0','ENDSEC','0','EOF']) + '\n')

def write_dxf(d, fn):
    x = DXF(); W = d['W']; K = 0.125                        # kerf allowance in the layout
    x.poly([(0,0),(48,0),(48,96),(0,96)], 'SHEET')
    x.text((0, 97), 1.0, f'4x8 sheet 3/4" MDF (units: mm). Layout v4 box, {W}" wide, net {d["net_L"]:.1f} L, fb {FB:.0f} Hz')
    P = panels(d)
    # 38.5"-long strips across the sheet, then the small parts above them
    place, yy = {}, 0.0
    for name in ('FRONT baffle', 'BACK', 'BOTTOM', 'TOP'):
        p = next(q for q in P if q[0] == name); place[name] = [(0, yy)]
        yy += max(v for _, v in p[2]) + K
    side = [('PORT DIVIDER', W + K, 0), ('BRACE', W + K + CH + K, 0)]
    for name, ox, oy in side: place[name] = [(ox, oy)]
    ib = P[4][2][1][0]
    place['END'] = [(0, yy), (ib + K, yy)]
    place['PORT SHELF'] = [(0, yy + H - 2*T + K)]
    for name, qty, poly, bevel, holes, note in P:
        for (ox, oy) in place[name]:
            if name in ('PORT DIVIDER', 'BRACE'):           # rotate 90 deg to fit the 9.5" offcut strip
                tf = lambda u, v: (ox + v, oy + u)
            else:
                tf = lambda u, v: (ox + u, oy + v)
            x.poly([tf(*p) for p in poly])
            if bevel: x.line(tf(0, bevel[1]), tf(poly[1][0], bevel[1]), 'BEVEL', 'DASHED')
            for h in holes:
                if h[0] == 'rect': x.poly([tf(h[1],h[2]),tf(h[3],h[2]),tf(h[3],h[4]),tf(h[1],h[4])], 'HOLES')
                else: x.circle(tf(h[1], h[2]), h[3], 'HOLES')
            lx, ly = tf(0.4, 0.4) if name not in ('PORT DIVIDER', 'BRACE') else (ox + 0.2, oy + 0.4)
            if name not in ('PORT DIVIDER', 'BRACE'):
                x.text(tf(0.4, max(v for _, v in poly) - 1.0), 0.6, f'{name} x{qty}')
                x.text((lx, ly + (2.2 if name == 'FRONT baffle' else 0)), 0.4, note)
    x.text((W + K, 30), 0.35, 'DIVIDER / BRACE (rotated)')
    # reference: side section (end view) to the right of the sheet
    ox, oy = 60, 0
    x.poly([(ox+u, oy+v) for u, v in [(0,0),(D_BOT,0),(D_TOP,H),(0,H)]], 'SHEET')
    x.poly([(ox+u, oy+v) for u, v in [(T,T),(yi(T),T),(yi(H-T),H-T),(T,H-T)]], 'SHEET')
    x.poly([(ox+u, oy+v) for u, v in [(T,T+CH),(T+CW+T,T+CH),(T+CW+T,T+CH+T),(T,T+CH+T)]], 'CUT')
    x.poly([(ox+u, oy+v) for u, v in [(T+CW,T),(T+CW+T,T),(T+CW+T,T+CH),(T+CW,T+CH)]], 'CUT')
    x.text((ox, H + 1), 0.6, 'Side section (front face at left, seatback at right)')
    x.text((ox, -1.5), 0.4, f'outer {D_BOT}" floor / {D_TOP}" top, back {math.degrees(TH):.1f} deg; slot {CH}" x {CW}" along floor')
    # reference: front elevation
    ox, oy = 60, 22
    x.poly([(ox,oy),(ox+W,oy),(ox+W,oy+H),(ox,oy+H)], 'SHEET')
    for h in P[0][4]:
        if h[0] == 'rect': x.poly([(ox+h[1],oy+h[2]),(ox+h[3],oy+h[2]),(ox+h[3],oy+h[4]),(ox+h[1],oy+h[4])], 'HOLES')
        else: x.circle((ox+h[1], oy+h[2]), h[3], 'HOLES'); x.circle((ox+h[1], oy+h[2]), DRV_OD/2, 'SHEET')
    x.poly([(ox+T,oy+T),(ox+d['port_L'],oy+T),(ox+d['port_L'],oy+T+CH+T),(ox+T,oy+T+CH+T)], 'BEVEL')
    x.text((ox, oy + H + 1), 0.6, f'Front elevation: port runs {d["port_L"]:.2f}" from the mouth end (dashed = hidden shelf)')
    x.save(fn)

# ---------------------------------------------------------------- FreeCAD 3D model
def build_freecad(d, stem):
    import FreeCAD as App, Part
    V = App.Vector; s = 25.4
    W, xe = d['W'], d['port_L']
    def prism_yz(pts, x0, x1):          # polygon in (y,z), extruded along x
        w = Part.makePolygon([V(x0*s, y*s, z*s) for y, z in pts + [pts[0]]])
        return Part.Face(w).extrude(V((x1-x0)*s, 0, 0))
    def box(x0, y0, z0, x1, y1, z1):
        return Part.makeBox((x1-x0)*s, (y1-y0)*s, (z1-z0)*s, V(x0*s, y0*s, z0*s))
    front = box(0, 0, 0, W, T, H)
    front = front.cut(box(T, -1, T, T + CW, T + 1, T + CH))
    front = front.cut(Part.makeCylinder(DRV_CUT/2*s, 3*s, V(d['drv_x']*s, -1*s, DRV_Z*s), V(0,1,0)))
    front = front.cut(box(W-T-1-TERM[0], -1, H-T-1-TERM[1], W-T-1, T+1, H-T-1))
    parts = {
        'Front': front,
        'Back': prism_yz([(yo(0),0),(yi(0),0),(yi(H),H),(yo(H),H)], 0, W),
        'Bottom': prism_yz([(T,0),(yi(0),0),(yi(T),T),(T,T)], 0, W),
        'Top': prism_yz([(T,H-T),(yi(H-T),H-T),(yi(H),H),(T,H)], 0, W),
        'End_L': prism_yz([(T,T),(yi(T),T),(yi(H-T),H-T),(T,H-T)], 0, T),
        'End_R': prism_yz([(T,T),(yi(T),T),(yi(H-T),H-T),(T,H-T)], W-T, W),
        'Port_shelf': box(T, T, T+CH, xe, T+CW+T, T+CH+T),
        'Port_divider': box(T, T+CW, T, xe, T+CW+T, T+CH),
        'Brace': prism_yz([(T,BRACE_Z),(yi(BRACE_Z),BRACE_Z),(yi(BRACE_Z+BRACE_H),BRACE_Z+BRACE_H),(T,BRACE_Z+BRACE_H)],
                          BRACE_X, BRACE_X + T),
    }
    doc = App.newDocument('SubBoxV4')
    objs = []
    for n, shp in parts.items():
        o = doc.addObject('Part::Feature', n); o.Shape = shp; objs.append(o)
    drv = doc.addObject('Part::Feature', 'Driver_frame_ref')
    drv.Shape = Part.makeCylinder(DRV_OD/2*s, 0.3*s, V(d['drv_x']*s, 0, DRV_Z*s), V(0,-1,0))
    doc.recompute()
    doc.saveAs(stem + '.FCStd')
    Part.export(objs, stem + '.step')
    # sanity: air volume = outer solid minus panels
    outer = prism_yz([(0,0),(yo(0),0),(yo(H),H),(0,H)], 0, W)
    wood = sum(p.Volume for p in parts.values())
    print(f'FreeCAD check: outer {outer.Volume/1e6:.2f} L, wood {wood/1e6:.2f} L, '
          f'air incl. slot {(outer.Volume-wood)/1e6:.2f} L')

def main():
    W = float(os.environ.get('BOX_W') or (sys.argv[1] if len(sys.argv) > 1 and sys.argv[1][0].isdigit() else 38.5))
    global CW
    for area in (18, 16, 14):                       # biggest slot that still fits straight (>= 3" at the closed end)
        CW = round(area / CH, 2); d = design(W)
        if d['slack'] >= 3: break
    else:
        print('WARNING: even a 14 in^2 port does not fit straight at this width')
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, 'cad'), exist_ok=True)
    stem = os.path.join(here, 'cad', f'box_v4_{W:g}in')
    print(f"W {W}\"  gross {d['gross_L']:.1f} L  net {d['net_L']:.1f} L  port {d['area']:.2f} in2 x {d['port_L']:.2f}\" "
          f"(open end {d['slack']:.1f}\" from far wall)  driver centre x {d['drv_x']:.2f}\"")
    for name, qty, poly, bevel, holes, note in panels(d):
        print(f'  {qty} x {name:13s} {note}')
    write_dxf(d, stem + '.dxf'); print('wrote', stem + '.dxf')
    try:
        import FreeCAD  # noqa
    except ImportError:
        return
    build_freecad(d, stem); print('wrote', stem + '.FCStd / .step')

if __name__ in ('__main__', 'box_cad'):
    main()
