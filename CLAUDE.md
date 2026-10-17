# Subwoofer project: Mk4 Jetta / Pioneer TS-W304R

Designing a **ported (22 Hz)** sub box for a 2005 VW Jetta TDI (Mk4) trunk, plus cut-only EQ
presets for the in-car response. (It started out as a sealed design; see PLAN.md for why that changed.)

## Read first
- [PLAN.md](PLAN.md): goal, decisions, current status, open items
- [SPECS.md](SPECS.md): car/trunk, LOC, amp, driver T/S, existing box geometry, formulas, cabin gain
- [box-designs.md](box-designs.md): every candidate box (sealed/ported, 22/24/27 Hz, big vs compact), with modelled results and trunk usage
- [SUBWOOFER_EQ_NOTES.md](SUBWOOFER_EQ_NOTES.md): Poweramp Equalizer preset design (`eq_design.py`, `poweramp_presets/`)

## Files
- `subwoofer.skp`: the user's SketchUp 2026 model of the existing box. It's a ZIP after a header; the geometry is float64 inches in `model.dat` (see SPECS.md for the extraction method)
- `Bentley VW MKIV Manual - Complete.pdf`: 1,984 pp, already searched. It has no trunk interior dimensions. **Proprietary: git-ignored, never commit it**
- `max_spl.py`: max clean SPL (Xmax / 185 W-limited) for sealed vs vented boxes; import `max_spl()` for comparisons
- `box_compare.html`: interactive comparison page (max SPL, 1 W response, excursion @ 185 W, port speed, port length). It's the same model as `max_spl.py` ported to JS; keep the two in sync. Add new candidate boxes to `DEFAULTS` in it
- `box_cad.py`: parametric v4 box (width as the argument): net volume, port length, DXF cut sheet in `cad/`; run under `freecadcmd` for the .FCStd/.step 3D model
- `box_drawing.py`: dimensioned 3rd-angle orthographic + parts sheet (`cad/box_v4_34x15.5in_{ortho,parts}.{png,pdf}`), geometry pulled from `box_cad.py`; re-run after changing it
- `eq_design.py`: models box + cabin and fits cut-only biquads, then exports the Poweramp JSON

## Keeping docs current (do this every session)
- When a measurement, decision or result changes, update **SPECS.md** (facts/numbers), **box-designs.md** (any box design or modelled result) and
  **PLAN.md** (status checklist + "Last updated" date) in the same turn. Update
  SUBWOOFER_EQ_NOTES.md when the EQ work changes.
- Mark the source and confidence of anything not measured by the user (e.g. "unverified, forum snippet").
- When values conflict, record both and explain which one wins and why. Don't silently overwrite.

## Git
- Git repo on `main`, remote `origin` = `git@github.com:Yofuness/subwoofer.git`. Push after committing. Commit doc/model changes as you go. `.gitignore` excludes all PDFs (the Bentley manual is proprietary).

## Working with the user
- Technically minded. Show the math and the mechanism behind every recommendation.
- Likes some sass and the occasional roast.
- Has prior DSP and sound-deadening experience on this car.
