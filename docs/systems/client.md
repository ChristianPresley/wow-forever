# Client, Gamepad & Tech

## System requirements

<div class="compare" markdown>

| Component | Minimum | Recommended |
|---|---|---|
| CPU | 4 cores @ 3.0 GHz | 8 P-cores, 5.2 GHz boost (Intel Core Ultra 200 / Ryzen 9000) |
| RAM | 8 GB | 16 GB |
| GPU | GTX 10-series / AMD RDNA 1, 4 GB VRAM | DX12, 8 GB VRAM (RTX 40 / RX 7000 / Arc B-series) |
| Storage | **SSD required, 128 GB free** (HDDs not supported) | — |
| OS | Windows 10 64-bit / macOS | — |

</div>

!!! unconfirmed "Partly unverified"
    PC Games Hardware says that the CPU, GPU and RAM rows come from Blizzard. A different FAQ says that only the **128 GB SSD** figure is official. Think of the CPU and GPU rows as unverified.

- **Download:** about **52.9 GB** for a new installation, or about 13 GB if retail or Classic is already installed.
- **Drivers:** NVIDIA Game Ready **621.14** WHQL includes Forever optimizations. **Ray-traced shadows were not available at launch**. Blizzard plans to restore them. AMD Anti-Lag 2 has no in-game option.
- **Graphics:** new lighting with global illumination, volumetric fog and god rays, a new water renderer, and real-time sun shadows. Blizzard adjusted the lighting by hand for each zone. Hazzikostas gave Duskwood at night, with torchlit patrols, as an example.
- On some Windows 11 computers, Battle.net refused the installation as "below minimum". This was an error.

## Gamepad (beta feature)

- Supports **all XInput controllers**, with Xbox or PlayStation glyphs. Enable it under *Options → Gameplay → Gamepad*.
- **Movement:** the left stick moves and the right stick turns the camera. To zoom, use LB+RB and the right stick.
- **Targeting:** **LB** targets friendly, **RB** targets hostile.
- **Face buttons:** X interacts, A jumps, B goes back, Y inspects.
- **Action bars:** 4 bars on screen. To change bars, hold LT, RT or both. **Up to 84 ability slots** across 3 bar sets.
- **Shortcuts:** LB+RB and a face button or the D-pad open the bags, quest tracker, chat and buffs.
- Faction-colored controller lights on supported pads.
- You can stop a flight early and dismount at the next flight point.
- **Chat still needs a keyboard.** Play without a keyboard is a long-term goal.
- Paul Kubit described controller support as an accessibility feature.
- **Known issues:** the game does not recognize the Xbox Elite 3 correctly, and you cannot bind its paddles. If you delete many items at the same time, an error can occur.

## Accessibility

- The pre-launch notes were mainly about UI and accessibility: combined-bag visibility, click-through debuff icons, and an elite-status nameplate fix.
- You can enable or disable the low-health screen flash (it is enabled by default).
- Colorblind, text-to-speech and font-scaling options for Forever are **not documented**. Forever probably uses the mainline options.

## Launch-night error codes

| Code / message | Meaning or fix |
|---|---|
| WOW51900337 | Servers not live yet |
| WOW51900309 | "No realms available". Queue again |
| BLZ51900033 / BLZ51901016 | Connection during maintenance |
| Fatal Error #134 | Invalid StartupFiles schema on some PCs |
| "No active game time" | Battle.net selected the wrong WoW account. Select the correct one |
| "Creation … currently throttled" | Population throttle on a race/class combination |
| Greyed-out rulesets | Cancel and queue again |
| 504 Gateway Time-out | Failed game-time purchases |
