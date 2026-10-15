# Specs & reference data

Facts about the car, the electronics, the driver and the existing box, plus the core formulas. Candidate box designs are in [box-designs.md](box-designs.md). Status and next steps
live in [PLAN.md](PLAN.md); the EQ preset work lives in
[SUBWOOFER_EQ_NOTES.md](SUBWOOFER_EQ_NOTES.md).

## Car

- **2005 VW Jetta TDI sedan, Mk4 (A4).** Check the build date: a "2005.5" Jetta is a Mk5,
  which has a different and larger trunk.
- Signal chain: head unit / phone (Poweramp Equalizer) → AudioControl LC2i Pro → sub amp → sub.
- The user has done DSP and sound-deadening work on this car before.

### Trunk (Mk4 Jetta sedan)

**Measured limits (Johann, 2026-10-15, later):** 39.5" between the wheel wells, current box profile stretched to 18" at the floor / 10.5" at the top (25.1° straight back), height 16" (see table). Layout v4 in box-designs.md.

**Earlier box-space limits from Johann (2026-10-15, by eye; v2, superseded by layout v3: wide along the seatback, see PLAN.md):** max height 16" (= the current box), max depth seatback→lid 27" (= 2× the current 13.5").
The box goes on the driver's side, with the driver firing toward the passenger side.


| Item | Value | Source / confidence |
|---|---|---|
| Trunk volume | 13 ft³ (0.4 m³ ≈ 368 L) | Bentley manual p. 00-7 and spec tables. Confirmed |
| Width between wheel wells | **39.5"** | **Johann's tape measurement, 2026-10-15. Wins over the forum figure.** Exact height/position not yet stated (floor? right at the seatback?) |
| Width between wheel wells (forum, superseded) | 38⅛" | VWVortex, via search snippet only. Unverified. 1⅜" narrower than measured, likely a different measuring point or carpet; kept for history |
| Box depth allowed at the floor (seatback → front face) | **18"** | Johann, 2026-10-15 (current box is 13.5") |
| Seatback profile | **The current box could keep its 10.5" top (at 16") and grow to 18" at the floor and still fit.** The seat/body panel it rests against is **curved**, so there's extra room low down. Straight-back chord: atan((18 − 10.5)/16) = **25.1°** | Johann, 2026-10-15 (clarified). Wins over the earlier "steeper than 10.62°, angle unknown" (the 20° placeholder in v4 is superseded). **The curve is concave: its middle is the farthest point from the box** (Johann, 2026-10-15), so a flat back (the straight chord, 14.25" deep at 8" up) clears it everywhere |
| Height | 18½"–22⅛" | VWVortex snippet. Unverified |
| Depth (seatback → lip) | 36" at floor / 27" at top | VWVortex snippet. Unverified |
| Known-fit commercial box | MTX JETTA10: 21" H × 35¾" W × 11⅜" D | MTX product listing via search snippet |

- The Bentley manual (`Bentley VW MKIV Manual - Complete.pdf`, 1,984 pp) has **no** interior
  trunk dimensions. It was searched in full; don't search it again for this.
- **Still need the user's tape measurements:**
  1. ~~Width between the wheel wells~~ 39.5" (done). Still need: is that at the floor or right at the seatback, and is it the same at 16" up?
  2. Height from the floor to the underside of the rear shelf, at the seatback.
  3. Depth from the seatback to the lip, at the floor and at ~16" up (gives the seatback angle). **Most important one now:** angle = atan((depth at floor − depth at 16")/16).
  4. Trunk lid opening: narrowest width and tallest clear height.
  5. Obstructions: jack/tool kit, seat-release latches, carpet humps.

## LOC: AudioControl LC2i Pro

- Rated **20 Hz – 50 kHz ±1 dB** (AudioControl product page). This is a spec limit, not a cutoff: a gentle capacitor rolloff.
- If that's a 1st-order rolloff, −3 dB lands at ≈ 10 Hz (−1.2 dB @ 18 Hz). If 2nd order, ≈ 14 Hz (−1.5 dB @ 18 Hz). Negligible above the 18 Hz subsonic.
- Forum anecdote (DIYMA, "cancels out 20 Hz" while 10 Hz is fine) is most likely a cabin/polarity null, not the unit.
- Unverified on this unit. The chain voltage test in PLAN.md (add 10 Hz) confirms it.
- The original LC2i (non-Pro) has a different, disputed spec (33 Hz vs 10 Hz lower limit across sources).

## Amplifier: Pioneer GM-3500T (2-ch Class AB, bridgeable)

From retailer listings (Crutchfield and others), not yet checked against the manual:

| Item | Value |
|---|---|
| RMS, 14.4 V | 60 W × 2 @ 4 Ω · 85 W × 2 @ 2 Ω · **185 W × 1 bridged @ 4 Ω** |
| LPF | Switchable on/off, **fixed 80 Hz, 12 dB/oct** |
| Subsonic filter | None listed |
| Bass boost | **Conflicting**: Crutchfield says none; Soundmaster says 0/6/12 dB. Check the owner's manual |

- The sub (4 Ω SVC) runs **bridged**. 185 W is well under the sub's 300 W RMS thermal rating, so the voice coil isn't at risk.
- Excursion matters more. Cone displacement scales as x ∝ √P. In the 69 L sealed box, Xmax (4.7 mm)
  is reached at ~38 W below ~40 Hz, so a full 185 W would push the cone to ≈ 10.4 mm, about 2.2× Xmax.
  Set the gain by ear/clipping and keep the subsonic cut in the EQ, since the amp has no subsonic filter.
- If the amp has bass boost, keep it at 0 dB. It would fight the cut-only EQ.

## Driver: Pioneer TS-W304R (12", 4 Ω SVC, discontinued)

Source: <https://loudspeakerdatabase.com/Pioneer/TS-W304R>, cross-checked against speakerboxlite.

| Param | Value | Param | Value |
|---|---|---|---|
| Fs | 28.6 Hz | Re | 3.0 Ω |
| Qts | 0.70 | Le | 2.39 mH (2.43 in one source) |
| Qes | 0.74 | Bl | 10.4 T·m |
| Qms | 13.3 | Mms | 150 g |
| Vas | 77.9 L | Cms | 0.207 mm/N |
| Sd | 520 cm² | SPL | 86.5 dB (85.8 measured; Pioneer's "95 dB" is marketing) |
| Xmax | 4.7 mm (one source says ~5) | Power | 300 W RMS / 600 W program |
| Vd | 244 cm³ | EBP (Fs/Qes) | ≈ 39, which points to sealed |
| Baffle cutout | 283 mm (11.14") | Mounting depth | 135 mm (5.31") |
| Driver displacement | ≈ 1.66 L | | |

## Existing box (from `subwoofer.skp`, SketchUp 2026 v26.2.0)

**How it was extracted:** a `.skp` file is a ZIP container after a short header. Unzip it;
the geometry is in `model.dat`. The vertex table is a run of float64 (x, y, z) triples, in inches,
with a 50-byte stride starting near byte offset 275,858. Read those directly; don't filter for
"clean" fractions, because the sloped inner faces land off-grid. Face normals follow after
~285,000 (the back normal is (0, 0.9829, −0.1843)). Thumbnails (`meta/*.png`) are only 256 px.
The model also contains SketchUp's "Ty" scale figure.

**Confirmed 2026-10-13 from the full vertex table.** Johann drew the model to the real
dimensions, with true wood thickness, a hollow interior and the correct back angle.

Coordinates: x = width, y = depth (front baffle at y = 0, going negative toward the seatback), z = height.

| | Value |
|---|---|
| Outer width × height | 17.000" × 16.000" |
| Outer depth | 13.500" at the bottom, 10.500" at the top |
| Back angle | 10.62° from vertical (normal (0, 0.9829, −0.1843) = atan(3/16)), leaning toward the front at the top |
| Panel thickness | 0.750" everywhere. The back is 0.750" measured perpendicular to the slope (0.763" horizontally) |
| Inner cavity | x 0.75→16.25 (15.5"), z 0.75→15.25 (14.5"), y −0.75 → back |
| Inner depth | 11.846" at the bottom (z = 0.75) / 9.128" at the top (z = 15.25), average 10.487" |
| Driver circle | Ø 12.5" (r = 6.25, a 24-segment polygon), centred at (8.5, 8.0) on the front face. That's the driver's outer frame (spec ≈ 12.4"). **No separate cutout circle is drawn**; the real cutout is 283 mm (11.14") |
| Bracing | None |
| Gross internal | **38.62 L** |
| Wood volume | 14.86 L |
| Outer volume (trunk space used) | 53.49 L |
| **Net Vb** | **36.96 L** (minus 1.66 L driver) |
| Alignment | Qtc 1.234, Fc 50.4 Hz, F3 36.8 Hz, peak +2.60 dB @ 62 Hz |
| Magnet clearance | Mounting depth 5.31" + 0.75" baffle → ~5.2" to the back at the driver centre. OK |

> **Resolved conflict:** an earlier session (`eq_design.py`, SUBWOOFER_EQ_NOTES.md) read the box
> as a 17 × 16.25 × 16" rectangle (52.7 L net, Qtc 1.10, Fc 45 Hz). That was wrong. No vertex
> sits at a depth of 16.25; 16.25 is the inner side-panel x-coordinate. Its "11.125 = cutout" and
> "5.375 = mounting depth" matches were also coincidences: both are coordinates of vertices on the
> 12.5" circle polygon. **The EQ presets were fitted to the wrong box and need re-fitting for 36.96 L.**

## Sealed-box formulas

- α = Vas/Vb; Qtc = Qts·√(1+α); Fc = Fs·√(1+α)
- F3 = Fc·√(a + √(a²+1)), where a = 1/(2Qtc²) − 1
- Peak (Qtc > 0.707) = Qtc²/√(Qtc² − ¼); f_peak = Fc/√(1 − 1/(2Qtc²))
- Response: |H| = r²/√((1−r²)² + (r/Qtc)²), where r = f/Fc
- Net Vb = gross internal − driver (1.66 L) − bracing
- Qtc can never go below Qts = 0.70, even in an infinite box, so this driver can't reach a true Butterworth (0.707)

> Box designs, modelled results and the sealed/ported comparisons moved to [box-designs.md](box-designs.md) (2026-10-13).

## Excursion-limited power (cone reaches Xmax 4.7 mm, 4 Ω nominal)

| Hz | Sealed 69 L | Ported 69 L @ 30 Hz |
|---|---|---|
| 20 | 39 W | 15 W |
| 25 | 36 W | 90 W |
| 30 | 35 W | 941 W |
| 35 | 36 W | 216 W |
| 40 | 42 W | 94 W |
| 50 | 75 W | 80 W |

In the low bass, the sub runs out of **linear** cone travel at about 40 W in a sealed box,
far below its 300 W thermal rating. "Takes abuse" is true thermally but not for excursion.
A ported box would raise headroom near fb, but it needs a subsonic filter (~24 Hz) because
the cone is unloaded below tuning.

## Cabin gain

Not measured. The working assumption is roughly +9 to +12 dB/oct below ~45–55 Hz, capped
around +14 dB. Replace it with a real RTA/REW measurement (mic at the driver's head, sub only).
