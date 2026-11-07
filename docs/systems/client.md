# Client, Gamepad & Tech

## System requirements

| Component | Minimum | Recommended |
|---|---|---|
| CPU | 4 cores @ 3.0 GHz | 8 P-cores, 5.2 GHz boost (Intel Core Ultra 200 / Ryzen 9000) |
| RAM | 8 GB | 16 GB |
| GPU | GTX 10-series / AMD RDNA 1, 4 GB VRAM | DX12, 8 GB VRAM (RTX 40 / RX 7000 / Arc B-series) |
| Storage | **SSD required, 128 GB free** (HDDs unsupported) | — |
| OS | Windows 10 64-bit / macOS | — |

!!! warning "Partly unverified"
    PC Games Hardware presents the CPU, GPU and RAM rows as Blizzard's. Another FAQ says only the **128 GB SSD** figure is official. Treat the CPU and GPU rows as unverified.

- **Download:** about **52.9 GB** fresh, or about 13 GB if retail or Classic is already installed.
- **Drivers:** NVIDIA Game Ready **621.14** WHQL includes Forever optimizations. **Ray-traced shadows were missing at launch**, and Blizzard plans to restore them. AMD Anti-Lag 2 has no in-game option.
- **Graphics:** new lighting with global illumination, volumetric fog and god rays, a new water renderer, and real-time sun shadows. The lighting was hand-tuned per zone; Hazzikostas gave Duskwood at night with torchlit patrols as an example.
- Some Windows 11 machines were wrongly refused installation as "below minimum" by Battle.net.

## Gamepad (beta feature)

- Supports **all XInput controllers**, with Xbox or PlayStation glyphs. Enable it under *Options → Gameplay → Gamepad*.
- **Movement:** the left stick moves and the right stick turns the camera. Zoom with LB+RB plus the right stick.
- **Targeting:** **LB** targets friendly, **RB** targets hostile.
- **Face buttons:** X interacts, A jumps, B goes back, Y inspects.
- **Action bars:** 4 bars on screen, swapped by holding LT, RT or both. **Up to 84 ability slots** across 3 bar sets.
- **Shortcuts:** LB+RB plus a face button or the D-pad opens the bags, quest tracker, chat and buffs.
- Faction-colored controller lights on supported pads.
- You can end a flight early and dismount at the next flight point.
- **Chat still needs a keyboard.** Keyboard-free play is a long-term goal.
- Paul Kubit framed controller support as an accessibility feature.
- **Known issues:** the Xbox Elite 3 isn't recognized correctly and its paddles can't be bound. Deleting several items at once can error.

## Accessibility

- The pre-launch notes focused on UI and accessibility: combined-bag visibility, click-through debuff icons, and an elite-status nameplate fix.
- The low-health screen flash can be toggled (on by default).
- Forever-specific colorblind, text-to-speech and font-scaling options are **not documented**. Forever probably inherits the mainline options.

## Launch-night error codes

| Code / message | Meaning or fix |
|---|---|
| WOW51900337 | Servers not live yet |
| WOW51900309 | "No realms available"; requeue |
| BLZ51900033 / BLZ51901016 | Connection during maintenance |
| Fatal Error #134 | Invalid StartupFiles schema on some PCs |
| "No active game time" | Battle.net picked the wrong WoW account; select the right one |
| "Creation … currently throttled" | Population throttle on a race/class combination |
| Greyed-out rulesets | Cancel and requeue |
| 504 Gateway Time-out | Failed game-time purchases |
