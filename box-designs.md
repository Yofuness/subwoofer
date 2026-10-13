# Box designs

Candidate enclosures and their modelled performance. Driver, amp, trunk and existing-box facts
live in [SPECS.md](SPECS.md); decisions and status live in [PLAN.md](PLAN.md). Compare any of these
interactively in [box_compare.html](box_compare.html) (keep its `DEFAULTS` in sync with this file).

**Current direction (2026-10-13):** ported, **tuned to 22 Hz**. Still to decide: **big (90.6 L) vs compact (45 L)**. The list has 3 sealed + 2 main ported options (22 Hz), plus 4 earlier ported candidates for comparison.
Final dimensions wait on Johann's trunk measurements.

| Tags | Option | Net Vb | Port | Outer (16" H) | Trunk use | Max SPL 20/22/25/30/40 Hz |
|---|---|---|---|---|---|---|
|  | **Sealed: current** (existing box) | 36.96 L | n/a | 17" W, 13.5/10.5" D | 15% | 91/93/95/98/103 |
|  | **Sealed: medium** | 69.1 L | n/a | 30" W, 13.5/10.5" D | ~26% | same as current (Xmax-limited) |
|  | **Sealed: large** | 100 L | n/a | ~42.4" W at 13.5/10.5" D (too wide for the 38⅛" between the wells, so it would need to be deeper) | ~36% | same as current (Xmax-limited) |
| `claude` `preferred` | **Ported 22 Hz: compact** | 45 L | 10 in² × 33.4" | 17.9" W, 18/15" D | ~21% | 99/100/102/105/106 |
| `preferred` | **Ported 22 Hz: big** | 90.6 L | 18 in² × 29.3" | 31.4" W, 18/15" D | ~40% | 103/105/107/105/106 |
|  | Ported 22 Hz: compact, small port | 45 L | 8 in² × 26.6" | 17.0" W, 18/15" D | ~20% | same as compact (port speed 18.3 m/s, too fast) |
|  | Ported 25 Hz: half-size | 40 L | 10 in² × 29" | 16.1" W, 18/15" D | ~19% | 96/99/101/104/108 |
| `claude` | Ported 24 Hz: big | 90.6 L | 25.4 in² × 34.8" | ~33" W, 18/15" D | ~40% | 99/105/107/107/107 |
|  | Ported 27 Hz: big | 90.6 L | 25.4 in² × 27" | 32" W, 18/15" D | ~40% | 94/98/107/110/108 |

The four rows below the two 22 Hz designs are earlier candidates, restored to the list (2026-10-13) for comparison. The main decision is still compact vs big at 22 Hz.

Tags: `claude` = Claude's recommendation, `preferred` = Johann's preference (22 Hz chosen; size undecided). Keep these in sync with box_compare.html.

Max SPL is the clean limit (Xmax 4.7 mm or 185 W) at 1 m half-space, before cabin gain.

## Compact 22 Hz option (2026-10-13)

Port length L ∝ A/(fb²·Vb): halving Vb doubles the port, so the area has to shrink. The limit is port air speed (~17 m/s). Port speeds are peak values from box_compare.html's fine frequency sweep; max_spl.py's coarse grid reads ~1 m/s low.

| Design | Port | Outer W (16" H, 18/15" D) | Outer vol | Max SPL 20/22/25/30/40 | Port v |
|---|---|---|---|---|---|
| 90.6 L @ 22 | 18 in² × 29.3" | 31.4" | 136 L | 103/105/107/105/106 | 13.5 m/s |
| **45 L @ 22** | **10 in² × 33.4"** | **17.9"** | **77 L** | **99/100/102/105/106** | **14.6 m/s** |
| 45 L @ 22 | 8 in² × 26.6" | 17.0" | 74 L | same | 18.3 ⚠ over the limit |
| 40 L @ 25 | 10 in² × 29.0" | 16.1" | 70 L | 96/99/101/104/108 | 14.9 m/s |

45 L @ 22 Hz vs the big box: −4 to −5 dB at 20–25 Hz, same from ~30 Hz up. vs current sealed: +7 dB at 20–22 Hz, +6.6 at 25–30 Hz.
Its 33" port needs a U/J fold. Narrow-port friction losses aren't modelled (≈ −0.5 to 1 dB near fb).
≈ 21% of trunk volume vs 40% for the big box.

## 22 Hz design: size and trunk usage (2026-10-13, preliminary, before trunk measurements)

- Slot port 18 in² = **1.24" × 14.5"**, ≈ 29.3" long → port air 8.6 L + port wall 5.2 L. Gross needed ≈ 106.4 L.
- With the same 16" H × 18"/15" D wedge, that's **outer width ≈ 31.4"** (supersedes the earlier "~33"" guess).
- Outer volume 136 L (+ 12 L for the 1.5" grille guard = 148 L) → **37% / 40% of the 368 L trunk** (Bentley SAE figure).
- Footprint with the guard: 31.4" × 19.5" = 612 in² → **45% of the floor** (38⅛ × 36", unverified forum figures).
  That leaves ~16.5" × full width of free floor and ~3.4" beside each wheel well. The current box uses 15% of the volume and 17% of the floor.

## Tuning options at ~90.6 L net (2026-10-13)

| Tuning | Slot area | Port length | Max SPL @ 20 / 25 / 30 / 40 Hz | Subsonic |
|---|---|---|---|---|
| 27 Hz | 25.4 in² | ~27.0" | 94 / 107 / 110 / 108 | ~23 Hz |
| 24 Hz | 25.4 in² | ~34.8" | 99 / 107 / 107 / 107 | ~20 Hz |
| 22 Hz | 18 in² | ~29.3" | 104 / 107 / 105 / 107 | ~18 Hz |
| Current sealed 37 L | — | — | 92 / 95 / 98 / 104 | (none needed) |

Going from 24 to 22 Hz gains +4–5 dB at 18–20 Hz and loses ~2–3 dB at 28–35 Hz. The 22 Hz port's
peak air speed (~13.5 m/s) is fine even with the smaller slot. Port lengths above are for the full 90.6 L
net; a longer port eats more volume, so the box width is re-checked at the final design.

## Ported design (current proposal, 2026-10-13)

| | |
|---|---|
| Outer | **32" W × 16" H × 18" deep at the bottom / 15" at the top** (same 10.62° back slope as the current box) |
| Material | ¾" MDF; one cross-brace |
| Inner | 30.5 × 14.5 × 14.99" average depth → 108.6 L gross |
| Port | Slot, **1.75" × 14.5" (25.4 in²)**, full inner height, using a box wall as one side. **Centre-line length ≈ 27"**, L-shaped (along one side, then along the back). Tune by measuring |
| Net Vb | **≈ 90.6 L** (gross − 1.66 driver − 0.3 brace − port air ≈ 11.2 L − port wall ≈ 4.8 L) |
| Tuning | **fb ≈ 27 Hz** |
| Port air speed | ≈ 10.9 m/s at full output (limit ~17 m/s), so no chuffing expected |
| Fit check | 32" vs 38⅛" between the wells; 18" vs 36" of floor depth; 16" vs 18½" height (internet trunk figures, unverified) |

Port length uses L = A·c²/(ω_b²·Vb) − 0.732·r (one flanged end, wall-loaded slot). The bend adds
a little effective length, so build it ~1" long and trim if a measured fb comes out low.

## Max clean output (`max_spl.py`), added 2026-10-13

Max SPL at 1 m (half-space, before cabin gain), limited by whichever comes first: Xmax 4.7 mm or the
GM-3500T's 185 W (27.2 V into a 4 Ω nominal load). Full lumped model: cone, box, port with QL 7.

**Key insight:** below ~60 Hz a sealed box is *Xmax-limited*, so its max output depends only on
Sd·Xmax, **not on box size**. Sealed 37 L and 69 L have identical ceilings (91 dB @ 20, 95 @ 25, 98 @ 30, 103 @ 40).
Growing the sealed box only changes the curve's shape, which DSP can do for free.

| Hz | 20 | 25 | 28 | 30 | 35 | 40 | 50 | 60+ |
|---|---|---|---|---|---|---|---|---|
| Sealed 37 L (current) | 91.2 | 95.1 | 97.0 | 98.2 | 100.9 | 103.2 | 107.1 | ~110–112 |
| Ported 90.6 L @ 27 Hz | 93 | 107.2 | 109.1 | 109.9 | 108.5 | 108.4 | 110.2 | ~111–112 |
| Difference | +2 | **+12.1** | **+11.9** | **+11.8** | **+7.6** | **+5.2** | +3 | ≈0 |

Below ~22 Hz the ported box falls off a cliff and the cone is unloaded, so a **subsonic filter at ~23 Hz is mandatory**.

## Ported analysis (Small 4th-order vented model, QL = 7)

Every combination tried peaks by at least +3.4 dB, so ported is **never flatter** with Qts 0.70.

| Vb | fb | Peak | F3 | @30 Hz |
|---|---|---|---|---|
| 50 L | 25–30 | +3.8 to 4.7 | 32 | −4.1 |
| 69 L | 25 | +3.5 | 28 | −1.8 |
| 69 L | 30 | +4.7 | 28 | −1.7 |
| 100 L | 25 | +3.4 | 23 | +0.5 |

## Sealed results

| Net Vb | Qtc | Fc | F3 | Peak | @30 Hz | @25 Hz |
|---|---|---|---|---|---|---|
| 36.96 L (existing box, confirmed) | 1.23 | 50.4 | 36.9 | +2.6 dB @ ~62 Hz | −7.1 | −10.8 |
| 52.7 L (old wrong reading, kept for reference) | 1.10 | 45.0 | — | +1.8 dB | −5.3 | −8.9 |
| 60 L | 1.06 | 43.4 | 33.3 | +1.6 | — | — |
| 69 L (proposed) | 1.02 | 41.7 | 32.6 | +1.4 | −4.4 | −7.7 |
| 100 L | 0.93 | 38.1 | 31.1 | +0.9 | −3.5 | −6.5 |
| 150 L | 0.86 | — | 30.1 | +0.5 | −3.0 | −5.6 |
| 254 L (Qtc 0.8) | 0.80 | — | 29.4 | +0.2 | −2.8 | −5.0 |

Past ~70 L the returns diminish quickly. Cabin gain and DSP do the rest more cheaply.

## Driver alternatives (hypothetical, 2026-10-13; Johann is keeping the TS-W304R)

Modelled at 22 Hz tuning with the GM-3500T (27.2 V bridged). Max clean SPL, 1 m.

| Tags | Driver | Key T/S | 45 L @ 22: 20/25/30/40 Hz | 90.6 L @ 22: 20/25/30/40 Hz |
|---|---|---|---|---|
| `preferred` | TS-W304R (current) | Xmax 4.7, Qts 0.70 | 98.6/101.7/104.8/106.3 | 102.9/106.7/104.8/106.3 |
| `claude` | Dayton DCS305-4 (4 Ω SVC) | Xmax 9.3, Qts 0.40, Fs 24.2, Vas 92.3 (Dayton datasheet) | 99.6/103.2/105.7/108.8 | 104.4/107.6/108.7/109.4 |
|  | Skar SDR-12 D4, series 8 Ω | Xmax 13.5, Qts 0.50 (loudspeakerdatabase) | 98.3/101.0/102.7/104.6 | 102.4/104.7/104.7/104.9 |

With only 185 W, the high-Xmax drivers become **amp-limited**, so most of their extra excursion goes unused.
DCS305-4: +1 to +2.5 dB (compact) or +1 to +4 dB (big) over the TS-W304R. The SDR-12 D4 is worse because the amp only
delivers ~92 W into 8 Ω, and a parallel 2 Ω load is too low for the bridged GM-3500T. A driver swap only pays off together with a bigger amp.

### DCS305-4 + new amp scenario (2026-10-13)
- Price: Parts Express **US$104.98** (open box US$88), via an Opentip/Parts Express listing, unverified on PE's own site. MSRP US$110.99–136.99.
- In a 22 Hz box, power needed to reach Xmax 9.3 mm: **45 L: 376–4,863 W** (380+ W even at 35–40 Hz); **90.6 L: 269–1,556 W**. So the driver's **250 W RMS thermal rating is the real limit**, not Xmax.
  The right amp is **~250–300 W RMS @ 4 Ω mono class-D**, gain set for ≤ 250 W. Example: Rockford R500X1D (300 W @ 4 Ω; LPF 50–250 Hz; subsonic not confirmed; possibly discontinued).
- In-car estimate (max clean SPL + assumed cabin gain), 20/22/25/30/40 Hz:

| Setup | 20 | 22 | 25 | 30 | 40 |
|---|---|---|---|---|---|
| Current sealed, W304R, 185 W | 105 | 105 | 105 | 105 | 105 |
| W304R, 45 L @ 22, 185 W | 113 | 112 | 112 | 112 | 108 |
| **DCS305-4, 45 L @ 22, 250 W** | 115 | 115 | 115 | 114 | 112 |
| W304R, 90.6 L @ 22, 185 W | 117 | 118 | 117 | 112 | 108 |
| **DCS305-4, 90.6 L @ 22, 250 W** | 120 | 120 | 119 | 117 | 113 |

  The upgrade is worth **+2 to +5 dB** over the TS-W304R in the same box; the largest gains are at 28–40 Hz.
  The box designs weren't re-optimised for the DCS305-4 (Qts 0.40, Vas 92.3 L), which would claw back maybe ~1 dB.
