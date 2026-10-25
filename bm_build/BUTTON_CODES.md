# Button codes (`/trigger bm.act set N`) - v2.94s

Written by `buttons.py` at the end of every build (`python3 gen_dp.py --phase2`); for any build: `python3 buttons.py <BlackMarket_DP dir> <version>`. Edit only the **Notes** - they are kept as written.

**1424 codes** on 2701 buttons and chat links (2 more built at run time) · 261 routes in `p28/act` · **6037 codes free** in 1-9999 · problems: **0**

## Adding a button

1. Pick a code: a free one inside your feature's block (**Blocks**), or a fresh run from **Free codes**.
2. Route it with an exact `matches N` line - a range only over a block your router owns - and have the router check `bm.menu` (the menu that shows the button) before it acts.
3. Build: phase129 refuses a shadowed route; this file rewrites itself; **Problems** should say none.
4. Test by pressing the button the client was shown (bots: `A.press(/words/)` sends exactly its command).

## Problems

None.

Same code, different words (fine when each menu's router checks `bm.menu`): **2240** « Outfits & buffs / $(r_home); **2260** « Outfits & buffs / $(r_home); **2300** « Outfits & buffs / $(r_home); **2460** « Outfits & buffs / $(r_home); **2520** « Outfits & buffs / $(r_home); **2560** « Outfits & buffs / $(r_home); **2640** « Outfits & buffs / $(r_home); **2660** « Outfits & buffs / $(r_home); **2680** « Outfits & buffs / $(r_home); **2720** « Outfits & buffs / $(r_home); **2760** « Outfits & buffs / $(r_home); **2800** « Outfits & buffs / $(r_home); **2840** « Outfits & buffs / $(r_home); **2880** « Outfits & buffs / $(r_home); **2900** « Outfits & buffs / $(r_home); **2960** « Outfits & buffs / $(r_home); **3000** « Outfits & buffs / $(r_home); **3040** « Outfits & buffs / $(r_home); **3351** Keep up: off / Keep up: on; **3360** Call Emma / Send Emma home; **3361** Call Celi / Send Celi home; **3362** Call Zib / Send Zib home; **3363** Call Cecil / Send Cecil home; **3364** Call KillerWatt / Send KillerWatt home; **3365** Call Leo / Send Leo home; **3366** Call Democratus / Send Democratus home; **3367** Call Apophiss / Send Apophiss home; **3368** Call Tullius / Send Tullius home; **3369** Call the Frog / Send the Frog home; **3370** Call Donado / Send Donado home; **3371** Call Pearlman / Send Pearlman home; **3372** Call Wilfrey / Send Wilfrey home; **3373** Call Fishy / Send Fishy home; **3374** Call Dennis / Send Dennis home; **3375** Call Pistachio / Send Pistachio home; **3376** Call King Omega / Send King Omega home; **3377** Call Ashur / Send Ashur home; **3378** Call the Chef / Send the Chef home; **3379** Call the Neighbor / Send the Neighbor home; **3380** Call Queen Ava / Send Queen Ava home; **3381** Call Queen Pearl / Send Queen Pearl home; **3382** Call Bloo / Send Bloo home; **3383** Call The Stalker / Send The Stalker home; **3384** Call The Arachno-Lantern / Send The Arachno-Lantern home; **3385** Call Bender / Send Bender home; **3386** Call Bones / Send Bones home; **3387** Call Mr. Capshun / Send Mr. Capshun home; **3388** Call 8-Bit Cecil / Send 8-Bit Cecil home; **3389** Call 8-Bit Leo / Send 8-Bit Leo home; **3420** Launch your Skiff Escort / Send your Skiff Escort home; **3482** Fall / Fall (locked); **3483** Christmas / Christmas (locked); **3484** Easter / Easter (locked); **3485** Summer / Summer (locked); **3700** Call 8-Bit Emma / Send 8-Bit Emma home; **3701** Call The Sky Buddies / Send The Sky Buddies home; **4072** « Back to your account / « Your account; **7735** Chatter: $(chat) (all followers) / Chatter: off / Chatter: on; **7800** « Office / « The Office / ◀ The Office / Stay on the job; **7802** « Back / Gutter Bank / ⛃ Gutter Bank / « Your account

## Blocks

Ranges `p28/act` hands whole to one router (the exact-code routes are in **All codes**).

| Block | Router | Menu | Buttons | Free inside |
|---|---|---|---:|---:|
| 1000-1999 | `p28/back/act` | — | 30 | 970 |
| 2000-2099 | `p28/gate/act` | 201 | 1 | 99 |
| 2100-2149 | `p162/dw/act` | 2100 | 11 | 39 |
| 2150-2199 | `p162/ps/act` | 2150 | 25 | 25 |
| 2240-2259 | `p99/act/dennis` | 2240 | 10 | 10 |
| 2260-2279 | `p99/act/pistachio` | 2260 | 10 | 10 |
| 2300-2319 | `p99/act/omega` | 2300 | 10 | 10 |
| 2361-2364 | `p173/wil/act` | 2360 | 4 | 0 |
| 2370-2400 | `p173/ar/act` | — | 31 | 0 |
| 2401-2421 | `p171/act` | 2400 | 21 | 0 |
| 2460-2479 | `p99/act/ashur` | 2460 | 10 | 10 |
| 2520-2539 | `p99/act/chef` | 2520 | 10 | 10 |
| 2560-2579 | `p99/act/neighbor` | 2560 | 10 | 10 |
| 2640-2659 | `p99/act/ava` | 2640 | 10 | 10 |
| 2660-2679 | `p99/act/pearlq` | 2660 | 10 | 10 |
| 2680-2699 | `p99/act/bloo` | 2680 | 10 | 10 |
| 2720-2739 | `p99/act/stalker` | 2720 | 10 | 10 |
| 2760-2779 | `p99/act/lantern` | 2760 | 10 | 10 |
| 2800-2819 | `p99/act/bender` | 2800 | 10 | 10 |
| 2840-2859 | `p99/act/bones` | 2840 | 10 | 10 |
| 2870-2876 | `p198/pal_act` | 2860 | 7 | 0 |
| 2880-2899 | `p99/act/capshun` | 2880 | 10 | 10 |
| 2900-2919 | `p99/act/sky` | 2900 | 10 | 10 |
| 2960-2979 | `p99/act/pxemma` | 2960 | 9 | 11 |
| 3000-3019 | `p99/act/pxleo` | 3000 | 9 | 11 |
| 3040-3059 | `p99/act/pxcecil` | 3040 | 9 | 11 |
| 3100-3199 | `p30/act` | 300 | 5 | 95 |
| 3200-3299 | `p177/act` | 3200 | 21 | 79 |
| 3300-3349 | `p178/pots/act` | 3300 | 26 | 24 |
| 3350-3449 | `p179/w/act` | 3350 | 69 | 31 |
| 3450-3479 | `p179/w/act` | 3350 | 30 | 0 |
| 3480-3485 | `p209/act` | 971 | 6 | 0 |
| 3600-3699 | `p103/tl/act` | — | 21 | 79 |
| 3700-3819 | `p179/w/act` | 3350 | 6 | 114 |
| 4000-4099 | `p31/bank/act` | 400 | 72 | 28 |
| 4100-4199 | `p201/act` | 4100 | 6 | 94 |
| 4200-4299 | `p205/act` | 4200 | 9 | 91 |
| 5000-5099 | `p31/conc/act` | 500 | 4 | 96 |
| 6001-6099 | `p29/burrow/act` | 600 | 6 | 93 |
| 7001-7099 | `p29/merc/act` | 700 | 7 | 92 |
| 7101-7102 | `p34/renew/act` | 950 | 2 | 0 |
| 7201-7203 | `p33/shift/act` | 900 | 3 | 0 |
| 7301-7309 | `p57/act` | 960 | 9 | 0 |
| 7310-7313 | `p57/act` | 960 | 4 | 0 |
| 7601-7605 | `p70/pick_tier` | 1100 | 5 | 0 |
| 7606-7607 | `p77/pick_mode` | 1100 | 2 | 0 |
| 7611-7613 | `p75/pick_lives` | 1100 | 3 | 0 |
| 7720-7723 | `p101/act` | — | 4 | 0 |
| 7724-7728 | `p103/act` | — | 5 | 0 |
| 7730-7732 | `p121/act` | — | 3 | 0 |
| 7740-7799 | `p103/tl/act` | — | 53 | 7 |
| 7800-7999 | `p80/act` | 7800..7999 | 124 | 76 |
| 8000-8099 | `p137/rc/act` | 8000 | 48 | 52 |
| 8100-8199 | `p103/tl/act` | — | 100 | 0 |
| 8200-8279 | `p103/tl/act` | — | 80 | 0 |
| 8280-8304 | `p119/act` | — | 25 | 0 |
| 8293-8299 | `p103/tl/act` | — | 7 | 0 |
| 8301-8309 | `p128/pm/act` | 970 | 5 | 4 |
| 8380-8399 | `p103/tl/act` | — | 7 | 13 |
| 8411-8413 | `p86/theme/pick` | 8410 | 0 | 3 |
| 8501-8507 | `p105/desk/buy` | 8500 | 7 | 0 |
| 9000-9019 | `p99/act/apo` | 9000 | 10 | 10 |
| 9020-9039 | `p99/act/tul` | 9020 | 10 | 10 |
| 9040-9059 | `p99/act/frog` | 9040 | 10 | 10 |
| 9060-9079 | `p99/act/don` | 9060 | 11 | 9 |
| 9080-9099 | `p99/act/pearl` | 9080 | 10 | 10 |
| 9100-9119 | `p99/act/wil` | 9100 | 10 | 10 |
| 9120-9139 | `p99/act/fishy` | 9120 | 10 | 10 |
| 9150-9159 | `p145/cab/act` | 9150 | 10 | 0 |
| 9701-9703 | `p97/act` | 9700 | 3 | 0 |
| 9800-9839 | `p99/act/emma` | 9800 | 21 | 19 |
| 9840-9859 | `p99/act/celi` | 9840 | 11 | 9 |
| 9860-9879 | `p99/act/zib` | 9860 | 9 | 11 |
| 9880-9899 | `p99/act/cecil` | 9880 | 9 | 11 |
| 9900-9919 | `p99/act/kw` | 9900 | 10 | 10 |
| 9920-9939 | `p99/act/leo` | 9920 | 9 | 11 |
| 9940-9959 | `p99/act/demo` | 9940 | 10 | 10 |

## All codes

"Shown in" is the dialog title (or the function, for chat links and rows built in storage); "Menu" is the `bm.menu` that function opens; the route reads `p28/act` → router [the menu it insists on] → handler.

| Code | Words | Shown in | Menu | Route |
|---:|---|---|---|---|
| 2 | Keep at it | Skip this puzzle? (p122/ask_dlg); The Fixer's mercy (p166/m_dlg) | — | (does nothing) |
| 1020 | Sealed Explorer's Map 2 Tokens | The Fence - Back Room (dialog p28/back_fence_1); The Fence - Back Room (dialog p28/back_fence_2); The Fence - Back Room (dialog p28/back_fence_3) (+1 more) | 101 | `p28/back/act` → `p28/back/act_1` [menu 101] → `p28/back/buy_1_0` |
| 1021 | 2 Ominous Trial Keys 2 Medallions | The Fence - Back Room (dialog p28/back_fence_2); The Fence - Back Room (dialog p28/back_fence_3); The Fence - Back Room (dialog p28/back_fence_4) | 101 | `p28/back/act` → `p28/back/act_1` [menu 101] → `p28/back/buy_1_1` |
| 1022 | Smuggler's Jar 4 Medallions | The Fence - Back Room (dialog p28/back_fence_4) | 101 | `p28/back/act` → `p28/back/act_1` [menu 101] → `p28/back/buy_1_2` |
| 1040 | Fair Weather Bell 4 Tokens | Old Barnaby - Back Room (dialog p28/back_pawn_1); Old Barnaby - Back Room (dialog p28/back_pawn_2); Old Barnaby - Back Room (dialog p28/back_pawn_3) (+1 more) | 102 | `p28/back/act` → `p28/back/act_2` [menu 102] → `p28/back/buy_2_0` |
| 1041 | 2 Totems of Undying 2 Medallions | Old Barnaby - Back Room (dialog p28/back_pawn_2); Old Barnaby - Back Room (dialog p28/back_pawn_3); Old Barnaby - Back Room (dialog p28/back_pawn_4) | 102 | `p28/back/act` → `p28/back/act_2` [menu 102] → `p28/back/buy_2_1` |
| 1042 | Spawner Crowbar 5 Medallions | Old Barnaby - Back Room (dialog p28/back_pawn_4) | 102 | `p28/back/act` → `p28/back/act_2` [menu 102] → `p28/back/buy_2_2` |
| 1060 | Rat Gang Portrait 2 Tokens | Madame Velour - Back Room (dialog p28/back_outfitter_1); Madame Velour - Back Room (dialog p28/back_outfitter_2); Madame Velour - Back Room (dialog p28/back_outfitter_3) (+1 more) | 103 | `p28/back/act` → `p28/back/act_3` [menu 103] → `p28/back/buy_3_0` |
| 1061 | Donado Trophy 2 Medallions | Madame Velour - Back Room (dialog p28/back_outfitter_2); Madame Velour - Back Room (dialog p28/back_outfitter_3); Madame Velour - Back Room (dialog p28/back_outfitter_4) | 103 | `p28/back/act` → `p28/back/act_3` [menu 103] → `p28/back/buy_3_1` |
| 1062 | Brass Wing Scroll 1 Trophy | Madame Velour - Back Room (dialog p28/back_outfitter_4) | 103 | `p28/back/act` → `p28/back/act_3` [menu 103] → `p28/back/buy_3_2` |
| 1080 | 16 Spectral Arrows 2 Tokens | Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_1); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_2); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_3) (+1 more) | 104 | `p28/back/act` → `p28/back/act_4` [menu 104] → `p28/back/buy_4_0` |
| 1081 | Netherite Upgrade Template 2 Medallions | Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_2); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_3); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_4) | 104 | `p28/back/act` → `p28/back/act_4` [menu 104] → `p28/back/buy_4_1` |
| 1082 | Showstopper Charm 1 Trophy | Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_4) | 104 | `p28/back/act` → `p28/back/act_4` [menu 104] → `p28/back/buy_4_2` |
| 1100 | Lodestone Locket 5 Tokens | Sgt. Steelwhisker - Back Room (dialog p28/back_armory_1); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_2); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_3) (+1 more) | 105 | `p28/back/act` → `p28/back/act_5` [menu 105] → `p28/back/buy_5_0` |
| 1101 | 3 Wither Skeleton Skulls 2 Medallions | Sgt. Steelwhisker - Back Room (dialog p28/back_armory_2); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_3); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_4) | 105 | `p28/back/act` → `p28/back/act_5` [menu 105] → `p28/back/buy_5_1` |
| 1102 | Market Crest Scroll 1 Trophy | Sgt. Steelwhisker - Back Room (dialog p28/back_armory_4) | 105 | `p28/back/act` → `p28/back/act_5` [menu 105] → `p28/back/buy_5_2` |
| 1120 | A Whole Cake 1 Token | Chef Fromage - Back Room (dialog p28/back_chef_1); Chef Fromage - Back Room (dialog p28/back_chef_2); Chef Fromage - Back Room (dialog p28/back_chef_3) (+1 more) | 106 | `p28/back/act` → `p28/back/act_6` [menu 106] → `p28/back/buy_6_0` |
| 1121 | Enchanted Golden Apple 4 Medallions | Chef Fromage - Back Room (dialog p28/back_chef_2); Chef Fromage - Back Room (dialog p28/back_chef_3); Chef Fromage - Back Room (dialog p28/back_chef_4) | 106 | `p28/back/act` → `p28/back/act_6` [menu 106] → `p28/back/buy_6_1` |
| 1122 | 3 Enchanted Golden Apples 1 Trophy | Chef Fromage - Back Room (dialog p28/back_chef_4) | 106 | `p28/back/act` → `p28/back/act_6` [menu 106] → `p28/back/buy_6_2` |
| 1140 | 16 Bottles o' Enchanting 2 Tokens | Prof. Whiskerton - Back Room (dialog p28/back_professor_1); Prof. Whiskerton - Back Room (dialog p28/back_professor_2); Prof. Whiskerton - Back Room (dialog p28/back_professor_3) (+1 more) | 107 | `p28/back/act` → `p28/back/act_7` [menu 107] → `p28/back/buy_7_0` |
| 1141 | Book of Mending 2 Medallions | Prof. Whiskerton - Back Room (dialog p28/back_professor_2); Prof. Whiskerton - Back Room (dialog p28/back_professor_3); Prof. Whiskerton - Back Room (dialog p28/back_professor_4) | 107 | `p28/back/act` → `p28/back/act_7` [menu 107] → `p28/back/buy_7_1` |
| 1142 | Auroral Crown 1 Trophy | Prof. Whiskerton - Back Room (dialog p28/back_professor_4) | 107 | `p28/back/act` → `p28/back/act_7` [menu 107] → `p28/back/buy_7_2` |
| 1160 | Jackpot Scratch Card 2 Lucky Tokens | Lucky Whiskers - Back Room (dialog p28/back_lucky_1); Lucky Whiskers - Back Room (dialog p28/back_lucky_2); Lucky Whiskers - Back Room (dialog p28/back_lucky_3) (+1 more) | 108 | `p28/back/act` → `p28/back/act_8` [menu 108] → `p28/back/buy_8_0` |
| 1161 | Heartstone 9 Lucky Tokens | Lucky Whiskers - Back Room (dialog p28/back_lucky_2); Lucky Whiskers - Back Room (dialog p28/back_lucky_3); Lucky Whiskers - Back Room (dialog p28/back_lucky_4) | 108 | `p28/back/act` → `p28/back/act_8` [menu 108] → `p28/back/buy_8_1` |
| 1162 | Bloomwalker Boots 1 Trophy | Lucky Whiskers - Back Room (dialog p28/back_lucky_4) | 108 | `p28/back/act` → `p28/back/act_8` [menu 108] → `p28/back/buy_8_2` |
| 1180 | Buried Treasure Map 2 Tokens | Capt. Cheddarbeard - Back Room (dialog p28/back_captain_1); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_2); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_3) (+1 more) | 109 | `p28/back/act` → `p28/back/act_9` [menu 109] → `p28/back/buy_9_0` |
| 1181 | Heart of the Sea 2 Medallions | Capt. Cheddarbeard - Back Room (dialog p28/back_captain_2); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_3); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_4) | 109 | `p28/back/act` → `p28/back/act_9` [menu 109] → `p28/back/buy_9_1` |
| 1182 | Rat Familiar 1 Trophy | Capt. Cheddarbeard - Back Room (dialog p28/back_captain_4) | 109 | `p28/back/act` → `p28/back/act_9` [menu 109] → `p28/back/buy_9_2` |
| 1200 | Ominous Bottle 4 Blood Moon Crystals | The Bloodbroker - Back Room (dialog p28/back_blood_1); The Bloodbroker - Back Room (dialog p28/back_blood_2); The Bloodbroker - Back Room (dialog p28/back_blood_3) (+1 more) | 110 | `p28/back/act` → `p28/back/act_10` [menu 110] → `p28/back/buy_10_0` |
| 1201 | Nether Star 14 Blood Moon Crystals | The Bloodbroker - Back Room (dialog p28/back_blood_2); The Bloodbroker - Back Room (dialog p28/back_blood_3); The Bloodbroker - Back Room (dialog p28/back_blood_4) | 110 | `p28/back/act` → `p28/back/act_10` [menu 110] → `p28/back/buy_10_1` |
| 1202 | 3 Heartstones 1 Trophy | The Bloodbroker - Back Room (dialog p28/back_blood_4) | 110 | `p28/back/act` → `p28/back/act_10` [menu 110] → `p28/back/buy_10_2` |
| 2001 | Buy a one-night pass 1 Medallion | The Dark Auction (dialog p28/pass) | 201 | `p28/gate/act` [menu 201] → `p28/gate/buy_pass` |
| 2110 | 32 Coal → 1 Token $(q0)/5 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot0` |
| 2111 | 32 Raw Copper → 1 Token $(q1)/5 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot1` |
| 2112 | 24 Raw Iron → 1 Token $(q2)/5 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot2` |
| 2113 | 16 Raw Gold → 1 Token $(q3)/4 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot3` |
| 2114 | 48 Redstone Dust → 1 Token $(q4)/4 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot4` |
| 2115 | 32 Lapis Lazuli → 1 Token $(q5)/4 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot5` |
| 2116 | 32 Nether Quartz → 1 Token $(q6)/4 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot6` |
| 2117 | 32 Amethyst Shards → 1 Token $(q7)/3 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot7` |
| 2118 | Diamond → 2 Tokens $(q8)/8 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot8` |
| 2119 | 2 Ancient Debris → 1 Token $(q9)/4 | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p162/dw/lot9` |
| 2140 | Buy the Ore Magnet 16 Tokens | DENNIS'S ASSAY OFFICE (p162/dw/pg2100_dlg) | 2100 | `p162/dw/act` [menu 2100] → `p174/col/buy_ore` |
| 2151 | « Common lots | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/pg2151` |
| 2152 | Rare parts » | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/pg2152` |
| 2160 | 32 Rotten Flesh → 1 Token $(q0)/5 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot0` |
| 2161 | 32 Bones → 1 Token $(q1)/5 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot1` |
| 2162 | 32 String → 1 Token $(q2)/5 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot2` |
| 2163 | 16 Spider Eyes → 1 Token $(q3)/4 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot3` |
| 2164 | 24 Gunpowder → 1 Token $(q4)/4 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot4` |
| 2165 | 16 Slimeballs → 1 Token $(q5)/4 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot5` |
| 2166 | 16 Leather → 1 Token $(q6)/4 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot6` |
| 2167 | 32 Feathers → 1 Token $(q7)/4 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot7` |
| 2168 | 24 Ink Sacs → 1 Token $(q8)/3 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot8` |
| 2169 | 8 Ender Pearls → 1 Token $(q9)/3 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot9` |
| 2170 | 8 Blaze Rods → 1 Token $(q10)/3 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot10` |
| 2171 | 12 Magma Cream → 1 Token $(q11)/3 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot11` |
| 2172 | 8 Phantom Membranes → 1 Token $(q12)/3 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot12` |
| 2173 | 24 Prismarine Shards → 1 Token $(q13)/3 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot13` |
| 2174 | 8 Breeze Rods → 1 Token $(q14)/3 | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot14` |
| 2175 | Wither Skeleton Skull → 5 Tokens $(q15)/3 | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot15` |
| 2176 | Zombie Head → 3 Tokens $(q16)/2 | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot16` |
| 2177 | Skeleton Skull → 3 Tokens $(q17)/2 | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot17` |
| 2178 | Creeper Head → 3 Tokens $(q18)/2 | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot18` |
| 2179 | Shulker Shell → 1 Token $(q19)/2 | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot19` |
| 2180 | 2 Rabbit's Feet → 1 Token $(q20)/2 | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot20` |
| 2181 | 2 Ghast Tears → 1 Token $(q21)/3 | PISTACHIO'S PANTRY · rare parts (p162/ps/pg2152_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p162/ps/lot21` |
| 2190 | Buy the Spirit Jar 16 Tokens | PISTACHIO'S PANTRY (p162/ps/pg2151_dlg) | 2150 | `p162/ps/act` [menu 2150] → `p174/col/buy_mob` |
| 2201 | Sit / follow | Dennis's Horn (p163/dw/menu) | 2200 | `p163/dw/act` [menu 2200] → `p163/dw/sit` (if if entity @e[type=minecraft:wolf,tag=bm.dwsel2]) |
| 2202 | Wardrobe | Dennis's Horn (p163/dw/menu) | 2200 | `p163/dw/act` [menu 2200] → `p119/plain/dennis` |
| 2204 | Dennis's ways | Dennis's Horn (p163/dw/menu) | 2200 | `p163/dw/act` [menu 2200] → `p163/dw/powers` |
| 2205 | « Back | DENNIS'S WAYS (p163/dw/powers) | 2200 | `p163/dw/act` [menu 2200] → `p163/dw/menu` |
| 2208 | Call for Dennis | Dennis's Horn (p163/dw/menu) | 2200 | `p163/dw/act` [menu 2200] → `p163/dw/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.dwsel2]) / `p163/dw/act` [menu 2200] → `p163/dw/recall` (if if entity @e[type=minecraft:wolf,tag=bm.dwsel2]) |
| 2209 | Send him home | Dennis's Horn (p163/dw/menu) | 2200 | `p163/dw/act` [menu 2200] → `p163/dw/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.dwsel2]) |
| 2221 | Sit / follow | Pistachio's Little Cloche (p163/pi/menu) | 2220 | `p163/pi/act` [menu 2220] → `p163/pi/sit` (if if entity @e[type=minecraft:wolf,tag=bm.pisel2]) |
| 2222 | Wardrobe | Pistachio's Little Cloche (p163/pi/menu) | 2220 | `p163/pi/act` [menu 2220] → `p119/plain/pistachio` |
| 2224 | Pistachio's ways | Pistachio's Little Cloche (p163/pi/menu) | 2220 | `p163/pi/act` [menu 2220] → `p163/pi/powers` |
| 2225 | « Back | PISTACHIO'S WAYS (p163/pi/powers) | 2220 | `p163/pi/act` [menu 2220] → `p163/pi/menu` |
| 2228 | Call for Pistachio | Pistachio's Little Cloche (p163/pi/menu) | 2220 | `p163/pi/act` [menu 2220] → `p163/pi/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.pisel2]) / `p163/pi/act` [menu 2220] → `p163/pi/recall` (if if entity @e[type=minecraft:wolf,tag=bm.pisel2]) |
| 2229 | Send him home | Pistachio's Little Cloche (p163/pi/menu) | 2220 | `p163/pi/act` [menu 2220] → `p163/pi/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.pisel2]) |
| 2240 | « Outfits & buffs / $(r_home) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/dennis` [menu 2240] → `p125/hc/dennis` |
| 2242 | His old black leather $(r_dennis0) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p99/pick/dennis0` |
| 2243 | Road Brown $(r_dennis1) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p99/pick/dennis1` |
| 2244 | Biker Red $(r_dennis2) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p99/pick/dennis2` |
| 2245 | Forest Leather $(r_dennis3) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p99/pick/dennis3` |
| 2246 | Gilded Jacket $(r_dennis4) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p99/pick/dennis4` |
| 2247 | Diamond Jacket $(r_dennis5) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p99/pick/dennis5` |
| 2248 | Netherite Jacket $(r_dennis6) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p99/pick/dennis6` |
| 2258 | Pixel costume $(r_px) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p214/t/dennis` |
| 2259 | Gold Rush Glimmer $(r_aura) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p99/act/dennis` [menu 2240] → `p138/au/t_dennis` |
| 2260 | « Outfits & buffs / $(r_home) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/pistachio` [menu 2260] → `p125/hc/pistachio` |
| 2262 | His charcoal tails $(r_pistachio0) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p99/pick/pistachio0` |
| 2263 | Midnight Tails $(r_pistachio1) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p99/pick/pistachio1` |
| 2264 | Claret Tails $(r_pistachio2) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p99/pick/pistachio2` |
| 2265 | Ivory Tails $(r_pistachio3) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p99/pick/pistachio3` |
| 2266 | Gilded Tails $(r_pistachio4) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p99/pick/pistachio4` |
| 2267 | Diamond Tails $(r_pistachio5) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p99/pick/pistachio5` |
| 2268 | Netherite Tails $(r_pistachio6) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p99/pick/pistachio6` |
| 2278 | Pixel costume $(r_px) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p214/t/pistachio` |
| 2279 | Ectoplasmic Mist $(r_aura) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p99/act/pistachio` [menu 2260] → `p138/au/t_pistachio` |
| 2281 | Sit / follow | Omega's Monocle (p170/menu_out) | 2280 | `p170/act` [menu 2280] → `p170/sit` (if if entity @e[type=minecraft:wolf,tag=bm.omsel2]) |
| 2282 | Wardrobe | Omega's Monocle (p170/menu); Omega's Monocle (p170/menu_out) | 2280 | `p170/act` [menu 2280] → `p119/plain/omega` |
| 2284 | King Omega's ways | Omega's Monocle (p170/menu); Omega's Monocle (p170/menu_out) | 2280 | `p170/act` [menu 2280] → `p170/powers` |
| 2285 | « Back | KING OMEGA'S WAYS (p170/powers) | 2280 | `p170/act` [menu 2280] → `p170/menu` |
| 2288 | Call for Omega | Omega's Monocle (p170/menu) | 2280 | `p170/act` [menu 2280] → `p170/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.omsel2]) / `p170/act` [menu 2280] → `p170/recall` (if if entity @e[type=minecraft:wolf,tag=bm.omsel2]) |
| 2289 | Send him home | Omega's Monocle (p170/menu_out) | 2280 | `p170/act` [menu 2280] → `p170/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.omsel2]) |
| 2300 | « Outfits & buffs / $(r_home) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/omega` [menu 2300] → `p125/hc/omega` |
| 2302 | His own grey ghost $(r_omega0) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p99/pick/omega0` |
| 2303 | Spectral Blue $(r_omega1) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p99/pick/omega1` |
| 2304 | Blood Moon $(r_omega2) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p99/pick/omega2` |
| 2305 | Verdant Wraith $(r_omega3) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p99/pick/omega3` |
| 2306 | Gilded King $(r_omega4) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p99/pick/omega4` |
| 2307 | Diamond King $(r_omega5) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p99/pick/omega5` |
| 2308 | Netherite King $(r_omega6) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p99/pick/omega6` |
| 2318 | Pixel costume $(r_px) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p214/t/omega` |
| 2319 | Court of Souls $(r_aura) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p99/act/omega` [menu 2300] → `p138/au/t_omega` |
| 2321 | The Peerage | KING OMEGA (p169/court/main_show) | 2320 | `p169/court/act` [menu 2320] → `p169/court/peer` |
| 2322 | The Ghost Garrison | KING OMEGA (p169/court/main_show) | 2320 | `p169/court/act` [menu 2320] → `p169/court/garr` |
| 2323 | Offer a gift | KING OMEGA (p169/court/main_show) | 2320 | `p169/court/act` [menu 2320] → `p169/court/gift` |
| 2324 | The Chronicle | KING OMEGA (p169/court/main_show) | 2320 | `p169/court/act` [menu 2320] → `p169/court/chron` |
| 2325 | My title on / off | KING OMEGA (p169/court/main_show) | 2320 | `p169/court/act` [menu 2320] → `p169/court/title` |
| 2326 | Re-challenge the King | KING OMEGA (p169/court/main_show) | 2320 | `p169/court/act` [menu 2320] → `p169/court/rematch` |
| 2329 | « Back | THE GHOST GARRISON (p169/court/garr); THE PEERAGE (p169/court/peer_show); p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/main` |
| 2331 | Tithe 4 Tokens +10 | THE PEERAGE (p169/court/peer_show) | 2320 | `p169/court/act` [menu 2320] → `p169/court/tithe` |
| 2332 | Offer your Court's souls | THE PEERAGE (p169/court/peer_show) | 2320 | `p169/court/act` [menu 2320] → `p170/tithe_souls` |
| 2341 | Buy a Soul Brazier 8 Tokens | THE GHOST GARRISON (p169/court/garr) | 2320 | `p169/court/act` [menu 2320] → `p169/court/buy` |
| 2350 | I. Two Eggs in the Sun | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read0` |
| 2351 | II. The Monocle | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read1` |
| 2352 | III. The Feast of Crowns | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read2` |
| 2353 | IV. The Library of Small Things | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read3` |
| 2354 | V. The Light to Lead Them | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read4` |
| 2355 | VI. The War of Brothers | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read5` |
| 2356 | VII. The Last Night | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read6` |
| 2357 | VIII. The Long Quiet | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read7` |
| 2358 | IX. The Butler and the Boy | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read8` |
| 2359 | X. What the Dead King Wants | p169/court/chron | 2320 | `p169/court/act` [menu 2320] → `p169/court/read9` |
| 2361 | Call him over | Wilfrey's Locket (p173/wil/menu_out) | 2360 | `p173/wil/act` [menu 2360] → `p2/wil/recall` (if if entity @e[type=minecraft:wolf,tag=bm.fsel]) |
| 2362 | Send him home | Wilfrey's Locket (p173/wil/menu_out) | 2360 | `p173/wil/act` [menu 2360] → `p2/wil/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.fsel]) |
| 2363 | Wardrobe | Wilfrey's Locket (p173/wil/menu_in); Wilfrey's Locket (p173/wil/menu_out) | 2360 | `p173/wil/act` [menu 2360] → `p119/plain/wil` |
| 2364 | Call Wilfrey | Wilfrey's Locket (p173/wil/menu_in) | 2360 | `p173/wil/act` [menu 2360] → `p2/wil/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.fsel]) / `p173/wil/act` [menu 2360] → `p2/wil/recall` (if if entity @e[type=minecraft:wolf,tag=bm.fsel]) |
| 2370 | Back after a faint $(r_ar) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p173/ar/act` → `p173/ar/t_0` [menu 9880] |
| 2371 | Back after a faint $(r_ar) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p173/ar/act` → `p173/ar/t_1` [menu 9800] |
| 2372 | Back after a faint $(r_ar) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p173/ar/act` → `p173/ar/t_2` [menu 9840] |
| 2373 | Back after a faint $(r_ar) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p173/ar/act` → `p173/ar/t_3` [menu 9860] |
| 2374 | Back after a faint $(r_ar) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p173/ar/act` → `p173/ar/t_4` [menu 9900] |
| 2375 | Back after a faint $(r_ar) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p173/ar/act` → `p173/ar/t_5` [menu 9920] |
| 2376 | Back after a faint $(r_ar) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p173/ar/act` → `p173/ar/t_6` [menu 9940] |
| 2377 | Back after a faint $(r_ar) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p173/ar/act` → `p173/ar/t_7` [menu 9000] |
| 2378 | Back after a faint $(r_ar) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p173/ar/act` → `p173/ar/t_8` [menu 9020] |
| 2379 | Back after a faint $(r_ar) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p173/ar/act` → `p173/ar/t_9` [menu 9040] |
| 2380 | Back after a faint $(r_ar) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p173/ar/act` → `p173/ar/t_10` [menu 9060] |
| 2381 | Back after a faint $(r_ar) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p173/ar/act` → `p173/ar/t_11` [menu 9100] |
| 2382 | Back after a faint $(r_ar) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p173/ar/act` → `p173/ar/t_12` [menu 9120] |
| 2383 | Back after a faint $(r_ar) | Dennis · wardrobe (p119/dlg/dennis); Dennis · wardrobe (p99/dlg/dennis) | 2240 | `p173/ar/act` → `p173/ar/t_13` [menu 2240] |
| 2384 | Back after a faint $(r_ar) | Pistachio · wardrobe (p119/dlg/pistachio); Pistachio · wardrobe (p99/dlg/pistachio) | 2260 | `p173/ar/act` → `p173/ar/t_14` [menu 2260] |
| 2385 | Back after a faint $(r_ar) | King Omega · wardrobe (p119/dlg/omega); King Omega · wardrobe (p99/dlg/omega) | 2300 | `p173/ar/act` → `p173/ar/t_15` [menu 2300] |
| 2386 | Back after a faint $(r_ar) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p173/ar/act` → `p173/ar/t_16` [menu 2460] |
| 2387 | Back after a faint $(r_ar) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p173/ar/act` → `p173/ar/t_17` [menu 2520] |
| 2388 | Back after a faint $(r_ar) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p173/ar/act` → `p173/ar/t_18` [menu 2560] |
| 2389 | Back after a faint $(r_ar) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p173/ar/act` → `p173/ar/t_19` [menu 2640] |
| 2390 | Back after a faint $(r_ar) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p173/ar/act` → `p173/ar/t_20` [menu 2660] |
| 2391 | Back after a faint $(r_ar) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p173/ar/act` → `p173/ar/t_21` [menu 2680] |
| 2392 | Back after a faint $(r_ar) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p173/ar/act` → `p173/ar/t_22` [menu 2720] |
| 2393 | Back after a faint $(r_ar) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p173/ar/act` → `p173/ar/t_23` [menu 2760] |
| 2394 | Back after a faint $(r_ar) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p173/ar/act` → `p173/ar/t_24` [menu 2800] |
| 2395 | Back after a faint $(r_ar) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p173/ar/act` → `p173/ar/t_25` [menu 2840] |
| 2396 | Back after a faint $(r_ar) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p173/ar/act` → `p173/ar/t_26` [menu 2880] |
| 2397 | Back after a faint $(r_ar) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p173/ar/act` → `p173/ar/t_27` [menu 3040] |
| 2398 | Back after a faint $(r_ar) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p173/ar/act` → `p173/ar/t_28` [menu 3000] |
| 2399 | Back after a faint $(r_ar) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p173/ar/act` → `p173/ar/t_29` [menu 2960] |
| 2400 | Back after a faint $(r_ar) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p173/ar/act` → `p173/ar/t_30` [menu 2900] |
| 2401 | Old Barnaby | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2402 | Prof. Whiskerton | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2403 | Madame Velour | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2404 | The Fence | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2405 | Dark Auction gate | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2406 | Gilded Gutter gate | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2407 | Scrap Bin | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2408 | Bounty Board | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2409 | Mike's pond | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2410 | Vinny 'Two-Blades' | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2411 | Steelwhisker | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2412 | Fishy's Cabinet | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2413 | Chef Fromage | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2414 | Cecil | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2415 | The Bloodbroker | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2416 | Lucky Whiskers | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2417 | The dock house | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2418 | Dennis | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2419 | Pistachio | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2420 | Newcomers' Book | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2421 | The way out | WHO'S WHERE · the rat town (p171/open) | 2400 | `p171/act` [menu 2400] |
| 2441 | Sit / follow | Ashur's Cinder (p185/menu_out) | 2440 | `p185/act` [menu 2440] → `p185/sit` (if if entity @e[type=minecraft:wolf,tag=bm.assel2]) |
| 2442 | Wardrobe | Ashur's Cinder (p185/menu); Ashur's Cinder (p185/menu_out) | 2440 | `p185/act` [menu 2440] → `p119/plain/ashur` |
| 2444 | Ashur's ways | Ashur's Cinder (p185/menu); Ashur's Cinder (p185/menu_out) | 2440 | `p185/act` [menu 2440] → `p185/powers` |
| 2445 | « Back | ASHUR'S WAYS (p185/powers) | 2440 | `p185/act` [menu 2440] → `p185/menu` |
| 2448 | Call for Ashur | Ashur's Cinder (p185/menu) | 2440 | `p185/act` [menu 2440] → `p185/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.assel2]) / `p185/act` [menu 2440] → `p185/recall` (if if entity @e[type=minecraft:wolf,tag=bm.assel2]) |
| 2449 | Send her home | Ashur's Cinder (p185/menu_out) | 2440 | `p185/act` [menu 2440] → `p185/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.assel2]) |
| 2460 | « Outfits & buffs / $(r_home) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/ashur` [menu 2460] → `p125/hc/ashur` |
| 2462 | Her own magma $(r_ashur0) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p99/pick/ashur0` |
| 2463 | Blue Flame $(r_ashur1) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p99/pick/ashur1` |
| 2464 | Verdant Ember $(r_ashur2) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p99/pick/ashur2` |
| 2465 | Obsidian Rose $(r_ashur3) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p99/pick/ashur3` |
| 2466 | Gilded Magma $(r_ashur4) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p99/pick/ashur4` |
| 2467 | Diamond Magma $(r_ashur5) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p99/pick/ashur5` |
| 2468 | Netherite Magma $(r_ashur6) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p99/pick/ashur6` |
| 2478 | Pixel costume $(r_px) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p214/t/ashur` |
| 2479 | Ashfall Crown $(r_aura) | Ashur · wardrobe (p119/dlg/ashur); Ashur · wardrobe (p99/dlg/ashur) | 2460 | `p99/act/ashur` [menu 2460] → `p138/au/t_ashur` |
| 2501 | Sit / follow | The Golden Ladle (p186/menu_out) | 2500 | `p186/act` [menu 2500] → `p186/sit` (if if entity @e[type=minecraft:wolf,tag=bm.kksel2]) |
| 2502 | Wardrobe | The Golden Ladle (p186/menu_in); The Golden Ladle (p186/menu_out) | 2500 | `p186/act` [menu 2500] → `p119/plain/chef` |
| 2504 | The Chef's ways | The Golden Ladle (p186/menu_in); The Golden Ladle (p186/menu_out) | 2500 | `p186/act` [menu 2500] → `p186/powers` |
| 2505 | « Back | THE CHEF'S WAYS (p186/powers) | 2500 | `p186/act` [menu 2500] → `p186/menu` |
| 2508 | Call for The Chef | The Golden Ladle (p186/menu_in) | 2500 | `p186/act` [menu 2500] → `p186/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.kksel2]) / `p186/act` [menu 2500] → `p186/recall` (if if entity @e[type=minecraft:wolf,tag=bm.kksel2]) |
| 2509 | Send him home | The Golden Ladle (p186/menu_out) | 2500 | `p186/act` [menu 2500] → `p186/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.kksel2]) |
| 2520 | « Outfits & buffs / $(r_home) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/chef` [menu 2520] → `p125/hc/chef` |
| 2522 | His spotless whites $(r_chef0) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p99/pick/chef0` |
| 2523 | Midnight Brigade $(r_chef1) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p99/pick/chef1` |
| 2524 | Bistro Blue $(r_chef2) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p99/pick/chef2` |
| 2525 | Sommelier Wine $(r_chef3) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p99/pick/chef3` |
| 2526 | Gilded Whites $(r_chef4) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p99/pick/chef4` |
| 2527 | Diamond Whites $(r_chef5) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p99/pick/chef5` |
| 2528 | Netherite Whites $(r_chef6) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p99/pick/chef6` |
| 2538 | Pixel costume $(r_px) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p214/t/chef` |
| 2539 | Kitchen Steam $(r_aura) | the Chef · wardrobe (p119/dlg/chef); the Chef · wardrobe (p99/dlg/chef) | 2520 | `p99/act/chef` [menu 2520] → `p138/au/t_chef` |
| 2541 | Sit / follow | The Neighbor's Baton (p187/menu) | 2540 | `p187/act` [menu 2540] → `p187/sit` (if if entity @e[type=minecraft:wolf,tag=bm.nbsel2]) |
| 2542 | Wardrobe | The Neighbor's Baton (p187/menu) | 2540 | `p187/act` [menu 2540] → `p119/plain/neighbor` |
| 2544 | The Neighbor's ways | The Neighbor's Baton (p187/menu) | 2540 | `p187/act` [menu 2540] → `p187/powers` |
| 2545 | « Back | THE NEIGHBOR'S WAYS (p187/powers) | 2540 | `p187/act` [menu 2540] → `p187/menu` |
| 2548 | Call for The Neighbor | The Neighbor's Baton (p187/menu) | 2540 | `p187/act` [menu 2540] → `p187/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.nbsel2]) / `p187/act` [menu 2540] → `p187/recall` (if if entity @e[type=minecraft:wolf,tag=bm.nbsel2]) |
| 2549 | Send him home | The Neighbor's Baton (p187/menu) | 2540 | `p187/act` [menu 2540] → `p187/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.nbsel2]) |
| 2560 | « Outfits & buffs / $(r_home) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/neighbor` [menu 2560] → `p125/hc/neighbor` |
| 2562 | His sailor whites $(r_neighbor0) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p99/pick/neighbor0` |
| 2563 | Navy Bandmaster $(r_neighbor1) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p99/pick/neighbor1` |
| 2564 | Encore Crimson $(r_neighbor2) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p99/pick/neighbor2` |
| 2565 | Jazz Violet $(r_neighbor3) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p99/pick/neighbor3` |
| 2566 | Gilded Suit $(r_neighbor4) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p99/pick/neighbor4` |
| 2567 | Diamond Suit $(r_neighbor5) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p99/pick/neighbor5` |
| 2568 | Netherite Suit $(r_neighbor6) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p99/pick/neighbor6` |
| 2578 | Pixel costume $(r_px) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p214/t/neighbor` |
| 2579 | Grand Symphony $(r_aura) | the Neighbor · wardrobe (p119/dlg/neighbor); the Neighbor · wardrobe (p99/dlg/neighbor) | 2560 | `p99/act/neighbor` [menu 2560] → `p138/au/t_neighbor` |
| 2581 | Sit / follow | Queen Ava's Locket (p189/menu) | 2580 | `p189/act` [menu 2580] → `p189/sit` (if if entity @e[type=minecraft:wolf,tag=bm.avsel2]) |
| 2582 | Wardrobe | Queen Ava's Locket (p189/menu) | 2580 | `p189/act` [menu 2580] → `p119/plain/ava` |
| 2583 | Living / ghostly form | Queen Ava's Locket (p189/menu) | 2580 | `p189/act` [menu 2580] → `p189/form` |
| 2584 | Queen Ava's ways | Queen Ava's Locket (p189/menu) | 2580 | `p189/act` [menu 2580] → `p189/powers` |
| 2585 | « Back | QUEEN AVA'S STORY (p189/story); QUEEN AVA'S WAYS (p189/powers) | 2580 | `p189/act` [menu 2580] → `p189/menu` |
| 2586 | Her story | Queen Ava's Locket (p189/menu) | 2580 | `p189/act` [menu 2580] → `p189/story` |
| 2588 | Call for Queen Ava | Queen Ava's Locket (p189/menu) | 2580 | `p189/act` [menu 2580] → `p189/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.avsel2]) / `p189/act` [menu 2580] → `p189/recall` (if if entity @e[type=minecraft:wolf,tag=bm.avsel2]) |
| 2589 | Send her home | Queen Ava's Locket (p189/menu) | 2580 | `p189/act` [menu 2580] → `p189/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.avsel2]) |
| 2601 | Sit / follow | Queen Pearl's Pearls (p190/menu) | 2600 | `p190/act` [menu 2600] → `p190/sit` (if if entity @e[type=minecraft:wolf,tag=bm.pqsel2]) |
| 2602 | Wardrobe | Queen Pearl's Pearls (p190/menu) | 2600 | `p190/act` [menu 2600] → `p119/plain/pearlq` |
| 2603 | Casual / regal outfit | Queen Pearl's Pearls (p190/menu) | 2600 | `p190/act` [menu 2600] → `p190/form` |
| 2604 | Queen Pearl's ways | Queen Pearl's Pearls (p190/menu) | 2600 | `p190/act` [menu 2600] → `p190/powers` |
| 2605 | « Back | QUEEN PEARL'S STORY (p190/story); QUEEN PEARL'S WAYS (p190/powers) | 2600 | `p190/act` [menu 2600] → `p190/menu` |
| 2606 | Her story | Queen Pearl's Pearls (p190/menu) | 2600 | `p190/act` [menu 2600] → `p190/story` |
| 2608 | Call for Queen Pearl | Queen Pearl's Pearls (p190/menu) | 2600 | `p190/act` [menu 2600] → `p190/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.pqsel2]) / `p190/act` [menu 2600] → `p190/recall` (if if entity @e[type=minecraft:wolf,tag=bm.pqsel2]) |
| 2609 | Send her home | Queen Pearl's Pearls (p190/menu) | 2600 | `p190/act` [menu 2600] → `p190/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.pqsel2]) |
| 2621 | Sit / follow | Bloo's Claw (p191/menu) | 2620 | `p191/act` [menu 2620] → `p191/sit` (if if entity @e[type=minecraft:wolf,tag=bm.bosel2]) |
| 2622 | Wardrobe | Bloo's Claw (p191/menu) | 2620 | `p191/act` [menu 2620] → `p119/plain/bloo` |
| 2624 | Bloo's ways | Bloo's Claw (p191/menu) | 2620 | `p191/act` [menu 2620] → `p191/powers` |
| 2625 | « Back | BLOO'S STORY (p191/story); BLOO'S WAYS (p191/powers) | 2620 | `p191/act` [menu 2620] → `p191/menu` |
| 2626 | His story | Bloo's Claw (p191/menu) | 2620 | `p191/act` [menu 2620] → `p191/story` |
| 2628 | Call for Bloo | Bloo's Claw (p191/menu) | 2620 | `p191/act` [menu 2620] → `p191/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.bosel2]) / `p191/act` [menu 2620] → `p191/recall` (if if entity @e[type=minecraft:wolf,tag=bm.bosel2]) |
| 2629 | Send him home | Bloo's Claw (p191/menu) | 2620 | `p191/act` [menu 2620] → `p191/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.bosel2]) |
| 2640 | « Outfits & buffs / $(r_home) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/ava` [menu 2640] → `p125/hc/ava` |
| 2642 | Her royal blue $(r_ava0) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p99/pick/ava0` |
| 2643 | Coral Reef $(r_ava1) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p99/pick/ava1` |
| 2644 | Abyssal Violet $(r_ava2) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p99/pick/ava2` |
| 2645 | Kelp Forest $(r_ava3) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p99/pick/ava3` |
| 2646 | Gilded Gown $(r_ava4) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p99/pick/ava4` |
| 2647 | Diamond Gown $(r_ava5) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p99/pick/ava5` |
| 2648 | Netherite Gown $(r_ava6) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p99/pick/ava6` |
| 2658 | Pixel costume $(r_px) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p214/t/ava` |
| 2659 | Crown of the Deep $(r_aura) | Queen Ava · wardrobe (p119/dlg/ava); Queen Ava · wardrobe (p99/dlg/ava) | 2640 | `p99/act/ava` [menu 2640] → `p138/au/t_ava` |
| 2660 | « Outfits & buffs / $(r_home) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/pearlq` [menu 2660] → `p125/hc/pearlq` |
| 2662 | Her own aqua $(r_pearlq0) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p99/pick/pearlq0` |
| 2663 | Coral Pink $(r_pearlq1) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p99/pick/pearlq1` |
| 2664 | Sunset Gold $(r_pearlq2) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p99/pick/pearlq2` |
| 2665 | Starlit Navy $(r_pearlq3) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p99/pick/pearlq3` |
| 2666 | Gilded Dress $(r_pearlq4) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p99/pick/pearlq4` |
| 2667 | Diamond Dress $(r_pearlq5) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p99/pick/pearlq5` |
| 2668 | Netherite Dress $(r_pearlq6) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p99/pick/pearlq6` |
| 2678 | Pixel costume $(r_px) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p214/t/pearlq` |
| 2679 | Pearlescent Tide $(r_aura) | Queen Pearl · wardrobe (p119/dlg/pearlq); Queen Pearl · wardrobe (p99/dlg/pearlq) | 2660 | `p99/act/pearlq` [menu 2660] → `p138/au/t_pearlq` |
| 2680 | « Outfits & buffs / $(r_home) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/bloo` [menu 2680] → `p125/hc/bloo` |
| 2682 | His own wild blue $(r_bloo0) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p99/pick/bloo0` |
| 2683 | Shadow Pelt $(r_bloo1) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p99/pick/bloo1` |
| 2684 | Ember Mane $(r_bloo2) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p99/pick/bloo2` |
| 2685 | Frost Coat $(r_bloo3) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p99/pick/bloo3` |
| 2686 | Gilded Fur $(r_bloo4) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p99/pick/bloo4` |
| 2687 | Diamond Fur $(r_bloo5) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p99/pick/bloo5` |
| 2688 | Netherite Fur $(r_bloo6) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p99/pick/bloo6` |
| 2698 | Pixel costume $(r_px) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p214/t/bloo` |
| 2699 | Feral Moon $(r_aura) | Bloo · wardrobe (p119/dlg/bloo); Bloo · wardrobe (p99/dlg/bloo) | 2680 | `p99/act/bloo` [menu 2680] → `p138/au/t_bloo` |
| 2701 | Sit / follow | The Hollow Hook (p193/menu) | 2700 | `p193/act` [menu 2700] → `p193/sit` (if if entity @e[type=minecraft:wolf,tag=bm.svsel2]) |
| 2702 | Wardrobe | The Hollow Hook (p193/menu) | 2700 | `p193/act` [menu 2700] → `p119/plain/stalker` |
| 2704 | The Stalker's ways | The Hollow Hook (p193/menu) | 2700 | `p193/act` [menu 2700] → `p193/powers` |
| 2705 | « Back | THE STALKER'S WAYS (p193/powers) | 2700 | `p193/act` [menu 2700] → `p193/menu` |
| 2708 | Call for The Stalker | The Hollow Hook (p193/menu) | 2700 | `p193/act` [menu 2700] → `p193/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.svsel2]) / `p193/act` [menu 2700] → `p193/recall` (if if entity @e[type=minecraft:wolf,tag=bm.svsel2]) |
| 2709 | Send it home | The Hollow Hook (p193/menu) | 2700 | `p193/act` [menu 2700] → `p193/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.svsel2]) |
| 2720 | « Outfits & buffs / $(r_home) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/stalker` [menu 2720] → `p125/hc/stalker` |
| 2722 | Its own sickly olive $(r_stalker0) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p99/pick/stalker0` |
| 2723 | Bone White $(r_stalker1) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p99/pick/stalker1` |
| 2724 | Ashen Grey $(r_stalker2) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p99/pick/stalker2` |
| 2725 | Blood Moon $(r_stalker3) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p99/pick/stalker3` |
| 2726 | Gilded Skin $(r_stalker4) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p99/pick/stalker4` |
| 2727 | Diamond Skin $(r_stalker5) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p99/pick/stalker5` |
| 2728 | Netherite Skin $(r_stalker6) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p99/pick/stalker6` |
| 2738 | Pixel costume $(r_px) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p214/t/stalker` |
| 2739 | The Long Night $(r_aura) | The Stalker · wardrobe (p119/dlg/stalker); The Stalker · wardrobe (p99/dlg/stalker) | 2720 | `p99/act/stalker` [menu 2720] → `p138/au/t_stalker` |
| 2741 | Sit / follow | Kindled Gourd (p194/menu) | 2740 | `p194/act` [menu 2740] → `p194/sit` (if if entity @e[type=minecraft:wolf,tag=bm.lnsel2]) |
| 2742 | Wardrobe | Kindled Gourd (p194/menu) | 2740 | `p194/act` [menu 2740] → `p119/plain/lantern` |
| 2744 | The Arachno-Lantern's ways | Kindled Gourd (p194/menu) | 2740 | `p194/act` [menu 2740] → `p194/powers` |
| 2745 | « Back | THE ARACHNO-LANTERN'S WAYS (p194/powers) | 2740 | `p194/act` [menu 2740] → `p194/menu` |
| 2746 | Ride | Kindled Gourd (p194/menu) | 2740 | `p194/act` [menu 2740] → `p194/ride_ask` |
| 2748 | Call for The Arachno-Lantern | Kindled Gourd (p194/menu) | 2740 | `p194/act` [menu 2740] → `p194/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.lnsel2]) / `p194/act` [menu 2740] → `p194/recall` (if if entity @e[type=minecraft:wolf,tag=bm.lnsel2]) |
| 2749 | Send it home | Kindled Gourd (p194/menu) | 2740 | `p194/act` [menu 2740] → `p194/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.lnsel2]) |
| 2760 | « Outfits & buffs / $(r_home) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/lantern` [menu 2760] → `p125/hc/lantern` |
| 2762 | Its own pumpkin orange $(r_lantern0) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p99/pick/lantern0` |
| 2763 | Ghost Gourd $(r_lantern1) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p99/pick/lantern1` |
| 2764 | Soulfire Rind $(r_lantern2) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p99/pick/lantern2` |
| 2765 | Harvest Moon $(r_lantern3) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p99/pick/lantern3` |
| 2766 | Gilded Rind $(r_lantern4) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p99/pick/lantern4` |
| 2767 | Diamond Rind $(r_lantern5) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p99/pick/lantern5` |
| 2768 | Netherite Rind $(r_lantern6) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p99/pick/lantern6` |
| 2778 | Pixel costume $(r_px) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p214/t/lantern` |
| 2779 | Hallowfire $(r_aura) | The Arachno-Lantern · wardrobe (p119/dlg/lantern); The Arachno-Lantern · wardrobe (p99/dlg/lantern) | 2760 | `p99/act/lantern` [menu 2760] → `p138/au/t_lantern` |
| 2781 | Sit / follow | Bender's Ball (p195/menu) | 2780 | `p195/act` [menu 2780] → `p195/sit` (if if entity @e[type=minecraft:wolf,tag=bm.bvsel2]) |
| 2782 | Wardrobe | Bender's Ball (p195/menu) | 2780 | `p195/act` [menu 2780] → `p119/plain/bender` |
| 2784 | Bender's ways | Bender's Ball (p195/menu) | 2780 | `p195/act` [menu 2780] → `p195/powers` |
| 2785 | « Back | BENDER'S WAYS (p195/powers) | 2780 | `p195/act` [menu 2780] → `p195/menu` |
| 2786 | Dig! | Bender's Ball (p195/menu) | 2780 | `p195/act` [menu 2780] → `p195/dig_ask` |
| 2787 | Sniff out treasure | Bender's Ball (p195/menu) | 2780 | `p195/act` [menu 2780] → `p195/sniff_ask` |
| 2788 | Call for Bender | Bender's Ball (p195/menu) | 2780 | `p195/act` [menu 2780] → `p195/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.bvsel2]) / `p195/act` [menu 2780] → `p195/recall` (if if entity @e[type=minecraft:wolf,tag=bm.bvsel2]) |
| 2789 | Send him home | Bender's Ball (p195/menu) | 2780 | `p195/act` [menu 2780] → `p195/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.bvsel2]) |
| 2800 | « Outfits & buffs / $(r_home) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/bender` [menu 2800] → `p125/hc/bender` |
| 2802 | His own fawn $(r_bender0) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p99/pick/bender0` |
| 2803 | Midnight Black $(r_bender1) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p99/pick/bender1` |
| 2804 | Snow White $(r_bender2) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p99/pick/bender2` |
| 2805 | Sable $(r_bender3) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p99/pick/bender3` |
| 2806 | Gilded Coat $(r_bender4) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p99/pick/bender4` |
| 2807 | Diamond Coat $(r_bender5) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p99/pick/bender5` |
| 2808 | Netherite Coat $(r_bender6) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p99/pick/bender6` |
| 2818 | Pixel costume $(r_px) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p214/t/bender` |
| 2819 | Goodest Boy $(r_aura) | Bender · wardrobe (p119/dlg/bender); Bender · wardrobe (p99/dlg/bender) | 2800 | `p99/act/bender` [menu 2800] → `p138/au/t_bender` |
| 2821 | Sit / follow | Bones's Whistle (p196/menu) | 2820 | `p196/act` [menu 2820] → `p196/sit` (if if entity @e[type=minecraft:wolf,tag=bm.bjsel2]) |
| 2822 | Wardrobe | Bones's Whistle (p196/menu) | 2820 | `p196/act` [menu 2820] → `p119/plain/bones` |
| 2824 | Bones' ways | Bones's Whistle (p196/menu) | 2820 | `p196/act` [menu 2820] → `p196/powers` |
| 2825 | « Back | BONES' WAYS (p196/powers) | 2820 | `p196/act` [menu 2820] → `p196/menu` |
| 2826 | Ride | Bones's Whistle (p196/menu) | 2820 | `p196/act` [menu 2820] → `p196/ride_ask` |
| 2828 | Call for Bones | Bones's Whistle (p196/menu) | 2820 | `p196/act` [menu 2820] → `p196/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.bjsel2]) / `p196/act` [menu 2820] → `p196/recall` (if if entity @e[type=minecraft:wolf,tag=bm.bjsel2]) |
| 2829 | Send him home | Bones's Whistle (p196/menu) | 2820 | `p196/act` [menu 2820] → `p196/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.bjsel2]) |
| 2840 | « Outfits & buffs / $(r_home) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/bones` [menu 2840] → `p125/hc/bones` |
| 2842 | His own shark grey $(r_bones0) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p99/pick/bones0` |
| 2843 | Great White $(r_bones1) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p99/pick/bones1` |
| 2844 | Hammerhead Bronze $(r_bones2) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p99/pick/bones2` |
| 2845 | Abyss Black $(r_bones3) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p99/pick/bones3` |
| 2846 | Gilded Skin $(r_bones4) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p99/pick/bones4` |
| 2847 | Diamond Skin $(r_bones5) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p99/pick/bones5` |
| 2848 | Netherite Skin $(r_bones6) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p99/pick/bones6` |
| 2858 | Pixel costume $(r_px) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p214/t/bones` |
| 2859 | Abyssal Tide $(r_aura) | Bones · wardrobe (p119/dlg/bones); Bones · wardrobe (p99/dlg/bones) | 2840 | `p99/act/bones` [menu 2840] → `p138/au/t_bones` |
| 2861 | Sit / follow | Mr. Capshun's Pencil (p198/menu) | 2860 | `p198/act` [menu 2860] → `p198/sit` (if if entity @e[type=minecraft:wolf,tag=bm.mzsel2]) |
| 2862 | Wardrobe | Mr. Capshun's Pencil (p198/menu) | 2860 | `p198/act` [menu 2860] → `p119/plain/capshun` |
| 2864 | Mr. Capshun's ways | Mr. Capshun's Pencil (p198/menu) | 2860 | `p198/act` [menu 2860] → `p198/powers` |
| 2865 | « Back | MR. CAPSHUN'S PALETTE (p198/pal); MR. CAPSHUN'S WAYS (p198/powers) | 2860 | `p198/act` [menu 2860] → `p198/menu` |
| 2866 | Palette | Mr. Capshun's Pencil (p198/menu) | 2860 | `p198/act` [menu 2860] → `p198/pal` |
| 2867 | The story so far | Mr. Capshun's Pencil (p198/menu) | 2860 | `p198/act` [menu 2860] → `p198/story` |
| 2868 | Call for Mr. Capshun | Mr. Capshun's Pencil (p198/menu) | 2860 | `p198/act` [menu 2860] → `p198/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.mzsel2]) / `p198/act` [menu 2860] → `p198/recall` (if if entity @e[type=minecraft:wolf,tag=bm.mzsel2]) |
| 2869 | Send him home | Mr. Capshun's Pencil (p198/menu) | 2860 | `p198/act` [menu 2860] → `p198/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.mzsel2]) |
| 2870 | Red | MR. CAPSHUN'S PALETTE (p198/pal) | 2860 | `p198/pal_act` [menu 2860] → (inline: scoreboard) / `p198/pal_act` [menu 2860] → (inline: title) |
| 2871 | Orange | MR. CAPSHUN'S PALETTE (p198/pal) | 2860 | `p198/pal_act` [menu 2860] → (inline: scoreboard) / `p198/pal_act` [menu 2860] → (inline: title) |
| 2872 | Yellow | MR. CAPSHUN'S PALETTE (p198/pal) | 2860 | `p198/pal_act` [menu 2860] → (inline: scoreboard) / `p198/pal_act` [menu 2860] → (inline: title) |
| 2873 | Green | MR. CAPSHUN'S PALETTE (p198/pal) | 2860 | `p198/pal_act` [menu 2860] → (inline: scoreboard) / `p198/pal_act` [menu 2860] → (inline: title) |
| 2874 | Blue | MR. CAPSHUN'S PALETTE (p198/pal) | 2860 | `p198/pal_act` [menu 2860] → (inline: scoreboard) / `p198/pal_act` [menu 2860] → (inline: title) |
| 2875 | Purple | MR. CAPSHUN'S PALETTE (p198/pal) | 2860 | `p198/pal_act` [menu 2860] → (inline: scoreboard) / `p198/pal_act` [menu 2860] → (inline: title) |
| 2876 | Rainbow | MR. CAPSHUN'S PALETTE (p198/pal) | 2860 | `p198/pal_act` [menu 2860] → (inline: scoreboard) / `p198/pal_act` [menu 2860] → (inline: title) |
| 2880 | « Outfits & buffs / $(r_home) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/capshun` [menu 2880] → `p125/hc/capshun` |
| 2882 | Plain black ink $(r_capshun0) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p99/pick/capshun0` |
| 2883 | Blue Ballpoint $(r_capshun1) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p99/pick/capshun1` |
| 2884 | Red Pen $(r_capshun2) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p99/pick/capshun2` |
| 2885 | Green Marker $(r_capshun3) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p99/pick/capshun3` |
| 2886 | Gilded Ink $(r_capshun4) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p99/pick/capshun4` |
| 2887 | Diamond Ink $(r_capshun5) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p99/pick/capshun5` |
| 2888 | Netherite Ink $(r_capshun6) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p99/pick/capshun6` |
| 2898 | Pixel costume $(r_px) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p214/t/capshun` |
| 2899 | Rainbow Doodles $(r_aura) | Mr. Capshun · wardrobe (p119/dlg/capshun); Mr. Capshun · wardrobe (p99/dlg/capshun) | 2880 | `p99/act/capshun` [menu 2880] → `p138/au/t_capshun` |
| 2900 | « Outfits & buffs / $(r_home) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/sky` [menu 2900] → `p125/hc/sky` |
| 2902 | Snooze's old blue $(r_sky0) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p99/pick/sky0` |
| 2903 | Bubblegum Pink $(r_sky1) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p99/pick/sky1` |
| 2904 | Mint Dream $(r_sky2) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p99/pick/sky2` |
| 2905 | Lavender Night $(r_sky3) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p99/pick/sky3` |
| 2906 | Gilded Nightcap $(r_sky4) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p99/pick/sky4` |
| 2907 | Diamond Nightcap $(r_sky5) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p99/pick/sky5` |
| 2908 | Netherite Nightcap $(r_sky6) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p99/pick/sky6` |
| 2918 | Pixel costume $(r_px) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p214/t/sky` |
| 2919 | Starry Sky $(r_aura) | The Sky Buddies · wardrobe (p119/dlg/sky); The Sky Buddies · wardrobe (p99/dlg/sky) | 2900 | `p99/act/sky` [menu 2900] → `p138/au/t_sky` |
| 2941 | Sit / follow | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p211/sit` (if if entity @e[type=minecraft:wolf,tag=bm.ybsel2]) |
| 2942 | Wardrobe | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p119/plain/sky` |
| 2943 | A bed on Nimbus | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p211/bed/try` |
| 2944 | The Sky Buddies' ways | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p211/powers` |
| 2945 | « Back | THE SKY BUDDIES' WAYS (p211/powers) | 2940 | `p211/act` [menu 2940] → `p211/menu` |
| 2946 | Today's forecast | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p211/today` |
| 2947 | Change the weather | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p211/wx/open` |
| 2948 | Call for The Sky Buddies | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p211/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.ybsel2]) / `p211/act` [menu 2940] → `p211/recall` (if if entity @e[type=minecraft:wolf,tag=bm.ybsel2]) |
| 2949 | Send them home | The Sky Mobile (p211/menu) | 2940 | `p211/act` [menu 2940] → `p211/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.ybsel2]) |
| 2950 | Clear skies | THE SKY, YOURS (p211/wx/open) | 2940 | `p211/wx/act` [menu 2940] → `p211/wx/clear` |
| 2951 | Rain | THE SKY, YOURS (p211/wx/open) | 2940 | `p211/wx/act` [menu 2940] → `p211/wx/rain` |
| 2952 | Thunderstorm | THE SKY, YOURS (p211/wx/open) | 2940 | `p211/wx/act` [menu 2940] → `p211/wx/storm` |
| 2953 | « Back | THE SKY, YOURS (p211/wx/open) | 2940 | `p211/wx/act` [menu 2940] → `p211/menu` |
| 2960 | « Outfits & buffs / $(r_home) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/pxemma` [menu 2960] → `p125/hc/pxemma` |
| 2962 | Sixteen colours $(r_pxemma0) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p99/pick/pxemma0` |
| 2963 | Game Boy $(r_pxemma1) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p99/pick/pxemma1` |
| 2964 | Virtual Boy $(r_pxemma2) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p99/pick/pxemma2` |
| 2965 | Sepia Print $(r_pxemma3) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p99/pick/pxemma3` |
| 2966 | Gilded Pixels $(r_pxemma4) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p99/pick/pxemma4` |
| 2967 | Diamond Pixels $(r_pxemma5) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p99/pick/pxemma5` |
| 2968 | Netherite Pixels $(r_pxemma6) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p99/pick/pxemma6` |
| 2979 | Scanlines $(r_aura) | 8-Bit Emma · wardrobe (p119/dlg/pxemma); 8-Bit Emma · wardrobe (p99/dlg/pxemma) | 2960 | `p99/act/pxemma` [menu 2960] → `p138/au/t_pxemma` |
| 2981 | Sit / follow | 8-Bit Emma's Cartridge (p213e/menu) | 2980 | `p213e/act` [menu 2980] → `p213e/sit` (if if entity @e[type=minecraft:wolf,tag=bm.xmsel2]) |
| 2982 | Wardrobe | 8-Bit Emma's Cartridge (p213e/menu) | 2980 | `p213e/act` [menu 2980] → `p119/plain/pxemma` |
| 2984 | 8-Bit Emma's ways | 8-Bit Emma's Cartridge (p213e/menu) | 2980 | `p213e/act` [menu 2980] → `p213e/powers` |
| 2985 | « Back | 8-BIT EMMA'S WAYS (p213e/powers) | 2980 | `p213e/act` [menu 2980] → `p213e/menu` |
| 2988 | Call for 8-Bit Emma | 8-Bit Emma's Cartridge (p213e/menu) | 2980 | `p213e/act` [menu 2980] → `p213e/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.xmsel2]) / `p213e/act` [menu 2980] → `p213e/recall` (if if entity @e[type=minecraft:wolf,tag=bm.xmsel2]) |
| 2989 | Send her home | 8-Bit Emma's Cartridge (p213e/menu) | 2980 | `p213e/act` [menu 2980] → `p213e/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.xmsel2]) |
| 3000 | « Outfits & buffs / $(r_home) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/pxleo` [menu 3000] → `p125/hc/pxleo` |
| 3002 | Sixteen colours $(r_pxleo0) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p99/pick/pxleo0` |
| 3003 | Game Boy $(r_pxleo1) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p99/pick/pxleo1` |
| 3004 | Virtual Boy $(r_pxleo2) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p99/pick/pxleo2` |
| 3005 | Sepia Print $(r_pxleo3) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p99/pick/pxleo3` |
| 3006 | Gilded Pixels $(r_pxleo4) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p99/pick/pxleo4` |
| 3007 | Diamond Pixels $(r_pxleo5) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p99/pick/pxleo5` |
| 3008 | Netherite Pixels $(r_pxleo6) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p99/pick/pxleo6` |
| 3019 | Scanlines $(r_aura) | 8-Bit Leo · wardrobe (p119/dlg/pxleo); 8-Bit Leo · wardrobe (p99/dlg/pxleo) | 3000 | `p99/act/pxleo` [menu 3000] → `p138/au/t_pxleo` |
| 3021 | Sit / follow | 8-Bit Leo's Cartridge (p213l/menu) | 3020 | `p213l/act` [menu 3020] → `p213l/sit` (if if entity @e[type=minecraft:wolf,tag=bm.xlsel2]) |
| 3022 | Wardrobe | 8-Bit Leo's Cartridge (p213l/menu) | 3020 | `p213l/act` [menu 3020] → `p119/plain/pxleo` |
| 3024 | 8-Bit Leo's ways | 8-Bit Leo's Cartridge (p213l/menu) | 3020 | `p213l/act` [menu 3020] → `p213l/powers` |
| 3025 | « Back | 8-BIT LEO'S WAYS (p213l/powers) | 3020 | `p213l/act` [menu 3020] → `p213l/menu` |
| 3028 | Call for 8-Bit Leo | 8-Bit Leo's Cartridge (p213l/menu) | 3020 | `p213l/act` [menu 3020] → `p213l/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.xlsel2]) / `p213l/act` [menu 3020] → `p213l/recall` (if if entity @e[type=minecraft:wolf,tag=bm.xlsel2]) |
| 3029 | Send him home | 8-Bit Leo's Cartridge (p213l/menu) | 3020 | `p213l/act` [menu 3020] → `p213l/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.xlsel2]) |
| 3040 | « Outfits & buffs / $(r_home) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/pxcecil` [menu 3040] → `p125/hc/pxcecil` |
| 3042 | Sixteen colours $(r_pxcecil0) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p99/pick/pxcecil0` |
| 3043 | Game Boy $(r_pxcecil1) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p99/pick/pxcecil1` |
| 3044 | Virtual Boy $(r_pxcecil2) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p99/pick/pxcecil2` |
| 3045 | Sepia Print $(r_pxcecil3) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p99/pick/pxcecil3` |
| 3046 | Gilded Pixels $(r_pxcecil4) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p99/pick/pxcecil4` |
| 3047 | Diamond Pixels $(r_pxcecil5) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p99/pick/pxcecil5` |
| 3048 | Netherite Pixels $(r_pxcecil6) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p99/pick/pxcecil6` |
| 3059 | Scanlines $(r_aura) | 8-Bit Cecil · wardrobe (p119/dlg/pxcecil); 8-Bit Cecil · wardrobe (p99/dlg/pxcecil) | 3040 | `p99/act/pxcecil` [menu 3040] → `p138/au/t_pxcecil` |
| 3061 | Sit / follow | 8-Bit Cecil's Cartridge (p213c/menu) | 3060 | `p213c/act` [menu 3060] → `p213c/sit` (if if entity @e[type=minecraft:wolf,tag=bm.xcsel2]) |
| 3062 | Wardrobe | 8-Bit Cecil's Cartridge (p213c/menu) | 3060 | `p213c/act` [menu 3060] → `p119/plain/pxcecil` |
| 3064 | 8-Bit Cecil's ways | 8-Bit Cecil's Cartridge (p213c/menu) | 3060 | `p213c/act` [menu 3060] → `p213c/powers` |
| 3065 | « Back | 8-BIT CECIL'S WAYS (p213c/powers) | 3060 | `p213c/act` [menu 3060] → `p213c/menu` |
| 3068 | Call for 8-Bit Cecil | 8-Bit Cecil's Cartridge (p213c/menu) | 3060 | `p213c/act` [menu 3060] → `p213c/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.xcsel2]) / `p213c/act` [menu 3060] → `p213c/recall` (if if entity @e[type=minecraft:wolf,tag=bm.xcsel2]) |
| 3069 | Send him home | 8-Bit Cecil's Cartridge (p213c/menu) | 3060 | `p213c/act` [menu 3060] → `p213c/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.xcsel2]) |
| 3100 | Open the bidding | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: title) (if unless score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3101 | Bid +1 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3102 | Bid +2 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3105 | Bid +5 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3110 | Bid +10 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3202 | Tuning | VESPER'S STOCK BOOK · the Dread Broker (p177/open_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune` |
| 3203 | Reforging | VESPER'S STOCK BOOK · the Dread Broker (p177/open_dlg) | 3200 | `p177/act` [menu 3200] → `p177/rf` |
| 3204 | About the Dread | VESPER'S STOCK BOOK · the Dread Broker (p177/open_dlg) | 3200 | `p177/act` [menu 3200] → `p177/about` |
| 3205 | Reforge what I hold | Reforging · past the old maximum (p177/rf_dlg) | 3200 | `p177/act` [menu 3200] → `p177/reforge` |
| 3209 | « The Ledger | About the Dread (p177/about); Reforging · past the old maximum (p177/rf_dlg); Tuning · a tool (p177/tp/tool_dlg) (+2 more) | 3200 | `p177/act` [menu 3200] → `p177/open` |
| 3220 | Attack Damage +0.75 (max 3) | Tuning · a weapon (p177/tp/weapon_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/weapon_dmg` |
| 3221 | Swing Speed +0.1 (max 3) | Tuning · a weapon (p177/tp/weapon_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/weapon_spd` |
| 3222 | Reach +0.25 (max 2) | Tuning · a weapon (p177/tp/weapon_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/weapon_rch` |
| 3223 | Luck +1 (max 2) | Tuning · a weapon (p177/tp/weapon_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/weapon_lck` |
| 3224 | Unbind all tunings (every token back) | Tuning · a weapon (p177/tp/weapon_dlg) | 3200 | `p177/act` [menu 3200] → `p177/unbind` |
| 3225 | Mining Speed +10% (max 3) | Tuning · a tool (p177/tp/tool_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/tool_brk` |
| 3226 | Mining Efficiency +3 (max 2) | Tuning · a tool (p177/tp/tool_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/tool_eff` |
| 3227 | Block Reach +0.5 (max 2) | Tuning · a tool (p177/tp/tool_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/tool_brc` |
| 3228 | Luck +1 (max 2) | Tuning · a tool (p177/tp/tool_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/tool_lck` |
| 3229 | Unbind all tunings (every token back) | Tuning · a tool (p177/tp/tool_dlg) | 3200 | `p177/act` [menu 3200] → `p177/unbind` |
| 3230 | Armor +1 (max 2) | Tuning · an armour piece (p177/tp/armor_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/armor_arm` |
| 3231 | Toughness +1 (max 2) | Tuning · an armour piece (p177/tp/armor_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/armor_tgh` |
| 3232 | Max Health +1 (max 2) | Tuning · an armour piece (p177/tp/armor_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/armor_hp` |
| 3233 | Knockback Resistance +0.05 (max 2) | Tuning · an armour piece (p177/tp/armor_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/armor_kb` |
| 3234 | Speed (boots) +2% (max 2) | Tuning · an armour piece (p177/tp/armor_dlg) | 3200 | `p177/act` [menu 3200] → `p177/tune/armor_mv` |
| 3235 | Unbind all tunings (every token back) | Tuning · an armour piece (p177/tp/armor_dlg) | 3200 | `p177/act` [menu 3200] → `p177/unbind` |
| 3301 | Lamplighters' Fund $(p0)/250$(s0) | Community Pots · The Rat Bank (p178/pots/dlg) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/page0` |
| 3302 | Harvest Guild $(p1)/300$(s1) | Community Pots · The Rat Bank (p178/pots/dlg) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/page1` |
| 3303 | Miners' Union $(p2)/400$(s2) | Community Pots · The Rat Bank (p178/pots/dlg) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/page2` |
| 3304 | Couriers' Guild $(p3)/400$(s3) | Community Pots · The Rat Bank (p178/pots/dlg) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/page3` |
| 3305 | Hearth Fund $(p4)/500$(s4) | Community Pots · The Rat Bank (p178/pots/dlg) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/page4` |
| 3306 | Bounty Office $(p5)/600$(s5) | Community Pots · The Rat Bank (p178/pots/dlg) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/page5` |
| 3309 | « Your account | Community Pots · The Rat Bank (p178/pots/dlg) | 3300 | `p178/pots/act` [menu 3300] → `p31/bank/open` |
| 3310 | Give 10 Tokens | Lamplighters' Fund · Community Pots (p178/pots/pdlg0) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give0_10` |
| 3311 | Give 10 Tokens | Harvest Guild · Community Pots (p178/pots/pdlg1) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give1_10` |
| 3312 | Give 10 Tokens | Miners' Union · Community Pots (p178/pots/pdlg2) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give2_10` |
| 3313 | Give 10 Tokens | Couriers' Guild · Community Pots (p178/pots/pdlg3) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give3_10` |
| 3314 | Give 10 Tokens | Hearth Fund · Community Pots (p178/pots/pdlg4) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give4_10` |
| 3315 | Give 10 Tokens | Bounty Office · Community Pots (p178/pots/pdlg5) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give5_10` |
| 3320 | Give 50 Tokens | Lamplighters' Fund · Community Pots (p178/pots/pdlg0) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give0_50` |
| 3321 | Give 50 Tokens | Harvest Guild · Community Pots (p178/pots/pdlg1) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give1_50` |
| 3322 | Give 50 Tokens | Miners' Union · Community Pots (p178/pots/pdlg2) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give2_50` |
| 3323 | Give 50 Tokens | Couriers' Guild · Community Pots (p178/pots/pdlg3) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give3_50` |
| 3324 | Give 50 Tokens | Hearth Fund · Community Pots (p178/pots/pdlg4) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give4_50` |
| 3325 | Give 50 Tokens | Bounty Office · Community Pots (p178/pots/pdlg5) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/give5_50` |
| 3330 | Switch it on / off | Lamplighters' Fund · Community Pots (p178/pots/pdlg0) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/toggle0` |
| 3331 | Switch it on / off | Harvest Guild · Community Pots (p178/pots/pdlg1) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/toggle1` |
| 3332 | Switch it on / off | Miners' Union · Community Pots (p178/pots/pdlg2) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/toggle2` |
| 3333 | Switch it on / off | Couriers' Guild · Community Pots (p178/pots/pdlg3) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/toggle3` |
| 3334 | Switch it on / off | Hearth Fund · Community Pots (p178/pots/pdlg4) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/toggle4` |
| 3335 | Switch it on / off | Bounty Office · Community Pots (p178/pots/pdlg5) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/toggle5` |
| 3340 | « The pots | Bounty Office · Community Pots (p178/pots/pdlg5); Couriers' Guild · Community Pots (p178/pots/pdlg3); Harvest Guild · Community Pots (p178/pots/pdlg1) (+3 more) | 3300 | `p178/pots/act` [menu 3300] → `p178/pots/open` |
| 3351 | Keep up: off / Keep up: on | p179/w/open | 3350 | `p179/w/act` [menu 3350] → `p179/k/toggle` |
| 3352 | ❖ Gallery | p179/w/open | 3350 | `p179/w/act` [menu 3350] → `p220/open` |
| 3353 | ◈ View in 3D: #01-#08 | Follower Gallery (p220/show) | 3350 | `p179/w/act` [menu 3350] → `p220/view0` |
| 3354 | ◈ View in 3D: #09-#16 | Follower Gallery (p220/show) | 3350 | `p179/w/act` [menu 3350] → `p220/view1` |
| 3355 | ◈ View in 3D: #17-#24 | Follower Gallery (p220/show) | 3350 | `p179/w/act` [menu 3350] → `p220/view2` |
| 3356 | ◈ View in 3D: #25-#32 | Follower Gallery (p220/show) | 3350 | `p179/w/act` [menu 3350] → `p220/view3` |
| 3359 | « Partner Wheel | Follower Gallery (p220/show) | 3350 | `p179/w/act` [menu 3350] → `p179/w/open` |
| 3360 | Call Emma / Send Emma home | p179/w/row0 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call0` |
| 3361 | Call Celi / Send Celi home | p179/w/row1 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call1` |
| 3362 | Call Zib / Send Zib home | p179/w/row2 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call2` |
| 3363 | Call Cecil / Send Cecil home | p179/w/row3 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call3` |
| 3364 | Call KillerWatt / Send KillerWatt home | p179/w/row4 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call4` |
| 3365 | Call Leo / Send Leo home | p179/w/row5 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call5` |
| 3366 | Call Democratus / Send Democratus home | p179/w/row6 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call6` |
| 3367 | Call Apophiss / Send Apophiss home | p179/w/row7 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call7` |
| 3368 | Call Tullius / Send Tullius home | p179/w/row8 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call8` |
| 3369 | Call the Frog / Send the Frog home | p179/w/row9 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call9` |
| 3370 | Call Donado / Send Donado home | p179/w/row10 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call10` |
| 3371 | Call Pearlman / Send Pearlman home | p179/w/row11 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call11` |
| 3372 | Call Wilfrey / Send Wilfrey home | p179/w/row12 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call12` |
| 3373 | Call Fishy / Send Fishy home | p179/w/row13 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call13` |
| 3374 | Call Dennis / Send Dennis home | p179/w/row14 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call14` |
| 3375 | Call Pistachio / Send Pistachio home | p179/w/row15 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call15` |
| 3376 | Call King Omega / Send King Omega home | p179/w/row16 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call16` |
| 3377 | Call Ashur / Send Ashur home | p179/w/row17 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call17` |
| 3378 | Call the Chef / Send the Chef home | p179/w/row18 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call18` |
| 3379 | Call the Neighbor / Send the Neighbor home | p179/w/row19 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call19` |
| 3380 | Call Queen Ava / Send Queen Ava home | p179/w/row20 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call20` |
| 3381 | Call Queen Pearl / Send Queen Pearl home | p179/w/row21 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call21` |
| 3382 | Call Bloo / Send Bloo home | p179/w/row22 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call22` |
| 3383 | Call The Stalker / Send The Stalker home | p179/w/row23 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call23` |
| 3384 | Call The Arachno-Lantern / Send The Arachno-Lantern home | p179/w/row24 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call24` |
| 3385 | Call Bender / Send Bender home | p179/w/row25 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call25` |
| 3386 | Call Bones / Send Bones home | p179/w/row26 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call26` |
| 3387 | Call Mr. Capshun / Send Mr. Capshun home | p179/w/row27 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call27` |
| 3388 | Call 8-Bit Cecil / Send 8-Bit Cecil home | p179/w/row28 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call28` |
| 3389 | Call 8-Bit Leo / Send 8-Bit Leo home | p179/w/row29 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call29` |
| 3390 | Take the item back | p179/w/row0 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out0` |
| 3391 | Take the item back | p179/w/row1 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out1` |
| 3392 | Take the item back | p179/w/row2 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out2` |
| 3393 | Take the item back | p179/w/row3 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out3` |
| 3394 | Take the item back | p179/w/row4 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out4` |
| 3395 | Take the item back | p179/w/row5 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out5` |
| 3396 | Take the item back | p179/w/row6 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out6` |
| 3397 | Take the item back | p179/w/row7 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out7` |
| 3398 | Take the item back | p179/w/row8 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out8` |
| 3399 | Take the item back | p179/w/row9 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out9` |
| 3400 | Take the item back | p179/w/row10 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out10` |
| 3401 | Take the item back | p179/w/row11 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out11` |
| 3402 | Take the item back | p179/w/row12 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out12` |
| 3403 | Take the item back | p179/w/row13 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out13` |
| 3404 | Take the item back | p179/w/row14 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out14` |
| 3405 | Take the item back | p179/w/row15 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out15` |
| 3406 | Take the item back | p179/w/row16 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out16` |
| 3407 | Take the item back | p179/w/row17 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out17` |
| 3408 | Take the item back | p179/w/row18 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out18` |
| 3409 | Take the item back | p179/w/row19 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out19` |
| 3410 | Take the item back | p179/w/row20 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out20` |
| 3411 | Take the item back | p179/w/row21 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out21` |
| 3412 | Take the item back | p179/w/row22 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out22` |
| 3413 | Take the item back | p179/w/row23 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out23` |
| 3414 | Take the item back | p179/w/row24 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out24` |
| 3415 | Take the item back | p179/w/row25 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out25` |
| 3416 | Take the item back | p179/w/row26 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out26` |
| 3417 | Take the item back | p179/w/row27 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out27` |
| 3418 | Take the item back | p179/w/row28 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out28` |
| 3419 | Take the item back | p179/w/row29 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out29` |
| 3420 | Launch your Skiff Escort / Send your Skiff Escort home | p184/wesc/row | 3350 | `p179/w/act` [menu 3350] → `p184/wesc/call` |
| 3421 | Take the escort back | p184/wesc/row | 3350 | `p179/w/act` [menu 3350] → `p184/wesc/out` |
| 3450 | ⚙ Menu | p179/w/row0 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu0` |
| 3451 | ⚙ Menu | p179/w/row1 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu1` |
| 3452 | ⚙ Menu | p179/w/row2 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu2` |
| 3453 | ⚙ Menu | p179/w/row3 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu3` |
| 3454 | ⚙ Menu | p179/w/row4 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu4` |
| 3455 | ⚙ Menu | p179/w/row5 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu5` |
| 3456 | ⚙ Menu | p179/w/row6 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu6` |
| 3457 | ⚙ Menu | p179/w/row7 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu7` |
| 3458 | ⚙ Menu | p179/w/row8 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu8` |
| 3459 | ⚙ Menu | p179/w/row9 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu9` |
| 3460 | ⚙ Menu | p179/w/row10 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu10` |
| 3461 | ⚙ Menu | p179/w/row11 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu11` |
| 3462 | ⚙ Menu | p179/w/row12 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu12` |
| 3463 | ⚙ Menu | p179/w/row13 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu13` |
| 3464 | ⚙ Menu | p179/w/row14 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu14` |
| 3465 | ⚙ Menu | p179/w/row15 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu15` |
| 3466 | ⚙ Menu | p179/w/row16 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu16` |
| 3467 | ⚙ Menu | p179/w/row17 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu17` |
| 3468 | ⚙ Menu | p179/w/row18 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu18` |
| 3469 | ⚙ Menu | p179/w/row19 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu19` |
| 3470 | ⚙ Menu | p179/w/row20 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu20` |
| 3471 | ⚙ Menu | p179/w/row21 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu21` |
| 3472 | ⚙ Menu | p179/w/row22 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu22` |
| 3473 | ⚙ Menu | p179/w/row23 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu23` |
| 3474 | ⚙ Menu | p179/w/row24 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu24` |
| 3475 | ⚙ Menu | p179/w/row25 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu25` |
| 3476 | ⚙ Menu | p179/w/row26 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu26` |
| 3477 | ⚙ Menu | p179/w/row27 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu27` |
| 3478 | ⚙ Menu | p179/w/row28 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu28` |
| 3479 | ⚙ Menu | p179/w/row29 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu29` |
| 3480 | Dynamic | Pearlman's Seasons (p209/menu) | 971 | `p209/act` [menu 971] → `p209/pick/dynamic` |
| 3481 | Off - his own colours | Pearlman's Seasons (p209/menu) | 971 | `p209/act` [menu 971] → `p209/pick/off` |
| 3482 | Fall / Fall (locked) | Pearlman's Seasons (p209/menu) | 971 | `p209/act` [menu 971] → `p209/pick/fall` |
| 3483 | Christmas / Christmas (locked) | Pearlman's Seasons (p209/menu) | 971 | `p209/act` [menu 971] → `p209/pick/xmas` |
| 3484 | Easter / Easter (locked) | Pearlman's Seasons (p209/menu) | 971 | `p209/act` [menu 971] → `p209/pick/easter` |
| 3485 | Summer / Summer (locked) | Pearlman's Seasons (p209/menu) | 971 | `p209/act` [menu 971] → `p209/pick/summer` |
| 3600 | Gilded Pixels $(r_182) | 8-BIT EMMA · the Tailor (p103/tl/p_pxemma_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b182` [menu 7740] |
| 3601 | Diamond Pixels $(r_183) | 8-BIT EMMA · the Tailor (p103/tl/p_pxemma_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b183` [menu 7740] |
| 3602 | Netherite Pixels $(r_184) | 8-BIT EMMA · the Tailor (p103/tl/p_pxemma_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b184` [menu 7740] |
| 3603 | Game Boy $(r_185) | 8-BIT LEO · the Tailor (p103/tl/p_pxleo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b185` [menu 7740] |
| 3604 | Virtual Boy $(r_186) | 8-BIT LEO · the Tailor (p103/tl/p_pxleo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b186` [menu 7740] |
| 3605 | Sepia Print $(r_187) | 8-BIT LEO · the Tailor (p103/tl/p_pxleo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b187` [menu 7740] |
| 3606 | Gilded Pixels $(r_188) | 8-BIT LEO · the Tailor (p103/tl/p_pxleo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b188` [menu 7740] |
| 3607 | Diamond Pixels $(r_189) | 8-BIT LEO · the Tailor (p103/tl/p_pxleo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b189` [menu 7740] |
| 3608 | Netherite Pixels $(r_190) | 8-BIT LEO · the Tailor (p103/tl/p_pxleo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b190` [menu 7740] |
| 3609 | Game Boy $(r_191) | 8-BIT CECIL · the Tailor (p103/tl/p_pxcecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b191` [menu 7740] |
| 3610 | Virtual Boy $(r_192) | 8-BIT CECIL · the Tailor (p103/tl/p_pxcecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b192` [menu 7740] |
| 3611 | Sepia Print $(r_193) | 8-BIT CECIL · the Tailor (p103/tl/p_pxcecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b193` [menu 7740] |
| 3612 | Gilded Pixels $(r_194) | 8-BIT CECIL · the Tailor (p103/tl/p_pxcecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b194` [menu 7740] |
| 3613 | Diamond Pixels $(r_195) | 8-BIT CECIL · the Tailor (p103/tl/p_pxcecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b195` [menu 7740] |
| 3614 | Netherite Pixels $(r_196) | 8-BIT CECIL · the Tailor (p103/tl/p_pxcecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b196` [menu 7740] |
| 3615 | Blue Ballpoint $(r_197) | MR. CAPSHUN · the Tailor (p103/tl/p_capshun_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b197` [menu 7740] |
| 3616 | Red Pen $(r_198) | MR. CAPSHUN · the Tailor (p103/tl/p_capshun_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b198` [menu 7740] |
| 3617 | Green Marker $(r_199) | MR. CAPSHUN · the Tailor (p103/tl/p_capshun_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b199` [menu 7740] |
| 3618 | Gilded Ink $(r_200) | MR. CAPSHUN · the Tailor (p103/tl/p_capshun_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b200` [menu 7740] |
| 3619 | Diamond Ink $(r_201) | MR. CAPSHUN · the Tailor (p103/tl/p_capshun_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b201` [menu 7740] |
| 3620 | Netherite Ink $(r_202) | MR. CAPSHUN · the Tailor (p103/tl/p_capshun_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b202` [menu 7740] |
| 3700 | Call 8-Bit Emma / Send 8-Bit Emma home | p179/w/row30 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call30` |
| 3701 | Call The Sky Buddies / Send The Sky Buddies home | p179/w/row31 | 3350 | `p179/w/act` [menu 3350] → `p179/w/call31` |
| 3740 | Take the item back | p179/w/row30 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out30` |
| 3741 | Take the item back | p179/w/row31 | 3350 | `p179/w/act` [menu 3350] → `p179/w/out31` |
| 3780 | ⚙ Menu | p179/w/row30 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu30` |
| 3781 | ⚙ Menu | p179/w/row31 | 3350 | `p179/w/act` [menu 3350] → `p179/w/menu31` |
| 4010 | Deposit all Tokens ($(h)) | Tokens · The Rat Bank (p31/bank/pdlg_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_token` |
| 4011 | Take 1 | Tokens · The Rat Bank (p31/bank/pdlg_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_token` |
| 4012 | Take 10 | Tokens · The Rat Bank (p31/bank/pdlg_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_token` |
| 4013 | Take all ($(n)) | Tokens · The Rat Bank (p31/bank/pdlg_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_token` |
| 4014 | Deposit all Lucky Tokens ($(h)) | Lucky Tokens · The Rat Bank (p31/bank/pdlg_lucky_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_lucky_token` |
| 4015 | Take 1 | Lucky Tokens · The Rat Bank (p31/bank/pdlg_lucky_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_lucky_token` |
| 4016 | Take 10 | Lucky Tokens · The Rat Bank (p31/bank/pdlg_lucky_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_lucky_token` |
| 4017 | Take all ($(n)) | Lucky Tokens · The Rat Bank (p31/bank/pdlg_lucky_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_lucky_token` |
| 4018 | Deposit all Medallions ($(h)) | Medallions · The Rat Bank (p31/bank/pdlg_medallion) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_medallion` |
| 4019 | Take 1 | Medallions · The Rat Bank (p31/bank/pdlg_medallion) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_medallion` |
| 4020 | Take 10 | Medallions · The Rat Bank (p31/bank/pdlg_medallion) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_medallion` |
| 4021 | Take all ($(n)) | Medallions · The Rat Bank (p31/bank/pdlg_medallion) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_medallion` |
| 4022 | Deposit all Trophies ($(h)) | Trophies · The Rat Bank (p31/bank/pdlg_trophy) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_trophy` |
| 4023 | Take 1 | Trophies · The Rat Bank (p31/bank/pdlg_trophy) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_trophy` |
| 4024 | Take 10 | Trophies · The Rat Bank (p31/bank/pdlg_trophy) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_trophy` |
| 4025 | Take all ($(n)) | Trophies · The Rat Bank (p31/bank/pdlg_trophy) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_trophy` |
| 4026 | Deposit all Blood Crystals ($(h)) | Blood Crystals · The Rat Bank (p31/bank/pdlg_blood_crystal) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_blood_crystal` |
| 4027 | Take 1 | Blood Crystals · The Rat Bank (p31/bank/pdlg_blood_crystal) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_blood_crystal` |
| 4028 | Take 10 | Blood Crystals · The Rat Bank (p31/bank/pdlg_blood_crystal) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_blood_crystal` |
| 4029 | Take all ($(n)) | Blood Crystals · The Rat Bank (p31/bank/pdlg_blood_crystal) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_blood_crystal` |
| 4030 | Deposit all Ember Scales ($(h)) | Ember Scales · The Rat Bank (p31/bank/pdlg_ember_scale) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_ember_scale` |
| 4031 | Take 1 | Ember Scales · The Rat Bank (p31/bank/pdlg_ember_scale) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_ember_scale` |
| 4032 | Take 10 | Ember Scales · The Rat Bank (p31/bank/pdlg_ember_scale) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_ember_scale` |
| 4033 | Take all ($(n)) | Ember Scales · The Rat Bank (p31/bank/pdlg_ember_scale) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_ember_scale` |
| 4034 | Deposit all Void Shards ($(h)) | Void Shards · The Rat Bank (p31/bank/pdlg_void_shard) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_void_shard` |
| 4035 | Take 1 | Void Shards · The Rat Bank (p31/bank/pdlg_void_shard) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_void_shard` |
| 4036 | Take 10 | Void Shards · The Rat Bank (p31/bank/pdlg_void_shard) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_void_shard` |
| 4037 | Take all ($(n)) | Void Shards · The Rat Bank (p31/bank/pdlg_void_shard) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_void_shard` |
| 4038 | Deposit all Green Xenite ($(h)) | Green Xenite · The Rat Bank (p31/bank/pdlg_xenite_green) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_green` |
| 4039 | Take 1 | Green Xenite · The Rat Bank (p31/bank/pdlg_xenite_green) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_green` |
| 4040 | Take 10 | Green Xenite · The Rat Bank (p31/bank/pdlg_xenite_green) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_green` |
| 4041 | Take all ($(n)) | Green Xenite · The Rat Bank (p31/bank/pdlg_xenite_green) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_green` |
| 4042 | Deposit all Violet Xenite ($(h)) | Violet Xenite · The Rat Bank (p31/bank/pdlg_xenite_violet) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_violet` |
| 4043 | Take 1 | Violet Xenite · The Rat Bank (p31/bank/pdlg_xenite_violet) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_violet` |
| 4044 | Take 10 | Violet Xenite · The Rat Bank (p31/bank/pdlg_xenite_violet) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_violet` |
| 4045 | Take all ($(n)) | Violet Xenite · The Rat Bank (p31/bank/pdlg_xenite_violet) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_violet` |
| 4046 | Deposit all Cyan Xenite ($(h)) | Cyan Xenite · The Rat Bank (p31/bank/pdlg_xenite_cyan) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_cyan` |
| 4047 | Take 1 | Cyan Xenite · The Rat Bank (p31/bank/pdlg_xenite_cyan) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_cyan` |
| 4048 | Take 10 | Cyan Xenite · The Rat Bank (p31/bank/pdlg_xenite_cyan) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_cyan` |
| 4049 | Take all ($(n)) | Cyan Xenite · The Rat Bank (p31/bank/pdlg_xenite_cyan) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_cyan` |
| 4050 | Deposit all Red Xenite ($(h)) | Red Xenite · The Rat Bank (p31/bank/pdlg_xenite_red) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_red` |
| 4051 | Take 1 | Red Xenite · The Rat Bank (p31/bank/pdlg_xenite_red) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_red` |
| 4052 | Take 10 | Red Xenite · The Rat Bank (p31/bank/pdlg_xenite_red) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_red` |
| 4053 | Take all ($(n)) | Red Xenite · The Rat Bank (p31/bank/pdlg_xenite_red) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_red` |
| 4054 | Deposit all Dread Tokens ($(h)) | Dread Tokens · The Rat Bank (p31/bank/pdlg_dread_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_dread_token` |
| 4055 | Take 1 | Dread Tokens · The Rat Bank (p31/bank/pdlg_dread_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_dread_token` |
| 4056 | Take 10 | Dread Tokens · The Rat Bank (p31/bank/pdlg_dread_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_dread_token` |
| 4057 | Take all ($(n)) | Dread Tokens · The Rat Bank (p31/bank/pdlg_dread_token) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_dread_token` |
| 4060 | Tokens $(token) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_token` |
| 4061 | Lucky Tokens $(lucky_token) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_lucky_token` |
| 4062 | Medallions $(medallion) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_medallion` |
| 4063 | Trophies $(trophy) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_trophy` |
| 4064 | Blood Crystals $(blood_crystal) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_blood_crystal` |
| 4065 | Ember Scales $(ember_scale) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_ember_scale` |
| 4066 | Void Shards $(void_shard) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_void_shard` |
| 4067 | Green Xenite $(xenite_green) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_xenite_green` |
| 4068 | Violet Xenite $(xenite_violet) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_xenite_violet` |
| 4069 | Cyan Xenite $(xenite_cyan) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_xenite_cyan` |
| 4070 | Red Xenite $(xenite_red) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_xenite_red` |
| 4071 | Deposit everything | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_every` |
| 4072 | « Back to your account / « Your account | Blood Crystals · The Rat Bank (p31/bank/pdlg_blood_crystal); Cyan Xenite · The Rat Bank (p31/bank/pdlg_xenite_cyan); Dread Tokens · The Rat Bank (p31/bank/pdlg_dread_token) (+11 more) | 400 | `p31/bank/act` [menu 400] → `p31/bank/open` |
| 4073 | Savings account | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/sav/btn` |
| 4074 | Exchange | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/xpage` |
| 4075 | 5 Tokens → 1 Medallion | The Exchange · The Rat Bank (p31/bank/xdlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/x0` |
| 4076 | 1 Medallion → 5 Tokens | The Exchange · The Rat Bank (p31/bank/xdlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/x1` |
| 4077 | 4 Medallions → 1 Trophy | The Exchange · The Rat Bank (p31/bank/xdlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/x2` |
| 4078 | 1 Trophy → 4 Medallions | The Exchange · The Rat Bank (p31/bank/xdlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/x3` |
| 4079 | Auto-deposit: $(ac) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/ac_toggle` |
| 4080 | 5 Trophies → 1 Dread Token | The Exchange · The Rat Bank (p31/bank/xdlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/xe0` |
| 4081 | 1 Dread Token → 5 Trophies | The Exchange · The Rat Bank (p31/bank/xdlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/xe1` |
| 4085 | Community Pots | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p178/pots/open` |
| 4090 | Dread Tokens $(dread_token) | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/page_dread_token` |
| 4101 | $(r_l0) | QUEEN AVA'S HONOURS · the Tide Font (p201/list_dlg) | 4100 | `p201/act` [menu 4100] → `p201/open` (if unless score @s bm.hns0 matches 1..) / `p201/act` [menu 4100] → (inline: scoreboard) / `p201/act` [menu 4100] → `p201/page` |
| 4102 | $(r_l1) | QUEEN AVA'S HONOURS · the Tide Font (p201/list_dlg) | 4100 | `p201/act` [menu 4100] → `p201/open` (if unless score @s bm.hns1 matches 1..) / `p201/act` [menu 4100] → (inline: scoreboard) / `p201/act` [menu 4100] → `p201/page` |
| 4103 | $(r_l2) | QUEEN AVA'S HONOURS · the Tide Font (p201/list_dlg) | 4100 | `p201/act` [menu 4100] → `p201/open` (if unless score @s bm.hns2 matches 1..) / `p201/act` [menu 4100] → (inline: scoreboard) / `p201/act` [menu 4100] → `p201/page` |
| 4105 | The Tide's Haste +1 ($(src)) | QUEEN AVA'S HONOURS · the Tide Font (p201/list_dlg) | 4100 | `p201/act` [menu 4100] → `p201/haste` |
| 4109 | « Her honours | QUEEN AVA'S HONOURS · $(r_nm) (p201/page_dlg) | 4100 | `p201/act` [menu 4100] → `p201/open` |
| 4111 | Honour +1 ($(hc)) | QUEEN AVA'S HONOURS · $(r_nm) (p201/page_dlg) | 4100 | `p201/act` [menu 4100] → `p201/buy` |
| 4201 | $(r_0md) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs0 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_md` (if if score @s bm.chs0 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_md` (if if score @s bm.chs0 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_md` (if if score @s bm.chs0 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_md` (if if score @s bm.chs0 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_md` (if if score @s bm.chs0 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_md` (if if score @s bm.chs0 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_md` (if if score @s bm.chs0 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_md` (if if score @s bm.chs0 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_md` (if if score @s bm.chs0 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_md` (if if score @s bm.chs0 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_md` (if if score @s bm.chs0 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_md` (if if score @s bm.chs0 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_md` (if if score @s bm.chs0 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_md` (if if score @s bm.chs0 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_md` (if if score @s bm.chs0 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_md` (if if score @s bm.chs0 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_md` (if if score @s bm.chs0 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_md` (if if score @s bm.chs0 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_md` (if if score @s bm.chs0 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_md` (if if score @s bm.chs0 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_md` (if if score @s bm.chs0 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_md` (if if score @s bm.chs0 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_md` (if if score @s bm.chs0 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_md` (if if score @s bm.chs0 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_md` (if if score @s bm.chs0 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_md` (if if score @s bm.chs0 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_md` (if if score @s bm.chs0 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_md` (if if score @s bm.chs0 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_md` (if if score @s bm.chs0 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_md` (if if score @s bm.chs0 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_md` (if if score @s bm.chs0 matches 31) |
| 4202 | $(r_0rg) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs0 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_rg` (if if score @s bm.chs0 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_rg` (if if score @s bm.chs0 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_rg` (if if score @s bm.chs0 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_rg` (if if score @s bm.chs0 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_rg` (if if score @s bm.chs0 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_rg` (if if score @s bm.chs0 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_rg` (if if score @s bm.chs0 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_rg` (if if score @s bm.chs0 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_rg` (if if score @s bm.chs0 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_rg` (if if score @s bm.chs0 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_rg` (if if score @s bm.chs0 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_rg` (if if score @s bm.chs0 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_rg` (if if score @s bm.chs0 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_rg` (if if score @s bm.chs0 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_rg` (if if score @s bm.chs0 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_rg` (if if score @s bm.chs0 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_rg` (if if score @s bm.chs0 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_rg` (if if score @s bm.chs0 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_rg` (if if score @s bm.chs0 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_rg` (if if score @s bm.chs0 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_rg` (if if score @s bm.chs0 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_rg` (if if score @s bm.chs0 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_rg` (if if score @s bm.chs0 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_rg` (if if score @s bm.chs0 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_rg` (if if score @s bm.chs0 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_rg` (if if score @s bm.chs0 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_rg` (if if score @s bm.chs0 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_rg` (if if score @s bm.chs0 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_rg` (if if score @s bm.chs0 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_rg` (if if score @s bm.chs0 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_rg` (if if score @s bm.chs0 matches 31) |
| 4203 | $(r_0au) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs0 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_au` (if if score @s bm.chs0 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_au` (if if score @s bm.chs0 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_au` (if if score @s bm.chs0 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_au` (if if score @s bm.chs0 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_au` (if if score @s bm.chs0 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_au` (if if score @s bm.chs0 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_au` (if if score @s bm.chs0 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_au` (if if score @s bm.chs0 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_au` (if if score @s bm.chs0 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_au` (if if score @s bm.chs0 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_au` (if if score @s bm.chs0 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_au` (if if score @s bm.chs0 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_au` (if if score @s bm.chs0 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_au` (if if score @s bm.chs0 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_au` (if if score @s bm.chs0 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_au` (if if score @s bm.chs0 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_au` (if if score @s bm.chs0 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_au` (if if score @s bm.chs0 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_au` (if if score @s bm.chs0 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_au` (if if score @s bm.chs0 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_au` (if if score @s bm.chs0 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_au` (if if score @s bm.chs0 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_au` (if if score @s bm.chs0 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_au` (if if score @s bm.chs0 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_au` (if if score @s bm.chs0 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_au` (if if score @s bm.chs0 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_au` (if if score @s bm.chs0 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_au` (if if score @s bm.chs0 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_au` (if if score @s bm.chs0 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_au` (if if score @s bm.chs0 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_au` (if if score @s bm.chs0 matches 31) |
| 4204 | $(r_1md) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs1 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_md` (if if score @s bm.chs1 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_md` (if if score @s bm.chs1 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_md` (if if score @s bm.chs1 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_md` (if if score @s bm.chs1 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_md` (if if score @s bm.chs1 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_md` (if if score @s bm.chs1 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_md` (if if score @s bm.chs1 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_md` (if if score @s bm.chs1 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_md` (if if score @s bm.chs1 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_md` (if if score @s bm.chs1 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_md` (if if score @s bm.chs1 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_md` (if if score @s bm.chs1 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_md` (if if score @s bm.chs1 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_md` (if if score @s bm.chs1 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_md` (if if score @s bm.chs1 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_md` (if if score @s bm.chs1 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_md` (if if score @s bm.chs1 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_md` (if if score @s bm.chs1 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_md` (if if score @s bm.chs1 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_md` (if if score @s bm.chs1 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_md` (if if score @s bm.chs1 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_md` (if if score @s bm.chs1 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_md` (if if score @s bm.chs1 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_md` (if if score @s bm.chs1 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_md` (if if score @s bm.chs1 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_md` (if if score @s bm.chs1 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_md` (if if score @s bm.chs1 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_md` (if if score @s bm.chs1 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_md` (if if score @s bm.chs1 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_md` (if if score @s bm.chs1 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_md` (if if score @s bm.chs1 matches 31) |
| 4205 | $(r_1rg) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs1 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_rg` (if if score @s bm.chs1 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_rg` (if if score @s bm.chs1 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_rg` (if if score @s bm.chs1 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_rg` (if if score @s bm.chs1 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_rg` (if if score @s bm.chs1 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_rg` (if if score @s bm.chs1 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_rg` (if if score @s bm.chs1 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_rg` (if if score @s bm.chs1 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_rg` (if if score @s bm.chs1 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_rg` (if if score @s bm.chs1 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_rg` (if if score @s bm.chs1 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_rg` (if if score @s bm.chs1 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_rg` (if if score @s bm.chs1 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_rg` (if if score @s bm.chs1 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_rg` (if if score @s bm.chs1 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_rg` (if if score @s bm.chs1 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_rg` (if if score @s bm.chs1 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_rg` (if if score @s bm.chs1 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_rg` (if if score @s bm.chs1 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_rg` (if if score @s bm.chs1 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_rg` (if if score @s bm.chs1 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_rg` (if if score @s bm.chs1 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_rg` (if if score @s bm.chs1 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_rg` (if if score @s bm.chs1 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_rg` (if if score @s bm.chs1 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_rg` (if if score @s bm.chs1 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_rg` (if if score @s bm.chs1 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_rg` (if if score @s bm.chs1 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_rg` (if if score @s bm.chs1 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_rg` (if if score @s bm.chs1 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_rg` (if if score @s bm.chs1 matches 31) |
| 4206 | $(r_1au) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs1 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_au` (if if score @s bm.chs1 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_au` (if if score @s bm.chs1 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_au` (if if score @s bm.chs1 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_au` (if if score @s bm.chs1 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_au` (if if score @s bm.chs1 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_au` (if if score @s bm.chs1 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_au` (if if score @s bm.chs1 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_au` (if if score @s bm.chs1 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_au` (if if score @s bm.chs1 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_au` (if if score @s bm.chs1 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_au` (if if score @s bm.chs1 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_au` (if if score @s bm.chs1 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_au` (if if score @s bm.chs1 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_au` (if if score @s bm.chs1 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_au` (if if score @s bm.chs1 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_au` (if if score @s bm.chs1 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_au` (if if score @s bm.chs1 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_au` (if if score @s bm.chs1 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_au` (if if score @s bm.chs1 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_au` (if if score @s bm.chs1 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_au` (if if score @s bm.chs1 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_au` (if if score @s bm.chs1 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_au` (if if score @s bm.chs1 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_au` (if if score @s bm.chs1 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_au` (if if score @s bm.chs1 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_au` (if if score @s bm.chs1 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_au` (if if score @s bm.chs1 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_au` (if if score @s bm.chs1 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_au` (if if score @s bm.chs1 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_au` (if if score @s bm.chs1 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_au` (if if score @s bm.chs1 matches 31) |
| 4207 | $(r_2md) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs2 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_md` (if if score @s bm.chs2 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_md` (if if score @s bm.chs2 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_md` (if if score @s bm.chs2 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_md` (if if score @s bm.chs2 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_md` (if if score @s bm.chs2 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_md` (if if score @s bm.chs2 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_md` (if if score @s bm.chs2 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_md` (if if score @s bm.chs2 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_md` (if if score @s bm.chs2 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_md` (if if score @s bm.chs2 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_md` (if if score @s bm.chs2 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_md` (if if score @s bm.chs2 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_md` (if if score @s bm.chs2 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_md` (if if score @s bm.chs2 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_md` (if if score @s bm.chs2 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_md` (if if score @s bm.chs2 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_md` (if if score @s bm.chs2 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_md` (if if score @s bm.chs2 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_md` (if if score @s bm.chs2 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_md` (if if score @s bm.chs2 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_md` (if if score @s bm.chs2 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_md` (if if score @s bm.chs2 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_md` (if if score @s bm.chs2 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_md` (if if score @s bm.chs2 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_md` (if if score @s bm.chs2 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_md` (if if score @s bm.chs2 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_md` (if if score @s bm.chs2 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_md` (if if score @s bm.chs2 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_md` (if if score @s bm.chs2 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_md` (if if score @s bm.chs2 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_md` (if if score @s bm.chs2 matches 31) |
| 4208 | $(r_2rg) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs2 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_rg` (if if score @s bm.chs2 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_rg` (if if score @s bm.chs2 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_rg` (if if score @s bm.chs2 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_rg` (if if score @s bm.chs2 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_rg` (if if score @s bm.chs2 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_rg` (if if score @s bm.chs2 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_rg` (if if score @s bm.chs2 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_rg` (if if score @s bm.chs2 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_rg` (if if score @s bm.chs2 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_rg` (if if score @s bm.chs2 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_rg` (if if score @s bm.chs2 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_rg` (if if score @s bm.chs2 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_rg` (if if score @s bm.chs2 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_rg` (if if score @s bm.chs2 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_rg` (if if score @s bm.chs2 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_rg` (if if score @s bm.chs2 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_rg` (if if score @s bm.chs2 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_rg` (if if score @s bm.chs2 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_rg` (if if score @s bm.chs2 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_rg` (if if score @s bm.chs2 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_rg` (if if score @s bm.chs2 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_rg` (if if score @s bm.chs2 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_rg` (if if score @s bm.chs2 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_rg` (if if score @s bm.chs2 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_rg` (if if score @s bm.chs2 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_rg` (if if score @s bm.chs2 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_rg` (if if score @s bm.chs2 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_rg` (if if score @s bm.chs2 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_rg` (if if score @s bm.chs2 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_rg` (if if score @s bm.chs2 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_rg` (if if score @s bm.chs2 matches 31) |
| 4209 | $(r_2au) | THE CHAMPION'S RIBBON · your Champions beside you (p205/rib_dlg) | 4200 | `p205/act` [menu 4200] → `p205/ribbon` (if unless score @s bm.chs2 matches 1..) / `p205/act` [menu 4200] → `p205/tg/cecil_au` (if if score @s bm.chs2 matches 1) / `p205/act` [menu 4200] → `p205/tg/emma_au` (if if score @s bm.chs2 matches 2) / `p205/act` [menu 4200] → `p205/tg/celi_au` (if if score @s bm.chs2 matches 3) / `p205/act` [menu 4200] → `p205/tg/zib_au` (if if score @s bm.chs2 matches 4) / `p205/act` [menu 4200] → `p205/tg/kw_au` (if if score @s bm.chs2 matches 5) / `p205/act` [menu 4200] → `p205/tg/leo_au` (if if score @s bm.chs2 matches 6) / `p205/act` [menu 4200] → `p205/tg/demo_au` (if if score @s bm.chs2 matches 7) / `p205/act` [menu 4200] → `p205/tg/apo_au` (if if score @s bm.chs2 matches 8) / `p205/act` [menu 4200] → `p205/tg/tul_au` (if if score @s bm.chs2 matches 9) / `p205/act` [menu 4200] → `p205/tg/frog_au` (if if score @s bm.chs2 matches 10) / `p205/act` [menu 4200] → `p205/tg/don_au` (if if score @s bm.chs2 matches 11) / `p205/act` [menu 4200] → `p205/tg/wil_au` (if if score @s bm.chs2 matches 12) / `p205/act` [menu 4200] → `p205/tg/fishy_au` (if if score @s bm.chs2 matches 13) / `p205/act` [menu 4200] → `p205/tg/dennis_au` (if if score @s bm.chs2 matches 14) / `p205/act` [menu 4200] → `p205/tg/pistachio_au` (if if score @s bm.chs2 matches 15) / `p205/act` [menu 4200] → `p205/tg/omega_au` (if if score @s bm.chs2 matches 16) / `p205/act` [menu 4200] → `p205/tg/ashur_au` (if if score @s bm.chs2 matches 17) / `p205/act` [menu 4200] → `p205/tg/chef_au` (if if score @s bm.chs2 matches 18) / `p205/act` [menu 4200] → `p205/tg/neighbor_au` (if if score @s bm.chs2 matches 19) / `p205/act` [menu 4200] → `p205/tg/ava_au` (if if score @s bm.chs2 matches 20) / `p205/act` [menu 4200] → `p205/tg/pearlq_au` (if if score @s bm.chs2 matches 21) / `p205/act` [menu 4200] → `p205/tg/bloo_au` (if if score @s bm.chs2 matches 22) / `p205/act` [menu 4200] → `p205/tg/stalker_au` (if if score @s bm.chs2 matches 23) / `p205/act` [menu 4200] → `p205/tg/lantern_au` (if if score @s bm.chs2 matches 24) / `p205/act` [menu 4200] → `p205/tg/bender_au` (if if score @s bm.chs2 matches 25) / `p205/act` [menu 4200] → `p205/tg/bones_au` (if if score @s bm.chs2 matches 26) / `p205/act` [menu 4200] → `p205/tg/capshun_au` (if if score @s bm.chs2 matches 27) / `p205/act` [menu 4200] → `p205/tg/pxcecil_au` (if if score @s bm.chs2 matches 28) / `p205/act` [menu 4200] → `p205/tg/pxleo_au` (if if score @s bm.chs2 matches 29) / `p205/act` [menu 4200] → `p205/tg/pxemma_au` (if if score @s bm.chs2 matches 30) / `p205/act` [menu 4200] → `p205/tg/sky_au` (if if score @s bm.chs2 matches 31) |
| 5001 | $(n1) $(p1) Medallions | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/buy1` |
| 5002 | $(n2) $(p2) Medallions | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/buy2` |
| 5003 | $(n3) $(p3) Medallions | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/buy3` |
| 5010 | Repair the item in my main hand 1 Medallion | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/repair` |
| 6001 | Go: $(t1) | Ring of Three Burrows (p29/burrow/dlg) | 600 | `p29/burrow/act` [menu 600] → `p29/burrow/go` |
| 6002 | Go: $(t2) | Ring of Three Burrows (p29/burrow/dlg) | 600 | `p29/burrow/act` [menu 600] → `p29/burrow/go` |
| 6003 | Go: $(t3) | Ring of Three Burrows (p29/burrow/dlg) | 600 | `p29/burrow/act` [menu 600] → `p29/burrow/go` |
| 6011 | Set burrow 1 here | Ring of Three Burrows (p29/burrow/dlg) | 600 | `p29/burrow/act` [menu 600] → `p29/burrow/set` |
| 6012 | Set burrow 2 here | Ring of Three Burrows (p29/burrow/dlg) | 600 | `p29/burrow/act` [menu 600] → `p29/burrow/set` |
| 6013 | Set burrow 3 here | Ring of Three Burrows (p29/burrow/dlg) | 600 | `p29/burrow/act` [menu 600] → `p29/burrow/set` |
| 7001 | Follow me | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/mode` |
| 7002 | Guard this spot | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/mode` |
| 7003 | Follow and scavenge | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/mode` |
| 7004 | Hand over the loot | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/handover` |
| 7005 | Pay a week 4 Tokens | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/pay` |
| 7006 | Call him to me | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/call` |
| 7007 | Patch him up 1 Medallion | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/patch` |
| 7101 | Yes - start over | Key of New Beginnings (p34/renew/use) | 950 | `p34/renew/act` [menu 950] |
| 7102 | No | Key of New Beginnings (p34/renew/use) | 950 | `p34/renew/act` [menu 950] → (does nothing) |
| 7201 | The Overworld | Dimension Shifter (p33/shift/use) | 900 | `p33/shift/act` [menu 900] → (inline: title) (if if dimension minecraft:overworld) / `p33/shift/act` [menu 900] → `p33/shift/to_ow` |
| 7202 | The Nether | Dimension Shifter (p33/shift/use) | 900 | `p33/shift/act` [menu 900] → (inline: title) (if if dimension minecraft:the_nether) / `p33/shift/act` [menu 900] → `p33/shift/to_nether` |
| 7203 | The End | Dimension Shifter (p33/shift/use) | 900 | `p33/shift/act` [menu 900] → (inline: title) (if if dimension minecraft:the_end) / `p33/shift/act` [menu 900] → `p33/shift/to_end` |
| 7301 | Speed | Emma's Ribbon (p57/menu_show); Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p57/set_mode` → (inline: title) |
| 7302 | Offense | Emma's Ribbon (p57/menu_show); Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p57/set_mode` → (inline: title) |
| 7303 | Defense | Emma's Ribbon (p57/menu_show); Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p57/set_mode` → (inline: title) |
| 7304 | Healing | Emma's Ribbon (p57/menu_show); Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p57/set_mode` → (inline: title) |
| 7305 | Mining | Emma's Ribbon (p57/menu_show); Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p57/set_mode` → (inline: title) |
| 7306 | Wardrobe | Emma's Ribbon (p57/menu_show); Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p119/plain/emma` |
| 7307 | Wraithfire Form: on / off | Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p127/em/toggle` |
| 7308 | Take back the heart | Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p127/em/take` |
| 7309 | Send her home | Emma's Ribbon (p57/menu_show); Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p57/dismiss` |
| 7310 | Fly with me | Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p130/menu_fly` |
| 7311 | Style: Guardian | Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p130/style` |
| 7312 | Style: Huntress | Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p130/style` |
| 7313 | Style: Tempest | Emma's Ribbon · the Wraithfire Heart (p127/em/menu_show) | 960 | `p57/act` [menu 960] → `p130/style` |
| 7601 | Tier I The Copper Strongroom | Plan a Heist (p70/menu_show) | 1100 | `p70/pick_tier` [menu 1100] |
| 7602 | Tier II The Silver Vaults | Plan a Heist (p70/menu_show) | 1100 | `p70/pick_tier` [menu 1100] |
| 7603 | Tier III The Gold Reserve | Plan a Heist (p70/menu_show) | 1100 | `p70/pick_tier` [menu 1100] |
| 7604 | Tier IV The Diamond Deposit | Plan a Heist (p70/menu_show) | 1100 | `p70/pick_tier` [menu 1100] |
| 7605 | Tier V The Gutter King's Hoard | Plan a Heist (p70/menu_show) | 1100 | `p70/pick_tier` [menu 1100] |
| 7606 | THE ENDLESS VAULT rooms without end | Plan a Heist (p70/menu_show) | 1100 | `p77/pick_mode` [menu 1100] |
| 7607 | THE PIT an arena of waves | Plan a Heist (p70/menu_show) | 1100 | `p77/pick_mode` [menu 1100] |
| 7611 | 3 TRIES +1 to +4 shares (by tier) - for the bold | How many tries? (p122/lives_show_na); How many tries? (p75/lives_show) | 1100 | `p75/pick_lives` [menu 1100] |
| 7612 | 5 TRIES +0 to +2 shares (by tier) | How many tries? (p122/lives_show_na); How many tries? (p75/lives_show) | 1100 | `p75/pick_lives` [menu 1100] |
| 7613 | 7 TRIES no bonus - for a first try | How many tries? (p122/lives_show_na); How many tries? (p75/lives_show) | 1100 | `p75/pick_lives` [menu 1100] |
| 7619 | ALARM: $(al) (click to switch) | How many tries? (p75/lives_show) | 1100 | `p90/alarm_toggle` [menu 1100] |
| 7711 (link) | [Accept] | p73/tp/ask_bring; p73/tp/ask_go | 0 | `p73/tp/accept` |
| 7712 (link) | [Deny] | p73/tp/ask_bring; p73/tp/ask_go | 0 | `p73/tp/deny` |
| 7720 | Back to the Overworld / [Back to the Overworld] | The heist is over (p101/ask_dlg); p101/ask_lead | — | `p101/act` → `p101/go_home` |
| 7721 | Start a new raid / [Start a new raid] | The heist is over (p101/ask_dlg); p101/ask_lead | — | `p101/act` → `p101/go_next` |
| 7722 | Count me in / [Count me in] | Another job? (p101/offer); Another job? (p103/offer_show); p101/offer | — | `p101/act` → `p101/opt_in` |
| 7723 | Head home / [Head home] | Another job? (p101/offer); Another job? (p103/offer_show); p101/offer | — | `p101/act` → `p101/opt_out` |
| 7724 | Leave now | Leave the heist? (p103/exit_ask) | — | `p103/act` → `p103/leave_yes` |
| 7725 | Stay | Leave the heist? (p103/exit_ask) | — | `p103/act` → `p103/leave_no` |
| 7726 | Head home now / [Head home now] | The heist is over (p103/mem_dlg); p101/wait_note | — | `p103/act` → `p103/mem_home` |
| 7727 | I'm in if we go again / [I'm in if we go again] | The heist is over (p103/mem_dlg); p101/wait_note | — | `p103/act` → `p103/pre_in` |
| 7728 | The Fixer's Office | The heist is over (p101/ask_dlg); The heist is over (p103/mem_dlg) | — | `p103/act` → `p80/office` |
| 7729 | Leave now | Leave the heist? (p104/leave_ask) | — | `p104/leave_now` |
| 7730 | Go to the Lounge | The heist is over (p101/ask_dlg) | — | `p121/act` → `p121/lead` |
| 7731 | Go to the Lounge | The heist is over (p103/mem_dlg) | — | `p121/act` → `p121/mem` |
| 7732 | Go to the Lounge | Another job? (p101/offer); Another job? (p103/offer_show) | — | `p121/act` → `p121/out` |
| 7733 (link) | [Skip this puzzle - costs a try] | p122/offer | — | `p122/ask` |
| 7734 | Skip it (costs a try) | Skip this puzzle? (p122/ask_dlg) | — | `p122/yes` |
| 7735 | Chatter: $(chat) (all followers) / Chatter: off / Chatter: on | 8-Bit Cecil · wardrobe (p99/dlg/pxcecil); 8-Bit Cecil's Cartridge (p213c/menu); 8-Bit Emma · wardrobe (p99/dlg/pxemma) (+62 more) | 960, 970, 2200, 2220, 2240, 2260, 2280, 2300, 2360, 2440, 2460, 2500, 2520, 2540, 2560, 2580, 2600, 2620, 2640, 2660, 2680, 2700, 2720, 2740, 2760, 2780, 2800, 2820, 2840, 2860, 2880, 2900, 2940, 2960, 2980, 3000, 3020, 3040, 3060, 3350, 8600, 8620, 8640, 8650, 9000, 9020, 9040, 9060, 9080, 9100, 9120, 9140, 9700, 9800, 9840, 9860, 9880, 9900, 9920, 9940 | `p123/chat` |
| 7736 | Pay the Fixer (half the pot, a share) | The Fixer's mercy (p166/m_dlg) | — | `p166/m_yes` |
| 7740 | « The Tailor | 8-BIT CECIL · the Tailor (p103/tl/p_pxcecil_dlg); 8-BIT EMMA · the Tailor (p103/tl/p_pxemma_dlg); 8-BIT LEO · the Tailor (p103/tl/p_pxleo_dlg) (+31 more) | 7740 | `p103/tl/act` → `p103/tl/main` |
| 7741 | Emma | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/p_emma` |
| 7742 | Celi | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/p_celi` |
| 7743 | Zib | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/p_zib` |
| 7744 | Cecil | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/p_cecil` |
| 7745 | KillerWatt | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/p_kw` |
| 7746 | Leo | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/p_leo` |
| 7747 | Democratus | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/p_demo` |
| 7748 | Display cases | p103/tl/main | 7740 | `p103/tl/act` → `p103/tl/cases` |
| 7750 | Gold $(r_0) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b0` [menu 7740] |
| 7751 | Midnight $(r_1) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b1` [menu 7740] |
| 7752 | Mint $(r_2) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b2` [menu 7740] |
| 7753 | Snow $(r_3) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b3` [menu 7740] |
| 7754 | Crimson $(r_4) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b4` [menu 7740] |
| 7755 | Phantom $(r_5) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b5` [menu 7740] |
| 7756 | Sundress $(r_6) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b6` [menu 7740] |
| 7757 | Midnight Gown $(r_7) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b7` [menu 7740] |
| 7758 | Sakura $(r_8) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b8` [menu 7740] |
| 7759 | Royal Gown $(r_9) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b9` [menu 7740] |
| 7760 | Starlight Gown $(r_10) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b10` [menu 7740] |
| 7761 | Gilded Gown $(r_11) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b11` [menu 7740] |
| 7762 | Diamond Gown $(r_12) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b12` [menu 7740] |
| 7763 | Netherite Gown $(r_13) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b13` [menu 7740] |
| 7764 | Flower Top $(r_14) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b14` [menu 7740] |
| 7765 | Cozy Sweater $(r_15) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b15` [menu 7740] |
| 7766 | Aurora $(r_16) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b16` [menu 7740] |
| 7767 | Rosehip $(r_17) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b17` [menu 7740] |
| 7768 | Midnight $(r_18) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b18` [menu 7740] |
| 7769 | Frostfire $(r_19) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b19` [menu 7740] |
| 7770 | Gilded $(r_20) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b20` [menu 7740] |
| 7771 | Diamond $(r_21) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b21` [menu 7740] |
| 7772 | Netherite $(r_22) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b22` [menu 7740] |
| 7773 | Crimson Guard $(r_23) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b23` [menu 7740] |
| 7774 | Forest Ranger $(r_24) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b24` [menu 7740] |
| 7775 | Golden Ace $(r_25) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b25` [menu 7740] |
| 7776 | Diamond Ace $(r_26) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b26` [menu 7740] |
| 7777 | Netherite Ace $(r_27) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b27` [menu 7740] |
| 7778 | Crimson Crusader $(r_28) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b28` [menu 7740] |
| 7779 | Royal Purple $(r_29) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b29` [menu 7740] |
| 7780 | Greenwood $(r_30) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b30` [menu 7740] |
| 7781 | Golden Champion $(r_31) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b31` [menu 7740] |
| 7782 | Diamond Champion $(r_32) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b32` [menu 7740] |
| 7783 | Netherite Champion $(r_33) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b33` [menu 7740] |
| 7784 | Crimson Reaper $(r_34) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b34` [menu 7740] |
| 7785 | Ashen Shroud $(r_35) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b35` [menu 7740] |
| 7786 | Royal Violet $(r_36) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b36` [menu 7740] |
| 7787 | Gilded Storm $(r_37) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b37` [menu 7740] |
| 7788 | Diamond Storm $(r_38) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b38` [menu 7740] |
| 7789 | Netherite Storm $(r_39) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b39` [menu 7740] |
| 7790 | Oak Display Case 3 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c0` [menu 7740] |
| 7791 | Dark Oak Display Case 3 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c1` [menu 7740] |
| 7792 | Quartz Display Case 5 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c2` [menu 7740] |
| 7793 | Gilded Display Case 8 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c3` [menu 7740] |
| 7800 | « Office / « The Office / ◀ The Office / Stay on the job | Leave the heist? (p104/leave_ask); THE ARMORY · your kits, for good (p80/armory_dlg); THE BOND SIGILS · two at most, each heist (p81/sigils_dlg) (+4 more) | 7801, 7802, 7803, 7804, 7807, 7808 | `p80/act` [menu 7800..7999] → `p80/office` |
| 7801 | « Armory / ⚒ Armory | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg); THE OFFENSE KIT · rank $(r2) (p80/rank2_dlg) (+5 more) | 7800, 7815, 7816, 7817, 7818, 7820, 7830 | `p80/act` [menu 7800..7999] → `p80/armory` |
| 7802 | « Back / Gutter Bank / ⛃ Gutter Bank / « Your account | CAPTAIN'S INSIGNIA · The Gutter Bank (p154/dlg_s6); COPPER COGS · The Gutter Bank (p154/dlg_s1); DEEP PEARLS · The Gutter Bank (p154/dlg_s4) (+11 more) | 7800, 7801, 7802, 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978 | `p80/act` [menu 7800..7999] → `p80/bank` |
| 7803 | 🏆 Trophy Case | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p81/case` |
| 7804 | ✦ Bond Sigils | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p81/sigils` |
| 7805 | ▣ Locker Hall | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p84/lk/from_ledger` |
| 7806 | ⛁ Crate Desk | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p86/theme/menu` |
| 7807 | « Raid Crew / ☺ Raid Crew | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg); p119/page | 7800, 7950 | `p80/act` [menu 7800..7999] → `p98/crew` |
| 7808 | ◀ The Codex / 📖 Codex | RAID ODDS · per raider, per won heist (p218/odds_dlg); THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) (+5 more) | 7800, 7808 | `p80/act` [menu 7800..7999] → `p117/cx/menu` |
| 7809 | ⚑ Plan a Heist | THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p70/plans` |
| 7811 | ⬆ Rank up | THE TANK KIT · rank $(r1) (p80/rank1_dlg) | 7815 | `p80/act` [menu 7800..7999] → `p80/up1` |
| 7812 | ⬆ Rank up | THE OFFENSE KIT · rank $(r2) (p80/rank2_dlg) | 7816 | `p80/act` [menu 7800..7999] → `p80/up2` |
| 7813 | ⬆ Rank up | THE RANGED KIT · rank $(r3) (p80/rank3_dlg) | 7817 | `p80/act` [menu 7800..7999] → `p80/up3` |
| 7814 | ⬆ Rank up | THE SUPPORT KIT · rank $(r4) (p80/rank4_dlg) | 7818 | `p80/act` [menu 7800..7999] → `p80/up4` |
| 7815 | Tank › | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/rank1` |
| 7816 | Offense › | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/rank2` |
| 7817 | Ranged › | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/rank3` |
| 7818 | Support › | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/rank4` |
| 7819 | none | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7820 | Secondary weapon | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/sec_menu` |
| 7821 | $(r_l0) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7822 | $(r_l1) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7823 | $(r_l2) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7824 | $(r_l3) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7825 | $(r_l4) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7826 | $(r_l5) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7827 | $(r_l6) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7828 | $(r_l7) | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7829 | none | YOUR SECONDARY · a weapon of your own (p80/sec_dlg) | 7820 | `p80/act` [menu 7800..7999] → `p80/sec_pick` |
| 7830 | Signature effect | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/sig_menu` |
| 7831 | $(r_l0) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7832 | $(r_l1) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7833 | $(r_l2) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7834 | $(r_l3) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7835 | $(r_l4) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7836 | $(r_l5) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7837 | $(r_l6) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7838 | $(r_l7) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7839 | $(r_l8) | YOUR SIGNATURE · an effect of your own (p80/sig_dlg) | 7830 | `p80/act` [menu 7800..7999] → `p80/sig_pick` |
| 7840 | ⬇ Deposit everything | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_deposit` |
| 7844 | Buy 1 Token (32) | THE GUTTER BANK · Black Market Tokens (p80/bank_tdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_buy1` |
| 7845 | Buy 10 Tokens (320) | THE GUTTER BANK · Black Market Tokens (p80/bank_tdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_buy10` |
| 7848 | ✦ Buy Tokens | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_tokens` |
| 7861 | 📖 Rooms of the Vault | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page1` |
| 7862 | 📖 Events and Secrets | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page2` |
| 7863 | 📖 Curses Lifted | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page3` |
| 7864 | 📖 Rare Finds | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page4` |
| 7865 | 📖 Masterworks | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page5` |
| 7866 | 🎲 Raid Odds | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p218/odds` |
| 7870 | ⇄ Change coins | GUTTER COINS · The Gutter Bank (p154/dlg_c); GUTTER MEDALLIONS · The Gutter Bank (p154/dlg_m); GUTTER TROPHIES · The Gutter Bank (p154/dlg_t) (+1 more) | 7802, 7970, 7971, 7972 | `p80/act` [menu 7800..7999] → `p120/bk_act` → `p120/bk_page` |
| 7875 | 16 coins → Medallion | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_c2m` |
| 7876 | 128 coins → Trophy | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_c2t` |
| 7877 | Medallion → 16 coins | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_m2c` |
| 7878 | Trophy → 128 coins | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_t2c` |
| 7879 | 8 Medallions → Trophy | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_m2t` |
| 7880 | ⌂ Fixer's Lounge | THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p121/from_ledger` |
| 7881 | ⏭ Skip this puzzle | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p122/ask` |
| 7883 | Trophy → 8 Medallions | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_t2m` |
| 7884 | The Stalker | p103/crew/row_20 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/stalker` |
| 7885 | The Arachno-Lantern | p103/crew/row_21 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/lantern` |
| 7886 | Bender | p103/crew/row_22 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/bender` |
| 7887 | Bones | p103/crew/row_23 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/bones` |
| 7888 | Mr. Capshun | p103/crew/row_24 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/capshun` |
| 7889 | The Sky Buddies | p103/crew/row_25 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/sky` |
| 7890 | 8-Bit Emma | p103/crew/row_26 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/pxemma` |
| 7891 | 8-Bit Leo | p103/crew/row_27 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/pxleo` |
| 7892 | 8-Bit Cecil | p103/crew/row_28 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/pxcecil` |
| 7899 | ⏏ Leave the heist | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p104/leave_ask` |
| 7900 | Cecil | p103/crew/row_0 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/cecil` |
| 7901 | Emma | p103/crew/row_1 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/emma` |
| 7902 | Celi | p103/crew/row_2 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/celi` |
| 7903 | Zib | p103/crew/row_3 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/zib` |
| 7904 | KillerWatt | p103/crew/row_4 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/killerwatt` |
| 7905 | Leo | p103/crew/row_5 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/leo` |
| 7906 | Democratus | p103/crew/row_6 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/demo` |
| 7907 | Skiff Escort | p103/crew/row_7 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/escort` |
| 7908 | Apophiss | p103/crew/row_8 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/apo` |
| 7909 | Tullius | p103/crew/row_9 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/tul` |
| 7910 | Fishy | p103/crew/row_10 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/fishy` |
| 7911 | Dennis | p103/crew/row_11 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/dennis` |
| 7912 | Pistachio | p103/crew/row_12 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/pistachio` |
| 7913 | Omega | p103/crew/row_13 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/omega` |
| 7914 | Ashur | p103/crew/row_14 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/ashur` |
| 7915 | The Chef | p103/crew/row_15 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/chef` |
| 7916 | The Neighbor | p103/crew/row_16 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/neighbor` |
| 7917 | Queen Ava | p103/crew/row_17 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/ava` |
| 7918 | Queen Pearl | p103/crew/row_18 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/pearlq` |
| 7919 | Bloo | p103/crew/row_19 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/bloo` |
| 7920 | The Frog | p103/crew/row_29 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/frog` |
| 7921 | Donado | p103/crew/row_30 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/donado` |
| 7931 | Knuckles | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h1` |
| 7932 | Doc Whiskers | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h2` |
| 7933 | Fingers | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h3` |
| 7934 | Tick-Tock | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h4` |
| 7935 | Boomer | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h5` |
| 7950 | Outfits & chatter / Outfits & Emma's buff | p98/crew | 7807 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/page` |
| 7951 | Emma's wardrobe | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/emma` |
| 7952 | Celi's wardrobe | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/celi` |
| 7953 | Zib's wardrobe | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/zib` |
| 7954 | Cecil's wardrobe | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/cecil` |
| 7955 | KillerWatt's wardrobe | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/kw` |
| 7956 | Leo's wardrobe | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/leo` |
| 7957 | Democratus's wardrobe | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/demo` |
| 7961 | Emma: Speed | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff1` |
| 7962 | Emma: Offense | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff2` |
| 7963 | Emma: Defense | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff3` |
| 7964 | Emma: Healing | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff4` |
| 7965 | Emma: Mining | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff5` |
| 7968 | Chatter on / off | p119/page | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/hush` |
| 7970 | Gutter Coins $(c) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_c` |
| 7971 | Gutter Medallions $(gm) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_m` |
| 7972 | Gutter Trophies $(gt) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_t` |
| 7973 | Copper Cogs $(m1) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_s1` |
| 7974 | Silver Seals $(m2) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_s2` |
| 7975 | Gilded Leaves $(m3) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_s3` |
| 7976 | Deep Pearls $(m4) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_s4` |
| 7977 | Hoard Embers $(m5) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_s5` |
| 7978 | Captain's Insignia $(m6) | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/page_s6` |
| 7980 | ⬇ Deposit 1 | CAPTAIN'S INSIGNIA · The Gutter Bank (p154/dlg_s6); COPPER COGS · The Gutter Bank (p154/dlg_s1); DEEP PEARLS · The Gutter Bank (p154/dlg_s4) (+6 more) | 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/dep` |
| 7981 | ⬇ Deposit 10 | CAPTAIN'S INSIGNIA · The Gutter Bank (p154/dlg_s6); COPPER COGS · The Gutter Bank (p154/dlg_s1); DEEP PEARLS · The Gutter Bank (p154/dlg_s4) (+6 more) | 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/dep` |
| 7982 | ⬇ Deposit all ($(h)) | CAPTAIN'S INSIGNIA · The Gutter Bank (p154/dlg_s6); COPPER COGS · The Gutter Bank (p154/dlg_s1); DEEP PEARLS · The Gutter Bank (p154/dlg_s4) (+6 more) | 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/dep` |
| 7983 | ⬆ Take 1 | CAPTAIN'S INSIGNIA · The Gutter Bank (p154/dlg_s6); COPPER COGS · The Gutter Bank (p154/dlg_s1); DEEP PEARLS · The Gutter Bank (p154/dlg_s4) (+6 more) | 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/take` |
| 7984 | ⬆ Take 10 | CAPTAIN'S INSIGNIA · The Gutter Bank (p154/dlg_s6); COPPER COGS · The Gutter Bank (p154/dlg_s1); DEEP PEARLS · The Gutter Bank (p154/dlg_s4) (+6 more) | 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/take` |
| 7985 | ⬆ Take all ($(n)) | CAPTAIN'S INSIGNIA · The Gutter Bank (p154/dlg_s6); COPPER COGS · The Gutter Bank (p154/dlg_s1); DEEP PEARLS · The Gutter Bank (p154/dlg_s4) (+6 more) | 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978 | `p80/act` [menu 7800..7999] → `p154/act` → `p154/take` |
| 8000 | « The Recruiter | p137/rc/gems; p137/rc/hires | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/main` |
| 8001 | Cecil 192 coins / Cecil IN YOUR PACK / Cecil SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f0` |
| 8002 | Emma 192 coins / Emma IN YOUR PACK / Emma SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f1` |
| 8003 | Celi 224 coins / Celi IN YOUR PACK / Celi SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f2` |
| 8004 | Zib 192 coins / Zib IN YOUR PACK / Zib SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f3` |
| 8005 | KillerWatt 320 coins / KillerWatt IN YOUR PACK / KillerWatt SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f4` |
| 8006 | Leo 208 coins / Leo IN YOUR PACK / Leo SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f5` |
| 8007 | Democratus 224 coins / Democratus IN YOUR PACK / Democratus SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f6` |
| 8008 | Skiff Escort 128 coins / Skiff Escort IN YOUR PACK / Skiff Escort SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f7` |
| 8009 | Apophiss 352 coins / Apophiss IN YOUR PACK / Apophiss SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f8` |
| 8010 | Tullius 336 coins / Tullius IN YOUR PACK / Tullius SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f9` |
| 8011 | Fishy 176 coins / Fishy IN YOUR PACK / Fishy SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f10` |
| 8012 | Dennis 176 coins / Dennis IN YOUR PACK / Dennis SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f11` |
| 8013 | Pistachio 176 coins / Pistachio IN YOUR PACK / Pistachio SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f12` |
| 8014 | Omega 176 coins / Omega IN YOUR PACK / Omega SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f13` |
| 8015 | Ashur 176 coins / Ashur IN YOUR PACK / Ashur SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f14` |
| 8016 | The Chef 176 coins / The Chef IN YOUR PACK / The Chef SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f15` |
| 8017 | The Neighbor 176 coins / The Neighbor IN YOUR PACK / The Neighbor SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f16` |
| 8018 | Queen Ava 176 coins / Queen Ava IN YOUR PACK / Queen Ava SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f17` |
| 8019 | Queen Pearl 176 coins / Queen Pearl IN YOUR PACK / Queen Pearl SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f18` |
| 8020 | Bloo 176 coins / Bloo IN YOUR PACK / Bloo SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f19` |
| 8021 | The Stalker 176 coins / The Stalker IN YOUR PACK / The Stalker SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f20` |
| 8022 | The Arachno-Lantern 176 coins / The Arachno-Lantern IN YOUR PACK / The Arachno-Lantern SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f21` |
| 8023 | Bender 176 coins / Bender IN YOUR PACK / Bender SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f22` |
| 8024 | Bones 176 coins / Bones IN YOUR PACK / Bones SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f23` |
| 8025 | Mr. Capshun 176 coins / Mr. Capshun IN YOUR PACK / Mr. Capshun SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f24` |
| 8026 | The Sky Buddies 176 coins / The Sky Buddies IN YOUR PACK / The Sky Buddies SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f25` |
| 8027 | 8-Bit Emma 176 coins / 8-Bit Emma IN YOUR PACK / 8-Bit Emma SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f26` |
| 8028 | 8-Bit Leo 176 coins / 8-Bit Leo IN YOUR PACK / 8-Bit Leo SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f27` |
| 8029 | 8-Bit Cecil 176 coins / 8-Bit Cecil IN YOUR PACK / 8-Bit Cecil SIGNED | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f28` |
| 8030 | The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f29` |
| 8031 | Donado 192 coins / Donado FILED / Donado IN YOUR PACK | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f30` |
| 8040 | Hirelings › | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/hires` |
| 8041 | Knuckles 48 coins / Knuckles FILED / Knuckles IN YOUR PACK | p137/rc/hires | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/h1` |
| 8042 | Doc Whiskers 64 coins / Doc Whiskers FILED / Doc Whiskers IN YOUR PACK | p137/rc/hires | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/h2` |
| 8043 | Fingers 48 coins / Fingers FILED / Fingers IN YOUR PACK | p137/rc/hires | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/h3` |
| 8044 | Tick-Tock 64 coins / Tick-Tock FILED / Tick-Tock IN YOUR PACK | p137/rc/hires | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/h4` |
| 8045 | Boomer 64 coins / Boomer FILED / Boomer IN YOUR PACK | p137/rc/hires | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/h5` |
| 8050 | Vault gems › | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/gems` |
| 8051 | Fire Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g0` |
| 8052 | Water Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g1` |
| 8053 | Poison Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g2` |
| 8054 | Earth Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g3` |
| 8055 | Electric Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g4` |
| 8056 | Rock Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g5` |
| 8057 | Air Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g6` |
| 8058 | Grass Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g7` |
| 8059 | Ice Gem 96 coins | p137/rc/gems | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/g8` |
| 8100 | Apophiss | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_apo` |
| 8101 | Tullius | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_tul` |
| 8102 | The Frog | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_frog` |
| 8103 | Donado | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_don` |
| 8104 | Pearlman | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_pearl` |
| 8105 | Wilfrey | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_wil` |
| 8106 | Auras (rare) | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/auras` |
| 8107 | Fishy | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_fishy` |
| 8108 | Dennis | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_dennis` |
| 8109 | Pistachio | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_pistachio` |
| 8110 | Crimson $(r_40) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b40` [menu 7740] |
| 8111 | Midnight $(r_41) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b41` [menu 7740] |
| 8112 | Bone $(r_42) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b42` [menu 7740] |
| 8113 | Gilded $(r_43) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b43` [menu 7740] |
| 8114 | Diamond $(r_44) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b44` [menu 7740] |
| 8115 | Netherite $(r_45) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b45` [menu 7740] |
| 8116 | Midnight $(r_46) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b46` [menu 7740] |
| 8117 | Bone $(r_47) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b47` [menu 7740] |
| 8118 | Neon $(r_48) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b48` [menu 7740] |
| 8119 | Golden Thunder $(r_49) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b49` [menu 7740] |
| 8120 | Diamond Thunder $(r_50) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b50` [menu 7740] |
| 8121 | Netherite Thunder $(r_51) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b51` [menu 7740] |
| 8122 | Obsidian Coil $(r_52) | APOPHISS · the Tailor (p103/tl/p_apo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b52` [menu 7740] |
| 8123 | Blood Wyrm $(r_53) | APOPHISS · the Tailor (p103/tl/p_apo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b53` [menu 7740] |
| 8124 | Frost Serpent $(r_54) | APOPHISS · the Tailor (p103/tl/p_apo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b54` [menu 7740] |
| 8125 | Gilded Coil $(r_55) | APOPHISS · the Tailor (p103/tl/p_apo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b55` [menu 7740] |
| 8126 | Diamond Coil $(r_56) | APOPHISS · the Tailor (p103/tl/p_apo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b56` [menu 7740] |
| 8127 | Netherite Coil $(r_57) | APOPHISS · the Tailor (p103/tl/p_apo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b57` [menu 7740] |
| 8128 | Admiral's Blue $(r_58) | TULLIUS · the Tailor (p103/tl/p_tul_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b58` [menu 7740] |
| 8129 | Corsair Crimson $(r_59) | TULLIUS · the Tailor (p103/tl/p_tul_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b59` [menu 7740] |
| 8130 | Bleached Bone $(r_60) | TULLIUS · the Tailor (p103/tl/p_tul_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b60` [menu 7740] |
| 8131 | Gilded Captain $(r_61) | TULLIUS · the Tailor (p103/tl/p_tul_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b61` [menu 7740] |
| 8132 | Diamond Captain $(r_62) | TULLIUS · the Tailor (p103/tl/p_tul_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b62` [menu 7740] |
| 8133 | Netherite Captain $(r_63) | TULLIUS · the Tailor (p103/tl/p_tul_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b63` [menu 7740] |
| 8134 | Bluejay $(r_64) | THE FROG · the Tailor (p103/tl/p_frog_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b64` [menu 7740] |
| 8135 | Ember Toad $(r_65) | THE FROG · the Tailor (p103/tl/p_frog_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b65` [menu 7740] |
| 8136 | Old Bog $(r_66) | THE FROG · the Tailor (p103/tl/p_frog_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b66` [menu 7740] |
| 8137 | Golden Prince $(r_67) | THE FROG · the Tailor (p103/tl/p_frog_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b67` [menu 7740] |
| 8138 | Diamond Prince $(r_68) | THE FROG · the Tailor (p103/tl/p_frog_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b68` [menu 7740] |
| 8139 | Netherite Prince $(r_69) | THE FROG · the Tailor (p103/tl/p_frog_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b69` [menu 7740] |
| 8140 | Chocolate $(r_70) | DONADO · the Tailor (p103/tl/p_don_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b70` [menu 7740] |
| 8141 | Midnight $(r_71) | DONADO · the Tailor (p103/tl/p_don_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b71` [menu 7740] |
| 8142 | Snowdrift $(r_72) | DONADO · the Tailor (p103/tl/p_don_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b72` [menu 7740] |
| 8143 | Starlit $(r_73) | DONADO · the Tailor (p103/tl/p_don_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b73` [menu 7740] |
| 8144 | Gilded $(r_74) | DONADO · the Tailor (p103/tl/p_don_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b74` [menu 7740] |
| 8145 | Diamond $(r_75) | DONADO · the Tailor (p103/tl/p_don_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b75` [menu 7740] |
| 8146 | Netherite $(r_76) | DONADO · the Tailor (p103/tl/p_don_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b76` [menu 7740] |
| 8147 | Ruby $(r_77) | PEARLMAN · the Tailor (p103/tl/p_pearl_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b77` [menu 7740] |
| 8148 | Emerald $(r_78) | PEARLMAN · the Tailor (p103/tl/p_pearl_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b78` [menu 7740] |
| 8149 | Amethyst $(r_79) | PEARLMAN · the Tailor (p103/tl/p_pearl_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b79` [menu 7740] |
| 8150 | Blossom Halo (Emma) 1280 coins / Blossom Halo (Emma) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a0` [menu 7740] |
| 8151 | Moonfrost Veil (Celi) 1280 coins / Moonfrost Veil (Celi) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a1` [menu 7740] |
| 8152 | Starfield Static (Zib) 1280 coins / Starfield Static (Zib) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a2` [menu 7740] |
| 8153 | Arcane Corona (Cecil) 1280 coins / Arcane Corona (Cecil) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a3` [menu 7740] |
| 8154 | Storm Crown (KillerWatt) 1280 coins / Storm Crown (KillerWatt) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a4` [menu 7740] |
| 8155 | Tidal Aegis (Leo) 1280 coins / Tidal Aegis (Leo) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a5` [menu 7740] |
| 8156 | Reaper's Shroud (Democratus) 1280 coins / Reaper's Shroud (Democratus) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a6` [menu 7740] |
| 8157 | Black-Flame Mantle (Apophiss) 1280 coins / Black-Flame Mantle (Apophiss) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a7` [menu 7740] |
| 8158 | Drowned Gale (Tullius) 1280 coins / Drowned Gale (Tullius) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a8` [menu 7740] |
| 8159 | Bog-Light Ring (the Frog) 1280 coins / Bog-Light Ring (the Frog) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a9` [menu 7740] |
| 8160 | Tractor Beam (Donado) 1280 coins / Tractor Beam (Donado) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a10` [menu 7740] |
| 8161 | Golden Gleam (Pearlman) 1280 coins / Golden Gleam (Pearlman) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a11` [menu 7740] |
| 8162 | Lordly Radiance (Wilfrey) 1280 coins / Lordly Radiance (Wilfrey) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a12` [menu 7740] |
| 8163 | Bubble Halo (Fishy) 1280 coins / Bubble Halo (Fishy) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a13` [menu 7740] |
| 8164 | Gilded $(r_80) | PEARLMAN · the Tailor (p103/tl/p_pearl_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b80` [menu 7740] |
| 8165 | Diamond $(r_81) | PEARLMAN · the Tailor (p103/tl/p_pearl_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b81` [menu 7740] |
| 8166 | Netherite $(r_82) | PEARLMAN · the Tailor (p103/tl/p_pearl_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b82` [menu 7740] |
| 8167 | Midnight Silk $(r_83) | FISHY · the Tailor (p103/tl/p_fishy_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b83` [menu 7740] |
| 8168 | Crimson Opera $(r_84) | FISHY · the Tailor (p103/tl/p_fishy_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b84` [menu 7740] |
| 8169 | Emerald Ascot $(r_85) | FISHY · the Tailor (p103/tl/p_fishy_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b85` [menu 7740] |
| 8170 | Gilded Topper $(r_86) | FISHY · the Tailor (p103/tl/p_fishy_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b86` [menu 7740] |
| 8171 | Diamond Topper $(r_87) | FISHY · the Tailor (p103/tl/p_fishy_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b87` [menu 7740] |
| 8172 | Netherite Topper $(r_88) | FISHY · the Tailor (p103/tl/p_fishy_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b88` [menu 7740] |
| 8173 | Crimson Cross $(r_89) | WILFREY · the Tailor (p103/tl/p_wil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b89` [menu 7740] |
| 8174 | Azure Chevron $(r_90) | WILFREY · the Tailor (p103/tl/p_wil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b90` [menu 7740] |
| 8175 | Verdant Bend $(r_91) | WILFREY · the Tailor (p103/tl/p_wil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b91` [menu 7740] |
| 8176 | Gilded Sun $(r_92) | WILFREY · the Tailor (p103/tl/p_wil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b92` [menu 7740] |
| 8177 | Diamond Sun $(r_93) | WILFREY · the Tailor (p103/tl/p_wil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b93` [menu 7740] |
| 8178 | Netherite Sun $(r_94) | WILFREY · the Tailor (p103/tl/p_wil_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b94` [menu 7740] |
| 8179 | Road Brown $(r_95) | DENNIS · the Tailor (p103/tl/p_dennis_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b95` [menu 7740] |
| 8180 | Biker Red $(r_96) | DENNIS · the Tailor (p103/tl/p_dennis_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b96` [menu 7740] |
| 8181 | Forest Leather $(r_97) | DENNIS · the Tailor (p103/tl/p_dennis_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b97` [menu 7740] |
| 8182 | Gilded Jacket $(r_98) | DENNIS · the Tailor (p103/tl/p_dennis_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b98` [menu 7740] |
| 8183 | Diamond Jacket $(r_99) | DENNIS · the Tailor (p103/tl/p_dennis_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b99` [menu 7740] |
| 8184 | Netherite Jacket $(r_100) | DENNIS · the Tailor (p103/tl/p_dennis_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b100` [menu 7740] |
| 8185 | Midnight Tails $(r_101) | PISTACHIO · the Tailor (p103/tl/p_pistachio_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b101` [menu 7740] |
| 8186 | Claret Tails $(r_102) | PISTACHIO · the Tailor (p103/tl/p_pistachio_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b102` [menu 7740] |
| 8187 | Ivory Tails $(r_103) | PISTACHIO · the Tailor (p103/tl/p_pistachio_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b103` [menu 7740] |
| 8188 | Gilded Tails $(r_104) | PISTACHIO · the Tailor (p103/tl/p_pistachio_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b104` [menu 7740] |
| 8189 | Diamond Tails $(r_105) | PISTACHIO · the Tailor (p103/tl/p_pistachio_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b105` [menu 7740] |
| 8190 | Netherite Tails $(r_106) | PISTACHIO · the Tailor (p103/tl/p_pistachio_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b106` [menu 7740] |
| 8191 | Spectral Blue $(r_107) | KING OMEGA · the Tailor (p103/tl/p_omega_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b107` [menu 7740] |
| 8192 | Blood Moon $(r_108) | KING OMEGA · the Tailor (p103/tl/p_omega_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b108` [menu 7740] |
| 8193 | Verdant Wraith $(r_109) | KING OMEGA · the Tailor (p103/tl/p_omega_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b109` [menu 7740] |
| 8194 | Gilded King $(r_110) | KING OMEGA · the Tailor (p103/tl/p_omega_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b110` [menu 7740] |
| 8195 | Diamond King $(r_111) | KING OMEGA · the Tailor (p103/tl/p_omega_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b111` [menu 7740] |
| 8196 | Gold Rush Glimmer (Dennis) 1280 coins / Gold Rush Glimmer (Dennis) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a14` [menu 7740] |
| 8197 | Ectoplasmic Mist (Pistachio) 1280 coins / Ectoplasmic Mist (Pistachio) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a15` [menu 7740] |
| 8198 | Court of Souls (King Omega) 1280 coins / Court of Souls (King Omega) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a16` [menu 7740] |
| 8199 | Ashfall Crown (Ashur) 1280 coins / Ashfall Crown (Ashur) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a17` [menu 7740] |
| 8200 | Netherite King $(r_112) | KING OMEGA · the Tailor (p103/tl/p_omega_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b112` [menu 7740] |
| 8201 | Blue Flame $(r_113) | ASHUR · the Tailor (p103/tl/p_ashur_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b113` [menu 7740] |
| 8202 | Verdant Ember $(r_114) | ASHUR · the Tailor (p103/tl/p_ashur_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b114` [menu 7740] |
| 8203 | Obsidian Rose $(r_115) | ASHUR · the Tailor (p103/tl/p_ashur_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b115` [menu 7740] |
| 8204 | Gilded Magma $(r_116) | ASHUR · the Tailor (p103/tl/p_ashur_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b116` [menu 7740] |
| 8205 | Diamond Magma $(r_117) | ASHUR · the Tailor (p103/tl/p_ashur_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b117` [menu 7740] |
| 8206 | Netherite Magma $(r_118) | ASHUR · the Tailor (p103/tl/p_ashur_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b118` [menu 7740] |
| 8207 | Midnight Brigade $(r_119) | THE CHEF · the Tailor (p103/tl/p_chef_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b119` [menu 7740] |
| 8208 | Bistro Blue $(r_120) | THE CHEF · the Tailor (p103/tl/p_chef_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b120` [menu 7740] |
| 8209 | Sommelier Wine $(r_121) | THE CHEF · the Tailor (p103/tl/p_chef_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b121` [menu 7740] |
| 8210 | Gilded Whites $(r_122) | THE CHEF · the Tailor (p103/tl/p_chef_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b122` [menu 7740] |
| 8211 | Diamond Whites $(r_123) | THE CHEF · the Tailor (p103/tl/p_chef_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b123` [menu 7740] |
| 8212 | Netherite Whites $(r_124) | THE CHEF · the Tailor (p103/tl/p_chef_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b124` [menu 7740] |
| 8213 | Navy Bandmaster $(r_125) | THE NEIGHBOR · the Tailor (p103/tl/p_neighbor_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b125` [menu 7740] |
| 8214 | Encore Crimson $(r_126) | THE NEIGHBOR · the Tailor (p103/tl/p_neighbor_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b126` [menu 7740] |
| 8215 | Jazz Violet $(r_127) | THE NEIGHBOR · the Tailor (p103/tl/p_neighbor_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b127` [menu 7740] |
| 8216 | Gilded Suit $(r_128) | THE NEIGHBOR · the Tailor (p103/tl/p_neighbor_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b128` [menu 7740] |
| 8217 | Diamond Suit $(r_129) | THE NEIGHBOR · the Tailor (p103/tl/p_neighbor_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b129` [menu 7740] |
| 8218 | Netherite Suit $(r_130) | THE NEIGHBOR · the Tailor (p103/tl/p_neighbor_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b130` [menu 7740] |
| 8219 | Coral Reef $(r_131) | QUEEN AVA · the Tailor (p103/tl/p_ava_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b131` [menu 7740] |
| 8220 | Abyssal Violet $(r_132) | QUEEN AVA · the Tailor (p103/tl/p_ava_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b132` [menu 7740] |
| 8221 | Kelp Forest $(r_133) | QUEEN AVA · the Tailor (p103/tl/p_ava_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b133` [menu 7740] |
| 8222 | Gilded Gown $(r_134) | QUEEN AVA · the Tailor (p103/tl/p_ava_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b134` [menu 7740] |
| 8223 | Diamond Gown $(r_135) | QUEEN AVA · the Tailor (p103/tl/p_ava_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b135` [menu 7740] |
| 8224 | Netherite Gown $(r_136) | QUEEN AVA · the Tailor (p103/tl/p_ava_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b136` [menu 7740] |
| 8225 | Coral Pink $(r_137) | QUEEN PEARL · the Tailor (p103/tl/p_pearlq_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b137` [menu 7740] |
| 8226 | Sunset Gold $(r_138) | QUEEN PEARL · the Tailor (p103/tl/p_pearlq_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b138` [menu 7740] |
| 8227 | Starlit Navy $(r_139) | QUEEN PEARL · the Tailor (p103/tl/p_pearlq_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b139` [menu 7740] |
| 8228 | Gilded Dress $(r_140) | QUEEN PEARL · the Tailor (p103/tl/p_pearlq_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b140` [menu 7740] |
| 8229 | Diamond Dress $(r_141) | QUEEN PEARL · the Tailor (p103/tl/p_pearlq_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b141` [menu 7740] |
| 8230 | Netherite Dress $(r_142) | QUEEN PEARL · the Tailor (p103/tl/p_pearlq_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b142` [menu 7740] |
| 8231 | Shadow Pelt $(r_143) | BLOO · the Tailor (p103/tl/p_bloo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b143` [menu 7740] |
| 8232 | Ember Mane $(r_144) | BLOO · the Tailor (p103/tl/p_bloo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b144` [menu 7740] |
| 8233 | Frost Coat $(r_145) | BLOO · the Tailor (p103/tl/p_bloo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b145` [menu 7740] |
| 8234 | Gilded Fur $(r_146) | BLOO · the Tailor (p103/tl/p_bloo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b146` [menu 7740] |
| 8235 | Diamond Fur $(r_147) | BLOO · the Tailor (p103/tl/p_bloo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b147` [menu 7740] |
| 8236 | Netherite Fur $(r_148) | BLOO · the Tailor (p103/tl/p_bloo_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b148` [menu 7740] |
| 8237 | Bone White $(r_149) | THE STALKER · the Tailor (p103/tl/p_stalker_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b149` [menu 7740] |
| 8238 | Ashen Grey $(r_150) | THE STALKER · the Tailor (p103/tl/p_stalker_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b150` [menu 7740] |
| 8239 | Blood Moon $(r_151) | THE STALKER · the Tailor (p103/tl/p_stalker_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b151` [menu 7740] |
| 8240 | Gilded Skin $(r_152) | THE STALKER · the Tailor (p103/tl/p_stalker_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b152` [menu 7740] |
| 8241 | Diamond Skin $(r_153) | THE STALKER · the Tailor (p103/tl/p_stalker_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b153` [menu 7740] |
| 8242 | Netherite Skin $(r_154) | THE STALKER · the Tailor (p103/tl/p_stalker_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b154` [menu 7740] |
| 8243 | Ghost Gourd $(r_155) | THE ARACHNO-LANTERN · the Tailor (p103/tl/p_lantern_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b155` [menu 7740] |
| 8244 | Soulfire Rind $(r_156) | THE ARACHNO-LANTERN · the Tailor (p103/tl/p_lantern_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b156` [menu 7740] |
| 8245 | Harvest Moon $(r_157) | THE ARACHNO-LANTERN · the Tailor (p103/tl/p_lantern_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b157` [menu 7740] |
| 8246 | Gilded Rind $(r_158) | THE ARACHNO-LANTERN · the Tailor (p103/tl/p_lantern_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b158` [menu 7740] |
| 8247 | Diamond Rind $(r_159) | THE ARACHNO-LANTERN · the Tailor (p103/tl/p_lantern_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b159` [menu 7740] |
| 8248 | Netherite Rind $(r_160) | THE ARACHNO-LANTERN · the Tailor (p103/tl/p_lantern_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b160` [menu 7740] |
| 8249 | Midnight Black $(r_161) | BENDER · the Tailor (p103/tl/p_bender_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b161` [menu 7740] |
| 8250 | Snow White $(r_162) | BENDER · the Tailor (p103/tl/p_bender_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b162` [menu 7740] |
| 8251 | Sable $(r_163) | BENDER · the Tailor (p103/tl/p_bender_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b163` [menu 7740] |
| 8252 | Gilded Coat $(r_164) | BENDER · the Tailor (p103/tl/p_bender_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b164` [menu 7740] |
| 8253 | Diamond Coat $(r_165) | BENDER · the Tailor (p103/tl/p_bender_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b165` [menu 7740] |
| 8254 | Netherite Coat $(r_166) | BENDER · the Tailor (p103/tl/p_bender_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b166` [menu 7740] |
| 8255 | Great White $(r_167) | BONES · the Tailor (p103/tl/p_bones_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b167` [menu 7740] |
| 8256 | Hammerhead Bronze $(r_168) | BONES · the Tailor (p103/tl/p_bones_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b168` [menu 7740] |
| 8257 | Abyss Black $(r_169) | BONES · the Tailor (p103/tl/p_bones_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b169` [menu 7740] |
| 8258 | Gilded Skin $(r_170) | BONES · the Tailor (p103/tl/p_bones_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b170` [menu 7740] |
| 8259 | Diamond Skin $(r_171) | BONES · the Tailor (p103/tl/p_bones_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b171` [menu 7740] |
| 8260 | Netherite Skin $(r_172) | BONES · the Tailor (p103/tl/p_bones_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b172` [menu 7740] |
| 8261 | Bubblegum Pink $(r_173) | THE SKY BUDDIES · the Tailor (p103/tl/p_sky_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b173` [menu 7740] |
| 8262 | Mint Dream $(r_174) | THE SKY BUDDIES · the Tailor (p103/tl/p_sky_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b174` [menu 7740] |
| 8263 | Lavender Night $(r_175) | THE SKY BUDDIES · the Tailor (p103/tl/p_sky_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b175` [menu 7740] |
| 8264 | Gilded Nightcap $(r_176) | THE SKY BUDDIES · the Tailor (p103/tl/p_sky_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b176` [menu 7740] |
| 8265 | Diamond Nightcap $(r_177) | THE SKY BUDDIES · the Tailor (p103/tl/p_sky_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b177` [menu 7740] |
| 8266 | Netherite Nightcap $(r_178) | THE SKY BUDDIES · the Tailor (p103/tl/p_sky_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b178` [menu 7740] |
| 8267 | Game Boy $(r_179) | 8-BIT EMMA · the Tailor (p103/tl/p_pxemma_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b179` [menu 7740] |
| 8268 | Virtual Boy $(r_180) | 8-BIT EMMA · the Tailor (p103/tl/p_pxemma_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b180` [menu 7740] |
| 8269 | Sepia Print $(r_181) | 8-BIT EMMA · the Tailor (p103/tl/p_pxemma_dlg) | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/b181` [menu 7740] |
| 8270 | King Omega | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_omega` |
| 8271 | Ashur | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_ashur` |
| 8272 | The Chef | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_chef` |
| 8273 | The Neighbor | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_neighbor` |
| 8274 | Queen Ava | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_ava` |
| 8275 | Queen Pearl | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_pearlq` |
| 8276 | Bloo | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_bloo` |
| 8277 | The Stalker | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_stalker` |
| 8278 | The Arachno-Lantern | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_lantern` |
| 8279 | Bender | p103/tl/main | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p103/tl/p_bender` |
| 8280 | Apophiss's wardrobe / Bones | p103/tl/main; p119/page | 7740, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/apo` |
| 8281 | Mr. Capshun / Tullius's wardrobe | p103/tl/main; p119/page | 7740, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/tul` |
| 8282 | 8-Bit Cecil / The Frog's wardrobe | p103/tl/main; p119/page | 7740, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/frog` |
| 8283 | 8-Bit Leo / Donado's wardrobe | p103/tl/main; p119/page | 7740, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/don` |
| 8284 | 8-Bit Emma / Pearlman's wardrobe | p103/tl/main; p119/page | 7740, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/pearl` |
| 8285 | The Sky Buddies / Wilfrey's wardrobe | p103/tl/main; p119/page | 7740, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/wil` |
| 8286 | Fishy's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/fishy` |
| 8287 | Dennis's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/dennis` |
| 8288 | Pistachio's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/pistachio` |
| 8289 | King Omega's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/omega` |
| 8290 | Ashur's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/ashur` |
| 8291 | The Chef's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/chef` |
| 8292 | The Neighbor's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/neighbor` |
| 8293 | Kitchen Steam (the Chef) 1280 coins / Kitchen Steam (the Chef) OWNED / Queen Ava's wardrobe | p103/tl/auras; p119/page | 7740, 7950 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a18` [menu 7740] / `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/ava` |
| 8294 | Grand Symphony (the Neighbor) 1280 coins / Grand Symphony (the Neighbor) OWNED / Queen Pearl's wardrobe | p103/tl/auras; p119/page | 7740, 7950 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a19` [menu 7740] / `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/pearlq` |
| 8295 | Bloo's wardrobe / Crown of the Deep (Queen Ava) 1280 coins / Crown of the Deep (Queen Ava) OWNED | p103/tl/auras; p119/page | 7740, 7950 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a20` [menu 7740] / `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/bloo` |
| 8296 | Pearlescent Tide (Queen Pearl) 1280 coins / Pearlescent Tide (Queen Pearl) OWNED / The Stalker's wardrobe | p103/tl/auras; p119/page | 7740, 7950 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a21` [menu 7740] / `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/stalker` |
| 8297 | The Arachno-Lantern's wardrobe / Feral Moon (Bloo) 1280 coins / Feral Moon (Bloo) OWNED | p103/tl/auras; p119/page | 7740, 7950 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a22` [menu 7740] / `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/lantern` |
| 8298 | Bender's wardrobe / The Long Night (The Stalker) 1280 coins / The Long Night (The Stalker) OWNED | p103/tl/auras; p119/page | 7740, 7950 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a23` [menu 7740] / `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/bender` |
| 8299 | Bones's wardrobe / Hallowfire (The Arachno-Lantern) 1280 coins / Hallowfire (The Arachno-Lantern) OWNED | p103/tl/auras; p119/page | 7740, 7950 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a24` [menu 7740] / `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/bones` |
| 8300 | Mr. Capshun's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/capshun` |
| 8301 | 8-Bit Cecil's wardrobe / Wait here / follow me | Pearlman's Business Card (p128/pm/menu); p119/page | 970, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/pxcecil` / `p128/pm/act` [menu 970] → `p128/pm/sit` |
| 8302 | 8-Bit Leo's wardrobe / Wardrobe | Pearlman's Business Card (p128/pm/menu); p119/page | 970, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/pxleo` / `p128/pm/act` [menu 970] → `p119/plain/pearl` |
| 8303 | 8-Bit Emma's wardrobe / Seasons | Pearlman's Business Card (p128/pm/menu); p119/page | 970, 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/pxemma` / `p128/pm/act` [menu 970] → `p209/menu` |
| 8304 | The Sky Buddies's wardrobe | p119/page | 7950 | `p119/act` (if if score @s bm.menu matches 7950) → `p119/wd/sky` / `p128/pm/act` [menu 970] |
| 8309 | Send him home | Pearlman's Business Card (p128/pm/menu) | 970 | `p128/pm/act` [menu 970] → `p128/pm/dismiss` |
| 8380 | Goodest Boy (Bender) 1280 coins / Goodest Boy (Bender) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a25` [menu 7740] |
| 8381 | Abyssal Tide (Bones) 1280 coins / Abyssal Tide (Bones) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a26` [menu 7740] |
| 8382 | Rainbow Doodles (Mr. Capshun) 1280 coins / Rainbow Doodles (Mr. Capshun) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a27` [menu 7740] |
| 8383 | Starry Sky (The Sky Buddies) 1280 coins / Starry Sky (The Sky Buddies) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a28` [menu 7740] |
| 8384 | Scanlines (8-Bit Emma) 1280 coins / Scanlines (8-Bit Emma) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a29` [menu 7740] |
| 8385 | Scanlines (8-Bit Leo) 1280 coins / Scanlines (8-Bit Leo) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a30` [menu 7740] |
| 8386 | Scanlines (8-Bit Cecil) 1280 coins / Scanlines (8-Bit Cecil) OWNED | p103/tl/auras | 7740 | `p103/tl/act` (if if score @s bm.menu matches 7740) → `p138/tl/a31` [menu 7740] |
| 8501 | Raw Materials Crate 16 coins | THE CRATE DESK · paid from your bank and pockets (p105/desk/show) | 8500 | `p105/desk/buy` [menu 8500] → (inline: scoreboard) / `p105/desk/buy` [menu 8500] → (inline: give) |
| 8502 | Adventurer's Crate 32 coins | THE CRATE DESK · paid from your bank and pockets (p105/desk/show) | 8500 | `p105/desk/buy` [menu 8500] → (inline: scoreboard) / `p105/desk/buy` [menu 8500] → (inline: give) |
| 8503 | Mineral Crate 48 coins | THE CRATE DESK · paid from your bank and pockets (p105/desk/show) | 8500 | `p105/desk/buy` [menu 8500] → (inline: scoreboard) / `p105/desk/buy` [menu 8500] → (inline: give) |
| 8504 | Crimson Tip-off 64 coins | THE CRATE DESK · paid from your bank and pockets (p105/desk/show) | 8500 | `p105/desk/buy` [menu 8500] → (inline: scoreboard) / `p105/desk/buy` [menu 8500] → (inline: give) |
| 8505 | Vorn Signal 64 coins | THE CRATE DESK · paid from your bank and pockets (p105/desk/show) | 8500 | `p105/desk/buy` [menu 8500] → (inline: scoreboard) / `p105/desk/buy` [menu 8500] → (inline: give) |
| 8506 | Stone Crate 6 coins | THE CRATE DESK · paid from your bank and pockets (p105/desk/show) | 8500 | `p105/desk/buy` [menu 8500] → (inline: scoreboard) / `p105/desk/buy` [menu 8500] → (inline: give) |
| 8507 | Timber Crate 8 coins | THE CRATE DESK · paid from your bank and pockets (p105/desk/show) | 8500 | `p105/desk/buy` [menu 8500] → (inline: scoreboard) / `p105/desk/buy` [menu 8500] → (inline: give) |
| 8601 | Sit / follow | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p131/sit` (if if entity @e[type=minecraft:wolf,tag=bm.apsel2]) |
| 8602 | Ride him | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p131/ride_ask` (if if entity @e[type=minecraft:wolf,tag=bm.apsel2]) |
| 8603 | Take off the saddle | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p131/unsaddle` (if if entity @e[type=minecraft:wolf,tag=bm.apsel2]) |
| 8604 | Wardrobe | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p119/plain/apo` |
| 8608 | Call for Apophiss | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p131/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.apsel2]) / `p131/act` [menu 8600] → `p131/recall` (if if entity @e[type=minecraft:wolf,tag=bm.apsel2]) |
| 8609 | Send him home | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p131/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.apsel2]) |
| 8621 | Sit / follow | Tullius's Frozen Doubloon (p132/menu) | 8620 | `p132/act` [menu 8620] → `p132/sit` (if if entity @e[type=minecraft:wolf,tag=bm.tusel2]) |
| 8624 | Wardrobe | Tullius's Frozen Doubloon (p132/menu) | 8620 | `p132/act` [menu 8620] → `p119/plain/tul` |
| 8628 | Call for Tullius | Tullius's Frozen Doubloon (p132/menu) | 8620 | `p132/act` [menu 8620] → `p132/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.tusel2]) / `p132/act` [menu 8620] → `p132/recall` (if if entity @e[type=minecraft:wolf,tag=bm.tusel2]) |
| 8629 | Send him home | Tullius's Frozen Doubloon (p132/menu) | 8620 | `p132/act` [menu 8620] → `p132/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.tusel2]) |
| 8641 | Sit / follow | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/sit` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8642 | Hand back my gear | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/strip` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8643 | Wardrobe | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p119/plain/frog` |
| 8648 | Call for the Frog | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/try` (if unless entity @e[type=minecraft:wolf,tag=bm.fgsel]) / `p136/fg/act` [menu 8640] → `p136/fg/recall` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8649 | Send him home | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/home` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8651 | Sit / follow | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/sit` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 8652 | Hand back my gear | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/strip` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 8653 | Wardrobe | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p119/plain/don` |
| 8658 | Call for Donado | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/try` (if unless entity @e[type=minecraft:wolf,tag=bm.dnsel]) / `p136/dn/act` [menu 8650] → `p136/dn/recall` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 8659 | Send him home | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/home` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 9000 | « Outfits & buffs / $(r_home) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/apo` [menu 9000] → `p125/hc/apo` |
| 9002 | His own scales $(r_apo0) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p99/pick/apo0` |
| 9003 | Obsidian Coil $(r_apo1) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p99/pick/apo1` |
| 9004 | Blood Wyrm $(r_apo2) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p99/pick/apo2` |
| 9005 | Frost Serpent $(r_apo3) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p99/pick/apo3` |
| 9006 | Gilded Coil $(r_apo4) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p99/pick/apo4` |
| 9007 | Diamond Coil $(r_apo5) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p99/pick/apo5` |
| 9008 | Netherite Coil $(r_apo6) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p99/pick/apo6` |
| 9018 | Pixel costume $(r_px) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p214/t/apo` |
| 9019 | Black-Flame Mantle $(r_aura) | Apophiss · wardrobe (p119/dlg/apo); Apophiss · wardrobe (p99/dlg/apo) | 9000 | `p99/act/apo` [menu 9000] → `p138/au/t_apo` |
| 9020 | « Outfits & buffs / $(r_home) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/tul` [menu 9020] → `p125/hc/tul` |
| 9022 | His old coat $(r_tul0) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p99/pick/tul0` |
| 9023 | Admiral's Blue $(r_tul1) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p99/pick/tul1` |
| 9024 | Corsair Crimson $(r_tul2) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p99/pick/tul2` |
| 9025 | Bleached Bone $(r_tul3) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p99/pick/tul3` |
| 9026 | Gilded Captain $(r_tul4) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p99/pick/tul4` |
| 9027 | Diamond Captain $(r_tul5) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p99/pick/tul5` |
| 9028 | Netherite Captain $(r_tul6) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p99/pick/tul6` |
| 9038 | Pixel costume $(r_px) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p214/t/tul` |
| 9039 | Drowned Gale $(r_aura) | Tullius · wardrobe (p119/dlg/tul); Tullius · wardrobe (p99/dlg/tul) | 9020 | `p99/act/tul` [menu 9020] → `p138/au/t_tul` |
| 9040 | « Outfits & buffs / $(r_home) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/frog` [menu 9040] → `p125/hc/frog` |
| 9042 | His own skin $(r_frog0) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p99/pick/frog0` |
| 9043 | Bluejay $(r_frog1) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p99/pick/frog1` |
| 9044 | Ember Toad $(r_frog2) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p99/pick/frog2` |
| 9045 | Old Bog $(r_frog3) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p99/pick/frog3` |
| 9046 | Golden Prince $(r_frog4) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p99/pick/frog4` |
| 9047 | Diamond Prince $(r_frog5) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p99/pick/frog5` |
| 9048 | Netherite Prince $(r_frog6) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p99/pick/frog6` |
| 9058 | Pixel costume $(r_px) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p214/t/frog` |
| 9059 | Bog-Light Ring $(r_aura) | the Frog with Mustache · wardrobe (p119/dlg/frog); the Frog with Mustache · wardrobe (p99/dlg/frog) | 9040 | `p99/act/frog` [menu 9040] → `p138/au/t_frog` |
| 9060 | « Outfits & buffs / $(r_home) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/don` [menu 9060] → `p125/hc/don` |
| 9062 | His own coat $(r_don0) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don0` |
| 9063 | Chocolate $(r_don1) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don1` |
| 9064 | Midnight $(r_don2) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don2` |
| 9065 | Snowdrift $(r_don3) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don3` |
| 9066 | Starlit $(r_don4) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don4` |
| 9067 | Gilded $(r_don5) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don5` |
| 9068 | Diamond $(r_don6) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don6` |
| 9069 | Netherite $(r_don7) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p99/pick/don7` |
| 9078 | Pixel costume $(r_px) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p214/t/don` |
| 9079 | Tractor Beam $(r_aura) | Donado · wardrobe (p119/dlg/don); Donado · wardrobe (p99/dlg/don) | 9060 | `p99/act/don` [menu 9060] → `p138/au/t_don` |
| 9080 | « Outfits & buffs / $(r_home) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/pearl` [menu 9080] → `p125/hc/pearl` |
| 9082 | The blue bow tie $(r_pearl0) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p99/pick/pearl0` |
| 9083 | Ruby $(r_pearl1) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p99/pick/pearl1` |
| 9084 | Emerald $(r_pearl2) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p99/pick/pearl2` |
| 9085 | Amethyst $(r_pearl3) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p99/pick/pearl3` |
| 9086 | Gilded $(r_pearl4) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p99/pick/pearl4` |
| 9087 | Diamond $(r_pearl5) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p99/pick/pearl5` |
| 9088 | Netherite $(r_pearl6) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p99/pick/pearl6` |
| 9098 | Pixel costume $(r_px) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p214/t/pearl` |
| 9099 | Golden Gleam $(r_aura) | Pearlman · wardrobe (p119/dlg/pearl); Pearlman · wardrobe (p99/dlg/pearl) | 9080 | `p99/act/pearl` [menu 9080] → `p138/au/t_pearl` |
| 9100 | « Outfits & buffs / $(r_home) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/wil` [menu 9100] → `p125/hc/wil` |
| 9102 | No shield $(r_wil0) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p99/pick/wil0` |
| 9103 | Crimson Cross $(r_wil1) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p99/pick/wil1` |
| 9104 | Azure Chevron $(r_wil2) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p99/pick/wil2` |
| 9105 | Verdant Bend $(r_wil3) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p99/pick/wil3` |
| 9106 | Gilded Sun $(r_wil4) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p99/pick/wil4` |
| 9107 | Diamond Sun $(r_wil5) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p99/pick/wil5` |
| 9108 | Netherite Sun $(r_wil6) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p99/pick/wil6` |
| 9118 | Pixel costume $(r_px) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p214/t/wil` |
| 9119 | Lordly Radiance $(r_aura) | Wilfrey · wardrobe (p119/dlg/wil); Wilfrey · wardrobe (p99/dlg/wil) | 9100 | `p99/act/wil` [menu 9100] → `p138/au/t_wil` |
| 9120 | « Outfits & buffs / $(r_home) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/fishy` [menu 9120] → `p125/hc/fishy` |
| 9122 | His old black topper $(r_fishy0) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p99/pick/fishy0` |
| 9123 | Midnight Silk $(r_fishy1) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p99/pick/fishy1` |
| 9124 | Crimson Opera $(r_fishy2) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p99/pick/fishy2` |
| 9125 | Emerald Ascot $(r_fishy3) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p99/pick/fishy3` |
| 9126 | Gilded Topper $(r_fishy4) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p99/pick/fishy4` |
| 9127 | Diamond Topper $(r_fishy5) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p99/pick/fishy5` |
| 9128 | Netherite Topper $(r_fishy6) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p99/pick/fishy6` |
| 9138 | Pixel costume $(r_px) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p214/t/fishy` |
| 9139 | Bubble Halo $(r_aura) | Fishy · wardrobe (p119/dlg/fishy); Fishy · wardrobe (p99/dlg/fishy) | 9120 | `p99/act/fishy` [menu 9120] → `p138/au/t_fishy` |
| 9141 | Sit / follow | Fishy's Pocket Bowl (p145/menu) | 9140 | `p145/act` [menu 9140] → `p145/sit` (if if entity @e[type=minecraft:wolf,tag=bm.fysel2]) |
| 9142 | Wardrobe | Fishy's Pocket Bowl (p145/menu) | 9140 | `p145/act` [menu 9140] → `p119/plain/fishy` |
| 9143 | The Cabinet | Fishy's Pocket Bowl (p145/menu) | 9140 | `p145/act` [menu 9140] → `p145/cab/main` |
| 9144 | Fishy's powers | Fishy's Pocket Bowl (p145/menu) | 9140 | `p145/act` [menu 9140] → `p145/cab/powers` |
| 9148 | Call for Fishy | Fishy's Pocket Bowl (p145/menu) | 9140 | `p145/act` [menu 9140] → `p145/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.fysel2]) / `p145/act` [menu 9140] → `p145/recall` (if if entity @e[type=minecraft:wolf,tag=bm.fysel2]) |
| 9149 | Send him home | Fishy's Pocket Bowl (p145/menu) | 9140 | `p145/act` [menu 9140] → `p145/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.fysel2]) |
| 9150 | « The Cabinet | FISHY'S POWERS · taught by the Cabinet (p145/cab/powers_dlg); THE COURT · $(n) of 20 (p145/pg/court_dlg); THE DEEP · $(n) of 20 (p145/pg/deep_dlg) (+4 more) | 9150 | `p145/cab/act` [menu 9150] → `p145/cab/main` |
| 9151 | The Hollow $(c_hollow) of 20$(r_hollow) | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/pg/hollow` |
| 9152 | The Gutter $(c_gutter) of 20$(r_gutter) | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/pg/gutter` |
| 9153 | The Skies $(c_skies) of 20$(r_skies) | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/pg/skies` |
| 9154 | The Deep $(c_deep) of 20$(r_deep) | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/pg/deep` |
| 9155 | The Wilds $(c_wilds) of 20$(r_wilds) | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/pg/wilds` |
| 9156 | The Court $(c_court) of 20$(r_court) | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/pg/court` |
| 9157 | Fishy's powers | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/cab/powers` |
| 9158 | Set it out in the hall | THE COURT · $(n) of 20 (p145/pg/court_dlg); THE DEEP · $(n) of 20 (p145/pg/deep_dlg); THE GUTTER · $(n) of 20 (p145/pg/gutter_dlg) (+3 more) | 9150 | `p145/cab/act` [menu 9150] → `p145/cab/set_out` |
| 9159 | A spare Pocket Bowl | FISHY'S CABINET OF CURIOSITIES (p145/cab/main_dlg) | 9150 | `p145/cab/act` [menu 9150] → `p145/cab/spare` |
| 9701 | Duel him | Democratus' Challenge (p97/menu) | 9700 | `p97/act` [menu 9700] → `p97/duel/start` |
| 9702 | Call for Democratus / Send him home | Democratus' Challenge (p97/menu) | 9700 | `p97/act` [menu 9700] → `p125/hc/demo` |
| 9703 | Wardrobe | Democratus' Challenge (p97/menu) | 9700 | `p97/act` [menu 9700] → `p119/plain/demo` |
| 9800 | « Outfits & buffs / $(r_home) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/emma` [menu 9800] → `p125/hc/emma` |
| 9802 | Pink ribbon $(r_ribbon0) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/ribbon0` |
| 9803 | Gold $(r_ribbon1) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/ribbon1` |
| 9804 | Midnight $(r_ribbon2) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/ribbon2` |
| 9805 | Mint $(r_ribbon3) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/ribbon3` |
| 9806 | Snow $(r_ribbon4) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/ribbon4` |
| 9807 | Crimson $(r_ribbon5) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/ribbon5` |
| 9808 | Phantom $(r_ribbon6) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/ribbon6` |
| 9812 | Her own dress $(r_dress0) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress0` |
| 9813 | Sundress $(r_dress1) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress1` |
| 9814 | Midnight Gown $(r_dress2) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress2` |
| 9815 | Sakura $(r_dress3) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress3` |
| 9816 | Royal Gown $(r_dress4) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress4` |
| 9817 | Starlight Gown $(r_dress5) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress5` |
| 9818 | Gilded Gown $(r_dress6) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress6` |
| 9819 | Diamond Gown $(r_dress7) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress7` |
| 9820 | Netherite Gown $(r_dress8) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/dress8` |
| 9823 | Flower Top $(r_outfit1) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/outfit1` |
| 9824 | Cozy Sweater $(r_outfit2) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p99/pick/outfit2` |
| 9837 | KillerWatt look $(r_kw) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p217/kw/t` |
| 9839 | Blossom Halo $(r_aura) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act/emma` [menu 9800] → `p138/au/t_emma` |
| 9840 | « Outfits & buffs / $(r_home) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/celi` [menu 9840] → `p125/hc/celi` |
| 9842 | Own clothes $(r_celi0) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi0` |
| 9843 | Aurora $(r_celi1) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi1` |
| 9844 | Rosehip $(r_celi2) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi2` |
| 9845 | Midnight $(r_celi3) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi3` |
| 9846 | Frostfire $(r_celi4) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi4` |
| 9847 | Gilded $(r_celi5) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi5` |
| 9848 | Diamond $(r_celi6) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi6` |
| 9849 | Netherite $(r_celi7) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p99/pick/celi7` |
| 9858 | Pixel costume $(r_px) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p214/t/celi` |
| 9859 | Moonfrost Veil $(r_aura) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act/celi` [menu 9840] → `p138/au/t_celi` |
| 9860 | « Outfits & buffs / $(r_home) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/zib` [menu 9860] → `p125/hc/zib` |
| 9862 | Own clothes $(r_zib0) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p99/pick/zib0` |
| 9863 | Crimson Guard $(r_zib1) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p99/pick/zib1` |
| 9864 | Forest Ranger $(r_zib2) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p99/pick/zib2` |
| 9865 | Golden Ace $(r_zib3) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p99/pick/zib3` |
| 9866 | Diamond Ace $(r_zib4) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p99/pick/zib4` |
| 9867 | Netherite Ace $(r_zib5) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p99/pick/zib5` |
| 9878 | Pixel costume $(r_px) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p214/t/zib` |
| 9879 | Starfield Static $(r_aura) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act/zib` [menu 9860] → `p138/au/t_zib` |
| 9880 | « Outfits & buffs / $(r_home) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/cecil` [menu 9880] → `p125/hc/cecil` |
| 9882 | Own colours $(r_cecil0) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p99/pick/cecil0` |
| 9883 | Crimson $(r_cecil1) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p99/pick/cecil1` |
| 9884 | Midnight $(r_cecil2) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p99/pick/cecil2` |
| 9885 | Bone $(r_cecil3) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p99/pick/cecil3` |
| 9886 | Gilded $(r_cecil4) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p99/pick/cecil4` |
| 9887 | Diamond $(r_cecil5) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p99/pick/cecil5` |
| 9888 | Netherite $(r_cecil6) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p99/pick/cecil6` |
| 9899 | Arcane Corona $(r_aura) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act/cecil` [menu 9880] → `p138/au/t_cecil` |
| 9900 | « Outfits & buffs / $(r_home) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/kw` [menu 9900] → `p125/hc/kw` |
| 9902 | Own colours $(r_kw0) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p99/pick/kw0` |
| 9903 | Midnight $(r_kw1) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p99/pick/kw1` |
| 9904 | Bone $(r_kw2) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p99/pick/kw2` |
| 9905 | Neon $(r_kw3) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p99/pick/kw3` |
| 9906 | Golden Thunder $(r_kw4) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p99/pick/kw4` |
| 9907 | Diamond Thunder $(r_kw5) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p99/pick/kw5` |
| 9908 | Netherite Thunder $(r_kw6) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p99/pick/kw6` |
| 9918 | Pixel costume $(r_px) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p214/t/kw` |
| 9919 | Storm Crown $(r_aura) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act/kw` [menu 9900] → `p138/au/t_kw` |
| 9920 | « Outfits & buffs / $(r_home) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/leo` [menu 9920] → `p125/hc/leo` |
| 9922 | Own clothes $(r_leo0) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p99/pick/leo0` |
| 9923 | Crimson Crusader $(r_leo1) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p99/pick/leo1` |
| 9924 | Royal Purple $(r_leo2) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p99/pick/leo2` |
| 9925 | Greenwood $(r_leo3) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p99/pick/leo3` |
| 9926 | Golden Champion $(r_leo4) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p99/pick/leo4` |
| 9927 | Diamond Champion $(r_leo5) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p99/pick/leo5` |
| 9928 | Netherite Champion $(r_leo6) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p99/pick/leo6` |
| 9939 | Tidal Aegis $(r_aura) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act/leo` [menu 9920] → `p138/au/t_leo` |
| 9940 | « Outfits & buffs / $(r_home) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act/demo` [menu 9940] → `p125/hc/demo` |
| 9942 | Own clothes $(r_demo0) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p99/pick/demo0` |
| 9943 | Crimson Reaper $(r_demo1) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p99/pick/demo1` |
| 9944 | Ashen Shroud $(r_demo2) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p99/pick/demo2` |
| 9945 | Royal Violet $(r_demo3) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p99/pick/demo3` |
| 9946 | Gilded Storm $(r_demo4) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p99/pick/demo4` |
| 9947 | Diamond Storm $(r_demo5) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p99/pick/demo5` |
| 9948 | Netherite Storm $(r_demo6) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p99/pick/demo6` |
| 9958 | Pixel costume $(r_px) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p214/t/demo` |
| 9959 | Reaper's Shroud $(r_aura) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act/demo` [menu 9940] → `p138/au/t_demo` |

## Built at run time

Codes a function fills in with a macro - check these by hand.

| Code | Words | Shown in |
|---|---|---|
| `$(bring)` | Bring $(nm) | p73/tp/btn2 |
| `$(go)` | Go to $(nm) | p73/tp/btn2 |

## Menus

`scoreboard players set @s bm.menu N` - the menu a player has open; the routers check it.

| Menu | Set by | Dialog |
|---:|---|---|
| 0 | p136/dn/act, p136/fg/act, p33/shift/act, p34/renew/act, p73/tp/ask_bring (+1) |  |
| 1 | p28/standing/show |  |
| 101 | p28/back/open_1 | The Fence - Back Room |
| 102 | p28/back/open_2 | Old Barnaby - Back Room |
| 103 | p28/back/open_3 | Madame Velour - Back Room |
| 104 | p28/back/open_4 | Vinny 'Two-Blades' - Back Room |
| 105 | p28/back/open_5 | Sgt. Steelwhisker - Back Room |
| 106 | p28/back/open_6 | Chef Fromage - Back Room |
| 107 | p28/back/open_7 | Prof. Whiskerton - Back Room |
| 108 | p28/back/open_8 | Lucky Whiskers - Back Room |
| 109 | p28/back/open_9 | Capt. Cheddarbeard - Back Room |
| 110 | p28/back/open_10 | The Bloodbroker - Back Room |
| 201 | p28/gate/pass_menu | The Dark Auction |
| 300 | p30/menu | The Dark Auction |
| 400 | p31/bank/open, p31/bank/page_blood_crystal, p31/bank/page_dread_token, p31/bank/page_ember_scale, p31/bank/page_lucky_token (+10) | Blood Crystals · The Rat Bank / Cyan Xenite · The Rat Bank / Dread Tokens · The Rat Bank |
| 500 | p31/conc/open | The Concierge |
| 600 | p29/burrow/use | Ring of Three Burrows |
| 700 | p29/merc/use | Rufus Gnaw, rat for hire |
| 900 | p33/shift/use | Dimension Shifter |
| 950 | p34/renew/use | Key of New Beginnings |
| 960 | p57/menu | Emma's Ribbon / Emma's Ribbon · the Wraithfire Heart |
| 970 | p128/pm/menu | Pearlman's Business Card |
| 971 | p209/menu | Pearlman's Seasons |
| 1100 | p70/menu, p75/lives_menu | How many tries? / Plan a Heist |
| 1310 | p73/tp/use |  |
| 2100 | p162/dw/pg2100 | DENNIS'S ASSAY OFFICE |
| 2150 | p162/ps/pg2151, p162/ps/pg2152 | PISTACHIO'S PANTRY / PISTACHIO'S PANTRY · rare parts |
| 2200 | p163/dw/menu, p163/dw/powers | DENNIS'S WAYS / Dennis's Horn |
| 2220 | p163/pi/menu, p163/pi/powers | PISTACHIO'S WAYS / Pistachio's Little Cloche |
| 2240 | p99/menu/dennis | Dennis · wardrobe |
| 2260 | p99/menu/pistachio | Pistachio · wardrobe |
| 2280 | p170/menu, p170/powers | KING OMEGA'S WAYS / Omega's Monocle |
| 2300 | p99/menu/omega | King Omega · wardrobe |
| 2320 | p169/court/chron, p169/court/garr, p169/court/main, p169/court/peer, p169/court/read0 (+9) | KING OMEGA / THE GHOST GARRISON / THE PEERAGE |
| 2360 | p173/wil/menu | Wilfrey's Locket |
| 2400 | p171/open | WHO'S WHERE · the rat town |
| 2440 | p185/menu, p185/powers | ASHUR'S WAYS / Ashur's Cinder |
| 2460 | p99/menu/ashur | Ashur · wardrobe |
| 2500 | p186/menu, p186/powers | THE CHEF'S WAYS / The Golden Ladle |
| 2520 | p99/menu/chef | the Chef · wardrobe |
| 2540 | p187/menu, p187/powers | THE NEIGHBOR'S WAYS / The Neighbor's Baton |
| 2560 | p99/menu/neighbor | the Neighbor · wardrobe |
| 2580 | p189/menu, p189/powers, p189/story | QUEEN AVA'S STORY / QUEEN AVA'S WAYS / Queen Ava's Locket |
| 2600 | p190/menu, p190/powers, p190/story | QUEEN PEARL'S STORY / QUEEN PEARL'S WAYS / Queen Pearl's Pearls |
| 2620 | p191/menu, p191/powers, p191/story | BLOO'S STORY / BLOO'S WAYS / Bloo's Claw |
| 2640 | p99/menu/ava | Queen Ava · wardrobe |
| 2660 | p99/menu/pearlq | Queen Pearl · wardrobe |
| 2680 | p99/menu/bloo | Bloo · wardrobe |
| 2700 | p193/menu, p193/powers | THE STALKER'S WAYS / The Hollow Hook |
| 2720 | p99/menu/stalker | The Stalker · wardrobe |
| 2740 | p194/menu, p194/powers | Kindled Gourd / THE ARACHNO-LANTERN'S WAYS |
| 2760 | p99/menu/lantern | The Arachno-Lantern · wardrobe |
| 2780 | p195/menu, p195/powers | BENDER'S WAYS / Bender's Ball |
| 2800 | p99/menu/bender | Bender · wardrobe |
| 2820 | p196/menu, p196/powers | BONES' WAYS / Bones's Whistle |
| 2840 | p99/menu/bones | Bones · wardrobe |
| 2860 | p198/menu, p198/pal, p198/powers | MR. CAPSHUN'S PALETTE / MR. CAPSHUN'S WAYS / Mr. Capshun's Pencil |
| 2880 | p99/menu/capshun | Mr. Capshun · wardrobe |
| 2900 | p99/menu/sky | The Sky Buddies · wardrobe |
| 2940 | p211/menu, p211/powers, p211/wx/open | THE SKY BUDDIES' WAYS / THE SKY, YOURS / The Sky Mobile |
| 2960 | p99/menu/pxemma | 8-Bit Emma · wardrobe |
| 2980 | p213e/menu, p213e/powers | 8-BIT EMMA'S WAYS / 8-Bit Emma's Cartridge |
| 3000 | p99/menu/pxleo | 8-Bit Leo · wardrobe |
| 3020 | p213l/menu, p213l/powers | 8-BIT LEO'S WAYS / 8-Bit Leo's Cartridge |
| 3040 | p99/menu/pxcecil | 8-Bit Cecil · wardrobe |
| 3060 | p213c/menu, p213c/powers | 8-BIT CECIL'S WAYS / 8-Bit Cecil's Cartridge |
| 3200 | p177/about, p177/open, p177/rf, p177/tune | About the Dread / Reforging · past the old maximum / Tuning · a tool |
| 3300 | p178/pots/open, p178/pots/page0, p178/pots/page1, p178/pots/page2, p178/pots/page3 (+2) | Bounty Office · Community Pots / Community Pots · The Rat Bank / Couriers' Guild · Community Pots |
| 3350 | p179/w/open, p220/open | Follower Gallery |
| 4100 | p201/open, p201/page | QUEEN AVA'S HONOURS · $(r_nm) / QUEEN AVA'S HONOURS · the Tide Font |
| 4200 | p205/ribbon | THE CHAMPION'S RIBBON · your Champions beside you |
| 7740 | p103/tl/auras, p103/tl/cases, p103/tl/main, p103/tl/p_apo, p103/tl/p_ashur (+30) | 8-BIT CECIL · the Tailor / 8-BIT EMMA · the Tailor / 8-BIT LEO · the Tailor |
| 7800 | p80/office | THE FIXER'S OFFICE · everything the vault owes you |
| 7801 | p80/armory | THE ARMORY · your kits, for good |
| 7802 | p120/bk_page, p80/bank, p80/bank_tokens | THE GUTTER BANK · Black Market Tokens / THE GUTTER BANK · Medallions & Trophies / THE GUTTER BANK · your coins and spoils |
| 7803 | p81/case | THE TROPHY CASE · twelve rooms, six metals |
| 7804 | p81/sigils | THE BOND SIGILS · two at most, each heist |
| 7807 | p98/crew |  |
| 7808 | p117/cx/menu, p117/cx/page1, p117/cx/page2, p117/cx/page3, p117/cx/page4 (+2) | RAID ODDS · per raider, per won heist / THE CODEX · what you've seen in the vault / 📖 Curses Lifted · $(n) of 7 |
| 7815 | p80/rank1 | THE TANK KIT · rank $(r1) |
| 7816 | p80/rank2 | THE OFFENSE KIT · rank $(r2) |
| 7817 | p80/rank3 | THE RANGED KIT · rank $(r3) |
| 7818 | p80/rank4 | THE SUPPORT KIT · rank $(r4) |
| 7820 | p80/sec_menu | YOUR SECONDARY · a weapon of your own |
| 7830 | p80/sig_menu | YOUR SIGNATURE · an effect of your own |
| 7950 | p119/page |  |
| 7970 | p154/page_c | GUTTER COINS · The Gutter Bank |
| 7971 | p154/page_m | GUTTER MEDALLIONS · The Gutter Bank |
| 7972 | p154/page_t | GUTTER TROPHIES · The Gutter Bank |
| 7973 | p154/page_s1 | COPPER COGS · The Gutter Bank |
| 7974 | p154/page_s2 | SILVER SEALS · The Gutter Bank |
| 7975 | p154/page_s3 | GILDED LEAVES · The Gutter Bank |
| 7976 | p154/page_s4 | DEEP PEARLS · The Gutter Bank |
| 7977 | p154/page_s5 | HOARD EMBERS · The Gutter Bank |
| 7978 | p154/page_s6 | CAPTAIN'S INSIGNIA · The Gutter Bank |
| 8000 | p137/rc/gems, p137/rc/hires, p137/rc/main |  |
| 8500 | p86/theme/menu | THE CRATE DESK · paid from your bank and pockets |
| 8600 | p131/menu | The Serpent's Oath |
| 8620 | p132/menu | Tullius's Frozen Doubloon |
| 8640 | p136/fg/menu | Signet of the Frog Knight |
| 8650 | p136/dn/menu | Donado's Collar Tag |
| 9000 | p99/menu/apo | Apophiss · wardrobe |
| 9020 | p99/menu/tul | Tullius · wardrobe |
| 9040 | p99/menu/frog | the Frog with Mustache · wardrobe |
| 9060 | p99/menu/don | Donado · wardrobe |
| 9080 | p99/menu/pearl | Pearlman · wardrobe |
| 9100 | p99/menu/wil | Wilfrey · wardrobe |
| 9120 | p99/menu/fishy | Fishy · wardrobe |
| 9140 | p145/menu | Fishy's Pocket Bowl |
| 9150 | p145/cab/main, p145/cab/powers, p145/pg/court, p145/pg/deep, p145/pg/gutter (+3) | FISHY'S CABINET OF CURIOSITIES / FISHY'S POWERS · taught by the Cabinet / THE COURT · $(n) of 20 |
| 9700 | p97/menu | Democratus' Challenge |
| 9800 | p99/menu/emma | Emma · wardrobe |
| 9840 | p99/menu/celi | Celi · wardrobe |
| 9860 | p99/menu/zib | Zib · wardrobe |
| 9880 | p99/menu/cecil | Cecil · wardrobe |
| 9900 | p99/menu/kw | KillerWatt · wardrobe |
| 9920 | p99/menu/leo | Leo · wardrobe |
| 9940 | p99/menu/demo | Democratus · wardrobe |

## Free codes

In 1-9999, outside every route of `p28/act` and on no button.

3-999, 2200, 2203, 2206-2207, 2210-2220, 2223, 2226-2227, 2230-2239, 2280, 2283, 2286-2287, 2290-2299, 2320, 2327-2328, 2330, 2333-2340, 2342-2349, 2360, 2365-2369, 2422-2440, 2443, 2446-2447, 2450-2459, 2480-2500, 2503, 2506-2507, 2510-2519, 2540, 2543, 2546-2547, 2550-2559, 2580, 2587, 2590-2600, 2607, 2610-2620, 2623, 2627, 2630-2639, 2700, 2703, 2706-2707, 2710-2719, 2740, 2743, 2747, 2750-2759, 2780, 2783, 2790-2799, 2820, 2823, 2827, 2830-2839, 2860, 2863, 2877-2879, 2920-2940, 2954-2959, 2980, 2983, 2986-2987, 2990-2999, 3020, 3023, 3026-3027, 3030-3039, 3060, 3063, 3066-3067, 3070-3099, 3486-3599, 3820-3999, 4300-4999, 5100-6000, 6100-7000, 7100, 7103-7200, 7204-7300, 7314-7600, 7608-7610, 7614-7618, 7620-7710, 7713-7719, 7737-7739, 8310-8379, 8400-8410, 8414-8500, 8508-8600, 8605-8607, 8610-8620, 8622-8623, 8625-8627, 8630-8640, 8644-8647, 8650, 8654-8657, 8660-8999, 9140, 9145-9147, 9160-9700, 9704-9799, 9960-9999

## Notes

<!-- notes -->
- 2.75: the Gutter Bank's exchange page routed the range 7875..7883 into its own router - and with it the Fixer's Lounge
  (7880) and Skip this puzzle (7881), which sat in that block. Route exact codes; claim a range only over a block you own.
  (phase129.check now fails the build on a shadowed route.)
- 2.76: the Rat Bank's Red Xenite buttons (deposit, take 1, take 10) and the Armory's Adrenaline used codes another line
  caught first - found by the same check.
- A code may sit on buttons in several menus only when the router checks bm.menu first (the 77xx end-of-heist codes are on
  the results card and on chat links - the same action, both ways in).
- 2.76c: code 1 isn't a no-op - it opens the standing screen. "Keep at it" on the Skip this puzzle? question used it as one
  (found by this legend). A button that should only close its menu uses `P28.NOOP` (code 2, routed to nothing).
- Testing: press what the client was shown (bots: `A.press(/words/)` sends that button's own command); open the menu the
  way a player does, so bm.menu is the one the router expects.
- 2.77: Apophiss's menu owns 8600-8609 (p131/act) and Tullius's 8620-8629 (p132/act); both routers check bm.menu first.
  8604-8607 and 8622-8627 are free for their later buttons.
- 2.78: the Recruiter is a dialog shop (p137/rc, menu 8000, block 8000-8099 routed whole to `p137/rc/act`, which checks bm.menu):
  8000 his book, 8001-8013 the follower contracts (2.79: 8011 Fishy) (a row only for a follower you've met - bm:met/<kind>), 8040 the hirelings'
  page and 8041-8045 theirs, 8050 the vault gems' page and 8051-8059 the gems. The rows are built in storage (bm:ui rc.acts).
- 2.79: Fishy owns three blocks, each router checking bm.menu first: 9120-9139 his wardrobe (`p99/act/fishy`, menu 9120 -
  the same layout as every follower's), 9140-9149 his Pocket Bowl menu (`p145/act`, menu 9140: 9141 sit, 9142 wardrobe, 9143
  the Cabinet, 9144 his powers, 9148 call, 9149 send home) and 9150-9158 the Cabinet (`p145/cab/act`, menu 9150: 9150 its main
  page, 9151-9156 a wing's page each, 9157 his powers, 9158 set the open wing out in the hall). His Tailor page is 8107 (the
  page numbering skips 8106, the Auras page) and his Raid Contract is the Recruiter's 8011 (the Frog and Donado moved
  up to 8012 and 8013; the book's codes are built each time, so nothing stored refers to the old ones). A wing page's back button uses
  9150, so it is only routed while bm.menu is the Cabinet's.
- 2.80h: a route added to `p28/act` goes AFTER the line that reads the click (`#act bm.pay = @s bm.act`, which phase126 put
  first). Inserted at the top, the Fixer's mercy (7736) tested the previous click, so every press acted one click late.
  check_logic now fails a test of `#act` above the read. 7736 is the mercy's confirm (p166/m_yes, from the Skip this puzzle?
  question on the last try); 7737-7739 stay free.
- 2.82: King Omega's two menus each check bm.menu first: his Monocle (`p170/act`, menu 2280: 2281 sit, 2282 wardrobe, 2284 his
  ways, 2285 back, 2288 call, 2289 send home) and his court (`p169/court/act`, menu 2320: 2321 the Peerage, 2322 the Ghost
  Garrison, 2323-2359 the court's own pages and the Chronicle). His wardrobe is the usual follower block, 2300-2319. The Tailor's
  numbering ran out: follower pages past the 16th go to 8270-8279 and outfits past the 112th to 8200-8269, routed to
  `p103/tl/act` only while bm.menu is the Tailor's.
- 2.82b: the Town Directory (`p171/act`, menu 2400) owns 2400-2421: 2401-2421 a place each (its guide), routed exactly and only
  while bm.menu is 2400. The Rat Bank's savings button is 4073 (beside 4071 deposit-all and 4072 back), on the account page.
  The Outfits page (7950) builds its buttons at run time now, like the Raid Crew page - only the wardrobes of followers you've
  met, Emma's buffs (7961-7965) only once you've met her - so a code there may not be on screen for everyone; the routes are
  unchanged.
- 2.84a: Vesper's Ledger owns 3200-3299 (`p177/act`, menu 3200; it also checks hard mode and that his book is within 8
  blocks): 3201-3205 and 3209 its pages, 3211-3213 the wards, 3220-3237 the tunings (one code per kind, a class's Unbind
  last). 3238-3299 are free. The Rat Bank outgrew 4060-4070 with its 12th currency (Dread Tokens): pages from the 12th on
  are 4090+ (4071-4079 were taken); the Exchange's Dread swaps are 4080/4081.
- 2.84b: the Community Pots menu owns 3300-3349 (`p178/pots/act`, menu 3300): 3301-3306 a pot's page, 3309 back to the
  account, 3310+i give 10, 3320+i give 50, 3330+i switch the buff, 3340 back to the pots. The account page's Community
  Pots button is 4085 (added through `P31.ACCT_EXTRA`, routed by the bank's act).
- 2.84c: the Partner Wheel owns 3350-3449 (`p179/w/act`, menu 3350): a partner's Call / Send home is 3360+i and Take the
  item back 3390+i (i: the partner's place in phase125.WHO). Its buttons are built at run time, one row per partner on the
  wheel - an unmet or unadded partner never shows.
<!-- /notes -->

## Revision log

### v2.94s
- no button changes

### v2.94r
- **3352** added: ❖ Gallery — p179/w/open
- **3353** added: ◈ View in 3D: #01-#08 — Follower Gallery
- **3354** added: ◈ View in 3D: #09-#16 — Follower Gallery
- **3355** added: ◈ View in 3D: #17-#24 — Follower Gallery
- **3356** added: ◈ View in 3D: #25-#32 — Follower Gallery
- **3359** added: « Partner Wheel — Follower Gallery

### v2.94q
- **3351** added: Keep up: off / Keep up: on — p179/w/open

### v2.94p
- no button changes

### v2.94o
- **7808** changed: ◀ The Codex / 📖 Codex — THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 30 → ◀ The Codex / 📖 Codex — RAID ODDS · per raider, per won heist, THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 30
- **7866** added: 🎲 Raid Odds — THE CODEX · what you've seen in the vault

### v2.94n
- no button changes

### v2.94m
- **9837** added: KillerWatt look $(r_kw) — Emma · wardrobe

### v2.94l
- no button changes

### v2.94k
- no button changes

### v2.94j
- no button changes

### v2.94i
- **2918** added: Pixel costume $(r_px) — The Sky Buddies · wardrobe

### v2.94h
- no button changes

### v2.94g
- no button changes

### v2.94f
- **2943** added: A bed on Nimbus — The Sky Mobile
- **2947** added: Change the weather — The Sky Mobile
- **2950** added: Clear skies — THE SKY, YOURS
- **2951** added: Rain — THE SKY, YOURS
- **2952** added: Thunderstorm — THE SKY, YOURS
- **2953** added: « Back — THE SKY, YOURS

### v2.94e
- no button changes

### v2.94d
- no button changes

### v2.94c
- no button changes

### v2.94b
- **2258** added: Pixel costume $(r_px) — Dennis · wardrobe
- **2278** added: Pixel costume $(r_px) — Pistachio · wardrobe
- **2318** added: Pixel costume $(r_px) — King Omega · wardrobe
- **2478** added: Pixel costume $(r_px) — Ashur · wardrobe
- **2538** added: Pixel costume $(r_px) — the Chef · wardrobe
- **2578** added: Pixel costume $(r_px) — the Neighbor · wardrobe
- **2658** added: Pixel costume $(r_px) — Queen Ava · wardrobe
- **2678** added: Pixel costume $(r_px) — Queen Pearl · wardrobe
- **2698** added: Pixel costume $(r_px) — Bloo · wardrobe
- **2738** added: Pixel costume $(r_px) — The Stalker · wardrobe
- **2778** added: Pixel costume $(r_px) — The Arachno-Lantern · wardrobe
- **2818** added: Pixel costume $(r_px) — Bender · wardrobe
- **2858** added: Pixel costume $(r_px) — Bones · wardrobe
- **2898** added: Pixel costume $(r_px) — Mr. Capshun · wardrobe
- **3831** removed (was: Celi: off / Celi: on — p214/menu)
- **3832** removed (was: Democratus: off / Democratus: on — p214/menu)
- **3833** removed (was: KillerWatt: off / KillerWatt: on — p214/menu)
- **3834** removed (was: Tullius: off / Tullius: on — p214/menu)
- **3835** removed (was: Fishy: off / Fishy: on — p214/menu)
- **3836** removed (was: Bloo: off / Bloo: on — p214/menu)
- **3837** removed (was: Apophiss: off / Apophiss: on — p214/menu)
- **3838** removed (was: The Chef: off / The Chef: on — p214/menu)
- **3839** removed (was: The Neighbor: off / The Neighbor: on — p214/menu)
- **3840** removed (was: The Stalker: off / The Stalker: on — p214/menu)
- **3841** removed (was: The Arachno-Lantern: off / The Arachno-Lantern: on — p214/menu)
- **3842** removed (was: Queen Ava: off / Queen Ava: on — p214/menu)
- **3843** removed (was: Pistachio: off / Pistachio: on — p214/menu)
- **3844** removed (was: Pearlman: off / Pearlman: on — p214/menu)
- **3845** removed (was: Queen Pearl: off / Queen Pearl: on — p214/menu)
- **3846** removed (was: King Omega: off / King Omega: on — p214/menu)
- **3847** removed (was: Ashur: off / Ashur: on — p214/menu)
- **3848** removed (was: Bones: off / Bones: on — p214/menu)
- **3849** removed (was: Bender: off / Bender: on — p214/menu)
- **3850** removed (was: Zib: off / Zib: on — p214/menu)
- **3851** removed (was: The Frog: off / The Frog: on — p214/menu)
- **3852** removed (was: Donado: off / Donado: on — p214/menu)
- **3853** removed (was: Wilfrey: off / Wilfrey: on — p214/menu)
- **3854** removed (was: Dennis: off / Dennis: on — p214/menu)
- **3855** removed (was: Mr. Capshun: off / Mr. Capshun: on — p214/menu)
- **9018** added: Pixel costume $(r_px) — Apophiss · wardrobe
- **9038** added: Pixel costume $(r_px) — Tullius · wardrobe
- **9058** added: Pixel costume $(r_px) — the Frog with Mustache · wardrobe
- **9078** added: Pixel costume $(r_px) — Donado · wardrobe
- **9098** added: Pixel costume $(r_px) — Pearlman · wardrobe
- **9118** added: Pixel costume $(r_px) — Wilfrey · wardrobe
- **9138** added: Pixel costume $(r_px) — Fishy · wardrobe
- **9858** added: Pixel costume $(r_px) — Celi · wardrobe
- **9878** added: Pixel costume $(r_px) — Zib · wardrobe
- **9918** added: Pixel costume $(r_px) — KillerWatt · wardrobe
- **9958** added: Pixel costume $(r_px) — Democratus · wardrobe

### v2.94a
- **2397** changed: Back after a faint $(r_ar) — The Sky Buddies · wardrobe → Back after a faint $(r_ar) — 8-Bit Cecil · wardrobe
- **2398** added: Back after a faint $(r_ar) — 8-Bit Leo · wardrobe
- **2399** added: Back after a faint $(r_ar) — 8-Bit Emma · wardrobe
- **2400** added: Back after a faint $(r_ar) — The Sky Buddies · wardrobe
- **2824** changed: Bones's ways — Bones's Whistle → Bones' ways — Bones's Whistle
- **2825** changed: « Back — BONES'S WAYS → « Back — BONES' WAYS
- **2944** changed: The Sky Buddies's ways — The Sky Mobile → The Sky Buddies' ways — The Sky Mobile
- **2945** changed: « Back — THE SKY BUDDIES'S WAYS → « Back — THE SKY BUDDIES' WAYS
- **2960** added: $(r_home) / « Outfits & buffs — 8-Bit Emma · wardrobe
- **2962** added: Sixteen colours $(r_pxemma0) — 8-Bit Emma · wardrobe
- **2963** added: Game Boy $(r_pxemma1) — 8-Bit Emma · wardrobe
- **2964** added: Virtual Boy $(r_pxemma2) — 8-Bit Emma · wardrobe
- **2965** added: Sepia Print $(r_pxemma3) — 8-Bit Emma · wardrobe
- **2966** added: Gilded Pixels $(r_pxemma4) — 8-Bit Emma · wardrobe
- **2967** added: Diamond Pixels $(r_pxemma5) — 8-Bit Emma · wardrobe
- **2968** added: Netherite Pixels $(r_pxemma6) — 8-Bit Emma · wardrobe
- **2979** added: Scanlines $(r_aura) — 8-Bit Emma · wardrobe
- **2981** added: Sit / follow — 8-Bit Emma's Cartridge
- **2982** added: Wardrobe — 8-Bit Emma's Cartridge
- **2984** added: 8-Bit Emma's ways — 8-Bit Emma's Cartridge
- **2985** added: « Back — 8-BIT EMMA'S WAYS
- **2988** added: Call for 8-Bit Emma — 8-Bit Emma's Cartridge
- **2989** added: Send her home — 8-Bit Emma's Cartridge
- **3000** added: $(r_home) / « Outfits & buffs — 8-Bit Leo · wardrobe
- **3002** added: Sixteen colours $(r_pxleo0) — 8-Bit Leo · wardrobe
- **3003** added: Game Boy $(r_pxleo1) — 8-Bit Leo · wardrobe
- **3004** added: Virtual Boy $(r_pxleo2) — 8-Bit Leo · wardrobe
- **3005** added: Sepia Print $(r_pxleo3) — 8-Bit Leo · wardrobe
- **3006** added: Gilded Pixels $(r_pxleo4) — 8-Bit Leo · wardrobe
- **3007** added: Diamond Pixels $(r_pxleo5) — 8-Bit Leo · wardrobe
- **3008** added: Netherite Pixels $(r_pxleo6) — 8-Bit Leo · wardrobe
- **3019** added: Scanlines $(r_aura) — 8-Bit Leo · wardrobe
- **3021** added: Sit / follow — 8-Bit Leo's Cartridge
- **3022** added: Wardrobe — 8-Bit Leo's Cartridge
- **3024** added: 8-Bit Leo's ways — 8-Bit Leo's Cartridge
- **3025** added: « Back — 8-BIT LEO'S WAYS
- **3028** added: Call for 8-Bit Leo — 8-Bit Leo's Cartridge
- **3029** added: Send him home — 8-Bit Leo's Cartridge
- **3040** added: $(r_home) / « Outfits & buffs — 8-Bit Cecil · wardrobe
- **3042** added: Sixteen colours $(r_pxcecil0) — 8-Bit Cecil · wardrobe
- **3043** added: Game Boy $(r_pxcecil1) — 8-Bit Cecil · wardrobe
- **3044** added: Virtual Boy $(r_pxcecil2) — 8-Bit Cecil · wardrobe
- **3045** added: Sepia Print $(r_pxcecil3) — 8-Bit Cecil · wardrobe
- **3046** added: Gilded Pixels $(r_pxcecil4) — 8-Bit Cecil · wardrobe
- **3047** added: Diamond Pixels $(r_pxcecil5) — 8-Bit Cecil · wardrobe
- **3048** added: Netherite Pixels $(r_pxcecil6) — 8-Bit Cecil · wardrobe
- **3059** added: Scanlines $(r_aura) — 8-Bit Cecil · wardrobe
- **3061** added: Sit / follow — 8-Bit Cecil's Cartridge
- **3062** added: Wardrobe — 8-Bit Cecil's Cartridge
- **3064** added: 8-Bit Cecil's ways — 8-Bit Cecil's Cartridge
- **3065** added: « Back — 8-BIT CECIL'S WAYS
- **3068** added: Call for 8-Bit Cecil — 8-Bit Cecil's Cartridge
- **3069** added: Send him home — 8-Bit Cecil's Cartridge
- **3388** changed: Call The Sky Buddies / Send The Sky Buddies home — p179/w/row28 → Call 8-Bit Cecil / Send 8-Bit Cecil home — p179/w/row28
- **3389** added: Call 8-Bit Leo / Send 8-Bit Leo home — p179/w/row29
- **3419** added: Take the item back — p179/w/row29
- **3479** added: ⚙ Menu — p179/w/row29
- **3600** changed: Gilded Ink $(r_182) — MR. CAPSHUN · the Tailor → Gilded Pixels $(r_182) — 8-BIT EMMA · the Tailor
- **3601** changed: Diamond Ink $(r_183) — MR. CAPSHUN · the Tailor → Diamond Pixels $(r_183) — 8-BIT EMMA · the Tailor
- **3602** changed: Netherite Ink $(r_184) — MR. CAPSHUN · the Tailor → Netherite Pixels $(r_184) — 8-BIT EMMA · the Tailor
- **3603** added: Game Boy $(r_185) — 8-BIT LEO · the Tailor
- **3604** added: Virtual Boy $(r_186) — 8-BIT LEO · the Tailor
- **3605** added: Sepia Print $(r_187) — 8-BIT LEO · the Tailor
- **3606** added: Gilded Pixels $(r_188) — 8-BIT LEO · the Tailor
- **3607** added: Diamond Pixels $(r_189) — 8-BIT LEO · the Tailor
- **3608** added: Netherite Pixels $(r_190) — 8-BIT LEO · the Tailor
- **3609** added: Game Boy $(r_191) — 8-BIT CECIL · the Tailor
- **3610** added: Virtual Boy $(r_192) — 8-BIT CECIL · the Tailor
- **3611** added: Sepia Print $(r_193) — 8-BIT CECIL · the Tailor
- **3612** added: Gilded Pixels $(r_194) — 8-BIT CECIL · the Tailor
- **3613** added: Diamond Pixels $(r_195) — 8-BIT CECIL · the Tailor
- **3614** added: Netherite Pixels $(r_196) — 8-BIT CECIL · the Tailor
- **3615** added: Blue Ballpoint $(r_197) — MR. CAPSHUN · the Tailor
- **3616** added: Red Pen $(r_198) — MR. CAPSHUN · the Tailor
- **3617** added: Green Marker $(r_199) — MR. CAPSHUN · the Tailor
- **3618** added: Gilded Ink $(r_200) — MR. CAPSHUN · the Tailor
- **3619** added: Diamond Ink $(r_201) — MR. CAPSHUN · the Tailor
- **3620** added: Netherite Ink $(r_202) — MR. CAPSHUN · the Tailor
- **3700** added: Call 8-Bit Emma / Send 8-Bit Emma home — p179/w/row30
- **3701** added: Call The Sky Buddies / Send The Sky Buddies home — p179/w/row31
- **3740** added: Take the item back — p179/w/row30
- **3741** added: Take the item back — p179/w/row31
- **3780** added: ⚙ Menu — p179/w/row30
- **3781** added: ⚙ Menu — p179/w/row31
- **3831** added: Celi: off / Celi: on — p214/menu
- **3832** added: Democratus: off / Democratus: on — p214/menu
- **3833** added: KillerWatt: off / KillerWatt: on — p214/menu
- **3834** added: Tullius: off / Tullius: on — p214/menu
- **3835** added: Fishy: off / Fishy: on — p214/menu
- **3836** added: Bloo: off / Bloo: on — p214/menu
- **3837** added: Apophiss: off / Apophiss: on — p214/menu
- **3838** added: The Chef: off / The Chef: on — p214/menu
- **3839** added: The Neighbor: off / The Neighbor: on — p214/menu
- **3840** added: The Stalker: off / The Stalker: on — p214/menu
- **3841** added: The Arachno-Lantern: off / The Arachno-Lantern: on — p214/menu
- **3842** added: Queen Ava: off / Queen Ava: on — p214/menu
- **3843** added: Pistachio: off / Pistachio: on — p214/menu
- **3844** added: Pearlman: off / Pearlman: on — p214/menu
- **3845** added: Queen Pearl: off / Queen Pearl: on — p214/menu
- **3846** added: King Omega: off / King Omega: on — p214/menu
- **3847** added: Ashur: off / Ashur: on — p214/menu
- **3848** added: Bones: off / Bones: on — p214/menu
- **3849** added: Bender: off / Bender: on — p214/menu
- **3850** added: Zib: off / Zib: on — p214/menu
- **3851** added: The Frog: off / The Frog: on — p214/menu
- **3852** added: Donado: off / Donado: on — p214/menu
- **3853** added: Wilfrey: off / Wilfrey: on — p214/menu
- **3854** added: Dennis: off / Dennis: on — p214/menu
- **3855** added: Mr. Capshun: off / Mr. Capshun: on — p214/menu
- **4111** changed: Vitality +1 ($(vc)) — QUEEN AVA'S HONOURS · $(r_nm) → Honour +1 ($(hc)) — QUEEN AVA'S HONOURS · $(r_nm)
- **4112** removed (was: Bulwark +1 ($(bc)) — QUEEN AVA'S HONOURS · $(r_nm))
- **4113** removed (was: Might +1 ($(mc)) — QUEEN AVA'S HONOURS · $(r_nm))
- **7735** changed: Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Mr. Capshun · wardrobe, Mr. Capshun's Pencil, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Sky Buddies · wardrobe, The Sky Mobile, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe → Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — 8-Bit Cecil · wardrobe, 8-Bit Cecil's Cartridge, 8-Bit Emma · wardrobe, 8-Bit Emma's Cartridge, 8-Bit Leo · wardrobe, 8-Bit Leo's Cartridge, Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Mr. Capshun · wardrobe, Mr. Capshun's Pencil, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Sky Buddies · wardrobe, The Sky Mobile, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, MR. CAPSHUN · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE SKY BUDDIES · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras → « The Tailor — 8-BIT CECIL · the Tailor, 8-BIT EMMA · the Tailor, 8-BIT LEO · the Tailor, APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, MR. CAPSHUN · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE SKY BUDDIES · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7890** added: 8-Bit Emma — p103/crew/row_26
- **7891** added: 8-Bit Leo — p103/crew/row_27
- **7892** added: 8-Bit Cecil — p103/crew/row_28
- **7920** changed: The Frog — p103/crew/row_26 → The Frog — p103/crew/row_29
- **7921** changed: Donado — p103/crew/row_27 → Donado — p103/crew/row_30
- **8027** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → 8-Bit Emma 176 coins / 8-Bit Emma IN YOUR PACK / 8-Bit Emma SIGNED — p137/rc/main
- **8028** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → 8-Bit Leo 176 coins / 8-Bit Leo IN YOUR PACK / 8-Bit Leo SIGNED — p137/rc/main
- **8029** added: 8-Bit Cecil 176 coins / 8-Bit Cecil IN YOUR PACK / 8-Bit Cecil SIGNED — p137/rc/main
- **8030** added: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8031** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8267** changed: Blue Ballpoint $(r_179) — MR. CAPSHUN · the Tailor → Game Boy $(r_179) — 8-BIT EMMA · the Tailor
- **8268** changed: Red Pen $(r_180) — MR. CAPSHUN · the Tailor → Virtual Boy $(r_180) — 8-BIT EMMA · the Tailor
- **8269** changed: Green Marker $(r_181) — MR. CAPSHUN · the Tailor → Sepia Print $(r_181) — 8-BIT EMMA · the Tailor
- **8282** changed: The Frog's wardrobe / The Sky Buddies — p103/tl/main, p119/page → 8-Bit Cecil / The Frog's wardrobe — p103/tl/main, p119/page
- **8283** changed: Donado's wardrobe — p119/page → 8-Bit Leo / Donado's wardrobe — p103/tl/main, p119/page
- **8284** changed: Pearlman's wardrobe — p119/page → 8-Bit Emma / Pearlman's wardrobe — p103/tl/main, p119/page
- **8285** changed: Wilfrey's wardrobe — p119/page → The Sky Buddies / Wilfrey's wardrobe — p103/tl/main, p119/page
- **8301** changed: The Sky Buddies's wardrobe / Wait here / follow me — Pearlman's Business Card, p119/page → 8-Bit Cecil's wardrobe / Wait here / follow me — Pearlman's Business Card, p119/page
- **8302** changed: Wardrobe — Pearlman's Business Card → 8-Bit Leo's wardrobe / Wardrobe — Pearlman's Business Card, p119/page
- **8303** changed: Seasons — Pearlman's Business Card → 8-Bit Emma's wardrobe / Seasons — Pearlman's Business Card, p119/page
- **8304** added: The Sky Buddies's wardrobe — p119/page
- **8384** added: Scanlines (8-Bit Emma) 1280 coins / Scanlines (8-Bit Emma) OWNED — p103/tl/auras
- **8385** added: Scanlines (8-Bit Leo) 1280 coins / Scanlines (8-Bit Leo) OWNED — p103/tl/auras
- **8386** added: Scanlines (8-Bit Cecil) 1280 coins / Scanlines (8-Bit Cecil) OWNED — p103/tl/auras

### v2.93e
- **2397** added: Back after a faint $(r_ar) — The Sky Buddies · wardrobe
- **2900** added: $(r_home) / « Outfits & buffs — The Sky Buddies · wardrobe
- **2902** added: Snooze's old blue $(r_sky0) — The Sky Buddies · wardrobe
- **2903** added: Bubblegum Pink $(r_sky1) — The Sky Buddies · wardrobe
- **2904** added: Mint Dream $(r_sky2) — The Sky Buddies · wardrobe
- **2905** added: Lavender Night $(r_sky3) — The Sky Buddies · wardrobe
- **2906** added: Gilded Nightcap $(r_sky4) — The Sky Buddies · wardrobe
- **2907** added: Diamond Nightcap $(r_sky5) — The Sky Buddies · wardrobe
- **2908** added: Netherite Nightcap $(r_sky6) — The Sky Buddies · wardrobe
- **2919** added: Starry Sky $(r_aura) — The Sky Buddies · wardrobe
- **2941** added: Sit / follow — The Sky Mobile
- **2942** added: Wardrobe — The Sky Mobile
- **2944** added: The Sky Buddies's ways — The Sky Mobile
- **2945** added: « Back — THE SKY BUDDIES'S WAYS
- **2946** added: Today's forecast — The Sky Mobile
- **2948** added: Call for The Sky Buddies — The Sky Mobile
- **2949** added: Send them home — The Sky Mobile
- **3388** added: Call The Sky Buddies / Send The Sky Buddies home — p179/w/row28
- **3418** added: Take the item back — p179/w/row28
- **3478** added: ⚙ Menu — p179/w/row28
- **3600** added: Gilded Ink $(r_182) — MR. CAPSHUN · the Tailor
- **3601** added: Diamond Ink $(r_183) — MR. CAPSHUN · the Tailor
- **3602** added: Netherite Ink $(r_184) — MR. CAPSHUN · the Tailor
- **7735** changed: Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Mr. Capshun · wardrobe, Mr. Capshun's Pencil, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe → Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Mr. Capshun · wardrobe, Mr. Capshun's Pencil, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Sky Buddies · wardrobe, The Sky Mobile, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, MR. CAPSHUN · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras → « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, MR. CAPSHUN · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE SKY BUDDIES · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7889** added: The Sky Buddies — p103/crew/row_25
- **7920** changed: The Frog — p103/crew/row_25 → The Frog — p103/crew/row_26
- **7921** changed: Donado — p103/crew/row_26 → Donado — p103/crew/row_27
- **8026** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → The Sky Buddies 176 coins / The Sky Buddies IN YOUR PACK / The Sky Buddies SIGNED — p137/rc/main
- **8027** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8028** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8261** changed: Blue Ballpoint $(r_173) — MR. CAPSHUN · the Tailor → Bubblegum Pink $(r_173) — THE SKY BUDDIES · the Tailor
- **8262** changed: Red Pen $(r_174) — MR. CAPSHUN · the Tailor → Mint Dream $(r_174) — THE SKY BUDDIES · the Tailor
- **8263** changed: Green Marker $(r_175) — MR. CAPSHUN · the Tailor → Lavender Night $(r_175) — THE SKY BUDDIES · the Tailor
- **8264** changed: Gilded Ink $(r_176) — MR. CAPSHUN · the Tailor → Gilded Nightcap $(r_176) — THE SKY BUDDIES · the Tailor
- **8265** changed: Diamond Ink $(r_177) — MR. CAPSHUN · the Tailor → Diamond Nightcap $(r_177) — THE SKY BUDDIES · the Tailor
- **8266** changed: Netherite Ink $(r_178) — MR. CAPSHUN · the Tailor → Netherite Nightcap $(r_178) — THE SKY BUDDIES · the Tailor
- **8267** added: Blue Ballpoint $(r_179) — MR. CAPSHUN · the Tailor
- **8268** added: Red Pen $(r_180) — MR. CAPSHUN · the Tailor
- **8269** added: Green Marker $(r_181) — MR. CAPSHUN · the Tailor
- **8282** changed: The Frog's wardrobe — p119/page → The Frog's wardrobe / The Sky Buddies — p103/tl/main, p119/page
- **8301** changed: Wait here / follow me — Pearlman's Business Card → The Sky Buddies's wardrobe / Wait here / follow me — Pearlman's Business Card, p119/page
- **8383** added: Starry Sky (The Sky Buddies) 1280 coins / Starry Sky (The Sky Buddies) OWNED — p103/tl/auras

### v2.93d
- **3480** added: Dynamic — Pearlman's Seasons
- **3481** added: Off - his own colours — Pearlman's Seasons
- **3482** added: Fall / Fall (locked) — Pearlman's Seasons
- **3483** added: Christmas / Christmas (locked) — Pearlman's Seasons
- **3484** added: Easter / Easter (locked) — Pearlman's Seasons
- **3485** added: Summer / Summer (locked) — Pearlman's Seasons
- **8303** added: Seasons — Pearlman's Business Card

### v2.93c
- no button changes

### v2.93b
- no button changes

### v2.93a
- no button changes

### v2.92a
- **4201** added: $(r_0md) — THE CHAMPION'S RIBBON · your Champions beside you
- **4202** added: $(r_0rg) — THE CHAMPION'S RIBBON · your Champions beside you
- **4203** added: $(r_0au) — THE CHAMPION'S RIBBON · your Champions beside you
- **4204** added: $(r_1md) — THE CHAMPION'S RIBBON · your Champions beside you
- **4205** added: $(r_1rg) — THE CHAMPION'S RIBBON · your Champions beside you
- **4206** added: $(r_1au) — THE CHAMPION'S RIBBON · your Champions beside you
- **4207** added: $(r_2md) — THE CHAMPION'S RIBBON · your Champions beside you
- **4208** added: $(r_2rg) — THE CHAMPION'S RIBBON · your Champions beside you
- **4209** added: $(r_2au) — THE CHAMPION'S RIBBON · your Champions beside you

### v2.91a
- **3201** removed (was: Followers' Wards — VESPER'S STOCK BOOK · the Dread Broker)
- **3209** changed: « The Ledger — About the Dread, Followers' Wards · Vesper, Reforging · past the old maximum, Tuning · a tool, Tuning · a weapon, Tuning · an armour piece → « The Ledger — About the Dread, Reforging · past the old maximum, Tuning · a tool, Tuning · a weapon, Tuning · an armour piece
- **3211** removed (was: Ward +1 (3/4/5 DT) — Followers' Wards · Vesper)
- **3212** removed (was: Vigor +1 (3/4/5 DT) — Followers' Wards · Vesper)
- **3213** removed (was: Swift Return +1 (3/5 DT) — Followers' Wards · Vesper)
- **4101** added: $(r_l0) — QUEEN AVA'S HONOURS · the Tide Font
- **4102** added: $(r_l1) — QUEEN AVA'S HONOURS · the Tide Font
- **4103** added: $(r_l2) — QUEEN AVA'S HONOURS · the Tide Font
- **4105** added: The Tide's Haste +1 ($(src)) — QUEEN AVA'S HONOURS · the Tide Font
- **4109** added: « Her honours — QUEEN AVA'S HONOURS · $(r_nm)
- **4111** added: Vitality +1 ($(vc)) — QUEEN AVA'S HONOURS · $(r_nm)
- **4112** added: Bulwark +1 ($(bc)) — QUEEN AVA'S HONOURS · $(r_nm)
- **4113** added: Might +1 ($(mc)) — QUEEN AVA'S HONOURS · $(r_nm)

### v2.90d
- no button changes

### v2.90c
- no button changes

### v2.90b
- no button changes

### v2.90a
- no button changes

### v2.90
- **2396** added: Back after a faint $(r_ar) — Mr. Capshun · wardrobe
- **2861** added: Sit / follow — Mr. Capshun's Pencil
- **2862** added: Wardrobe — Mr. Capshun's Pencil
- **2864** added: Mr. Capshun's ways — Mr. Capshun's Pencil
- **2865** added: « Back — MR. CAPSHUN'S PALETTE, MR. CAPSHUN'S WAYS
- **2866** added: Palette — Mr. Capshun's Pencil
- **2867** added: The story so far — Mr. Capshun's Pencil
- **2868** added: Call for Mr. Capshun — Mr. Capshun's Pencil
- **2869** added: Send him home — Mr. Capshun's Pencil
- **2870** added: Red — MR. CAPSHUN'S PALETTE
- **2871** added: Orange — MR. CAPSHUN'S PALETTE
- **2872** added: Yellow — MR. CAPSHUN'S PALETTE
- **2873** added: Green — MR. CAPSHUN'S PALETTE
- **2874** added: Blue — MR. CAPSHUN'S PALETTE
- **2875** added: Purple — MR. CAPSHUN'S PALETTE
- **2876** added: Rainbow — MR. CAPSHUN'S PALETTE
- **2880** added: $(r_home) / « Outfits & buffs — Mr. Capshun · wardrobe
- **2882** added: Plain black ink $(r_capshun0) — Mr. Capshun · wardrobe
- **2883** added: Blue Ballpoint $(r_capshun1) — Mr. Capshun · wardrobe
- **2884** added: Red Pen $(r_capshun2) — Mr. Capshun · wardrobe
- **2885** added: Green Marker $(r_capshun3) — Mr. Capshun · wardrobe
- **2886** added: Gilded Ink $(r_capshun4) — Mr. Capshun · wardrobe
- **2887** added: Diamond Ink $(r_capshun5) — Mr. Capshun · wardrobe
- **2888** added: Netherite Ink $(r_capshun6) — Mr. Capshun · wardrobe
- **2899** added: Rainbow Doodles $(r_aura) — Mr. Capshun · wardrobe
- **3387** added: Call Mr. Capshun / Send Mr. Capshun home — p179/w/row27
- **3417** added: Take the item back — p179/w/row27
- **3477** added: ⚙ Menu — p179/w/row27
- **7735** changed: Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe → Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Mr. Capshun · wardrobe, Mr. Capshun's Pencil, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras → « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, MR. CAPSHUN · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7888** added: Mr. Capshun — p103/crew/row_24
- **7920** changed: The Frog — p103/crew/row_24 → The Frog — p103/crew/row_25
- **7921** changed: Donado — p103/crew/row_25 → Donado — p103/crew/row_26
- **8025** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → Mr. Capshun 176 coins / Mr. Capshun IN YOUR PACK / Mr. Capshun SIGNED — p137/rc/main
- **8026** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8027** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8261** added: Blue Ballpoint $(r_173) — MR. CAPSHUN · the Tailor
- **8262** added: Red Pen $(r_174) — MR. CAPSHUN · the Tailor
- **8263** added: Green Marker $(r_175) — MR. CAPSHUN · the Tailor
- **8264** added: Gilded Ink $(r_176) — MR. CAPSHUN · the Tailor
- **8265** added: Diamond Ink $(r_177) — MR. CAPSHUN · the Tailor
- **8266** added: Netherite Ink $(r_178) — MR. CAPSHUN · the Tailor
- **8281** changed: Tullius's wardrobe — p119/page → Mr. Capshun / Tullius's wardrobe — p103/tl/main, p119/page
- **8300** added: Mr. Capshun's wardrobe — p119/page
- **8382** added: Rainbow Doodles (Mr. Capshun) 1280 coins / Rainbow Doodles (Mr. Capshun) OWNED — p103/tl/auras

### v2.89b
- **3201** changed: Followers' Wards — VESPER'S LEDGER · the Dread Broker → Followers' Wards — VESPER'S STOCK BOOK · the Dread Broker
- **3202** changed: Tuning — VESPER'S LEDGER · the Dread Broker → Tuning — VESPER'S STOCK BOOK · the Dread Broker
- **3203** changed: Reforging — VESPER'S LEDGER · the Dread Broker → Reforging — VESPER'S STOCK BOOK · the Dread Broker
- **3204** changed: About the Dread — VESPER'S LEDGER · the Dread Broker → About the Dread — VESPER'S STOCK BOOK · the Dread Broker

### v2.89a
- no button changes

### v2.89
- no button changes

### v2.88
- **2394** added: Back after a faint $(r_ar) — Bender · wardrobe
- **2395** added: Back after a faint $(r_ar) — Bones · wardrobe
- **2781** added: Sit / follow — Bender's Ball
- **2782** added: Wardrobe — Bender's Ball
- **2784** added: Bender's ways — Bender's Ball
- **2785** added: « Back — BENDER'S WAYS
- **2786** added: Dig! — Bender's Ball
- **2787** added: Sniff out treasure — Bender's Ball
- **2788** added: Call for Bender — Bender's Ball
- **2789** added: Send him home — Bender's Ball
- **2800** added: $(r_home) / « Outfits & buffs — Bender · wardrobe
- **2802** added: His own fawn $(r_bender0) — Bender · wardrobe
- **2803** added: Midnight Black $(r_bender1) — Bender · wardrobe
- **2804** added: Snow White $(r_bender2) — Bender · wardrobe
- **2805** added: Sable $(r_bender3) — Bender · wardrobe
- **2806** added: Gilded Coat $(r_bender4) — Bender · wardrobe
- **2807** added: Diamond Coat $(r_bender5) — Bender · wardrobe
- **2808** added: Netherite Coat $(r_bender6) — Bender · wardrobe
- **2819** added: Goodest Boy $(r_aura) — Bender · wardrobe
- **2821** added: Sit / follow — Bones's Whistle
- **2822** added: Wardrobe — Bones's Whistle
- **2824** added: Bones's ways — Bones's Whistle
- **2825** added: « Back — BONES'S WAYS
- **2826** added: Ride — Bones's Whistle
- **2828** added: Call for Bones — Bones's Whistle
- **2829** added: Send him home — Bones's Whistle
- **2840** added: $(r_home) / « Outfits & buffs — Bones · wardrobe
- **2842** added: His own shark grey $(r_bones0) — Bones · wardrobe
- **2843** added: Great White $(r_bones1) — Bones · wardrobe
- **2844** added: Hammerhead Bronze $(r_bones2) — Bones · wardrobe
- **2845** added: Abyss Black $(r_bones3) — Bones · wardrobe
- **2846** added: Gilded Skin $(r_bones4) — Bones · wardrobe
- **2847** added: Diamond Skin $(r_bones5) — Bones · wardrobe
- **2848** added: Netherite Skin $(r_bones6) — Bones · wardrobe
- **2859** added: Abyssal Tide $(r_aura) — Bones · wardrobe
- **3385** added: Call Bender / Send Bender home — p179/w/row25
- **3386** added: Call Bones / Send Bones home — p179/w/row26
- **3415** added: Take the item back — p179/w/row25
- **3416** added: Take the item back — p179/w/row26
- **3450** added: ⚙ Menu — p179/w/row0
- **3451** added: ⚙ Menu — p179/w/row1
- **3452** added: ⚙ Menu — p179/w/row2
- **3453** added: ⚙ Menu — p179/w/row3
- **3454** added: ⚙ Menu — p179/w/row4
- **3455** added: ⚙ Menu — p179/w/row5
- **3456** added: ⚙ Menu — p179/w/row6
- **3457** added: ⚙ Menu — p179/w/row7
- **3458** added: ⚙ Menu — p179/w/row8
- **3459** added: ⚙ Menu — p179/w/row9
- **3460** added: ⚙ Menu — p179/w/row10
- **3461** added: ⚙ Menu — p179/w/row11
- **3462** added: ⚙ Menu — p179/w/row12
- **3463** added: ⚙ Menu — p179/w/row13
- **3464** added: ⚙ Menu — p179/w/row14
- **3465** added: ⚙ Menu — p179/w/row15
- **3466** added: ⚙ Menu — p179/w/row16
- **3467** added: ⚙ Menu — p179/w/row17
- **3468** added: ⚙ Menu — p179/w/row18
- **3469** added: ⚙ Menu — p179/w/row19
- **3470** added: ⚙ Menu — p179/w/row20
- **3471** added: ⚙ Menu — p179/w/row21
- **3472** added: ⚙ Menu — p179/w/row22
- **3473** added: ⚙ Menu — p179/w/row23
- **3474** added: ⚙ Menu — p179/w/row24
- **3475** added: ⚙ Menu — p179/w/row25
- **3476** added: ⚙ Menu — p179/w/row26
- **7735** changed: Chatter: $(chat) (all followers) — Apophiss · wardrobe, Ashur · wardrobe, Bloo · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Queen Ava · wardrobe, Queen Pearl · wardrobe, The Arachno-Lantern · wardrobe, The Stalker · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe → Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BLOO · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras → « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7886** added: Bender — p103/crew/row_22
- **7887** added: Bones — p103/crew/row_23
- **7920** changed: The Frog — p103/crew/row_22 → The Frog — p103/crew/row_24
- **7921** changed: Donado — p103/crew/row_23 → Donado — p103/crew/row_25
- **8023** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → Bender 176 coins / Bender IN YOUR PACK / Bender SIGNED — p137/rc/main
- **8024** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → Bones 176 coins / Bones IN YOUR PACK / Bones SIGNED — p137/rc/main
- **8025** added: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8026** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8249** added: Midnight Black $(r_161) — BENDER · the Tailor
- **8250** added: Snow White $(r_162) — BENDER · the Tailor
- **8251** added: Sable $(r_163) — BENDER · the Tailor
- **8252** added: Gilded Coat $(r_164) — BENDER · the Tailor
- **8253** added: Diamond Coat $(r_165) — BENDER · the Tailor
- **8254** added: Netherite Coat $(r_166) — BENDER · the Tailor
- **8255** added: Great White $(r_167) — BONES · the Tailor
- **8256** added: Hammerhead Bronze $(r_168) — BONES · the Tailor
- **8257** added: Abyss Black $(r_169) — BONES · the Tailor
- **8258** added: Gilded Skin $(r_170) — BONES · the Tailor
- **8259** added: Diamond Skin $(r_171) — BONES · the Tailor
- **8260** added: Netherite Skin $(r_172) — BONES · the Tailor
- **8279** added: Bender — p103/tl/main
- **8280** changed: Apophiss's wardrobe — p119/page → Apophiss's wardrobe / Bones — p103/tl/main, p119/page
- **8298** changed: The Long Night (The Stalker) 1280 coins / The Long Night (The Stalker) OWNED — p103/tl/auras → Bender's wardrobe / The Long Night (The Stalker) 1280 coins / The Long Night (The Stalker) OWNED — p103/tl/auras, p119/page
- **8299** changed: Hallowfire (The Arachno-Lantern) 1280 coins / Hallowfire (The Arachno-Lantern) OWNED — p103/tl/auras → Bones's wardrobe / Hallowfire (The Arachno-Lantern) 1280 coins / Hallowfire (The Arachno-Lantern) OWNED — p103/tl/auras, p119/page
- **8380** added: Goodest Boy (Bender) 1280 coins / Goodest Boy (Bender) OWNED — p103/tl/auras
- **8381** added: Abyssal Tide (Bones) 1280 coins / Abyssal Tide (Bones) OWNED — p103/tl/auras

### v2.87
- **2393** added: Back after a faint $(r_ar) — The Arachno-Lantern · wardrobe
- **2741** added: Sit / follow — Kindled Gourd
- **2742** added: Wardrobe — Kindled Gourd
- **2744** added: The Arachno-Lantern's ways — Kindled Gourd
- **2745** added: « Back — THE ARACHNO-LANTERN'S WAYS
- **2746** added: Ride — Kindled Gourd
- **2748** added: Call for The Arachno-Lantern — Kindled Gourd
- **2749** added: Send it home — Kindled Gourd
- **2760** added: $(r_home) / « Outfits & buffs — The Arachno-Lantern · wardrobe
- **2762** added: Its own pumpkin orange $(r_lantern0) — The Arachno-Lantern · wardrobe
- **2763** added: Ghost Gourd $(r_lantern1) — The Arachno-Lantern · wardrobe
- **2764** added: Soulfire Rind $(r_lantern2) — The Arachno-Lantern · wardrobe
- **2765** added: Harvest Moon $(r_lantern3) — The Arachno-Lantern · wardrobe
- **2766** added: Gilded Rind $(r_lantern4) — The Arachno-Lantern · wardrobe
- **2767** added: Diamond Rind $(r_lantern5) — The Arachno-Lantern · wardrobe
- **2768** added: Netherite Rind $(r_lantern6) — The Arachno-Lantern · wardrobe
- **2779** added: Hallowfire $(r_aura) — The Arachno-Lantern · wardrobe
- **3384** added: Call The Arachno-Lantern / Send The Arachno-Lantern home — p179/w/row24
- **3414** added: Take the item back — p179/w/row24
- **7735** changed: Chatter: $(chat) (all followers) — Apophiss · wardrobe, Ashur · wardrobe, Bloo · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Queen Ava · wardrobe, Queen Pearl · wardrobe, The Stalker · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe → Chatter: $(chat) (all followers) — Apophiss · wardrobe, Ashur · wardrobe, Bloo · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Queen Ava · wardrobe, Queen Pearl · wardrobe, The Arachno-Lantern · wardrobe, The Stalker · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BLOO · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras → « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BLOO · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7885** added: The Arachno-Lantern — p103/crew/row_21
- **7920** changed: The Frog — p103/crew/row_21 → The Frog — p103/crew/row_22
- **7921** changed: Donado — p103/crew/row_22 → Donado — p103/crew/row_23
- **8022** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → The Arachno-Lantern 176 coins / The Arachno-Lantern IN YOUR PACK / The Arachno-Lantern SIGNED — p137/rc/main
- **8023** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8024** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8243** added: Ghost Gourd $(r_155) — THE ARACHNO-LANTERN · the Tailor
- **8244** added: Soulfire Rind $(r_156) — THE ARACHNO-LANTERN · the Tailor
- **8245** added: Harvest Moon $(r_157) — THE ARACHNO-LANTERN · the Tailor
- **8246** added: Gilded Rind $(r_158) — THE ARACHNO-LANTERN · the Tailor
- **8247** added: Diamond Rind $(r_159) — THE ARACHNO-LANTERN · the Tailor
- **8248** added: Netherite Rind $(r_160) — THE ARACHNO-LANTERN · the Tailor
- **8278** added: The Arachno-Lantern — p103/tl/main
- **8297** changed: Feral Moon (Bloo) 1280 coins / Feral Moon (Bloo) OWNED — p103/tl/auras → Feral Moon (Bloo) 1280 coins / Feral Moon (Bloo) OWNED / The Arachno-Lantern's wardrobe — p103/tl/auras, p119/page
- **8299** added: Hallowfire (The Arachno-Lantern) 1280 coins / Hallowfire (The Arachno-Lantern) OWNED — p103/tl/auras

### v2.86a
- **2326** added: Re-challenge the King — KING OMEGA
- **2389** added: Back after a faint $(r_ar) — Queen Ava · wardrobe
- **2390** added: Back after a faint $(r_ar) — Queen Pearl · wardrobe
- **2391** added: Back after a faint $(r_ar) — Bloo · wardrobe
- **2392** added: Back after a faint $(r_ar) — The Stalker · wardrobe
- **2581** added: Sit / follow — Queen Ava's Locket
- **2582** added: Wardrobe — Queen Ava's Locket
- **2583** added: Living / ghostly form — Queen Ava's Locket
- **2584** added: Queen Ava's ways — Queen Ava's Locket
- **2585** added: « Back — QUEEN AVA'S STORY, QUEEN AVA'S WAYS
- **2586** added: Her story — Queen Ava's Locket
- **2588** added: Call for Queen Ava — Queen Ava's Locket
- **2589** added: Send her home — Queen Ava's Locket
- **2601** added: Sit / follow — Queen Pearl's Pearls
- **2602** added: Wardrobe — Queen Pearl's Pearls
- **2603** added: Casual / regal outfit — Queen Pearl's Pearls
- **2604** added: Queen Pearl's ways — Queen Pearl's Pearls
- **2605** added: « Back — QUEEN PEARL'S STORY, QUEEN PEARL'S WAYS
- **2606** added: Her story — Queen Pearl's Pearls
- **2608** added: Call for Queen Pearl — Queen Pearl's Pearls
- **2609** added: Send her home — Queen Pearl's Pearls
- **2621** added: Sit / follow — Bloo's Claw
- **2622** added: Wardrobe — Bloo's Claw
- **2624** added: Bloo's ways — Bloo's Claw
- **2625** added: « Back — BLOO'S STORY, BLOO'S WAYS
- **2626** added: His story — Bloo's Claw
- **2628** added: Call for Bloo — Bloo's Claw
- **2629** added: Send him home — Bloo's Claw
- **2640** added: $(r_home) / « Outfits & buffs — Queen Ava · wardrobe
- **2642** added: Her royal blue $(r_ava0) — Queen Ava · wardrobe
- **2643** added: Coral Reef $(r_ava1) — Queen Ava · wardrobe
- **2644** added: Abyssal Violet $(r_ava2) — Queen Ava · wardrobe
- **2645** added: Kelp Forest $(r_ava3) — Queen Ava · wardrobe
- **2646** added: Gilded Gown $(r_ava4) — Queen Ava · wardrobe
- **2647** added: Diamond Gown $(r_ava5) — Queen Ava · wardrobe
- **2648** added: Netherite Gown $(r_ava6) — Queen Ava · wardrobe
- **2659** added: Crown of the Deep $(r_aura) — Queen Ava · wardrobe
- **2660** added: $(r_home) / « Outfits & buffs — Queen Pearl · wardrobe
- **2662** added: Her own aqua $(r_pearlq0) — Queen Pearl · wardrobe
- **2663** added: Coral Pink $(r_pearlq1) — Queen Pearl · wardrobe
- **2664** added: Sunset Gold $(r_pearlq2) — Queen Pearl · wardrobe
- **2665** added: Starlit Navy $(r_pearlq3) — Queen Pearl · wardrobe
- **2666** added: Gilded Dress $(r_pearlq4) — Queen Pearl · wardrobe
- **2667** added: Diamond Dress $(r_pearlq5) — Queen Pearl · wardrobe
- **2668** added: Netherite Dress $(r_pearlq6) — Queen Pearl · wardrobe
- **2679** added: Pearlescent Tide $(r_aura) — Queen Pearl · wardrobe
- **2680** added: $(r_home) / « Outfits & buffs — Bloo · wardrobe
- **2682** added: His own wild blue $(r_bloo0) — Bloo · wardrobe
- **2683** added: Shadow Pelt $(r_bloo1) — Bloo · wardrobe
- **2684** added: Ember Mane $(r_bloo2) — Bloo · wardrobe
- **2685** added: Frost Coat $(r_bloo3) — Bloo · wardrobe
- **2686** added: Gilded Fur $(r_bloo4) — Bloo · wardrobe
- **2687** added: Diamond Fur $(r_bloo5) — Bloo · wardrobe
- **2688** added: Netherite Fur $(r_bloo6) — Bloo · wardrobe
- **2699** added: Feral Moon $(r_aura) — Bloo · wardrobe
- **2701** added: Sit / follow — The Hollow Hook
- **2702** added: Wardrobe — The Hollow Hook
- **2704** added: The Stalker's ways — The Hollow Hook
- **2705** added: « Back — THE STALKER'S WAYS
- **2708** added: Call for The Stalker — The Hollow Hook
- **2709** added: Send it home — The Hollow Hook
- **2720** added: $(r_home) / « Outfits & buffs — The Stalker · wardrobe
- **2722** added: Its own sickly olive $(r_stalker0) — The Stalker · wardrobe
- **2723** added: Bone White $(r_stalker1) — The Stalker · wardrobe
- **2724** added: Ashen Grey $(r_stalker2) — The Stalker · wardrobe
- **2725** added: Blood Moon $(r_stalker3) — The Stalker · wardrobe
- **2726** added: Gilded Skin $(r_stalker4) — The Stalker · wardrobe
- **2727** added: Diamond Skin $(r_stalker5) — The Stalker · wardrobe
- **2728** added: Netherite Skin $(r_stalker6) — The Stalker · wardrobe
- **2739** added: The Long Night $(r_aura) — The Stalker · wardrobe
- **3380** added: Call Queen Ava / Send Queen Ava home — p179/w/row20
- **3381** added: Call Queen Pearl / Send Queen Pearl home — p179/w/row21
- **3382** added: Call Bloo / Send Bloo home — p179/w/row22
- **3383** added: Call The Stalker / Send The Stalker home — p179/w/row23
- **3410** added: Take the item back — p179/w/row20
- **3411** added: Take the item back — p179/w/row21
- **3412** added: Take the item back — p179/w/row22
- **3413** added: Take the item back — p179/w/row23
- **7735** changed: Chatter: $(chat) (all followers) — Apophiss · wardrobe, Ashur · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe → Chatter: $(chat) (all followers) — Apophiss · wardrobe, Ashur · wardrobe, Bloo · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Queen Ava · wardrobe, Queen Pearl · wardrobe, The Stalker · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras → « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, BLOO · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7884** added: The Stalker — p103/crew/row_20
- **7917** added: Queen Ava — p103/crew/row_17
- **7918** added: Queen Pearl — p103/crew/row_18
- **7919** added: Bloo — p103/crew/row_19
- **7920** changed: The Frog — p103/crew/row_17 → The Frog — p103/crew/row_21
- **7921** changed: Donado — p103/crew/row_18 → Donado — p103/crew/row_22
- **8018** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → Queen Ava 176 coins / Queen Ava IN YOUR PACK / Queen Ava SIGNED — p137/rc/main
- **8019** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → Queen Pearl 176 coins / Queen Pearl IN YOUR PACK / Queen Pearl SIGNED — p137/rc/main
- **8020** added: Bloo 176 coins / Bloo IN YOUR PACK / Bloo SIGNED — p137/rc/main
- **8021** added: The Stalker 176 coins / The Stalker IN YOUR PACK / The Stalker SIGNED — p137/rc/main
- **8022** added: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8023** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8219** added: Coral Reef $(r_131) — QUEEN AVA · the Tailor
- **8220** added: Abyssal Violet $(r_132) — QUEEN AVA · the Tailor
- **8221** added: Kelp Forest $(r_133) — QUEEN AVA · the Tailor
- **8222** added: Gilded Gown $(r_134) — QUEEN AVA · the Tailor
- **8223** added: Diamond Gown $(r_135) — QUEEN AVA · the Tailor
- **8224** added: Netherite Gown $(r_136) — QUEEN AVA · the Tailor
- **8225** added: Coral Pink $(r_137) — QUEEN PEARL · the Tailor
- **8226** added: Sunset Gold $(r_138) — QUEEN PEARL · the Tailor
- **8227** added: Starlit Navy $(r_139) — QUEEN PEARL · the Tailor
- **8228** added: Gilded Dress $(r_140) — QUEEN PEARL · the Tailor
- **8229** added: Diamond Dress $(r_141) — QUEEN PEARL · the Tailor
- **8230** added: Netherite Dress $(r_142) — QUEEN PEARL · the Tailor
- **8231** added: Shadow Pelt $(r_143) — BLOO · the Tailor
- **8232** added: Ember Mane $(r_144) — BLOO · the Tailor
- **8233** added: Frost Coat $(r_145) — BLOO · the Tailor
- **8234** added: Gilded Fur $(r_146) — BLOO · the Tailor
- **8235** added: Diamond Fur $(r_147) — BLOO · the Tailor
- **8236** added: Netherite Fur $(r_148) — BLOO · the Tailor
- **8237** added: Bone White $(r_149) — THE STALKER · the Tailor
- **8238** added: Ashen Grey $(r_150) — THE STALKER · the Tailor
- **8239** added: Blood Moon $(r_151) — THE STALKER · the Tailor
- **8240** added: Gilded Skin $(r_152) — THE STALKER · the Tailor
- **8241** added: Diamond Skin $(r_153) — THE STALKER · the Tailor
- **8242** added: Netherite Skin $(r_154) — THE STALKER · the Tailor
- **8274** added: Queen Ava — p103/tl/main
- **8275** added: Queen Pearl — p103/tl/main
- **8276** added: Bloo — p103/tl/main
- **8277** added: The Stalker — p103/tl/main
- **8293** changed: Kitchen Steam (the Chef) 1280 coins / Kitchen Steam (the Chef) OWNED — p103/tl/auras → Kitchen Steam (the Chef) 1280 coins / Kitchen Steam (the Chef) OWNED / Queen Ava's wardrobe — p103/tl/auras, p119/page
- **8294** changed: Grand Symphony (the Neighbor) 1280 coins / Grand Symphony (the Neighbor) OWNED — p103/tl/auras → Grand Symphony (the Neighbor) 1280 coins / Grand Symphony (the Neighbor) OWNED / Queen Pearl's wardrobe — p103/tl/auras, p119/page
- **8295** added: Bloo's wardrobe / Crown of the Deep (Queen Ava) 1280 coins / Crown of the Deep (Queen Ava) OWNED — p103/tl/auras, p119/page
- **8296** added: Pearlescent Tide (Queen Pearl) 1280 coins / Pearlescent Tide (Queen Pearl) OWNED / The Stalker's wardrobe — p103/tl/auras, p119/page
- **8297** added: Feral Moon (Bloo) 1280 coins / Feral Moon (Bloo) OWNED — p103/tl/auras
- **8298** added: The Long Night (The Stalker) 1280 coins / The Long Night (The Stalker) OWNED — p103/tl/auras

### v2.86
- **2386** added: Back after a faint $(r_ar) — Ashur · wardrobe
- **2387** added: Back after a faint $(r_ar) — the Chef · wardrobe
- **2388** added: Back after a faint $(r_ar) — the Neighbor · wardrobe
- **2441** added: Sit / follow — Ashur's Cinder
- **2442** added: Wardrobe — Ashur's Cinder
- **2444** added: Ashur's ways — Ashur's Cinder
- **2445** added: « Back — ASHUR'S WAYS
- **2448** added: Call for Ashur — Ashur's Cinder
- **2449** added: Send her home — Ashur's Cinder
- **2460** added: $(r_home) / « Outfits & buffs — Ashur · wardrobe
- **2462** added: Her own magma $(r_ashur0) — Ashur · wardrobe
- **2463** added: Blue Flame $(r_ashur1) — Ashur · wardrobe
- **2464** added: Verdant Ember $(r_ashur2) — Ashur · wardrobe
- **2465** added: Obsidian Rose $(r_ashur3) — Ashur · wardrobe
- **2466** added: Gilded Magma $(r_ashur4) — Ashur · wardrobe
- **2467** added: Diamond Magma $(r_ashur5) — Ashur · wardrobe
- **2468** added: Netherite Magma $(r_ashur6) — Ashur · wardrobe
- **2479** added: Ashfall Crown $(r_aura) — Ashur · wardrobe
- **2501** added: Sit / follow — The Golden Ladle
- **2502** added: Wardrobe — The Golden Ladle
- **2504** added: The Chef's ways — The Golden Ladle
- **2505** added: « Back — THE CHEF'S WAYS
- **2508** added: Call for The Chef — The Golden Ladle
- **2509** added: Send him home — The Golden Ladle
- **2520** added: $(r_home) / « Outfits & buffs — the Chef · wardrobe
- **2522** added: His spotless whites $(r_chef0) — the Chef · wardrobe
- **2523** added: Midnight Brigade $(r_chef1) — the Chef · wardrobe
- **2524** added: Bistro Blue $(r_chef2) — the Chef · wardrobe
- **2525** added: Sommelier Wine $(r_chef3) — the Chef · wardrobe
- **2526** added: Gilded Whites $(r_chef4) — the Chef · wardrobe
- **2527** added: Diamond Whites $(r_chef5) — the Chef · wardrobe
- **2528** added: Netherite Whites $(r_chef6) — the Chef · wardrobe
- **2539** added: Kitchen Steam $(r_aura) — the Chef · wardrobe
- **2541** added: Sit / follow — The Neighbor's Baton
- **2542** added: Wardrobe — The Neighbor's Baton
- **2544** added: The Neighbor's ways — The Neighbor's Baton
- **2545** added: « Back — THE NEIGHBOR'S WAYS
- **2548** added: Call for The Neighbor — The Neighbor's Baton
- **2549** added: Send him home — The Neighbor's Baton
- **2560** added: $(r_home) / « Outfits & buffs — the Neighbor · wardrobe
- **2562** added: His sailor whites $(r_neighbor0) — the Neighbor · wardrobe
- **2563** added: Navy Bandmaster $(r_neighbor1) — the Neighbor · wardrobe
- **2564** added: Encore Crimson $(r_neighbor2) — the Neighbor · wardrobe
- **2565** added: Jazz Violet $(r_neighbor3) — the Neighbor · wardrobe
- **2566** added: Gilded Suit $(r_neighbor4) — the Neighbor · wardrobe
- **2567** added: Diamond Suit $(r_neighbor5) — the Neighbor · wardrobe
- **2568** added: Netherite Suit $(r_neighbor6) — the Neighbor · wardrobe
- **2579** added: Grand Symphony $(r_aura) — the Neighbor · wardrobe
- **3377** added: Call Ashur / Send Ashur home — p179/w/row17
- **3378** added: Call the Chef / Send the Chef home — p179/w/row18
- **3379** added: Call the Neighbor / Send the Neighbor home — p179/w/row19
- **3407** added: Take the item back — p179/w/row17
- **3408** added: Take the item back — p179/w/row18
- **3409** added: Take the item back — p179/w/row19
- **7735** changed: Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe → Chatter: $(chat) (all followers) — Apophiss · wardrobe, Ashur · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras → « The Tailor — APOPHISS · the Tailor, ASHUR · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7914** added: Ashur — p103/crew/row_14
- **7915** added: The Chef — p103/crew/row_15
- **7916** added: The Neighbor — p103/crew/row_16
- **7920** changed: The Frog — p103/crew/row_14 → The Frog — p103/crew/row_17
- **7921** changed: Donado — p103/crew/row_15 → Donado — p103/crew/row_18
- **8015** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → Ashur 176 coins / Ashur IN YOUR PACK / Ashur SIGNED — p137/rc/main
- **8016** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → The Chef 176 coins / The Chef IN YOUR PACK / The Chef SIGNED — p137/rc/main
- **8017** added: The Neighbor 176 coins / The Neighbor IN YOUR PACK / The Neighbor SIGNED — p137/rc/main
- **8018** added: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8019** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8199** added: Ashfall Crown (Ashur) 1280 coins / Ashfall Crown (Ashur) OWNED — p103/tl/auras
- **8201** added: Blue Flame $(r_113) — ASHUR · the Tailor
- **8202** added: Verdant Ember $(r_114) — ASHUR · the Tailor
- **8203** added: Obsidian Rose $(r_115) — ASHUR · the Tailor
- **8204** added: Gilded Magma $(r_116) — ASHUR · the Tailor
- **8205** added: Diamond Magma $(r_117) — ASHUR · the Tailor
- **8206** added: Netherite Magma $(r_118) — ASHUR · the Tailor
- **8207** added: Midnight Brigade $(r_119) — THE CHEF · the Tailor
- **8208** added: Bistro Blue $(r_120) — THE CHEF · the Tailor
- **8209** added: Sommelier Wine $(r_121) — THE CHEF · the Tailor
- **8210** added: Gilded Whites $(r_122) — THE CHEF · the Tailor
- **8211** added: Diamond Whites $(r_123) — THE CHEF · the Tailor
- **8212** added: Netherite Whites $(r_124) — THE CHEF · the Tailor
- **8213** added: Navy Bandmaster $(r_125) — THE NEIGHBOR · the Tailor
- **8214** added: Encore Crimson $(r_126) — THE NEIGHBOR · the Tailor
- **8215** added: Jazz Violet $(r_127) — THE NEIGHBOR · the Tailor
- **8216** added: Gilded Suit $(r_128) — THE NEIGHBOR · the Tailor
- **8217** added: Diamond Suit $(r_129) — THE NEIGHBOR · the Tailor
- **8218** added: Netherite Suit $(r_130) — THE NEIGHBOR · the Tailor
- **8271** added: Ashur — p103/tl/main
- **8272** added: The Chef — p103/tl/main
- **8273** added: The Neighbor — p103/tl/main
- **8290** added: Ashur's wardrobe — p119/page
- **8291** added: The Chef's wardrobe — p119/page
- **8292** added: The Neighbor's wardrobe — p119/page
- **8293** added: Kitchen Steam (the Chef) 1280 coins / Kitchen Steam (the Chef) OWNED — p103/tl/auras
- **8294** added: Grand Symphony (the Neighbor) 1280 coins / Grand Symphony (the Neighbor) OWNED — p103/tl/auras

### v2.85d
- **3420** added: Launch your Skiff Escort / Send your Skiff Escort home — p184/wesc/row
- **3421** added: Take the escort back — p184/wesc/row
- **7808** changed: ◀ The Codex / 📖 Codex — THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 23 → ◀ The Codex / 📖 Codex — THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 30

### v2.85c
- no button changes

### v2.85b
- no button changes

### v2.85a
- no button changes

### v2.84d
- no button changes

### v2.84c
- **3360** added: Call Emma / Send Emma home — p179/w/row0
- **3361** added: Call Celi / Send Celi home — p179/w/row1
- **3362** added: Call Zib / Send Zib home — p179/w/row2
- **3363** added: Call Cecil / Send Cecil home — p179/w/row3
- **3364** added: Call KillerWatt / Send KillerWatt home — p179/w/row4
- **3365** added: Call Leo / Send Leo home — p179/w/row5
- **3366** added: Call Democratus / Send Democratus home — p179/w/row6
- **3367** added: Call Apophiss / Send Apophiss home — p179/w/row7
- **3368** added: Call Tullius / Send Tullius home — p179/w/row8
- **3369** added: Call the Frog / Send the Frog home — p179/w/row9
- **3370** added: Call Donado / Send Donado home — p179/w/row10
- **3371** added: Call Pearlman / Send Pearlman home — p179/w/row11
- **3372** added: Call Wilfrey / Send Wilfrey home — p179/w/row12
- **3373** added: Call Fishy / Send Fishy home — p179/w/row13
- **3374** added: Call Dennis / Send Dennis home — p179/w/row14
- **3375** added: Call Pistachio / Send Pistachio home — p179/w/row15
- **3376** added: Call King Omega / Send King Omega home — p179/w/row16
- **3390** added: Take the item back — p179/w/row0
- **3391** added: Take the item back — p179/w/row1
- **3392** added: Take the item back — p179/w/row2
- **3393** added: Take the item back — p179/w/row3
- **3394** added: Take the item back — p179/w/row4
- **3395** added: Take the item back — p179/w/row5
- **3396** added: Take the item back — p179/w/row6
- **3397** added: Take the item back — p179/w/row7
- **3398** added: Take the item back — p179/w/row8
- **3399** added: Take the item back — p179/w/row9
- **3400** added: Take the item back — p179/w/row10
- **3401** added: Take the item back — p179/w/row11
- **3402** added: Take the item back — p179/w/row12
- **3403** added: Take the item back — p179/w/row13
- **3404** added: Take the item back — p179/w/row14
- **3405** added: Take the item back — p179/w/row15
- **3406** added: Take the item back — p179/w/row16

### v2.84b
- **3301** added: Lamplighters' Fund $(p0)/250$(s0) — Community Pots · The Rat Bank
- **3302** added: Harvest Guild $(p1)/300$(s1) — Community Pots · The Rat Bank
- **3303** added: Miners' Union $(p2)/400$(s2) — Community Pots · The Rat Bank
- **3304** added: Couriers' Guild $(p3)/400$(s3) — Community Pots · The Rat Bank
- **3305** added: Hearth Fund $(p4)/500$(s4) — Community Pots · The Rat Bank
- **3306** added: Bounty Office $(p5)/600$(s5) — Community Pots · The Rat Bank
- **3309** added: « Your account — Community Pots · The Rat Bank
- **3310** added: Give 10 Tokens — Lamplighters' Fund · Community Pots
- **3311** added: Give 10 Tokens — Harvest Guild · Community Pots
- **3312** added: Give 10 Tokens — Miners' Union · Community Pots
- **3313** added: Give 10 Tokens — Couriers' Guild · Community Pots
- **3314** added: Give 10 Tokens — Hearth Fund · Community Pots
- **3315** added: Give 10 Tokens — Bounty Office · Community Pots
- **3320** added: Give 50 Tokens — Lamplighters' Fund · Community Pots
- **3321** added: Give 50 Tokens — Harvest Guild · Community Pots
- **3322** added: Give 50 Tokens — Miners' Union · Community Pots
- **3323** added: Give 50 Tokens — Couriers' Guild · Community Pots
- **3324** added: Give 50 Tokens — Hearth Fund · Community Pots
- **3325** added: Give 50 Tokens — Bounty Office · Community Pots
- **3330** added: Switch it on / off — Lamplighters' Fund · Community Pots
- **3331** added: Switch it on / off — Harvest Guild · Community Pots
- **3332** added: Switch it on / off — Miners' Union · Community Pots
- **3333** added: Switch it on / off — Couriers' Guild · Community Pots
- **3334** added: Switch it on / off — Hearth Fund · Community Pots
- **3335** added: Switch it on / off — Bounty Office · Community Pots
- **3340** added: « The pots — Bounty Office · Community Pots, Couriers' Guild · Community Pots, Harvest Guild · Community Pots, Hearth Fund · Community Pots, Lamplighters' Fund · Community Pots, Miners' Union · Community Pots
- **4085** added: Community Pots — The Rat Bank - your account

### v2.84a
- **3201** added: Followers' Wards — VESPER'S LEDGER · the Dread Broker
- **3202** added: Tuning — VESPER'S LEDGER · the Dread Broker
- **3203** added: Reforging — VESPER'S LEDGER · the Dread Broker
- **3204** added: About the Dread — VESPER'S LEDGER · the Dread Broker
- **3205** added: Reforge what I hold — Reforging · past the old maximum
- **3209** added: « The Ledger — About the Dread, Followers' Wards · Vesper, Reforging · past the old maximum, Tuning · a tool, Tuning · a weapon, Tuning · an armour piece
- **3211** added: Ward +1 (3/4/5 DT) — Followers' Wards · Vesper
- **3212** added: Vigor +1 (3/4/5 DT) — Followers' Wards · Vesper
- **3213** added: Swift Return +1 (3/5 DT) — Followers' Wards · Vesper
- **3220** added: Attack Damage +0.75 (max 3) — Tuning · a weapon
- **3221** added: Swing Speed +0.1 (max 3) — Tuning · a weapon
- **3222** added: Reach +0.25 (max 2) — Tuning · a weapon
- **3223** added: Luck +1 (max 2) — Tuning · a weapon
- **3224** added: Unbind all tunings (every token back) — Tuning · a weapon
- **3225** added: Mining Speed +10% (max 3) — Tuning · a tool
- **3226** added: Mining Efficiency +3 (max 2) — Tuning · a tool
- **3227** added: Block Reach +0.5 (max 2) — Tuning · a tool
- **3228** added: Luck +1 (max 2) — Tuning · a tool
- **3229** added: Unbind all tunings (every token back) — Tuning · a tool
- **3230** added: Armor +1 (max 2) — Tuning · an armour piece
- **3231** added: Toughness +1 (max 2) — Tuning · an armour piece
- **3232** added: Max Health +1 (max 2) — Tuning · an armour piece
- **3233** added: Knockback Resistance +0.05 (max 2) — Tuning · an armour piece
- **3234** added: Speed (boots) +2% (max 2) — Tuning · an armour piece
- **3235** added: Unbind all tunings (every token back) — Tuning · an armour piece
- **4054** added: Deposit all Dread Tokens ($(h)) — Dread Tokens · The Rat Bank
- **4055** added: Take 1 — Dread Tokens · The Rat Bank
- **4056** added: Take 10 — Dread Tokens · The Rat Bank
- **4057** added: Take all ($(n)) — Dread Tokens · The Rat Bank
- **4072** changed: « Back to your account / « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Savings · The Rat Bank, The Exchange · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank → « Back to your account / « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Dread Tokens · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Savings · The Rat Bank, The Exchange · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank
- **4080** added: 5 Trophies → 1 Dread Token — The Exchange · The Rat Bank
- **4081** added: 1 Dread Token → 5 Trophies — The Exchange · The Rat Bank
- **4090** added: Dread Tokens $(dread_token) — The Rat Bank - your account

### v2.83b
- no button changes

### v2.83a
- no button changes

### v2.83
- **2140** added: Buy the Ore Magnet 16 Tokens — DENNIS'S ASSAY OFFICE
- **2190** added: Buy the Spirit Jar 16 Tokens — PISTACHIO'S PANTRY
- **4072** changed: « Back to your account / « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Savings · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank → « Back to your account / « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Savings · The Rat Bank, The Exchange · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank
- **4074** added: Exchange — The Rat Bank - your account
- **4075** added: 5 Tokens → 1 Medallion — The Exchange · The Rat Bank
- **4076** added: 1 Medallion → 5 Tokens — The Exchange · The Rat Bank
- **4077** added: 4 Medallions → 1 Trophy — The Exchange · The Rat Bank
- **4078** added: 1 Trophy → 4 Medallions — The Exchange · The Rat Bank
- **4079** added: Auto-deposit: $(ac) — The Rat Bank - your account

### v2.82t
- **2361** added: Call him over — Wilfrey's Locket
- **2362** added: Send him home — Wilfrey's Locket
- **2363** added: Wardrobe — Wilfrey's Locket
- **2364** added: Call Wilfrey — Wilfrey's Locket
- **2370** added: Back after a faint $(r_ar) — Cecil · wardrobe
- **2371** added: Back after a faint $(r_ar) — Emma · wardrobe
- **2372** added: Back after a faint $(r_ar) — Celi · wardrobe
- **2373** added: Back after a faint $(r_ar) — Zib · wardrobe
- **2374** added: Back after a faint $(r_ar) — KillerWatt · wardrobe
- **2375** added: Back after a faint $(r_ar) — Leo · wardrobe
- **2376** added: Back after a faint $(r_ar) — Democratus · wardrobe
- **2377** added: Back after a faint $(r_ar) — Apophiss · wardrobe
- **2378** added: Back after a faint $(r_ar) — Tullius · wardrobe
- **2379** added: Back after a faint $(r_ar) — the Frog with Mustache · wardrobe
- **2380** added: Back after a faint $(r_ar) — Donado · wardrobe
- **2381** added: Back after a faint $(r_ar) — Wilfrey · wardrobe
- **2382** added: Back after a faint $(r_ar) — Fishy · wardrobe
- **2383** added: Back after a faint $(r_ar) — Dennis · wardrobe
- **2384** added: Back after a faint $(r_ar) — Pistachio · wardrobe
- **2385** added: Back after a faint $(r_ar) — King Omega · wardrobe
- **9159** added: A spare Pocket Bowl — FISHY'S CABINET OF CURIOSITIES

### v2.82s
- no button changes

### v2.82r
- no button changes

### v2.82q
- no button changes

### v2.82p
- no button changes

### v2.82o
- no button changes

### v2.82n
- no button changes

### v2.82m
- no button changes

### v2.82l
- no button changes

### v2.82k
- no button changes

### v2.82j
- no button changes

### v2.82i
- no button changes

### v2.82h
- no button changes

### v2.82g
- no button changes

### v2.82f
- no button changes

### v2.82e
- no button changes

### v2.82d
- no button changes

### v2.82c
- no button changes

### v2.82b
- **1021** changed: Banker's Card 4 Tokens — The Fence - Back Room → 2 Ominous Trial Keys 2 Medallions — The Fence - Back Room
- **7740** changed: « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor → « The Tailor — APOPHISS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras
- **7741** changed: Emma — THE TAILOR · outfits for your followers → Emma — p103/tl/main
- **7742** changed: Celi — THE TAILOR · outfits for your followers → Celi — p103/tl/main
- **7743** changed: Zib — THE TAILOR · outfits for your followers → Zib — p103/tl/main
- **7744** changed: Cecil — THE TAILOR · outfits for your followers → Cecil — p103/tl/main
- **7745** changed: KillerWatt — THE TAILOR · outfits for your followers → KillerWatt — p103/tl/main
- **7746** changed: Leo — THE TAILOR · outfits for your followers → Leo — p103/tl/main
- **7747** changed: Democratus — THE TAILOR · outfits for your followers → Democratus — p103/tl/main
- **7748** changed: Display cases — THE TAILOR · outfits for your followers → Display cases — p103/tl/main
- **8100** changed: Apophiss — THE TAILOR · outfits for your followers → Apophiss — p103/tl/main
- **8101** changed: Tullius — THE TAILOR · outfits for your followers → Tullius — p103/tl/main
- **8102** changed: The Frog — THE TAILOR · outfits for your followers → The Frog — p103/tl/main
- **8103** changed: Donado — THE TAILOR · outfits for your followers → Donado — p103/tl/main
- **8104** changed: Pearlman — THE TAILOR · outfits for your followers → Pearlman — p103/tl/main
- **8105** changed: Wilfrey — THE TAILOR · outfits for your followers → Wilfrey — p103/tl/main
- **8106** changed: Auras (rare) — THE TAILOR · outfits for your followers → Auras (rare) — p103/tl/main
- **8107** changed: Fishy — THE TAILOR · outfits for your followers → Fishy — p103/tl/main
- **8108** changed: Dennis — THE TAILOR · outfits for your followers → Dennis — p103/tl/main
- **8109** changed: Pistachio — THE TAILOR · outfits for your followers → Pistachio — p103/tl/main
- **8150** changed: Blossom Halo (Emma) $(r_a0) — AURAS · the Tailor → Blossom Halo (Emma) 1280 coins / Blossom Halo (Emma) OWNED — p103/tl/auras
- **8151** changed: Moonfrost Veil (Celi) $(r_a1) — AURAS · the Tailor → Moonfrost Veil (Celi) 1280 coins / Moonfrost Veil (Celi) OWNED — p103/tl/auras
- **8152** changed: Starfield Static (Zib) $(r_a2) — AURAS · the Tailor → Starfield Static (Zib) 1280 coins / Starfield Static (Zib) OWNED — p103/tl/auras
- **8153** changed: Arcane Corona (Cecil) $(r_a3) — AURAS · the Tailor → Arcane Corona (Cecil) 1280 coins / Arcane Corona (Cecil) OWNED — p103/tl/auras
- **8154** changed: Storm Crown (KillerWatt) $(r_a4) — AURAS · the Tailor → Storm Crown (KillerWatt) 1280 coins / Storm Crown (KillerWatt) OWNED — p103/tl/auras
- **8155** changed: Tidal Aegis (Leo) $(r_a5) — AURAS · the Tailor → Tidal Aegis (Leo) 1280 coins / Tidal Aegis (Leo) OWNED — p103/tl/auras
- **8156** changed: Reaper's Shroud (Democratus) $(r_a6) — AURAS · the Tailor → Reaper's Shroud (Democratus) 1280 coins / Reaper's Shroud (Democratus) OWNED — p103/tl/auras
- **8157** changed: Black-Flame Mantle (Apophiss) $(r_a7) — AURAS · the Tailor → Black-Flame Mantle (Apophiss) 1280 coins / Black-Flame Mantle (Apophiss) OWNED — p103/tl/auras
- **8158** changed: Drowned Gale (Tullius) $(r_a8) — AURAS · the Tailor → Drowned Gale (Tullius) 1280 coins / Drowned Gale (Tullius) OWNED — p103/tl/auras
- **8159** changed: Bog-Light Ring (the Frog) $(r_a9) — AURAS · the Tailor → Bog-Light Ring (the Frog) 1280 coins / Bog-Light Ring (the Frog) OWNED — p103/tl/auras
- **8160** changed: Tractor Beam (Donado) $(r_a10) — AURAS · the Tailor → Tractor Beam (Donado) 1280 coins / Tractor Beam (Donado) OWNED — p103/tl/auras
- **8161** changed: Golden Gleam (Pearlman) $(r_a11) — AURAS · the Tailor → Golden Gleam (Pearlman) 1280 coins / Golden Gleam (Pearlman) OWNED — p103/tl/auras
- **8162** changed: Lordly Radiance (Wilfrey) $(r_a12) — AURAS · the Tailor → Lordly Radiance (Wilfrey) 1280 coins / Lordly Radiance (Wilfrey) OWNED — p103/tl/auras
- **8163** changed: Bubble Halo (Fishy) $(r_a13) — AURAS · the Tailor → Bubble Halo (Fishy) 1280 coins / Bubble Halo (Fishy) OWNED — p103/tl/auras
- **8196** changed: Gold Rush Glimmer (Dennis) $(r_a14) — AURAS · the Tailor → Gold Rush Glimmer (Dennis) 1280 coins / Gold Rush Glimmer (Dennis) OWNED — p103/tl/auras
- **8197** changed: Ectoplasmic Mist (Pistachio) $(r_a15) — AURAS · the Tailor → Ectoplasmic Mist (Pistachio) 1280 coins / Ectoplasmic Mist (Pistachio) OWNED — p103/tl/auras
- **8198** changed: Court of Souls (King Omega) $(r_a16) — AURAS · the Tailor → Court of Souls (King Omega) 1280 coins / Court of Souls (King Omega) OWNED — p103/tl/auras
- **8270** changed: King Omega — THE TAILOR · outfits for your followers → King Omega — p103/tl/main

### v2.82
- **1020** changed: Sealed Explorer's Map 3 Tokens — The Fence - Back Room → Sealed Explorer's Map 2 Tokens — The Fence - Back Room
- **1021** changed: Banker's Card 3 Medallions — The Fence - Back Room → Banker's Card 4 Tokens — The Fence - Back Room
- **1022** changed: Smuggler's Jar 6 Medallions — The Fence - Back Room → Smuggler's Jar 4 Medallions — The Fence - Back Room
- **1040** changed: Fair Weather Bell 6 Tokens — Old Barnaby - Back Room → Fair Weather Bell 4 Tokens — Old Barnaby - Back Room
- **1041** changed: 2 Totems of Undying 4 Medallions — Old Barnaby - Back Room → 2 Totems of Undying 2 Medallions — Old Barnaby - Back Room
- **1042** changed: Spawner Crowbar 8 Medallions — Old Barnaby - Back Room → Spawner Crowbar 5 Medallions — Old Barnaby - Back Room
- **1060** changed: Rat Gang Portrait 4 Tokens — Madame Velour - Back Room → Rat Gang Portrait 2 Tokens — Madame Velour - Back Room
- **1061** changed: Donado Trophy 4 Medallions — Madame Velour - Back Room → Donado Trophy 2 Medallions — Madame Velour - Back Room
- **1062** changed: Brass Wing Scroll 2 Trophies — Madame Velour - Back Room → Brass Wing Scroll 1 Trophy — Madame Velour - Back Room
- **1080** changed: 16 Spectral Arrows 3 Tokens — Vinny 'Two-Blades' - Back Room → 16 Spectral Arrows 2 Tokens — Vinny 'Two-Blades' - Back Room
- **1081** changed: Netherite Upgrade Template 3 Medallions — Vinny 'Two-Blades' - Back Room → Netherite Upgrade Template 2 Medallions — Vinny 'Two-Blades' - Back Room
- **1082** changed: Showstopper Charm 2 Trophies — Vinny 'Two-Blades' - Back Room → Showstopper Charm 1 Trophy — Vinny 'Two-Blades' - Back Room
- **1100** changed: Lodestone Locket 8 Tokens — Sgt. Steelwhisker - Back Room → Lodestone Locket 5 Tokens — Sgt. Steelwhisker - Back Room
- **1101** changed: 3 Wither Skeleton Skulls 4 Medallions — Sgt. Steelwhisker - Back Room → 3 Wither Skeleton Skulls 2 Medallions — Sgt. Steelwhisker - Back Room
- **1102** changed: Market Crest Scroll 2 Trophies — Sgt. Steelwhisker - Back Room → Market Crest Scroll 1 Trophy — Sgt. Steelwhisker - Back Room
- **1120** changed: A Whole Cake 2 Tokens — Chef Fromage - Back Room → A Whole Cake 1 Token — Chef Fromage - Back Room
- **1121** changed: Enchanted Golden Apple 6 Medallions — Chef Fromage - Back Room → Enchanted Golden Apple 4 Medallions — Chef Fromage - Back Room
- **1122** changed: 3 Enchanted Golden Apples 2 Trophies — Chef Fromage - Back Room → 3 Enchanted Golden Apples 1 Trophy — Chef Fromage - Back Room
- **1140** changed: 16 Bottles o' Enchanting 3 Tokens — Prof. Whiskerton - Back Room → 16 Bottles o' Enchanting 2 Tokens — Prof. Whiskerton - Back Room
- **1141** changed: Book of Mending 4 Medallions — Prof. Whiskerton - Back Room → Book of Mending 2 Medallions — Prof. Whiskerton - Back Room
- **1142** changed: Auroral Crown 2 Trophies — Prof. Whiskerton - Back Room → Auroral Crown 1 Trophy — Prof. Whiskerton - Back Room
- **1160** changed: Jackpot Scratch Card 4 Lucky Tokens — Lucky Whiskers - Back Room → Jackpot Scratch Card 2 Lucky Tokens — Lucky Whiskers - Back Room
- **1161** changed: Heartstone 15 Lucky Tokens — Lucky Whiskers - Back Room → Heartstone 9 Lucky Tokens — Lucky Whiskers - Back Room
- **1162** changed: Bloomwalker Boots 2 Trophies — Lucky Whiskers - Back Room → Bloomwalker Boots 1 Trophy — Lucky Whiskers - Back Room
- **1180** changed: Buried Treasure Map 3 Tokens — Capt. Cheddarbeard - Back Room → Buried Treasure Map 2 Tokens — Capt. Cheddarbeard - Back Room
- **1181** changed: Heart of the Sea 3 Medallions — Capt. Cheddarbeard - Back Room → Heart of the Sea 2 Medallions — Capt. Cheddarbeard - Back Room
- **1182** changed: Rat Familiar 2 Trophies — Capt. Cheddarbeard - Back Room → Rat Familiar 1 Trophy — Capt. Cheddarbeard - Back Room
- **1200** changed: Ominous Bottle 6 Blood Moon Crystals — The Bloodbroker - Back Room → Ominous Bottle 4 Blood Moon Crystals — The Bloodbroker - Back Room
- **1201** changed: Nether Star 24 Blood Moon Crystals — The Bloodbroker - Back Room → Nether Star 14 Blood Moon Crystals — The Bloodbroker - Back Room
- **2001** changed: Buy a one-night pass 2 Medallions — The Dark Auction → Buy a one-night pass 1 Medallion — The Dark Auction
- **2281** added: Sit / follow — Omega's Monocle
- **2282** added: Wardrobe — Omega's Monocle
- **2284** added: King Omega's ways — Omega's Monocle
- **2285** added: « Back — KING OMEGA'S WAYS
- **2288** added: Call for Omega — Omega's Monocle
- **2289** added: Send him home — Omega's Monocle
- **2300** added: $(r_home) / « Outfits & buffs — King Omega · wardrobe
- **2302** added: His own grey ghost $(r_omega0) — King Omega · wardrobe
- **2303** added: Spectral Blue $(r_omega1) — King Omega · wardrobe
- **2304** added: Blood Moon $(r_omega2) — King Omega · wardrobe
- **2305** added: Verdant Wraith $(r_omega3) — King Omega · wardrobe
- **2306** added: Gilded King $(r_omega4) — King Omega · wardrobe
- **2307** added: Diamond King $(r_omega5) — King Omega · wardrobe
- **2308** added: Netherite King $(r_omega6) — King Omega · wardrobe
- **2319** added: Court of Souls $(r_aura) — King Omega · wardrobe
- **2321** added: The Peerage — KING OMEGA
- **2322** added: The Ghost Garrison — KING OMEGA
- **2323** added: Offer a gift — KING OMEGA
- **2324** added: The Chronicle — KING OMEGA
- **2325** added: My title on / off — KING OMEGA
- **2329** added: « Back — THE GHOST GARRISON, THE PEERAGE, p169/court/chron
- **2331** added: Tithe 4 Tokens +10 — THE PEERAGE
- **2332** added: Offer your Court's souls — THE PEERAGE
- **2341** added: Buy a Soul Brazier 8 Tokens — THE GHOST GARRISON
- **2350** added: I. Two Eggs in the Sun — p169/court/chron
- **2351** added: II. The Monocle — p169/court/chron
- **2352** added: III. The Feast of Crowns — p169/court/chron
- **2353** added: IV. The Library of Small Things — p169/court/chron
- **2354** added: V. The Light to Lead Them — p169/court/chron
- **2355** added: VI. The War of Brothers — p169/court/chron
- **2356** added: VII. The Last Night — p169/court/chron
- **2357** added: VIII. The Long Quiet — p169/court/chron
- **2358** added: IX. The Butler and the Boy — p169/court/chron
- **2359** added: X. What the Dead King Wants — p169/court/chron
- **2401** added: Old Barnaby — WHO'S WHERE · the rat town
- **2402** added: Prof. Whiskerton — WHO'S WHERE · the rat town
- **2403** added: Madame Velour — WHO'S WHERE · the rat town
- **2404** added: The Fence — WHO'S WHERE · the rat town
- **2405** added: Dark Auction gate — WHO'S WHERE · the rat town
- **2406** added: Gilded Gutter gate — WHO'S WHERE · the rat town
- **2407** added: Scrap Bin — WHO'S WHERE · the rat town
- **2408** added: Bounty Board — WHO'S WHERE · the rat town
- **2409** added: Mike's pond — WHO'S WHERE · the rat town
- **2410** added: Vinny 'Two-Blades' — WHO'S WHERE · the rat town
- **2411** added: Steelwhisker — WHO'S WHERE · the rat town
- **2412** added: Fishy's Cabinet — WHO'S WHERE · the rat town
- **2413** added: Chef Fromage — WHO'S WHERE · the rat town
- **2414** added: Cecil — WHO'S WHERE · the rat town
- **2415** added: The Bloodbroker — WHO'S WHERE · the rat town
- **2416** added: Lucky Whiskers — WHO'S WHERE · the rat town
- **2417** added: The dock house — WHO'S WHERE · the rat town
- **2418** added: Dennis — WHO'S WHERE · the rat town
- **2419** added: Pistachio — WHO'S WHERE · the rat town
- **2420** added: Newcomers' Book — WHO'S WHERE · the rat town
- **2421** added: The way out — WHO'S WHERE · the rat town
- **4072** changed: « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank → « Back to your account / « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Savings · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank
- **4073** added: Savings account — The Rat Bank - your account
- **5010** changed: Repair the item in my main hand 2 Medallions — The Concierge → Repair the item in my main hand 1 Medallion — The Concierge
- **7005** changed: Pay a week 7 Tokens — Rufus Gnaw, rat for hire → Pay a week 4 Tokens — Rufus Gnaw, rat for hire
- **7007** changed: Patch him up 2 Medallions — Rufus Gnaw, rat for hire → Patch him up 1 Medallion — Rufus Gnaw, rat for hire
- **7735** changed: Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe → Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, King Omega · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor → « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor
- **7807** changed: « Raid Crew / ☺ Raid Crew — OUTFITS & EMMA'S BUFF · your followers, from the Ledger, THE FIXER'S OFFICE · everything the vault owes you → « Raid Crew / ☺ Raid Crew — THE FIXER'S OFFICE · everything the vault owes you, p119/page
- **7913** added: Omega — p103/crew/row_13
- **7920** changed: The Frog — p103/crew/row_13 → The Frog — p103/crew/row_14
- **7921** changed: Donado — p103/crew/row_14 → Donado — p103/crew/row_15
- **7950** changed: Outfits & Emma's buff — p98/crew → Outfits & Emma's buff / Outfits & chatter — p98/crew
- **7951** changed: Emma's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Emma's wardrobe — p119/page
- **7952** changed: Celi's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Celi's wardrobe — p119/page
- **7953** changed: Zib's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Zib's wardrobe — p119/page
- **7954** changed: Cecil's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Cecil's wardrobe — p119/page
- **7955** changed: KillerWatt's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → KillerWatt's wardrobe — p119/page
- **7956** changed: Leo's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Leo's wardrobe — p119/page
- **7957** changed: Democratus's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Democratus's wardrobe — p119/page
- **7961** changed: Emma: Speed — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Emma: Speed — p119/page
- **7962** changed: Emma: Offense — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Emma: Offense — p119/page
- **7963** changed: Emma: Defense — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Emma: Defense — p119/page
- **7964** changed: Emma: Healing — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Emma: Healing — p119/page
- **7965** changed: Emma: Mining — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Emma: Mining — p119/page
- **7968** changed: Chatter on / off — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Chatter on / off — p119/page
- **8014** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → Omega 176 coins / Omega IN YOUR PACK / Omega SIGNED — p137/rc/main
- **8015** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8016** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8191** added: Spectral Blue $(r_107) — KING OMEGA · the Tailor
- **8192** added: Blood Moon $(r_108) — KING OMEGA · the Tailor
- **8193** added: Verdant Wraith $(r_109) — KING OMEGA · the Tailor
- **8194** added: Gilded King $(r_110) — KING OMEGA · the Tailor
- **8195** added: Diamond King $(r_111) — KING OMEGA · the Tailor
- **8198** added: Court of Souls (King Omega) $(r_a16) — AURAS · the Tailor
- **8200** added: Netherite King $(r_112) — KING OMEGA · the Tailor
- **8270** added: King Omega — THE TAILOR · outfits for your followers
- **8280** changed: Apophiss's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Apophiss's wardrobe — p119/page
- **8281** changed: Tullius's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Tullius's wardrobe — p119/page
- **8282** changed: The Frog's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → The Frog's wardrobe — p119/page
- **8283** changed: Donado's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Donado's wardrobe — p119/page
- **8284** changed: Pearlman's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Pearlman's wardrobe — p119/page
- **8285** changed: Wilfrey's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Wilfrey's wardrobe — p119/page
- **8286** changed: Fishy's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Fishy's wardrobe — p119/page
- **8287** changed: Dennis's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Dennis's wardrobe — p119/page
- **8288** changed: Pistachio's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger → Pistachio's wardrobe — p119/page
- **8289** added: King Omega's wardrobe — p119/page

### v2.81a
- no button changes

### v2.81
- no button changes

### v2.80i
- no button changes

### v2.80h
- **2** changed: Keep at it — Skip this puzzle? → Keep at it — Skip this puzzle?, The Fixer's mercy
- **7736** added: Pay the Fixer (half the pot, a share) — The Fixer's mercy

### v2.80g
- no button changes

### v2.80f
- no button changes

### v2.80e
- no button changes

### v2.80d
- **2110** added: 32 Coal → 1 Token $(q0)/5 — DENNIS'S ASSAY OFFICE
- **2111** added: 32 Raw Copper → 1 Token $(q1)/5 — DENNIS'S ASSAY OFFICE
- **2112** added: 24 Raw Iron → 1 Token $(q2)/5 — DENNIS'S ASSAY OFFICE
- **2113** added: 16 Raw Gold → 1 Token $(q3)/4 — DENNIS'S ASSAY OFFICE
- **2114** added: 48 Redstone Dust → 1 Token $(q4)/4 — DENNIS'S ASSAY OFFICE
- **2115** added: 32 Lapis Lazuli → 1 Token $(q5)/4 — DENNIS'S ASSAY OFFICE
- **2116** added: 32 Nether Quartz → 1 Token $(q6)/4 — DENNIS'S ASSAY OFFICE
- **2117** added: 32 Amethyst Shards → 1 Token $(q7)/3 — DENNIS'S ASSAY OFFICE
- **2118** added: Diamond → 2 Tokens $(q8)/8 — DENNIS'S ASSAY OFFICE
- **2119** added: 2 Ancient Debris → 1 Token $(q9)/4 — DENNIS'S ASSAY OFFICE
- **2151** added: « Common lots — PISTACHIO'S PANTRY · rare parts
- **2152** added: Rare parts » — PISTACHIO'S PANTRY
- **2160** added: 32 Rotten Flesh → 1 Token $(q0)/5 — PISTACHIO'S PANTRY
- **2161** added: 32 Bones → 1 Token $(q1)/5 — PISTACHIO'S PANTRY
- **2162** added: 32 String → 1 Token $(q2)/5 — PISTACHIO'S PANTRY
- **2163** added: 16 Spider Eyes → 1 Token $(q3)/4 — PISTACHIO'S PANTRY
- **2164** added: 24 Gunpowder → 1 Token $(q4)/4 — PISTACHIO'S PANTRY
- **2165** added: 16 Slimeballs → 1 Token $(q5)/4 — PISTACHIO'S PANTRY
- **2166** added: 16 Leather → 1 Token $(q6)/4 — PISTACHIO'S PANTRY
- **2167** added: 32 Feathers → 1 Token $(q7)/4 — PISTACHIO'S PANTRY
- **2168** added: 24 Ink Sacs → 1 Token $(q8)/3 — PISTACHIO'S PANTRY
- **2169** added: 8 Ender Pearls → 1 Token $(q9)/3 — PISTACHIO'S PANTRY
- **2170** added: 8 Blaze Rods → 1 Token $(q10)/3 — PISTACHIO'S PANTRY
- **2171** added: 12 Magma Cream → 1 Token $(q11)/3 — PISTACHIO'S PANTRY
- **2172** added: 8 Phantom Membranes → 1 Token $(q12)/3 — PISTACHIO'S PANTRY
- **2173** added: 24 Prismarine Shards → 1 Token $(q13)/3 — PISTACHIO'S PANTRY
- **2174** added: 8 Breeze Rods → 1 Token $(q14)/3 — PISTACHIO'S PANTRY
- **2175** added: Wither Skeleton Skull → 5 Tokens $(q15)/3 — PISTACHIO'S PANTRY · rare parts
- **2176** added: Zombie Head → 3 Tokens $(q16)/2 — PISTACHIO'S PANTRY · rare parts
- **2177** added: Skeleton Skull → 3 Tokens $(q17)/2 — PISTACHIO'S PANTRY · rare parts
- **2178** added: Creeper Head → 3 Tokens $(q18)/2 — PISTACHIO'S PANTRY · rare parts
- **2179** added: Shulker Shell → 1 Token $(q19)/2 — PISTACHIO'S PANTRY · rare parts
- **2180** added: 2 Rabbit's Feet → 1 Token $(q20)/2 — PISTACHIO'S PANTRY · rare parts
- **2181** added: 2 Ghast Tears → 1 Token $(q21)/3 — PISTACHIO'S PANTRY · rare parts
- **2201** added: Sit / follow — Dennis's Horn
- **2202** added: Wardrobe — Dennis's Horn
- **2204** added: Dennis's ways — Dennis's Horn
- **2205** added: « Back — DENNIS'S WAYS
- **2208** added: Call for Dennis — Dennis's Horn
- **2209** added: Send him home — Dennis's Horn
- **2221** added: Sit / follow — Pistachio's Little Cloche
- **2222** added: Wardrobe — Pistachio's Little Cloche
- **2224** added: Pistachio's ways — Pistachio's Little Cloche
- **2225** added: « Back — PISTACHIO'S WAYS
- **2228** added: Call for Pistachio — Pistachio's Little Cloche
- **2229** added: Send him home — Pistachio's Little Cloche
- **2240** added: $(r_home) / « Outfits & buffs — Dennis · wardrobe
- **2242** added: His old black leather $(r_dennis0) — Dennis · wardrobe
- **2243** added: Road Brown $(r_dennis1) — Dennis · wardrobe
- **2244** added: Biker Red $(r_dennis2) — Dennis · wardrobe
- **2245** added: Forest Leather $(r_dennis3) — Dennis · wardrobe
- **2246** added: Gilded Jacket $(r_dennis4) — Dennis · wardrobe
- **2247** added: Diamond Jacket $(r_dennis5) — Dennis · wardrobe
- **2248** added: Netherite Jacket $(r_dennis6) — Dennis · wardrobe
- **2259** added: Gold Rush Glimmer $(r_aura) — Dennis · wardrobe
- **2260** added: $(r_home) / « Outfits & buffs — Pistachio · wardrobe
- **2262** added: His charcoal tails $(r_pistachio0) — Pistachio · wardrobe
- **2263** added: Midnight Tails $(r_pistachio1) — Pistachio · wardrobe
- **2264** added: Claret Tails $(r_pistachio2) — Pistachio · wardrobe
- **2265** added: Ivory Tails $(r_pistachio3) — Pistachio · wardrobe
- **2266** added: Gilded Tails $(r_pistachio4) — Pistachio · wardrobe
- **2267** added: Diamond Tails $(r_pistachio5) — Pistachio · wardrobe
- **2268** added: Netherite Tails $(r_pistachio6) — Pistachio · wardrobe
- **2279** added: Ectoplasmic Mist $(r_aura) — Pistachio · wardrobe
- **7735** changed: Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe → Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Dennis · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Pistachio · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor → « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor
- **7911** added: Dennis — p103/crew/row_11
- **7912** added: Pistachio — p103/crew/row_12
- **7920** changed: The Frog — p103/crew/row_11 → The Frog — p103/crew/row_13
- **7921** changed: Donado — p103/crew/row_12 → Donado — p103/crew/row_14
- **8012** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → Dennis 176 coins / Dennis IN YOUR PACK / Dennis SIGNED — p137/rc/main
- **8013** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → Pistachio 176 coins / Pistachio IN YOUR PACK / Pistachio SIGNED — p137/rc/main
- **8014** added: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8015** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8108** added: Dennis — THE TAILOR · outfits for your followers
- **8109** added: Pistachio — THE TAILOR · outfits for your followers
- **8179** added: Road Brown $(r_95) — DENNIS · the Tailor
- **8180** added: Biker Red $(r_96) — DENNIS · the Tailor
- **8181** added: Forest Leather $(r_97) — DENNIS · the Tailor
- **8182** added: Gilded Jacket $(r_98) — DENNIS · the Tailor
- **8183** added: Diamond Jacket $(r_99) — DENNIS · the Tailor
- **8184** added: Netherite Jacket $(r_100) — DENNIS · the Tailor
- **8185** added: Midnight Tails $(r_101) — PISTACHIO · the Tailor
- **8186** added: Claret Tails $(r_102) — PISTACHIO · the Tailor
- **8187** added: Ivory Tails $(r_103) — PISTACHIO · the Tailor
- **8188** added: Gilded Tails $(r_104) — PISTACHIO · the Tailor
- **8189** added: Diamond Tails $(r_105) — PISTACHIO · the Tailor
- **8190** added: Netherite Tails $(r_106) — PISTACHIO · the Tailor
- **8196** added: Gold Rush Glimmer (Dennis) $(r_a14) — AURAS · the Tailor
- **8197** added: Ectoplasmic Mist (Pistachio) $(r_a15) — AURAS · the Tailor
- **8287** added: Dennis's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **8288** added: Pistachio's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger

### v2.80c
- **7762** changed: Flower Top $(r_12) — EMMA · the Tailor → Diamond Gown $(r_12) — EMMA · the Tailor
- **7763** changed: Cozy Sweater $(r_13) — EMMA · the Tailor → Netherite Gown $(r_13) — EMMA · the Tailor
- **7764** changed: Aurora $(r_14) — CELI · the Tailor → Flower Top $(r_14) — EMMA · the Tailor
- **7765** changed: Rosehip $(r_15) — CELI · the Tailor → Cozy Sweater $(r_15) — EMMA · the Tailor
- **7766** changed: Midnight $(r_16) — CELI · the Tailor → Aurora $(r_16) — CELI · the Tailor
- **7767** changed: Frostfire $(r_17) — CELI · the Tailor → Rosehip $(r_17) — CELI · the Tailor
- **7768** changed: Gilded $(r_18) — CELI · the Tailor → Midnight $(r_18) — CELI · the Tailor
- **7769** changed: Crimson Guard $(r_19) — ZIB · the Tailor → Frostfire $(r_19) — CELI · the Tailor
- **7770** changed: Forest Ranger $(r_20) — ZIB · the Tailor → Gilded $(r_20) — CELI · the Tailor
- **7771** changed: Golden Ace $(r_21) — ZIB · the Tailor → Diamond $(r_21) — CELI · the Tailor
- **7772** changed: Crimson Crusader $(r_22) — LEO · the Tailor → Netherite $(r_22) — CELI · the Tailor
- **7773** changed: Royal Purple $(r_23) — LEO · the Tailor → Crimson Guard $(r_23) — ZIB · the Tailor
- **7774** changed: Greenwood $(r_24) — LEO · the Tailor → Forest Ranger $(r_24) — ZIB · the Tailor
- **7775** changed: Golden Champion $(r_25) — LEO · the Tailor → Golden Ace $(r_25) — ZIB · the Tailor
- **7776** changed: Crimson Reaper $(r_26) — DEMOCRATUS · the Tailor → Diamond Ace $(r_26) — ZIB · the Tailor
- **7777** changed: Ashen Shroud $(r_27) — DEMOCRATUS · the Tailor → Netherite Ace $(r_27) — ZIB · the Tailor
- **7778** changed: Royal Violet $(r_28) — DEMOCRATUS · the Tailor → Crimson Crusader $(r_28) — LEO · the Tailor
- **7779** changed: Gilded Storm $(r_29) — DEMOCRATUS · the Tailor → Royal Purple $(r_29) — LEO · the Tailor
- **7780** changed: Crimson $(r_30) — CECIL · the Tailor → Greenwood $(r_30) — LEO · the Tailor
- **7781** changed: Midnight $(r_31) — CECIL · the Tailor → Golden Champion $(r_31) — LEO · the Tailor
- **7782** changed: Bone $(r_32) — CECIL · the Tailor → Diamond Champion $(r_32) — LEO · the Tailor
- **7783** changed: Gilded $(r_33) — CECIL · the Tailor → Netherite Champion $(r_33) — LEO · the Tailor
- **7784** changed: Midnight $(r_34) — KILLERWATT · the Tailor → Crimson Reaper $(r_34) — DEMOCRATUS · the Tailor
- **7785** changed: Bone $(r_35) — KILLERWATT · the Tailor → Ashen Shroud $(r_35) — DEMOCRATUS · the Tailor
- **7786** changed: Neon $(r_36) — KILLERWATT · the Tailor → Royal Violet $(r_36) — DEMOCRATUS · the Tailor
- **7787** changed: Golden Thunder $(r_37) — KILLERWATT · the Tailor → Gilded Storm $(r_37) — DEMOCRATUS · the Tailor
- **7788** changed: Obsidian Coil $(r_38) — APOPHISS · the Tailor → Diamond Storm $(r_38) — DEMOCRATUS · the Tailor
- **7789** changed: Blood Wyrm $(r_39) — APOPHISS · the Tailor → Netherite Storm $(r_39) — DEMOCRATUS · the Tailor
- **8110** changed: Frost Serpent $(r_40) — APOPHISS · the Tailor → Crimson $(r_40) — CECIL · the Tailor
- **8111** changed: Gilded Coil $(r_41) — APOPHISS · the Tailor → Midnight $(r_41) — CECIL · the Tailor
- **8112** changed: Admiral's Blue $(r_42) — TULLIUS · the Tailor → Bone $(r_42) — CECIL · the Tailor
- **8113** changed: Corsair Crimson $(r_43) — TULLIUS · the Tailor → Gilded $(r_43) — CECIL · the Tailor
- **8114** changed: Bleached Bone $(r_44) — TULLIUS · the Tailor → Diamond $(r_44) — CECIL · the Tailor
- **8115** changed: Gilded Captain $(r_45) — TULLIUS · the Tailor → Netherite $(r_45) — CECIL · the Tailor
- **8116** changed: Bluejay $(r_46) — THE FROG · the Tailor → Midnight $(r_46) — KILLERWATT · the Tailor
- **8117** changed: Ember Toad $(r_47) — THE FROG · the Tailor → Bone $(r_47) — KILLERWATT · the Tailor
- **8118** changed: Old Bog $(r_48) — THE FROG · the Tailor → Neon $(r_48) — KILLERWATT · the Tailor
- **8119** changed: Golden Prince $(r_49) — THE FROG · the Tailor → Golden Thunder $(r_49) — KILLERWATT · the Tailor
- **8120** changed: Chocolate $(r_50) — DONADO · the Tailor → Diamond Thunder $(r_50) — KILLERWATT · the Tailor
- **8121** changed: Midnight $(r_51) — DONADO · the Tailor → Netherite Thunder $(r_51) — KILLERWATT · the Tailor
- **8122** changed: Snowdrift $(r_52) — DONADO · the Tailor → Obsidian Coil $(r_52) — APOPHISS · the Tailor
- **8123** changed: Starlit $(r_53) — DONADO · the Tailor → Blood Wyrm $(r_53) — APOPHISS · the Tailor
- **8124** changed: Gilded $(r_54) — DONADO · the Tailor → Frost Serpent $(r_54) — APOPHISS · the Tailor
- **8125** changed: Ruby $(r_55) — PEARLMAN · the Tailor → Gilded Coil $(r_55) — APOPHISS · the Tailor
- **8126** changed: Emerald $(r_56) — PEARLMAN · the Tailor → Diamond Coil $(r_56) — APOPHISS · the Tailor
- **8127** changed: Amethyst $(r_57) — PEARLMAN · the Tailor → Netherite Coil $(r_57) — APOPHISS · the Tailor
- **8128** changed: Gilded $(r_58) — PEARLMAN · the Tailor → Admiral's Blue $(r_58) — TULLIUS · the Tailor
- **8129** changed: Midnight Silk $(r_59) — FISHY · the Tailor → Corsair Crimson $(r_59) — TULLIUS · the Tailor
- **8130** changed: Crimson Opera $(r_60) — FISHY · the Tailor → Bleached Bone $(r_60) — TULLIUS · the Tailor
- **8131** changed: Emerald Ascot $(r_61) — FISHY · the Tailor → Gilded Captain $(r_61) — TULLIUS · the Tailor
- **8132** changed: Gilded Topper $(r_62) — FISHY · the Tailor → Diamond Captain $(r_62) — TULLIUS · the Tailor
- **8133** changed: Crimson Cross $(r_63) — WILFREY · the Tailor → Netherite Captain $(r_63) — TULLIUS · the Tailor
- **8134** changed: Azure Chevron $(r_64) — WILFREY · the Tailor → Bluejay $(r_64) — THE FROG · the Tailor
- **8135** changed: Verdant Bend $(r_65) — WILFREY · the Tailor → Ember Toad $(r_65) — THE FROG · the Tailor
- **8136** changed: Gilded Sun $(r_66) — WILFREY · the Tailor → Old Bog $(r_66) — THE FROG · the Tailor
- **8137** added: Golden Prince $(r_67) — THE FROG · the Tailor
- **8138** added: Diamond Prince $(r_68) — THE FROG · the Tailor
- **8139** added: Netherite Prince $(r_69) — THE FROG · the Tailor
- **8140** added: Chocolate $(r_70) — DONADO · the Tailor
- **8141** added: Midnight $(r_71) — DONADO · the Tailor
- **8142** added: Snowdrift $(r_72) — DONADO · the Tailor
- **8143** added: Starlit $(r_73) — DONADO · the Tailor
- **8144** added: Gilded $(r_74) — DONADO · the Tailor
- **8145** added: Diamond $(r_75) — DONADO · the Tailor
- **8146** added: Netherite $(r_76) — DONADO · the Tailor
- **8147** added: Ruby $(r_77) — PEARLMAN · the Tailor
- **8148** added: Emerald $(r_78) — PEARLMAN · the Tailor
- **8149** added: Amethyst $(r_79) — PEARLMAN · the Tailor
- **8164** added: Gilded $(r_80) — PEARLMAN · the Tailor
- **8165** added: Diamond $(r_81) — PEARLMAN · the Tailor
- **8166** added: Netherite $(r_82) — PEARLMAN · the Tailor
- **8167** added: Midnight Silk $(r_83) — FISHY · the Tailor
- **8168** added: Crimson Opera $(r_84) — FISHY · the Tailor
- **8169** added: Emerald Ascot $(r_85) — FISHY · the Tailor
- **8170** added: Gilded Topper $(r_86) — FISHY · the Tailor
- **8171** added: Diamond Topper $(r_87) — FISHY · the Tailor
- **8172** added: Netherite Topper $(r_88) — FISHY · the Tailor
- **8173** added: Crimson Cross $(r_89) — WILFREY · the Tailor
- **8174** added: Azure Chevron $(r_90) — WILFREY · the Tailor
- **8175** added: Verdant Bend $(r_91) — WILFREY · the Tailor
- **8176** added: Gilded Sun $(r_92) — WILFREY · the Tailor
- **8177** added: Diamond Sun $(r_93) — WILFREY · the Tailor
- **8178** added: Netherite Sun $(r_94) — WILFREY · the Tailor
- **9007** added: Diamond Coil $(r_apo5) — Apophiss · wardrobe
- **9008** added: Netherite Coil $(r_apo6) — Apophiss · wardrobe
- **9027** added: Diamond Captain $(r_tul5) — Tullius · wardrobe
- **9028** added: Netherite Captain $(r_tul6) — Tullius · wardrobe
- **9047** added: Diamond Prince $(r_frog5) — the Frog with Mustache · wardrobe
- **9048** added: Netherite Prince $(r_frog6) — the Frog with Mustache · wardrobe
- **9068** added: Diamond $(r_don6) — Donado · wardrobe
- **9069** added: Netherite $(r_don7) — Donado · wardrobe
- **9087** added: Diamond $(r_pearl5) — Pearlman · wardrobe
- **9088** added: Netherite $(r_pearl6) — Pearlman · wardrobe
- **9107** added: Diamond Sun $(r_wil5) — Wilfrey · wardrobe
- **9108** added: Netherite Sun $(r_wil6) — Wilfrey · wardrobe
- **9127** added: Diamond Topper $(r_fishy5) — Fishy · wardrobe
- **9128** added: Netherite Topper $(r_fishy6) — Fishy · wardrobe
- **9819** added: Diamond Gown $(r_dress7) — Emma · wardrobe
- **9820** added: Netherite Gown $(r_dress8) — Emma · wardrobe
- **9848** added: Diamond $(r_celi6) — Celi · wardrobe
- **9849** added: Netherite $(r_celi7) — Celi · wardrobe
- **9866** added: Diamond Ace $(r_zib4) — Zib · wardrobe
- **9867** added: Netherite Ace $(r_zib5) — Zib · wardrobe
- **9887** added: Diamond $(r_cecil5) — Cecil · wardrobe
- **9888** added: Netherite $(r_cecil6) — Cecil · wardrobe
- **9907** added: Diamond Thunder $(r_kw5) — KillerWatt · wardrobe
- **9908** added: Netherite Thunder $(r_kw6) — KillerWatt · wardrobe
- **9927** added: Diamond Champion $(r_leo5) — Leo · wardrobe
- **9928** added: Netherite Champion $(r_leo6) — Leo · wardrobe
- **9947** added: Diamond Storm $(r_demo5) — Democratus · wardrobe
- **9948** added: Netherite Storm $(r_demo6) — Democratus · wardrobe

### v2.80b
- no button changes

### v2.80a
- no button changes

### v2.80
- **7802** changed: Gutter Bank / « Back / ⛃ Gutter Bank — THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies, THE GUTTER BANK · take out coins, THE GUTTER BANK · take out spoils → Gutter Bank / « Back / « Your account / ⛃ Gutter Bank — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank, THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies
- **7841** removed (was: Take 16 coins — THE GUTTER BANK · take out coins)
- **7842** removed (was: Take 64 coins — THE GUTTER BANK · take out coins)
- **7843** removed (was: Take all my coins — THE GUTTER BANK · take out coins)
- **7846** removed (was: ⬆ Take out coins — THE GUTTER BANK · your coins and spoils)
- **7847** removed (was: ⬆ Take out spoils — THE GUTTER BANK · your coins and spoils)
- **7851** removed (was: Copper Cogs ($(m1)) — THE GUTTER BANK · take out spoils)
- **7852** removed (was: Silver Seals ($(m2)) — THE GUTTER BANK · take out spoils)
- **7853** removed (was: Gilded Leaves ($(m3)) — THE GUTTER BANK · take out spoils)
- **7854** removed (was: Deep Pearls ($(m4)) — THE GUTTER BANK · take out spoils)
- **7855** removed (was: Hoard Embers ($(m5)) — THE GUTTER BANK · take out spoils)
- **7856** removed (was: Captain's Insignia ($(m6)) — THE GUTTER BANK · take out spoils)
- **7870** changed: ⇄ Medallions & Trophies — THE GUTTER BANK · your coins and spoils → ⇄ Change coins — GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, THE GUTTER BANK · your coins and spoils
- **7871** removed (was: Take 1 Medallion — THE GUTTER BANK · Medallions & Trophies)
- **7872** removed (was: Take all Medallions — THE GUTTER BANK · Medallions & Trophies)
- **7873** removed (was: Take 1 Trophy — THE GUTTER BANK · Medallions & Trophies)
- **7874** removed (was: Take all Trophies — THE GUTTER BANK · Medallions & Trophies)
- **7970** added: Gutter Coins $(c) — THE GUTTER BANK · your coins and spoils
- **7971** added: Gutter Medallions $(gm) — THE GUTTER BANK · your coins and spoils
- **7972** added: Gutter Trophies $(gt) — THE GUTTER BANK · your coins and spoils
- **7973** added: Copper Cogs $(m1) — THE GUTTER BANK · your coins and spoils
- **7974** added: Silver Seals $(m2) — THE GUTTER BANK · your coins and spoils
- **7975** added: Gilded Leaves $(m3) — THE GUTTER BANK · your coins and spoils
- **7976** added: Deep Pearls $(m4) — THE GUTTER BANK · your coins and spoils
- **7977** added: Hoard Embers $(m5) — THE GUTTER BANK · your coins and spoils
- **7978** added: Captain's Insignia $(m6) — THE GUTTER BANK · your coins and spoils
- **7980** added: ⬇ Deposit 1 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank
- **7981** added: ⬇ Deposit 10 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank
- **7982** added: ⬇ Deposit all ($(h)) — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank
- **7983** added: ⬆ Take 1 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank
- **7984** added: ⬆ Take 10 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank
- **7985** added: ⬆ Take all ($(n)) — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank

### v2.79c
- **4010** changed: Deposit all Tokens — The Rat Bank - your account → Deposit all Tokens ($(h)) — Tokens · The Rat Bank
- **4011** changed: Take 1 — The Rat Bank - your account → Take 1 — Tokens · The Rat Bank
- **4012** changed: Take 10 — The Rat Bank - your account → Take 10 — Tokens · The Rat Bank
- **4013** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Tokens · The Rat Bank
- **4014** changed: Deposit all Lucky Tokens — The Rat Bank - your account → Deposit all Lucky Tokens ($(h)) — Lucky Tokens · The Rat Bank
- **4015** changed: Take 1 — The Rat Bank - your account → Take 1 — Lucky Tokens · The Rat Bank
- **4016** changed: Take 10 — The Rat Bank - your account → Take 10 — Lucky Tokens · The Rat Bank
- **4017** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Lucky Tokens · The Rat Bank
- **4018** changed: Deposit all Medallions — The Rat Bank - your account → Deposit all Medallions ($(h)) — Medallions · The Rat Bank
- **4019** changed: Take 1 — The Rat Bank - your account → Take 1 — Medallions · The Rat Bank
- **4020** changed: Take 10 — The Rat Bank - your account → Take 10 — Medallions · The Rat Bank
- **4021** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Medallions · The Rat Bank
- **4022** changed: Deposit all Trophies — The Rat Bank - your account → Deposit all Trophies ($(h)) — Trophies · The Rat Bank
- **4023** changed: Take 1 — The Rat Bank - your account → Take 1 — Trophies · The Rat Bank
- **4024** changed: Take 10 — The Rat Bank - your account → Take 10 — Trophies · The Rat Bank
- **4025** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Trophies · The Rat Bank
- **4026** changed: Deposit all Blood Crystals — The Rat Bank - your account → Deposit all Blood Crystals ($(h)) — Blood Crystals · The Rat Bank
- **4027** changed: Take 1 — The Rat Bank - your account → Take 1 — Blood Crystals · The Rat Bank
- **4028** changed: Take 10 — The Rat Bank - your account → Take 10 — Blood Crystals · The Rat Bank
- **4029** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Blood Crystals · The Rat Bank
- **4030** changed: Deposit all Ember Scales — The Rat Bank - your account → Deposit all Ember Scales ($(h)) — Ember Scales · The Rat Bank
- **4031** changed: Take 1 — The Rat Bank - your account → Take 1 — Ember Scales · The Rat Bank
- **4032** changed: Take 10 — The Rat Bank - your account → Take 10 — Ember Scales · The Rat Bank
- **4033** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Ember Scales · The Rat Bank
- **4034** changed: Deposit all Void Shards — The Rat Bank - your account → Deposit all Void Shards ($(h)) — Void Shards · The Rat Bank
- **4035** changed: Take 1 — The Rat Bank - your account → Take 1 — Void Shards · The Rat Bank
- **4036** changed: Take 10 — The Rat Bank - your account → Take 10 — Void Shards · The Rat Bank
- **4037** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Void Shards · The Rat Bank
- **4038** changed: Deposit all Green Xenite — The Rat Bank - your account → Deposit all Green Xenite ($(h)) — Green Xenite · The Rat Bank
- **4039** changed: Take 1 — The Rat Bank - your account → Take 1 — Green Xenite · The Rat Bank
- **4040** changed: Take 10 — The Rat Bank - your account → Take 10 — Green Xenite · The Rat Bank
- **4041** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Green Xenite · The Rat Bank
- **4042** changed: Deposit all Violet Xenite — The Rat Bank - your account → Deposit all Violet Xenite ($(h)) — Violet Xenite · The Rat Bank
- **4043** changed: Take 1 — The Rat Bank - your account → Take 1 — Violet Xenite · The Rat Bank
- **4044** changed: Take 10 — The Rat Bank - your account → Take 10 — Violet Xenite · The Rat Bank
- **4045** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Violet Xenite · The Rat Bank
- **4046** changed: Deposit all Cyan Xenite — The Rat Bank - your account → Deposit all Cyan Xenite ($(h)) — Cyan Xenite · The Rat Bank
- **4047** changed: Take 1 — The Rat Bank - your account → Take 1 — Cyan Xenite · The Rat Bank
- **4048** changed: Take 10 — The Rat Bank - your account → Take 10 — Cyan Xenite · The Rat Bank
- **4049** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Cyan Xenite · The Rat Bank
- **4050** changed: Deposit all Red Xenite — The Rat Bank - your account → Deposit all Red Xenite ($(h)) — Red Xenite · The Rat Bank
- **4051** changed: Take 1 — The Rat Bank - your account → Take 1 — Red Xenite · The Rat Bank
- **4052** changed: Take 10 — The Rat Bank - your account → Take 10 — Red Xenite · The Rat Bank
- **4053** changed: Take all — The Rat Bank - your account → Take all ($(n)) — Red Xenite · The Rat Bank
- **4060** added: Tokens $(token) — The Rat Bank - your account
- **4061** added: Lucky Tokens $(lucky_token) — The Rat Bank - your account
- **4062** added: Medallions $(medallion) — The Rat Bank - your account
- **4063** added: Trophies $(trophy) — The Rat Bank - your account
- **4064** added: Blood Crystals $(blood_crystal) — The Rat Bank - your account
- **4065** added: Ember Scales $(ember_scale) — The Rat Bank - your account
- **4066** added: Void Shards $(void_shard) — The Rat Bank - your account
- **4067** added: Green Xenite $(xenite_green) — The Rat Bank - your account
- **4068** added: Violet Xenite $(xenite_violet) — The Rat Bank - your account
- **4069** added: Cyan Xenite $(xenite_cyan) — The Rat Bank - your account
- **4070** added: Red Xenite $(xenite_red) — The Rat Bank - your account
- **4071** added: Deposit everything — The Rat Bank - your account
- **4072** added: « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank
- **7801** changed: « Armory / ⚒ Armory — THE FIXER'S OFFICE · everything the vault owes you, YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own → « Armory / ⚒ Armory — THE FIXER'S OFFICE · everything the vault owes you, THE OFFENSE KIT · rank $(r2), THE RANGED KIT · rank $(r3), THE SUPPORT KIT · rank $(r4), THE TANK KIT · rank $(r1), YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own
- **7811** changed: ⬆ Tank — THE ARMORY · your kits, for good → ⬆ Rank up — THE TANK KIT · rank $(r1)
- **7812** changed: ⬆ Offense — THE ARMORY · your kits, for good → ⬆ Rank up — THE OFFENSE KIT · rank $(r2)
- **7813** changed: ⬆ Ranged — THE ARMORY · your kits, for good → ⬆ Rank up — THE RANGED KIT · rank $(r3)
- **7814** changed: ⬆ Support — THE ARMORY · your kits, for good → ⬆ Rank up — THE SUPPORT KIT · rank $(r4)
- **7815** added: Tank › — THE ARMORY · your kits, for good
- **7816** added: Offense › — THE ARMORY · your kits, for good
- **7817** added: Ranged › — THE ARMORY · your kits, for good
- **7818** added: Support › — THE ARMORY · your kits, for good

### v2.79b
- no button changes

### v2.79a
- **7761** changed: Flower Top $(r_11) — EMMA · the Tailor → Gilded Gown $(r_11) — EMMA · the Tailor
- **7762** changed: Cozy Sweater $(r_12) — EMMA · the Tailor → Flower Top $(r_12) — EMMA · the Tailor
- **7763** changed: Aurora $(r_13) — CELI · the Tailor → Cozy Sweater $(r_13) — EMMA · the Tailor
- **7764** changed: Rosehip $(r_14) — CELI · the Tailor → Aurora $(r_14) — CELI · the Tailor
- **7765** changed: Midnight $(r_15) — CELI · the Tailor → Rosehip $(r_15) — CELI · the Tailor
- **7766** changed: Frostfire $(r_16) — CELI · the Tailor → Midnight $(r_16) — CELI · the Tailor
- **7767** changed: Crimson Guard $(r_17) — ZIB · the Tailor → Frostfire $(r_17) — CELI · the Tailor
- **7768** changed: Forest Ranger $(r_18) — ZIB · the Tailor → Gilded $(r_18) — CELI · the Tailor
- **7769** changed: Golden Ace $(r_19) — ZIB · the Tailor → Crimson Guard $(r_19) — ZIB · the Tailor
- **7770** changed: Crimson Crusader $(r_20) — LEO · the Tailor → Forest Ranger $(r_20) — ZIB · the Tailor
- **7771** changed: Royal Purple $(r_21) — LEO · the Tailor → Golden Ace $(r_21) — ZIB · the Tailor
- **7772** changed: Greenwood $(r_22) — LEO · the Tailor → Crimson Crusader $(r_22) — LEO · the Tailor
- **7773** changed: Golden Champion $(r_23) — LEO · the Tailor → Royal Purple $(r_23) — LEO · the Tailor
- **7774** changed: Crimson Reaper $(r_24) — DEMOCRATUS · the Tailor → Greenwood $(r_24) — LEO · the Tailor
- **7775** changed: Ashen Shroud $(r_25) — DEMOCRATUS · the Tailor → Golden Champion $(r_25) — LEO · the Tailor
- **7776** changed: Royal Violet $(r_26) — DEMOCRATUS · the Tailor → Crimson Reaper $(r_26) — DEMOCRATUS · the Tailor
- **7777** changed: Gilded Storm $(r_27) — DEMOCRATUS · the Tailor → Ashen Shroud $(r_27) — DEMOCRATUS · the Tailor
- **7778** changed: Crimson $(r_28) — CECIL · the Tailor → Royal Violet $(r_28) — DEMOCRATUS · the Tailor
- **7779** changed: Midnight $(r_29) — CECIL · the Tailor → Gilded Storm $(r_29) — DEMOCRATUS · the Tailor
- **7780** changed: Bone $(r_30) — CECIL · the Tailor → Crimson $(r_30) — CECIL · the Tailor
- **7781** changed: Gilded $(r_31) — CECIL · the Tailor → Midnight $(r_31) — CECIL · the Tailor
- **7782** changed: Midnight $(r_32) — KILLERWATT · the Tailor → Bone $(r_32) — CECIL · the Tailor
- **7783** changed: Bone $(r_33) — KILLERWATT · the Tailor → Gilded $(r_33) — CECIL · the Tailor
- **7784** changed: Neon $(r_34) — KILLERWATT · the Tailor → Midnight $(r_34) — KILLERWATT · the Tailor
- **7785** changed: Golden Thunder $(r_35) — KILLERWATT · the Tailor → Bone $(r_35) — KILLERWATT · the Tailor
- **7786** changed: Obsidian Coil $(r_36) — APOPHISS · the Tailor → Neon $(r_36) — KILLERWATT · the Tailor
- **7787** changed: Blood Wyrm $(r_37) — APOPHISS · the Tailor → Golden Thunder $(r_37) — KILLERWATT · the Tailor
- **7788** changed: Frost Serpent $(r_38) — APOPHISS · the Tailor → Obsidian Coil $(r_38) — APOPHISS · the Tailor
- **7789** changed: Gilded Coil $(r_39) — APOPHISS · the Tailor → Blood Wyrm $(r_39) — APOPHISS · the Tailor
- **8110** changed: Admiral's Blue $(r_40) — TULLIUS · the Tailor → Frost Serpent $(r_40) — APOPHISS · the Tailor
- **8111** changed: Corsair Crimson $(r_41) — TULLIUS · the Tailor → Gilded Coil $(r_41) — APOPHISS · the Tailor
- **8112** changed: Bleached Bone $(r_42) — TULLIUS · the Tailor → Admiral's Blue $(r_42) — TULLIUS · the Tailor
- **8113** changed: Gilded Captain $(r_43) — TULLIUS · the Tailor → Corsair Crimson $(r_43) — TULLIUS · the Tailor
- **8114** changed: Bluejay $(r_44) — THE FROG · the Tailor → Bleached Bone $(r_44) — TULLIUS · the Tailor
- **8115** changed: Ember Toad $(r_45) — THE FROG · the Tailor → Gilded Captain $(r_45) — TULLIUS · the Tailor
- **8116** changed: Old Bog $(r_46) — THE FROG · the Tailor → Bluejay $(r_46) — THE FROG · the Tailor
- **8117** changed: Golden Prince $(r_47) — THE FROG · the Tailor → Ember Toad $(r_47) — THE FROG · the Tailor
- **8118** changed: Chocolate $(r_48) — DONADO · the Tailor → Old Bog $(r_48) — THE FROG · the Tailor
- **8119** changed: Midnight $(r_49) — DONADO · the Tailor → Golden Prince $(r_49) — THE FROG · the Tailor
- **8120** changed: Snowdrift $(r_50) — DONADO · the Tailor → Chocolate $(r_50) — DONADO · the Tailor
- **8121** changed: Starlit $(r_51) — DONADO · the Tailor → Midnight $(r_51) — DONADO · the Tailor
- **8122** changed: Ruby $(r_52) — PEARLMAN · the Tailor → Snowdrift $(r_52) — DONADO · the Tailor
- **8123** changed: Emerald $(r_53) — PEARLMAN · the Tailor → Starlit $(r_53) — DONADO · the Tailor
- **8124** changed: Amethyst $(r_54) — PEARLMAN · the Tailor → Gilded $(r_54) — DONADO · the Tailor
- **8125** changed: Gilded $(r_55) — PEARLMAN · the Tailor → Ruby $(r_55) — PEARLMAN · the Tailor
- **8126** changed: Midnight Silk $(r_56) — FISHY · the Tailor → Emerald $(r_56) — PEARLMAN · the Tailor
- **8127** changed: Crimson Opera $(r_57) — FISHY · the Tailor → Amethyst $(r_57) — PEARLMAN · the Tailor
- **8128** changed: Emerald Ascot $(r_58) — FISHY · the Tailor → Gilded $(r_58) — PEARLMAN · the Tailor
- **8129** changed: Gilded Topper $(r_59) — FISHY · the Tailor → Midnight Silk $(r_59) — FISHY · the Tailor
- **8130** changed: Crimson Cross $(r_60) — WILFREY · the Tailor → Crimson Opera $(r_60) — FISHY · the Tailor
- **8131** changed: Azure Chevron $(r_61) — WILFREY · the Tailor → Emerald Ascot $(r_61) — FISHY · the Tailor
- **8132** changed: Verdant Bend $(r_62) — WILFREY · the Tailor → Gilded Topper $(r_62) — FISHY · the Tailor
- **8133** changed: Gilded Sun $(r_63) — WILFREY · the Tailor → Crimson Cross $(r_63) — WILFREY · the Tailor
- **8134** added: Azure Chevron $(r_64) — WILFREY · the Tailor
- **8135** added: Verdant Bend $(r_65) — WILFREY · the Tailor
- **8136** added: Gilded Sun $(r_66) — WILFREY · the Tailor
- **9067** added: Gilded $(r_don5) — Donado · wardrobe
- **9818** added: Gilded Gown $(r_dress6) — Emma · wardrobe
- **9847** added: Gilded $(r_celi5) — Celi · wardrobe

### v2.79
- **7735** changed: Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Donado · wardrobe, Emma · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe → Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Donado · wardrobe, Emma · wardrobe, Fishy · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe
- **7740** changed: « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor → « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor
- **7910** added: Fishy — p103/crew/row_10
- **7920** changed: The Frog — p103/crew/row_10 → The Frog — p103/crew/row_11
- **7921** changed: Donado — p103/crew/row_11 → Donado — p103/crew/row_12
- **8011** changed: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main → Fishy 176 coins / Fishy IN YOUR PACK / Fishy SIGNED — p137/rc/main
- **8012** changed: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main → The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8013** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8107** added: Fishy — THE TAILOR · outfits for your followers
- **8126** changed: Crimson Cross $(r_56) — WILFREY · the Tailor → Midnight Silk $(r_56) — FISHY · the Tailor
- **8127** changed: Azure Chevron $(r_57) — WILFREY · the Tailor → Crimson Opera $(r_57) — FISHY · the Tailor
- **8128** changed: Verdant Bend $(r_58) — WILFREY · the Tailor → Emerald Ascot $(r_58) — FISHY · the Tailor
- **8129** changed: Gilded Sun $(r_59) — WILFREY · the Tailor → Gilded Topper $(r_59) — FISHY · the Tailor
- **8130** added: Crimson Cross $(r_60) — WILFREY · the Tailor
- **8131** added: Azure Chevron $(r_61) — WILFREY · the Tailor
- **8132** added: Verdant Bend $(r_62) — WILFREY · the Tailor
- **8133** added: Gilded Sun $(r_63) — WILFREY · the Tailor
- **8163** added: Bubble Halo (Fishy) $(r_a13) — AURAS · the Tailor
- **8286** added: Fishy's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **9120** added: $(r_home) / « Outfits & buffs — Fishy · wardrobe
- **9122** added: His old black topper $(r_fishy0) — Fishy · wardrobe
- **9123** added: Midnight Silk $(r_fishy1) — Fishy · wardrobe
- **9124** added: Crimson Opera $(r_fishy2) — Fishy · wardrobe
- **9125** added: Emerald Ascot $(r_fishy3) — Fishy · wardrobe
- **9126** added: Gilded Topper $(r_fishy4) — Fishy · wardrobe
- **9139** added: Bubble Halo $(r_aura) — Fishy · wardrobe
- **9141** added: Sit / follow — Fishy's Pocket Bowl
- **9142** added: Wardrobe — Fishy's Pocket Bowl
- **9143** added: The Cabinet — Fishy's Pocket Bowl
- **9144** added: Fishy's powers — Fishy's Pocket Bowl
- **9148** added: Call for Fishy — Fishy's Pocket Bowl
- **9149** added: Send him home — Fishy's Pocket Bowl
- **9150** added: « The Cabinet — FISHY'S POWERS · taught by the Cabinet, THE COURT · $(n) of 20, THE DEEP · $(n) of 20, THE GUTTER · $(n) of 20, THE HOLLOW · $(n) of 20, THE SKIES · $(n) of 20, THE WILDS · $(n) of 20
- **9151** added: The Hollow $(c_hollow) of 20$(r_hollow) — FISHY'S CABINET OF CURIOSITIES
- **9152** added: The Gutter $(c_gutter) of 20$(r_gutter) — FISHY'S CABINET OF CURIOSITIES
- **9153** added: The Skies $(c_skies) of 20$(r_skies) — FISHY'S CABINET OF CURIOSITIES
- **9154** added: The Deep $(c_deep) of 20$(r_deep) — FISHY'S CABINET OF CURIOSITIES
- **9155** added: The Wilds $(c_wilds) of 20$(r_wilds) — FISHY'S CABINET OF CURIOSITIES
- **9156** added: The Court $(c_court) of 20$(r_court) — FISHY'S CABINET OF CURIOSITIES
- **9157** added: Fishy's powers — FISHY'S CABINET OF CURIOSITIES
- **9158** added: Set it out in the hall — THE COURT · $(n) of 20, THE DEEP · $(n) of 20, THE GUTTER · $(n) of 20, THE HOLLOW · $(n) of 20, THE SKIES · $(n) of 20, THE WILDS · $(n) of 20

### v2.78c
- no button changes

### v2.78b
- no button changes

### v2.78a
- no button changes

### v2.78
- no button changes

### v2.77d
- **7735** changed: Chatter: $(chat) (all followers) — Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Emma · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Zib · wardrobe → Chatter: $(chat) (all followers) — Apophiss · wardrobe, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Donado · wardrobe, Emma · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Pearlman · wardrobe, Tullius · wardrobe, Wilfrey · wardrobe, Zib · wardrobe, the Frog with Mustache · wardrobe
- **7740** changed: « The Tailor — CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DISPLAY CASES · the Tailor, EMMA · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, ZIB · the Tailor → « The Tailor — APOPHISS · the Tailor, AURAS · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, PEARLMAN · the Tailor, THE FROG · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor
- **7786** added: Obsidian Coil $(r_36) — APOPHISS · the Tailor
- **7787** added: Blood Wyrm $(r_37) — APOPHISS · the Tailor
- **7788** added: Frost Serpent $(r_38) — APOPHISS · the Tailor
- **7789** added: Gilded Coil $(r_39) — APOPHISS · the Tailor
- **7801** changed: « Armory / ⚒ The Armory — THE FIXER'S OFFICE · everything the vault owes you, YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own → « Armory / ⚒ Armory — THE FIXER'S OFFICE · everything the vault owes you, YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own
- **7802** changed: Gutter Bank / « Back / ⛃ The Gutter Bank — THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies, THE GUTTER BANK · take out coins, THE GUTTER BANK · take out spoils → Gutter Bank / « Back / ⛃ Gutter Bank — THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies, THE GUTTER BANK · take out coins, THE GUTTER BANK · take out spoils
- **7805** changed: ▣ The Locker Hall — THE FIXER'S OFFICE · everything the vault owes you → ▣ Locker Hall — THE FIXER'S OFFICE · everything the vault owes you
- **7806** changed: ⛁ The Crate Desk — THE FIXER'S OFFICE · everything the vault owes you → ⛁ Crate Desk — THE FIXER'S OFFICE · everything the vault owes you
- **7808** changed: ◀ The Codex / 📖 The Codex — THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 23 → ◀ The Codex / 📖 Codex — THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 23
- **7809** changed: ⚑ Plan a Heist or join your party's — THE FIXER'S OFFICE · everything the vault owes you → ⚑ Plan a Heist — THE FIXER'S OFFICE · everything the vault owes you
- **7880** changed: ⌂ The Fixer's Lounge — THE FIXER'S OFFICE · everything the vault owes you → ⌂ Fixer's Lounge — THE FIXER'S OFFICE · everything the vault owes you
- **8000** added: « The Recruiter — p137/rc/gems, p137/rc/hires
- **8001** added: Cecil 192 coins / Cecil IN YOUR PACK / Cecil SIGNED — p137/rc/main
- **8002** added: Emma 192 coins / Emma IN YOUR PACK / Emma SIGNED — p137/rc/main
- **8003** added: Celi 224 coins / Celi IN YOUR PACK / Celi SIGNED — p137/rc/main
- **8004** added: Zib 192 coins / Zib IN YOUR PACK / Zib SIGNED — p137/rc/main
- **8005** added: KillerWatt 320 coins / KillerWatt IN YOUR PACK / KillerWatt SIGNED — p137/rc/main
- **8006** added: Leo 208 coins / Leo IN YOUR PACK / Leo SIGNED — p137/rc/main
- **8007** added: Democratus 224 coins / Democratus IN YOUR PACK / Democratus SIGNED — p137/rc/main
- **8008** added: Skiff Escort 128 coins / Skiff Escort IN YOUR PACK / Skiff Escort SIGNED — p137/rc/main
- **8009** added: Apophiss 352 coins / Apophiss IN YOUR PACK / Apophiss SIGNED — p137/rc/main
- **8010** added: Tullius 336 coins / Tullius IN YOUR PACK / Tullius SIGNED — p137/rc/main
- **8011** added: The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main
- **8012** added: Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main
- **8040** added: Hirelings › — p137/rc/main
- **8041** added: Knuckles 48 coins / Knuckles FILED / Knuckles IN YOUR PACK — p137/rc/hires
- **8042** added: Doc Whiskers 64 coins / Doc Whiskers FILED / Doc Whiskers IN YOUR PACK — p137/rc/hires
- **8043** added: Fingers 48 coins / Fingers FILED / Fingers IN YOUR PACK — p137/rc/hires
- **8044** added: Tick-Tock 64 coins / Tick-Tock FILED / Tick-Tock IN YOUR PACK — p137/rc/hires
- **8045** added: Boomer 64 coins / Boomer FILED / Boomer IN YOUR PACK — p137/rc/hires
- **8050** added: Vault gems › — p137/rc/main
- **8051** added: Fire Gem 96 coins — p137/rc/gems
- **8052** added: Water Gem 96 coins — p137/rc/gems
- **8053** added: Poison Gem 96 coins — p137/rc/gems
- **8054** added: Earth Gem 96 coins — p137/rc/gems
- **8055** added: Electric Gem 96 coins — p137/rc/gems
- **8056** added: Rock Gem 96 coins — p137/rc/gems
- **8057** added: Air Gem 96 coins — p137/rc/gems
- **8058** added: Grass Gem 96 coins — p137/rc/gems
- **8059** added: Ice Gem 96 coins — p137/rc/gems
- **8100** added: Apophiss — THE TAILOR · outfits for your followers
- **8101** added: Tullius — THE TAILOR · outfits for your followers
- **8102** added: The Frog — THE TAILOR · outfits for your followers
- **8103** added: Donado — THE TAILOR · outfits for your followers
- **8104** added: Pearlman — THE TAILOR · outfits for your followers
- **8105** added: Wilfrey — THE TAILOR · outfits for your followers
- **8106** added: Auras (rare) — THE TAILOR · outfits for your followers
- **8110** added: Admiral's Blue $(r_40) — TULLIUS · the Tailor
- **8111** added: Corsair Crimson $(r_41) — TULLIUS · the Tailor
- **8112** added: Bleached Bone $(r_42) — TULLIUS · the Tailor
- **8113** added: Gilded Captain $(r_43) — TULLIUS · the Tailor
- **8114** added: Bluejay $(r_44) — THE FROG · the Tailor
- **8115** added: Ember Toad $(r_45) — THE FROG · the Tailor
- **8116** added: Old Bog $(r_46) — THE FROG · the Tailor
- **8117** added: Golden Prince $(r_47) — THE FROG · the Tailor
- **8118** added: Chocolate $(r_48) — DONADO · the Tailor
- **8119** added: Midnight $(r_49) — DONADO · the Tailor
- **8120** added: Snowdrift $(r_50) — DONADO · the Tailor
- **8121** added: Starlit $(r_51) — DONADO · the Tailor
- **8122** added: Ruby $(r_52) — PEARLMAN · the Tailor
- **8123** added: Emerald $(r_53) — PEARLMAN · the Tailor
- **8124** added: Amethyst $(r_54) — PEARLMAN · the Tailor
- **8125** added: Gilded $(r_55) — PEARLMAN · the Tailor
- **8126** added: Crimson Cross $(r_56) — WILFREY · the Tailor
- **8127** added: Azure Chevron $(r_57) — WILFREY · the Tailor
- **8128** added: Verdant Bend $(r_58) — WILFREY · the Tailor
- **8129** added: Gilded Sun $(r_59) — WILFREY · the Tailor
- **8150** added: Blossom Halo (Emma) $(r_a0) — AURAS · the Tailor
- **8151** added: Moonfrost Veil (Celi) $(r_a1) — AURAS · the Tailor
- **8152** added: Starfield Static (Zib) $(r_a2) — AURAS · the Tailor
- **8153** added: Arcane Corona (Cecil) $(r_a3) — AURAS · the Tailor
- **8154** added: Storm Crown (KillerWatt) $(r_a4) — AURAS · the Tailor
- **8155** added: Tidal Aegis (Leo) $(r_a5) — AURAS · the Tailor
- **8156** added: Reaper's Shroud (Democratus) $(r_a6) — AURAS · the Tailor
- **8157** added: Black-Flame Mantle (Apophiss) $(r_a7) — AURAS · the Tailor
- **8158** added: Drowned Gale (Tullius) $(r_a8) — AURAS · the Tailor
- **8159** added: Bog-Light Ring (the Frog) $(r_a9) — AURAS · the Tailor
- **8160** added: Tractor Beam (Donado) $(r_a10) — AURAS · the Tailor
- **8161** added: Golden Gleam (Pearlman) $(r_a11) — AURAS · the Tailor
- **8162** added: Lordly Radiance (Wilfrey) $(r_a12) — AURAS · the Tailor
- **8280** added: Apophiss's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **8281** added: Tullius's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **8282** added: The Frog's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **8283** added: Donado's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **8284** added: Pearlman's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **8285** added: Wilfrey's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger
- **8302** added: Wardrobe — Pearlman's Business Card
- **8604** added: Wardrobe — The Serpent's Oath
- **8624** added: Wardrobe — Tullius's Frozen Doubloon
- **8641** added: Sit / follow — Signet of the Frog Knight
- **8642** added: Hand back my gear — Signet of the Frog Knight
- **8643** added: Wardrobe — Signet of the Frog Knight
- **8648** added: Call for the Frog — Signet of the Frog Knight
- **8649** added: Send him home — Signet of the Frog Knight
- **8651** added: Sit / follow — Donado's Collar Tag
- **8652** added: Hand back my gear — Donado's Collar Tag
- **8653** added: Wardrobe — Donado's Collar Tag
- **8658** added: Call for Donado — Donado's Collar Tag
- **8659** added: Send him home — Donado's Collar Tag
- **9000** added: $(r_home) / « Outfits & buffs — Apophiss · wardrobe
- **9002** added: His own scales $(r_apo0) — Apophiss · wardrobe
- **9003** added: Obsidian Coil $(r_apo1) — Apophiss · wardrobe
- **9004** added: Blood Wyrm $(r_apo2) — Apophiss · wardrobe
- **9005** added: Frost Serpent $(r_apo3) — Apophiss · wardrobe
- **9006** added: Gilded Coil $(r_apo4) — Apophiss · wardrobe
- **9019** added: Black-Flame Mantle $(r_aura) — Apophiss · wardrobe
- **9020** added: $(r_home) / « Outfits & buffs — Tullius · wardrobe
- **9022** added: His old coat $(r_tul0) — Tullius · wardrobe
- **9023** added: Admiral's Blue $(r_tul1) — Tullius · wardrobe
- **9024** added: Corsair Crimson $(r_tul2) — Tullius · wardrobe
- **9025** added: Bleached Bone $(r_tul3) — Tullius · wardrobe
- **9026** added: Gilded Captain $(r_tul4) — Tullius · wardrobe
- **9039** added: Drowned Gale $(r_aura) — Tullius · wardrobe
- **9040** added: $(r_home) / « Outfits & buffs — the Frog with Mustache · wardrobe
- **9042** added: His own skin $(r_frog0) — the Frog with Mustache · wardrobe
- **9043** added: Bluejay $(r_frog1) — the Frog with Mustache · wardrobe
- **9044** added: Ember Toad $(r_frog2) — the Frog with Mustache · wardrobe
- **9045** added: Old Bog $(r_frog3) — the Frog with Mustache · wardrobe
- **9046** added: Golden Prince $(r_frog4) — the Frog with Mustache · wardrobe
- **9059** added: Bog-Light Ring $(r_aura) — the Frog with Mustache · wardrobe
- **9060** added: $(r_home) / « Outfits & buffs — Donado · wardrobe
- **9062** added: His own coat $(r_don0) — Donado · wardrobe
- **9063** added: Chocolate $(r_don1) — Donado · wardrobe
- **9064** added: Midnight $(r_don2) — Donado · wardrobe
- **9065** added: Snowdrift $(r_don3) — Donado · wardrobe
- **9066** added: Starlit $(r_don4) — Donado · wardrobe
- **9079** added: Tractor Beam $(r_aura) — Donado · wardrobe
- **9080** added: $(r_home) / « Outfits & buffs — Pearlman · wardrobe
- **9082** added: The blue bow tie $(r_pearl0) — Pearlman · wardrobe
- **9083** added: Ruby $(r_pearl1) — Pearlman · wardrobe
- **9084** added: Emerald $(r_pearl2) — Pearlman · wardrobe
- **9085** added: Amethyst $(r_pearl3) — Pearlman · wardrobe
- **9086** added: Gilded $(r_pearl4) — Pearlman · wardrobe
- **9099** added: Golden Gleam $(r_aura) — Pearlman · wardrobe
- **9100** added: $(r_home) / « Outfits & buffs — Wilfrey · wardrobe
- **9102** added: No shield $(r_wil0) — Wilfrey · wardrobe
- **9103** added: Crimson Cross $(r_wil1) — Wilfrey · wardrobe
- **9104** added: Azure Chevron $(r_wil2) — Wilfrey · wardrobe
- **9105** added: Verdant Bend $(r_wil3) — Wilfrey · wardrobe
- **9106** added: Gilded Sun $(r_wil4) — Wilfrey · wardrobe
- **9119** added: Lordly Radiance $(r_aura) — Wilfrey · wardrobe
- **9839** added: Blossom Halo $(r_aura) — Emma · wardrobe
- **9859** added: Moonfrost Veil $(r_aura) — Celi · wardrobe
- **9879** added: Starfield Static $(r_aura) — Zib · wardrobe
- **9899** added: Arcane Corona $(r_aura) — Cecil · wardrobe
- **9919** added: Storm Crown $(r_aura) — KillerWatt · wardrobe
- **9939** added: Tidal Aegis $(r_aura) — Leo · wardrobe
- **9959** added: Reaper's Shroud $(r_aura) — Democratus · wardrobe

### v2.77c
- no button changes

### v2.77b
- no button changes

### v2.77
- **7908** added: Apophiss — p103/crew/row_8
- **7909** added: Tullius — p103/crew/row_9
- **7920** changed: The Frog — p103/crew/row_8 → The Frog — p103/crew/row_10
- **7921** changed: Donado — p103/crew/row_9 → Donado — p103/crew/row_11
- **8601** added: Sit / follow — The Serpent's Oath
- **8602** added: Ride him — The Serpent's Oath
- **8603** added: Take off the saddle — The Serpent's Oath
- **8608** added: Call for Apophiss — The Serpent's Oath
- **8609** added: Send him home — The Serpent's Oath
- **8621** added: Sit / follow — Tullius's Frozen Doubloon
- **8628** added: Call for Tullius — Tullius's Frozen Doubloon
- **8629** added: Send him home — Tullius's Frozen Doubloon

### v2.76c
- **1** removed (was: Keep at it — Skip this puzzle?)
- **2** added: Keep at it — Skip this puzzle?

### v2.76b
- **7307** changed: Stay ethereal: on / off — Emma's Ribbon · the Wraithfire Heart → Wraithfire Form: on / off — Emma's Ribbon · the Wraithfire Heart
- **7310** added: Fly with me — Emma's Ribbon · the Wraithfire Heart
- **7311** added: Style: Guardian — Emma's Ribbon · the Wraithfire Heart
- **7312** added: Style: Huntress — Emma's Ribbon · the Wraithfire Heart
- **7313** added: Style: Tempest — Emma's Ribbon · the Wraithfire Heart

### v2.76
- legend started: 351 codes, 2 built at run time

<!-- legend-data {"base": {"1020": "Sealed Explorer's Map 2 Tokens — The Fence - Back Room", "1021": "2 Ominous Trial Keys 2 Medallions — The Fence - Back Room", "1022": "Smuggler's Jar 4 Medallions — The Fence - Back Room", "1040": "Fair Weather Bell 4 Tokens — Old Barnaby - Back Room", "1041": "2 Totems of Undying 2 Medallions — Old Barnaby - Back Room", "1042": "Spawner Crowbar 5 Medallions — Old Barnaby - Back Room", "1060": "Rat Gang Portrait 2 Tokens — Madame Velour - Back Room", "1061": "Donado Trophy 2 Medallions — Madame Velour - Back Room", "1062": "Brass Wing Scroll 1 Trophy — Madame Velour - Back Room", "1080": "16 Spectral Arrows 2 Tokens — Vinny 'Two-Blades' - Back Room", "1081": "Netherite Upgrade Template 2 Medallions — Vinny 'Two-Blades' - Back Room", "1082": "Showstopper Charm 1 Trophy — Vinny 'Two-Blades' - Back Room", "1100": "Lodestone Locket 5 Tokens — Sgt. Steelwhisker - Back Room", "1101": "3 Wither Skeleton Skulls 2 Medallions — Sgt. Steelwhisker - Back Room", "1102": "Market Crest Scroll 1 Trophy — Sgt. Steelwhisker - Back Room", "1120": "A Whole Cake 1 Token — Chef Fromage - Back Room", "1121": "Enchanted Golden Apple 4 Medallions — Chef Fromage - Back Room", "1122": "3 Enchanted Golden Apples 1 Trophy — Chef Fromage - Back Room", "1140": "16 Bottles o' Enchanting 2 Tokens — Prof. Whiskerton - Back Room", "1141": "Book of Mending 2 Medallions — Prof. Whiskerton - Back Room", "1142": "Auroral Crown 1 Trophy — Prof. Whiskerton - Back Room", "1160": "Jackpot Scratch Card 2 Lucky Tokens — Lucky Whiskers - Back Room", "1161": "Heartstone 9 Lucky Tokens — Lucky Whiskers - Back Room", "1162": "Bloomwalker Boots 1 Trophy — Lucky Whiskers - Back Room", "1180": "Buried Treasure Map 2 Tokens — Capt. Cheddarbeard - Back Room", "1181": "Heart of the Sea 2 Medallions — Capt. Cheddarbeard - Back Room", "1182": "Rat Familiar 1 Trophy — Capt. Cheddarbeard - Back Room", "1200": "Ominous Bottle 4 Blood Moon Crystals — The Bloodbroker - Back Room", "1201": "Nether Star 14 Blood Moon Crystals — The Bloodbroker - Back Room", "1202": "3 Heartstones 1 Trophy — The Bloodbroker - Back Room", "2": "Keep at it — Skip this puzzle?, The Fixer's mercy", "2001": "Buy a one-night pass 1 Medallion — The Dark Auction", "2110": "32 Coal → 1 Token $(q0)/5 — DENNIS'S ASSAY OFFICE", "2111": "32 Raw Copper → 1 Token $(q1)/5 — DENNIS'S ASSAY OFFICE", "2112": "24 Raw Iron → 1 Token $(q2)/5 — DENNIS'S ASSAY OFFICE", "2113": "16 Raw Gold → 1 Token $(q3)/4 — DENNIS'S ASSAY OFFICE", "2114": "48 Redstone Dust → 1 Token $(q4)/4 — DENNIS'S ASSAY OFFICE", "2115": "32 Lapis Lazuli → 1 Token $(q5)/4 — DENNIS'S ASSAY OFFICE", "2116": "32 Nether Quartz → 1 Token $(q6)/4 — DENNIS'S ASSAY OFFICE", "2117": "32 Amethyst Shards → 1 Token $(q7)/3 — DENNIS'S ASSAY OFFICE", "2118": "Diamond → 2 Tokens $(q8)/8 — DENNIS'S ASSAY OFFICE", "2119": "2 Ancient Debris → 1 Token $(q9)/4 — DENNIS'S ASSAY OFFICE", "2140": "Buy the Ore Magnet 16 Tokens — DENNIS'S ASSAY OFFICE", "2151": "« Common lots — PISTACHIO'S PANTRY · rare parts", "2152": "Rare parts » — PISTACHIO'S PANTRY", "2160": "32 Rotten Flesh → 1 Token $(q0)/5 — PISTACHIO'S PANTRY", "2161": "32 Bones → 1 Token $(q1)/5 — PISTACHIO'S PANTRY", "2162": "32 String → 1 Token $(q2)/5 — PISTACHIO'S PANTRY", "2163": "16 Spider Eyes → 1 Token $(q3)/4 — PISTACHIO'S PANTRY", "2164": "24 Gunpowder → 1 Token $(q4)/4 — PISTACHIO'S PANTRY", "2165": "16 Slimeballs → 1 Token $(q5)/4 — PISTACHIO'S PANTRY", "2166": "16 Leather → 1 Token $(q6)/4 — PISTACHIO'S PANTRY", "2167": "32 Feathers → 1 Token $(q7)/4 — PISTACHIO'S PANTRY", "2168": "24 Ink Sacs → 1 Token $(q8)/3 — PISTACHIO'S PANTRY", "2169": "8 Ender Pearls → 1 Token $(q9)/3 — PISTACHIO'S PANTRY", "2170": "8 Blaze Rods → 1 Token $(q10)/3 — PISTACHIO'S PANTRY", "2171": "12 Magma Cream → 1 Token $(q11)/3 — PISTACHIO'S PANTRY", "2172": "8 Phantom Membranes → 1 Token $(q12)/3 — PISTACHIO'S PANTRY", "2173": "24 Prismarine Shards → 1 Token $(q13)/3 — PISTACHIO'S PANTRY", "2174": "8 Breeze Rods → 1 Token $(q14)/3 — PISTACHIO'S PANTRY", "2175": "Wither Skeleton Skull → 5 Tokens $(q15)/3 — PISTACHIO'S PANTRY · rare parts", "2176": "Zombie Head → 3 Tokens $(q16)/2 — PISTACHIO'S PANTRY · rare parts", "2177": "Skeleton Skull → 3 Tokens $(q17)/2 — PISTACHIO'S PANTRY · rare parts", "2178": "Creeper Head → 3 Tokens $(q18)/2 — PISTACHIO'S PANTRY · rare parts", "2179": "Shulker Shell → 1 Token $(q19)/2 — PISTACHIO'S PANTRY · rare parts", "2180": "2 Rabbit's Feet → 1 Token $(q20)/2 — PISTACHIO'S PANTRY · rare parts", "2181": "2 Ghast Tears → 1 Token $(q21)/3 — PISTACHIO'S PANTRY · rare parts", "2190": "Buy the Spirit Jar 16 Tokens — PISTACHIO'S PANTRY", "2201": "Sit / follow — Dennis's Horn", "2202": "Wardrobe — Dennis's Horn", "2204": "Dennis's ways — Dennis's Horn", "2205": "« Back — DENNIS'S WAYS", "2208": "Call for Dennis — Dennis's Horn", "2209": "Send him home — Dennis's Horn", "2221": "Sit / follow — Pistachio's Little Cloche", "2222": "Wardrobe — Pistachio's Little Cloche", "2224": "Pistachio's ways — Pistachio's Little Cloche", "2225": "« Back — PISTACHIO'S WAYS", "2228": "Call for Pistachio — Pistachio's Little Cloche", "2229": "Send him home — Pistachio's Little Cloche", "2240": "$(r_home) / « Outfits & buffs — Dennis · wardrobe", "2242": "His old black leather $(r_dennis0) — Dennis · wardrobe", "2243": "Road Brown $(r_dennis1) — Dennis · wardrobe", "2244": "Biker Red $(r_dennis2) — Dennis · wardrobe", "2245": "Forest Leather $(r_dennis3) — Dennis · wardrobe", "2246": "Gilded Jacket $(r_dennis4) — Dennis · wardrobe", "2247": "Diamond Jacket $(r_dennis5) — Dennis · wardrobe", "2248": "Netherite Jacket $(r_dennis6) — Dennis · wardrobe", "2258": "Pixel costume $(r_px) — Dennis · wardrobe", "2259": "Gold Rush Glimmer $(r_aura) — Dennis · wardrobe", "2260": "$(r_home) / « Outfits & buffs — Pistachio · wardrobe", "2262": "His charcoal tails $(r_pistachio0) — Pistachio · wardrobe", "2263": "Midnight Tails $(r_pistachio1) — Pistachio · wardrobe", "2264": "Claret Tails $(r_pistachio2) — Pistachio · wardrobe", "2265": "Ivory Tails $(r_pistachio3) — Pistachio · wardrobe", "2266": "Gilded Tails $(r_pistachio4) — Pistachio · wardrobe", "2267": "Diamond Tails $(r_pistachio5) — Pistachio · wardrobe", "2268": "Netherite Tails $(r_pistachio6) — Pistachio · wardrobe", "2278": "Pixel costume $(r_px) — Pistachio · wardrobe", "2279": "Ectoplasmic Mist $(r_aura) — Pistachio · wardrobe", "2281": "Sit / follow — Omega's Monocle", "2282": "Wardrobe — Omega's Monocle", "2284": "King Omega's ways — Omega's Monocle", "2285": "« Back — KING OMEGA'S WAYS", "2288": "Call for Omega — Omega's Monocle", "2289": "Send him home — Omega's Monocle", "2300": "$(r_home) / « Outfits & buffs — King Omega · wardrobe", "2302": "His own grey ghost $(r_omega0) — King Omega · wardrobe", "2303": "Spectral Blue $(r_omega1) — King Omega · wardrobe", "2304": "Blood Moon $(r_omega2) — King Omega · wardrobe", "2305": "Verdant Wraith $(r_omega3) — King Omega · wardrobe", "2306": "Gilded King $(r_omega4) — King Omega · wardrobe", "2307": "Diamond King $(r_omega5) — King Omega · wardrobe", "2308": "Netherite King $(r_omega6) — King Omega · wardrobe", "2318": "Pixel costume $(r_px) — King Omega · wardrobe", "2319": "Court of Souls $(r_aura) — King Omega · wardrobe", "2321": "The Peerage — KING OMEGA", "2322": "The Ghost Garrison — KING OMEGA", "2323": "Offer a gift — KING OMEGA", "2324": "The Chronicle — KING OMEGA", "2325": "My title on / off — KING OMEGA", "2326": "Re-challenge the King — KING OMEGA", "2329": "« Back — THE GHOST GARRISON, THE PEERAGE, p169/court/chron", "2331": "Tithe 4 Tokens +10 — THE PEERAGE", "2332": "Offer your Court's souls — THE PEERAGE", "2341": "Buy a Soul Brazier 8 Tokens — THE GHOST GARRISON", "2350": "I. Two Eggs in the Sun — p169/court/chron", "2351": "II. The Monocle — p169/court/chron", "2352": "III. The Feast of Crowns — p169/court/chron", "2353": "IV. The Library of Small Things — p169/court/chron", "2354": "V. The Light to Lead Them — p169/court/chron", "2355": "VI. The War of Brothers — p169/court/chron", "2356": "VII. The Last Night — p169/court/chron", "2357": "VIII. The Long Quiet — p169/court/chron", "2358": "IX. The Butler and the Boy — p169/court/chron", "2359": "X. What the Dead King Wants — p169/court/chron", "2361": "Call him over — Wilfrey's Locket", "2362": "Send him home — Wilfrey's Locket", "2363": "Wardrobe — Wilfrey's Locket", "2364": "Call Wilfrey — Wilfrey's Locket", "2370": "Back after a faint $(r_ar) — Cecil · wardrobe", "2371": "Back after a faint $(r_ar) — Emma · wardrobe", "2372": "Back after a faint $(r_ar) — Celi · wardrobe", "2373": "Back after a faint $(r_ar) — Zib · wardrobe", "2374": "Back after a faint $(r_ar) — KillerWatt · wardrobe", "2375": "Back after a faint $(r_ar) — Leo · wardrobe", "2376": "Back after a faint $(r_ar) — Democratus · wardrobe", "2377": "Back after a faint $(r_ar) — Apophiss · wardrobe", "2378": "Back after a faint $(r_ar) — Tullius · wardrobe", "2379": "Back after a faint $(r_ar) — the Frog with Mustache · wardrobe", "2380": "Back after a faint $(r_ar) — Donado · wardrobe", "2381": "Back after a faint $(r_ar) — Wilfrey · wardrobe", "2382": "Back after a faint $(r_ar) — Fishy · wardrobe", "2383": "Back after a faint $(r_ar) — Dennis · wardrobe", "2384": "Back after a faint $(r_ar) — Pistachio · wardrobe", "2385": "Back after a faint $(r_ar) — King Omega · wardrobe", "2386": "Back after a faint $(r_ar) — Ashur · wardrobe", "2387": "Back after a faint $(r_ar) — the Chef · wardrobe", "2388": "Back after a faint $(r_ar) — the Neighbor · wardrobe", "2389": "Back after a faint $(r_ar) — Queen Ava · wardrobe", "2390": "Back after a faint $(r_ar) — Queen Pearl · wardrobe", "2391": "Back after a faint $(r_ar) — Bloo · wardrobe", "2392": "Back after a faint $(r_ar) — The Stalker · wardrobe", "2393": "Back after a faint $(r_ar) — The Arachno-Lantern · wardrobe", "2394": "Back after a faint $(r_ar) — Bender · wardrobe", "2395": "Back after a faint $(r_ar) — Bones · wardrobe", "2396": "Back after a faint $(r_ar) — Mr. Capshun · wardrobe", "2397": "Back after a faint $(r_ar) — 8-Bit Cecil · wardrobe", "2398": "Back after a faint $(r_ar) — 8-Bit Leo · wardrobe", "2399": "Back after a faint $(r_ar) — 8-Bit Emma · wardrobe", "2400": "Back after a faint $(r_ar) — The Sky Buddies · wardrobe", "2401": "Old Barnaby — WHO'S WHERE · the rat town", "2402": "Prof. Whiskerton — WHO'S WHERE · the rat town", "2403": "Madame Velour — WHO'S WHERE · the rat town", "2404": "The Fence — WHO'S WHERE · the rat town", "2405": "Dark Auction gate — WHO'S WHERE · the rat town", "2406": "Gilded Gutter gate — WHO'S WHERE · the rat town", "2407": "Scrap Bin — WHO'S WHERE · the rat town", "2408": "Bounty Board — WHO'S WHERE · the rat town", "2409": "Mike's pond — WHO'S WHERE · the rat town", "2410": "Vinny 'Two-Blades' — WHO'S WHERE · the rat town", "2411": "Steelwhisker — WHO'S WHERE · the rat town", "2412": "Fishy's Cabinet — WHO'S WHERE · the rat town", "2413": "Chef Fromage — WHO'S WHERE · the rat town", "2414": "Cecil — WHO'S WHERE · the rat town", "2415": "The Bloodbroker — WHO'S WHERE · the rat town", "2416": "Lucky Whiskers — WHO'S WHERE · the rat town", "2417": "The dock house — WHO'S WHERE · the rat town", "2418": "Dennis — WHO'S WHERE · the rat town", "2419": "Pistachio — WHO'S WHERE · the rat town", "2420": "Newcomers' Book — WHO'S WHERE · the rat town", "2421": "The way out — WHO'S WHERE · the rat town", "2441": "Sit / follow — Ashur's Cinder", "2442": "Wardrobe — Ashur's Cinder", "2444": "Ashur's ways — Ashur's Cinder", "2445": "« Back — ASHUR'S WAYS", "2448": "Call for Ashur — Ashur's Cinder", "2449": "Send her home — Ashur's Cinder", "2460": "$(r_home) / « Outfits & buffs — Ashur · wardrobe", "2462": "Her own magma $(r_ashur0) — Ashur · wardrobe", "2463": "Blue Flame $(r_ashur1) — Ashur · wardrobe", "2464": "Verdant Ember $(r_ashur2) — Ashur · wardrobe", "2465": "Obsidian Rose $(r_ashur3) — Ashur · wardrobe", "2466": "Gilded Magma $(r_ashur4) — Ashur · wardrobe", "2467": "Diamond Magma $(r_ashur5) — Ashur · wardrobe", "2468": "Netherite Magma $(r_ashur6) — Ashur · wardrobe", "2478": "Pixel costume $(r_px) — Ashur · wardrobe", "2479": "Ashfall Crown $(r_aura) — Ashur · wardrobe", "2501": "Sit / follow — The Golden Ladle", "2502": "Wardrobe — The Golden Ladle", "2504": "The Chef's ways — The Golden Ladle", "2505": "« Back — THE CHEF'S WAYS", "2508": "Call for The Chef — The Golden Ladle", "2509": "Send him home — The Golden Ladle", "2520": "$(r_home) / « Outfits & buffs — the Chef · wardrobe", "2522": "His spotless whites $(r_chef0) — the Chef · wardrobe", "2523": "Midnight Brigade $(r_chef1) — the Chef · wardrobe", "2524": "Bistro Blue $(r_chef2) — the Chef · wardrobe", "2525": "Sommelier Wine $(r_chef3) — the Chef · wardrobe", "2526": "Gilded Whites $(r_chef4) — the Chef · wardrobe", "2527": "Diamond Whites $(r_chef5) — the Chef · wardrobe", "2528": "Netherite Whites $(r_chef6) — the Chef · wardrobe", "2538": "Pixel costume $(r_px) — the Chef · wardrobe", "2539": "Kitchen Steam $(r_aura) — the Chef · wardrobe", "2541": "Sit / follow — The Neighbor's Baton", "2542": "Wardrobe — The Neighbor's Baton", "2544": "The Neighbor's ways — The Neighbor's Baton", "2545": "« Back — THE NEIGHBOR'S WAYS", "2548": "Call for The Neighbor — The Neighbor's Baton", "2549": "Send him home — The Neighbor's Baton", "2560": "$(r_home) / « Outfits & buffs — the Neighbor · wardrobe", "2562": "His sailor whites $(r_neighbor0) — the Neighbor · wardrobe", "2563": "Navy Bandmaster $(r_neighbor1) — the Neighbor · wardrobe", "2564": "Encore Crimson $(r_neighbor2) — the Neighbor · wardrobe", "2565": "Jazz Violet $(r_neighbor3) — the Neighbor · wardrobe", "2566": "Gilded Suit $(r_neighbor4) — the Neighbor · wardrobe", "2567": "Diamond Suit $(r_neighbor5) — the Neighbor · wardrobe", "2568": "Netherite Suit $(r_neighbor6) — the Neighbor · wardrobe", "2578": "Pixel costume $(r_px) — the Neighbor · wardrobe", "2579": "Grand Symphony $(r_aura) — the Neighbor · wardrobe", "2581": "Sit / follow — Queen Ava's Locket", "2582": "Wardrobe — Queen Ava's Locket", "2583": "Living / ghostly form — Queen Ava's Locket", "2584": "Queen Ava's ways — Queen Ava's Locket", "2585": "« Back — QUEEN AVA'S STORY, QUEEN AVA'S WAYS", "2586": "Her story — Queen Ava's Locket", "2588": "Call for Queen Ava — Queen Ava's Locket", "2589": "Send her home — Queen Ava's Locket", "2601": "Sit / follow — Queen Pearl's Pearls", "2602": "Wardrobe — Queen Pearl's Pearls", "2603": "Casual / regal outfit — Queen Pearl's Pearls", "2604": "Queen Pearl's ways — Queen Pearl's Pearls", "2605": "« Back — QUEEN PEARL'S STORY, QUEEN PEARL'S WAYS", "2606": "Her story — Queen Pearl's Pearls", "2608": "Call for Queen Pearl — Queen Pearl's Pearls", "2609": "Send her home — Queen Pearl's Pearls", "2621": "Sit / follow — Bloo's Claw", "2622": "Wardrobe — Bloo's Claw", "2624": "Bloo's ways — Bloo's Claw", "2625": "« Back — BLOO'S STORY, BLOO'S WAYS", "2626": "His story — Bloo's Claw", "2628": "Call for Bloo — Bloo's Claw", "2629": "Send him home — Bloo's Claw", "2640": "$(r_home) / « Outfits & buffs — Queen Ava · wardrobe", "2642": "Her royal blue $(r_ava0) — Queen Ava · wardrobe", "2643": "Coral Reef $(r_ava1) — Queen Ava · wardrobe", "2644": "Abyssal Violet $(r_ava2) — Queen Ava · wardrobe", "2645": "Kelp Forest $(r_ava3) — Queen Ava · wardrobe", "2646": "Gilded Gown $(r_ava4) — Queen Ava · wardrobe", "2647": "Diamond Gown $(r_ava5) — Queen Ava · wardrobe", "2648": "Netherite Gown $(r_ava6) — Queen Ava · wardrobe", "2658": "Pixel costume $(r_px) — Queen Ava · wardrobe", "2659": "Crown of the Deep $(r_aura) — Queen Ava · wardrobe", "2660": "$(r_home) / « Outfits & buffs — Queen Pearl · wardrobe", "2662": "Her own aqua $(r_pearlq0) — Queen Pearl · wardrobe", "2663": "Coral Pink $(r_pearlq1) — Queen Pearl · wardrobe", "2664": "Sunset Gold $(r_pearlq2) — Queen Pearl · wardrobe", "2665": "Starlit Navy $(r_pearlq3) — Queen Pearl · wardrobe", "2666": "Gilded Dress $(r_pearlq4) — Queen Pearl · wardrobe", "2667": "Diamond Dress $(r_pearlq5) — Queen Pearl · wardrobe", "2668": "Netherite Dress $(r_pearlq6) — Queen Pearl · wardrobe", "2678": "Pixel costume $(r_px) — Queen Pearl · wardrobe", "2679": "Pearlescent Tide $(r_aura) — Queen Pearl · wardrobe", "2680": "$(r_home) / « Outfits & buffs — Bloo · wardrobe", "2682": "His own wild blue $(r_bloo0) — Bloo · wardrobe", "2683": "Shadow Pelt $(r_bloo1) — Bloo · wardrobe", "2684": "Ember Mane $(r_bloo2) — Bloo · wardrobe", "2685": "Frost Coat $(r_bloo3) — Bloo · wardrobe", "2686": "Gilded Fur $(r_bloo4) — Bloo · wardrobe", "2687": "Diamond Fur $(r_bloo5) — Bloo · wardrobe", "2688": "Netherite Fur $(r_bloo6) — Bloo · wardrobe", "2698": "Pixel costume $(r_px) — Bloo · wardrobe", "2699": "Feral Moon $(r_aura) — Bloo · wardrobe", "2701": "Sit / follow — The Hollow Hook", "2702": "Wardrobe — The Hollow Hook", "2704": "The Stalker's ways — The Hollow Hook", "2705": "« Back — THE STALKER'S WAYS", "2708": "Call for The Stalker — The Hollow Hook", "2709": "Send it home — The Hollow Hook", "2720": "$(r_home) / « Outfits & buffs — The Stalker · wardrobe", "2722": "Its own sickly olive $(r_stalker0) — The Stalker · wardrobe", "2723": "Bone White $(r_stalker1) — The Stalker · wardrobe", "2724": "Ashen Grey $(r_stalker2) — The Stalker · wardrobe", "2725": "Blood Moon $(r_stalker3) — The Stalker · wardrobe", "2726": "Gilded Skin $(r_stalker4) — The Stalker · wardrobe", "2727": "Diamond Skin $(r_stalker5) — The Stalker · wardrobe", "2728": "Netherite Skin $(r_stalker6) — The Stalker · wardrobe", "2738": "Pixel costume $(r_px) — The Stalker · wardrobe", "2739": "The Long Night $(r_aura) — The Stalker · wardrobe", "2741": "Sit / follow — Kindled Gourd", "2742": "Wardrobe — Kindled Gourd", "2744": "The Arachno-Lantern's ways — Kindled Gourd", "2745": "« Back — THE ARACHNO-LANTERN'S WAYS", "2746": "Ride — Kindled Gourd", "2748": "Call for The Arachno-Lantern — Kindled Gourd", "2749": "Send it home — Kindled Gourd", "2760": "$(r_home) / « Outfits & buffs — The Arachno-Lantern · wardrobe", "2762": "Its own pumpkin orange $(r_lantern0) — The Arachno-Lantern · wardrobe", "2763": "Ghost Gourd $(r_lantern1) — The Arachno-Lantern · wardrobe", "2764": "Soulfire Rind $(r_lantern2) — The Arachno-Lantern · wardrobe", "2765": "Harvest Moon $(r_lantern3) — The Arachno-Lantern · wardrobe", "2766": "Gilded Rind $(r_lantern4) — The Arachno-Lantern · wardrobe", "2767": "Diamond Rind $(r_lantern5) — The Arachno-Lantern · wardrobe", "2768": "Netherite Rind $(r_lantern6) — The Arachno-Lantern · wardrobe", "2778": "Pixel costume $(r_px) — The Arachno-Lantern · wardrobe", "2779": "Hallowfire $(r_aura) — The Arachno-Lantern · wardrobe", "2781": "Sit / follow — Bender's Ball", "2782": "Wardrobe — Bender's Ball", "2784": "Bender's ways — Bender's Ball", "2785": "« Back — BENDER'S WAYS", "2786": "Dig! — Bender's Ball", "2787": "Sniff out treasure — Bender's Ball", "2788": "Call for Bender — Bender's Ball", "2789": "Send him home — Bender's Ball", "2800": "$(r_home) / « Outfits & buffs — Bender · wardrobe", "2802": "His own fawn $(r_bender0) — Bender · wardrobe", "2803": "Midnight Black $(r_bender1) — Bender · wardrobe", "2804": "Snow White $(r_bender2) — Bender · wardrobe", "2805": "Sable $(r_bender3) — Bender · wardrobe", "2806": "Gilded Coat $(r_bender4) — Bender · wardrobe", "2807": "Diamond Coat $(r_bender5) — Bender · wardrobe", "2808": "Netherite Coat $(r_bender6) — Bender · wardrobe", "2818": "Pixel costume $(r_px) — Bender · wardrobe", "2819": "Goodest Boy $(r_aura) — Bender · wardrobe", "2821": "Sit / follow — Bones's Whistle", "2822": "Wardrobe — Bones's Whistle", "2824": "Bones' ways — Bones's Whistle", "2825": "« Back — BONES' WAYS", "2826": "Ride — Bones's Whistle", "2828": "Call for Bones — Bones's Whistle", "2829": "Send him home — Bones's Whistle", "2840": "$(r_home) / « Outfits & buffs — Bones · wardrobe", "2842": "His own shark grey $(r_bones0) — Bones · wardrobe", "2843": "Great White $(r_bones1) — Bones · wardrobe", "2844": "Hammerhead Bronze $(r_bones2) — Bones · wardrobe", "2845": "Abyss Black $(r_bones3) — Bones · wardrobe", "2846": "Gilded Skin $(r_bones4) — Bones · wardrobe", "2847": "Diamond Skin $(r_bones5) — Bones · wardrobe", "2848": "Netherite Skin $(r_bones6) — Bones · wardrobe", "2858": "Pixel costume $(r_px) — Bones · wardrobe", "2859": "Abyssal Tide $(r_aura) — Bones · wardrobe", "2861": "Sit / follow — Mr. Capshun's Pencil", "2862": "Wardrobe — Mr. Capshun's Pencil", "2864": "Mr. Capshun's ways — Mr. Capshun's Pencil", "2865": "« Back — MR. CAPSHUN'S PALETTE, MR. CAPSHUN'S WAYS", "2866": "Palette — Mr. Capshun's Pencil", "2867": "The story so far — Mr. Capshun's Pencil", "2868": "Call for Mr. Capshun — Mr. Capshun's Pencil", "2869": "Send him home — Mr. Capshun's Pencil", "2870": "Red — MR. CAPSHUN'S PALETTE", "2871": "Orange — MR. CAPSHUN'S PALETTE", "2872": "Yellow — MR. CAPSHUN'S PALETTE", "2873": "Green — MR. CAPSHUN'S PALETTE", "2874": "Blue — MR. CAPSHUN'S PALETTE", "2875": "Purple — MR. CAPSHUN'S PALETTE", "2876": "Rainbow — MR. CAPSHUN'S PALETTE", "2880": "$(r_home) / « Outfits & buffs — Mr. Capshun · wardrobe", "2882": "Plain black ink $(r_capshun0) — Mr. Capshun · wardrobe", "2883": "Blue Ballpoint $(r_capshun1) — Mr. Capshun · wardrobe", "2884": "Red Pen $(r_capshun2) — Mr. Capshun · wardrobe", "2885": "Green Marker $(r_capshun3) — Mr. Capshun · wardrobe", "2886": "Gilded Ink $(r_capshun4) — Mr. Capshun · wardrobe", "2887": "Diamond Ink $(r_capshun5) — Mr. Capshun · wardrobe", "2888": "Netherite Ink $(r_capshun6) — Mr. Capshun · wardrobe", "2898": "Pixel costume $(r_px) — Mr. Capshun · wardrobe", "2899": "Rainbow Doodles $(r_aura) — Mr. Capshun · wardrobe", "2900": "$(r_home) / « Outfits & buffs — The Sky Buddies · wardrobe", "2902": "Snooze's old blue $(r_sky0) — The Sky Buddies · wardrobe", "2903": "Bubblegum Pink $(r_sky1) — The Sky Buddies · wardrobe", "2904": "Mint Dream $(r_sky2) — The Sky Buddies · wardrobe", "2905": "Lavender Night $(r_sky3) — The Sky Buddies · wardrobe", "2906": "Gilded Nightcap $(r_sky4) — The Sky Buddies · wardrobe", "2907": "Diamond Nightcap $(r_sky5) — The Sky Buddies · wardrobe", "2908": "Netherite Nightcap $(r_sky6) — The Sky Buddies · wardrobe", "2918": "Pixel costume $(r_px) — The Sky Buddies · wardrobe", "2919": "Starry Sky $(r_aura) — The Sky Buddies · wardrobe", "2941": "Sit / follow — The Sky Mobile", "2942": "Wardrobe — The Sky Mobile", "2943": "A bed on Nimbus — The Sky Mobile", "2944": "The Sky Buddies' ways — The Sky Mobile", "2945": "« Back — THE SKY BUDDIES' WAYS", "2946": "Today's forecast — The Sky Mobile", "2947": "Change the weather — The Sky Mobile", "2948": "Call for The Sky Buddies — The Sky Mobile", "2949": "Send them home — The Sky Mobile", "2950": "Clear skies — THE SKY, YOURS", "2951": "Rain — THE SKY, YOURS", "2952": "Thunderstorm — THE SKY, YOURS", "2953": "« Back — THE SKY, YOURS", "2960": "$(r_home) / « Outfits & buffs — 8-Bit Emma · wardrobe", "2962": "Sixteen colours $(r_pxemma0) — 8-Bit Emma · wardrobe", "2963": "Game Boy $(r_pxemma1) — 8-Bit Emma · wardrobe", "2964": "Virtual Boy $(r_pxemma2) — 8-Bit Emma · wardrobe", "2965": "Sepia Print $(r_pxemma3) — 8-Bit Emma · wardrobe", "2966": "Gilded Pixels $(r_pxemma4) — 8-Bit Emma · wardrobe", "2967": "Diamond Pixels $(r_pxemma5) — 8-Bit Emma · wardrobe", "2968": "Netherite Pixels $(r_pxemma6) — 8-Bit Emma · wardrobe", "2979": "Scanlines $(r_aura) — 8-Bit Emma · wardrobe", "2981": "Sit / follow — 8-Bit Emma's Cartridge", "2982": "Wardrobe — 8-Bit Emma's Cartridge", "2984": "8-Bit Emma's ways — 8-Bit Emma's Cartridge", "2985": "« Back — 8-BIT EMMA'S WAYS", "2988": "Call for 8-Bit Emma — 8-Bit Emma's Cartridge", "2989": "Send her home — 8-Bit Emma's Cartridge", "3000": "$(r_home) / « Outfits & buffs — 8-Bit Leo · wardrobe", "3002": "Sixteen colours $(r_pxleo0) — 8-Bit Leo · wardrobe", "3003": "Game Boy $(r_pxleo1) — 8-Bit Leo · wardrobe", "3004": "Virtual Boy $(r_pxleo2) — 8-Bit Leo · wardrobe", "3005": "Sepia Print $(r_pxleo3) — 8-Bit Leo · wardrobe", "3006": "Gilded Pixels $(r_pxleo4) — 8-Bit Leo · wardrobe", "3007": "Diamond Pixels $(r_pxleo5) — 8-Bit Leo · wardrobe", "3008": "Netherite Pixels $(r_pxleo6) — 8-Bit Leo · wardrobe", "3019": "Scanlines $(r_aura) — 8-Bit Leo · wardrobe", "3021": "Sit / follow — 8-Bit Leo's Cartridge", "3022": "Wardrobe — 8-Bit Leo's Cartridge", "3024": "8-Bit Leo's ways — 8-Bit Leo's Cartridge", "3025": "« Back — 8-BIT LEO'S WAYS", "3028": "Call for 8-Bit Leo — 8-Bit Leo's Cartridge", "3029": "Send him home — 8-Bit Leo's Cartridge", "3040": "$(r_home) / « Outfits & buffs — 8-Bit Cecil · wardrobe", "3042": "Sixteen colours $(r_pxcecil0) — 8-Bit Cecil · wardrobe", "3043": "Game Boy $(r_pxcecil1) — 8-Bit Cecil · wardrobe", "3044": "Virtual Boy $(r_pxcecil2) — 8-Bit Cecil · wardrobe", "3045": "Sepia Print $(r_pxcecil3) — 8-Bit Cecil · wardrobe", "3046": "Gilded Pixels $(r_pxcecil4) — 8-Bit Cecil · wardrobe", "3047": "Diamond Pixels $(r_pxcecil5) — 8-Bit Cecil · wardrobe", "3048": "Netherite Pixels $(r_pxcecil6) — 8-Bit Cecil · wardrobe", "3059": "Scanlines $(r_aura) — 8-Bit Cecil · wardrobe", "3061": "Sit / follow — 8-Bit Cecil's Cartridge", "3062": "Wardrobe — 8-Bit Cecil's Cartridge", "3064": "8-Bit Cecil's ways — 8-Bit Cecil's Cartridge", "3065": "« Back — 8-BIT CECIL'S WAYS", "3068": "Call for 8-Bit Cecil — 8-Bit Cecil's Cartridge", "3069": "Send him home — 8-Bit Cecil's Cartridge", "3100": "Open the bidding — The Dark Auction", "3101": "Bid +1 — The Dark Auction", "3102": "Bid +2 — The Dark Auction", "3105": "Bid +5 — The Dark Auction", "3110": "Bid +10 — The Dark Auction", "3202": "Tuning — VESPER'S STOCK BOOK · the Dread Broker", "3203": "Reforging — VESPER'S STOCK BOOK · the Dread Broker", "3204": "About the Dread — VESPER'S STOCK BOOK · the Dread Broker", "3205": "Reforge what I hold — Reforging · past the old maximum", "3209": "« The Ledger — About the Dread, Reforging · past the old maximum, Tuning · a tool, Tuning · a weapon, Tuning · an armour piece", "3220": "Attack Damage +0.75 (max 3) — Tuning · a weapon", "3221": "Swing Speed +0.1 (max 3) — Tuning · a weapon", "3222": "Reach +0.25 (max 2) — Tuning · a weapon", "3223": "Luck +1 (max 2) — Tuning · a weapon", "3224": "Unbind all tunings (every token back) — Tuning · a weapon", "3225": "Mining Speed +10% (max 3) — Tuning · a tool", "3226": "Mining Efficiency +3 (max 2) — Tuning · a tool", "3227": "Block Reach +0.5 (max 2) — Tuning · a tool", "3228": "Luck +1 (max 2) — Tuning · a tool", "3229": "Unbind all tunings (every token back) — Tuning · a tool", "3230": "Armor +1 (max 2) — Tuning · an armour piece", "3231": "Toughness +1 (max 2) — Tuning · an armour piece", "3232": "Max Health +1 (max 2) — Tuning · an armour piece", "3233": "Knockback Resistance +0.05 (max 2) — Tuning · an armour piece", "3234": "Speed (boots) +2% (max 2) — Tuning · an armour piece", "3235": "Unbind all tunings (every token back) — Tuning · an armour piece", "3301": "Lamplighters' Fund $(p0)/250$(s0) — Community Pots · The Rat Bank", "3302": "Harvest Guild $(p1)/300$(s1) — Community Pots · The Rat Bank", "3303": "Miners' Union $(p2)/400$(s2) — Community Pots · The Rat Bank", "3304": "Couriers' Guild $(p3)/400$(s3) — Community Pots · The Rat Bank", "3305": "Hearth Fund $(p4)/500$(s4) — Community Pots · The Rat Bank", "3306": "Bounty Office $(p5)/600$(s5) — Community Pots · The Rat Bank", "3309": "« Your account — Community Pots · The Rat Bank", "3310": "Give 10 Tokens — Lamplighters' Fund · Community Pots", "3311": "Give 10 Tokens — Harvest Guild · Community Pots", "3312": "Give 10 Tokens — Miners' Union · Community Pots", "3313": "Give 10 Tokens — Couriers' Guild · Community Pots", "3314": "Give 10 Tokens — Hearth Fund · Community Pots", "3315": "Give 10 Tokens — Bounty Office · Community Pots", "3320": "Give 50 Tokens — Lamplighters' Fund · Community Pots", "3321": "Give 50 Tokens — Harvest Guild · Community Pots", "3322": "Give 50 Tokens — Miners' Union · Community Pots", "3323": "Give 50 Tokens — Couriers' Guild · Community Pots", "3324": "Give 50 Tokens — Hearth Fund · Community Pots", "3325": "Give 50 Tokens — Bounty Office · Community Pots", "3330": "Switch it on / off — Lamplighters' Fund · Community Pots", "3331": "Switch it on / off — Harvest Guild · Community Pots", "3332": "Switch it on / off — Miners' Union · Community Pots", "3333": "Switch it on / off — Couriers' Guild · Community Pots", "3334": "Switch it on / off — Hearth Fund · Community Pots", "3335": "Switch it on / off — Bounty Office · Community Pots", "3340": "« The pots — Bounty Office · Community Pots, Couriers' Guild · Community Pots, Harvest Guild · Community Pots, Hearth Fund · Community Pots, Lamplighters' Fund · Community Pots, Miners' Union · Community Pots", "3351": "Keep up: off / Keep up: on — p179/w/open", "3352": "❖ Gallery — p179/w/open", "3353": "◈ View in 3D: #01-#08 — Follower Gallery", "3354": "◈ View in 3D: #09-#16 — Follower Gallery", "3355": "◈ View in 3D: #17-#24 — Follower Gallery", "3356": "◈ View in 3D: #25-#32 — Follower Gallery", "3359": "« Partner Wheel — Follower Gallery", "3360": "Call Emma / Send Emma home — p179/w/row0", "3361": "Call Celi / Send Celi home — p179/w/row1", "3362": "Call Zib / Send Zib home — p179/w/row2", "3363": "Call Cecil / Send Cecil home — p179/w/row3", "3364": "Call KillerWatt / Send KillerWatt home — p179/w/row4", "3365": "Call Leo / Send Leo home — p179/w/row5", "3366": "Call Democratus / Send Democratus home — p179/w/row6", "3367": "Call Apophiss / Send Apophiss home — p179/w/row7", "3368": "Call Tullius / Send Tullius home — p179/w/row8", "3369": "Call the Frog / Send the Frog home — p179/w/row9", "3370": "Call Donado / Send Donado home — p179/w/row10", "3371": "Call Pearlman / Send Pearlman home — p179/w/row11", "3372": "Call Wilfrey / Send Wilfrey home — p179/w/row12", "3373": "Call Fishy / Send Fishy home — p179/w/row13", "3374": "Call Dennis / Send Dennis home — p179/w/row14", "3375": "Call Pistachio / Send Pistachio home — p179/w/row15", "3376": "Call King Omega / Send King Omega home — p179/w/row16", "3377": "Call Ashur / Send Ashur home — p179/w/row17", "3378": "Call the Chef / Send the Chef home — p179/w/row18", "3379": "Call the Neighbor / Send the Neighbor home — p179/w/row19", "3380": "Call Queen Ava / Send Queen Ava home — p179/w/row20", "3381": "Call Queen Pearl / Send Queen Pearl home — p179/w/row21", "3382": "Call Bloo / Send Bloo home — p179/w/row22", "3383": "Call The Stalker / Send The Stalker home — p179/w/row23", "3384": "Call The Arachno-Lantern / Send The Arachno-Lantern home — p179/w/row24", "3385": "Call Bender / Send Bender home — p179/w/row25", "3386": "Call Bones / Send Bones home — p179/w/row26", "3387": "Call Mr. Capshun / Send Mr. Capshun home — p179/w/row27", "3388": "Call 8-Bit Cecil / Send 8-Bit Cecil home — p179/w/row28", "3389": "Call 8-Bit Leo / Send 8-Bit Leo home — p179/w/row29", "3390": "Take the item back — p179/w/row0", "3391": "Take the item back — p179/w/row1", "3392": "Take the item back — p179/w/row2", "3393": "Take the item back — p179/w/row3", "3394": "Take the item back — p179/w/row4", "3395": "Take the item back — p179/w/row5", "3396": "Take the item back — p179/w/row6", "3397": "Take the item back — p179/w/row7", "3398": "Take the item back — p179/w/row8", "3399": "Take the item back — p179/w/row9", "3400": "Take the item back — p179/w/row10", "3401": "Take the item back — p179/w/row11", "3402": "Take the item back — p179/w/row12", "3403": "Take the item back — p179/w/row13", "3404": "Take the item back — p179/w/row14", "3405": "Take the item back — p179/w/row15", "3406": "Take the item back — p179/w/row16", "3407": "Take the item back — p179/w/row17", "3408": "Take the item back — p179/w/row18", "3409": "Take the item back — p179/w/row19", "3410": "Take the item back — p179/w/row20", "3411": "Take the item back — p179/w/row21", "3412": "Take the item back — p179/w/row22", "3413": "Take the item back — p179/w/row23", "3414": "Take the item back — p179/w/row24", "3415": "Take the item back — p179/w/row25", "3416": "Take the item back — p179/w/row26", "3417": "Take the item back — p179/w/row27", "3418": "Take the item back — p179/w/row28", "3419": "Take the item back — p179/w/row29", "3420": "Launch your Skiff Escort / Send your Skiff Escort home — p184/wesc/row", "3421": "Take the escort back — p184/wesc/row", "3450": "⚙ Menu — p179/w/row0", "3451": "⚙ Menu — p179/w/row1", "3452": "⚙ Menu — p179/w/row2", "3453": "⚙ Menu — p179/w/row3", "3454": "⚙ Menu — p179/w/row4", "3455": "⚙ Menu — p179/w/row5", "3456": "⚙ Menu — p179/w/row6", "3457": "⚙ Menu — p179/w/row7", "3458": "⚙ Menu — p179/w/row8", "3459": "⚙ Menu — p179/w/row9", "3460": "⚙ Menu — p179/w/row10", "3461": "⚙ Menu — p179/w/row11", "3462": "⚙ Menu — p179/w/row12", "3463": "⚙ Menu — p179/w/row13", "3464": "⚙ Menu — p179/w/row14", "3465": "⚙ Menu — p179/w/row15", "3466": "⚙ Menu — p179/w/row16", "3467": "⚙ Menu — p179/w/row17", "3468": "⚙ Menu — p179/w/row18", "3469": "⚙ Menu — p179/w/row19", "3470": "⚙ Menu — p179/w/row20", "3471": "⚙ Menu — p179/w/row21", "3472": "⚙ Menu — p179/w/row22", "3473": "⚙ Menu — p179/w/row23", "3474": "⚙ Menu — p179/w/row24", "3475": "⚙ Menu — p179/w/row25", "3476": "⚙ Menu — p179/w/row26", "3477": "⚙ Menu — p179/w/row27", "3478": "⚙ Menu — p179/w/row28", "3479": "⚙ Menu — p179/w/row29", "3480": "Dynamic — Pearlman's Seasons", "3481": "Off - his own colours — Pearlman's Seasons", "3482": "Fall / Fall (locked) — Pearlman's Seasons", "3483": "Christmas / Christmas (locked) — Pearlman's Seasons", "3484": "Easter / Easter (locked) — Pearlman's Seasons", "3485": "Summer / Summer (locked) — Pearlman's Seasons", "3600": "Gilded Pixels $(r_182) — 8-BIT EMMA · the Tailor", "3601": "Diamond Pixels $(r_183) — 8-BIT EMMA · the Tailor", "3602": "Netherite Pixels $(r_184) — 8-BIT EMMA · the Tailor", "3603": "Game Boy $(r_185) — 8-BIT LEO · the Tailor", "3604": "Virtual Boy $(r_186) — 8-BIT LEO · the Tailor", "3605": "Sepia Print $(r_187) — 8-BIT LEO · the Tailor", "3606": "Gilded Pixels $(r_188) — 8-BIT LEO · the Tailor", "3607": "Diamond Pixels $(r_189) — 8-BIT LEO · the Tailor", "3608": "Netherite Pixels $(r_190) — 8-BIT LEO · the Tailor", "3609": "Game Boy $(r_191) — 8-BIT CECIL · the Tailor", "3610": "Virtual Boy $(r_192) — 8-BIT CECIL · the Tailor", "3611": "Sepia Print $(r_193) — 8-BIT CECIL · the Tailor", "3612": "Gilded Pixels $(r_194) — 8-BIT CECIL · the Tailor", "3613": "Diamond Pixels $(r_195) — 8-BIT CECIL · the Tailor", "3614": "Netherite Pixels $(r_196) — 8-BIT CECIL · the Tailor", "3615": "Blue Ballpoint $(r_197) — MR. CAPSHUN · the Tailor", "3616": "Red Pen $(r_198) — MR. CAPSHUN · the Tailor", "3617": "Green Marker $(r_199) — MR. CAPSHUN · the Tailor", "3618": "Gilded Ink $(r_200) — MR. CAPSHUN · the Tailor", "3619": "Diamond Ink $(r_201) — MR. CAPSHUN · the Tailor", "3620": "Netherite Ink $(r_202) — MR. CAPSHUN · the Tailor", "3700": "Call 8-Bit Emma / Send 8-Bit Emma home — p179/w/row30", "3701": "Call The Sky Buddies / Send The Sky Buddies home — p179/w/row31", "3740": "Take the item back — p179/w/row30", "3741": "Take the item back — p179/w/row31", "3780": "⚙ Menu — p179/w/row30", "3781": "⚙ Menu — p179/w/row31", "4010": "Deposit all Tokens ($(h)) — Tokens · The Rat Bank", "4011": "Take 1 — Tokens · The Rat Bank", "4012": "Take 10 — Tokens · The Rat Bank", "4013": "Take all ($(n)) — Tokens · The Rat Bank", "4014": "Deposit all Lucky Tokens ($(h)) — Lucky Tokens · The Rat Bank", "4015": "Take 1 — Lucky Tokens · The Rat Bank", "4016": "Take 10 — Lucky Tokens · The Rat Bank", "4017": "Take all ($(n)) — Lucky Tokens · The Rat Bank", "4018": "Deposit all Medallions ($(h)) — Medallions · The Rat Bank", "4019": "Take 1 — Medallions · The Rat Bank", "4020": "Take 10 — Medallions · The Rat Bank", "4021": "Take all ($(n)) — Medallions · The Rat Bank", "4022": "Deposit all Trophies ($(h)) — Trophies · The Rat Bank", "4023": "Take 1 — Trophies · The Rat Bank", "4024": "Take 10 — Trophies · The Rat Bank", "4025": "Take all ($(n)) — Trophies · The Rat Bank", "4026": "Deposit all Blood Crystals ($(h)) — Blood Crystals · The Rat Bank", "4027": "Take 1 — Blood Crystals · The Rat Bank", "4028": "Take 10 — Blood Crystals · The Rat Bank", "4029": "Take all ($(n)) — Blood Crystals · The Rat Bank", "4030": "Deposit all Ember Scales ($(h)) — Ember Scales · The Rat Bank", "4031": "Take 1 — Ember Scales · The Rat Bank", "4032": "Take 10 — Ember Scales · The Rat Bank", "4033": "Take all ($(n)) — Ember Scales · The Rat Bank", "4034": "Deposit all Void Shards ($(h)) — Void Shards · The Rat Bank", "4035": "Take 1 — Void Shards · The Rat Bank", "4036": "Take 10 — Void Shards · The Rat Bank", "4037": "Take all ($(n)) — Void Shards · The Rat Bank", "4038": "Deposit all Green Xenite ($(h)) — Green Xenite · The Rat Bank", "4039": "Take 1 — Green Xenite · The Rat Bank", "4040": "Take 10 — Green Xenite · The Rat Bank", "4041": "Take all ($(n)) — Green Xenite · The Rat Bank", "4042": "Deposit all Violet Xenite ($(h)) — Violet Xenite · The Rat Bank", "4043": "Take 1 — Violet Xenite · The Rat Bank", "4044": "Take 10 — Violet Xenite · The Rat Bank", "4045": "Take all ($(n)) — Violet Xenite · The Rat Bank", "4046": "Deposit all Cyan Xenite ($(h)) — Cyan Xenite · The Rat Bank", "4047": "Take 1 — Cyan Xenite · The Rat Bank", "4048": "Take 10 — Cyan Xenite · The Rat Bank", "4049": "Take all ($(n)) — Cyan Xenite · The Rat Bank", "4050": "Deposit all Red Xenite ($(h)) — Red Xenite · The Rat Bank", "4051": "Take 1 — Red Xenite · The Rat Bank", "4052": "Take 10 — Red Xenite · The Rat Bank", "4053": "Take all ($(n)) — Red Xenite · The Rat Bank", "4054": "Deposit all Dread Tokens ($(h)) — Dread Tokens · The Rat Bank", "4055": "Take 1 — Dread Tokens · The Rat Bank", "4056": "Take 10 — Dread Tokens · The Rat Bank", "4057": "Take all ($(n)) — Dread Tokens · The Rat Bank", "4060": "Tokens $(token) — The Rat Bank - your account", "4061": "Lucky Tokens $(lucky_token) — The Rat Bank - your account", "4062": "Medallions $(medallion) — The Rat Bank - your account", "4063": "Trophies $(trophy) — The Rat Bank - your account", "4064": "Blood Crystals $(blood_crystal) — The Rat Bank - your account", "4065": "Ember Scales $(ember_scale) — The Rat Bank - your account", "4066": "Void Shards $(void_shard) — The Rat Bank - your account", "4067": "Green Xenite $(xenite_green) — The Rat Bank - your account", "4068": "Violet Xenite $(xenite_violet) — The Rat Bank - your account", "4069": "Cyan Xenite $(xenite_cyan) — The Rat Bank - your account", "4070": "Red Xenite $(xenite_red) — The Rat Bank - your account", "4071": "Deposit everything — The Rat Bank - your account", "4072": "« Back to your account / « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Dread Tokens · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Savings · The Rat Bank, The Exchange · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank", "4073": "Savings account — The Rat Bank - your account", "4074": "Exchange — The Rat Bank - your account", "4075": "5 Tokens → 1 Medallion — The Exchange · The Rat Bank", "4076": "1 Medallion → 5 Tokens — The Exchange · The Rat Bank", "4077": "4 Medallions → 1 Trophy — The Exchange · The Rat Bank", "4078": "1 Trophy → 4 Medallions — The Exchange · The Rat Bank", "4079": "Auto-deposit: $(ac) — The Rat Bank - your account", "4080": "5 Trophies → 1 Dread Token — The Exchange · The Rat Bank", "4081": "1 Dread Token → 5 Trophies — The Exchange · The Rat Bank", "4085": "Community Pots — The Rat Bank - your account", "4090": "Dread Tokens $(dread_token) — The Rat Bank - your account", "4101": "$(r_l0) — QUEEN AVA'S HONOURS · the Tide Font", "4102": "$(r_l1) — QUEEN AVA'S HONOURS · the Tide Font", "4103": "$(r_l2) — QUEEN AVA'S HONOURS · the Tide Font", "4105": "The Tide's Haste +1 ($(src)) — QUEEN AVA'S HONOURS · the Tide Font", "4109": "« Her honours — QUEEN AVA'S HONOURS · $(r_nm)", "4111": "Honour +1 ($(hc)) — QUEEN AVA'S HONOURS · $(r_nm)", "4201": "$(r_0md) — THE CHAMPION'S RIBBON · your Champions beside you", "4202": "$(r_0rg) — THE CHAMPION'S RIBBON · your Champions beside you", "4203": "$(r_0au) — THE CHAMPION'S RIBBON · your Champions beside you", "4204": "$(r_1md) — THE CHAMPION'S RIBBON · your Champions beside you", "4205": "$(r_1rg) — THE CHAMPION'S RIBBON · your Champions beside you", "4206": "$(r_1au) — THE CHAMPION'S RIBBON · your Champions beside you", "4207": "$(r_2md) — THE CHAMPION'S RIBBON · your Champions beside you", "4208": "$(r_2rg) — THE CHAMPION'S RIBBON · your Champions beside you", "4209": "$(r_2au) — THE CHAMPION'S RIBBON · your Champions beside you", "5001": "$(n1) $(p1) Medallions — The Concierge", "5002": "$(n2) $(p2) Medallions — The Concierge", "5003": "$(n3) $(p3) Medallions — The Concierge", "5010": "Repair the item in my main hand 1 Medallion — The Concierge", "6001": "Go: $(t1) — Ring of Three Burrows", "6002": "Go: $(t2) — Ring of Three Burrows", "6003": "Go: $(t3) — Ring of Three Burrows", "6011": "Set burrow 1 here — Ring of Three Burrows", "6012": "Set burrow 2 here — Ring of Three Burrows", "6013": "Set burrow 3 here — Ring of Three Burrows", "7001": "Follow me — Rufus Gnaw, rat for hire", "7002": "Guard this spot — Rufus Gnaw, rat for hire", "7003": "Follow and scavenge — Rufus Gnaw, rat for hire", "7004": "Hand over the loot — Rufus Gnaw, rat for hire", "7005": "Pay a week 4 Tokens — Rufus Gnaw, rat for hire", "7006": "Call him to me — Rufus Gnaw, rat for hire", "7007": "Patch him up 1 Medallion — Rufus Gnaw, rat for hire", "7101": "Yes - start over — Key of New Beginnings", "7102": "No — Key of New Beginnings", "7201": "The Overworld — Dimension Shifter", "7202": "The Nether — Dimension Shifter", "7203": "The End — Dimension Shifter", "7301": "Speed — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7302": "Offense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7303": "Defense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7304": "Healing — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7305": "Mining — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7306": "Wardrobe — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7307": "Wraithfire Form: on / off — Emma's Ribbon · the Wraithfire Heart", "7308": "Take back the heart — Emma's Ribbon · the Wraithfire Heart", "7309": "Send her home — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7310": "Fly with me — Emma's Ribbon · the Wraithfire Heart", "7311": "Style: Guardian — Emma's Ribbon · the Wraithfire Heart", "7312": "Style: Huntress — Emma's Ribbon · the Wraithfire Heart", "7313": "Style: Tempest — Emma's Ribbon · the Wraithfire Heart", "7601": "Tier I The Copper Strongroom — Plan a Heist", "7602": "Tier II The Silver Vaults — Plan a Heist", "7603": "Tier III The Gold Reserve — Plan a Heist", "7604": "Tier IV The Diamond Deposit — Plan a Heist", "7605": "Tier V The Gutter King's Hoard — Plan a Heist", "7606": "THE ENDLESS VAULT rooms without end — Plan a Heist", "7607": "THE PIT an arena of waves — Plan a Heist", "7611": "3 TRIES +1 to +4 shares (by tier) - for the bold — How many tries?", "7612": "5 TRIES +0 to +2 shares (by tier) — How many tries?", "7613": "7 TRIES no bonus - for a first try — How many tries?", "7619": "ALARM: $(al) (click to switch) — How many tries?", "7711": "[Accept] — p73/tp/ask_bring, p73/tp/ask_go", "7712": "[Deny] — p73/tp/ask_bring, p73/tp/ask_go", "7720": "Back to the Overworld / [Back to the Overworld] — The heist is over, p101/ask_lead", "7721": "Start a new raid / [Start a new raid] — The heist is over, p101/ask_lead", "7722": "Count me in / [Count me in] — Another job?, p101/offer", "7723": "Head home / [Head home] — Another job?, p101/offer", "7724": "Leave now — Leave the heist?", "7725": "Stay — Leave the heist?", "7726": "Head home now / [Head home now] — The heist is over, p101/wait_note", "7727": "I'm in if we go again / [I'm in if we go again] — The heist is over, p101/wait_note", "7728": "The Fixer's Office — The heist is over", "7729": "Leave now — Leave the heist?", "7730": "Go to the Lounge — The heist is over", "7731": "Go to the Lounge — The heist is over", "7732": "Go to the Lounge — Another job?", "7733": "[Skip this puzzle - costs a try] — p122/offer", "7734": "Skip it (costs a try) — Skip this puzzle?", "7735": "Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — 8-Bit Cecil · wardrobe, 8-Bit Cecil's Cartridge, 8-Bit Emma · wardrobe, 8-Bit Emma's Cartridge, 8-Bit Leo · wardrobe, 8-Bit Leo's Cartridge, Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Mr. Capshun · wardrobe, Mr. Capshun's Pencil, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Sky Buddies · wardrobe, The Sky Mobile, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe", "7736": "Pay the Fixer (half the pot, a share) — The Fixer's mercy", "7740": "« The Tailor — 8-BIT CECIL · the Tailor, 8-BIT EMMA · the Tailor, 8-BIT LEO · the Tailor, APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, MR. CAPSHUN · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE SKY BUDDIES · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras", "7741": "Emma — p103/tl/main", "7742": "Celi — p103/tl/main", "7743": "Zib — p103/tl/main", "7744": "Cecil — p103/tl/main", "7745": "KillerWatt — p103/tl/main", "7746": "Leo — p103/tl/main", "7747": "Democratus — p103/tl/main", "7748": "Display cases — p103/tl/main", "7750": "Gold $(r_0) — EMMA · the Tailor", "7751": "Midnight $(r_1) — EMMA · the Tailor", "7752": "Mint $(r_2) — EMMA · the Tailor", "7753": "Snow $(r_3) — EMMA · the Tailor", "7754": "Crimson $(r_4) — EMMA · the Tailor", "7755": "Phantom $(r_5) — EMMA · the Tailor", "7756": "Sundress $(r_6) — EMMA · the Tailor", "7757": "Midnight Gown $(r_7) — EMMA · the Tailor", "7758": "Sakura $(r_8) — EMMA · the Tailor", "7759": "Royal Gown $(r_9) — EMMA · the Tailor", "7760": "Starlight Gown $(r_10) — EMMA · the Tailor", "7761": "Gilded Gown $(r_11) — EMMA · the Tailor", "7762": "Diamond Gown $(r_12) — EMMA · the Tailor", "7763": "Netherite Gown $(r_13) — EMMA · the Tailor", "7764": "Flower Top $(r_14) — EMMA · the Tailor", "7765": "Cozy Sweater $(r_15) — EMMA · the Tailor", "7766": "Aurora $(r_16) — CELI · the Tailor", "7767": "Rosehip $(r_17) — CELI · the Tailor", "7768": "Midnight $(r_18) — CELI · the Tailor", "7769": "Frostfire $(r_19) — CELI · the Tailor", "7770": "Gilded $(r_20) — CELI · the Tailor", "7771": "Diamond $(r_21) — CELI · the Tailor", "7772": "Netherite $(r_22) — CELI · the Tailor", "7773": "Crimson Guard $(r_23) — ZIB · the Tailor", "7774": "Forest Ranger $(r_24) — ZIB · the Tailor", "7775": "Golden Ace $(r_25) — ZIB · the Tailor", "7776": "Diamond Ace $(r_26) — ZIB · the Tailor", "7777": "Netherite Ace $(r_27) — ZIB · the Tailor", "7778": "Crimson Crusader $(r_28) — LEO · the Tailor", "7779": "Royal Purple $(r_29) — LEO · the Tailor", "7780": "Greenwood $(r_30) — LEO · the Tailor", "7781": "Golden Champion $(r_31) — LEO · the Tailor", "7782": "Diamond Champion $(r_32) — LEO · the Tailor", "7783": "Netherite Champion $(r_33) — LEO · the Tailor", "7784": "Crimson Reaper $(r_34) — DEMOCRATUS · the Tailor", "7785": "Ashen Shroud $(r_35) — DEMOCRATUS · the Tailor", "7786": "Royal Violet $(r_36) — DEMOCRATUS · the Tailor", "7787": "Gilded Storm $(r_37) — DEMOCRATUS · the Tailor", "7788": "Diamond Storm $(r_38) — DEMOCRATUS · the Tailor", "7789": "Netherite Storm $(r_39) — DEMOCRATUS · the Tailor", "7790": "Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7791": "Dark Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7792": "Quartz Display Case 5 coins — DISPLAY CASES · the Tailor", "7793": "Gilded Display Case 8 coins — DISPLAY CASES · the Tailor", "7800": "Stay on the job / « Office / « The Office / ◀ The Office — Leave the heist?, THE ARMORY · your kits, for good, THE BOND SIGILS · two at most, each heist, THE CODEX · what you've seen in the vault, THE GUTTER BANK · your coins and spoils, THE TROPHY CASE · twelve rooms, six metals, p98/crew", "7801": "« Armory / ⚒ Armory — THE FIXER'S OFFICE · everything the vault owes you, THE OFFENSE KIT · rank $(r2), THE RANGED KIT · rank $(r3), THE SUPPORT KIT · rank $(r4), THE TANK KIT · rank $(r1), YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own", "7802": "Gutter Bank / « Back / « Your account / ⛃ Gutter Bank — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank, THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies", "7803": "🏆 Trophy Case — THE FIXER'S OFFICE · everything the vault owes you", "7804": "✦ Bond Sigils — THE FIXER'S OFFICE · everything the vault owes you", "7805": "▣ Locker Hall — THE FIXER'S OFFICE · everything the vault owes you", "7806": "⛁ Crate Desk — THE FIXER'S OFFICE · everything the vault owes you", "7807": "« Raid Crew / ☺ Raid Crew — THE FIXER'S OFFICE · everything the vault owes you, p119/page", "7808": "◀ The Codex / 📖 Codex — RAID ODDS · per raider, per won heist, THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 30", "7809": "⚑ Plan a Heist — THE FIXER'S OFFICE · everything the vault owes you", "7811": "⬆ Rank up — THE TANK KIT · rank $(r1)", "7812": "⬆ Rank up — THE OFFENSE KIT · rank $(r2)", "7813": "⬆ Rank up — THE RANGED KIT · rank $(r3)", "7814": "⬆ Rank up — THE SUPPORT KIT · rank $(r4)", "7815": "Tank › — THE ARMORY · your kits, for good", "7816": "Offense › — THE ARMORY · your kits, for good", "7817": "Ranged › — THE ARMORY · your kits, for good", "7818": "Support › — THE ARMORY · your kits, for good", "7819": "none — YOUR SIGNATURE · an effect of your own", "7820": "Secondary weapon — THE ARMORY · your kits, for good", "7821": "$(r_l0) — YOUR SECONDARY · a weapon of your own", "7822": "$(r_l1) — YOUR SECONDARY · a weapon of your own", "7823": "$(r_l2) — YOUR SECONDARY · a weapon of your own", "7824": "$(r_l3) — YOUR SECONDARY · a weapon of your own", "7825": "$(r_l4) — YOUR SECONDARY · a weapon of your own", "7826": "$(r_l5) — YOUR SECONDARY · a weapon of your own", "7827": "$(r_l6) — YOUR SECONDARY · a weapon of your own", "7828": "$(r_l7) — YOUR SECONDARY · a weapon of your own", "7829": "none — YOUR SECONDARY · a weapon of your own", "7830": "Signature effect — THE ARMORY · your kits, for good", "7831": "$(r_l0) — YOUR SIGNATURE · an effect of your own", "7832": "$(r_l1) — YOUR SIGNATURE · an effect of your own", "7833": "$(r_l2) — YOUR SIGNATURE · an effect of your own", "7834": "$(r_l3) — YOUR SIGNATURE · an effect of your own", "7835": "$(r_l4) — YOUR SIGNATURE · an effect of your own", "7836": "$(r_l5) — YOUR SIGNATURE · an effect of your own", "7837": "$(r_l6) — YOUR SIGNATURE · an effect of your own", "7838": "$(r_l7) — YOUR SIGNATURE · an effect of your own", "7839": "$(r_l8) — YOUR SIGNATURE · an effect of your own", "7840": "⬇ Deposit everything — THE GUTTER BANK · your coins and spoils", "7844": "Buy 1 Token (32) — THE GUTTER BANK · Black Market Tokens", "7845": "Buy 10 Tokens (320) — THE GUTTER BANK · Black Market Tokens", "7848": "✦ Buy Tokens — THE GUTTER BANK · your coins and spoils", "7861": "📖 Rooms of the Vault — THE CODEX · what you've seen in the vault", "7862": "📖 Events and Secrets — THE CODEX · what you've seen in the vault", "7863": "📖 Curses Lifted — THE CODEX · what you've seen in the vault", "7864": "📖 Rare Finds — THE CODEX · what you've seen in the vault", "7865": "📖 Masterworks — THE CODEX · what you've seen in the vault", "7866": "🎲 Raid Odds — THE CODEX · what you've seen in the vault", "7870": "⇄ Change coins — GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, THE GUTTER BANK · your coins and spoils", "7875": "16 coins → Medallion — THE GUTTER BANK · Medallions & Trophies", "7876": "128 coins → Trophy — THE GUTTER BANK · Medallions & Trophies", "7877": "Medallion → 16 coins — THE GUTTER BANK · Medallions & Trophies", "7878": "Trophy → 128 coins — THE GUTTER BANK · Medallions & Trophies", "7879": "8 Medallions → Trophy — THE GUTTER BANK · Medallions & Trophies", "7880": "⌂ Fixer's Lounge — THE FIXER'S OFFICE · everything the vault owes you", "7881": "⏭ Skip this puzzle — THE FIXER'S OFFICE · everything the vault owes you", "7883": "Trophy → 8 Medallions — THE GUTTER BANK · Medallions & Trophies", "7884": "The Stalker — p103/crew/row_20", "7885": "The Arachno-Lantern — p103/crew/row_21", "7886": "Bender — p103/crew/row_22", "7887": "Bones — p103/crew/row_23", "7888": "Mr. Capshun — p103/crew/row_24", "7889": "The Sky Buddies — p103/crew/row_25", "7890": "8-Bit Emma — p103/crew/row_26", "7891": "8-Bit Leo — p103/crew/row_27", "7892": "8-Bit Cecil — p103/crew/row_28", "7899": "⏏ Leave the heist — THE FIXER'S OFFICE · everything the vault owes you", "7900": "Cecil — p103/crew/row_0", "7901": "Emma — p103/crew/row_1", "7902": "Celi — p103/crew/row_2", "7903": "Zib — p103/crew/row_3", "7904": "KillerWatt — p103/crew/row_4", "7905": "Leo — p103/crew/row_5", "7906": "Democratus — p103/crew/row_6", "7907": "Skiff Escort — p103/crew/row_7", "7908": "Apophiss — p103/crew/row_8", "7909": "Tullius — p103/crew/row_9", "7910": "Fishy — p103/crew/row_10", "7911": "Dennis — p103/crew/row_11", "7912": "Pistachio — p103/crew/row_12", "7913": "Omega — p103/crew/row_13", "7914": "Ashur — p103/crew/row_14", "7915": "The Chef — p103/crew/row_15", "7916": "The Neighbor — p103/crew/row_16", "7917": "Queen Ava — p103/crew/row_17", "7918": "Queen Pearl — p103/crew/row_18", "7919": "Bloo — p103/crew/row_19", "7920": "The Frog — p103/crew/row_29", "7921": "Donado — p103/crew/row_30", "7931": "Knuckles — p103/crew/hire_rows", "7932": "Doc Whiskers — p103/crew/hire_rows", "7933": "Fingers — p103/crew/hire_rows", "7934": "Tick-Tock — p103/crew/hire_rows", "7935": "Boomer — p103/crew/hire_rows", "7950": "Outfits & Emma's buff / Outfits & chatter — p98/crew", "7951": "Emma's wardrobe — p119/page", "7952": "Celi's wardrobe — p119/page", "7953": "Zib's wardrobe — p119/page", "7954": "Cecil's wardrobe — p119/page", "7955": "KillerWatt's wardrobe — p119/page", "7956": "Leo's wardrobe — p119/page", "7957": "Democratus's wardrobe — p119/page", "7961": "Emma: Speed — p119/page", "7962": "Emma: Offense — p119/page", "7963": "Emma: Defense — p119/page", "7964": "Emma: Healing — p119/page", "7965": "Emma: Mining — p119/page", "7968": "Chatter on / off — p119/page", "7970": "Gutter Coins $(c) — THE GUTTER BANK · your coins and spoils", "7971": "Gutter Medallions $(gm) — THE GUTTER BANK · your coins and spoils", "7972": "Gutter Trophies $(gt) — THE GUTTER BANK · your coins and spoils", "7973": "Copper Cogs $(m1) — THE GUTTER BANK · your coins and spoils", "7974": "Silver Seals $(m2) — THE GUTTER BANK · your coins and spoils", "7975": "Gilded Leaves $(m3) — THE GUTTER BANK · your coins and spoils", "7976": "Deep Pearls $(m4) — THE GUTTER BANK · your coins and spoils", "7977": "Hoard Embers $(m5) — THE GUTTER BANK · your coins and spoils", "7978": "Captain's Insignia $(m6) — THE GUTTER BANK · your coins and spoils", "7980": "⬇ Deposit 1 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7981": "⬇ Deposit 10 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7982": "⬇ Deposit all ($(h)) — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7983": "⬆ Take 1 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7984": "⬆ Take 10 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7985": "⬆ Take all ($(n)) — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "8000": "« The Recruiter — p137/rc/gems, p137/rc/hires", "8001": "Cecil 192 coins / Cecil IN YOUR PACK / Cecil SIGNED — p137/rc/main", "8002": "Emma 192 coins / Emma IN YOUR PACK / Emma SIGNED — p137/rc/main", "8003": "Celi 224 coins / Celi IN YOUR PACK / Celi SIGNED — p137/rc/main", "8004": "Zib 192 coins / Zib IN YOUR PACK / Zib SIGNED — p137/rc/main", "8005": "KillerWatt 320 coins / KillerWatt IN YOUR PACK / KillerWatt SIGNED — p137/rc/main", "8006": "Leo 208 coins / Leo IN YOUR PACK / Leo SIGNED — p137/rc/main", "8007": "Democratus 224 coins / Democratus IN YOUR PACK / Democratus SIGNED — p137/rc/main", "8008": "Skiff Escort 128 coins / Skiff Escort IN YOUR PACK / Skiff Escort SIGNED — p137/rc/main", "8009": "Apophiss 352 coins / Apophiss IN YOUR PACK / Apophiss SIGNED — p137/rc/main", "8010": "Tullius 336 coins / Tullius IN YOUR PACK / Tullius SIGNED — p137/rc/main", "8011": "Fishy 176 coins / Fishy IN YOUR PACK / Fishy SIGNED — p137/rc/main", "8012": "Dennis 176 coins / Dennis IN YOUR PACK / Dennis SIGNED — p137/rc/main", "8013": "Pistachio 176 coins / Pistachio IN YOUR PACK / Pistachio SIGNED — p137/rc/main", "8014": "Omega 176 coins / Omega IN YOUR PACK / Omega SIGNED — p137/rc/main", "8015": "Ashur 176 coins / Ashur IN YOUR PACK / Ashur SIGNED — p137/rc/main", "8016": "The Chef 176 coins / The Chef IN YOUR PACK / The Chef SIGNED — p137/rc/main", "8017": "The Neighbor 176 coins / The Neighbor IN YOUR PACK / The Neighbor SIGNED — p137/rc/main", "8018": "Queen Ava 176 coins / Queen Ava IN YOUR PACK / Queen Ava SIGNED — p137/rc/main", "8019": "Queen Pearl 176 coins / Queen Pearl IN YOUR PACK / Queen Pearl SIGNED — p137/rc/main", "8020": "Bloo 176 coins / Bloo IN YOUR PACK / Bloo SIGNED — p137/rc/main", "8021": "The Stalker 176 coins / The Stalker IN YOUR PACK / The Stalker SIGNED — p137/rc/main", "8022": "The Arachno-Lantern 176 coins / The Arachno-Lantern IN YOUR PACK / The Arachno-Lantern SIGNED — p137/rc/main", "8023": "Bender 176 coins / Bender IN YOUR PACK / Bender SIGNED — p137/rc/main", "8024": "Bones 176 coins / Bones IN YOUR PACK / Bones SIGNED — p137/rc/main", "8025": "Mr. Capshun 176 coins / Mr. Capshun IN YOUR PACK / Mr. Capshun SIGNED — p137/rc/main", "8026": "The Sky Buddies 176 coins / The Sky Buddies IN YOUR PACK / The Sky Buddies SIGNED — p137/rc/main", "8027": "8-Bit Emma 176 coins / 8-Bit Emma IN YOUR PACK / 8-Bit Emma SIGNED — p137/rc/main", "8028": "8-Bit Leo 176 coins / 8-Bit Leo IN YOUR PACK / 8-Bit Leo SIGNED — p137/rc/main", "8029": "8-Bit Cecil 176 coins / 8-Bit Cecil IN YOUR PACK / 8-Bit Cecil SIGNED — p137/rc/main", "8030": "The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main", "8031": "Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main", "8040": "Hirelings › — p137/rc/main", "8041": "Knuckles 48 coins / Knuckles FILED / Knuckles IN YOUR PACK — p137/rc/hires", "8042": "Doc Whiskers 64 coins / Doc Whiskers FILED / Doc Whiskers IN YOUR PACK — p137/rc/hires", "8043": "Fingers 48 coins / Fingers FILED / Fingers IN YOUR PACK — p137/rc/hires", "8044": "Tick-Tock 64 coins / Tick-Tock FILED / Tick-Tock IN YOUR PACK — p137/rc/hires", "8045": "Boomer 64 coins / Boomer FILED / Boomer IN YOUR PACK — p137/rc/hires", "8050": "Vault gems › — p137/rc/main", "8051": "Fire Gem 96 coins — p137/rc/gems", "8052": "Water Gem 96 coins — p137/rc/gems", "8053": "Poison Gem 96 coins — p137/rc/gems", "8054": "Earth Gem 96 coins — p137/rc/gems", "8055": "Electric Gem 96 coins — p137/rc/gems", "8056": "Rock Gem 96 coins — p137/rc/gems", "8057": "Air Gem 96 coins — p137/rc/gems", "8058": "Grass Gem 96 coins — p137/rc/gems", "8059": "Ice Gem 96 coins — p137/rc/gems", "8100": "Apophiss — p103/tl/main", "8101": "Tullius — p103/tl/main", "8102": "The Frog — p103/tl/main", "8103": "Donado — p103/tl/main", "8104": "Pearlman — p103/tl/main", "8105": "Wilfrey — p103/tl/main", "8106": "Auras (rare) — p103/tl/main", "8107": "Fishy — p103/tl/main", "8108": "Dennis — p103/tl/main", "8109": "Pistachio — p103/tl/main", "8110": "Crimson $(r_40) — CECIL · the Tailor", "8111": "Midnight $(r_41) — CECIL · the Tailor", "8112": "Bone $(r_42) — CECIL · the Tailor", "8113": "Gilded $(r_43) — CECIL · the Tailor", "8114": "Diamond $(r_44) — CECIL · the Tailor", "8115": "Netherite $(r_45) — CECIL · the Tailor", "8116": "Midnight $(r_46) — KILLERWATT · the Tailor", "8117": "Bone $(r_47) — KILLERWATT · the Tailor", "8118": "Neon $(r_48) — KILLERWATT · the Tailor", "8119": "Golden Thunder $(r_49) — KILLERWATT · the Tailor", "8120": "Diamond Thunder $(r_50) — KILLERWATT · the Tailor", "8121": "Netherite Thunder $(r_51) — KILLERWATT · the Tailor", "8122": "Obsidian Coil $(r_52) — APOPHISS · the Tailor", "8123": "Blood Wyrm $(r_53) — APOPHISS · the Tailor", "8124": "Frost Serpent $(r_54) — APOPHISS · the Tailor", "8125": "Gilded Coil $(r_55) — APOPHISS · the Tailor", "8126": "Diamond Coil $(r_56) — APOPHISS · the Tailor", "8127": "Netherite Coil $(r_57) — APOPHISS · the Tailor", "8128": "Admiral's Blue $(r_58) — TULLIUS · the Tailor", "8129": "Corsair Crimson $(r_59) — TULLIUS · the Tailor", "8130": "Bleached Bone $(r_60) — TULLIUS · the Tailor", "8131": "Gilded Captain $(r_61) — TULLIUS · the Tailor", "8132": "Diamond Captain $(r_62) — TULLIUS · the Tailor", "8133": "Netherite Captain $(r_63) — TULLIUS · the Tailor", "8134": "Bluejay $(r_64) — THE FROG · the Tailor", "8135": "Ember Toad $(r_65) — THE FROG · the Tailor", "8136": "Old Bog $(r_66) — THE FROG · the Tailor", "8137": "Golden Prince $(r_67) — THE FROG · the Tailor", "8138": "Diamond Prince $(r_68) — THE FROG · the Tailor", "8139": "Netherite Prince $(r_69) — THE FROG · the Tailor", "8140": "Chocolate $(r_70) — DONADO · the Tailor", "8141": "Midnight $(r_71) — DONADO · the Tailor", "8142": "Snowdrift $(r_72) — DONADO · the Tailor", "8143": "Starlit $(r_73) — DONADO · the Tailor", "8144": "Gilded $(r_74) — DONADO · the Tailor", "8145": "Diamond $(r_75) — DONADO · the Tailor", "8146": "Netherite $(r_76) — DONADO · the Tailor", "8147": "Ruby $(r_77) — PEARLMAN · the Tailor", "8148": "Emerald $(r_78) — PEARLMAN · the Tailor", "8149": "Amethyst $(r_79) — PEARLMAN · the Tailor", "8150": "Blossom Halo (Emma) 1280 coins / Blossom Halo (Emma) OWNED — p103/tl/auras", "8151": "Moonfrost Veil (Celi) 1280 coins / Moonfrost Veil (Celi) OWNED — p103/tl/auras", "8152": "Starfield Static (Zib) 1280 coins / Starfield Static (Zib) OWNED — p103/tl/auras", "8153": "Arcane Corona (Cecil) 1280 coins / Arcane Corona (Cecil) OWNED — p103/tl/auras", "8154": "Storm Crown (KillerWatt) 1280 coins / Storm Crown (KillerWatt) OWNED — p103/tl/auras", "8155": "Tidal Aegis (Leo) 1280 coins / Tidal Aegis (Leo) OWNED — p103/tl/auras", "8156": "Reaper's Shroud (Democratus) 1280 coins / Reaper's Shroud (Democratus) OWNED — p103/tl/auras", "8157": "Black-Flame Mantle (Apophiss) 1280 coins / Black-Flame Mantle (Apophiss) OWNED — p103/tl/auras", "8158": "Drowned Gale (Tullius) 1280 coins / Drowned Gale (Tullius) OWNED — p103/tl/auras", "8159": "Bog-Light Ring (the Frog) 1280 coins / Bog-Light Ring (the Frog) OWNED — p103/tl/auras", "8160": "Tractor Beam (Donado) 1280 coins / Tractor Beam (Donado) OWNED — p103/tl/auras", "8161": "Golden Gleam (Pearlman) 1280 coins / Golden Gleam (Pearlman) OWNED — p103/tl/auras", "8162": "Lordly Radiance (Wilfrey) 1280 coins / Lordly Radiance (Wilfrey) OWNED — p103/tl/auras", "8163": "Bubble Halo (Fishy) 1280 coins / Bubble Halo (Fishy) OWNED — p103/tl/auras", "8164": "Gilded $(r_80) — PEARLMAN · the Tailor", "8165": "Diamond $(r_81) — PEARLMAN · the Tailor", "8166": "Netherite $(r_82) — PEARLMAN · the Tailor", "8167": "Midnight Silk $(r_83) — FISHY · the Tailor", "8168": "Crimson Opera $(r_84) — FISHY · the Tailor", "8169": "Emerald Ascot $(r_85) — FISHY · the Tailor", "8170": "Gilded Topper $(r_86) — FISHY · the Tailor", "8171": "Diamond Topper $(r_87) — FISHY · the Tailor", "8172": "Netherite Topper $(r_88) — FISHY · the Tailor", "8173": "Crimson Cross $(r_89) — WILFREY · the Tailor", "8174": "Azure Chevron $(r_90) — WILFREY · the Tailor", "8175": "Verdant Bend $(r_91) — WILFREY · the Tailor", "8176": "Gilded Sun $(r_92) — WILFREY · the Tailor", "8177": "Diamond Sun $(r_93) — WILFREY · the Tailor", "8178": "Netherite Sun $(r_94) — WILFREY · the Tailor", "8179": "Road Brown $(r_95) — DENNIS · the Tailor", "8180": "Biker Red $(r_96) — DENNIS · the Tailor", "8181": "Forest Leather $(r_97) — DENNIS · the Tailor", "8182": "Gilded Jacket $(r_98) — DENNIS · the Tailor", "8183": "Diamond Jacket $(r_99) — DENNIS · the Tailor", "8184": "Netherite Jacket $(r_100) — DENNIS · the Tailor", "8185": "Midnight Tails $(r_101) — PISTACHIO · the Tailor", "8186": "Claret Tails $(r_102) — PISTACHIO · the Tailor", "8187": "Ivory Tails $(r_103) — PISTACHIO · the Tailor", "8188": "Gilded Tails $(r_104) — PISTACHIO · the Tailor", "8189": "Diamond Tails $(r_105) — PISTACHIO · the Tailor", "8190": "Netherite Tails $(r_106) — PISTACHIO · the Tailor", "8191": "Spectral Blue $(r_107) — KING OMEGA · the Tailor", "8192": "Blood Moon $(r_108) — KING OMEGA · the Tailor", "8193": "Verdant Wraith $(r_109) — KING OMEGA · the Tailor", "8194": "Gilded King $(r_110) — KING OMEGA · the Tailor", "8195": "Diamond King $(r_111) — KING OMEGA · the Tailor", "8196": "Gold Rush Glimmer (Dennis) 1280 coins / Gold Rush Glimmer (Dennis) OWNED — p103/tl/auras", "8197": "Ectoplasmic Mist (Pistachio) 1280 coins / Ectoplasmic Mist (Pistachio) OWNED — p103/tl/auras", "8198": "Court of Souls (King Omega) 1280 coins / Court of Souls (King Omega) OWNED — p103/tl/auras", "8199": "Ashfall Crown (Ashur) 1280 coins / Ashfall Crown (Ashur) OWNED — p103/tl/auras", "8200": "Netherite King $(r_112) — KING OMEGA · the Tailor", "8201": "Blue Flame $(r_113) — ASHUR · the Tailor", "8202": "Verdant Ember $(r_114) — ASHUR · the Tailor", "8203": "Obsidian Rose $(r_115) — ASHUR · the Tailor", "8204": "Gilded Magma $(r_116) — ASHUR · the Tailor", "8205": "Diamond Magma $(r_117) — ASHUR · the Tailor", "8206": "Netherite Magma $(r_118) — ASHUR · the Tailor", "8207": "Midnight Brigade $(r_119) — THE CHEF · the Tailor", "8208": "Bistro Blue $(r_120) — THE CHEF · the Tailor", "8209": "Sommelier Wine $(r_121) — THE CHEF · the Tailor", "8210": "Gilded Whites $(r_122) — THE CHEF · the Tailor", "8211": "Diamond Whites $(r_123) — THE CHEF · the Tailor", "8212": "Netherite Whites $(r_124) — THE CHEF · the Tailor", "8213": "Navy Bandmaster $(r_125) — THE NEIGHBOR · the Tailor", "8214": "Encore Crimson $(r_126) — THE NEIGHBOR · the Tailor", "8215": "Jazz Violet $(r_127) — THE NEIGHBOR · the Tailor", "8216": "Gilded Suit $(r_128) — THE NEIGHBOR · the Tailor", "8217": "Diamond Suit $(r_129) — THE NEIGHBOR · the Tailor", "8218": "Netherite Suit $(r_130) — THE NEIGHBOR · the Tailor", "8219": "Coral Reef $(r_131) — QUEEN AVA · the Tailor", "8220": "Abyssal Violet $(r_132) — QUEEN AVA · the Tailor", "8221": "Kelp Forest $(r_133) — QUEEN AVA · the Tailor", "8222": "Gilded Gown $(r_134) — QUEEN AVA · the Tailor", "8223": "Diamond Gown $(r_135) — QUEEN AVA · the Tailor", "8224": "Netherite Gown $(r_136) — QUEEN AVA · the Tailor", "8225": "Coral Pink $(r_137) — QUEEN PEARL · the Tailor", "8226": "Sunset Gold $(r_138) — QUEEN PEARL · the Tailor", "8227": "Starlit Navy $(r_139) — QUEEN PEARL · the Tailor", "8228": "Gilded Dress $(r_140) — QUEEN PEARL · the Tailor", "8229": "Diamond Dress $(r_141) — QUEEN PEARL · the Tailor", "8230": "Netherite Dress $(r_142) — QUEEN PEARL · the Tailor", "8231": "Shadow Pelt $(r_143) — BLOO · the Tailor", "8232": "Ember Mane $(r_144) — BLOO · the Tailor", "8233": "Frost Coat $(r_145) — BLOO · the Tailor", "8234": "Gilded Fur $(r_146) — BLOO · the Tailor", "8235": "Diamond Fur $(r_147) — BLOO · the Tailor", "8236": "Netherite Fur $(r_148) — BLOO · the Tailor", "8237": "Bone White $(r_149) — THE STALKER · the Tailor", "8238": "Ashen Grey $(r_150) — THE STALKER · the Tailor", "8239": "Blood Moon $(r_151) — THE STALKER · the Tailor", "8240": "Gilded Skin $(r_152) — THE STALKER · the Tailor", "8241": "Diamond Skin $(r_153) — THE STALKER · the Tailor", "8242": "Netherite Skin $(r_154) — THE STALKER · the Tailor", "8243": "Ghost Gourd $(r_155) — THE ARACHNO-LANTERN · the Tailor", "8244": "Soulfire Rind $(r_156) — THE ARACHNO-LANTERN · the Tailor", "8245": "Harvest Moon $(r_157) — THE ARACHNO-LANTERN · the Tailor", "8246": "Gilded Rind $(r_158) — THE ARACHNO-LANTERN · the Tailor", "8247": "Diamond Rind $(r_159) — THE ARACHNO-LANTERN · the Tailor", "8248": "Netherite Rind $(r_160) — THE ARACHNO-LANTERN · the Tailor", "8249": "Midnight Black $(r_161) — BENDER · the Tailor", "8250": "Snow White $(r_162) — BENDER · the Tailor", "8251": "Sable $(r_163) — BENDER · the Tailor", "8252": "Gilded Coat $(r_164) — BENDER · the Tailor", "8253": "Diamond Coat $(r_165) — BENDER · the Tailor", "8254": "Netherite Coat $(r_166) — BENDER · the Tailor", "8255": "Great White $(r_167) — BONES · the Tailor", "8256": "Hammerhead Bronze $(r_168) — BONES · the Tailor", "8257": "Abyss Black $(r_169) — BONES · the Tailor", "8258": "Gilded Skin $(r_170) — BONES · the Tailor", "8259": "Diamond Skin $(r_171) — BONES · the Tailor", "8260": "Netherite Skin $(r_172) — BONES · the Tailor", "8261": "Bubblegum Pink $(r_173) — THE SKY BUDDIES · the Tailor", "8262": "Mint Dream $(r_174) — THE SKY BUDDIES · the Tailor", "8263": "Lavender Night $(r_175) — THE SKY BUDDIES · the Tailor", "8264": "Gilded Nightcap $(r_176) — THE SKY BUDDIES · the Tailor", "8265": "Diamond Nightcap $(r_177) — THE SKY BUDDIES · the Tailor", "8266": "Netherite Nightcap $(r_178) — THE SKY BUDDIES · the Tailor", "8267": "Game Boy $(r_179) — 8-BIT EMMA · the Tailor", "8268": "Virtual Boy $(r_180) — 8-BIT EMMA · the Tailor", "8269": "Sepia Print $(r_181) — 8-BIT EMMA · the Tailor", "8270": "King Omega — p103/tl/main", "8271": "Ashur — p103/tl/main", "8272": "The Chef — p103/tl/main", "8273": "The Neighbor — p103/tl/main", "8274": "Queen Ava — p103/tl/main", "8275": "Queen Pearl — p103/tl/main", "8276": "Bloo — p103/tl/main", "8277": "The Stalker — p103/tl/main", "8278": "The Arachno-Lantern — p103/tl/main", "8279": "Bender — p103/tl/main", "8280": "Apophiss's wardrobe / Bones — p103/tl/main, p119/page", "8281": "Mr. Capshun / Tullius's wardrobe — p103/tl/main, p119/page", "8282": "8-Bit Cecil / The Frog's wardrobe — p103/tl/main, p119/page", "8283": "8-Bit Leo / Donado's wardrobe — p103/tl/main, p119/page", "8284": "8-Bit Emma / Pearlman's wardrobe — p103/tl/main, p119/page", "8285": "The Sky Buddies / Wilfrey's wardrobe — p103/tl/main, p119/page", "8286": "Fishy's wardrobe — p119/page", "8287": "Dennis's wardrobe — p119/page", "8288": "Pistachio's wardrobe — p119/page", "8289": "King Omega's wardrobe — p119/page", "8290": "Ashur's wardrobe — p119/page", "8291": "The Chef's wardrobe — p119/page", "8292": "The Neighbor's wardrobe — p119/page", "8293": "Kitchen Steam (the Chef) 1280 coins / Kitchen Steam (the Chef) OWNED / Queen Ava's wardrobe — p103/tl/auras, p119/page", "8294": "Grand Symphony (the Neighbor) 1280 coins / Grand Symphony (the Neighbor) OWNED / Queen Pearl's wardrobe — p103/tl/auras, p119/page", "8295": "Bloo's wardrobe / Crown of the Deep (Queen Ava) 1280 coins / Crown of the Deep (Queen Ava) OWNED — p103/tl/auras, p119/page", "8296": "Pearlescent Tide (Queen Pearl) 1280 coins / Pearlescent Tide (Queen Pearl) OWNED / The Stalker's wardrobe — p103/tl/auras, p119/page", "8297": "Feral Moon (Bloo) 1280 coins / Feral Moon (Bloo) OWNED / The Arachno-Lantern's wardrobe — p103/tl/auras, p119/page", "8298": "Bender's wardrobe / The Long Night (The Stalker) 1280 coins / The Long Night (The Stalker) OWNED — p103/tl/auras, p119/page", "8299": "Bones's wardrobe / Hallowfire (The Arachno-Lantern) 1280 coins / Hallowfire (The Arachno-Lantern) OWNED — p103/tl/auras, p119/page", "8300": "Mr. Capshun's wardrobe — p119/page", "8301": "8-Bit Cecil's wardrobe / Wait here / follow me — Pearlman's Business Card, p119/page", "8302": "8-Bit Leo's wardrobe / Wardrobe — Pearlman's Business Card, p119/page", "8303": "8-Bit Emma's wardrobe / Seasons — Pearlman's Business Card, p119/page", "8304": "The Sky Buddies's wardrobe — p119/page", "8309": "Send him home — Pearlman's Business Card", "8380": "Goodest Boy (Bender) 1280 coins / Goodest Boy (Bender) OWNED — p103/tl/auras", "8381": "Abyssal Tide (Bones) 1280 coins / Abyssal Tide (Bones) OWNED — p103/tl/auras", "8382": "Rainbow Doodles (Mr. Capshun) 1280 coins / Rainbow Doodles (Mr. Capshun) OWNED — p103/tl/auras", "8383": "Starry Sky (The Sky Buddies) 1280 coins / Starry Sky (The Sky Buddies) OWNED — p103/tl/auras", "8384": "Scanlines (8-Bit Emma) 1280 coins / Scanlines (8-Bit Emma) OWNED — p103/tl/auras", "8385": "Scanlines (8-Bit Leo) 1280 coins / Scanlines (8-Bit Leo) OWNED — p103/tl/auras", "8386": "Scanlines (8-Bit Cecil) 1280 coins / Scanlines (8-Bit Cecil) OWNED — p103/tl/auras", "8501": "Raw Materials Crate 16 coins — THE CRATE DESK · paid from your bank and pockets", "8502": "Adventurer's Crate 32 coins — THE CRATE DESK · paid from your bank and pockets", "8503": "Mineral Crate 48 coins — THE CRATE DESK · paid from your bank and pockets", "8504": "Crimson Tip-off 64 coins — THE CRATE DESK · paid from your bank and pockets", "8505": "Vorn Signal 64 coins — THE CRATE DESK · paid from your bank and pockets", "8506": "Stone Crate 6 coins — THE CRATE DESK · paid from your bank and pockets", "8507": "Timber Crate 8 coins — THE CRATE DESK · paid from your bank and pockets", "8601": "Sit / follow — The Serpent's Oath", "8602": "Ride him — The Serpent's Oath", "8603": "Take off the saddle — The Serpent's Oath", "8604": "Wardrobe — The Serpent's Oath", "8608": "Call for Apophiss — The Serpent's Oath", "8609": "Send him home — The Serpent's Oath", "8621": "Sit / follow — Tullius's Frozen Doubloon", "8624": "Wardrobe — Tullius's Frozen Doubloon", "8628": "Call for Tullius — Tullius's Frozen Doubloon", "8629": "Send him home — Tullius's Frozen Doubloon", "8641": "Sit / follow — Signet of the Frog Knight", "8642": "Hand back my gear — Signet of the Frog Knight", "8643": "Wardrobe — Signet of the Frog Knight", "8648": "Call for the Frog — Signet of the Frog Knight", "8649": "Send him home — Signet of the Frog Knight", "8651": "Sit / follow — Donado's Collar Tag", "8652": "Hand back my gear — Donado's Collar Tag", "8653": "Wardrobe — Donado's Collar Tag", "8658": "Call for Donado — Donado's Collar Tag", "8659": "Send him home — Donado's Collar Tag", "9000": "$(r_home) / « Outfits & buffs — Apophiss · wardrobe", "9002": "His own scales $(r_apo0) — Apophiss · wardrobe", "9003": "Obsidian Coil $(r_apo1) — Apophiss · wardrobe", "9004": "Blood Wyrm $(r_apo2) — Apophiss · wardrobe", "9005": "Frost Serpent $(r_apo3) — Apophiss · wardrobe", "9006": "Gilded Coil $(r_apo4) — Apophiss · wardrobe", "9007": "Diamond Coil $(r_apo5) — Apophiss · wardrobe", "9008": "Netherite Coil $(r_apo6) — Apophiss · wardrobe", "9018": "Pixel costume $(r_px) — Apophiss · wardrobe", "9019": "Black-Flame Mantle $(r_aura) — Apophiss · wardrobe", "9020": "$(r_home) / « Outfits & buffs — Tullius · wardrobe", "9022": "His old coat $(r_tul0) — Tullius · wardrobe", "9023": "Admiral's Blue $(r_tul1) — Tullius · wardrobe", "9024": "Corsair Crimson $(r_tul2) — Tullius · wardrobe", "9025": "Bleached Bone $(r_tul3) — Tullius · wardrobe", "9026": "Gilded Captain $(r_tul4) — Tullius · wardrobe", "9027": "Diamond Captain $(r_tul5) — Tullius · wardrobe", "9028": "Netherite Captain $(r_tul6) — Tullius · wardrobe", "9038": "Pixel costume $(r_px) — Tullius · wardrobe", "9039": "Drowned Gale $(r_aura) — Tullius · wardrobe", "9040": "$(r_home) / « Outfits & buffs — the Frog with Mustache · wardrobe", "9042": "His own skin $(r_frog0) — the Frog with Mustache · wardrobe", "9043": "Bluejay $(r_frog1) — the Frog with Mustache · wardrobe", "9044": "Ember Toad $(r_frog2) — the Frog with Mustache · wardrobe", "9045": "Old Bog $(r_frog3) — the Frog with Mustache · wardrobe", "9046": "Golden Prince $(r_frog4) — the Frog with Mustache · wardrobe", "9047": "Diamond Prince $(r_frog5) — the Frog with Mustache · wardrobe", "9048": "Netherite Prince $(r_frog6) — the Frog with Mustache · wardrobe", "9058": "Pixel costume $(r_px) — the Frog with Mustache · wardrobe", "9059": "Bog-Light Ring $(r_aura) — the Frog with Mustache · wardrobe", "9060": "$(r_home) / « Outfits & buffs — Donado · wardrobe", "9062": "His own coat $(r_don0) — Donado · wardrobe", "9063": "Chocolate $(r_don1) — Donado · wardrobe", "9064": "Midnight $(r_don2) — Donado · wardrobe", "9065": "Snowdrift $(r_don3) — Donado · wardrobe", "9066": "Starlit $(r_don4) — Donado · wardrobe", "9067": "Gilded $(r_don5) — Donado · wardrobe", "9068": "Diamond $(r_don6) — Donado · wardrobe", "9069": "Netherite $(r_don7) — Donado · wardrobe", "9078": "Pixel costume $(r_px) — Donado · wardrobe", "9079": "Tractor Beam $(r_aura) — Donado · wardrobe", "9080": "$(r_home) / « Outfits & buffs — Pearlman · wardrobe", "9082": "The blue bow tie $(r_pearl0) — Pearlman · wardrobe", "9083": "Ruby $(r_pearl1) — Pearlman · wardrobe", "9084": "Emerald $(r_pearl2) — Pearlman · wardrobe", "9085": "Amethyst $(r_pearl3) — Pearlman · wardrobe", "9086": "Gilded $(r_pearl4) — Pearlman · wardrobe", "9087": "Diamond $(r_pearl5) — Pearlman · wardrobe", "9088": "Netherite $(r_pearl6) — Pearlman · wardrobe", "9098": "Pixel costume $(r_px) — Pearlman · wardrobe", "9099": "Golden Gleam $(r_aura) — Pearlman · wardrobe", "9100": "$(r_home) / « Outfits & buffs — Wilfrey · wardrobe", "9102": "No shield $(r_wil0) — Wilfrey · wardrobe", "9103": "Crimson Cross $(r_wil1) — Wilfrey · wardrobe", "9104": "Azure Chevron $(r_wil2) — Wilfrey · wardrobe", "9105": "Verdant Bend $(r_wil3) — Wilfrey · wardrobe", "9106": "Gilded Sun $(r_wil4) — Wilfrey · wardrobe", "9107": "Diamond Sun $(r_wil5) — Wilfrey · wardrobe", "9108": "Netherite Sun $(r_wil6) — Wilfrey · wardrobe", "9118": "Pixel costume $(r_px) — Wilfrey · wardrobe", "9119": "Lordly Radiance $(r_aura) — Wilfrey · wardrobe", "9120": "$(r_home) / « Outfits & buffs — Fishy · wardrobe", "9122": "His old black topper $(r_fishy0) — Fishy · wardrobe", "9123": "Midnight Silk $(r_fishy1) — Fishy · wardrobe", "9124": "Crimson Opera $(r_fishy2) — Fishy · wardrobe", "9125": "Emerald Ascot $(r_fishy3) — Fishy · wardrobe", "9126": "Gilded Topper $(r_fishy4) — Fishy · wardrobe", "9127": "Diamond Topper $(r_fishy5) — Fishy · wardrobe", "9128": "Netherite Topper $(r_fishy6) — Fishy · wardrobe", "9138": "Pixel costume $(r_px) — Fishy · wardrobe", "9139": "Bubble Halo $(r_aura) — Fishy · wardrobe", "9141": "Sit / follow — Fishy's Pocket Bowl", "9142": "Wardrobe — Fishy's Pocket Bowl", "9143": "The Cabinet — Fishy's Pocket Bowl", "9144": "Fishy's powers — Fishy's Pocket Bowl", "9148": "Call for Fishy — Fishy's Pocket Bowl", "9149": "Send him home — Fishy's Pocket Bowl", "9150": "« The Cabinet — FISHY'S POWERS · taught by the Cabinet, THE COURT · $(n) of 20, THE DEEP · $(n) of 20, THE GUTTER · $(n) of 20, THE HOLLOW · $(n) of 20, THE SKIES · $(n) of 20, THE WILDS · $(n) of 20", "9151": "The Hollow $(c_hollow) of 20$(r_hollow) — FISHY'S CABINET OF CURIOSITIES", "9152": "The Gutter $(c_gutter) of 20$(r_gutter) — FISHY'S CABINET OF CURIOSITIES", "9153": "The Skies $(c_skies) of 20$(r_skies) — FISHY'S CABINET OF CURIOSITIES", "9154": "The Deep $(c_deep) of 20$(r_deep) — FISHY'S CABINET OF CURIOSITIES", "9155": "The Wilds $(c_wilds) of 20$(r_wilds) — FISHY'S CABINET OF CURIOSITIES", "9156": "The Court $(c_court) of 20$(r_court) — FISHY'S CABINET OF CURIOSITIES", "9157": "Fishy's powers — FISHY'S CABINET OF CURIOSITIES", "9158": "Set it out in the hall — THE COURT · $(n) of 20, THE DEEP · $(n) of 20, THE GUTTER · $(n) of 20, THE HOLLOW · $(n) of 20, THE SKIES · $(n) of 20, THE WILDS · $(n) of 20", "9159": "A spare Pocket Bowl — FISHY'S CABINET OF CURIOSITIES", "9701": "Duel him — Democratus' Challenge", "9702": "Call for Democratus / Send him home — Democratus' Challenge", "9703": "Wardrobe — Democratus' Challenge", "9800": "$(r_home) / « Outfits & buffs — Emma · wardrobe", "9802": "Pink ribbon $(r_ribbon0) — Emma · wardrobe", "9803": "Gold $(r_ribbon1) — Emma · wardrobe", "9804": "Midnight $(r_ribbon2) — Emma · wardrobe", "9805": "Mint $(r_ribbon3) — Emma · wardrobe", "9806": "Snow $(r_ribbon4) — Emma · wardrobe", "9807": "Crimson $(r_ribbon5) — Emma · wardrobe", "9808": "Phantom $(r_ribbon6) — Emma · wardrobe", "9812": "Her own dress $(r_dress0) — Emma · wardrobe", "9813": "Sundress $(r_dress1) — Emma · wardrobe", "9814": "Midnight Gown $(r_dress2) — Emma · wardrobe", "9815": "Sakura $(r_dress3) — Emma · wardrobe", "9816": "Royal Gown $(r_dress4) — Emma · wardrobe", "9817": "Starlight Gown $(r_dress5) — Emma · wardrobe", "9818": "Gilded Gown $(r_dress6) — Emma · wardrobe", "9819": "Diamond Gown $(r_dress7) — Emma · wardrobe", "9820": "Netherite Gown $(r_dress8) — Emma · wardrobe", "9823": "Flower Top $(r_outfit1) — Emma · wardrobe", "9824": "Cozy Sweater $(r_outfit2) — Emma · wardrobe", "9837": "KillerWatt look $(r_kw) — Emma · wardrobe", "9839": "Blossom Halo $(r_aura) — Emma · wardrobe", "9840": "$(r_home) / « Outfits & buffs — Celi · wardrobe", "9842": "Own clothes $(r_celi0) — Celi · wardrobe", "9843": "Aurora $(r_celi1) — Celi · wardrobe", "9844": "Rosehip $(r_celi2) — Celi · wardrobe", "9845": "Midnight $(r_celi3) — Celi · wardrobe", "9846": "Frostfire $(r_celi4) — Celi · wardrobe", "9847": "Gilded $(r_celi5) — Celi · wardrobe", "9848": "Diamond $(r_celi6) — Celi · wardrobe", "9849": "Netherite $(r_celi7) — Celi · wardrobe", "9858": "Pixel costume $(r_px) — Celi · wardrobe", "9859": "Moonfrost Veil $(r_aura) — Celi · wardrobe", "9860": "$(r_home) / « Outfits & buffs — Zib · wardrobe", "9862": "Own clothes $(r_zib0) — Zib · wardrobe", "9863": "Crimson Guard $(r_zib1) — Zib · wardrobe", "9864": "Forest Ranger $(r_zib2) — Zib · wardrobe", "9865": "Golden Ace $(r_zib3) — Zib · wardrobe", "9866": "Diamond Ace $(r_zib4) — Zib · wardrobe", "9867": "Netherite Ace $(r_zib5) — Zib · wardrobe", "9878": "Pixel costume $(r_px) — Zib · wardrobe", "9879": "Starfield Static $(r_aura) — Zib · wardrobe", "9880": "$(r_home) / « Outfits & buffs — Cecil · wardrobe", "9882": "Own colours $(r_cecil0) — Cecil · wardrobe", "9883": "Crimson $(r_cecil1) — Cecil · wardrobe", "9884": "Midnight $(r_cecil2) — Cecil · wardrobe", "9885": "Bone $(r_cecil3) — Cecil · wardrobe", "9886": "Gilded $(r_cecil4) — Cecil · wardrobe", "9887": "Diamond $(r_cecil5) — Cecil · wardrobe", "9888": "Netherite $(r_cecil6) — Cecil · wardrobe", "9899": "Arcane Corona $(r_aura) — Cecil · wardrobe", "9900": "$(r_home) / « Outfits & buffs — KillerWatt · wardrobe", "9902": "Own colours $(r_kw0) — KillerWatt · wardrobe", "9903": "Midnight $(r_kw1) — KillerWatt · wardrobe", "9904": "Bone $(r_kw2) — KillerWatt · wardrobe", "9905": "Neon $(r_kw3) — KillerWatt · wardrobe", "9906": "Golden Thunder $(r_kw4) — KillerWatt · wardrobe", "9907": "Diamond Thunder $(r_kw5) — KillerWatt · wardrobe", "9908": "Netherite Thunder $(r_kw6) — KillerWatt · wardrobe", "9918": "Pixel costume $(r_px) — KillerWatt · wardrobe", "9919": "Storm Crown $(r_aura) — KillerWatt · wardrobe", "9920": "$(r_home) / « Outfits & buffs — Leo · wardrobe", "9922": "Own clothes $(r_leo0) — Leo · wardrobe", "9923": "Crimson Crusader $(r_leo1) — Leo · wardrobe", "9924": "Royal Purple $(r_leo2) — Leo · wardrobe", "9925": "Greenwood $(r_leo3) — Leo · wardrobe", "9926": "Golden Champion $(r_leo4) — Leo · wardrobe", "9927": "Diamond Champion $(r_leo5) — Leo · wardrobe", "9928": "Netherite Champion $(r_leo6) — Leo · wardrobe", "9939": "Tidal Aegis $(r_aura) — Leo · wardrobe", "9940": "$(r_home) / « Outfits & buffs — Democratus · wardrobe", "9942": "Own clothes $(r_demo0) — Democratus · wardrobe", "9943": "Crimson Reaper $(r_demo1) — Democratus · wardrobe", "9944": "Ashen Shroud $(r_demo2) — Democratus · wardrobe", "9945": "Royal Violet $(r_demo3) — Democratus · wardrobe", "9946": "Gilded Storm $(r_demo4) — Democratus · wardrobe", "9947": "Diamond Storm $(r_demo5) — Democratus · wardrobe", "9948": "Netherite Storm $(r_demo6) — Democratus · wardrobe", "9958": "Pixel costume $(r_px) — Democratus · wardrobe", "9959": "Reaper's Shroud $(r_aura) — Democratus · wardrobe"}, "now": {"1020": "Sealed Explorer's Map 2 Tokens — The Fence - Back Room", "1021": "2 Ominous Trial Keys 2 Medallions — The Fence - Back Room", "1022": "Smuggler's Jar 4 Medallions — The Fence - Back Room", "1040": "Fair Weather Bell 4 Tokens — Old Barnaby - Back Room", "1041": "2 Totems of Undying 2 Medallions — Old Barnaby - Back Room", "1042": "Spawner Crowbar 5 Medallions — Old Barnaby - Back Room", "1060": "Rat Gang Portrait 2 Tokens — Madame Velour - Back Room", "1061": "Donado Trophy 2 Medallions — Madame Velour - Back Room", "1062": "Brass Wing Scroll 1 Trophy — Madame Velour - Back Room", "1080": "16 Spectral Arrows 2 Tokens — Vinny 'Two-Blades' - Back Room", "1081": "Netherite Upgrade Template 2 Medallions — Vinny 'Two-Blades' - Back Room", "1082": "Showstopper Charm 1 Trophy — Vinny 'Two-Blades' - Back Room", "1100": "Lodestone Locket 5 Tokens — Sgt. Steelwhisker - Back Room", "1101": "3 Wither Skeleton Skulls 2 Medallions — Sgt. Steelwhisker - Back Room", "1102": "Market Crest Scroll 1 Trophy — Sgt. Steelwhisker - Back Room", "1120": "A Whole Cake 1 Token — Chef Fromage - Back Room", "1121": "Enchanted Golden Apple 4 Medallions — Chef Fromage - Back Room", "1122": "3 Enchanted Golden Apples 1 Trophy — Chef Fromage - Back Room", "1140": "16 Bottles o' Enchanting 2 Tokens — Prof. Whiskerton - Back Room", "1141": "Book of Mending 2 Medallions — Prof. Whiskerton - Back Room", "1142": "Auroral Crown 1 Trophy — Prof. Whiskerton - Back Room", "1160": "Jackpot Scratch Card 2 Lucky Tokens — Lucky Whiskers - Back Room", "1161": "Heartstone 9 Lucky Tokens — Lucky Whiskers - Back Room", "1162": "Bloomwalker Boots 1 Trophy — Lucky Whiskers - Back Room", "1180": "Buried Treasure Map 2 Tokens — Capt. Cheddarbeard - Back Room", "1181": "Heart of the Sea 2 Medallions — Capt. Cheddarbeard - Back Room", "1182": "Rat Familiar 1 Trophy — Capt. Cheddarbeard - Back Room", "1200": "Ominous Bottle 4 Blood Moon Crystals — The Bloodbroker - Back Room", "1201": "Nether Star 14 Blood Moon Crystals — The Bloodbroker - Back Room", "1202": "3 Heartstones 1 Trophy — The Bloodbroker - Back Room", "2": "Keep at it — Skip this puzzle?, The Fixer's mercy", "2001": "Buy a one-night pass 1 Medallion — The Dark Auction", "2110": "32 Coal → 1 Token $(q0)/5 — DENNIS'S ASSAY OFFICE", "2111": "32 Raw Copper → 1 Token $(q1)/5 — DENNIS'S ASSAY OFFICE", "2112": "24 Raw Iron → 1 Token $(q2)/5 — DENNIS'S ASSAY OFFICE", "2113": "16 Raw Gold → 1 Token $(q3)/4 — DENNIS'S ASSAY OFFICE", "2114": "48 Redstone Dust → 1 Token $(q4)/4 — DENNIS'S ASSAY OFFICE", "2115": "32 Lapis Lazuli → 1 Token $(q5)/4 — DENNIS'S ASSAY OFFICE", "2116": "32 Nether Quartz → 1 Token $(q6)/4 — DENNIS'S ASSAY OFFICE", "2117": "32 Amethyst Shards → 1 Token $(q7)/3 — DENNIS'S ASSAY OFFICE", "2118": "Diamond → 2 Tokens $(q8)/8 — DENNIS'S ASSAY OFFICE", "2119": "2 Ancient Debris → 1 Token $(q9)/4 — DENNIS'S ASSAY OFFICE", "2140": "Buy the Ore Magnet 16 Tokens — DENNIS'S ASSAY OFFICE", "2151": "« Common lots — PISTACHIO'S PANTRY · rare parts", "2152": "Rare parts » — PISTACHIO'S PANTRY", "2160": "32 Rotten Flesh → 1 Token $(q0)/5 — PISTACHIO'S PANTRY", "2161": "32 Bones → 1 Token $(q1)/5 — PISTACHIO'S PANTRY", "2162": "32 String → 1 Token $(q2)/5 — PISTACHIO'S PANTRY", "2163": "16 Spider Eyes → 1 Token $(q3)/4 — PISTACHIO'S PANTRY", "2164": "24 Gunpowder → 1 Token $(q4)/4 — PISTACHIO'S PANTRY", "2165": "16 Slimeballs → 1 Token $(q5)/4 — PISTACHIO'S PANTRY", "2166": "16 Leather → 1 Token $(q6)/4 — PISTACHIO'S PANTRY", "2167": "32 Feathers → 1 Token $(q7)/4 — PISTACHIO'S PANTRY", "2168": "24 Ink Sacs → 1 Token $(q8)/3 — PISTACHIO'S PANTRY", "2169": "8 Ender Pearls → 1 Token $(q9)/3 — PISTACHIO'S PANTRY", "2170": "8 Blaze Rods → 1 Token $(q10)/3 — PISTACHIO'S PANTRY", "2171": "12 Magma Cream → 1 Token $(q11)/3 — PISTACHIO'S PANTRY", "2172": "8 Phantom Membranes → 1 Token $(q12)/3 — PISTACHIO'S PANTRY", "2173": "24 Prismarine Shards → 1 Token $(q13)/3 — PISTACHIO'S PANTRY", "2174": "8 Breeze Rods → 1 Token $(q14)/3 — PISTACHIO'S PANTRY", "2175": "Wither Skeleton Skull → 5 Tokens $(q15)/3 — PISTACHIO'S PANTRY · rare parts", "2176": "Zombie Head → 3 Tokens $(q16)/2 — PISTACHIO'S PANTRY · rare parts", "2177": "Skeleton Skull → 3 Tokens $(q17)/2 — PISTACHIO'S PANTRY · rare parts", "2178": "Creeper Head → 3 Tokens $(q18)/2 — PISTACHIO'S PANTRY · rare parts", "2179": "Shulker Shell → 1 Token $(q19)/2 — PISTACHIO'S PANTRY · rare parts", "2180": "2 Rabbit's Feet → 1 Token $(q20)/2 — PISTACHIO'S PANTRY · rare parts", "2181": "2 Ghast Tears → 1 Token $(q21)/3 — PISTACHIO'S PANTRY · rare parts", "2190": "Buy the Spirit Jar 16 Tokens — PISTACHIO'S PANTRY", "2201": "Sit / follow — Dennis's Horn", "2202": "Wardrobe — Dennis's Horn", "2204": "Dennis's ways — Dennis's Horn", "2205": "« Back — DENNIS'S WAYS", "2208": "Call for Dennis — Dennis's Horn", "2209": "Send him home — Dennis's Horn", "2221": "Sit / follow — Pistachio's Little Cloche", "2222": "Wardrobe — Pistachio's Little Cloche", "2224": "Pistachio's ways — Pistachio's Little Cloche", "2225": "« Back — PISTACHIO'S WAYS", "2228": "Call for Pistachio — Pistachio's Little Cloche", "2229": "Send him home — Pistachio's Little Cloche", "2240": "$(r_home) / « Outfits & buffs — Dennis · wardrobe", "2242": "His old black leather $(r_dennis0) — Dennis · wardrobe", "2243": "Road Brown $(r_dennis1) — Dennis · wardrobe", "2244": "Biker Red $(r_dennis2) — Dennis · wardrobe", "2245": "Forest Leather $(r_dennis3) — Dennis · wardrobe", "2246": "Gilded Jacket $(r_dennis4) — Dennis · wardrobe", "2247": "Diamond Jacket $(r_dennis5) — Dennis · wardrobe", "2248": "Netherite Jacket $(r_dennis6) — Dennis · wardrobe", "2258": "Pixel costume $(r_px) — Dennis · wardrobe", "2259": "Gold Rush Glimmer $(r_aura) — Dennis · wardrobe", "2260": "$(r_home) / « Outfits & buffs — Pistachio · wardrobe", "2262": "His charcoal tails $(r_pistachio0) — Pistachio · wardrobe", "2263": "Midnight Tails $(r_pistachio1) — Pistachio · wardrobe", "2264": "Claret Tails $(r_pistachio2) — Pistachio · wardrobe", "2265": "Ivory Tails $(r_pistachio3) — Pistachio · wardrobe", "2266": "Gilded Tails $(r_pistachio4) — Pistachio · wardrobe", "2267": "Diamond Tails $(r_pistachio5) — Pistachio · wardrobe", "2268": "Netherite Tails $(r_pistachio6) — Pistachio · wardrobe", "2278": "Pixel costume $(r_px) — Pistachio · wardrobe", "2279": "Ectoplasmic Mist $(r_aura) — Pistachio · wardrobe", "2281": "Sit / follow — Omega's Monocle", "2282": "Wardrobe — Omega's Monocle", "2284": "King Omega's ways — Omega's Monocle", "2285": "« Back — KING OMEGA'S WAYS", "2288": "Call for Omega — Omega's Monocle", "2289": "Send him home — Omega's Monocle", "2300": "$(r_home) / « Outfits & buffs — King Omega · wardrobe", "2302": "His own grey ghost $(r_omega0) — King Omega · wardrobe", "2303": "Spectral Blue $(r_omega1) — King Omega · wardrobe", "2304": "Blood Moon $(r_omega2) — King Omega · wardrobe", "2305": "Verdant Wraith $(r_omega3) — King Omega · wardrobe", "2306": "Gilded King $(r_omega4) — King Omega · wardrobe", "2307": "Diamond King $(r_omega5) — King Omega · wardrobe", "2308": "Netherite King $(r_omega6) — King Omega · wardrobe", "2318": "Pixel costume $(r_px) — King Omega · wardrobe", "2319": "Court of Souls $(r_aura) — King Omega · wardrobe", "2321": "The Peerage — KING OMEGA", "2322": "The Ghost Garrison — KING OMEGA", "2323": "Offer a gift — KING OMEGA", "2324": "The Chronicle — KING OMEGA", "2325": "My title on / off — KING OMEGA", "2326": "Re-challenge the King — KING OMEGA", "2329": "« Back — THE GHOST GARRISON, THE PEERAGE, p169/court/chron", "2331": "Tithe 4 Tokens +10 — THE PEERAGE", "2332": "Offer your Court's souls — THE PEERAGE", "2341": "Buy a Soul Brazier 8 Tokens — THE GHOST GARRISON", "2350": "I. Two Eggs in the Sun — p169/court/chron", "2351": "II. The Monocle — p169/court/chron", "2352": "III. The Feast of Crowns — p169/court/chron", "2353": "IV. The Library of Small Things — p169/court/chron", "2354": "V. The Light to Lead Them — p169/court/chron", "2355": "VI. The War of Brothers — p169/court/chron", "2356": "VII. The Last Night — p169/court/chron", "2357": "VIII. The Long Quiet — p169/court/chron", "2358": "IX. The Butler and the Boy — p169/court/chron", "2359": "X. What the Dead King Wants — p169/court/chron", "2361": "Call him over — Wilfrey's Locket", "2362": "Send him home — Wilfrey's Locket", "2363": "Wardrobe — Wilfrey's Locket", "2364": "Call Wilfrey — Wilfrey's Locket", "2370": "Back after a faint $(r_ar) — Cecil · wardrobe", "2371": "Back after a faint $(r_ar) — Emma · wardrobe", "2372": "Back after a faint $(r_ar) — Celi · wardrobe", "2373": "Back after a faint $(r_ar) — Zib · wardrobe", "2374": "Back after a faint $(r_ar) — KillerWatt · wardrobe", "2375": "Back after a faint $(r_ar) — Leo · wardrobe", "2376": "Back after a faint $(r_ar) — Democratus · wardrobe", "2377": "Back after a faint $(r_ar) — Apophiss · wardrobe", "2378": "Back after a faint $(r_ar) — Tullius · wardrobe", "2379": "Back after a faint $(r_ar) — the Frog with Mustache · wardrobe", "2380": "Back after a faint $(r_ar) — Donado · wardrobe", "2381": "Back after a faint $(r_ar) — Wilfrey · wardrobe", "2382": "Back after a faint $(r_ar) — Fishy · wardrobe", "2383": "Back after a faint $(r_ar) — Dennis · wardrobe", "2384": "Back after a faint $(r_ar) — Pistachio · wardrobe", "2385": "Back after a faint $(r_ar) — King Omega · wardrobe", "2386": "Back after a faint $(r_ar) — Ashur · wardrobe", "2387": "Back after a faint $(r_ar) — the Chef · wardrobe", "2388": "Back after a faint $(r_ar) — the Neighbor · wardrobe", "2389": "Back after a faint $(r_ar) — Queen Ava · wardrobe", "2390": "Back after a faint $(r_ar) — Queen Pearl · wardrobe", "2391": "Back after a faint $(r_ar) — Bloo · wardrobe", "2392": "Back after a faint $(r_ar) — The Stalker · wardrobe", "2393": "Back after a faint $(r_ar) — The Arachno-Lantern · wardrobe", "2394": "Back after a faint $(r_ar) — Bender · wardrobe", "2395": "Back after a faint $(r_ar) — Bones · wardrobe", "2396": "Back after a faint $(r_ar) — Mr. Capshun · wardrobe", "2397": "Back after a faint $(r_ar) — 8-Bit Cecil · wardrobe", "2398": "Back after a faint $(r_ar) — 8-Bit Leo · wardrobe", "2399": "Back after a faint $(r_ar) — 8-Bit Emma · wardrobe", "2400": "Back after a faint $(r_ar) — The Sky Buddies · wardrobe", "2401": "Old Barnaby — WHO'S WHERE · the rat town", "2402": "Prof. Whiskerton — WHO'S WHERE · the rat town", "2403": "Madame Velour — WHO'S WHERE · the rat town", "2404": "The Fence — WHO'S WHERE · the rat town", "2405": "Dark Auction gate — WHO'S WHERE · the rat town", "2406": "Gilded Gutter gate — WHO'S WHERE · the rat town", "2407": "Scrap Bin — WHO'S WHERE · the rat town", "2408": "Bounty Board — WHO'S WHERE · the rat town", "2409": "Mike's pond — WHO'S WHERE · the rat town", "2410": "Vinny 'Two-Blades' — WHO'S WHERE · the rat town", "2411": "Steelwhisker — WHO'S WHERE · the rat town", "2412": "Fishy's Cabinet — WHO'S WHERE · the rat town", "2413": "Chef Fromage — WHO'S WHERE · the rat town", "2414": "Cecil — WHO'S WHERE · the rat town", "2415": "The Bloodbroker — WHO'S WHERE · the rat town", "2416": "Lucky Whiskers — WHO'S WHERE · the rat town", "2417": "The dock house — WHO'S WHERE · the rat town", "2418": "Dennis — WHO'S WHERE · the rat town", "2419": "Pistachio — WHO'S WHERE · the rat town", "2420": "Newcomers' Book — WHO'S WHERE · the rat town", "2421": "The way out — WHO'S WHERE · the rat town", "2441": "Sit / follow — Ashur's Cinder", "2442": "Wardrobe — Ashur's Cinder", "2444": "Ashur's ways — Ashur's Cinder", "2445": "« Back — ASHUR'S WAYS", "2448": "Call for Ashur — Ashur's Cinder", "2449": "Send her home — Ashur's Cinder", "2460": "$(r_home) / « Outfits & buffs — Ashur · wardrobe", "2462": "Her own magma $(r_ashur0) — Ashur · wardrobe", "2463": "Blue Flame $(r_ashur1) — Ashur · wardrobe", "2464": "Verdant Ember $(r_ashur2) — Ashur · wardrobe", "2465": "Obsidian Rose $(r_ashur3) — Ashur · wardrobe", "2466": "Gilded Magma $(r_ashur4) — Ashur · wardrobe", "2467": "Diamond Magma $(r_ashur5) — Ashur · wardrobe", "2468": "Netherite Magma $(r_ashur6) — Ashur · wardrobe", "2478": "Pixel costume $(r_px) — Ashur · wardrobe", "2479": "Ashfall Crown $(r_aura) — Ashur · wardrobe", "2501": "Sit / follow — The Golden Ladle", "2502": "Wardrobe — The Golden Ladle", "2504": "The Chef's ways — The Golden Ladle", "2505": "« Back — THE CHEF'S WAYS", "2508": "Call for The Chef — The Golden Ladle", "2509": "Send him home — The Golden Ladle", "2520": "$(r_home) / « Outfits & buffs — the Chef · wardrobe", "2522": "His spotless whites $(r_chef0) — the Chef · wardrobe", "2523": "Midnight Brigade $(r_chef1) — the Chef · wardrobe", "2524": "Bistro Blue $(r_chef2) — the Chef · wardrobe", "2525": "Sommelier Wine $(r_chef3) — the Chef · wardrobe", "2526": "Gilded Whites $(r_chef4) — the Chef · wardrobe", "2527": "Diamond Whites $(r_chef5) — the Chef · wardrobe", "2528": "Netherite Whites $(r_chef6) — the Chef · wardrobe", "2538": "Pixel costume $(r_px) — the Chef · wardrobe", "2539": "Kitchen Steam $(r_aura) — the Chef · wardrobe", "2541": "Sit / follow — The Neighbor's Baton", "2542": "Wardrobe — The Neighbor's Baton", "2544": "The Neighbor's ways — The Neighbor's Baton", "2545": "« Back — THE NEIGHBOR'S WAYS", "2548": "Call for The Neighbor — The Neighbor's Baton", "2549": "Send him home — The Neighbor's Baton", "2560": "$(r_home) / « Outfits & buffs — the Neighbor · wardrobe", "2562": "His sailor whites $(r_neighbor0) — the Neighbor · wardrobe", "2563": "Navy Bandmaster $(r_neighbor1) — the Neighbor · wardrobe", "2564": "Encore Crimson $(r_neighbor2) — the Neighbor · wardrobe", "2565": "Jazz Violet $(r_neighbor3) — the Neighbor · wardrobe", "2566": "Gilded Suit $(r_neighbor4) — the Neighbor · wardrobe", "2567": "Diamond Suit $(r_neighbor5) — the Neighbor · wardrobe", "2568": "Netherite Suit $(r_neighbor6) — the Neighbor · wardrobe", "2578": "Pixel costume $(r_px) — the Neighbor · wardrobe", "2579": "Grand Symphony $(r_aura) — the Neighbor · wardrobe", "2581": "Sit / follow — Queen Ava's Locket", "2582": "Wardrobe — Queen Ava's Locket", "2583": "Living / ghostly form — Queen Ava's Locket", "2584": "Queen Ava's ways — Queen Ava's Locket", "2585": "« Back — QUEEN AVA'S STORY, QUEEN AVA'S WAYS", "2586": "Her story — Queen Ava's Locket", "2588": "Call for Queen Ava — Queen Ava's Locket", "2589": "Send her home — Queen Ava's Locket", "2601": "Sit / follow — Queen Pearl's Pearls", "2602": "Wardrobe — Queen Pearl's Pearls", "2603": "Casual / regal outfit — Queen Pearl's Pearls", "2604": "Queen Pearl's ways — Queen Pearl's Pearls", "2605": "« Back — QUEEN PEARL'S STORY, QUEEN PEARL'S WAYS", "2606": "Her story — Queen Pearl's Pearls", "2608": "Call for Queen Pearl — Queen Pearl's Pearls", "2609": "Send her home — Queen Pearl's Pearls", "2621": "Sit / follow — Bloo's Claw", "2622": "Wardrobe — Bloo's Claw", "2624": "Bloo's ways — Bloo's Claw", "2625": "« Back — BLOO'S STORY, BLOO'S WAYS", "2626": "His story — Bloo's Claw", "2628": "Call for Bloo — Bloo's Claw", "2629": "Send him home — Bloo's Claw", "2640": "$(r_home) / « Outfits & buffs — Queen Ava · wardrobe", "2642": "Her royal blue $(r_ava0) — Queen Ava · wardrobe", "2643": "Coral Reef $(r_ava1) — Queen Ava · wardrobe", "2644": "Abyssal Violet $(r_ava2) — Queen Ava · wardrobe", "2645": "Kelp Forest $(r_ava3) — Queen Ava · wardrobe", "2646": "Gilded Gown $(r_ava4) — Queen Ava · wardrobe", "2647": "Diamond Gown $(r_ava5) — Queen Ava · wardrobe", "2648": "Netherite Gown $(r_ava6) — Queen Ava · wardrobe", "2658": "Pixel costume $(r_px) — Queen Ava · wardrobe", "2659": "Crown of the Deep $(r_aura) — Queen Ava · wardrobe", "2660": "$(r_home) / « Outfits & buffs — Queen Pearl · wardrobe", "2662": "Her own aqua $(r_pearlq0) — Queen Pearl · wardrobe", "2663": "Coral Pink $(r_pearlq1) — Queen Pearl · wardrobe", "2664": "Sunset Gold $(r_pearlq2) — Queen Pearl · wardrobe", "2665": "Starlit Navy $(r_pearlq3) — Queen Pearl · wardrobe", "2666": "Gilded Dress $(r_pearlq4) — Queen Pearl · wardrobe", "2667": "Diamond Dress $(r_pearlq5) — Queen Pearl · wardrobe", "2668": "Netherite Dress $(r_pearlq6) — Queen Pearl · wardrobe", "2678": "Pixel costume $(r_px) — Queen Pearl · wardrobe", "2679": "Pearlescent Tide $(r_aura) — Queen Pearl · wardrobe", "2680": "$(r_home) / « Outfits & buffs — Bloo · wardrobe", "2682": "His own wild blue $(r_bloo0) — Bloo · wardrobe", "2683": "Shadow Pelt $(r_bloo1) — Bloo · wardrobe", "2684": "Ember Mane $(r_bloo2) — Bloo · wardrobe", "2685": "Frost Coat $(r_bloo3) — Bloo · wardrobe", "2686": "Gilded Fur $(r_bloo4) — Bloo · wardrobe", "2687": "Diamond Fur $(r_bloo5) — Bloo · wardrobe", "2688": "Netherite Fur $(r_bloo6) — Bloo · wardrobe", "2698": "Pixel costume $(r_px) — Bloo · wardrobe", "2699": "Feral Moon $(r_aura) — Bloo · wardrobe", "2701": "Sit / follow — The Hollow Hook", "2702": "Wardrobe — The Hollow Hook", "2704": "The Stalker's ways — The Hollow Hook", "2705": "« Back — THE STALKER'S WAYS", "2708": "Call for The Stalker — The Hollow Hook", "2709": "Send it home — The Hollow Hook", "2720": "$(r_home) / « Outfits & buffs — The Stalker · wardrobe", "2722": "Its own sickly olive $(r_stalker0) — The Stalker · wardrobe", "2723": "Bone White $(r_stalker1) — The Stalker · wardrobe", "2724": "Ashen Grey $(r_stalker2) — The Stalker · wardrobe", "2725": "Blood Moon $(r_stalker3) — The Stalker · wardrobe", "2726": "Gilded Skin $(r_stalker4) — The Stalker · wardrobe", "2727": "Diamond Skin $(r_stalker5) — The Stalker · wardrobe", "2728": "Netherite Skin $(r_stalker6) — The Stalker · wardrobe", "2738": "Pixel costume $(r_px) — The Stalker · wardrobe", "2739": "The Long Night $(r_aura) — The Stalker · wardrobe", "2741": "Sit / follow — Kindled Gourd", "2742": "Wardrobe — Kindled Gourd", "2744": "The Arachno-Lantern's ways — Kindled Gourd", "2745": "« Back — THE ARACHNO-LANTERN'S WAYS", "2746": "Ride — Kindled Gourd", "2748": "Call for The Arachno-Lantern — Kindled Gourd", "2749": "Send it home — Kindled Gourd", "2760": "$(r_home) / « Outfits & buffs — The Arachno-Lantern · wardrobe", "2762": "Its own pumpkin orange $(r_lantern0) — The Arachno-Lantern · wardrobe", "2763": "Ghost Gourd $(r_lantern1) — The Arachno-Lantern · wardrobe", "2764": "Soulfire Rind $(r_lantern2) — The Arachno-Lantern · wardrobe", "2765": "Harvest Moon $(r_lantern3) — The Arachno-Lantern · wardrobe", "2766": "Gilded Rind $(r_lantern4) — The Arachno-Lantern · wardrobe", "2767": "Diamond Rind $(r_lantern5) — The Arachno-Lantern · wardrobe", "2768": "Netherite Rind $(r_lantern6) — The Arachno-Lantern · wardrobe", "2778": "Pixel costume $(r_px) — The Arachno-Lantern · wardrobe", "2779": "Hallowfire $(r_aura) — The Arachno-Lantern · wardrobe", "2781": "Sit / follow — Bender's Ball", "2782": "Wardrobe — Bender's Ball", "2784": "Bender's ways — Bender's Ball", "2785": "« Back — BENDER'S WAYS", "2786": "Dig! — Bender's Ball", "2787": "Sniff out treasure — Bender's Ball", "2788": "Call for Bender — Bender's Ball", "2789": "Send him home — Bender's Ball", "2800": "$(r_home) / « Outfits & buffs — Bender · wardrobe", "2802": "His own fawn $(r_bender0) — Bender · wardrobe", "2803": "Midnight Black $(r_bender1) — Bender · wardrobe", "2804": "Snow White $(r_bender2) — Bender · wardrobe", "2805": "Sable $(r_bender3) — Bender · wardrobe", "2806": "Gilded Coat $(r_bender4) — Bender · wardrobe", "2807": "Diamond Coat $(r_bender5) — Bender · wardrobe", "2808": "Netherite Coat $(r_bender6) — Bender · wardrobe", "2818": "Pixel costume $(r_px) — Bender · wardrobe", "2819": "Goodest Boy $(r_aura) — Bender · wardrobe", "2821": "Sit / follow — Bones's Whistle", "2822": "Wardrobe — Bones's Whistle", "2824": "Bones' ways — Bones's Whistle", "2825": "« Back — BONES' WAYS", "2826": "Ride — Bones's Whistle", "2828": "Call for Bones — Bones's Whistle", "2829": "Send him home — Bones's Whistle", "2840": "$(r_home) / « Outfits & buffs — Bones · wardrobe", "2842": "His own shark grey $(r_bones0) — Bones · wardrobe", "2843": "Great White $(r_bones1) — Bones · wardrobe", "2844": "Hammerhead Bronze $(r_bones2) — Bones · wardrobe", "2845": "Abyss Black $(r_bones3) — Bones · wardrobe", "2846": "Gilded Skin $(r_bones4) — Bones · wardrobe", "2847": "Diamond Skin $(r_bones5) — Bones · wardrobe", "2848": "Netherite Skin $(r_bones6) — Bones · wardrobe", "2858": "Pixel costume $(r_px) — Bones · wardrobe", "2859": "Abyssal Tide $(r_aura) — Bones · wardrobe", "2861": "Sit / follow — Mr. Capshun's Pencil", "2862": "Wardrobe — Mr. Capshun's Pencil", "2864": "Mr. Capshun's ways — Mr. Capshun's Pencil", "2865": "« Back — MR. CAPSHUN'S PALETTE, MR. CAPSHUN'S WAYS", "2866": "Palette — Mr. Capshun's Pencil", "2867": "The story so far — Mr. Capshun's Pencil", "2868": "Call for Mr. Capshun — Mr. Capshun's Pencil", "2869": "Send him home — Mr. Capshun's Pencil", "2870": "Red — MR. CAPSHUN'S PALETTE", "2871": "Orange — MR. CAPSHUN'S PALETTE", "2872": "Yellow — MR. CAPSHUN'S PALETTE", "2873": "Green — MR. CAPSHUN'S PALETTE", "2874": "Blue — MR. CAPSHUN'S PALETTE", "2875": "Purple — MR. CAPSHUN'S PALETTE", "2876": "Rainbow — MR. CAPSHUN'S PALETTE", "2880": "$(r_home) / « Outfits & buffs — Mr. Capshun · wardrobe", "2882": "Plain black ink $(r_capshun0) — Mr. Capshun · wardrobe", "2883": "Blue Ballpoint $(r_capshun1) — Mr. Capshun · wardrobe", "2884": "Red Pen $(r_capshun2) — Mr. Capshun · wardrobe", "2885": "Green Marker $(r_capshun3) — Mr. Capshun · wardrobe", "2886": "Gilded Ink $(r_capshun4) — Mr. Capshun · wardrobe", "2887": "Diamond Ink $(r_capshun5) — Mr. Capshun · wardrobe", "2888": "Netherite Ink $(r_capshun6) — Mr. Capshun · wardrobe", "2898": "Pixel costume $(r_px) — Mr. Capshun · wardrobe", "2899": "Rainbow Doodles $(r_aura) — Mr. Capshun · wardrobe", "2900": "$(r_home) / « Outfits & buffs — The Sky Buddies · wardrobe", "2902": "Snooze's old blue $(r_sky0) — The Sky Buddies · wardrobe", "2903": "Bubblegum Pink $(r_sky1) — The Sky Buddies · wardrobe", "2904": "Mint Dream $(r_sky2) — The Sky Buddies · wardrobe", "2905": "Lavender Night $(r_sky3) — The Sky Buddies · wardrobe", "2906": "Gilded Nightcap $(r_sky4) — The Sky Buddies · wardrobe", "2907": "Diamond Nightcap $(r_sky5) — The Sky Buddies · wardrobe", "2908": "Netherite Nightcap $(r_sky6) — The Sky Buddies · wardrobe", "2918": "Pixel costume $(r_px) — The Sky Buddies · wardrobe", "2919": "Starry Sky $(r_aura) — The Sky Buddies · wardrobe", "2941": "Sit / follow — The Sky Mobile", "2942": "Wardrobe — The Sky Mobile", "2943": "A bed on Nimbus — The Sky Mobile", "2944": "The Sky Buddies' ways — The Sky Mobile", "2945": "« Back — THE SKY BUDDIES' WAYS", "2946": "Today's forecast — The Sky Mobile", "2947": "Change the weather — The Sky Mobile", "2948": "Call for The Sky Buddies — The Sky Mobile", "2949": "Send them home — The Sky Mobile", "2950": "Clear skies — THE SKY, YOURS", "2951": "Rain — THE SKY, YOURS", "2952": "Thunderstorm — THE SKY, YOURS", "2953": "« Back — THE SKY, YOURS", "2960": "$(r_home) / « Outfits & buffs — 8-Bit Emma · wardrobe", "2962": "Sixteen colours $(r_pxemma0) — 8-Bit Emma · wardrobe", "2963": "Game Boy $(r_pxemma1) — 8-Bit Emma · wardrobe", "2964": "Virtual Boy $(r_pxemma2) — 8-Bit Emma · wardrobe", "2965": "Sepia Print $(r_pxemma3) — 8-Bit Emma · wardrobe", "2966": "Gilded Pixels $(r_pxemma4) — 8-Bit Emma · wardrobe", "2967": "Diamond Pixels $(r_pxemma5) — 8-Bit Emma · wardrobe", "2968": "Netherite Pixels $(r_pxemma6) — 8-Bit Emma · wardrobe", "2979": "Scanlines $(r_aura) — 8-Bit Emma · wardrobe", "2981": "Sit / follow — 8-Bit Emma's Cartridge", "2982": "Wardrobe — 8-Bit Emma's Cartridge", "2984": "8-Bit Emma's ways — 8-Bit Emma's Cartridge", "2985": "« Back — 8-BIT EMMA'S WAYS", "2988": "Call for 8-Bit Emma — 8-Bit Emma's Cartridge", "2989": "Send her home — 8-Bit Emma's Cartridge", "3000": "$(r_home) / « Outfits & buffs — 8-Bit Leo · wardrobe", "3002": "Sixteen colours $(r_pxleo0) — 8-Bit Leo · wardrobe", "3003": "Game Boy $(r_pxleo1) — 8-Bit Leo · wardrobe", "3004": "Virtual Boy $(r_pxleo2) — 8-Bit Leo · wardrobe", "3005": "Sepia Print $(r_pxleo3) — 8-Bit Leo · wardrobe", "3006": "Gilded Pixels $(r_pxleo4) — 8-Bit Leo · wardrobe", "3007": "Diamond Pixels $(r_pxleo5) — 8-Bit Leo · wardrobe", "3008": "Netherite Pixels $(r_pxleo6) — 8-Bit Leo · wardrobe", "3019": "Scanlines $(r_aura) — 8-Bit Leo · wardrobe", "3021": "Sit / follow — 8-Bit Leo's Cartridge", "3022": "Wardrobe — 8-Bit Leo's Cartridge", "3024": "8-Bit Leo's ways — 8-Bit Leo's Cartridge", "3025": "« Back — 8-BIT LEO'S WAYS", "3028": "Call for 8-Bit Leo — 8-Bit Leo's Cartridge", "3029": "Send him home — 8-Bit Leo's Cartridge", "3040": "$(r_home) / « Outfits & buffs — 8-Bit Cecil · wardrobe", "3042": "Sixteen colours $(r_pxcecil0) — 8-Bit Cecil · wardrobe", "3043": "Game Boy $(r_pxcecil1) — 8-Bit Cecil · wardrobe", "3044": "Virtual Boy $(r_pxcecil2) — 8-Bit Cecil · wardrobe", "3045": "Sepia Print $(r_pxcecil3) — 8-Bit Cecil · wardrobe", "3046": "Gilded Pixels $(r_pxcecil4) — 8-Bit Cecil · wardrobe", "3047": "Diamond Pixels $(r_pxcecil5) — 8-Bit Cecil · wardrobe", "3048": "Netherite Pixels $(r_pxcecil6) — 8-Bit Cecil · wardrobe", "3059": "Scanlines $(r_aura) — 8-Bit Cecil · wardrobe", "3061": "Sit / follow — 8-Bit Cecil's Cartridge", "3062": "Wardrobe — 8-Bit Cecil's Cartridge", "3064": "8-Bit Cecil's ways — 8-Bit Cecil's Cartridge", "3065": "« Back — 8-BIT CECIL'S WAYS", "3068": "Call for 8-Bit Cecil — 8-Bit Cecil's Cartridge", "3069": "Send him home — 8-Bit Cecil's Cartridge", "3100": "Open the bidding — The Dark Auction", "3101": "Bid +1 — The Dark Auction", "3102": "Bid +2 — The Dark Auction", "3105": "Bid +5 — The Dark Auction", "3110": "Bid +10 — The Dark Auction", "3202": "Tuning — VESPER'S STOCK BOOK · the Dread Broker", "3203": "Reforging — VESPER'S STOCK BOOK · the Dread Broker", "3204": "About the Dread — VESPER'S STOCK BOOK · the Dread Broker", "3205": "Reforge what I hold — Reforging · past the old maximum", "3209": "« The Ledger — About the Dread, Reforging · past the old maximum, Tuning · a tool, Tuning · a weapon, Tuning · an armour piece", "3220": "Attack Damage +0.75 (max 3) — Tuning · a weapon", "3221": "Swing Speed +0.1 (max 3) — Tuning · a weapon", "3222": "Reach +0.25 (max 2) — Tuning · a weapon", "3223": "Luck +1 (max 2) — Tuning · a weapon", "3224": "Unbind all tunings (every token back) — Tuning · a weapon", "3225": "Mining Speed +10% (max 3) — Tuning · a tool", "3226": "Mining Efficiency +3 (max 2) — Tuning · a tool", "3227": "Block Reach +0.5 (max 2) — Tuning · a tool", "3228": "Luck +1 (max 2) — Tuning · a tool", "3229": "Unbind all tunings (every token back) — Tuning · a tool", "3230": "Armor +1 (max 2) — Tuning · an armour piece", "3231": "Toughness +1 (max 2) — Tuning · an armour piece", "3232": "Max Health +1 (max 2) — Tuning · an armour piece", "3233": "Knockback Resistance +0.05 (max 2) — Tuning · an armour piece", "3234": "Speed (boots) +2% (max 2) — Tuning · an armour piece", "3235": "Unbind all tunings (every token back) — Tuning · an armour piece", "3301": "Lamplighters' Fund $(p0)/250$(s0) — Community Pots · The Rat Bank", "3302": "Harvest Guild $(p1)/300$(s1) — Community Pots · The Rat Bank", "3303": "Miners' Union $(p2)/400$(s2) — Community Pots · The Rat Bank", "3304": "Couriers' Guild $(p3)/400$(s3) — Community Pots · The Rat Bank", "3305": "Hearth Fund $(p4)/500$(s4) — Community Pots · The Rat Bank", "3306": "Bounty Office $(p5)/600$(s5) — Community Pots · The Rat Bank", "3309": "« Your account — Community Pots · The Rat Bank", "3310": "Give 10 Tokens — Lamplighters' Fund · Community Pots", "3311": "Give 10 Tokens — Harvest Guild · Community Pots", "3312": "Give 10 Tokens — Miners' Union · Community Pots", "3313": "Give 10 Tokens — Couriers' Guild · Community Pots", "3314": "Give 10 Tokens — Hearth Fund · Community Pots", "3315": "Give 10 Tokens — Bounty Office · Community Pots", "3320": "Give 50 Tokens — Lamplighters' Fund · Community Pots", "3321": "Give 50 Tokens — Harvest Guild · Community Pots", "3322": "Give 50 Tokens — Miners' Union · Community Pots", "3323": "Give 50 Tokens — Couriers' Guild · Community Pots", "3324": "Give 50 Tokens — Hearth Fund · Community Pots", "3325": "Give 50 Tokens — Bounty Office · Community Pots", "3330": "Switch it on / off — Lamplighters' Fund · Community Pots", "3331": "Switch it on / off — Harvest Guild · Community Pots", "3332": "Switch it on / off — Miners' Union · Community Pots", "3333": "Switch it on / off — Couriers' Guild · Community Pots", "3334": "Switch it on / off — Hearth Fund · Community Pots", "3335": "Switch it on / off — Bounty Office · Community Pots", "3340": "« The pots — Bounty Office · Community Pots, Couriers' Guild · Community Pots, Harvest Guild · Community Pots, Hearth Fund · Community Pots, Lamplighters' Fund · Community Pots, Miners' Union · Community Pots", "3351": "Keep up: off / Keep up: on — p179/w/open", "3352": "❖ Gallery — p179/w/open", "3353": "◈ View in 3D: #01-#08 — Follower Gallery", "3354": "◈ View in 3D: #09-#16 — Follower Gallery", "3355": "◈ View in 3D: #17-#24 — Follower Gallery", "3356": "◈ View in 3D: #25-#32 — Follower Gallery", "3359": "« Partner Wheel — Follower Gallery", "3360": "Call Emma / Send Emma home — p179/w/row0", "3361": "Call Celi / Send Celi home — p179/w/row1", "3362": "Call Zib / Send Zib home — p179/w/row2", "3363": "Call Cecil / Send Cecil home — p179/w/row3", "3364": "Call KillerWatt / Send KillerWatt home — p179/w/row4", "3365": "Call Leo / Send Leo home — p179/w/row5", "3366": "Call Democratus / Send Democratus home — p179/w/row6", "3367": "Call Apophiss / Send Apophiss home — p179/w/row7", "3368": "Call Tullius / Send Tullius home — p179/w/row8", "3369": "Call the Frog / Send the Frog home — p179/w/row9", "3370": "Call Donado / Send Donado home — p179/w/row10", "3371": "Call Pearlman / Send Pearlman home — p179/w/row11", "3372": "Call Wilfrey / Send Wilfrey home — p179/w/row12", "3373": "Call Fishy / Send Fishy home — p179/w/row13", "3374": "Call Dennis / Send Dennis home — p179/w/row14", "3375": "Call Pistachio / Send Pistachio home — p179/w/row15", "3376": "Call King Omega / Send King Omega home — p179/w/row16", "3377": "Call Ashur / Send Ashur home — p179/w/row17", "3378": "Call the Chef / Send the Chef home — p179/w/row18", "3379": "Call the Neighbor / Send the Neighbor home — p179/w/row19", "3380": "Call Queen Ava / Send Queen Ava home — p179/w/row20", "3381": "Call Queen Pearl / Send Queen Pearl home — p179/w/row21", "3382": "Call Bloo / Send Bloo home — p179/w/row22", "3383": "Call The Stalker / Send The Stalker home — p179/w/row23", "3384": "Call The Arachno-Lantern / Send The Arachno-Lantern home — p179/w/row24", "3385": "Call Bender / Send Bender home — p179/w/row25", "3386": "Call Bones / Send Bones home — p179/w/row26", "3387": "Call Mr. Capshun / Send Mr. Capshun home — p179/w/row27", "3388": "Call 8-Bit Cecil / Send 8-Bit Cecil home — p179/w/row28", "3389": "Call 8-Bit Leo / Send 8-Bit Leo home — p179/w/row29", "3390": "Take the item back — p179/w/row0", "3391": "Take the item back — p179/w/row1", "3392": "Take the item back — p179/w/row2", "3393": "Take the item back — p179/w/row3", "3394": "Take the item back — p179/w/row4", "3395": "Take the item back — p179/w/row5", "3396": "Take the item back — p179/w/row6", "3397": "Take the item back — p179/w/row7", "3398": "Take the item back — p179/w/row8", "3399": "Take the item back — p179/w/row9", "3400": "Take the item back — p179/w/row10", "3401": "Take the item back — p179/w/row11", "3402": "Take the item back — p179/w/row12", "3403": "Take the item back — p179/w/row13", "3404": "Take the item back — p179/w/row14", "3405": "Take the item back — p179/w/row15", "3406": "Take the item back — p179/w/row16", "3407": "Take the item back — p179/w/row17", "3408": "Take the item back — p179/w/row18", "3409": "Take the item back — p179/w/row19", "3410": "Take the item back — p179/w/row20", "3411": "Take the item back — p179/w/row21", "3412": "Take the item back — p179/w/row22", "3413": "Take the item back — p179/w/row23", "3414": "Take the item back — p179/w/row24", "3415": "Take the item back — p179/w/row25", "3416": "Take the item back — p179/w/row26", "3417": "Take the item back — p179/w/row27", "3418": "Take the item back — p179/w/row28", "3419": "Take the item back — p179/w/row29", "3420": "Launch your Skiff Escort / Send your Skiff Escort home — p184/wesc/row", "3421": "Take the escort back — p184/wesc/row", "3450": "⚙ Menu — p179/w/row0", "3451": "⚙ Menu — p179/w/row1", "3452": "⚙ Menu — p179/w/row2", "3453": "⚙ Menu — p179/w/row3", "3454": "⚙ Menu — p179/w/row4", "3455": "⚙ Menu — p179/w/row5", "3456": "⚙ Menu — p179/w/row6", "3457": "⚙ Menu — p179/w/row7", "3458": "⚙ Menu — p179/w/row8", "3459": "⚙ Menu — p179/w/row9", "3460": "⚙ Menu — p179/w/row10", "3461": "⚙ Menu — p179/w/row11", "3462": "⚙ Menu — p179/w/row12", "3463": "⚙ Menu — p179/w/row13", "3464": "⚙ Menu — p179/w/row14", "3465": "⚙ Menu — p179/w/row15", "3466": "⚙ Menu — p179/w/row16", "3467": "⚙ Menu — p179/w/row17", "3468": "⚙ Menu — p179/w/row18", "3469": "⚙ Menu — p179/w/row19", "3470": "⚙ Menu — p179/w/row20", "3471": "⚙ Menu — p179/w/row21", "3472": "⚙ Menu — p179/w/row22", "3473": "⚙ Menu — p179/w/row23", "3474": "⚙ Menu — p179/w/row24", "3475": "⚙ Menu — p179/w/row25", "3476": "⚙ Menu — p179/w/row26", "3477": "⚙ Menu — p179/w/row27", "3478": "⚙ Menu — p179/w/row28", "3479": "⚙ Menu — p179/w/row29", "3480": "Dynamic — Pearlman's Seasons", "3481": "Off - his own colours — Pearlman's Seasons", "3482": "Fall / Fall (locked) — Pearlman's Seasons", "3483": "Christmas / Christmas (locked) — Pearlman's Seasons", "3484": "Easter / Easter (locked) — Pearlman's Seasons", "3485": "Summer / Summer (locked) — Pearlman's Seasons", "3600": "Gilded Pixels $(r_182) — 8-BIT EMMA · the Tailor", "3601": "Diamond Pixels $(r_183) — 8-BIT EMMA · the Tailor", "3602": "Netherite Pixels $(r_184) — 8-BIT EMMA · the Tailor", "3603": "Game Boy $(r_185) — 8-BIT LEO · the Tailor", "3604": "Virtual Boy $(r_186) — 8-BIT LEO · the Tailor", "3605": "Sepia Print $(r_187) — 8-BIT LEO · the Tailor", "3606": "Gilded Pixels $(r_188) — 8-BIT LEO · the Tailor", "3607": "Diamond Pixels $(r_189) — 8-BIT LEO · the Tailor", "3608": "Netherite Pixels $(r_190) — 8-BIT LEO · the Tailor", "3609": "Game Boy $(r_191) — 8-BIT CECIL · the Tailor", "3610": "Virtual Boy $(r_192) — 8-BIT CECIL · the Tailor", "3611": "Sepia Print $(r_193) — 8-BIT CECIL · the Tailor", "3612": "Gilded Pixels $(r_194) — 8-BIT CECIL · the Tailor", "3613": "Diamond Pixels $(r_195) — 8-BIT CECIL · the Tailor", "3614": "Netherite Pixels $(r_196) — 8-BIT CECIL · the Tailor", "3615": "Blue Ballpoint $(r_197) — MR. CAPSHUN · the Tailor", "3616": "Red Pen $(r_198) — MR. CAPSHUN · the Tailor", "3617": "Green Marker $(r_199) — MR. CAPSHUN · the Tailor", "3618": "Gilded Ink $(r_200) — MR. CAPSHUN · the Tailor", "3619": "Diamond Ink $(r_201) — MR. CAPSHUN · the Tailor", "3620": "Netherite Ink $(r_202) — MR. CAPSHUN · the Tailor", "3700": "Call 8-Bit Emma / Send 8-Bit Emma home — p179/w/row30", "3701": "Call The Sky Buddies / Send The Sky Buddies home — p179/w/row31", "3740": "Take the item back — p179/w/row30", "3741": "Take the item back — p179/w/row31", "3780": "⚙ Menu — p179/w/row30", "3781": "⚙ Menu — p179/w/row31", "4010": "Deposit all Tokens ($(h)) — Tokens · The Rat Bank", "4011": "Take 1 — Tokens · The Rat Bank", "4012": "Take 10 — Tokens · The Rat Bank", "4013": "Take all ($(n)) — Tokens · The Rat Bank", "4014": "Deposit all Lucky Tokens ($(h)) — Lucky Tokens · The Rat Bank", "4015": "Take 1 — Lucky Tokens · The Rat Bank", "4016": "Take 10 — Lucky Tokens · The Rat Bank", "4017": "Take all ($(n)) — Lucky Tokens · The Rat Bank", "4018": "Deposit all Medallions ($(h)) — Medallions · The Rat Bank", "4019": "Take 1 — Medallions · The Rat Bank", "4020": "Take 10 — Medallions · The Rat Bank", "4021": "Take all ($(n)) — Medallions · The Rat Bank", "4022": "Deposit all Trophies ($(h)) — Trophies · The Rat Bank", "4023": "Take 1 — Trophies · The Rat Bank", "4024": "Take 10 — Trophies · The Rat Bank", "4025": "Take all ($(n)) — Trophies · The Rat Bank", "4026": "Deposit all Blood Crystals ($(h)) — Blood Crystals · The Rat Bank", "4027": "Take 1 — Blood Crystals · The Rat Bank", "4028": "Take 10 — Blood Crystals · The Rat Bank", "4029": "Take all ($(n)) — Blood Crystals · The Rat Bank", "4030": "Deposit all Ember Scales ($(h)) — Ember Scales · The Rat Bank", "4031": "Take 1 — Ember Scales · The Rat Bank", "4032": "Take 10 — Ember Scales · The Rat Bank", "4033": "Take all ($(n)) — Ember Scales · The Rat Bank", "4034": "Deposit all Void Shards ($(h)) — Void Shards · The Rat Bank", "4035": "Take 1 — Void Shards · The Rat Bank", "4036": "Take 10 — Void Shards · The Rat Bank", "4037": "Take all ($(n)) — Void Shards · The Rat Bank", "4038": "Deposit all Green Xenite ($(h)) — Green Xenite · The Rat Bank", "4039": "Take 1 — Green Xenite · The Rat Bank", "4040": "Take 10 — Green Xenite · The Rat Bank", "4041": "Take all ($(n)) — Green Xenite · The Rat Bank", "4042": "Deposit all Violet Xenite ($(h)) — Violet Xenite · The Rat Bank", "4043": "Take 1 — Violet Xenite · The Rat Bank", "4044": "Take 10 — Violet Xenite · The Rat Bank", "4045": "Take all ($(n)) — Violet Xenite · The Rat Bank", "4046": "Deposit all Cyan Xenite ($(h)) — Cyan Xenite · The Rat Bank", "4047": "Take 1 — Cyan Xenite · The Rat Bank", "4048": "Take 10 — Cyan Xenite · The Rat Bank", "4049": "Take all ($(n)) — Cyan Xenite · The Rat Bank", "4050": "Deposit all Red Xenite ($(h)) — Red Xenite · The Rat Bank", "4051": "Take 1 — Red Xenite · The Rat Bank", "4052": "Take 10 — Red Xenite · The Rat Bank", "4053": "Take all ($(n)) — Red Xenite · The Rat Bank", "4054": "Deposit all Dread Tokens ($(h)) — Dread Tokens · The Rat Bank", "4055": "Take 1 — Dread Tokens · The Rat Bank", "4056": "Take 10 — Dread Tokens · The Rat Bank", "4057": "Take all ($(n)) — Dread Tokens · The Rat Bank", "4060": "Tokens $(token) — The Rat Bank - your account", "4061": "Lucky Tokens $(lucky_token) — The Rat Bank - your account", "4062": "Medallions $(medallion) — The Rat Bank - your account", "4063": "Trophies $(trophy) — The Rat Bank - your account", "4064": "Blood Crystals $(blood_crystal) — The Rat Bank - your account", "4065": "Ember Scales $(ember_scale) — The Rat Bank - your account", "4066": "Void Shards $(void_shard) — The Rat Bank - your account", "4067": "Green Xenite $(xenite_green) — The Rat Bank - your account", "4068": "Violet Xenite $(xenite_violet) — The Rat Bank - your account", "4069": "Cyan Xenite $(xenite_cyan) — The Rat Bank - your account", "4070": "Red Xenite $(xenite_red) — The Rat Bank - your account", "4071": "Deposit everything — The Rat Bank - your account", "4072": "« Back to your account / « Your account — Blood Crystals · The Rat Bank, Cyan Xenite · The Rat Bank, Dread Tokens · The Rat Bank, Ember Scales · The Rat Bank, Green Xenite · The Rat Bank, Lucky Tokens · The Rat Bank, Medallions · The Rat Bank, Red Xenite · The Rat Bank, Savings · The Rat Bank, The Exchange · The Rat Bank, Tokens · The Rat Bank, Trophies · The Rat Bank, Violet Xenite · The Rat Bank, Void Shards · The Rat Bank", "4073": "Savings account — The Rat Bank - your account", "4074": "Exchange — The Rat Bank - your account", "4075": "5 Tokens → 1 Medallion — The Exchange · The Rat Bank", "4076": "1 Medallion → 5 Tokens — The Exchange · The Rat Bank", "4077": "4 Medallions → 1 Trophy — The Exchange · The Rat Bank", "4078": "1 Trophy → 4 Medallions — The Exchange · The Rat Bank", "4079": "Auto-deposit: $(ac) — The Rat Bank - your account", "4080": "5 Trophies → 1 Dread Token — The Exchange · The Rat Bank", "4081": "1 Dread Token → 5 Trophies — The Exchange · The Rat Bank", "4085": "Community Pots — The Rat Bank - your account", "4090": "Dread Tokens $(dread_token) — The Rat Bank - your account", "4101": "$(r_l0) — QUEEN AVA'S HONOURS · the Tide Font", "4102": "$(r_l1) — QUEEN AVA'S HONOURS · the Tide Font", "4103": "$(r_l2) — QUEEN AVA'S HONOURS · the Tide Font", "4105": "The Tide's Haste +1 ($(src)) — QUEEN AVA'S HONOURS · the Tide Font", "4109": "« Her honours — QUEEN AVA'S HONOURS · $(r_nm)", "4111": "Honour +1 ($(hc)) — QUEEN AVA'S HONOURS · $(r_nm)", "4201": "$(r_0md) — THE CHAMPION'S RIBBON · your Champions beside you", "4202": "$(r_0rg) — THE CHAMPION'S RIBBON · your Champions beside you", "4203": "$(r_0au) — THE CHAMPION'S RIBBON · your Champions beside you", "4204": "$(r_1md) — THE CHAMPION'S RIBBON · your Champions beside you", "4205": "$(r_1rg) — THE CHAMPION'S RIBBON · your Champions beside you", "4206": "$(r_1au) — THE CHAMPION'S RIBBON · your Champions beside you", "4207": "$(r_2md) — THE CHAMPION'S RIBBON · your Champions beside you", "4208": "$(r_2rg) — THE CHAMPION'S RIBBON · your Champions beside you", "4209": "$(r_2au) — THE CHAMPION'S RIBBON · your Champions beside you", "5001": "$(n1) $(p1) Medallions — The Concierge", "5002": "$(n2) $(p2) Medallions — The Concierge", "5003": "$(n3) $(p3) Medallions — The Concierge", "5010": "Repair the item in my main hand 1 Medallion — The Concierge", "6001": "Go: $(t1) — Ring of Three Burrows", "6002": "Go: $(t2) — Ring of Three Burrows", "6003": "Go: $(t3) — Ring of Three Burrows", "6011": "Set burrow 1 here — Ring of Three Burrows", "6012": "Set burrow 2 here — Ring of Three Burrows", "6013": "Set burrow 3 here — Ring of Three Burrows", "7001": "Follow me — Rufus Gnaw, rat for hire", "7002": "Guard this spot — Rufus Gnaw, rat for hire", "7003": "Follow and scavenge — Rufus Gnaw, rat for hire", "7004": "Hand over the loot — Rufus Gnaw, rat for hire", "7005": "Pay a week 4 Tokens — Rufus Gnaw, rat for hire", "7006": "Call him to me — Rufus Gnaw, rat for hire", "7007": "Patch him up 1 Medallion — Rufus Gnaw, rat for hire", "7101": "Yes - start over — Key of New Beginnings", "7102": "No — Key of New Beginnings", "7201": "The Overworld — Dimension Shifter", "7202": "The Nether — Dimension Shifter", "7203": "The End — Dimension Shifter", "7301": "Speed — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7302": "Offense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7303": "Defense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7304": "Healing — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7305": "Mining — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7306": "Wardrobe — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7307": "Wraithfire Form: on / off — Emma's Ribbon · the Wraithfire Heart", "7308": "Take back the heart — Emma's Ribbon · the Wraithfire Heart", "7309": "Send her home — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7310": "Fly with me — Emma's Ribbon · the Wraithfire Heart", "7311": "Style: Guardian — Emma's Ribbon · the Wraithfire Heart", "7312": "Style: Huntress — Emma's Ribbon · the Wraithfire Heart", "7313": "Style: Tempest — Emma's Ribbon · the Wraithfire Heart", "7601": "Tier I The Copper Strongroom — Plan a Heist", "7602": "Tier II The Silver Vaults — Plan a Heist", "7603": "Tier III The Gold Reserve — Plan a Heist", "7604": "Tier IV The Diamond Deposit — Plan a Heist", "7605": "Tier V The Gutter King's Hoard — Plan a Heist", "7606": "THE ENDLESS VAULT rooms without end — Plan a Heist", "7607": "THE PIT an arena of waves — Plan a Heist", "7611": "3 TRIES +1 to +4 shares (by tier) - for the bold — How many tries?", "7612": "5 TRIES +0 to +2 shares (by tier) — How many tries?", "7613": "7 TRIES no bonus - for a first try — How many tries?", "7619": "ALARM: $(al) (click to switch) — How many tries?", "7711": "[Accept] — p73/tp/ask_bring, p73/tp/ask_go", "7712": "[Deny] — p73/tp/ask_bring, p73/tp/ask_go", "7720": "Back to the Overworld / [Back to the Overworld] — The heist is over, p101/ask_lead", "7721": "Start a new raid / [Start a new raid] — The heist is over, p101/ask_lead", "7722": "Count me in / [Count me in] — Another job?, p101/offer", "7723": "Head home / [Head home] — Another job?, p101/offer", "7724": "Leave now — Leave the heist?", "7725": "Stay — Leave the heist?", "7726": "Head home now / [Head home now] — The heist is over, p101/wait_note", "7727": "I'm in if we go again / [I'm in if we go again] — The heist is over, p101/wait_note", "7728": "The Fixer's Office — The heist is over", "7729": "Leave now — Leave the heist?", "7730": "Go to the Lounge — The heist is over", "7731": "Go to the Lounge — The heist is over", "7732": "Go to the Lounge — Another job?", "7733": "[Skip this puzzle - costs a try] — p122/offer", "7734": "Skip it (costs a try) — Skip this puzzle?", "7735": "Chatter: $(chat) (all followers) / Chatter: off / Chatter: on — 8-Bit Cecil · wardrobe, 8-Bit Cecil's Cartridge, 8-Bit Emma · wardrobe, 8-Bit Emma's Cartridge, 8-Bit Leo · wardrobe, 8-Bit Leo's Cartridge, Apophiss · wardrobe, Ashur · wardrobe, Ashur's Cinder, Bender · wardrobe, Bender's Ball, Bloo · wardrobe, Bloo's Claw, Bones · wardrobe, Bones's Whistle, Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Democratus' Challenge, Dennis · wardrobe, Dennis's Horn, Donado · wardrobe, Donado's Collar Tag, Emma · wardrobe, Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart, Fishy · wardrobe, Fishy's Pocket Bowl, KillerWatt · wardrobe, Kindled Gourd, King Omega · wardrobe, Leo · wardrobe, Mr. Capshun · wardrobe, Mr. Capshun's Pencil, Omega's Monocle, Pearlman · wardrobe, Pearlman's Business Card, Pistachio · wardrobe, Pistachio's Little Cloche, Queen Ava · wardrobe, Queen Ava's Locket, Queen Pearl · wardrobe, Queen Pearl's Pearls, Signet of the Frog Knight, The Arachno-Lantern · wardrobe, The Golden Ladle, The Hollow Hook, The Neighbor's Baton, The Serpent's Oath, The Sky Buddies · wardrobe, The Sky Mobile, The Stalker · wardrobe, Tullius · wardrobe, Tullius's Frozen Doubloon, Wilfrey · wardrobe, Wilfrey's Locket, Zib · wardrobe, p179/w/open, the Chef · wardrobe, the Frog with Mustache · wardrobe, the Neighbor · wardrobe", "7736": "Pay the Fixer (half the pot, a share) — The Fixer's mercy", "7740": "« The Tailor — 8-BIT CECIL · the Tailor, 8-BIT EMMA · the Tailor, 8-BIT LEO · the Tailor, APOPHISS · the Tailor, ASHUR · the Tailor, BENDER · the Tailor, BLOO · the Tailor, BONES · the Tailor, CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DENNIS · the Tailor, DISPLAY CASES · the Tailor, DONADO · the Tailor, EMMA · the Tailor, FISHY · the Tailor, KILLERWATT · the Tailor, KING OMEGA · the Tailor, LEO · the Tailor, MR. CAPSHUN · the Tailor, PEARLMAN · the Tailor, PISTACHIO · the Tailor, QUEEN AVA · the Tailor, QUEEN PEARL · the Tailor, THE ARACHNO-LANTERN · the Tailor, THE CHEF · the Tailor, THE FROG · the Tailor, THE NEIGHBOR · the Tailor, THE SKY BUDDIES · the Tailor, THE STALKER · the Tailor, TULLIUS · the Tailor, WILFREY · the Tailor, ZIB · the Tailor, p103/tl/auras", "7741": "Emma — p103/tl/main", "7742": "Celi — p103/tl/main", "7743": "Zib — p103/tl/main", "7744": "Cecil — p103/tl/main", "7745": "KillerWatt — p103/tl/main", "7746": "Leo — p103/tl/main", "7747": "Democratus — p103/tl/main", "7748": "Display cases — p103/tl/main", "7750": "Gold $(r_0) — EMMA · the Tailor", "7751": "Midnight $(r_1) — EMMA · the Tailor", "7752": "Mint $(r_2) — EMMA · the Tailor", "7753": "Snow $(r_3) — EMMA · the Tailor", "7754": "Crimson $(r_4) — EMMA · the Tailor", "7755": "Phantom $(r_5) — EMMA · the Tailor", "7756": "Sundress $(r_6) — EMMA · the Tailor", "7757": "Midnight Gown $(r_7) — EMMA · the Tailor", "7758": "Sakura $(r_8) — EMMA · the Tailor", "7759": "Royal Gown $(r_9) — EMMA · the Tailor", "7760": "Starlight Gown $(r_10) — EMMA · the Tailor", "7761": "Gilded Gown $(r_11) — EMMA · the Tailor", "7762": "Diamond Gown $(r_12) — EMMA · the Tailor", "7763": "Netherite Gown $(r_13) — EMMA · the Tailor", "7764": "Flower Top $(r_14) — EMMA · the Tailor", "7765": "Cozy Sweater $(r_15) — EMMA · the Tailor", "7766": "Aurora $(r_16) — CELI · the Tailor", "7767": "Rosehip $(r_17) — CELI · the Tailor", "7768": "Midnight $(r_18) — CELI · the Tailor", "7769": "Frostfire $(r_19) — CELI · the Tailor", "7770": "Gilded $(r_20) — CELI · the Tailor", "7771": "Diamond $(r_21) — CELI · the Tailor", "7772": "Netherite $(r_22) — CELI · the Tailor", "7773": "Crimson Guard $(r_23) — ZIB · the Tailor", "7774": "Forest Ranger $(r_24) — ZIB · the Tailor", "7775": "Golden Ace $(r_25) — ZIB · the Tailor", "7776": "Diamond Ace $(r_26) — ZIB · the Tailor", "7777": "Netherite Ace $(r_27) — ZIB · the Tailor", "7778": "Crimson Crusader $(r_28) — LEO · the Tailor", "7779": "Royal Purple $(r_29) — LEO · the Tailor", "7780": "Greenwood $(r_30) — LEO · the Tailor", "7781": "Golden Champion $(r_31) — LEO · the Tailor", "7782": "Diamond Champion $(r_32) — LEO · the Tailor", "7783": "Netherite Champion $(r_33) — LEO · the Tailor", "7784": "Crimson Reaper $(r_34) — DEMOCRATUS · the Tailor", "7785": "Ashen Shroud $(r_35) — DEMOCRATUS · the Tailor", "7786": "Royal Violet $(r_36) — DEMOCRATUS · the Tailor", "7787": "Gilded Storm $(r_37) — DEMOCRATUS · the Tailor", "7788": "Diamond Storm $(r_38) — DEMOCRATUS · the Tailor", "7789": "Netherite Storm $(r_39) — DEMOCRATUS · the Tailor", "7790": "Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7791": "Dark Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7792": "Quartz Display Case 5 coins — DISPLAY CASES · the Tailor", "7793": "Gilded Display Case 8 coins — DISPLAY CASES · the Tailor", "7800": "Stay on the job / « Office / « The Office / ◀ The Office — Leave the heist?, THE ARMORY · your kits, for good, THE BOND SIGILS · two at most, each heist, THE CODEX · what you've seen in the vault, THE GUTTER BANK · your coins and spoils, THE TROPHY CASE · twelve rooms, six metals, p98/crew", "7801": "« Armory / ⚒ Armory — THE FIXER'S OFFICE · everything the vault owes you, THE OFFENSE KIT · rank $(r2), THE RANGED KIT · rank $(r3), THE SUPPORT KIT · rank $(r4), THE TANK KIT · rank $(r1), YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own", "7802": "Gutter Bank / « Back / « Your account / ⛃ Gutter Bank — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank, THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies", "7803": "🏆 Trophy Case — THE FIXER'S OFFICE · everything the vault owes you", "7804": "✦ Bond Sigils — THE FIXER'S OFFICE · everything the vault owes you", "7805": "▣ Locker Hall — THE FIXER'S OFFICE · everything the vault owes you", "7806": "⛁ Crate Desk — THE FIXER'S OFFICE · everything the vault owes you", "7807": "« Raid Crew / ☺ Raid Crew — THE FIXER'S OFFICE · everything the vault owes you, p119/page", "7808": "◀ The Codex / 📖 Codex — RAID ODDS · per raider, per won heist, THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 30", "7809": "⚑ Plan a Heist — THE FIXER'S OFFICE · everything the vault owes you", "7811": "⬆ Rank up — THE TANK KIT · rank $(r1)", "7812": "⬆ Rank up — THE OFFENSE KIT · rank $(r2)", "7813": "⬆ Rank up — THE RANGED KIT · rank $(r3)", "7814": "⬆ Rank up — THE SUPPORT KIT · rank $(r4)", "7815": "Tank › — THE ARMORY · your kits, for good", "7816": "Offense › — THE ARMORY · your kits, for good", "7817": "Ranged › — THE ARMORY · your kits, for good", "7818": "Support › — THE ARMORY · your kits, for good", "7819": "none — YOUR SIGNATURE · an effect of your own", "7820": "Secondary weapon — THE ARMORY · your kits, for good", "7821": "$(r_l0) — YOUR SECONDARY · a weapon of your own", "7822": "$(r_l1) — YOUR SECONDARY · a weapon of your own", "7823": "$(r_l2) — YOUR SECONDARY · a weapon of your own", "7824": "$(r_l3) — YOUR SECONDARY · a weapon of your own", "7825": "$(r_l4) — YOUR SECONDARY · a weapon of your own", "7826": "$(r_l5) — YOUR SECONDARY · a weapon of your own", "7827": "$(r_l6) — YOUR SECONDARY · a weapon of your own", "7828": "$(r_l7) — YOUR SECONDARY · a weapon of your own", "7829": "none — YOUR SECONDARY · a weapon of your own", "7830": "Signature effect — THE ARMORY · your kits, for good", "7831": "$(r_l0) — YOUR SIGNATURE · an effect of your own", "7832": "$(r_l1) — YOUR SIGNATURE · an effect of your own", "7833": "$(r_l2) — YOUR SIGNATURE · an effect of your own", "7834": "$(r_l3) — YOUR SIGNATURE · an effect of your own", "7835": "$(r_l4) — YOUR SIGNATURE · an effect of your own", "7836": "$(r_l5) — YOUR SIGNATURE · an effect of your own", "7837": "$(r_l6) — YOUR SIGNATURE · an effect of your own", "7838": "$(r_l7) — YOUR SIGNATURE · an effect of your own", "7839": "$(r_l8) — YOUR SIGNATURE · an effect of your own", "7840": "⬇ Deposit everything — THE GUTTER BANK · your coins and spoils", "7844": "Buy 1 Token (32) — THE GUTTER BANK · Black Market Tokens", "7845": "Buy 10 Tokens (320) — THE GUTTER BANK · Black Market Tokens", "7848": "✦ Buy Tokens — THE GUTTER BANK · your coins and spoils", "7861": "📖 Rooms of the Vault — THE CODEX · what you've seen in the vault", "7862": "📖 Events and Secrets — THE CODEX · what you've seen in the vault", "7863": "📖 Curses Lifted — THE CODEX · what you've seen in the vault", "7864": "📖 Rare Finds — THE CODEX · what you've seen in the vault", "7865": "📖 Masterworks — THE CODEX · what you've seen in the vault", "7866": "🎲 Raid Odds — THE CODEX · what you've seen in the vault", "7870": "⇄ Change coins — GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, THE GUTTER BANK · your coins and spoils", "7875": "16 coins → Medallion — THE GUTTER BANK · Medallions & Trophies", "7876": "128 coins → Trophy — THE GUTTER BANK · Medallions & Trophies", "7877": "Medallion → 16 coins — THE GUTTER BANK · Medallions & Trophies", "7878": "Trophy → 128 coins — THE GUTTER BANK · Medallions & Trophies", "7879": "8 Medallions → Trophy — THE GUTTER BANK · Medallions & Trophies", "7880": "⌂ Fixer's Lounge — THE FIXER'S OFFICE · everything the vault owes you", "7881": "⏭ Skip this puzzle — THE FIXER'S OFFICE · everything the vault owes you", "7883": "Trophy → 8 Medallions — THE GUTTER BANK · Medallions & Trophies", "7884": "The Stalker — p103/crew/row_20", "7885": "The Arachno-Lantern — p103/crew/row_21", "7886": "Bender — p103/crew/row_22", "7887": "Bones — p103/crew/row_23", "7888": "Mr. Capshun — p103/crew/row_24", "7889": "The Sky Buddies — p103/crew/row_25", "7890": "8-Bit Emma — p103/crew/row_26", "7891": "8-Bit Leo — p103/crew/row_27", "7892": "8-Bit Cecil — p103/crew/row_28", "7899": "⏏ Leave the heist — THE FIXER'S OFFICE · everything the vault owes you", "7900": "Cecil — p103/crew/row_0", "7901": "Emma — p103/crew/row_1", "7902": "Celi — p103/crew/row_2", "7903": "Zib — p103/crew/row_3", "7904": "KillerWatt — p103/crew/row_4", "7905": "Leo — p103/crew/row_5", "7906": "Democratus — p103/crew/row_6", "7907": "Skiff Escort — p103/crew/row_7", "7908": "Apophiss — p103/crew/row_8", "7909": "Tullius — p103/crew/row_9", "7910": "Fishy — p103/crew/row_10", "7911": "Dennis — p103/crew/row_11", "7912": "Pistachio — p103/crew/row_12", "7913": "Omega — p103/crew/row_13", "7914": "Ashur — p103/crew/row_14", "7915": "The Chef — p103/crew/row_15", "7916": "The Neighbor — p103/crew/row_16", "7917": "Queen Ava — p103/crew/row_17", "7918": "Queen Pearl — p103/crew/row_18", "7919": "Bloo — p103/crew/row_19", "7920": "The Frog — p103/crew/row_29", "7921": "Donado — p103/crew/row_30", "7931": "Knuckles — p103/crew/hire_rows", "7932": "Doc Whiskers — p103/crew/hire_rows", "7933": "Fingers — p103/crew/hire_rows", "7934": "Tick-Tock — p103/crew/hire_rows", "7935": "Boomer — p103/crew/hire_rows", "7950": "Outfits & Emma's buff / Outfits & chatter — p98/crew", "7951": "Emma's wardrobe — p119/page", "7952": "Celi's wardrobe — p119/page", "7953": "Zib's wardrobe — p119/page", "7954": "Cecil's wardrobe — p119/page", "7955": "KillerWatt's wardrobe — p119/page", "7956": "Leo's wardrobe — p119/page", "7957": "Democratus's wardrobe — p119/page", "7961": "Emma: Speed — p119/page", "7962": "Emma: Offense — p119/page", "7963": "Emma: Defense — p119/page", "7964": "Emma: Healing — p119/page", "7965": "Emma: Mining — p119/page", "7968": "Chatter on / off — p119/page", "7970": "Gutter Coins $(c) — THE GUTTER BANK · your coins and spoils", "7971": "Gutter Medallions $(gm) — THE GUTTER BANK · your coins and spoils", "7972": "Gutter Trophies $(gt) — THE GUTTER BANK · your coins and spoils", "7973": "Copper Cogs $(m1) — THE GUTTER BANK · your coins and spoils", "7974": "Silver Seals $(m2) — THE GUTTER BANK · your coins and spoils", "7975": "Gilded Leaves $(m3) — THE GUTTER BANK · your coins and spoils", "7976": "Deep Pearls $(m4) — THE GUTTER BANK · your coins and spoils", "7977": "Hoard Embers $(m5) — THE GUTTER BANK · your coins and spoils", "7978": "Captain's Insignia $(m6) — THE GUTTER BANK · your coins and spoils", "7980": "⬇ Deposit 1 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7981": "⬇ Deposit 10 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7982": "⬇ Deposit all ($(h)) — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7983": "⬆ Take 1 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7984": "⬆ Take 10 — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "7985": "⬆ Take all ($(n)) — CAPTAIN'S INSIGNIA · The Gutter Bank, COPPER COGS · The Gutter Bank, DEEP PEARLS · The Gutter Bank, GILDED LEAVES · The Gutter Bank, GUTTER COINS · The Gutter Bank, GUTTER MEDALLIONS · The Gutter Bank, GUTTER TROPHIES · The Gutter Bank, HOARD EMBERS · The Gutter Bank, SILVER SEALS · The Gutter Bank", "8000": "« The Recruiter — p137/rc/gems, p137/rc/hires", "8001": "Cecil 192 coins / Cecil IN YOUR PACK / Cecil SIGNED — p137/rc/main", "8002": "Emma 192 coins / Emma IN YOUR PACK / Emma SIGNED — p137/rc/main", "8003": "Celi 224 coins / Celi IN YOUR PACK / Celi SIGNED — p137/rc/main", "8004": "Zib 192 coins / Zib IN YOUR PACK / Zib SIGNED — p137/rc/main", "8005": "KillerWatt 320 coins / KillerWatt IN YOUR PACK / KillerWatt SIGNED — p137/rc/main", "8006": "Leo 208 coins / Leo IN YOUR PACK / Leo SIGNED — p137/rc/main", "8007": "Democratus 224 coins / Democratus IN YOUR PACK / Democratus SIGNED — p137/rc/main", "8008": "Skiff Escort 128 coins / Skiff Escort IN YOUR PACK / Skiff Escort SIGNED — p137/rc/main", "8009": "Apophiss 352 coins / Apophiss IN YOUR PACK / Apophiss SIGNED — p137/rc/main", "8010": "Tullius 336 coins / Tullius IN YOUR PACK / Tullius SIGNED — p137/rc/main", "8011": "Fishy 176 coins / Fishy IN YOUR PACK / Fishy SIGNED — p137/rc/main", "8012": "Dennis 176 coins / Dennis IN YOUR PACK / Dennis SIGNED — p137/rc/main", "8013": "Pistachio 176 coins / Pistachio IN YOUR PACK / Pistachio SIGNED — p137/rc/main", "8014": "Omega 176 coins / Omega IN YOUR PACK / Omega SIGNED — p137/rc/main", "8015": "Ashur 176 coins / Ashur IN YOUR PACK / Ashur SIGNED — p137/rc/main", "8016": "The Chef 176 coins / The Chef IN YOUR PACK / The Chef SIGNED — p137/rc/main", "8017": "The Neighbor 176 coins / The Neighbor IN YOUR PACK / The Neighbor SIGNED — p137/rc/main", "8018": "Queen Ava 176 coins / Queen Ava IN YOUR PACK / Queen Ava SIGNED — p137/rc/main", "8019": "Queen Pearl 176 coins / Queen Pearl IN YOUR PACK / Queen Pearl SIGNED — p137/rc/main", "8020": "Bloo 176 coins / Bloo IN YOUR PACK / Bloo SIGNED — p137/rc/main", "8021": "The Stalker 176 coins / The Stalker IN YOUR PACK / The Stalker SIGNED — p137/rc/main", "8022": "The Arachno-Lantern 176 coins / The Arachno-Lantern IN YOUR PACK / The Arachno-Lantern SIGNED — p137/rc/main", "8023": "Bender 176 coins / Bender IN YOUR PACK / Bender SIGNED — p137/rc/main", "8024": "Bones 176 coins / Bones IN YOUR PACK / Bones SIGNED — p137/rc/main", "8025": "Mr. Capshun 176 coins / Mr. Capshun IN YOUR PACK / Mr. Capshun SIGNED — p137/rc/main", "8026": "The Sky Buddies 176 coins / The Sky Buddies IN YOUR PACK / The Sky Buddies SIGNED — p137/rc/main", "8027": "8-Bit Emma 176 coins / 8-Bit Emma IN YOUR PACK / 8-Bit Emma SIGNED — p137/rc/main", "8028": "8-Bit Leo 176 coins / 8-Bit Leo IN YOUR PACK / 8-Bit Leo SIGNED — p137/rc/main", "8029": "8-Bit Cecil 176 coins / 8-Bit Cecil IN YOUR PACK / 8-Bit Cecil SIGNED — p137/rc/main", "8030": "The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main", "8031": "Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main", "8040": "Hirelings › — p137/rc/main", "8041": "Knuckles 48 coins / Knuckles FILED / Knuckles IN YOUR PACK — p137/rc/hires", "8042": "Doc Whiskers 64 coins / Doc Whiskers FILED / Doc Whiskers IN YOUR PACK — p137/rc/hires", "8043": "Fingers 48 coins / Fingers FILED / Fingers IN YOUR PACK — p137/rc/hires", "8044": "Tick-Tock 64 coins / Tick-Tock FILED / Tick-Tock IN YOUR PACK — p137/rc/hires", "8045": "Boomer 64 coins / Boomer FILED / Boomer IN YOUR PACK — p137/rc/hires", "8050": "Vault gems › — p137/rc/main", "8051": "Fire Gem 96 coins — p137/rc/gems", "8052": "Water Gem 96 coins — p137/rc/gems", "8053": "Poison Gem 96 coins — p137/rc/gems", "8054": "Earth Gem 96 coins — p137/rc/gems", "8055": "Electric Gem 96 coins — p137/rc/gems", "8056": "Rock Gem 96 coins — p137/rc/gems", "8057": "Air Gem 96 coins — p137/rc/gems", "8058": "Grass Gem 96 coins — p137/rc/gems", "8059": "Ice Gem 96 coins — p137/rc/gems", "8100": "Apophiss — p103/tl/main", "8101": "Tullius — p103/tl/main", "8102": "The Frog — p103/tl/main", "8103": "Donado — p103/tl/main", "8104": "Pearlman — p103/tl/main", "8105": "Wilfrey — p103/tl/main", "8106": "Auras (rare) — p103/tl/main", "8107": "Fishy — p103/tl/main", "8108": "Dennis — p103/tl/main", "8109": "Pistachio — p103/tl/main", "8110": "Crimson $(r_40) — CECIL · the Tailor", "8111": "Midnight $(r_41) — CECIL · the Tailor", "8112": "Bone $(r_42) — CECIL · the Tailor", "8113": "Gilded $(r_43) — CECIL · the Tailor", "8114": "Diamond $(r_44) — CECIL · the Tailor", "8115": "Netherite $(r_45) — CECIL · the Tailor", "8116": "Midnight $(r_46) — KILLERWATT · the Tailor", "8117": "Bone $(r_47) — KILLERWATT · the Tailor", "8118": "Neon $(r_48) — KILLERWATT · the Tailor", "8119": "Golden Thunder $(r_49) — KILLERWATT · the Tailor", "8120": "Diamond Thunder $(r_50) — KILLERWATT · the Tailor", "8121": "Netherite Thunder $(r_51) — KILLERWATT · the Tailor", "8122": "Obsidian Coil $(r_52) — APOPHISS · the Tailor", "8123": "Blood Wyrm $(r_53) — APOPHISS · the Tailor", "8124": "Frost Serpent $(r_54) — APOPHISS · the Tailor", "8125": "Gilded Coil $(r_55) — APOPHISS · the Tailor", "8126": "Diamond Coil $(r_56) — APOPHISS · the Tailor", "8127": "Netherite Coil $(r_57) — APOPHISS · the Tailor", "8128": "Admiral's Blue $(r_58) — TULLIUS · the Tailor", "8129": "Corsair Crimson $(r_59) — TULLIUS · the Tailor", "8130": "Bleached Bone $(r_60) — TULLIUS · the Tailor", "8131": "Gilded Captain $(r_61) — TULLIUS · the Tailor", "8132": "Diamond Captain $(r_62) — TULLIUS · the Tailor", "8133": "Netherite Captain $(r_63) — TULLIUS · the Tailor", "8134": "Bluejay $(r_64) — THE FROG · the Tailor", "8135": "Ember Toad $(r_65) — THE FROG · the Tailor", "8136": "Old Bog $(r_66) — THE FROG · the Tailor", "8137": "Golden Prince $(r_67) — THE FROG · the Tailor", "8138": "Diamond Prince $(r_68) — THE FROG · the Tailor", "8139": "Netherite Prince $(r_69) — THE FROG · the Tailor", "8140": "Chocolate $(r_70) — DONADO · the Tailor", "8141": "Midnight $(r_71) — DONADO · the Tailor", "8142": "Snowdrift $(r_72) — DONADO · the Tailor", "8143": "Starlit $(r_73) — DONADO · the Tailor", "8144": "Gilded $(r_74) — DONADO · the Tailor", "8145": "Diamond $(r_75) — DONADO · the Tailor", "8146": "Netherite $(r_76) — DONADO · the Tailor", "8147": "Ruby $(r_77) — PEARLMAN · the Tailor", "8148": "Emerald $(r_78) — PEARLMAN · the Tailor", "8149": "Amethyst $(r_79) — PEARLMAN · the Tailor", "8150": "Blossom Halo (Emma) 1280 coins / Blossom Halo (Emma) OWNED — p103/tl/auras", "8151": "Moonfrost Veil (Celi) 1280 coins / Moonfrost Veil (Celi) OWNED — p103/tl/auras", "8152": "Starfield Static (Zib) 1280 coins / Starfield Static (Zib) OWNED — p103/tl/auras", "8153": "Arcane Corona (Cecil) 1280 coins / Arcane Corona (Cecil) OWNED — p103/tl/auras", "8154": "Storm Crown (KillerWatt) 1280 coins / Storm Crown (KillerWatt) OWNED — p103/tl/auras", "8155": "Tidal Aegis (Leo) 1280 coins / Tidal Aegis (Leo) OWNED — p103/tl/auras", "8156": "Reaper's Shroud (Democratus) 1280 coins / Reaper's Shroud (Democratus) OWNED — p103/tl/auras", "8157": "Black-Flame Mantle (Apophiss) 1280 coins / Black-Flame Mantle (Apophiss) OWNED — p103/tl/auras", "8158": "Drowned Gale (Tullius) 1280 coins / Drowned Gale (Tullius) OWNED — p103/tl/auras", "8159": "Bog-Light Ring (the Frog) 1280 coins / Bog-Light Ring (the Frog) OWNED — p103/tl/auras", "8160": "Tractor Beam (Donado) 1280 coins / Tractor Beam (Donado) OWNED — p103/tl/auras", "8161": "Golden Gleam (Pearlman) 1280 coins / Golden Gleam (Pearlman) OWNED — p103/tl/auras", "8162": "Lordly Radiance (Wilfrey) 1280 coins / Lordly Radiance (Wilfrey) OWNED — p103/tl/auras", "8163": "Bubble Halo (Fishy) 1280 coins / Bubble Halo (Fishy) OWNED — p103/tl/auras", "8164": "Gilded $(r_80) — PEARLMAN · the Tailor", "8165": "Diamond $(r_81) — PEARLMAN · the Tailor", "8166": "Netherite $(r_82) — PEARLMAN · the Tailor", "8167": "Midnight Silk $(r_83) — FISHY · the Tailor", "8168": "Crimson Opera $(r_84) — FISHY · the Tailor", "8169": "Emerald Ascot $(r_85) — FISHY · the Tailor", "8170": "Gilded Topper $(r_86) — FISHY · the Tailor", "8171": "Diamond Topper $(r_87) — FISHY · the Tailor", "8172": "Netherite Topper $(r_88) — FISHY · the Tailor", "8173": "Crimson Cross $(r_89) — WILFREY · the Tailor", "8174": "Azure Chevron $(r_90) — WILFREY · the Tailor", "8175": "Verdant Bend $(r_91) — WILFREY · the Tailor", "8176": "Gilded Sun $(r_92) — WILFREY · the Tailor", "8177": "Diamond Sun $(r_93) — WILFREY · the Tailor", "8178": "Netherite Sun $(r_94) — WILFREY · the Tailor", "8179": "Road Brown $(r_95) — DENNIS · the Tailor", "8180": "Biker Red $(r_96) — DENNIS · the Tailor", "8181": "Forest Leather $(r_97) — DENNIS · the Tailor", "8182": "Gilded Jacket $(r_98) — DENNIS · the Tailor", "8183": "Diamond Jacket $(r_99) — DENNIS · the Tailor", "8184": "Netherite Jacket $(r_100) — DENNIS · the Tailor", "8185": "Midnight Tails $(r_101) — PISTACHIO · the Tailor", "8186": "Claret Tails $(r_102) — PISTACHIO · the Tailor", "8187": "Ivory Tails $(r_103) — PISTACHIO · the Tailor", "8188": "Gilded Tails $(r_104) — PISTACHIO · the Tailor", "8189": "Diamond Tails $(r_105) — PISTACHIO · the Tailor", "8190": "Netherite Tails $(r_106) — PISTACHIO · the Tailor", "8191": "Spectral Blue $(r_107) — KING OMEGA · the Tailor", "8192": "Blood Moon $(r_108) — KING OMEGA · the Tailor", "8193": "Verdant Wraith $(r_109) — KING OMEGA · the Tailor", "8194": "Gilded King $(r_110) — KING OMEGA · the Tailor", "8195": "Diamond King $(r_111) — KING OMEGA · the Tailor", "8196": "Gold Rush Glimmer (Dennis) 1280 coins / Gold Rush Glimmer (Dennis) OWNED — p103/tl/auras", "8197": "Ectoplasmic Mist (Pistachio) 1280 coins / Ectoplasmic Mist (Pistachio) OWNED — p103/tl/auras", "8198": "Court of Souls (King Omega) 1280 coins / Court of Souls (King Omega) OWNED — p103/tl/auras", "8199": "Ashfall Crown (Ashur) 1280 coins / Ashfall Crown (Ashur) OWNED — p103/tl/auras", "8200": "Netherite King $(r_112) — KING OMEGA · the Tailor", "8201": "Blue Flame $(r_113) — ASHUR · the Tailor", "8202": "Verdant Ember $(r_114) — ASHUR · the Tailor", "8203": "Obsidian Rose $(r_115) — ASHUR · the Tailor", "8204": "Gilded Magma $(r_116) — ASHUR · the Tailor", "8205": "Diamond Magma $(r_117) — ASHUR · the Tailor", "8206": "Netherite Magma $(r_118) — ASHUR · the Tailor", "8207": "Midnight Brigade $(r_119) — THE CHEF · the Tailor", "8208": "Bistro Blue $(r_120) — THE CHEF · the Tailor", "8209": "Sommelier Wine $(r_121) — THE CHEF · the Tailor", "8210": "Gilded Whites $(r_122) — THE CHEF · the Tailor", "8211": "Diamond Whites $(r_123) — THE CHEF · the Tailor", "8212": "Netherite Whites $(r_124) — THE CHEF · the Tailor", "8213": "Navy Bandmaster $(r_125) — THE NEIGHBOR · the Tailor", "8214": "Encore Crimson $(r_126) — THE NEIGHBOR · the Tailor", "8215": "Jazz Violet $(r_127) — THE NEIGHBOR · the Tailor", "8216": "Gilded Suit $(r_128) — THE NEIGHBOR · the Tailor", "8217": "Diamond Suit $(r_129) — THE NEIGHBOR · the Tailor", "8218": "Netherite Suit $(r_130) — THE NEIGHBOR · the Tailor", "8219": "Coral Reef $(r_131) — QUEEN AVA · the Tailor", "8220": "Abyssal Violet $(r_132) — QUEEN AVA · the Tailor", "8221": "Kelp Forest $(r_133) — QUEEN AVA · the Tailor", "8222": "Gilded Gown $(r_134) — QUEEN AVA · the Tailor", "8223": "Diamond Gown $(r_135) — QUEEN AVA · the Tailor", "8224": "Netherite Gown $(r_136) — QUEEN AVA · the Tailor", "8225": "Coral Pink $(r_137) — QUEEN PEARL · the Tailor", "8226": "Sunset Gold $(r_138) — QUEEN PEARL · the Tailor", "8227": "Starlit Navy $(r_139) — QUEEN PEARL · the Tailor", "8228": "Gilded Dress $(r_140) — QUEEN PEARL · the Tailor", "8229": "Diamond Dress $(r_141) — QUEEN PEARL · the Tailor", "8230": "Netherite Dress $(r_142) — QUEEN PEARL · the Tailor", "8231": "Shadow Pelt $(r_143) — BLOO · the Tailor", "8232": "Ember Mane $(r_144) — BLOO · the Tailor", "8233": "Frost Coat $(r_145) — BLOO · the Tailor", "8234": "Gilded Fur $(r_146) — BLOO · the Tailor", "8235": "Diamond Fur $(r_147) — BLOO · the Tailor", "8236": "Netherite Fur $(r_148) — BLOO · the Tailor", "8237": "Bone White $(r_149) — THE STALKER · the Tailor", "8238": "Ashen Grey $(r_150) — THE STALKER · the Tailor", "8239": "Blood Moon $(r_151) — THE STALKER · the Tailor", "8240": "Gilded Skin $(r_152) — THE STALKER · the Tailor", "8241": "Diamond Skin $(r_153) — THE STALKER · the Tailor", "8242": "Netherite Skin $(r_154) — THE STALKER · the Tailor", "8243": "Ghost Gourd $(r_155) — THE ARACHNO-LANTERN · the Tailor", "8244": "Soulfire Rind $(r_156) — THE ARACHNO-LANTERN · the Tailor", "8245": "Harvest Moon $(r_157) — THE ARACHNO-LANTERN · the Tailor", "8246": "Gilded Rind $(r_158) — THE ARACHNO-LANTERN · the Tailor", "8247": "Diamond Rind $(r_159) — THE ARACHNO-LANTERN · the Tailor", "8248": "Netherite Rind $(r_160) — THE ARACHNO-LANTERN · the Tailor", "8249": "Midnight Black $(r_161) — BENDER · the Tailor", "8250": "Snow White $(r_162) — BENDER · the Tailor", "8251": "Sable $(r_163) — BENDER · the Tailor", "8252": "Gilded Coat $(r_164) — BENDER · the Tailor", "8253": "Diamond Coat $(r_165) — BENDER · the Tailor", "8254": "Netherite Coat $(r_166) — BENDER · the Tailor", "8255": "Great White $(r_167) — BONES · the Tailor", "8256": "Hammerhead Bronze $(r_168) — BONES · the Tailor", "8257": "Abyss Black $(r_169) — BONES · the Tailor", "8258": "Gilded Skin $(r_170) — BONES · the Tailor", "8259": "Diamond Skin $(r_171) — BONES · the Tailor", "8260": "Netherite Skin $(r_172) — BONES · the Tailor", "8261": "Bubblegum Pink $(r_173) — THE SKY BUDDIES · the Tailor", "8262": "Mint Dream $(r_174) — THE SKY BUDDIES · the Tailor", "8263": "Lavender Night $(r_175) — THE SKY BUDDIES · the Tailor", "8264": "Gilded Nightcap $(r_176) — THE SKY BUDDIES · the Tailor", "8265": "Diamond Nightcap $(r_177) — THE SKY BUDDIES · the Tailor", "8266": "Netherite Nightcap $(r_178) — THE SKY BUDDIES · the Tailor", "8267": "Game Boy $(r_179) — 8-BIT EMMA · the Tailor", "8268": "Virtual Boy $(r_180) — 8-BIT EMMA · the Tailor", "8269": "Sepia Print $(r_181) — 8-BIT EMMA · the Tailor", "8270": "King Omega — p103/tl/main", "8271": "Ashur — p103/tl/main", "8272": "The Chef — p103/tl/main", "8273": "The Neighbor — p103/tl/main", "8274": "Queen Ava — p103/tl/main", "8275": "Queen Pearl — p103/tl/main", "8276": "Bloo — p103/tl/main", "8277": "The Stalker — p103/tl/main", "8278": "The Arachno-Lantern — p103/tl/main", "8279": "Bender — p103/tl/main", "8280": "Apophiss's wardrobe / Bones — p103/tl/main, p119/page", "8281": "Mr. Capshun / Tullius's wardrobe — p103/tl/main, p119/page", "8282": "8-Bit Cecil / The Frog's wardrobe — p103/tl/main, p119/page", "8283": "8-Bit Leo / Donado's wardrobe — p103/tl/main, p119/page", "8284": "8-Bit Emma / Pearlman's wardrobe — p103/tl/main, p119/page", "8285": "The Sky Buddies / Wilfrey's wardrobe — p103/tl/main, p119/page", "8286": "Fishy's wardrobe — p119/page", "8287": "Dennis's wardrobe — p119/page", "8288": "Pistachio's wardrobe — p119/page", "8289": "King Omega's wardrobe — p119/page", "8290": "Ashur's wardrobe — p119/page", "8291": "The Chef's wardrobe — p119/page", "8292": "The Neighbor's wardrobe — p119/page", "8293": "Kitchen Steam (the Chef) 1280 coins / Kitchen Steam (the Chef) OWNED / Queen Ava's wardrobe — p103/tl/auras, p119/page", "8294": "Grand Symphony (the Neighbor) 1280 coins / Grand Symphony (the Neighbor) OWNED / Queen Pearl's wardrobe — p103/tl/auras, p119/page", "8295": "Bloo's wardrobe / Crown of the Deep (Queen Ava) 1280 coins / Crown of the Deep (Queen Ava) OWNED — p103/tl/auras, p119/page", "8296": "Pearlescent Tide (Queen Pearl) 1280 coins / Pearlescent Tide (Queen Pearl) OWNED / The Stalker's wardrobe — p103/tl/auras, p119/page", "8297": "Feral Moon (Bloo) 1280 coins / Feral Moon (Bloo) OWNED / The Arachno-Lantern's wardrobe — p103/tl/auras, p119/page", "8298": "Bender's wardrobe / The Long Night (The Stalker) 1280 coins / The Long Night (The Stalker) OWNED — p103/tl/auras, p119/page", "8299": "Bones's wardrobe / Hallowfire (The Arachno-Lantern) 1280 coins / Hallowfire (The Arachno-Lantern) OWNED — p103/tl/auras, p119/page", "8300": "Mr. Capshun's wardrobe — p119/page", "8301": "8-Bit Cecil's wardrobe / Wait here / follow me — Pearlman's Business Card, p119/page", "8302": "8-Bit Leo's wardrobe / Wardrobe — Pearlman's Business Card, p119/page", "8303": "8-Bit Emma's wardrobe / Seasons — Pearlman's Business Card, p119/page", "8304": "The Sky Buddies's wardrobe — p119/page", "8309": "Send him home — Pearlman's Business Card", "8380": "Goodest Boy (Bender) 1280 coins / Goodest Boy (Bender) OWNED — p103/tl/auras", "8381": "Abyssal Tide (Bones) 1280 coins / Abyssal Tide (Bones) OWNED — p103/tl/auras", "8382": "Rainbow Doodles (Mr. Capshun) 1280 coins / Rainbow Doodles (Mr. Capshun) OWNED — p103/tl/auras", "8383": "Starry Sky (The Sky Buddies) 1280 coins / Starry Sky (The Sky Buddies) OWNED — p103/tl/auras", "8384": "Scanlines (8-Bit Emma) 1280 coins / Scanlines (8-Bit Emma) OWNED — p103/tl/auras", "8385": "Scanlines (8-Bit Leo) 1280 coins / Scanlines (8-Bit Leo) OWNED — p103/tl/auras", "8386": "Scanlines (8-Bit Cecil) 1280 coins / Scanlines (8-Bit Cecil) OWNED — p103/tl/auras", "8501": "Raw Materials Crate 16 coins — THE CRATE DESK · paid from your bank and pockets", "8502": "Adventurer's Crate 32 coins — THE CRATE DESK · paid from your bank and pockets", "8503": "Mineral Crate 48 coins — THE CRATE DESK · paid from your bank and pockets", "8504": "Crimson Tip-off 64 coins — THE CRATE DESK · paid from your bank and pockets", "8505": "Vorn Signal 64 coins — THE CRATE DESK · paid from your bank and pockets", "8506": "Stone Crate 6 coins — THE CRATE DESK · paid from your bank and pockets", "8507": "Timber Crate 8 coins — THE CRATE DESK · paid from your bank and pockets", "8601": "Sit / follow — The Serpent's Oath", "8602": "Ride him — The Serpent's Oath", "8603": "Take off the saddle — The Serpent's Oath", "8604": "Wardrobe — The Serpent's Oath", "8608": "Call for Apophiss — The Serpent's Oath", "8609": "Send him home — The Serpent's Oath", "8621": "Sit / follow — Tullius's Frozen Doubloon", "8624": "Wardrobe — Tullius's Frozen Doubloon", "8628": "Call for Tullius — Tullius's Frozen Doubloon", "8629": "Send him home — Tullius's Frozen Doubloon", "8641": "Sit / follow — Signet of the Frog Knight", "8642": "Hand back my gear — Signet of the Frog Knight", "8643": "Wardrobe — Signet of the Frog Knight", "8648": "Call for the Frog — Signet of the Frog Knight", "8649": "Send him home — Signet of the Frog Knight", "8651": "Sit / follow — Donado's Collar Tag", "8652": "Hand back my gear — Donado's Collar Tag", "8653": "Wardrobe — Donado's Collar Tag", "8658": "Call for Donado — Donado's Collar Tag", "8659": "Send him home — Donado's Collar Tag", "9000": "$(r_home) / « Outfits & buffs — Apophiss · wardrobe", "9002": "His own scales $(r_apo0) — Apophiss · wardrobe", "9003": "Obsidian Coil $(r_apo1) — Apophiss · wardrobe", "9004": "Blood Wyrm $(r_apo2) — Apophiss · wardrobe", "9005": "Frost Serpent $(r_apo3) — Apophiss · wardrobe", "9006": "Gilded Coil $(r_apo4) — Apophiss · wardrobe", "9007": "Diamond Coil $(r_apo5) — Apophiss · wardrobe", "9008": "Netherite Coil $(r_apo6) — Apophiss · wardrobe", "9018": "Pixel costume $(r_px) — Apophiss · wardrobe", "9019": "Black-Flame Mantle $(r_aura) — Apophiss · wardrobe", "9020": "$(r_home) / « Outfits & buffs — Tullius · wardrobe", "9022": "His old coat $(r_tul0) — Tullius · wardrobe", "9023": "Admiral's Blue $(r_tul1) — Tullius · wardrobe", "9024": "Corsair Crimson $(r_tul2) — Tullius · wardrobe", "9025": "Bleached Bone $(r_tul3) — Tullius · wardrobe", "9026": "Gilded Captain $(r_tul4) — Tullius · wardrobe", "9027": "Diamond Captain $(r_tul5) — Tullius · wardrobe", "9028": "Netherite Captain $(r_tul6) — Tullius · wardrobe", "9038": "Pixel costume $(r_px) — Tullius · wardrobe", "9039": "Drowned Gale $(r_aura) — Tullius · wardrobe", "9040": "$(r_home) / « Outfits & buffs — the Frog with Mustache · wardrobe", "9042": "His own skin $(r_frog0) — the Frog with Mustache · wardrobe", "9043": "Bluejay $(r_frog1) — the Frog with Mustache · wardrobe", "9044": "Ember Toad $(r_frog2) — the Frog with Mustache · wardrobe", "9045": "Old Bog $(r_frog3) — the Frog with Mustache · wardrobe", "9046": "Golden Prince $(r_frog4) — the Frog with Mustache · wardrobe", "9047": "Diamond Prince $(r_frog5) — the Frog with Mustache · wardrobe", "9048": "Netherite Prince $(r_frog6) — the Frog with Mustache · wardrobe", "9058": "Pixel costume $(r_px) — the Frog with Mustache · wardrobe", "9059": "Bog-Light Ring $(r_aura) — the Frog with Mustache · wardrobe", "9060": "$(r_home) / « Outfits & buffs — Donado · wardrobe", "9062": "His own coat $(r_don0) — Donado · wardrobe", "9063": "Chocolate $(r_don1) — Donado · wardrobe", "9064": "Midnight $(r_don2) — Donado · wardrobe", "9065": "Snowdrift $(r_don3) — Donado · wardrobe", "9066": "Starlit $(r_don4) — Donado · wardrobe", "9067": "Gilded $(r_don5) — Donado · wardrobe", "9068": "Diamond $(r_don6) — Donado · wardrobe", "9069": "Netherite $(r_don7) — Donado · wardrobe", "9078": "Pixel costume $(r_px) — Donado · wardrobe", "9079": "Tractor Beam $(r_aura) — Donado · wardrobe", "9080": "$(r_home) / « Outfits & buffs — Pearlman · wardrobe", "9082": "The blue bow tie $(r_pearl0) — Pearlman · wardrobe", "9083": "Ruby $(r_pearl1) — Pearlman · wardrobe", "9084": "Emerald $(r_pearl2) — Pearlman · wardrobe", "9085": "Amethyst $(r_pearl3) — Pearlman · wardrobe", "9086": "Gilded $(r_pearl4) — Pearlman · wardrobe", "9087": "Diamond $(r_pearl5) — Pearlman · wardrobe", "9088": "Netherite $(r_pearl6) — Pearlman · wardrobe", "9098": "Pixel costume $(r_px) — Pearlman · wardrobe", "9099": "Golden Gleam $(r_aura) — Pearlman · wardrobe", "9100": "$(r_home) / « Outfits & buffs — Wilfrey · wardrobe", "9102": "No shield $(r_wil0) — Wilfrey · wardrobe", "9103": "Crimson Cross $(r_wil1) — Wilfrey · wardrobe", "9104": "Azure Chevron $(r_wil2) — Wilfrey · wardrobe", "9105": "Verdant Bend $(r_wil3) — Wilfrey · wardrobe", "9106": "Gilded Sun $(r_wil4) — Wilfrey · wardrobe", "9107": "Diamond Sun $(r_wil5) — Wilfrey · wardrobe", "9108": "Netherite Sun $(r_wil6) — Wilfrey · wardrobe", "9118": "Pixel costume $(r_px) — Wilfrey · wardrobe", "9119": "Lordly Radiance $(r_aura) — Wilfrey · wardrobe", "9120": "$(r_home) / « Outfits & buffs — Fishy · wardrobe", "9122": "His old black topper $(r_fishy0) — Fishy · wardrobe", "9123": "Midnight Silk $(r_fishy1) — Fishy · wardrobe", "9124": "Crimson Opera $(r_fishy2) — Fishy · wardrobe", "9125": "Emerald Ascot $(r_fishy3) — Fishy · wardrobe", "9126": "Gilded Topper $(r_fishy4) — Fishy · wardrobe", "9127": "Diamond Topper $(r_fishy5) — Fishy · wardrobe", "9128": "Netherite Topper $(r_fishy6) — Fishy · wardrobe", "9138": "Pixel costume $(r_px) — Fishy · wardrobe", "9139": "Bubble Halo $(r_aura) — Fishy · wardrobe", "9141": "Sit / follow — Fishy's Pocket Bowl", "9142": "Wardrobe — Fishy's Pocket Bowl", "9143": "The Cabinet — Fishy's Pocket Bowl", "9144": "Fishy's powers — Fishy's Pocket Bowl", "9148": "Call for Fishy — Fishy's Pocket Bowl", "9149": "Send him home — Fishy's Pocket Bowl", "9150": "« The Cabinet — FISHY'S POWERS · taught by the Cabinet, THE COURT · $(n) of 20, THE DEEP · $(n) of 20, THE GUTTER · $(n) of 20, THE HOLLOW · $(n) of 20, THE SKIES · $(n) of 20, THE WILDS · $(n) of 20", "9151": "The Hollow $(c_hollow) of 20$(r_hollow) — FISHY'S CABINET OF CURIOSITIES", "9152": "The Gutter $(c_gutter) of 20$(r_gutter) — FISHY'S CABINET OF CURIOSITIES", "9153": "The Skies $(c_skies) of 20$(r_skies) — FISHY'S CABINET OF CURIOSITIES", "9154": "The Deep $(c_deep) of 20$(r_deep) — FISHY'S CABINET OF CURIOSITIES", "9155": "The Wilds $(c_wilds) of 20$(r_wilds) — FISHY'S CABINET OF CURIOSITIES", "9156": "The Court $(c_court) of 20$(r_court) — FISHY'S CABINET OF CURIOSITIES", "9157": "Fishy's powers — FISHY'S CABINET OF CURIOSITIES", "9158": "Set it out in the hall — THE COURT · $(n) of 20, THE DEEP · $(n) of 20, THE GUTTER · $(n) of 20, THE HOLLOW · $(n) of 20, THE SKIES · $(n) of 20, THE WILDS · $(n) of 20", "9159": "A spare Pocket Bowl — FISHY'S CABINET OF CURIOSITIES", "9701": "Duel him — Democratus' Challenge", "9702": "Call for Democratus / Send him home — Democratus' Challenge", "9703": "Wardrobe — Democratus' Challenge", "9800": "$(r_home) / « Outfits & buffs — Emma · wardrobe", "9802": "Pink ribbon $(r_ribbon0) — Emma · wardrobe", "9803": "Gold $(r_ribbon1) — Emma · wardrobe", "9804": "Midnight $(r_ribbon2) — Emma · wardrobe", "9805": "Mint $(r_ribbon3) — Emma · wardrobe", "9806": "Snow $(r_ribbon4) — Emma · wardrobe", "9807": "Crimson $(r_ribbon5) — Emma · wardrobe", "9808": "Phantom $(r_ribbon6) — Emma · wardrobe", "9812": "Her own dress $(r_dress0) — Emma · wardrobe", "9813": "Sundress $(r_dress1) — Emma · wardrobe", "9814": "Midnight Gown $(r_dress2) — Emma · wardrobe", "9815": "Sakura $(r_dress3) — Emma · wardrobe", "9816": "Royal Gown $(r_dress4) — Emma · wardrobe", "9817": "Starlight Gown $(r_dress5) — Emma · wardrobe", "9818": "Gilded Gown $(r_dress6) — Emma · wardrobe", "9819": "Diamond Gown $(r_dress7) — Emma · wardrobe", "9820": "Netherite Gown $(r_dress8) — Emma · wardrobe", "9823": "Flower Top $(r_outfit1) — Emma · wardrobe", "9824": "Cozy Sweater $(r_outfit2) — Emma · wardrobe", "9837": "KillerWatt look $(r_kw) — Emma · wardrobe", "9839": "Blossom Halo $(r_aura) — Emma · wardrobe", "9840": "$(r_home) / « Outfits & buffs — Celi · wardrobe", "9842": "Own clothes $(r_celi0) — Celi · wardrobe", "9843": "Aurora $(r_celi1) — Celi · wardrobe", "9844": "Rosehip $(r_celi2) — Celi · wardrobe", "9845": "Midnight $(r_celi3) — Celi · wardrobe", "9846": "Frostfire $(r_celi4) — Celi · wardrobe", "9847": "Gilded $(r_celi5) — Celi · wardrobe", "9848": "Diamond $(r_celi6) — Celi · wardrobe", "9849": "Netherite $(r_celi7) — Celi · wardrobe", "9858": "Pixel costume $(r_px) — Celi · wardrobe", "9859": "Moonfrost Veil $(r_aura) — Celi · wardrobe", "9860": "$(r_home) / « Outfits & buffs — Zib · wardrobe", "9862": "Own clothes $(r_zib0) — Zib · wardrobe", "9863": "Crimson Guard $(r_zib1) — Zib · wardrobe", "9864": "Forest Ranger $(r_zib2) — Zib · wardrobe", "9865": "Golden Ace $(r_zib3) — Zib · wardrobe", "9866": "Diamond Ace $(r_zib4) — Zib · wardrobe", "9867": "Netherite Ace $(r_zib5) — Zib · wardrobe", "9878": "Pixel costume $(r_px) — Zib · wardrobe", "9879": "Starfield Static $(r_aura) — Zib · wardrobe", "9880": "$(r_home) / « Outfits & buffs — Cecil · wardrobe", "9882": "Own colours $(r_cecil0) — Cecil · wardrobe", "9883": "Crimson $(r_cecil1) — Cecil · wardrobe", "9884": "Midnight $(r_cecil2) — Cecil · wardrobe", "9885": "Bone $(r_cecil3) — Cecil · wardrobe", "9886": "Gilded $(r_cecil4) — Cecil · wardrobe", "9887": "Diamond $(r_cecil5) — Cecil · wardrobe", "9888": "Netherite $(r_cecil6) — Cecil · wardrobe", "9899": "Arcane Corona $(r_aura) — Cecil · wardrobe", "9900": "$(r_home) / « Outfits & buffs — KillerWatt · wardrobe", "9902": "Own colours $(r_kw0) — KillerWatt · wardrobe", "9903": "Midnight $(r_kw1) — KillerWatt · wardrobe", "9904": "Bone $(r_kw2) — KillerWatt · wardrobe", "9905": "Neon $(r_kw3) — KillerWatt · wardrobe", "9906": "Golden Thunder $(r_kw4) — KillerWatt · wardrobe", "9907": "Diamond Thunder $(r_kw5) — KillerWatt · wardrobe", "9908": "Netherite Thunder $(r_kw6) — KillerWatt · wardrobe", "9918": "Pixel costume $(r_px) — KillerWatt · wardrobe", "9919": "Storm Crown $(r_aura) — KillerWatt · wardrobe", "9920": "$(r_home) / « Outfits & buffs — Leo · wardrobe", "9922": "Own clothes $(r_leo0) — Leo · wardrobe", "9923": "Crimson Crusader $(r_leo1) — Leo · wardrobe", "9924": "Royal Purple $(r_leo2) — Leo · wardrobe", "9925": "Greenwood $(r_leo3) — Leo · wardrobe", "9926": "Golden Champion $(r_leo4) — Leo · wardrobe", "9927": "Diamond Champion $(r_leo5) — Leo · wardrobe", "9928": "Netherite Champion $(r_leo6) — Leo · wardrobe", "9939": "Tidal Aegis $(r_aura) — Leo · wardrobe", "9940": "$(r_home) / « Outfits & buffs — Democratus · wardrobe", "9942": "Own clothes $(r_demo0) — Democratus · wardrobe", "9943": "Crimson Reaper $(r_demo1) — Democratus · wardrobe", "9944": "Ashen Shroud $(r_demo2) — Democratus · wardrobe", "9945": "Royal Violet $(r_demo3) — Democratus · wardrobe", "9946": "Gilded Storm $(r_demo4) — Democratus · wardrobe", "9947": "Diamond Storm $(r_demo5) — Democratus · wardrobe", "9948": "Netherite Storm $(r_demo6) — Democratus · wardrobe", "9958": "Pixel costume $(r_px) — Democratus · wardrobe", "9959": "Reaper's Shroud $(r_aura) — Democratus · wardrobe"}, "version": "v2.94s"} -->
