# Patches & Builds

The launch client is **Patch 1.60.1** (TOC `16001`). It is built on the same Mainline UI architecture as retail **12.1.5**. The next patch number seen in data is **1.60.2**, with no announced date.

## 1.60.1 build history

| Build | Date | Notes |
|---|---|---|
| 69977 | 22 Sep 2026 | Beta: Mac display, stability and controller fixes |
| 70009 | 23 Sep 2026 | Beta notable changes |
| 70058 | ~29 Sep 2026 | Beta: stability, audio, cooldown and weather fixes |
| 70170 | 1 Oct 2026 | Beta level cap raised to 30 |
| 70205 | 2 Oct 2026 | Consolidated API changes vs 12.1.5 |
| 70291 | 7 or 8 Oct 2026 | Beta 4 (sources disagree on the date) |
| 70425 | 16 Oct 2026 | Beta 5 |
| 70685 | 31 Oct 2026 | Paladin trees reworked. Feral and Restoration Druid reshaped. Frost and Arcane Mage retuned. Binding Heal becomes a trainer spell |
| 70707 | 3 Nov 2026 | Rogue rework (Shank, Death Mark, six new talents). Warrior *Reckless Swings* and *Improved Whirlwind*. Retribution changes |
| 70753 | 2 Nov 2026 | Blizzard's pre-launch notes: higher damage and tank threat, new training costs, gamepad and world fixes |
| 70755 | 3 Nov 2026 | Shaman rework: *Lava Burst* removed, *Call of Thunder* added, *Elemental Mastery* renamed *Lightning Mastery*. *Holy Shield* gains a 3rd rank |
| 70790 | 4 Nov 2026 | Launch-day client. Writes earlier hotfixes (including training costs) into the client |
| 70862 | 7 Nov 2026 | Current build. Tooltip fixes, Natural flask and Adventurer's Tent changes, 25 dungeon quest rewards filled in. No official notes |

!!! conflict "Conflict"
    Trackers disagree on whether **70755** or **70790** is the "launch client". Build dates come from community trackers (wowforevertalents.com) and the Warcraft Wiki.

## Hotfixes

- **5 Nov:** NPC spawn fixes (including a Zephras Druid trainer), Mild Spices vendor price, Plainsrunning stacking blocked in battlegrounds, quest text and respawn fixes.
- **6 Nov:** better long-range visibility of other players and their targets, in response to "empty world" feedback.
- **10 Nov (reported):** a class-tuning hotfix, per a third-party tracker. *unconfirmed*{ .unconfirmed }

## Add-on API (vs retail 12.1.5)

<div class="fc-matrix" markdown>

| | Added | Removed |
|---|---|---|
| Global API functions | 176 | 10 |
| FrameXML | 471 | 1,041 |

</div>

- Midnight's add-on restrictions ("disarmament" and secret values) apply to Forever.
- Creature, pet and object GUIDs use obfuscated IDs.
- Trial accounts cannot send add-on messages.
- Emote chat requires a hardware event outside instances.
- Lua `require` is renamed to `import`.
- Edit Mode layouts are saved separately for keyboard/mouse and gamepad.
- The `forever` game type is equivalent to `camelot`, and `WOW_PROJECT_CAMELOT` = 18.

See also: [Add-ons & UI](../systems/addons.md).
