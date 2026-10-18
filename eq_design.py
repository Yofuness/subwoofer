#!/usr/bin/env python3
"""Model the TS-W304R box in a VW Mk4 cabin and fit cut-only Poweramp EQ presets.

    python3 eq_design.py          -> ported FINAL box (82.1 L @ 22 Hz)  -> poweramp_presets/Subwoofer_Ported22.json
                                     one preset, box-only (no cabin gain), nothing touched above 100 Hz
    python3 eq_design.py sealed   -> old sealed box (legacy presets)    -> poweramp_presets/Subwoofer_Flatten_*.json
"""
import json, sys
import max_spl
import numpy as np
from scipy.optimize import least_squares

FS = 48000.0
IN3_PER_L = 61.0237

# Box geometry from subwoofer.skp (inches)
EXT_W, EXT_D, EXT_H, WALL = 17.0, 16.25, 16.0, 0.75
DRIVER_DISPLACEMENT_L = 1.66

# Pioneer TS-W304R T/S
FS_DRV, QTS, VAS_L = 28.6, 0.70, 77.9

# Cabin gain assumption: ~9 dB/oct rise below this corner (Mk4 Golf/Jetta sized cabin)
CABIN_FC, CABIN_ORDER = 55.0, 3

SUB_BAND = (28.0, 80.0)      # region flattened to its own weakest point
BLEND_END = 160.0            # above this, full "highs" cut applies
SUBSONIC = [(20.0, -6.0), (15.0, -12.0)]  # extra cut below the sub band (excursion protection)

# Ported FINAL box (box-designs.md -> FINAL size). Response from max_spl.solve (same lumped model as box_compare.html)
PORTED = len(sys.argv) < 2 or sys.argv[1] != "sealed"
VB_PORTED, FB_PORTED, QL_PORTED = 82.1, 22.0, 7.0
if PORTED:
    SUB_BAND = (22.0, 100.0)       # cut the box's 40-60 Hz hump down to its 100 Hz level; 0 dB from 100 Hz up
    SUBSONIC_FC = 21.0             # target = 4th-order Butterworth HPF (24 dB/oct) below the band
    EXC_MARGIN = 3.0               # keep >= 3 dB under the Xmax limit below the band (see excursion_cap_db)

PRESETS = [
    {"name": "Sub Flatten - Mild (-6)", "highs_cut": 6.0, "n_pk": 5 if PORTED else 4},
    {"name": "Sub Flatten - Strong (-15)", "highs_cut": 15.0, "n_pk": 5},
    {"name": "Sub Flatten - Max (-30)", "highs_cut": 30.0, "n_pk": 8},
]


def box_numbers():
    vb_gross = (EXT_W - 2 * WALL) * (EXT_D - 2 * WALL) * (EXT_H - 2 * WALL) / IN3_PER_L
    vb = vb_gross - DRIVER_DISPLACEMENT_L
    alpha = VAS_L / vb
    return vb_gross, vb, alpha, QTS * np.sqrt(1 + alpha), FS_DRV * np.sqrt(1 + alpha)


def ported_db(f):
    """1 V response of the vented box (dB, arbitrary ref), and the cone excursion per volt (m/V)."""
    max_spl.f = np.asarray(f, float)
    x, u, _ = max_spl.solve(VB_PORTED, FB_PORTED, QL_PORTED)
    return 20 * np.log10(max_spl.rho * max_spl.f * u / 2e-5), x


def excursion_cap_db(f, room):
    """Most the EQ may leave (dB re its 0 dB passband) so the cone stays EXC_MARGIN under Xmax when the 0 dB
    part of the passband is driven to the amp's full 27 V: 20 log10(min(V_amp, Xmax / x(f)) / V_amp) - margin."""
    _, x = ported_db(f)
    vmax = np.minimum(max_spl.V_AMP, max_spl.XMAX / x)
    return 20 * np.log10(vmax / max_spl.V_AMP) - EXC_MARGIN, vmax


def box_db(f, fc, qtc):
    s = 1j * f / fc
    return 20 * np.log10(np.abs(s**2 / (s**2 + s / qtc + 1)))


def cabin_db(f):
    return 10 * np.log10(1 + (CABIN_FC / f) ** CABIN_ORDER)


def biquad_db(kind, f0, q, gain, f):
    # RBJ Audio EQ Cookbook
    A = 10 ** (gain / 40)
    w0 = 2 * np.pi * f0 / FS
    alpha = np.sin(w0) / (2 * q)
    cw = np.cos(w0)
    if kind == 2:
        b = [1 + alpha * A, -2 * cw, 1 - alpha * A]
        a = [1 + alpha / A, -2 * cw, 1 - alpha / A]
    else:
        sA = 2 * np.sqrt(A) * alpha
        if kind == 0:
            b = [A * ((A + 1) - (A - 1) * cw + sA), 2 * A * ((A - 1) - (A + 1) * cw), A * ((A + 1) - (A - 1) * cw - sA)]
            a = [(A + 1) + (A - 1) * cw + sA, -2 * ((A - 1) + (A + 1) * cw), (A + 1) + (A - 1) * cw - sA]
        else:
            b = [A * ((A + 1) + (A - 1) * cw + sA), -2 * A * ((A - 1) + (A + 1) * cw), A * ((A + 1) + (A - 1) * cw - sA)]
            a = [(A + 1) - (A - 1) * cw + sA, 2 * ((A - 1) - (A + 1) * cw), (A + 1) - (A - 1) * cw - sA]
    z = np.exp(-1j * 2 * np.pi * f / FS)
    h = (b[0] + b[1] * z + b[2] * z**2) / (a[0] + a[1] * z + a[2] * z**2)
    return 20 * np.log10(np.abs(h))


def eq_db(bands, f):
    return sum(biquad_db(b["type"], b["frequency"], b["q"], b["gain"], f) for b in bands)


def target_db(f, room, highs_cut):
    if PORTED:
        return target_ported(f, room, highs_cut)
    in_band = (f >= SUB_BAND[0]) & (f <= SUB_BAND[1])
    ref = room[in_band].min()
    t = np.minimum(0.0, ref - room)
    t_lo = np.interp(SUB_BAND[0], f, t)
    for i, fi in enumerate(f):
        if fi < SUB_BAND[0]:
            pts_f = [SUB_BAND[0]] + [p[0] for p in SUBSONIC]
            pts_d = [0.0] + [p[1] for p in SUBSONIC]
            extra = np.interp(np.log(fi), np.log(pts_f[::-1]), pts_d[::-1])
            t[i] = t_lo + extra
    t_hi = np.interp(SUB_BAND[1], f, t)
    blend = (f > SUB_BAND[1]) & (f < BLEND_END)
    x = np.log(f[blend] / SUB_BAND[1]) / np.log(BLEND_END / SUB_BAND[1])
    t[blend] = t_hi + (-highs_cut - t_hi) * x
    t[f >= BLEND_END] = -highs_cut
    return t - max(0.0, t.max())


def target_ported(f, room, highs_cut):
    in_band = (f >= SUB_BAND[0]) & (f <= SUB_BAND[1])
    t = np.minimum(0.0, np.interp(SUB_BAND[1], f, room) - room)   # cut-only: hump down to the 100 Hz level
    t[~in_band] = 0.0
    t_lo = np.interp(SUB_BAND[0], f, t)
    lo = f < SUB_BAND[0]
    hpf = -10 * np.log10(1 + (SUBSONIC_FC / f) ** 8)              # 4th-order Butterworth magnitude
    t[lo] = t_lo + hpf[lo] - np.interp(SUB_BAND[0], f, hpf)
    cap, _ = excursion_cap_db(f, room)
    t[lo] = np.minimum(t[lo], cap[lo])
    return t


def fit(f, target, n_pk):
    n_ls = 2 if PORTED else 1
    n_hs = 0 if PORTED else 1                                                  # no high shelf: flat above 100 Hz
    pk_f0 = (np.r_[13.0, 18.0, 45.0, np.geomspace(60, 80, n_pk - 3)] if PORTED   # subsonic notches + hump
             else np.geomspace(35, 12000, n_pk))
    # params: LSC f,g (x n_ls) | HSC f,g | per PK: logf, q, g
    x0, lo, hi = [], [], []
    nq = 1 if PORTED else 0                       # ported: shelf Q is free (steeper subsonic knee)
    for k in range(n_ls):
        x0 += [np.log(18 + 2 * k), -12] + [0.707] * nq
        lo += [np.log(12), -15] + [0.5] * nq
        hi += [np.log(30), 0] + [1.4] * nq
    sl = 2 + nq
    if n_hs:
        x0 += [np.log(110), -6]; lo += [np.log(70), -15]; hi += [np.log(400), 0]
    pk0 = sl * n_ls + 2 * n_hs
    for fp in pk_f0:
        x0 += [np.log(fp), 1.0, -3]
        lo += [np.log(12 if PORTED else 25), 0.3, -15]
        hi += [np.log(90 if PORTED else 16000), 6.0, 0]
    w = np.where(f < 200, 3.0, 1.0)
    if PORTED:
        w = np.where(f < SUB_BAND[0], 6.0, w)      # the subsonic is driver protection: fit it hardest
        w = np.where((f >= SUB_BAND[0]) & (f <= SUB_BAND[1]), 5.0, w)
        w = np.where(f > SUB_BAND[1], 8.0, w)      # must stay ~0 dB above 100 Hz

    def bands_from(x):
        bands = [{"type": 0, "frequency": float(np.exp(x[sl * k])), "q": float(x[sl * k + 2]) if nq else 0.707,
                  "gain": float(x[sl * k + 1])} for k in range(n_ls)]
        if n_hs:
            bands.append({"type": 1, "frequency": float(np.exp(x[sl * n_ls])), "q": 0.707, "gain": float(x[sl * n_ls + 1])})
        for k in range(n_pk):
            lf, q, g = x[pk0 + 3 * k: pk0 + 3 + 3 * k]
            bands.append({"type": 2, "frequency": float(np.exp(lf)), "q": float(q), "gain": float(g)})
        return bands

    def resid(x):
        e = eq_db(bands_from(x), f)
        r = w * (e - target)
        return np.r_[r, 30 * np.maximum(0.0, e)] if PORTED else r   # ported: hard penalty on any boost (cut-only)
    res = least_squares(resid, x0, bounds=(lo, hi), max_nfev=20000)
    return bands_from(res.x)


def to_poweramp(name, bands):
    out = []
    for b in bands:
        if b["type"] == 2 and abs(b["gain"]) < 0.2:
            continue
        out.append({
            "type": b["type"],
            "channels": 0,
            "frequency": int(round(b["frequency"])),
            "q": round(b["q"], 2),
            "gain": round(min(0.0, max(-15.0, b["gain"])), 1),
            "color": 0,
        })
    shelves = [b for b in out if b["type"] == 0] + [b for b in out if b["type"] == 1]
    pks = sorted((b for b in out if b["type"] == 2), key=lambda b: b["frequency"])
    return {"name": name, "preamp": 0.0, "parametric": True, "bands": shelves + pks}


def main():
    f = np.geomspace(12 if PORTED else 15, 20000, 400)
    if PORTED:
        print(f"Ported: Vb {VB_PORTED} L, fb {FB_PORTED} Hz, Ql {QL_PORTED}; box only (no cabin gain); hump cut to the "
              f"{SUB_BAND[1]:g} Hz level, 0 dB above; subsonic 24 dB/oct @ {SUBSONIC_FC:g} Hz, {EXC_MARGIN:g} dB under Xmax at 27 V")
        box1, _ = ported_db(f)
        box1 -= np.interp(100, f, box1)
        room = box1
        presets_def = [{"name": "Sub Ported22", "highs_cut": 0.0, "n_pk": 5}]
        prefix = "Subwoofer_Ported22"
    else:
        vb_gross, vb, alpha, qtc, fc = box_numbers()
        print(f"Gross internal {vb_gross:.1f} L, net {vb:.1f} L ({vb / 28.3168:.2f} ft^3)")
        print(f"alpha={alpha:.2f}  Qtc={qtc:.2f}  Fc={fc:.1f} Hz")
        room = box_db(f, fc, qtc) + cabin_db(f)
        presets_def, prefix = PRESETS, "Subwoofer_Flatten"

    report_f = [12, 15, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 100, 125, 160, 250, 500, 1000, 4000, 10000]
    presets = []
    rows = {}
    for p in presets_def:
        tgt = target_db(f, room, p["highs_cut"])
        pa = to_poweramp(p["name"], fit(f, tgt, p["n_pk"]))
        presets.append(pa)
        eq = eq_db(pa["bands"], np.array(report_f, float))
        rows[p["name"]] = (np.interp(report_f, f, tgt), eq)
        err = np.abs(eq_db(pa["bands"], f) - tgt)
        if PORTED:
            cap, _ = excursion_cap_db(f, room)
            lo_ = f < SUB_BAND[0]
            over = (eq_db(pa["bands"], f) - (cap + EXC_MARGIN))[lo_].max()
            print(f"\n{p['name']}: below {SUB_BAND[0]:g} Hz the EQ stays {-over:.1f} dB under the Xmax limit (need >= 0)", end="")
        print(f"\n{p['name']}: max fit error {err.max():.1f} dB, max EQ gain {eq_db(pa['bands'], f).max():+.2f} dB")
        for b in pa["bands"]:
            kind = {0: "LowShelf", 1: "HighShelf", 2: "Peak"}[b["type"]]
            print(f"  {kind:9s} {b['frequency']:6d} Hz  Q {b['q']:5.2f}  {b['gain']:+6.1f} dB")

    box_r = np.interp(report_f, f, room) if PORTED else box_db(np.array(report_f, float), fc, qtc)
    room_r = np.interp(report_f, f, room)
    print("\nFreq | box | box+cabin | " + " | ".join(f"{n} target/EQ" for n in rows))
    for i, fr in enumerate(report_f):
        cols = " | ".join(f"{rows[n][0][i]:+6.1f}/{rows[n][1][i]:+6.1f}" for n in rows)
        print(f"{fr:5d} | {box_r[i]:+6.1f} | {room_r[i]:+6.1f} | {cols}")

    if PORTED:
        with open(f"poweramp_presets/{prefix}.json", "w") as fh:
            json.dump(presets, fh, indent=2)
        return
    with open(f"poweramp_presets/{prefix}_All.json", "w") as fh:
        json.dump(presets, fh, indent=2)
    for pa in presets:
        slug = pa["name"].split(" - ")[1].split(" ")[0].lower()
        with open(f"poweramp_presets/{prefix}_{slug}.json", "w") as fh:
            json.dump([pa], fh, indent=2)


if __name__ == "__main__":
    main()
