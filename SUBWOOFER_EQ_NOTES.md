# Subwoofer EQ Correction Project: Notes

## ▶ CURRENT: presets for the ported FINAL box (82.1 L @ 22 Hz), added 2026-10-17

`python3 eq_design.py` (needs numpy + scipy) → `poweramp_presets/Subwoofer_Ported22_{All,mild,strong,max}.json`,
full output in `poweramp_presets/design_output_ported22.txt`. The old `Subwoofer_Flatten_*` presets below are for
the old sealed box only (`python3 eq_design.py sealed`).

**Model:** the 1 V response comes from `max_spl.solve(82.1, 22, Ql=7)`, the same lumped model as `box_compare.html`.
The cabin gain is the same assumption as before (+9 dB/oct below 55 Hz, **not measured**). Together they give an
in-car response that's **nearly flat from 18 to 50 Hz** (88 dB/V ±0.5): the box is falling below fb just as
cabin gain rises. Above that it sags to −4 dB at 80 Hz relative to the plateau.

**Target (cut-only, never above 0 dB):**
- **22–63 Hz:** flattened to the band's weakest point. In practice that cuts about 3 dB at 35–45 Hz, where box and cabin overlap.
- **63–160 Hz:** log blend into the highs cut. The amp's fixed 80 Hz / 12 dB LPF does the real crossover.
- **Below 22 Hz: subsonic = 4th-order Butterworth (24 dB/oct) at 21 Hz,** capped so the cone stays under Xmax.
  The cap is max in-car SPL(f) − (the flat in-band max) − 3 dB margin. The flat in-band max is **111.9 dB at 40 Hz**,
  Xmax-limited, at 1 m before cabin gain. The fit leaves **1.4 dB** of margin at 12 Hz, where it's tightest, and more above that.
  A ported box unloads below fb (x at 27 V: 4.9 mm @ 20 Hz, 10.5 @ 18, 22 @ 15, 25 @ 12), and the GM-3500T has
  no subsonic, so these presets are the driver's only protection.
- **Above 160 Hz:** −6 / −15 / −30 dB depending on the preset.

| Preset | Low shelves | High shelf | Peaks |
|---|---|---|---|
| **Mild (−6)** | 12 Hz −9.8, 12 Hz −10.1 | 125 Hz −6.0 | 13 Hz Q2.38 −9.7 · 39 Hz Q2.43 −3.0 · 143 Hz Q1.60 −1.7 |
| **Strong (−15)** | 12 Hz −10.2 ×2 | 134 Hz −14.9 | 13 Hz Q2.39 −9.5 · 37 Hz Q2.91 −2.8 · 147 Hz Q1.45 −5.4 |
| **Max (−30)** | 12 Hz −10.3, −10.4 | 154 Hz −15.0 | 13 Q2.46 −9.3 · 36 Q3.77 −2.3 · 102 Q3.55 −6.3 · 137 Q2.63 −9.1 · 176 Q2.14 −12.0 · 338 Q0.92 −10.2 · 1701 Q0.30 −14.2 · 15368 Q0.30 −15.0 |

All shelves are Q 0.71. Resulting cut (Mild): 12 Hz −18.3, 15 −12.7, 18 −6.8, 20 −4.8, 25 −2.6, 40 −3.5, 60 −1.1, 80 −1.5 dB.
Fit error is ≤ 1.6 dB (Mild) / 2.0 (Strong) / 4.2 (Max, in the 250 Hz stacked-cut region).

**Gain setting (important):** from 35 to 50 Hz the driver reaches Xmax about **5–6 dB before the amp clips** (at 40 Hz, 9.0 mm at 27 V).
So turning the LC2i up until the amp clips will push the cone past Xmax in that band. Set sub level by ear and
back off at the first sign of distortion or slapping. The EQ can't fix this, because it's a level issue, not a shape one.

**After the build:** measure fb (impedance dip). If it lands off 22 Hz, change `FB_PORTED` and re-run.
Then measure in-car with REW and replace `room`. The cabin-gain guess is still the biggest uncertainty.

---

Project: Poweramp Equalizer presets that correct the in-car bass response of a
sealed Pioneer TS-W304R box using **cut-only** EQ, so the head unit and the car's
factory speakers never see a boosted signal. Sub level is made up downstream with
the AudioControl LC2i Pro bass knob, which only affects the sub path.

## Goal / strategy (as specified by user)

- Don't flatten the curve by boosting the weak bands. Pick the weakest point in the
  sub's passband as the ceiling and cut everything else down to meet it.
- Pull mids/highs down hard to reduce stress on the factory speakers.
- The LC2i Pro supplies the makeup gain for the sub, so deep cuts (up to ~30 dB) are fine.
- Poweramp caps each band at ±15 dB. Overlapping/stacked bands are used to exceed that.
- Several presets with different levels of aggressiveness.

## Hardware

- **Car**: VW Mk4 platform (Bentley Mk4 service manual in this folder).
- **Subwoofer**: Pioneer TS-W304R, 12" (30 cm), 4 Ω single voice coil.
- **Enclosure**: Sealed, ¾" MDF (dimensions below, from `subwoofer.skp`).
- **LOC**: AudioControl LC2i Pro.
- **Amp**: Pioneer GM-3500T, bridged @ 4 Ω (185 W RMS). Built-in LPF fixed at 80 Hz/12 dB, so use that for the "~80 Hz low-pass". No subsonic filter, so the EQ's low-shelf subsonic cut is the only excursion protection in the chain (unless the LC2i Pro adds one).
- **EQ app**: Poweramp Equalizer (standalone companion app), **parametric** mode.

## Box dimensions (extracted from `subwoofer.skp`)

> **⚠ WRONG, superseded (2026-10-13, confirmed from the full vertex table):** a later check of the exact vertex triples in `model.dat`
> shows the box is a **wedge**: 17" W × 16" H, 13.5" deep at the bottom and 10.5" at the top.
> That gives ≈ **37 L net** (Qtc 1.23, Fc 50.4 Hz, hump ≈ +2.6 dB @ 62 Hz), not the
> rectangle below. No vertex sits at a depth of 16.25"; that value is the inner side-panel
> x-coordinate. The 11.125 and 5.375 values are vertices of the 12.5" driver circle polygon, not a cutout or a depth. The presets below were fitted to the wrong (52.7 L) box and **must be re-fitted**. See SPECS.md and PLAN.md.

The `.skp` file is a zip container. The geometry is in `model.dat`, a tagged binary
format. No SketchUp parser was available, so the dimensions were recovered by:

1. Scanning `model.dat` for little-endian 64-bit floats that land on clean 1/32"
   values (SketchUp stores everything in inches), then tallying the recurring ones.
2. Cross-checking against the dimension labels in the embedded thumbnails
   (`meta/preview_thumbnail.png`, `meta/model_thumbnail.png`). The labels are only
   256 px wide, so they're partly legible: roughly "17 ½" (width) and "16 ½"
   (depth). The height label is unreadable.

Recurring values found:

| Value (in) | Hits | Interpretation |
|---|---|---|
| 0.75 | 53 | Panel thickness (¾" MDF) |
| 16.25 | 23 | Outer dimension (depth) |
| 16.0 | 17 | Outer dimension (height) |
| 15.25 | 13 | 16 − 0.75 (inner/panel offset) |
| 17.0 | 9 | Outer dimension (width) |
| 11.125 | 2 | Driver cutout diameter. Matches Pioneer's spec (Ø283 mm = 11.14") exactly, which confirms this is the real box model |
| 5.375 | 2 | ≈ driver mounting depth (Pioneer spec: 135 mm = 5.31") |

**Dimensions used for the model:**

| | Value |
|---|---|
| External W × D × H | 17.0" × 16.25" × 16.0" |
| Wall thickness | 0.75" |
| Internal W × D × H | 15.5" × 14.75" × 14.5" = 3,315 in³ |
| Gross internal volume | 54.3 L (1.92 ft³) |
| Driver displacement (basket + magnet) | −1.66 L |
| Bracing | none visible in model |
| **Net internal volume** | **52.7 L (1.86 ft³)** |

### Dimensions to confirm with a tape measure

These are the parts of the extraction I'm least sure of. Correct them in `eq_design.py`
(`EXT_W`, `EXT_D`, `EXT_H`, `WALL`) and re-run it if they're wrong:

- **External width, depth and height.** The thumbnail labels may read 17½ / 16½, not
  17 / 16¼. If so, net volume rises to ≈ 57 L, Fc drops ~1 Hz, and Qtc drops ~0.02.
  That's negligible for the EQ.
- **Wall thickness.** ¾" assumed. A double-thick baffle would cost ≈ 2.5 L.
- **Any internal bracing or a port.** None visible. The box is assumed sealed and unbraced.

## Pioneer TS-W304R Thiele/Small parameters

From speakerboxlite.com, cross-checked against a second WinISD-format listing:

| Parameter | Value |
|---|---|
| Fs | 28.6 Hz |
| Qts / Qes / Qms | 0.70 / 0.74 / 13.3 |
| Vas | 77.9 L (2.75 ft³) |
| Sd | 520 cm² |
| Mms | 150 g |
| Cms | 0.207 mm/N |
| Bl | 10.4 T·m |
| Re / Le | 3.0 Ω / 2.43 mH |
| Xmax (one-way) | ~5 mm (one source says 4.7 mm) |
| Vd (Sd × Xmax, cone swept volume) | 0.245 L |
| Driver displacement in box | 1.66 L |
| Sensitivity (measured, 1 W/1 m) | 85.8 dB (Pioneer's "95 dB" is a marketing figure) |
| Power | 300 W RMS / 1300 W max |

## Box + cabin model

Sealed-box alignment:

```
α   = Vas / Vb       = 77.9 / 52.7 = 1.48
Qtc = Qts·√(1+α)     = 1.10
Fc  = Fs·√(1+α)      = 45.0 Hz
```

Qtc 1.10 is a "punchy", slightly peaky alignment. In free air the box has a broad
+1.8 dB hump around 55–65 Hz and rolls off at 12 dB/oct below 45 Hz.

**Cabin gain (assumed, not measured):** a Mk4 Golf/Jetta-sized cabin, modelled as a
~9 dB/oct rise below 55 Hz. Together with the box this gives a predicted in-car hump
of about **+5 dB centred near 45 Hz**, falling to about +2.6 dB at 80 Hz and +3 dB at 30 Hz.
The cabin model is the biggest source of uncertainty. A real measurement (see below)
would replace it.

| Hz | Box alone | Box + cabin (predicted) |
|---|---|---|
| 20 | −13.2 | +0.2 |
| 25 | −8.9 | +1.8 |
| 30 | −5.3 | +3.2 |
| 35 | −2.5 | +4.4 |
| 40 | −0.5 | +5.1 |
| 45 | +0.8 | +5.3 |
| 50 | +1.5 | +5.2 |
| 60 | +1.8 | +4.3 |
| 70 | +1.6 | +3.4 |
| 80 | +1.4 | +2.6 |

## EQ design

Target curve for each preset (all cut, nothing above 0 dB):

- **28–80 Hz (sub band):** flattened down to the band's weakest point, which mainly
  means cutting ~2.5 dB out of the 40–55 Hz hump.
- **Below 28 Hz:** extra subsonic cut (−6 dB at 20 Hz, −12 dB at 15 Hz). This protects
  the driver's small ~5 mm Xmax from infrasonic excursion that cabin gain would otherwise exaggerate.
- **80–160 Hz:** smooth log-frequency blend into the highs cut.
- **Above 160 Hz:** flat cut of 6 / 15 / 30 dB, depending on the preset.

Fit with least squares (`eq_design.py`) to RBJ-cookbook biquads at 48 kHz. Gains are
bounded to [−15, 0] dB, which keeps every preset cut-only by construction. Shelf Q is
fixed at 0.707. The −30 dB preset reaches its depth by stacking wide peaking cuts
(≈ −9 to −15 dB each) on top of a −15 dB high shelf.

### Presets (files in `poweramp_presets/`)

`Subwoofer_Flatten_All.json` holds all three presets. Each is also available as its
own file. Full fit output is in `poweramp_presets/design_output.txt`.

**Sub Flatten: Mild (−6)**. Highs −6 dB. Max EQ gain −0.9 dB.

| Type | Hz | Q | Gain |
|---|---|---|---|
| Low shelf | 17 | 0.71 | −15.0 |
| High shelf | 150 | 0.71 | −6.0 |
| Peak | 48 | 3.60 | −2.4 |
| Peak | 154 | 1.88 | −2.6 |

**Sub Flatten: Strong (−15)**. Highs −15 dB. Max EQ gain −1.2 dB.

| Type | Hz | Q | Gain |
|---|---|---|---|
| Low shelf | 17 | 0.71 | −15.0 |
| High shelf | 193 | 0.71 | −15.0 |
| Peak | 47 | 4.25 | −2.3 |
| Peak | 120 | 3.59 | −3.7 |
| Peak | 156 | 2.85 | −6.8 |
| Peak | 210 | 1.91 | −5.0 |

**Sub Flatten: Max (−30)**. Highs −30 dB via stacked bands. Max EQ gain −1.7 dB.

| Type | Hz | Q | Gain |
|---|---|---|---|
| Low shelf | 17 | 0.71 | −15.0 |
| High shelf | 192 | 0.71 | −15.0 |
| Peak | 45 | 5.98 | −1.6 |
| Peak | 120 | 3.89 | −7.6 |
| Peak | 151 | 3.44 | −11.6 |
| Peak | 181 | 2.79 | −11.2 |
| Peak | 253 | 1.91 | −10.8 |
| Peak | 498 | 0.84 | −8.6 |
| Peak | 2132 | 0.30 | −13.3 |
| Peak | 16000 | 0.30 | −14.7 |

Fit accuracy: within ~1 dB across 35–20 kHz. Up to ~3 dB of extra cut at 25–30 Hz,
where the 17 Hz low shelf overshoots slightly, and ~3 dB at 80 Hz in the Max preset.
That's well inside the uncertainty of the cabin-gain assumption.

## Poweramp Equalizer format reference

- Parametric mode, 5–32 bands, per-band frequency/Q/gain, ±15 dB per band.
- JSON import/export via Presets → Import. The file is an **array** of presets, so one
  file can hold several.
- Band `type`: `0` = low shelf, `1` = high shelf, `2` = peaking. Confirmed from a
  real exported preset: Poweramp's default layout puts the low shelf first, then the
  high shelf, then the peaks.
- `channels: 0` = both channels. `preamp` stays at 0.0, since no preset boosts anything.

## How to use / tune in the car

1. Import `poweramp_presets/Subwoofer_Flatten_All.json` into Poweramp Equalizer and
   make sure **parametric** mode is on.
2. Start with **Mild**. Raise the head unit / Poweramp volume to bring the mains back
   to a comfortable level, then set sub level with the LC2i Pro bass knob.
3. The Strong and Max presets drop the overall output by 15 / 30 dB, so the phone or
   head unit volume will need to go up a lot. If you run out of volume with Max, step
   back to Strong.
4. **LC2i Pro AccuBASS** dynamically boosts bass that it thinks the head unit is rolling
   off. That counteracts this EQ, so keep AccuBASS off (or at minimum) while tuning.
5. Set the sub amp's low-pass around 80 Hz so the flattened 28–80 Hz band is what the sub plays.

## Next step to improve accuracy

Measure the real in-car response: REW or a phone RTA app playing pink noise or sweeps,
mic at the driver's head position, with the sub alone. Then replace `room` in
`eq_design.py` with the measured curve and re-run it. Everything above (target logic,
fitting, JSON export) stays the same.
