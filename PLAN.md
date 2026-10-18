# Plan & status

_Last updated: 2026-10-18 (2026-10-18: single ported preset `Subwoofer_Ported22.json`, box-only, flat above 100 Hz, 24 dB/oct subsonic @ 21 Hz; build starting: one 4×8 sheet of ¾" MDF covers the whole cut list; terminal cup moved to the back panel, see box-designs.md → FINAL size)_

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

## ✗ Dropped: layout v5, a box that slides straight out through the pass-through (2026-10-15, dropped 2026-10-16)
- **Dropped (Johann, 2026-10-16):** going with the 34" × 15.5" box. The fix for the removal problem is operational: **keep the trunk floor behind the box clear** so it can always be turned and pulled out through the seats. Johann now keeps only a minimal tool kit in the trunk. The pass-through measurements below are no longer needed.
- Removal check (from the dummy test): the 34 × 18" footprint needs its 38.5" diagonal to turn, so the floor behind the box has to be empty, which is now the standing rule. The key cylinder + pull cord plan (Status) still covers a dead lid release.
- **Why:** the 34" box has to be turned inside the trunk to come out, which needs clear floor behind it. Johann has had a broken latch before and **had to unscrew it from inside the trunk**, so a pull cord isn't enough: he needs to be able to empty the front of the trunk from the cabin quickly.
- **Concept:** the long axis runs fore-aft, the cross-section fits the rear-seat pass-through, and it pulls straight back onto the folded seat with no rotation. A strap or handle on the seat end, and felt/UHMW skids on the bottom.
- **Measurements Johann will bring (2026-10-16):** pass-through width × height (narrowest clear opening, seat folded) and which side it's on; the height of its bottom edge above the trunk floor; trunk depth from the seatback face to the rear wall at the floor and at the box's height (rear slope); the width available beside the pass-through; floor flatness along that path; and room in the cabin to land the box. Then do a new cardboard mock-up.

## ✅ FINAL size, building this one (cardboard dummy 2026-10-15, confirmed 2026-10-16)
- **34" W × 15.5" H × 18"/10.73" D, net 82.1 L, 16 in² × 28.8" floor slot, fb 22 Hz.** Cut list in box-designs.md → FINAL size. Files: `cad/box_v4_34x15.5in.{dxf,FCStd,step}`.
- Why: the 34" dummy wouldn't pass the trunk lid. It went in through the rear seats and turned flat in the trunk, but at 16" tall it barely cleared the pass-through (with cardboard flex). MDF won't flex, so −½".
- 15.5" is also the lowest height that works without redesign: the driver cutout clears the shelf and top by 0.18" each.

## Layout v4 (measured, 2026-10-15, latest)
- **Measured:** 39.5" between the wheel wells (forum said 38⅛"). **Profile (clarified): the current box's 10.5" top can stay, with the bottom stretched to 18"** (the body panel is curved). Straight back = 25.1°.
- Same placement as v3 (against the seatback, front-firing, 16" H, 22 Hz), but deeper. **Claude's pick (revised): as wide as fits, target 38.5" W × 16" H × 18"/10.5" D, 96.8 L, 18 in² × 27.3" straight floor slot.** Johann's point: the side gaps beside a 34" box are dead space, so the extra +1.1 dB at 22 Hz (+0.7 at 25) costs no usable trunk. Width = min(well gap − ~1", lid opening − ~½"). If the lid opening or the well gap comes in tight, drop to 36" (91.2 L). Details in box-designs.md → Layout v4.
- Johann's 75 L choice predates these measurements; at 18"/10.5" it would be 30.8" wide with only ~2" of port end clearance. **Leaning max width (Johann + Claude); the measurements below set the final number.**

## Layout v3 (Johann, 2026-10-15, later; superseded by v4)
- The box goes **at the back of the trunk, against the seatback, very wide and shallow**, along the seatback. **75 L net @ 22 Hz kept** (14 in² × ~27.6" port, straight, no bends).
- Height 16" and the seatback wedge (10.62°) kept. Front-firing toward the trunk lid. Proposed **36" W × 16" H × 13.8"/10.8" D** (see box-designs.md → Layout v3).
- Critical measurement: **width between the wheel wells at the seatback** (38⅛" is an unverified forum figure).

## Layout constraints v2 (Johann, 2026-10-15; superseded by v3 above)
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
- [x] **Size settled: 75 L net @ 22 Hz** (Johann, 2026-10-15), built as layout v3 (36" wide along the seatback) Alternatives: big (90.6 L, layout v2: 20.2" wide, ~37% of the trunk) vs compact (45 L, 10 in² port, layout v2: 11.7" wide, ~21%, −4–5 dB at 20–25 Hz)?** Johann reacted to the big one with "that's massive". Table in box-designs.md
- [x] **Tuning chosen: 22 Hz** (2026-10-13). Starting point: ~90.6 L net, 18 in² slot, ~29" port, subsonic ~18 Hz
- [x] ~~Don't design the final box yet~~ The main trunk measurements are in (2026-10-15). Only the lid opening and the well-gap location remain
- [ ] **Chain low-end test:** with EQ off and AccuBASS off, play 10/15/20/25/30/40/60 Hz tones and read AC volts at the LC2i RCA output (amp off). dB = 20·log10(V/V60). Checks whether the stock head unit rolls off the deep bass. (Bluetooth SBC/AAC and the XY-BT board do not cut lows.)
- [ ] _(Partly answered: steeper than 10.62°, see Seatback angle above)_ **Re-measure the seatback wedge** (Johann will provide): seatback horizontal depth at the floor vs 16" up (gives the angle), whether it's flat or curved, and any latches or hinges in the way. All v2 designs currently use the 10.62° (3" over 16") slope from subwoofer.skp. Each +1" of lean costs ~0.5" of average depth (~2% Vb)
- [x] **Wheel-well width measured: 39.5"** (Johann, 2026-10-15). Floor depth allowed: 18"
- [x] **Seatback profile:** current box with the bottom stretched to 18" (top 10.5") fits; the panel is curved → 25.1° straight back (Johann, 2026-10-15)
- [x] **Curve check:** the panel curves away from the box (concave), so the flat 25.1° back clears it (Johann, 2026-10-15). Flat back kept; a two-facet back would gain ~+0.2 dB, not worth it
- [x] ~~Was the 39.5" measured at the floor or right at the seatback?~~ Moot: the 34" dummy fit and turned between the wells. Measure the well gap at ~1", 8" and 15" up, at the seatback
- [x] ~~Lid-hinge clearance~~ Not gooseneck: struts + conventional hinge (Johann, 2026-10-15). Not a width limit
- [x] **Install route check (done with the dummy, 2026-10-15):** the lid is too narrow for 34"; the box goes in through the rear seats and turns flat in the trunk. Original note: Johann's fallback is to pass the box through the folded rear seats and rotate it in the trunk. **Rotating it flat in the trunk can't work:** a 38.5 × 18" footprint needs 42.5" of room in *both* directions partway through the turn (at 25°: 38.5·cos25 + 18·sin25 = 42.5" wide, 38.5·sin25 + 18·cos25 = 32.6" deep; mirrored at 65°), and the trunk is 36" deep (forum). The seat route works only if the box can keep its tail in the pass-through while it turns, so it depends on the pass-through width. A better fallback goes through the lid: lower one end under the side lip (the trunk is wider behind the wells than the opening), drop the other end, slide it forward. Best test: a cardboard or 2×2 dummy at 38.5 × 16 × 18 (back slope optional) tried both ways.
- [x] **Trunk-lid opening width:** < 34" (the dummy didn't fit). Moot now that the box goes through the seats. Original note: No forum figure exists; the largest proven fit is the MTX JETTA10 at 35¾". So ≤ ~35" is safe blind; 36–38.5" needs this measurement (or a 38.5" stick test). A 38.5" box must pass through flat; it can't be rotated inside, since its 42.5" plan diagonal is longer than the 39.5" between the wells. The MTX JETTA10 at 35¾" is known to fit
- [x] **Size: FINAL 34" W × 15.5" H, 82.1 L** (cardboard dummy, 2026-10-15). ~~v4 size: max width (~38.5", ~97 L)~~, final number = min(well gap − ~1", lid opening − ~½") once the two measurements above are in
- [ ] Get the user's trunk measurements **+ the sub's surround height above the mounting ring** (for guard clearance) (list in SPECS.md → Trunk)
- [x] **CAD + cut list: FINAL `cad/box_v4_34x15.5in.*`** (2026-10-15). First drafted at 38.5": `box_cad.py` → `cad/box_v4_38.5in.dxf` (cut sheet, mm), `.FCStd`, `.step`. Net 97.6 L, 18 in² × 27.1" slot. Re-run with the final width after the cardboard dummy test
- [ ] Final **ported 22 Hz** box design + cut list (after measurements), **based on **layout v4 (~38.5" W × 16" H × 18"/10.5" D, 25.1° back, front-firing, 18 in² straight floor slot)**. Earlier 27 Hz sketch, for reference: 32" W × 16" H × 18"/15" deep, slot port 1.75" × 14.5" × ~27" L-shaped, fb 27 Hz, ~90.6 L net (see box-designs.md). _Old sealed starting point, now superseded:_ 30" W × 16" H, **same 13.5"/10.5" deep wedge as the current box** (only the width changes), ¾" MDF, one cross-brace, ≈ 69.1 L net (28.5 × 14.5 × 10.487 = 71.0 L gross − 1.66 driver − 0.3 brace); Qtc 1.02, Fc 41.7, F3 32.6 (2.49 L net per inch of outer width at the current wedge cross-section)
- [ ] **Trunk access with the box installed** (Johann's concern, 2026-10-15: the box blocks crawling in from the rear seats if the lid won't open):
  1. **Exercise the key cylinder now** (behind the VW emblem; mechanical, works with a dead battery or a broken lid harness). Lube it with graphite/lock lube if stiff. Keep the physical key blade on you
  2. **Add an emergency pull cord** from the latch (the glow T-handle if present, or the lock's release lever) along the trunk side, through the ~2.75" gap between the box end and the wheel well, ending in a loop at the top of the box by the pass-through. It needs a slack loop for lid travel. Test it with the box installed and the trunk loaded
  3. That covers: dead battery / broken lid harness / dead release motor (key) and seized or unlinked key path (cord). Only a jammed latch itself is left, and that's a shop job either way
- [ ] **REW test matrix** (mic at the driver's head): rear seats up vs folded · pass-through closed vs open (if fitted) · sub rear-firing vs up-firing vs firing at the seatback. Johann reports that low bass drops a lot with the seats up. Likely cause: trunk pressure escaping out the body vents instead of reaching the cabin through the seatback
- [ ] Future project (Johann): deadening under the carpet and in the doors, plus new door seals. Expect the same or slightly more deep bass (a tighter cabin gives more pressure gain below ~30 Hz) and far fewer rattles. **Re-measure in REW and re-fit the EQ afterwards**, or do the deadening before the final measurement
- [ ] Measure the in-car response (REW / RTA) and replace the assumed cabin gain in `eq_design.py`
- [x] **EQ preset for the ported FINAL box** (revised 2026-10-18, Johann: one profile, nothing above 100 Hz, no cabin gain): `poweramp_presets/Subwoofer_Ported22.json`, modelled box-only. Subsonic 24 dB/oct @ 21 Hz, kept under Xmax. See SUBWOOFER_EQ_NOTES.md
- [ ] Re-fit the EQ presets to the final box + measurement. **For the ported box: the subsonic filter at ~23 Hz (≥ 24 dB/oct) is mandatory**, because the amp has none. Stack Poweramp low shelves, or use the LC2i Pro if it has one
- [ ] **Port chuffing (Johann, 2026-10-17): audible, tolerable in the trunk.** Model port speed at 27 V: 14.4 m/s @ 20 Hz, 12.3 @ 22, 10.1 @ 25 (17.1 @ 18, but the subsonic cuts that). Square mouth + sharp 90° bend chuffs from ~10–12 m/s, so it's likely the edges. Check first: 20 Hz vs 40 Hz tone. Noise only at 20 = velocity; hiss at both = air leak (shelf joints, terminal cup). Fixes: 1/2" roundover on the outside mouth edges, roundover on the inner bend edge (x = 9 7/8"), 45° fillet block in the outer bend corner, roundover on the open end (x = 28 13/16"). Silicone the shelf joints if it's a leak
- [ ] After building: measure fb (impedance dip or port-output peak) and trim the port to hit ~22 Hz

## Amp question (2026-10-13)
In the 22 Hz box, the GM-3500T's 185 W is **not** the bottleneck. Power to reach Xmax: 20 Hz 141 W · 22 Hz 541 W · 25 Hz 193 W ·
28 Hz 90 W · 30 Hz 68 W · 35–40 Hz 49 W · 50 Hz 81 W · 60 Hz 162 W. More power only adds output in a narrow band around 22 Hz
(+2.1 dB @ 300 W, +4.6 dB @ 600 W); everywhere else the result is unchanged (Xmax-limited). The only good upgrade reasons:
a built-in adjustable subsonic filter (the GM-3500T has none), class-D efficiency, or a future bigger or second sub.

## Design requirements (from Johann)
- ~~**Removable guard** over the front face (2026-10-13)~~ **Dropped (2026-10-15):** Johann will buy a **generic 12" sub grille** (Amazon) instead. Check that it gives ≥ ~1.15" of clearance from the mounting ring to the inside of the mesh (use spacers if not). The **port mouth is not covered**: keep cargo ~2"+ away, or add a cheap perforated strip/dowels over it. A top-firing port was ruled out (only ~2.5–6" to the parcel shelf). Original guard plan:, because cargo sometimes sits against the box. Plan: a ~1.5"-deep frame (MDF or pine
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
