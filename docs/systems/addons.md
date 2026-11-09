# Add-ons & UI

## API rules

- **Midnight's add-on restrictions apply to Forever.** These include **secret values** and private auras. With secret values, combat-state APIs return values that add-ons can show but cannot use in calculations.
- Forever uses the same UI architecture as mainline WoW and gives access to **most APIs from patch 12.1.5**.
- **TOC interface number: `16001`.** Add-ons must have a separate *Forever* build. Classic Era packages do not load.
- The **CurseForge** app detects Forever installs from app version 1.324.
- Lua `require` has the new name `import`. GUIDs are obfuscated. Trial accounts cannot send add-on messages. See [Patches](../about/patches.md#add-on-api-vs-retail-1215).
- **Design goal:** you do not *need* add-ons to play your class correctly.

## Built-ins that replace add-ons

Damage Meter · Cooldown Manager · Swing Timer · Equipment Manager (in place of ItemRack) · mouseover casting · nameplate options · Edit Mode · Quest POIs · one-bag

## Notable Forever add-ons

| Add-on | Purpose | Notes |
|---|---|---|
| **Questie** (Forever build) | Quest map and objective helper | Updated for new zones. Data for new quests is possibly incomplete |
| **Dungeon Quests Forever** | Dungeon quest list | Uses the Questie DB |
| **Details!** (Forever Edition) | Damage meter | Optional, because the game now has a built-in meter |
| **Leatrix Plus** (Forever) | QoL toggles (auto-repair, sell greys…) | |
| **ClassicUI Forever** | Classic-style UI look | Blizzard told players to use this type of add-on and did not add a toggle |
| **OpenMap** | World map with bosses, loot and routes | Works with Questie |
| **Vendor Price** | Vendor prices in tooltips | |
| **Forever Layer Hop** | Layer and group helper | |
| **Communities Forever** | Social grouping without a guild | |
| ForeverUI / ForeverPlus | UI suite / vendor helper | *unconfirmed*{ .unconfirmed } (single source) |
| CampfireKit | Camp features helper | *unconfirmed*{ .unconfirmed } |

!!! warning "WeakAuras"
    Some guides recommend WeakAuras, but it has **no Forever version**. Its team stopped support for Midnight because of the secret-values API. Think of all "WeakAuras for Forever" as unavailable.

## Data collection

The **Lexicon Client** (WarcraftDB) is a third-party desktop app for Windows and Linux. It reads your WoW cache and uploads the hidden items that it finds to *forever.warcraftdb.com*. It is not known if it obeys the terms of service *unconfirmed*{ .unconfirmed }.

## UI defaults & tips

See [Systems & QoL](index.md) for the built-in UI features and the defaults that you can change.
