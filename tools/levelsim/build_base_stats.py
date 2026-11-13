"""Build base_stats.json from cmangos classic-db player_levelstats. See BASE_STATS.md.

Usage: python build_base_stats.py ClassicDB_1_12_1_z2815.sql.gz [out.json]
Source: https://github.com/cmangos/classic-db/raw/master/Full_DB/ClassicDB_1_12_1_z2815.sql.gz (GPL-2.0)
"""
import gzip, re, json, sys
from pathlib import Path
src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else Path(__file__).resolve().parent / "base_stats.json"
RACE={1:"human",2:"orc",3:"dwarf",4:"nelf",5:"undead",6:"tauren",7:"gnome",8:"troll"}
CLS={1:"warrior",2:"paladin",3:"hunter",4:"rogue",5:"priest",7:"shaman",8:"mage",9:"warlock",11:"druid"}
K=["str","agi","sta","int","spi"]
t={}
sql = gzip.open(src, "rt", encoding="utf-8", errors="replace").read()
sql = sql.split("INSERT INTO `player_levelstats`", 1)[1].split(";\n", 1)[0]
for m in re.finditer(r"\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)\)", sql):
    r,c,l,*v=map(int,m.groups())
    if l<=60 and r in RACE and c in CLS: t.setdefault(CLS[c],{}).setdefault(RACE[r],{})[l]=v
# race offset vs human, from warrior level 1
d={r:[a-b for a,b in zip(t["warrior"][r][1],t["warrior"]["human"][1])] for r in t["warrior"]}
sky=list(d["nelf"]); sky[0]=5  # Forever fix: Skyborne +5 Str vs Human (like Tauren)
d["sho"]=d["sws"]=sky
CR={"warrior":["human","dwarf","gnome","nelf","sho","orc","troll","tauren","undead","sws"],"paladin":["human","dwarf","undead"],"hunter":["human","dwarf","nelf","sho","orc","troll","tauren","sws"],"rogue":["human","dwarf","gnome","nelf","sho","orc","troll","undead","sws"],"priest":["human","dwarf","gnome","nelf","troll","undead"],"shaman":["dwarf","orc","troll","tauren","sws"],"mage":["human","gnome","sho","orc","troll","undead"],"warlock":["human","gnome","orc","troll","undead"],"druid":["nelf","sho","tauren","sws"]}
res={}; derived=[]
for c,races in CR.items():
    ref=sorted(t[c])[0]
    res[c]={}
    for r in races:
        if r in t[c]: rows=t[c][r]
        else:
            derived.append(f"{c}/{r}")
            rows={l:[v-d[ref][i]+d[r][i] for i,v in enumerate(vs)] for l,vs in t[c][ref].items()}
        res[c][r]={str(l):dict(zip(K,rows[l])) for l in range(1,61)}
res["mage"]["undead"]["1"].update(int=21, spi=27)  # cmangos row has Int/Spi swapped
res={"_source":{
 "summary":"Base attributes (no gear, no buffs) per class/race/level 1-60. See BASE_STATS.md.",
 "tags":{"F":"Forever client data","C":"Classic 1.12 server data","A":"assumption"},
 "C":"Existing Classic class/race pairs copied from player_levelstats in cmangos classic-db (ClassicDB_1_12_1_z2815, GPL-2.0), https://github.com/cmangos/classic-db",
 "F":"Forever client RaceStat (build 1.60.1.70938) checked: its one unknown column is 0 for every race, so it holds no stats. Base attributes are server-side; no other client table was found to hold them.",
 "A_new_pairs":"New Forever pairs built as Classic class curve (from "+"the first Classic race of that class) minus that race's level-1 offset vs Human Warrior plus the target race's offset: "+", ".join(derived),
 "A_skyborne":"sho/sws: Night Elf offsets vs Human, but Str set to Human+5 (published Forever fix: Tauren Warrior +5 Str vs Human, same fix for both Skyborne). No published Skyborne table.",
 "A_tauren":"Classic Tauren Warrior is already +5 Str vs Human at level 1, so the Tauren fix needs no change."}, **res}
res["_source"]["A_fix"]="mage/undead level 1: cmangos has int 27 / spi 21, which looks swapped (Undead is Int -2, Spi +5 vs Human). Swapped to int 21 / spi 27."
json.dump(res,open(out,"w"),indent=1)
print(derived)
