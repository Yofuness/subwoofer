#!/usr/bin/env python3
"""Model the sealed TS-W304R box in a VW Mk4 cabin and fit cut-only Poweramp EQ presets."""
import json
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

PRESETS = [
    {"name": "Sub Flatten - Mild (-6)", "highs_cut": 6.0, "n_pk": 4},
    {"name": "Sub Flatten - Strong (-15)", "highs_cut": 15.0, "n_pk": 5},
    {"name": "Sub Flatten - Max (-30)", "highs_cut": 30.0, "n_pk": 8},
]


def box_numbers():
    vb_gross = (EXT_W - 2 * WALL) * (EXT_D - 2 * WALL) * (EXT_H - 2 * WALL) / IN3_PER_L
    vb = vb_gross - DRIVER_DISPLACEMENT_L
    alpha = VAS_L / vb
    return vb_gross, vb, alpha, QTS * np.sqrt(1 + alpha), FS_DRV * np.sqrt(1 + alpha)


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


def fit(f, target, n_pk):
    pk_f0 = np.geomspace(35, 12000, n_pk)
    # params: LSC f,g | HSC f,g | per PK: logf, q, g
    x0 = [np.log(22), -6, np.log(110), -6]
    lo = [np.log(15), -15, np.log(70), -15]
    hi = [np.log(40), 0, np.log(400), 0]
    for fp in pk_f0:
        x0 += [np.log(fp), 1.0, -3]
        lo += [np.log(25), 0.3, -15]
        hi += [np.log(16000), 6.0, 0]
    w = np.where(f < 200, 3.0, 1.0)

    def bands_from(x):
        bands = [
            {"type": 0, "frequency": float(np.exp(x[0])), "q": 0.707, "gain": float(x[1])},
            {"type": 1, "frequency": float(np.exp(x[2])), "q": 0.707, "gain": float(x[3])},
        ]
        for k in range(n_pk):
            lf, q, g = x[4 + 3 * k: 7 + 3 * k]
            bands.append({"type": 2, "frequency": float(np.exp(lf)), "q": float(q), "gain": float(g)})
        return bands

    res = least_squares(lambda x: w * (eq_db(bands_from(x), f) - target), x0, bounds=(lo, hi), max_nfev=20000)
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
    shelves, pks = out[:2], sorted(out[2:], key=lambda b: b["frequency"])
    return {"name": name, "preamp": 0.0, "parametric": True, "bands": shelves + pks}


def main():
    vb_gross, vb, alpha, qtc, fc = box_numbers()
    print(f"Gross internal {vb_gross:.1f} L, net {vb:.1f} L ({vb / 28.3168:.2f} ft^3)")
    print(f"alpha={alpha:.2f}  Qtc={qtc:.2f}  Fc={fc:.1f} Hz")

    f = np.geomspace(15, 20000, 400)
    room = box_db(f, fc, qtc) + cabin_db(f)

    report_f = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 100, 125, 160, 250, 500, 1000, 4000, 10000]
    presets = []
    rows = {}
    for p in PRESETS:
        tgt = target_db(f, room, p["highs_cut"])
        pa = to_poweramp(p["name"], fit(f, tgt, p["n_pk"]))
        presets.append(pa)
        eq = eq_db(pa["bands"], np.array(report_f, float))
        rows[p["name"]] = (np.interp(report_f, f, tgt), eq)
        err = np.abs(eq_db(pa["bands"], f) - tgt)
        print(f"\n{p['name']}: max fit error {err.max():.1f} dB, max EQ gain {eq_db(pa['bands'], f).max():+.2f} dB")
        for b in pa["bands"]:
            kind = {0: "LowShelf", 1: "HighShelf", 2: "Peak"}[b["type"]]
            print(f"  {kind:9s} {b['frequency']:6d} Hz  Q {b['q']:5.2f}  {b['gain']:+6.1f} dB")

    box_r = box_db(np.array(report_f, float), fc, qtc)
    room_r = np.interp(report_f, f, room)
    print("\nFreq | box | box+cabin | " + " | ".join(f"{n} target/EQ" for n in rows))
    for i, fr in enumerate(report_f):
        cols = " | ".join(f"{rows[n][0][i]:+6.1f}/{rows[n][1][i]:+6.1f}" for n in rows)
        print(f"{fr:5d} | {box_r[i]:+6.1f} | {room_r[i]:+6.1f} | {cols}")

    with open("poweramp_presets/Subwoofer_Flatten_All.json", "w") as fh:
        json.dump(presets, fh, indent=2)
    for pa in presets:
        slug = pa["name"].split(" - ")[1].split(" ")[0].lower()
        with open(f"poweramp_presets/Subwoofer_Flatten_{slug}.json", "w") as fh:
            json.dump([pa], fh, indent=2)


if __name__ == "__main__":
    main()
