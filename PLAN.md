# Plan & status

_Last updated: 2026-10-15 (new size limits; side-firing layout v2)_

## Goal
An enclosure for the Pioneer TS-W304R in the 2005 Mk4 Jetta TDI trunk. It sits against the rear
seatback with the driver firing rearward. **Goal (since 2026-10-13): much louder low frequencies.**
Response shape is fixed with DSP (Poweramp Equalizer → LC2i Pro). Originally the goal was a flat sealed box.

## Decisions made
- **Keeping the TS-W304R and the GM-3500T** (2026-10-13). No new driver or amp; the goal is to use what's on hand.
  A DCS305-4 + 250–300 W amp was evaluated: +2–5 dB for ~CAD $350–500, vs +7–13 dB from the box alone for ~$70–130. Rejected as not worth the money (details in box-designs.md).
- **2026-10-13 change of direction: the goal is now max low-frequency output, not flatness.** Johann will shape the response with DSP.
  A bigger *sealed* box only adds ~3 dB of shape and **zero** max output (Xmax-limited), so it was rejected.
  **The new direction is ported: ~90 L net @ 27 Hz** (+12 dB clean output at 25–30 Hz vs the current box). Design in box-designs.md.
- _(Superseded, kept for history:)_ - **Sealed, not ported.** Qts 0.70 / EBP ≈ 39 means every ported alignment humps
  ≥ +3.4 dB, and Xmax is small. Ported only helps output near fb, and it needs a subsonic
  filter. See box-designs.md for the numbers.
- _(Superseded)_ Target ≈ 60–70 L net, keeping the 16"-tall seatback wedge** (10.6° slope). Beyond ~70 L
  there's little to gain.
- EQ is cut-only. Sub makeup gain comes from the LC2i Pro bass knob (see SUBWOOFER_EQ_NOTES.md).

## Layout constraints (Johann, 2026-10-15, from looking at the car; not yet tape-measured)
- **Height ≤ current box: 16"** outer.
- **Depth (seatback → trunk lid) ≤ 2× current: 27"** at the bottom (current is 13.5"). The 10.62° seatback slope is kept, so 24" at the top.
- **The box sits on the driver's side of the trunk; the driver fires sideways toward the passenger side.**
- Width (left-right) is the free dimension. Layout v2 is in box-designs.md.

## Hardware chain
Phone (Poweramp EQ) → Bluetooth (XY-BT-MINI BT 4.1 board, 3.5 mm out, 100 µF output caps → ~0.16 Hz HPF into a ~10 kΩ line input) → CD-changer-to-AUX adapter → **stock non-Monsoon head unit** (speaker-level out) → AudioControl LC2i Pro → **Pioneer GM-3500T, bridged @ 4 Ω (185 W RMS, LPF fixed at 80 Hz/12 dB, no subsonic)** → TS-W304R

## Status
- [x] Amp identified: GM-3500T. Specs in SPECS.md; bass-boost existence still unconfirmed
- [ ] Confirm whether the GM-3500T has bass boost (owner's manual), and set it to 0 dB if so
- [x] Driver T/S parameters collected
- [x] `subwoofer.skp` geometry fully extracted and **confirmed**: 36.96 L net (Qtc 1.234, Fc 50.4 Hz, +2.6 dB @ 62 Hz). See SPECS.md
- [x] Bigger-sealed vs ported comparison and excursion analysis done
- [x] Trunk dimensions: internet figures found (unverified). Bentley manual has none
- [x] Cut-only Poweramp EQ presets made (`poweramp_presets/`, `eq_design.py`). **Built on the 52.7 L rectangle reading**
- [x] Box-volume conflict resolved: 36.96 L wedge (the 52.7 L rectangle reading was wrong)
- [ ] _(Only if keeping the current box)_ Re-fit the EQ presets for the real 36.96 L box: `eq_design.py` needs wedge geometry (or a direct Vb override), then re-run. The hump is at ~62 Hz, not ~45–50
- [x] Built `box_compare.html` to compare all candidate boxes (2026-10-13)
- [ ] **Size: medium 17" wide (75.1 L, 14 in² × 27.6" port, ~31% of the trunk, within 0–2 dB of big). Johann wants to keep the current 17" width, and it's Claude's pick.** Alternatives: big (90.6 L, layout v2: 20.2" wide, ~37% of the trunk) vs compact (45 L, 10 in² port, layout v2: 11.7" wide, ~21%, −4–5 dB at 20–25 Hz)?** Johann reacted to the big one with "that's massive". Table in box-designs.md
- [x] **Tuning chosen: 22 Hz** (2026-10-13). Starting point: ~90.6 L net, 18 in² slot, ~29" port, subsonic ~18 Hz
- [ ] ⏸ **Don't design the final box yet.** Johann is getting trunk measurements first (his instruction, 2026-10-13)
- [ ] **Chain low-end test:** with EQ off and AccuBASS off, play 10/15/20/25/30/40/60 Hz tones and read AC volts at the LC2i RCA output (amp off). dB = 20·log10(V/V60). Checks whether the stock head unit rolls off the deep bass. (Bluetooth SBC/AAC and the XY-BT board do not cut lows.)
- [ ] **Check that layout v2 clears the driver-side wheel well:** the box is 27" deep, so where does the well start and end front-to-back, and how far does it stick in?
- [ ] Get the user's trunk measurements **+ the sub's surround height above the mounting ring** (for guard clearance) (list in SPECS.md → Trunk)
- [ ] Final **ported 22 Hz** box design + cut list (after measurements), **based on layout v2 (side-firing, 16" H × 27"/24" D)**. Earlier 27 Hz sketch, for reference: 32" W × 16" H × 18"/15" deep, slot port 1.75" × 14.5" × ~27" L-shaped, fb 27 Hz, ~90.6 L net (see box-designs.md). _Old sealed starting point, now superseded:_ 30" W × 16" H, **same 13.5"/10.5" deep wedge as the current box** (only the width changes), ¾" MDF, one cross-brace, ≈ 69.1 L net (28.5 × 14.5 × 10.487 = 71.0 L gross − 1.66 driver − 0.3 brace); Qtc 1.02, Fc 41.7, F3 32.6 (2.49 L net per inch of outer width at the current wedge cross-section)
- [ ] **REW test matrix** (mic at the driver's head): rear seats up vs folded · pass-through closed vs open (if fitted) · sub rear-firing vs up-firing vs firing at the seatback. Johann reports that low bass drops a lot with the seats up. Likely cause: trunk pressure escaping out the body vents instead of reaching the cabin through the seatback
- [ ] Future project (Johann): deadening under the carpet and in the doors, plus new door seals. Expect the same or slightly more deep bass (a tighter cabin gives more pressure gain below ~30 Hz) and far fewer rattles. **Re-measure in REW and re-fit the EQ afterwards**, or do the deadening before the final measurement
- [ ] Measure the in-car response (REW / RTA) and replace the assumed cabin gain in `eq_design.py`
- [ ] Re-fit the EQ presets to the final box + measurement. **For the ported box: the subsonic filter at ~23 Hz (≥ 24 dB/oct) is mandatory**, because the amp has none. Stack Poweramp low shelves, or use the LC2i Pro if it has one
- [ ] After building: measure fb (impedance dip or port-output peak) and trim the port to hit ~27 Hz

## Amp question (2026-10-13)
In the 22 Hz box, the GM-3500T's 185 W is **not** the bottleneck. Power to reach Xmax: 20 Hz 141 W · 22 Hz 541 W · 25 Hz 193 W ·
28 Hz 90 W · 30 Hz 68 W · 35–40 Hz 49 W · 50 Hz 81 W · 60 Hz 162 W. More power only adds output in a narrow band around 22 Hz
(+2.1 dB @ 300 W, +4.6 dB @ 600 W); everywhere else the result is unchanged (Xmax-limited). The only good upgrade reasons:
a built-in adjustable subsonic filter (the GM-3500T has none), class-D efficiency, or a future bigger or second sub.

## Design requirements (from Johann)
- **Removable guard** over the front face (2026-10-13), because cargo sometimes sits against the box. Plan: a ~1.5"-deep frame (MDF or pine
  offcuts) with perforated/expanded steel (≥ 50% open, 16–20 ga), a centre cross-bar, held on by 4–6 neodymium magnets (~10+ lb each),
  with the mesh glued in and foam tape at contact points (rattles at 22 Hz). **It must cover the port too**, or the port must exit where cargo can't
  block it. Openings in front of the port should total well over the port area (18 in²). Adds ~1.5" to overall depth. ≈ $30–50.
  Depth check: surround height (assumed ~0.75", **measure it**) + ~2× Xmax on peaks (~0.4") ≈ 1.15" minimum clearance.

- **Material: ¾" MDF** (2026-10-14, Johann). Over Baltic birch for cost and easy, clean cutting. Seal it against moisture (carpet/paint/primer; bottom panel especially). Use T-nuts for the driver and pre-drill pilot holes, since MDF strips. Avoid construction plywood (voids, so air leaks).
- **3D printing (2026-10-14):** printing the whole box was rejected: ~15 kg PETG/ASA even with 6 mm ribbed walls, 600–1,000 h of printing,
  15–25 glued sections (leak risk at 22 Hz), wall flex, and PLA softens at ~55–60 °C in a hot trunk. **Plan: an MDF box with printed parts:**
  port U-bends and flared ends, the guard frame (with magnet pockets), wheel-well fit spacers (outside the box), a driver ring/gasket, and a terminal-cup adapter.
  Need to ask: Johann's printer model and bed size. A fully trunk-shaped box would be fibreglass, not a print.

## Build budget (2026-10-13, rough CAD estimates, not quotes)
Already on hand: wood screws, wood glue, construction adhesive, speaker wire, spray adhesive,
the terminal cup and driver screws from the old box.
To buy: one 4×8 sheet of ¾" MDF (~$60–80; ~3,170 in² needed of 4,608), plus optionally carpet
(~$25–40) and foam gasket tape (~$8–12). **Total ≈ $60–80 bare, ≈ $95–130 carpeted.**

## Options still on the table
- **Keep the 37 L box + DSP:** a Linkwitz transform from (50.4 Hz, Q 1.23) to (~35 Hz, Q 0.707) needs ~+6 dB at 35 Hz. That conflicts with the cut-only strategy and with the ~40 W excursion limit. Needs a subsonic HPF at ~25 Hz.
- **Ported 70–80 L @ 25–28 Hz:** only if more output at 25–40 Hz matters more than flatness. Needs a ~16 in² × ~17" port, a −4 dB PEQ on the hump, and a 24 Hz subsonic filter.
