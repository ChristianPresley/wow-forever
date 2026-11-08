# Add-ons & UI

## API rules

- **Midnight's add-on restrictions apply to Forever.** That includes **secret values**, where combat-state APIs return values add-ons can display but not compute on, and private auras.
- Forever shares the mainline UI architecture and exposes **most APIs from patch 12.1.5**.
- **TOC interface number: `16001`.** Add-ons need a separate *Forever* build. Classic Era packages won't load.
- The **CurseForge** app detects Forever installs from app version 1.324.
- Lua `require` is renamed `import`, GUIDs are obfuscated, and trial accounts can't send add-on messages. See [Patches](../about/patches.md#add-on-api-vs-retail-1215).
- **Design goal:** you shouldn't *need* add-ons to play your class correctly.

## Built-ins that replace add-ons

Damage Meter · Cooldown Manager · Swing Timer · Equipment Manager (in place of ItemRack) · mouseover casting · nameplate options · Edit Mode · Quest POIs · one-bag

## Notable Forever add-ons

| Add-on | Purpose | Notes |
|---|---|---|
| **Questie** (Forever build) | Quest map and objective helper | Updated for new zones. Data for new quests may be incomplete |
| **Dungeon Quests Forever** | Dungeon quest list | Uses the Questie DB |
| **Details!** (Forever Edition) | Damage meter | Optional now that a meter is built in |
| **Leatrix Plus** (Forever) | QoL toggles (auto-repair, sell greys…) | |
| **ClassicUI Forever** | Classic-style UI look | The kind of add-on Blizzard pointed players to instead of adding a toggle |
| **OpenMap** | World map with bosses, loot and routes | Works with Questie |
| **Vendor Price** | Vendor prices in tooltips | |
| **Forever Layer Hop** | Layer and group helper | |
| **Communities Forever** | Social grouping without a guild | |
| ForeverUI / ForeverPlus | UI suite / vendor helper | *unconfirmed*{ .unconfirmed } (single source) |
| CampfireKit | Camp features helper | *unconfirmed*{ .unconfirmed } |

!!! warning "WeakAuras"
    Some guides recommend WeakAuras, but it has **no Forever version**, and its team ended support for Midnight under the secret-values API. Treat any "WeakAuras for Forever" as unavailable.

## Data collection

The **Lexicon Client** (WarcraftDB) is a third-party desktop app for Windows and Linux. It reads your WoW cache and uploads discovered hidden items to *forever.warcraftdb.com*. Its terms-of-service status is unverified *unconfirmed*{ .unconfirmed }.

## UI defaults & tips

See [Systems & QoL](index.md) for the built-in UI features and the defaults worth changing.
