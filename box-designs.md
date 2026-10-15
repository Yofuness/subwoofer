# Box designs

Candidate enclosures and their modelled performance. Driver, amp, trunk and existing-box facts
live in [SPECS.md](SPECS.md); decisions and status live in [PLAN.md](PLAN.md). Compare any of these
interactively in [box_compare.html](box_compare.html) (keep its `DEFAULTS` in sync with this file).

**Update (2026-10-15, measured):** 39.5" between the wells, 18" floor depth, seatback steeper than 10.62°. See **Layout v4** below: the extra depth makes a 32"-wide, ~85 L box with a straight port the sweet spot (seat angle still to be measured).

**Current direction (2026-10-15, later):** ported, **tuned to 22 Hz, 75 L net**, built as **layout v3**: wide and shallow along the seatback, front-firing toward the trunk lid. Layout v2 (side-firing) is superseded. Size settled at **75 L** (Johann, 2026-10-15). The list has 3 sealed + 2 main ported options (22 Hz), plus 4 earlier ported candidates for comparison.
Final dimensions wait on Johann's trunk measurements.

| Tags | Option | Net Vb | Port | Outer (16" H) | Trunk use | Max SPL 20/22/25/30/40 Hz |
|---|---|---|---|---|---|---|
|  | **Sealed: current** (existing box) | 36.96 L | n/a | 17" W, 13.5/10.5" D | 15% | 91/93/95/98/103 |
|  | **Sealed: medium** | 69.1 L | n/a | 30" W, 13.5/10.5" D | ~26% | same as current (Xmax-limited) |
|  | **Sealed: large** | 100 L | n/a | ~42.4" W at 13.5/10.5" D (too wide for the 38⅛" between the wells, so it would need to be deeper) | ~36% | same as current (Xmax-limited) |
|  | **Ported 22 Hz: compact** | 45 L | 10 in² × 33.4" | 11.7" W, 27/24" D (v2) | ~21% | 99/100/102/105/106 |
| `preferred` | **Ported 22 Hz: medium 75 L** | 75.1 L | 14 in² × 27.6" | **v3: 36" W × 16" H × 13.8/10.8" D** (v2 was 17" W, 27/24" D) | ~32% | 103/104/105/105/106 |
| `claude` | **Ported 22 Hz: v4 32" wide** (20° seat assumed) | 84.6 L | 16 in² × 27.9" | 32" W × 16" H × 18"/12.2" D | ~34% | 103/105/106/105/106 |
|  | Ported 22 Hz: v4 max width (20° seat assumed) | 105.6 L | 18 in² × 24.9" | 38.5" W × 16" H × 18"/12.2" D | ~41% | 103/106/107/105/106 |
|  | Ported 22 Hz: 16" wide + 1" grate (v2, superseded) | 69.9 L | 13 in² × 27.6" | 16.0" W, 27/24" D (v2) | ~29% (+ grate) | 102/103/105/105/106 |
|  | **Ported 22 Hz: big** | 90.6 L | 18 in² × 29.3" | 20.2" W, 27/24" D (v2) | ~37% | 103/105/107/105/106 |
|  | Ported 22 Hz: compact, small port | 45 L | 8 in² × 26.6" | 17.0" W, 18/15" D | ~20% | same as compact (port speed 18.3 m/s, too fast) |
|  | Ported 25 Hz: half-size | 40 L | 10 in² × 29" | 16.1" W, 18/15" D | ~19% | 96/99/101/104/108 |
|  | Ported 24 Hz: big | 90.6 L | 25.4 in² × 34.8" | ~33" W, 18/15" D | ~40% | 99/105/107/107/107 |
|  | Ported 27 Hz: big | 90.6 L | 25.4 in² × 27" | 32" W, 18/15" D | ~40% | 94/98/107/110/108 |

The four rows below the two 22 Hz designs are earlier candidates, restored to the list (2026-10-13) for comparison. The main decision is still compact vs big at 22 Hz.

Tags: `claude` = Claude's recommendation, `preferred` = Johann's preference (22 Hz chosen; 75 L picked before the v4 measurements). Keep these in sync with box_compare.html.

Max SPL is the clean limit (Xmax 4.7 mm or 185 W) at 1 m half-space, before cabin gain.

## Layout v4: measured trunk, 18" deep, steeper seatback (2026-10-15, latest)

**New measurements (Johann):** 39.5" between the wheel wells (the forum said 38⅛"), the box may be **18" deep at the floor** (the current box is 13.5"), and the **seatback leans more than the current box's 10.62°** (angle not measured yet).

**Why the angle matters.** The front face is vertical and the back follows the seat. Outer top depth = 18 − 16·tan θ. Inner average depth (at z = 8") = 18 − 0.75 front − 0.75/cos θ back − 8·tan θ. Per inch of outer width you get 14.5" × that depth:

| Seat angle θ | Outer top depth | Inner avg depth | Gross L per inch of width | 75 L (88.3 L gross) needs |
|---|---|---|---|---|
| 10.62° (old box, **too shallow** for this seat) | 15.0" | 14.99" | 3.56 | 26.3" W |
| 15° | 13.7" | 14.33" | 3.41 | 27.4" W |
| **20° (working assumption)** | **12.2"** | **13.54"** | **3.22** | **28.9" W** |
| 25° | 10.5" | 12.69" | 3.02 | 30.8" W |
| 30° | 8.8" | 11.77" | 2.80 | 33.1" W |

A 10.62° back against a steeper seat touches at the **top** first and leaves a wedge of air behind the bottom, so the old angle can't use the 18".

**Port fit:** run the slot straight along the floor (1.75" tall). It needs an inner width ≳ port length + ~2" clearance at the closed end. A 75 L box at 28.9" W (27.4" inner) with its 27.2" port **doesn't fit straight** and would need a bend.
Port wall now modelled as shelf top + side wall (¾"), about 3.4 L for a 27" port. That's less than the 4.9 L assumed in v3, which is why the v3 numbers were slightly pessimistic.

**Candidates at 20° (outer 16" H × 18"/12.2" D), fb 22 Hz:**

| Outer W | Port | Net Vb | Port L | Port v | Outer vol / trunk | Max SPL 20/22/25/30/40 |
|---|---|---|---|---|---|---|
| 28.9" | 14 in² | 76.2 L | 27.2" (needs bend) | 15.4 m/s | 114 L / 31% | 102.8/103.9/105.5/104.8/106.3 |
| 31" | 16 in² | 80.8 L | 29.3" (tight) | 13.9 | 123 L / 33% | 102.9/104.3/105.9/104.8/106.3 |
| **32"** | **16 in² (1.75" × 9.1")** | **84.6 L** | **27.9", straight in 30.5" inner** | **14.5** | **127 L / 34%** | **102.9/104.7/106.3/104.8/106.3** |
| 38.5" (max) | 18 in² | 105.6 L | 24.9" | 15.0 | 152 L / 41% | 102.9/106.3/106.9/104.8/106.3 |
| v3 75 L, for comparison | 14 in² | 75.1 L | 27.6" | 15.3 | 116 L / 32% | 102.7/103.8/105.5/104.8/106.4 |

Sensitivity of the 32" box to the angle: 15° gives 91.2 L (+0.5 dB at 22 Hz); 25° gives 77.3 L, 30.7" port (no longer fits straight; go 33–34" wide or use 18 in²).

**Takeaways**
- **20 Hz and 30–40 Hz don't move at all** (Xmax-limited above fb, port-limited below it). Volume only buys output at **22–25 Hz**: 32" W gives +0.9/+0.8 dB over v3, and the 38.5" max box gives +2.5/+1.4 dB.
- **Claude's pick: 32" W × 16" H × 18" D (back at the measured seat angle), ~85 L, 16 in² straight floor slot.** It's 4" *narrower* than v3, has the straight port, keeps ~7.5" of floor beside it for the jack or loading slack, and gives a free ~1 dB. The 38.5" box costs another 25 L of trunk for +1.6 dB at 22 Hz, with ½" of slack per side.
- Fit check: 32" vs 39.5" leaves 3.75" per side. **Also check the trunk-lid opening width** (the MTX JETTA10 at 35¾" W is known to fit).
- **Needed before the final design:** the seat angle (depth at the floor vs at 16" up), and where the 39.5" was measured (floor vs at the seatback).

## Layout v3: wide along the seatback, front-firing (2026-10-15, superseded by v4)

Johann changed his mind: the box should sit **as far back as possible, against the rear seatback, very wide and shallow**, running along the seatback.
**75 L net @ 22 Hz** (14 in² port, ~27.6" long) is kept. The 16" height and 10.62° seatback wedge are kept. The driver fires toward the trunk lid, as on the current box.

Gross needed = 75.1 + 1.66 driver + 0.3 brace + 6.3 port air + ~4.9 port wall = **88.3 L**. With 14.5" inner height, inner avg depth = gross / ((W − 1.5) × 14.5):

| Outer W | Outer depth (bottom / top) | Outer vol | Trunk share |
|---|---|---|---|
| 30" | 16.1" / 13.1" | 114 L | 31% |
| 32" | 15.2" / 12.2" | 115 L | 31% |
| 34" | 14.4" / 11.4" | 115 L | 31% |
| **36" (proposed)** | **13.8" / 10.8"** | **116 L** | **32%** |
| 38" | 13.2" / 10.2" | 117 L | 32% |

- **Proposal: 36" W × 16" H × 13.8"/10.8" D.** That's basically the current box's side profile (13.5/10.5) stretched to 36" wide. It leaves ~1" of slack against the
  38⅛" wheel-well gap, which is an unverified forum figure, so **measuring the width at the seatback is critical**. 38" would be too tight to rely on.
- **Driver:** front-firing, on the trunk-lid face. Inner depth at the driver's centre is ≈ 10.8"; the magnet needs 5.31" + 0.75" baffle, which leaves ~4.7" behind it. OK.
- **Port:** 27.6" fits straight along the width (inner 34.5"), so **no bends**. Concept: a low slot along the floor (e.g. 1.75" tall × 8" deep = 14 in²) running across the box,
  with its mouth on the front face at one end and the driver toward the other end, raised slightly (centre ~8.75") to clear the port shelf. A shelf wall uses ~2.7 L instead of
  the ~4.9 L assumed, so there's ~2 L of margin to trim back at final design. Final geometry comes after measurements.
- **Grille:** a generic 12" sub grille over the driver (Johann, 2026-10-15). It needs ≥ ~1.15" of clearance (spacers if needed). The port mouth stays open on the front face: keep cargo clear, or add a perforated strip.
- **Floor left over:** about 36" − 13.8" − guard ≈ 20" of clear floor depth in front of the box (if the floor is ~36", unverified).
- **Measure:** width between the wheel wells **right at the seatback** (they may intrude there), and the seatback angle. If the seat is wider above the wells,
  a stepped box could reach over them (only if needed).

## Layout v2: side-firing, driver's side of the trunk (2026-10-15, superseded by v3)

Constraints from Johann (judged by eye, not tape-measured): height ≤ 16" (current box), depth seatback→lid ≤ 2 × 13.5" = **27"** at the bottom.
The back keeps the 10.62° seatback slope (the **wedge is required by the rear seats**; angle from subwoofer.skp, to be re-measured), so the top is **24"** deep. The box sits on the **driver's side**, and the **driver is on the passenger-side panel**, firing across the trunk.

Inner cross-section (the side profile): 14.5" tall × 23.99" average depth = 347.8 in², which works out to **5.70 L per inch of inner width**.

| | Compact 45 L @ 22 Hz | **Medium 75.1 L @ 22 Hz (17" wide)** | Big 90.6 L @ 22 Hz |
|---|---|---|---|
| Port | 10 in² × ~33.4" | **14 in² × ~27.6"** | 18 in² × ~29.3" |
| Port air + port wall | 5.5 + ~6.0 L | 6.3 + ~4.8 L | 8.6 + ~5.2 L |
| Gross internal | 58.4 L | **88.3 L** | 106.4 L |
| **Outer W × H × D** | **11.7" × 16" × 27"/24"** | **17.0" × 16" × 27"/24"** | **20.2" × 16" × 27"/24"** |
| Outer volume / trunk share | 79 L / ~21% | 114 L / ~31% | 135 L / ~37% |
| Peak port speed | ~14.6 m/s | ~15.3 m/s | ~13.5 m/s |
| Max SPL 20/22/25/30/40 | 99/100/102/105/106 | **103/104/105/105/106** | 103/105/107/105/106 |

Layout notes:
- **Driver on the passenger-side panel** (27"/24" × 16"): the 12.5" frame fits with ~1.75" top/bottom margin. Magnet depth 5.31" + 0.75" panel
  leaves ~4" behind the magnet in the compact box (10.2" inner width), so there's room for the port to run along the far (driver-side) inner wall.
- **The port won't fit straight:** 29–33" is longer than the ~24" inner depth, so it needs **one bend** (an L running along the inner driver-side wall, then along the bottom or the seatback).
  The port mouth most likely goes on the rear (trunk-lid) face or the passenger face. Pick whichever the guard covers more easily. Slot shape is TBD
  (a 10 in² full-height slot would be only 0.69" wide, which is too narrow, so the compact box probably wants something like a 1.25" × 8" slot).
- The guard now covers the passenger-side face (plus the port mouth if it's on another face).
- ⚠ **Wheel well:** a 27"-deep box on the driver's side is likely to run into the wheel well. It has to sit inboard of the well, or be notched around it. **Needs measuring.**
- **Medium (2026-10-15):** Johann wants to keep the current 17" width. Inner 15.5" × 347.8 in² = 88.3 L gross. Port area was swept at fb 22: 10 in² → 22.3 m/s ✗, 12 → 18.2 ✗, **14 → 15.3 m/s ✓ (75.1 L net, 27.6" port)**, 16 → 13.0 but 71.7 L.
  Within 0–2 dB of the big box everywhere, and +4 dB over compact at 20–22 Hz.
- **16" + grate (2026-10-15):** Johann asked for 1" less width so a grate fits within the old 17" envelope. Inner 14.5" × 347.8 = 82.6 L gross.
  Port sweep: 12 in² → 71.4 L, 24.9", 17.2 m/s ✗ · **13 in² → 69.9 L, 27.6", 15.6 m/s ✓** · 14 → 68.2 L, 30.5", 14.2 · 15 → 66.4 L, 33.7", 13.1.
  Max SPL 20/22/25/30/40 = 102.1/103.2/105.0/104.8/106.4 vs 102.7/103.8/105.5/104.8/106.4 for 17": **−0.6 dB at most**. It's now Claude's pick (the grate is a requirement).
  ⚠ The grate needs ~1.15" from the mounting ring to the inside of the mesh (assumed 0.75" surround + ~0.4" on hard hits), so **1" is tight. Measure the surround height.**
  If it needs 1.5", make the box 15.5" (≈ −0.6 dB more).
- Supersedes the earlier 18"/15"-deep, front-firing geometry (31.4" / 17.9" wide).

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
