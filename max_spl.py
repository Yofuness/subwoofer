#!/usr/bin/env python3
"""Max clean SPL (Xmax- or amp-limited) for TS-W304R in sealed vs vented boxes. 1 m half-space, no cabin gain."""
import numpy as np
rho, c = 1.18, 343.0
FS, QMS, VAS, RE, BL, SD, MMS, XMAX = 28.6, 13.3, 77.9e-3, 3.0, 10.4, 0.052, 0.150, 4.7e-3
CMS = VAS / (rho * c**2 * SD**2); RMS = 2*np.pi*FS*MMS/QMS
P_AMP, Z_NOM = 185.0, 4.0                     # GM-3500T bridged
V_AMP = np.sqrt(P_AMP * Z_NOM)                 # ~27.2 V
f = np.array([20, 22, 25, 28, 30, 32, 35, 40, 45, 50, 60, 70, 80], float)

def solve(vb_l, fb=None, ql=7.0, v=1.0):
    w = 2*np.pi*f; cab = vb_l*1e-3/(rho*c**2)
    if fb is None:
        zab = 1/(1j*w*cab); map_ = None
    else:
        map_ = 1/((2*np.pi*fb)**2*cab); ral = ql/(2*np.pi*fb*cab)
        zab = 1/(1j*w*cab + 1/(1j*w*map_) + 1/ral)
    zm = 1j*w*MMS + RMS + 1/(1j*w*CMS) + BL**2/RE + SD**2*zab
    u = (BL*v/RE)/zm                             # cone velocity
    uc = u*SD; p = uc*zab
    up = p/(1j*w*map_) if fb else 0
    utot = np.abs(up - uc)                        # front & port radiate, cone back goes in box
    x = np.abs(u/(1j*w))
    return x, utot, np.abs(up)

def max_spl(vb_l, fb=None):
    x, u, up = solve(vb_l, fb)
    v = np.minimum(V_AMP, XMAX/x)                 # whichever limit hits first
    pr = rho*2*np.pi*f*u*v/(2*np.pi*1.0)          # half-space, 1 m
    return 20*np.log10(pr/2e-5), v, up*v

if __name__ == "__main__":
    print("Hz      " + " ".join(f"{int(x):>5}" for x in f))
    for name, vb, fb in [("sealed 37", 36.96, None), ("sealed 69", 69.1, None)] + \
                        [(f"vent {vb}L/{fb}", vb, fb) for vb in (60, 80, 100, 120, 140) for fb in (25, 28, 30, 32)]:
        s, v, _ = max_spl(vb, fb)
        print(f"{name:14s}" + " ".join(f"{x:5.1f}" for x in s))
