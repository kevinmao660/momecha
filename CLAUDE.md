# momecha — notes for Claude

## Goal
Web-first top-down pixel mech game. Milestone 1 is single player (learn the game, one fun district, real combat). Later: authoritative-server multiplayer split into district zones, then a desktop/Steam build by wrapping the web client (Electron or Tauri).

## Planned stack
- Client: TypeScript + Phaser 3 + Vite. Maps may move to Tiled.
- Art pipeline stays in Python (`art/`): mechs are 3D models built from parts and rendered to pixel sprites. Don't hand-draw mech frames; change poses/parts and re-render.
- Multiplayer later: server owns game state, clients send inputs only. Design game logic so it can run server-side (keep simulation separate from rendering).

## Design rules (from the owner's feedback)
- All designs are original. Armored Core is a structural reference only: never copy specific AC parts, names, emblems or art.
- Mechs are slim and upright, not blocky or "transformer"-like; thinner at the waist and joints. Torsos stay straight, not hunched.
- Heads are sharp and hawk-like, not boxy. Sensor eyes are a single slit, not "angry eyes".
- Both knees bend the same way (`matchKnees`); a mismatched leg reads as broken.
- Heron (`specs/ac_heron.json`, reverse-joint legs, raptor head) is the hero mech and its study stance is the approved look.
- Mechs never walk. They hover-skate on thrusters or fly, fast, with inertia.
- Animation: the torso leads and the legs follow. Legs hold still in flight (no flutter). Standing uses the angled 3/4 study stance with staggered feet, never a stiff straight front-on pose.

## Scale and look
- About 4.6 px per metre: Heron is 46 px (10 m), a storey is 15 px, a car is about 22 px, a lamp about 28 px, a four-lane road 64 px. Tiles are 16 px.
- Native view 1024 x 576, drawn with pixelated scaling.
- Night palette: teal ambient light map multiplied over the scene; only lamps, fires, lit windows and thrusters add light (warm orange, cold blue), in stepped bands.
- Diorama feel: y-sorted objects, outlined sprites, parallax fog and foreground girders.

## Prototype internals (`prototype/index.html`)
- Seeded procedural city (120 x 90 tiles); buildings sized so a roof never overhangs a road.
- Sprite sheet: 88 px frames, ground line at y=78. Rows are directions (0 down, 1 down-right, 2 right, 3 up-right, 4 up, 5 up-left, 6 left, 7 down-left); columns are poses: 0-3 idle, 4 + torsoLevel*3 + legLevel for movement, 12/13 flight, 14/15 brake.
- `H.ln` (torso lean) eases fast, `H.lg` (leg sweep) eases slowly; a hard turn resets the legs partway.
- Movement: ~250 px/s boost, x1.25 in flight, Shift quick boost to 560 px/s; motion is sub-stepped so it can't tunnel through props. Flying (z > 14) ignores low blockers (cars, lamps, rubble) but not buildings.
- Headless testing: `requestAnimationFrame` doesn't advance under Chrome's `--virtual-time-budget`; shim it with `setTimeout` in a test copy.
