# Patches & Builds

The launch client is **Patch 1.60.1** (TOC `16001`). It uses the same Mainline UI architecture as retail **12.1.5**. The data shows **1.60.2** as the next patch number. Blizzard has not announced a date for it.

## 1.60.1 build history

<div class="timeline" markdown>

- **22 Sep 2026 · build 69977** Beta: Mac display, stability and controller fixes **Beta**{ .pill .pill--outline .pill--sm }
- **23 Sep 2026 · build 70009** Beta notable changes **Beta**{ .pill .pill--outline .pill--sm }
- **~29 Sep 2026 · build 70058** Beta: stability, audio, cooldown and weather fixes **Beta**{ .pill .pill--outline .pill--sm }
- **1 Oct 2026 · build 70170** Beta level cap raised to 30 **Beta**{ .pill .pill--outline .pill--sm }
- **2 Oct 2026 · build 70205** Consolidated API changes vs 12.1.5
- **7 or 8 Oct 2026 · build 70291** Beta 4 (sources disagree on the date) **Beta**{ .pill .pill--outline .pill--sm }
- **16 Oct 2026 · build 70425** Beta 5 **Beta**{ .pill .pill--outline .pill--sm }
- **31 Oct 2026 · build 70685** Paladin trees reworked. Feral and Restoration Druid reshaped. Frost and Arcane Mage retuned. Binding Heal becomes a trainer spell
- **3 Nov 2026 · build 70707** Rogue rework (Shank, Death Mark, 6 new talents). Warrior *Reckless Swings* and *Improved Whirlwind*. Retribution changes
- **2 Nov 2026 · build 70753** Blizzard's pre-launch notes: higher damage and tank threat, new training costs, gamepad and world fixes
- **3 Nov 2026 · build 70755** Shaman rework: *Lava Burst* removed, *Call of Thunder* added, *Elemental Mastery* renamed *Lightning Mastery*. *Holy Shield* gains a 3rd rank
- **4 Nov 2026 · build 70790** Launch-day client. Puts earlier hotfixes (including training costs) into the client **Launch day**{ .pill .pill--gold }
- **7 Nov 2026 · build 70862** Current build. Tooltip fixes, Natural flask and Adventurer's Tent changes, 25 dungeon quest rewards added. No official notes **Current**{ .pill .pill--live }

</div>

!!! conflict "Conflict"
    Trackers disagree on whether **70755** or **70790** is the "launch client". Build dates come from community trackers (wowforevertalents.com) and the Warcraft Wiki.

## Hotfixes

- **5 Nov:** NPC spawn fixes (including a Zephras Druid trainer), Mild Spices vendor price, Plainsrunning stacking blocked in battlegrounds, quest text and respawn fixes.
- **6 Nov:** better long-range visibility of other players and their targets, in response to "empty world" feedback.
- **10 Nov (reported):** a class-tuning hotfix, from a third-party tracker. *unconfirmed*{ .unconfirmed }

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
- Outside instances, emote chat needs a hardware event.
- Lua `require` is renamed to `import`.
- Edit Mode saves layouts separately for keyboard/mouse and gamepad.
- The `forever` game type is the same as `camelot`, and `WOW_PROJECT_CAMELOT` = 18.

See also: [Add-ons & UI](../systems/addons.md).
