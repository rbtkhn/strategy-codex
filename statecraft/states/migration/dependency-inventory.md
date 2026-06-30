
# CIV-STATE Dependency Inventory

This report inventories direct legacy `civ-mem` references inside the four active statecraft lanes. It is inventory-only and does not perform semantic migration.

## Summary

- Direct legacy reference occurrences: `610`
- Files with direct references: `36`
- Unique upstream `civ-mem` files referenced: `333`
- First-wave symmetric targets: `20`
- Current active-lane words: `98134`
- Current `civ-state` subtree words: `57662`

## Direct References By Lane

| Lane | Direct reference occurrences | Files with direct references |
| --- | ---: | ---: |
| America | 142 | 9 |
| China | 172 | 9 |
| Iran | 151 | 9 |
| Russia | 145 | 9 |

## Direct References By Object Class

| Object class | Direct reference occurrences |
| --- | ---: |
| `art` | 57 |
| `empire-instrument` | 35 |
| `geo` | 67 |
| `god` | 59 |
| `lit` | 74 |
| `peace` | 85 |
| `seed-patterns` | 71 |
| `state-memory` | 68 |
| `war` | 94 |

## Direct References By Upstream Civilization Folder

| Upstream folder | Direct reference occurrences |
| --- | ---: |
| `AMERICA` | 142 |
| `CHINA` | 172 |
| `PERSIA` | 151 |
| `RUSSIA` | 145 |

## Duplicate Upstream Source Usage

| Upstream `civ-mem` source | Consumer files | Notes |
| --- | --- | --- |
| `research/repos/civilization_memory/content/civilizations/AMERICA/CIVâ€“STATEâ€“AMERICA.md` | continuity/academy/statecraft/america/civilization/geo.md<br>continuity/academy/statecraft/america/civilization/objects/state-memory.md<br>continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `5` lane-local files |
| `research/repos/civilization_memory/content/civilizations/RUSSIA/CIV–CORE–RUSSIA.md` | continuity/academy/statecraft/russia/civilization/art.md<br>continuity/academy/statecraft/russia/civilization/god.md<br>continuity/academy/statecraft/russia/civilization/lit.md<br>continuity/academy/statecraft/russia/civilization/objects/state-memory.md<br>continuity/academy/statecraft/russia/civilization/seed-patterns.md | used by `5` lane-local files |
| `research/repos/civilization_memory/content/civilizations/RUSSIA/CIV–STATE–RUSSIA.md` | continuity/academy/statecraft/russia/civilization/art.md<br>continuity/academy/statecraft/russia/civilization/god.md<br>continuity/academy/statecraft/russia/civilization/lit.md<br>continuity/academy/statecraft/russia/civilization/objects/state-memory.md<br>continuity/academy/statecraft/russia/civilization/seed-patterns.md | used by `5` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/CIVâ€“COREâ€“AMERICA.md` | continuity/academy/statecraft/america/civilization/geo.md<br>continuity/academy/statecraft/america/civilization/objects/state-memory.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/CIVâ€“DOCTRINEâ€“AMERICA.md` | continuity/academy/statecraft/america/civilization/objects/state-memory.md<br>continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/CIV–CORE–AMERICA.md` | continuity/academy/statecraft/america/civilization/art.md<br>continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md<br>continuity/academy/statecraft/america/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/CIV–STATE–AMERICA.md` | continuity/academy/statecraft/america/civilization/art.md<br>continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md<br>continuity/academy/statecraft/america/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEMâ€“AMERICAâ€“LAWâ€“CONGRESS.md` | continuity/academy/statecraft/america/civilization/objects/state-memory.md<br>continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEMâ€“AMERICAâ€“LAWâ€“CONSTITUTION.md` | continuity/academy/statecraft/america/civilization/objects/state-memory.md<br>continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEMâ€“RELEVANCEâ€“AMERICA.md` | continuity/academy/statecraft/america/civilization/geo.md<br>continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/CIV–CORE–CHINA.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/CIV–DOCTRINE–CHINA.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–DYNASTY–QIN.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–DYNASTY–ZHOU.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–WAR–BOXER–REBELLION.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–WAR–TAIPING–REBELLION.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–RELEVANCE–CHINA.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/CIV–CORE–PERSIA.md` | continuity/academy/statecraft/persia/civilization/art.md<br>continuity/academy/statecraft/persia/civilization/god.md<br>continuity/academy/statecraft/persia/civilization/lit.md<br>continuity/academy/statecraft/persia/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/CIV–STATE–PERSIA.md` | continuity/academy/statecraft/persia/civilization/art.md<br>continuity/academy/statecraft/persia/civilization/god.md<br>continuity/academy/statecraft/persia/civilization/lit.md<br>continuity/academy/statecraft/persia/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/MEM–PERSIA–ISLAM.md` | continuity/academy/statecraft/persia/civilization/art.md<br>continuity/academy/statecraft/persia/civilization/god.md<br>continuity/academy/statecraft/persia/civilization/lit.md<br>continuity/academy/statecraft/persia/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/MEM–PERSIA–LAW–SASANIAN.md` | continuity/academy/statecraft/persia/civilization/art.md<br>continuity/academy/statecraft/persia/civilization/god.md<br>continuity/academy/statecraft/persia/civilization/lit.md<br>continuity/academy/statecraft/persia/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/RUSSIA/MEM–RELEVANCE–RUSSIA.md` | continuity/academy/statecraft/russia/civilization/art.md<br>continuity/academy/statecraft/russia/civilization/god.md<br>continuity/academy/statecraft/russia/civilization/lit.md<br>continuity/academy/statecraft/russia/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/RUSSIA/MEM–RUSSIA–SOVIET–UNION.md` | continuity/academy/statecraft/russia/civilization/art.md<br>continuity/academy/statecraft/russia/civilization/god.md<br>continuity/academy/statecraft/russia/civilization/objects/state-memory.md<br>continuity/academy/statecraft/russia/civilization/seed-patterns.md | used by `4` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/CIV–DOCTRINE–AMERICA.md` | continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md<br>continuity/academy/statecraft/america/civilization/seed-patterns.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEMâ€“AMERICAâ€“DIPLOMACYâ€“COLDâ€“WAR.md` | continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEMâ€“AMERICAâ€“DIPLOMACYâ€“MONROEâ€“DOCTRINE.md` | continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEMâ€“AMERICAâ€“WARâ€“NAVY.md` | continuity/academy/statecraft/america/civilization/peace.md<br>continuity/academy/statecraft/america/civilization/war.md<br>continuity/academy/statecraft/america/empire/seed-instruments.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEM–AMERICA–LAW–CONSTITUTION.md` | continuity/academy/statecraft/america/civilization/art.md<br>continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEM–AMERICA–LAW–SLAVERY.md` | continuity/academy/statecraft/america/civilization/art.md<br>continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEM–AMERICA–MANIFEST–DESTINY.md` | continuity/academy/statecraft/america/civilization/art.md<br>continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEM–AMERICA–PRESIDENT–WILSON.md` | continuity/academy/statecraft/america/civilization/art.md<br>continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/AMERICA/MEM–RELEVANCE–AMERICA.md` | continuity/academy/statecraft/america/civilization/art.md<br>continuity/academy/statecraft/america/civilization/god.md<br>continuity/academy/statecraft/america/civilization/lit.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/CIVâ€“COREâ€“CHINA.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/CIVâ€“DOCTRINEâ€“CHINA.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/CIVâ€“STATEâ€“CHINA.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/CIV–STATE–CHINA.md` | continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEMâ€“CHINAâ€“GEOâ€“EASTâ€“CHINAâ€“SEA.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEMâ€“CHINAâ€“GEOâ€“SOUTHâ€“CHINAâ€“SEA.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEMâ€“CHINAâ€“GEOâ€“TAIWANâ€“STRAIT.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEMâ€“CHINAâ€“GRANDâ€“CANAL.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEMâ€“RELEVANCEâ€“CHINA.md` | continuity/academy/statecraft/china/civilization/geo.md<br>continuity/academy/statecraft/china/civilization/peace.md<br>continuity/academy/statecraft/china/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–LIT–KONGZI.md` | continuity/academy/statecraft/china/civilization/art.md<br>continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–PRC.md` | continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–ROC.md` | continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–TAIWAN.md` | continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/CHINA/MEM–CHINA–WAR–FIRST–OPIUM.md` | continuity/academy/statecraft/china/civilization/god.md<br>continuity/academy/statecraft/china/civilization/lit.md<br>continuity/academy/statecraft/china/civilization/seed-patterns.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/CIVâ€“COREâ€“PERSIA.md` | continuity/academy/statecraft/persia/civilization/geo.md<br>continuity/academy/statecraft/persia/civilization/peace.md<br>continuity/academy/statecraft/persia/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/CIVâ€“STATEâ€“PERSIA.md` | continuity/academy/statecraft/persia/civilization/geo.md<br>continuity/academy/statecraft/persia/civilization/peace.md<br>continuity/academy/statecraft/persia/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/MEMâ€“PERSIAâ€“GEOâ€“PERSIANâ€“GULF.md` | continuity/academy/statecraft/persia/civilization/geo.md<br>continuity/academy/statecraft/persia/civilization/peace.md<br>continuity/academy/statecraft/persia/civilization/war.md | used by `3` lane-local files |
| `research/repos/civilization_memory/content/civilizations/PERSIA/MEMâ€“PERSIAâ€“IRANâ€“ISLAMICâ€“REPUBLIC.md` | continuity/academy/statecraft/persia/civilization/geo.md<br>continuity/academy/statecraft/persia/civilization/peace.md<br>continuity/academy/statecraft/persia/civilization/war.md | used by `3` lane-local files |

## Candidate First-Wave Objects Implied By Current Dependency Surface

| Target object | Volume side | Current lane-local consumers | Direct reference count | Current words | Target band | Current note |
| --- | --- | --- | ---: | ---: | --- | --- |
| `america-state-memory` | `civilization` | continuity/academy/statecraft/america/civilization/objects/state-memory.md | 10 | 3553 | `3500-4500` | direct CIV-MEM dependency already present |
| `america-geo` | `civilization` | continuity/academy/statecraft/america/civilization/geo.md | 16 | 2683 | `2500-3500` | direct CIV-MEM dependency already present |
| `america-war` | `civilization` | continuity/academy/statecraft/america/civilization/war.md | 35 | 2942 | `3000-4000` | direct CIV-MEM dependency already present |
| `america-peace` | `civilization` | continuity/academy/statecraft/america/civilization/peace.md | 16 | 2891 | `3000-4000` | direct CIV-MEM dependency already present |
| `america-empire-instrument` | `empire` | continuity/academy/statecraft/america/empire/seed-instruments.md | 9 | 2821 | `2500-3500` | direct CIV-MEM dependency already present |
| `russia-state-memory` | `civilization` | continuity/academy/statecraft/russia/civilization/objects/state-memory.md | 13 | 3443 | `3500-4500` | direct CIV-MEM dependency already present |
| `russia-geo` | `civilization` | continuity/academy/statecraft/russia/civilization/geo.md | 16 | 2565 | `2500-3500` | direct CIV-MEM dependency already present |
| `russia-war` | `civilization` | continuity/academy/statecraft/russia/civilization/war.md | 19 | 2889 | `3000-4000` | direct CIV-MEM dependency already present |
| `russia-peace` | `civilization` | continuity/academy/statecraft/russia/civilization/peace.md | 23 | 2958 | `3000-4000` | direct CIV-MEM dependency already present |
| `russia-empire-instrument` | `empire` | continuity/academy/statecraft/russia/empire/seed-instruments.md | 9 | 3230 | `2500-3500` | direct CIV-MEM dependency already present |
| `china-state-memory` | `civilization` | continuity/academy/statecraft/china/civilization/objects/state-memory.md | 24 | 3580 | `3500-4500` | direct CIV-MEM dependency already present |
| `china-geo` | `civilization` | continuity/academy/statecraft/china/civilization/geo.md | 18 | 2575 | `2500-3500` | direct CIV-MEM dependency already present |
| `china-war` | `civilization` | continuity/academy/statecraft/china/civilization/war.md | 22 | 2990 | `3000-4000` | direct CIV-MEM dependency already present |
| `china-peace` | `civilization` | continuity/academy/statecraft/china/civilization/peace.md | 24 | 2880 | `3000-4000` | direct CIV-MEM dependency already present |
| `china-empire-instrument` | `empire` | continuity/academy/statecraft/china/empire/seed-instruments.md | 9 | 3063 | `2500-3500` | direct CIV-MEM dependency already present |
| `iran-state-memory` | `civilization` | continuity/academy/statecraft/persia/civilization/objects/state-memory.md | 21 | 3276 | `3500-4500` | direct CIV-MEM dependency already present |
| `iran-geo` | `civilization` | continuity/academy/statecraft/persia/civilization/geo.md | 17 | 2592 | `2500-3500` | direct CIV-MEM dependency already present |
| `iran-war` | `civilization` | continuity/academy/statecraft/persia/civilization/war.md | 18 | 2799 | `3000-4000` | direct CIV-MEM dependency already present |
| `iran-peace` | `civilization` | continuity/academy/statecraft/persia/civilization/peace.md | 22 | 2819 | `3000-4000` | direct CIV-MEM dependency already present |
| `iran-empire-instrument` | `empire` | continuity/academy/statecraft/persia/empire/seed-instruments.md | 8 | 2832 | `2500-3500` | direct CIV-MEM dependency already present |
