# Button codes (`/trigger bm.act set N`) - v2.77d

Written by `buttons.py` at the end of every build (`python3 gen_dp.py --phase2`); for any build: `python3 buttons.py <BlackMarket_DP dir> <version>`. Edit only the **Notes** - they are kept as written.

**402 codes** on 609 buttons and chat links (2 more built at run time) · 52 routes in `p28/act` · **7794 codes free** in 1-9999 · problems: **0**

## Adding a button

1. Pick a code: a free one inside your feature's block (**Blocks**), or a fresh run from **Free codes**.
2. Route it with an exact `matches N` line - a range only over a block your router owns - and have the router check `bm.menu` (the menu that shows the button) before it acts.
3. Build: phase129 refuses a shadowed route; this file rewrites itself; **Problems** should say none.
4. Test by pressing the button the client was shown (bots: `A.press(/words/)` sends exactly its command).

## Problems

None.

Same code, different words (fine when each menu's router checks `bm.menu`): **7800** « Office / « The Office / ◀ The Office / Stay on the job; **7802** « Back / Gutter Bank / ⛃ The Gutter Bank; **8001** Cecil 192 coins / Cecil IN YOUR PACK / Cecil SIGNED; **8002** Emma 192 coins / Emma IN YOUR PACK / Emma SIGNED; **8003** Celi 224 coins / Celi IN YOUR PACK / Celi SIGNED; **8004** Zib 192 coins / Zib IN YOUR PACK / Zib SIGNED; **8005** KillerWatt 320 coins / KillerWatt IN YOUR PACK / KillerWatt SIGNED; **8006** Leo 208 coins / Leo IN YOUR PACK / Leo SIGNED; **8007** Democratus 224 coins / Democratus IN YOUR PACK / Democratus SIGNED; **8008** Skiff Escort 128 coins / Skiff Escort IN YOUR PACK / Skiff Escort SIGNED; **8009** Apophiss 352 coins / Apophiss IN YOUR PACK / Apophiss SIGNED; **8010** Tullius 336 coins / Tullius IN YOUR PACK / Tullius SIGNED; **8011** The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK; **8012** Donado 192 coins / Donado FILED / Donado IN YOUR PACK; **8041** Knuckles 48 coins / Knuckles FILED / Knuckles IN YOUR PACK; **8042** Doc Whiskers 64 coins / Doc Whiskers FILED / Doc Whiskers IN YOUR PACK; **8043** Fingers 48 coins / Fingers FILED / Fingers IN YOUR PACK; **8044** Tick-Tock 64 coins / Tick-Tock FILED / Tick-Tock IN YOUR PACK; **8045** Boomer 64 coins / Boomer FILED / Boomer IN YOUR PACK; **9702** Call for Democratus / Send him home; **9800** « Outfits & buffs / $(r_home); **9840** « Outfits & buffs / $(r_home); **9860** « Outfits & buffs / $(r_home); **9880** « Outfits & buffs / $(r_home); **9900** « Outfits & buffs / $(r_home); **9920** « Outfits & buffs / $(r_home); **9940** « Outfits & buffs / $(r_home)

## Blocks

Ranges `p28/act` hands whole to one router (the exact-code routes are in **All codes**).

| Block | Router | Menu | Buttons | Free inside |
|---|---|---|---:|---:|
| 1000-1999 | `p28/back/act` | — | 30 | 970 |
| 2000-2099 | `p28/gate/act` | 201 | 1 | 99 |
| 3100-3199 | `p30/act` | 300 | 5 | 95 |
| 4000-4099 | `p31/bank/act` | 400 | 44 | 56 |
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
| 7740-7799 | `p103/tl/act` | — | 49 | 11 |
| 7800-7999 | `p80/act` | 7800..7999 | 100 | 100 |
| 8000-8099 | `p137/rc/act` | 8000 | 29 | 71 |
| 8301-8309 | `p128/pm/act` | 970 | 2 | 7 |
| 8411-8413 | `p86/theme/pick` | 8410 | 0 | 3 |
| 8501-8507 | `p105/desk/buy` | 8500 | 7 | 0 |
| 9701-9703 | `p97/act` | 9700 | 3 | 0 |
| 9800-9959 | `p99/act` | — | 51 | 109 |

## All codes

"Shown in" is the dialog title (or the function, for chat links and rows built in storage); "Menu" is the `bm.menu` that function opens; the route reads `p28/act` → router [the menu it insists on] → handler.

| Code | Words | Shown in | Menu | Route |
|---:|---|---|---|---|
| 2 | Keep at it | Skip this puzzle? (p122/ask_dlg) | — | (does nothing) |
| 1020 | Sealed Explorer's Map 3 Tokens | The Fence - Back Room (dialog p28/back_fence_1); The Fence - Back Room (dialog p28/back_fence_2); The Fence - Back Room (dialog p28/back_fence_3) (+1 more) | 101 | `p28/back/act` → `p28/back/act_1` [menu 101] → `p28/back/buy_1_0` |
| 1021 | Banker's Card 3 Medallions | The Fence - Back Room (dialog p28/back_fence_2); The Fence - Back Room (dialog p28/back_fence_3); The Fence - Back Room (dialog p28/back_fence_4) | 101 | `p28/back/act` → `p28/back/act_1` [menu 101] → `p28/back/buy_1_1` |
| 1022 | Smuggler's Jar 6 Medallions | The Fence - Back Room (dialog p28/back_fence_4) | 101 | `p28/back/act` → `p28/back/act_1` [menu 101] → `p28/back/buy_1_2` |
| 1040 | Fair Weather Bell 6 Tokens | Old Barnaby - Back Room (dialog p28/back_pawn_1); Old Barnaby - Back Room (dialog p28/back_pawn_2); Old Barnaby - Back Room (dialog p28/back_pawn_3) (+1 more) | 102 | `p28/back/act` → `p28/back/act_2` [menu 102] → `p28/back/buy_2_0` |
| 1041 | 2 Totems of Undying 4 Medallions | Old Barnaby - Back Room (dialog p28/back_pawn_2); Old Barnaby - Back Room (dialog p28/back_pawn_3); Old Barnaby - Back Room (dialog p28/back_pawn_4) | 102 | `p28/back/act` → `p28/back/act_2` [menu 102] → `p28/back/buy_2_1` |
| 1042 | Spawner Crowbar 8 Medallions | Old Barnaby - Back Room (dialog p28/back_pawn_4) | 102 | `p28/back/act` → `p28/back/act_2` [menu 102] → `p28/back/buy_2_2` |
| 1060 | Rat Gang Portrait 4 Tokens | Madame Velour - Back Room (dialog p28/back_outfitter_1); Madame Velour - Back Room (dialog p28/back_outfitter_2); Madame Velour - Back Room (dialog p28/back_outfitter_3) (+1 more) | 103 | `p28/back/act` → `p28/back/act_3` [menu 103] → `p28/back/buy_3_0` |
| 1061 | Donado Trophy 4 Medallions | Madame Velour - Back Room (dialog p28/back_outfitter_2); Madame Velour - Back Room (dialog p28/back_outfitter_3); Madame Velour - Back Room (dialog p28/back_outfitter_4) | 103 | `p28/back/act` → `p28/back/act_3` [menu 103] → `p28/back/buy_3_1` |
| 1062 | Brass Wing Scroll 2 Trophies | Madame Velour - Back Room (dialog p28/back_outfitter_4) | 103 | `p28/back/act` → `p28/back/act_3` [menu 103] → `p28/back/buy_3_2` |
| 1080 | 16 Spectral Arrows 3 Tokens | Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_1); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_2); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_3) (+1 more) | 104 | `p28/back/act` → `p28/back/act_4` [menu 104] → `p28/back/buy_4_0` |
| 1081 | Netherite Upgrade Template 3 Medallions | Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_2); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_3); Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_4) | 104 | `p28/back/act` → `p28/back/act_4` [menu 104] → `p28/back/buy_4_1` |
| 1082 | Showstopper Charm 2 Trophies | Vinny 'Two-Blades' - Back Room (dialog p28/back_arms_4) | 104 | `p28/back/act` → `p28/back/act_4` [menu 104] → `p28/back/buy_4_2` |
| 1100 | Lodestone Locket 8 Tokens | Sgt. Steelwhisker - Back Room (dialog p28/back_armory_1); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_2); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_3) (+1 more) | 105 | `p28/back/act` → `p28/back/act_5` [menu 105] → `p28/back/buy_5_0` |
| 1101 | 3 Wither Skeleton Skulls 4 Medallions | Sgt. Steelwhisker - Back Room (dialog p28/back_armory_2); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_3); Sgt. Steelwhisker - Back Room (dialog p28/back_armory_4) | 105 | `p28/back/act` → `p28/back/act_5` [menu 105] → `p28/back/buy_5_1` |
| 1102 | Market Crest Scroll 2 Trophies | Sgt. Steelwhisker - Back Room (dialog p28/back_armory_4) | 105 | `p28/back/act` → `p28/back/act_5` [menu 105] → `p28/back/buy_5_2` |
| 1120 | A Whole Cake 2 Tokens | Chef Fromage - Back Room (dialog p28/back_chef_1); Chef Fromage - Back Room (dialog p28/back_chef_2); Chef Fromage - Back Room (dialog p28/back_chef_3) (+1 more) | 106 | `p28/back/act` → `p28/back/act_6` [menu 106] → `p28/back/buy_6_0` |
| 1121 | Enchanted Golden Apple 6 Medallions | Chef Fromage - Back Room (dialog p28/back_chef_2); Chef Fromage - Back Room (dialog p28/back_chef_3); Chef Fromage - Back Room (dialog p28/back_chef_4) | 106 | `p28/back/act` → `p28/back/act_6` [menu 106] → `p28/back/buy_6_1` |
| 1122 | 3 Enchanted Golden Apples 2 Trophies | Chef Fromage - Back Room (dialog p28/back_chef_4) | 106 | `p28/back/act` → `p28/back/act_6` [menu 106] → `p28/back/buy_6_2` |
| 1140 | 16 Bottles o' Enchanting 3 Tokens | Prof. Whiskerton - Back Room (dialog p28/back_professor_1); Prof. Whiskerton - Back Room (dialog p28/back_professor_2); Prof. Whiskerton - Back Room (dialog p28/back_professor_3) (+1 more) | 107 | `p28/back/act` → `p28/back/act_7` [menu 107] → `p28/back/buy_7_0` |
| 1141 | Book of Mending 4 Medallions | Prof. Whiskerton - Back Room (dialog p28/back_professor_2); Prof. Whiskerton - Back Room (dialog p28/back_professor_3); Prof. Whiskerton - Back Room (dialog p28/back_professor_4) | 107 | `p28/back/act` → `p28/back/act_7` [menu 107] → `p28/back/buy_7_1` |
| 1142 | Auroral Crown 2 Trophies | Prof. Whiskerton - Back Room (dialog p28/back_professor_4) | 107 | `p28/back/act` → `p28/back/act_7` [menu 107] → `p28/back/buy_7_2` |
| 1160 | Jackpot Scratch Card 4 Lucky Tokens | Lucky Whiskers - Back Room (dialog p28/back_lucky_1); Lucky Whiskers - Back Room (dialog p28/back_lucky_2); Lucky Whiskers - Back Room (dialog p28/back_lucky_3) (+1 more) | 108 | `p28/back/act` → `p28/back/act_8` [menu 108] → `p28/back/buy_8_0` |
| 1161 | Heartstone 15 Lucky Tokens | Lucky Whiskers - Back Room (dialog p28/back_lucky_2); Lucky Whiskers - Back Room (dialog p28/back_lucky_3); Lucky Whiskers - Back Room (dialog p28/back_lucky_4) | 108 | `p28/back/act` → `p28/back/act_8` [menu 108] → `p28/back/buy_8_1` |
| 1162 | Bloomwalker Boots 2 Trophies | Lucky Whiskers - Back Room (dialog p28/back_lucky_4) | 108 | `p28/back/act` → `p28/back/act_8` [menu 108] → `p28/back/buy_8_2` |
| 1180 | Buried Treasure Map 3 Tokens | Capt. Cheddarbeard - Back Room (dialog p28/back_captain_1); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_2); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_3) (+1 more) | 109 | `p28/back/act` → `p28/back/act_9` [menu 109] → `p28/back/buy_9_0` |
| 1181 | Heart of the Sea 3 Medallions | Capt. Cheddarbeard - Back Room (dialog p28/back_captain_2); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_3); Capt. Cheddarbeard - Back Room (dialog p28/back_captain_4) | 109 | `p28/back/act` → `p28/back/act_9` [menu 109] → `p28/back/buy_9_1` |
| 1182 | Rat Familiar 2 Trophies | Capt. Cheddarbeard - Back Room (dialog p28/back_captain_4) | 109 | `p28/back/act` → `p28/back/act_9` [menu 109] → `p28/back/buy_9_2` |
| 1200 | Ominous Bottle 6 Blood Moon Crystals | The Bloodbroker - Back Room (dialog p28/back_blood_1); The Bloodbroker - Back Room (dialog p28/back_blood_2); The Bloodbroker - Back Room (dialog p28/back_blood_3) (+1 more) | 110 | `p28/back/act` → `p28/back/act_10` [menu 110] → `p28/back/buy_10_0` |
| 1201 | Nether Star 24 Blood Moon Crystals | The Bloodbroker - Back Room (dialog p28/back_blood_2); The Bloodbroker - Back Room (dialog p28/back_blood_3); The Bloodbroker - Back Room (dialog p28/back_blood_4) | 110 | `p28/back/act` → `p28/back/act_10` [menu 110] → `p28/back/buy_10_1` |
| 1202 | 3 Heartstones 1 Trophy | The Bloodbroker - Back Room (dialog p28/back_blood_4) | 110 | `p28/back/act` → `p28/back/act_10` [menu 110] → `p28/back/buy_10_2` |
| 2001 | Buy a one-night pass 2 Medallions | The Dark Auction (dialog p28/pass) | 201 | `p28/gate/act` [menu 201] → `p28/gate/buy_pass` |
| 3100 | Open the bidding | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: title) (if unless score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3101 | Bid +1 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3102 | Bid +2 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3105 | Bid +5 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 3110 | Bid +10 | The Dark Auction (p30/menu_m) | 300 | `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) (if if score #hb bm.auc matches 0) / `p30/act` [menu 300] → (inline: scoreboard) |
| 4010 | Deposit all Tokens | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_token` |
| 4011 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_token` |
| 4012 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_token` |
| 4013 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_token` |
| 4014 | Deposit all Lucky Tokens | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_lucky_token` |
| 4015 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_lucky_token` |
| 4016 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_lucky_token` |
| 4017 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_lucky_token` |
| 4018 | Deposit all Medallions | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_medallion` |
| 4019 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_medallion` |
| 4020 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_medallion` |
| 4021 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_medallion` |
| 4022 | Deposit all Trophies | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_trophy` |
| 4023 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_trophy` |
| 4024 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_trophy` |
| 4025 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_trophy` |
| 4026 | Deposit all Blood Crystals | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_blood_crystal` |
| 4027 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_blood_crystal` |
| 4028 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_blood_crystal` |
| 4029 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_blood_crystal` |
| 4030 | Deposit all Ember Scales | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_ember_scale` |
| 4031 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_ember_scale` |
| 4032 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_ember_scale` |
| 4033 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_ember_scale` |
| 4034 | Deposit all Void Shards | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_void_shard` |
| 4035 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_void_shard` |
| 4036 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_void_shard` |
| 4037 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_void_shard` |
| 4038 | Deposit all Green Xenite | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_green` |
| 4039 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_green` |
| 4040 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_green` |
| 4041 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_green` |
| 4042 | Deposit all Violet Xenite | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_violet` |
| 4043 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_violet` |
| 4044 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_violet` |
| 4045 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_violet` |
| 4046 | Deposit all Cyan Xenite | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_cyan` |
| 4047 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_cyan` |
| 4048 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_cyan` |
| 4049 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_cyan` |
| 4050 | Deposit all Red Xenite | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/dep_xenite_red` |
| 4051 | Take 1 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_red` |
| 4052 | Take 10 | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_xenite_red` |
| 4053 | Take all | The Rat Bank - your account (p31/bank/dlg) | 400 | `p31/bank/act` [menu 400] → `p31/bank/take_all_xenite_red` |
| 5001 | $(n1) $(p1) Medallions | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/buy1` |
| 5002 | $(n2) $(p2) Medallions | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/buy2` |
| 5003 | $(n3) $(p3) Medallions | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/buy3` |
| 5010 | Repair the item in my main hand 2 Medallions | The Concierge (p31/conc/dlg) | 500 | `p31/conc/act` [menu 500] → `p31/conc/repair` |
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
| 7005 | Pay a week 7 Tokens | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/pay` |
| 7006 | Call him to me | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/call` |
| 7007 | Patch him up 2 Medallions | Rufus Gnaw, rat for hire (p29/merc/dlg) | 700 | `p29/merc/act` [menu 700] → `p29/merc/patch` |
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
| 7735 | Chatter: $(chat) (all followers) | Cecil · wardrobe (p99/dlg/cecil); Celi · wardrobe (p99/dlg/celi); Democratus · wardrobe (p99/dlg/demo) (+4 more) | 9800, 9840, 9860, 9880, 9900, 9920, 9940 | `p123/chat` |
| 7740 | « The Tailor | CECIL · the Tailor (p103/tl/p_cecil_dlg); CELI · the Tailor (p103/tl/p_celi_dlg); DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) (+5 more) | 7740 | `p103/tl/act` → `p103/tl/main` |
| 7741 | Emma | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/p_emma` |
| 7742 | Celi | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/p_celi` |
| 7743 | Zib | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/p_zib` |
| 7744 | Cecil | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/p_cecil` |
| 7745 | KillerWatt | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/p_kw` |
| 7746 | Leo | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/p_leo` |
| 7747 | Democratus | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/p_demo` |
| 7748 | Display cases | THE TAILOR · outfits for your followers (p103/tl/main_dlg) | 7740 | `p103/tl/act` → `p103/tl/cases` |
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
| 7761 | Flower Top $(r_11) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b11` [menu 7740] |
| 7762 | Cozy Sweater $(r_12) | EMMA · the Tailor (p103/tl/p_emma_dlg) | 7740 | `p103/tl/act` → `p103/tl/b12` [menu 7740] |
| 7763 | Aurora $(r_13) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b13` [menu 7740] |
| 7764 | Rosehip $(r_14) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b14` [menu 7740] |
| 7765 | Midnight $(r_15) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b15` [menu 7740] |
| 7766 | Frostfire $(r_16) | CELI · the Tailor (p103/tl/p_celi_dlg) | 7740 | `p103/tl/act` → `p103/tl/b16` [menu 7740] |
| 7767 | Crimson Guard $(r_17) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b17` [menu 7740] |
| 7768 | Forest Ranger $(r_18) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b18` [menu 7740] |
| 7769 | Golden Ace $(r_19) | ZIB · the Tailor (p103/tl/p_zib_dlg) | 7740 | `p103/tl/act` → `p103/tl/b19` [menu 7740] |
| 7770 | Crimson Crusader $(r_20) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b20` [menu 7740] |
| 7771 | Royal Purple $(r_21) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b21` [menu 7740] |
| 7772 | Greenwood $(r_22) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b22` [menu 7740] |
| 7773 | Golden Champion $(r_23) | LEO · the Tailor (p103/tl/p_leo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b23` [menu 7740] |
| 7774 | Crimson Reaper $(r_24) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b24` [menu 7740] |
| 7775 | Ashen Shroud $(r_25) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b25` [menu 7740] |
| 7776 | Royal Violet $(r_26) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b26` [menu 7740] |
| 7777 | Gilded Storm $(r_27) | DEMOCRATUS · the Tailor (p103/tl/p_demo_dlg) | 7740 | `p103/tl/act` → `p103/tl/b27` [menu 7740] |
| 7778 | Crimson $(r_28) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` → `p103/tl/b28` [menu 7740] |
| 7779 | Midnight $(r_29) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` → `p103/tl/b29` [menu 7740] |
| 7780 | Bone $(r_30) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` → `p103/tl/b30` [menu 7740] |
| 7781 | Gilded $(r_31) | CECIL · the Tailor (p103/tl/p_cecil_dlg) | 7740 | `p103/tl/act` → `p103/tl/b31` [menu 7740] |
| 7782 | Midnight $(r_32) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` → `p103/tl/b32` [menu 7740] |
| 7783 | Bone $(r_33) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` → `p103/tl/b33` [menu 7740] |
| 7784 | Neon $(r_34) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` → `p103/tl/b34` [menu 7740] |
| 7785 | Golden Thunder $(r_35) | KILLERWATT · the Tailor (p103/tl/p_kw_dlg) | 7740 | `p103/tl/act` → `p103/tl/b35` [menu 7740] |
| 7790 | Oak Display Case 3 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c0` [menu 7740] |
| 7791 | Dark Oak Display Case 3 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c1` [menu 7740] |
| 7792 | Quartz Display Case 5 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c2` [menu 7740] |
| 7793 | Gilded Display Case 8 coins | DISPLAY CASES · the Tailor (p103/tl/cases_dlg) | 7740 | `p103/tl/act` → `p103/tl/c3` [menu 7740] |
| 7800 | « Office / « The Office / ◀ The Office / Stay on the job | Leave the heist? (p104/leave_ask); THE ARMORY · your kits, for good (p80/armory_dlg); THE BOND SIGILS · two at most, each heist (p81/sigils_dlg) (+4 more) | 7801, 7802, 7803, 7804, 7807, 7808 | `p80/act` [menu 7800..7999] → `p80/office` |
| 7801 | « Armory / ⚒ The Armory | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg); YOUR SECONDARY · a weapon of your own (p80/sec_dlg) (+1 more) | 7800, 7820, 7830 | `p80/act` [menu 7800..7999] → `p80/armory` |
| 7802 | « Back / Gutter Bank / ⛃ The Gutter Bank | THE ARMORY · your kits, for good (p80/armory_dlg); THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) (+4 more) | 7800, 7801, 7802 | `p80/act` [menu 7800..7999] → `p80/bank` |
| 7803 | 🏆 Trophy Case | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p81/case` |
| 7804 | ✦ Bond Sigils | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p81/sigils` |
| 7805 | ▣ The Locker Hall | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p84/lk/from_ledger` |
| 7806 | ⛁ The Crate Desk | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p86/theme/menu` |
| 7807 | « Raid Crew / ☺ Raid Crew | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg); THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800, 7950 | `p80/act` [menu 7800..7999] → `p98/crew` |
| 7808 | ◀ The Codex / 📖 The Codex | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg); THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg); 📖 Curses Lifted · $(n) of 7 (p117/cx/page3_dlg) (+4 more) | 7800, 7808 | `p80/act` [menu 7800..7999] → `p117/cx/menu` |
| 7809 | ⚑ Plan a Heist or join your party's | THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p70/plans` |
| 7811 | ⬆ Tank | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/up1` |
| 7812 | ⬆ Offense | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/up2` |
| 7813 | ⬆ Ranged | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/up3` |
| 7814 | ⬆ Support | THE ARMORY · your kits, for good (p80/armory_dlg) | 7801 | `p80/act` [menu 7800..7999] → `p80/up4` |
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
| 7841 | Take 16 coins | THE GUTTER BANK · take out coins (p80/bank_cdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_take16` |
| 7842 | Take 64 coins | THE GUTTER BANK · take out coins (p80/bank_cdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_take64` |
| 7843 | Take all my coins | THE GUTTER BANK · take out coins (p80/bank_cdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_takeall` |
| 7844 | Buy 1 Token (32) | THE GUTTER BANK · Black Market Tokens (p80/bank_tdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_buy1` |
| 7845 | Buy 10 Tokens (320) | THE GUTTER BANK · Black Market Tokens (p80/bank_tdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_buy10` |
| 7846 | ⬆ Take out coins | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_coins` |
| 7847 | ⬆ Take out spoils | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_spoils` |
| 7848 | ✦ Buy Tokens | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_tokens` |
| 7851 | Copper Cogs ($(m1)) | THE GUTTER BANK · take out spoils (p80/bank_sdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_mat` |
| 7852 | Silver Seals ($(m2)) | THE GUTTER BANK · take out spoils (p80/bank_sdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_mat` |
| 7853 | Gilded Leaves ($(m3)) | THE GUTTER BANK · take out spoils (p80/bank_sdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_mat` |
| 7854 | Deep Pearls ($(m4)) | THE GUTTER BANK · take out spoils (p80/bank_sdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_mat` |
| 7855 | Hoard Embers ($(m5)) | THE GUTTER BANK · take out spoils (p80/bank_sdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_mat` |
| 7856 | Captain's Insignia ($(m6)) | THE GUTTER BANK · take out spoils (p80/bank_sdlg) | 7802 | `p80/act` [menu 7800..7999] → `p80/bank_mat` |
| 7861 | 📖 Rooms of the Vault | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page1` |
| 7862 | 📖 Events and Secrets | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page2` |
| 7863 | 📖 Curses Lifted | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page3` |
| 7864 | 📖 Rare Finds | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page4` |
| 7865 | 📖 Masterworks | THE CODEX · what you've seen in the vault (p117/cx/menu_dlg) | 7808 | `p80/act` [menu 7800..7999] → `p117/cx/page5` |
| 7870 | ⇄ Medallions & Trophies | THE GUTTER BANK · your coins and spoils (p80/bank_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p120/bk_act` → `p120/bk_page` |
| 7871 | Take 1 Medallion | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p120/bk_act` → `p120/bk_m1` |
| 7872 | Take all Medallions | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p120/bk_act` → `p120/bk_ma` |
| 7873 | Take 1 Trophy | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p120/bk_act` → `p120/bk_t1` |
| 7874 | Take all Trophies | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p120/bk_act` → `p120/bk_ta` |
| 7875 | 16 coins → Medallion | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_c2m` |
| 7876 | 128 coins → Trophy | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_c2t` |
| 7877 | Medallion → 16 coins | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_m2c` |
| 7878 | Trophy → 128 coins | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_t2c` |
| 7879 | 8 Medallions → Trophy | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_m2t` |
| 7880 | ⌂ The Fixer's Lounge | THE FIXER'S OFFICE · everything the vault owes you (p80/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p121/from_ledger` |
| 7881 | ⏭ Skip this puzzle | THE FIXER'S OFFICE · everything the vault owes you (p104/office_dlg) | 7800 | `p80/act` [menu 7800..7999] → `p122/ask` |
| 7883 | Trophy → 8 Medallions | THE GUTTER BANK · Medallions & Trophies (p120/bk_dlg) | 7802 | `p80/act` [menu 7800..7999] → `p123/ex_act` → `p123/ex_t2m` |
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
| 7920 | The Frog | p103/crew/row_10 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/frog` |
| 7921 | Donado | p103/crew/row_11 | 7807 | `p80/act` [menu 7800..7999] → `p98/t/donado` |
| 7931 | Knuckles | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h1` |
| 7932 | Doc Whiskers | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h2` |
| 7933 | Fingers | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h3` |
| 7934 | Tick-Tock | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h4` |
| 7935 | Boomer | p103/crew/hire_rows | 7807 | `p80/act` [menu 7800..7999] → `p98/t/h5` |
| 7950 | Outfits & Emma's buff | p98/crew | 7807 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/page` |
| 7951 | Emma's wardrobe | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/emma` |
| 7952 | Celi's wardrobe | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/celi` |
| 7953 | Zib's wardrobe | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/zib` |
| 7954 | Cecil's wardrobe | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/cecil` |
| 7955 | KillerWatt's wardrobe | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/kw` |
| 7956 | Leo's wardrobe | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/leo` |
| 7957 | Democratus's wardrobe | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/wd/demo` |
| 7961 | Emma: Speed | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff1` |
| 7962 | Emma: Offense | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff2` |
| 7963 | Emma: Defense | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff3` |
| 7964 | Emma: Healing | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff4` |
| 7965 | Emma: Mining | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/buff5` |
| 7968 | Chatter on / off | OUTFITS & EMMA'S BUFF · your followers, from the Ledger (p119/page_dlg) | 7950 | `p80/act` [menu 7800..7999] → `p119/act` → `p119/hush` |
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
| 8011 | The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f10` |
| 8012 | Donado 192 coins / Donado FILED / Donado IN YOUR PACK | p137/rc/main | 8000 | `p137/rc/act` [menu 8000] → `p137/rc/f11` |
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
| 8301 | Wait here / follow me | Pearlman's Business Card (p128/pm/menu) | 970 | `p128/pm/act` [menu 970] → `p128/pm/sit` |
| 8309 | Send him home | Pearlman's Business Card (p128/pm/menu) | 970 | `p128/pm/act` [menu 970] → `p128/pm/dismiss` |
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
| 8608 | Call for Apophiss | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p131/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.apsel2]) / `p131/act` [menu 8600] → `p131/recall` (if if entity @e[type=minecraft:wolf,tag=bm.apsel2]) |
| 8609 | Send him home | The Serpent's Oath (p131/menu) | 8600 | `p131/act` [menu 8600] → `p131/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.apsel2]) |
| 8621 | Sit / follow | Tullius's Frozen Doubloon (p132/menu) | 8620 | `p132/act` [menu 8620] → `p132/sit` (if if entity @e[type=minecraft:wolf,tag=bm.tusel2]) |
| 8628 | Call for Tullius | Tullius's Frozen Doubloon (p132/menu) | 8620 | `p132/act` [menu 8620] → `p132/try_summon` (if unless entity @e[type=minecraft:wolf,tag=bm.tusel2]) / `p132/act` [menu 8620] → `p132/recall` (if if entity @e[type=minecraft:wolf,tag=bm.tusel2]) |
| 8629 | Send him home | Tullius's Frozen Doubloon (p132/menu) | 8620 | `p132/act` [menu 8620] → `p132/dismiss` (if if entity @e[type=minecraft:wolf,tag=bm.tusel2]) |
| 8641 | Sit / follow | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/sit` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8642 | Hand back my gear | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/strip` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8648 | Call for the Frog | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/try` (if unless entity @e[type=minecraft:wolf,tag=bm.fgsel]) / `p136/fg/act` [menu 8640] → `p136/fg/recall` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8649 | Send him home | Signet of the Frog Knight (p136/fg/menu) | 8640 | `p136/fg/act` [menu 8640] → `p136/fg/home` (if if entity @e[type=minecraft:wolf,tag=bm.fgsel]) |
| 8651 | Sit / follow | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/sit` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 8652 | Hand back my gear | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/strip` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 8658 | Call for Donado | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/try` (if unless entity @e[type=minecraft:wolf,tag=bm.dnsel]) / `p136/dn/act` [menu 8650] → `p136/dn/recall` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 8659 | Send him home | Donado's Collar Tag (p136/dn/menu) | 8650 | `p136/dn/act` [menu 8650] → `p136/dn/home` (if if entity @e[type=minecraft:wolf,tag=bm.dnsel]) |
| 9701 | Duel him | Democratus' Challenge (p97/menu) | 9700 | `p97/act` [menu 9700] → `p97/duel/start` |
| 9702 | Call for Democratus / Send him home | Democratus' Challenge (p97/menu) | 9700 | `p97/act` [menu 9700] → `p125/hc/demo` |
| 9703 | Wardrobe | Democratus' Challenge (p97/menu) | 9700 | `p97/act` [menu 9700] → `p119/plain/demo` |
| 9800 | « Outfits & buffs / $(r_home) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act` → `p99/act/emma` [menu 9800] → `p125/hc/emma` |
| 9802 | Pink ribbon $(r_ribbon0) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/ribbon0` |
| 9803 | Gold $(r_ribbon1) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/ribbon1` |
| 9804 | Midnight $(r_ribbon2) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/ribbon2` |
| 9805 | Mint $(r_ribbon3) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/ribbon3` |
| 9806 | Snow $(r_ribbon4) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/ribbon4` |
| 9807 | Crimson $(r_ribbon5) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/ribbon5` |
| 9808 | Phantom $(r_ribbon6) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/ribbon6` |
| 9812 | Her own dress $(r_dress0) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/dress0` |
| 9813 | Sundress $(r_dress1) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/dress1` |
| 9814 | Midnight Gown $(r_dress2) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/dress2` |
| 9815 | Sakura $(r_dress3) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/dress3` |
| 9816 | Royal Gown $(r_dress4) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/dress4` |
| 9817 | Starlight Gown $(r_dress5) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/dress5` |
| 9823 | Flower Top $(r_outfit1) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/outfit1` |
| 9824 | Cozy Sweater $(r_outfit2) | Emma · wardrobe (p119/dlg/emma); Emma · wardrobe (p99/dlg/emma) | 9800 | `p99/act` → `p99/act/emma` [menu 9800] → `p99/pick/outfit2` |
| 9840 | « Outfits & buffs / $(r_home) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act` → `p99/act/celi` [menu 9840] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act` → `p99/act/celi` [menu 9840] → `p125/hc/celi` |
| 9842 | Own clothes $(r_celi0) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act` → `p99/act/celi` [menu 9840] → `p99/pick/celi0` |
| 9843 | Aurora $(r_celi1) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act` → `p99/act/celi` [menu 9840] → `p99/pick/celi1` |
| 9844 | Rosehip $(r_celi2) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act` → `p99/act/celi` [menu 9840] → `p99/pick/celi2` |
| 9845 | Midnight $(r_celi3) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act` → `p99/act/celi` [menu 9840] → `p99/pick/celi3` |
| 9846 | Frostfire $(r_celi4) | Celi · wardrobe (p119/dlg/celi); Celi · wardrobe (p99/dlg/celi) | 9840 | `p99/act` → `p99/act/celi` [menu 9840] → `p99/pick/celi4` |
| 9860 | « Outfits & buffs / $(r_home) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act` → `p99/act/zib` [menu 9860] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act` → `p99/act/zib` [menu 9860] → `p125/hc/zib` |
| 9862 | Own clothes $(r_zib0) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act` → `p99/act/zib` [menu 9860] → `p99/pick/zib0` |
| 9863 | Crimson Guard $(r_zib1) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act` → `p99/act/zib` [menu 9860] → `p99/pick/zib1` |
| 9864 | Forest Ranger $(r_zib2) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act` → `p99/act/zib` [menu 9860] → `p99/pick/zib2` |
| 9865 | Golden Ace $(r_zib3) | Zib · wardrobe (p119/dlg/zib); Zib · wardrobe (p99/dlg/zib) | 9860 | `p99/act` → `p99/act/zib` [menu 9860] → `p99/pick/zib3` |
| 9880 | « Outfits & buffs / $(r_home) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act` → `p99/act/cecil` [menu 9880] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act` → `p99/act/cecil` [menu 9880] → `p125/hc/cecil` |
| 9882 | Own colours $(r_cecil0) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act` → `p99/act/cecil` [menu 9880] → `p99/pick/cecil0` |
| 9883 | Crimson $(r_cecil1) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act` → `p99/act/cecil` [menu 9880] → `p99/pick/cecil1` |
| 9884 | Midnight $(r_cecil2) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act` → `p99/act/cecil` [menu 9880] → `p99/pick/cecil2` |
| 9885 | Bone $(r_cecil3) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act` → `p99/act/cecil` [menu 9880] → `p99/pick/cecil3` |
| 9886 | Gilded $(r_cecil4) | Cecil · wardrobe (p119/dlg/cecil); Cecil · wardrobe (p99/dlg/cecil) | 9880 | `p99/act` → `p99/act/cecil` [menu 9880] → `p99/pick/cecil4` |
| 9900 | « Outfits & buffs / $(r_home) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act` → `p99/act/kw` [menu 9900] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act` → `p99/act/kw` [menu 9900] → `p125/hc/kw` |
| 9902 | Own colours $(r_kw0) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act` → `p99/act/kw` [menu 9900] → `p99/pick/kw0` |
| 9903 | Midnight $(r_kw1) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act` → `p99/act/kw` [menu 9900] → `p99/pick/kw1` |
| 9904 | Bone $(r_kw2) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act` → `p99/act/kw` [menu 9900] → `p99/pick/kw2` |
| 9905 | Neon $(r_kw3) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act` → `p99/act/kw` [menu 9900] → `p99/pick/kw3` |
| 9906 | Golden Thunder $(r_kw4) | KillerWatt · wardrobe (p119/dlg/kw); KillerWatt · wardrobe (p99/dlg/kw) | 9900 | `p99/act` → `p99/act/kw` [menu 9900] → `p99/pick/kw4` |
| 9920 | « Outfits & buffs / $(r_home) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act` → `p99/act/leo` [menu 9920] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act` → `p99/act/leo` [menu 9920] → `p125/hc/leo` |
| 9922 | Own clothes $(r_leo0) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act` → `p99/act/leo` [menu 9920] → `p99/pick/leo0` |
| 9923 | Crimson Crusader $(r_leo1) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act` → `p99/act/leo` [menu 9920] → `p99/pick/leo1` |
| 9924 | Royal Purple $(r_leo2) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act` → `p99/act/leo` [menu 9920] → `p99/pick/leo2` |
| 9925 | Greenwood $(r_leo3) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act` → `p99/act/leo` [menu 9920] → `p99/pick/leo3` |
| 9926 | Golden Champion $(r_leo4) | Leo · wardrobe (p119/dlg/leo); Leo · wardrobe (p99/dlg/leo) | 9920 | `p99/act` → `p99/act/leo` [menu 9920] → `p99/pick/leo4` |
| 9940 | « Outfits & buffs / $(r_home) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act` → `p99/act/demo` [menu 9940] → `p119/page` (if if entity @s[tag=bm.wdled]) / `p99/act` → `p99/act/demo` [menu 9940] → `p125/hc/demo` |
| 9942 | Own clothes $(r_demo0) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act` → `p99/act/demo` [menu 9940] → `p99/pick/demo0` |
| 9943 | Crimson Reaper $(r_demo1) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act` → `p99/act/demo` [menu 9940] → `p99/pick/demo1` |
| 9944 | Ashen Shroud $(r_demo2) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act` → `p99/act/demo` [menu 9940] → `p99/pick/demo2` |
| 9945 | Royal Violet $(r_demo3) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act` → `p99/act/demo` [menu 9940] → `p99/pick/demo3` |
| 9946 | Gilded Storm $(r_demo4) | Democratus · wardrobe (p119/dlg/demo); Democratus · wardrobe (p99/dlg/demo) | 9940 | `p99/act` → `p99/act/demo` [menu 9940] → `p99/pick/demo4` |

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
| 400 | p31/bank/open | The Rat Bank - your account |
| 500 | p31/conc/open | The Concierge |
| 600 | p29/burrow/use | Ring of Three Burrows |
| 700 | p29/merc/use | Rufus Gnaw, rat for hire |
| 900 | p33/shift/use | Dimension Shifter |
| 950 | p34/renew/use | Key of New Beginnings |
| 960 | p57/menu | Emma's Ribbon / Emma's Ribbon · the Wraithfire Heart |
| 970 | p128/pm/menu | Pearlman's Business Card |
| 1100 | p70/menu, p75/lives_menu | How many tries? / Plan a Heist |
| 1310 | p73/tp/use |  |
| 7740 | p103/tl/cases, p103/tl/main, p103/tl/p_cecil, p103/tl/p_celi, p103/tl/p_demo (+4) | CECIL · the Tailor / CELI · the Tailor / DEMOCRATUS · the Tailor |
| 7800 | p80/office | THE FIXER'S OFFICE · everything the vault owes you |
| 7801 | p80/armory | THE ARMORY · your kits, for good |
| 7802 | p120/bk_page, p80/bank, p80/bank_coins, p80/bank_spoils, p80/bank_tokens | THE GUTTER BANK · Black Market Tokens / THE GUTTER BANK · Medallions & Trophies / THE GUTTER BANK · take out coins |
| 7803 | p81/case | THE TROPHY CASE · twelve rooms, six metals |
| 7804 | p81/sigils | THE BOND SIGILS · two at most, each heist |
| 7807 | p98/crew |  |
| 7808 | p117/cx/menu, p117/cx/page1, p117/cx/page2, p117/cx/page3, p117/cx/page4 (+1) | THE CODEX · what you've seen in the vault / 📖 Curses Lifted · $(n) of 7 / 📖 Events and Secrets · $(n) of 28 |
| 7820 | p80/sec_menu | YOUR SECONDARY · a weapon of your own |
| 7830 | p80/sig_menu | YOUR SIGNATURE · an effect of your own |
| 7950 | p119/page | OUTFITS & EMMA'S BUFF · your followers, from the Ledger |
| 8000 | p137/rc/gems, p137/rc/hires, p137/rc/main |  |
| 8500 | p86/theme/menu | THE CRATE DESK · paid from your bank and pockets |
| 8600 | p131/menu | The Serpent's Oath |
| 8620 | p132/menu | Tullius's Frozen Doubloon |
| 8640 | p136/fg/menu | Signet of the Frog Knight |
| 8650 | p136/dn/menu | Donado's Collar Tag |
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

3-999, 2100-3099, 3200-3999, 4100-4999, 5100-6000, 6100-7000, 7100, 7103-7200, 7204-7300, 7314-7600, 7608-7610, 7614-7618, 7620-7710, 7713-7719, 7736-7739, 8100-8300, 8310-8410, 8414-8500, 8508-8600, 8604-8607, 8610-8620, 8622-8627, 8630-8640, 8643-8647, 8650, 8653-8657, 8660-9700, 9704-9799, 9960-9999

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
  8000 his book, 8001-8012 the follower contracts (a row only for a follower you've met - bm:met/<kind>), 8040 the hirelings'
  page and 8041-8045 theirs, 8050 the vault gems' page and 8051-8059 the gems. The rows are built in storage (bm:ui rc.acts).
<!-- /notes -->

## Revision log

### v2.77d
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
- **8641** added: Sit / follow — Signet of the Frog Knight
- **8642** added: Hand back my gear — Signet of the Frog Knight
- **8648** added: Call for the Frog — Signet of the Frog Knight
- **8649** added: Send him home — Signet of the Frog Knight
- **8651** added: Sit / follow — Donado's Collar Tag
- **8652** added: Hand back my gear — Donado's Collar Tag
- **8658** added: Call for Donado — Donado's Collar Tag
- **8659** added: Send him home — Donado's Collar Tag

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

<!-- legend-data {"base": {"1020": "Sealed Explorer's Map 3 Tokens — The Fence - Back Room", "1021": "Banker's Card 3 Medallions — The Fence - Back Room", "1022": "Smuggler's Jar 6 Medallions — The Fence - Back Room", "1040": "Fair Weather Bell 6 Tokens — Old Barnaby - Back Room", "1041": "2 Totems of Undying 4 Medallions — Old Barnaby - Back Room", "1042": "Spawner Crowbar 8 Medallions — Old Barnaby - Back Room", "1060": "Rat Gang Portrait 4 Tokens — Madame Velour - Back Room", "1061": "Donado Trophy 4 Medallions — Madame Velour - Back Room", "1062": "Brass Wing Scroll 2 Trophies — Madame Velour - Back Room", "1080": "16 Spectral Arrows 3 Tokens — Vinny 'Two-Blades' - Back Room", "1081": "Netherite Upgrade Template 3 Medallions — Vinny 'Two-Blades' - Back Room", "1082": "Showstopper Charm 2 Trophies — Vinny 'Two-Blades' - Back Room", "1100": "Lodestone Locket 8 Tokens — Sgt. Steelwhisker - Back Room", "1101": "3 Wither Skeleton Skulls 4 Medallions — Sgt. Steelwhisker - Back Room", "1102": "Market Crest Scroll 2 Trophies — Sgt. Steelwhisker - Back Room", "1120": "A Whole Cake 2 Tokens — Chef Fromage - Back Room", "1121": "Enchanted Golden Apple 6 Medallions — Chef Fromage - Back Room", "1122": "3 Enchanted Golden Apples 2 Trophies — Chef Fromage - Back Room", "1140": "16 Bottles o' Enchanting 3 Tokens — Prof. Whiskerton - Back Room", "1141": "Book of Mending 4 Medallions — Prof. Whiskerton - Back Room", "1142": "Auroral Crown 2 Trophies — Prof. Whiskerton - Back Room", "1160": "Jackpot Scratch Card 4 Lucky Tokens — Lucky Whiskers - Back Room", "1161": "Heartstone 15 Lucky Tokens — Lucky Whiskers - Back Room", "1162": "Bloomwalker Boots 2 Trophies — Lucky Whiskers - Back Room", "1180": "Buried Treasure Map 3 Tokens — Capt. Cheddarbeard - Back Room", "1181": "Heart of the Sea 3 Medallions — Capt. Cheddarbeard - Back Room", "1182": "Rat Familiar 2 Trophies — Capt. Cheddarbeard - Back Room", "1200": "Ominous Bottle 6 Blood Moon Crystals — The Bloodbroker - Back Room", "1201": "Nether Star 24 Blood Moon Crystals — The Bloodbroker - Back Room", "1202": "3 Heartstones 1 Trophy — The Bloodbroker - Back Room", "2": "Keep at it — Skip this puzzle?", "2001": "Buy a one-night pass 2 Medallions — The Dark Auction", "3100": "Open the bidding — The Dark Auction", "3101": "Bid +1 — The Dark Auction", "3102": "Bid +2 — The Dark Auction", "3105": "Bid +5 — The Dark Auction", "3110": "Bid +10 — The Dark Auction", "4010": "Deposit all Tokens — The Rat Bank - your account", "4011": "Take 1 — The Rat Bank - your account", "4012": "Take 10 — The Rat Bank - your account", "4013": "Take all — The Rat Bank - your account", "4014": "Deposit all Lucky Tokens — The Rat Bank - your account", "4015": "Take 1 — The Rat Bank - your account", "4016": "Take 10 — The Rat Bank - your account", "4017": "Take all — The Rat Bank - your account", "4018": "Deposit all Medallions — The Rat Bank - your account", "4019": "Take 1 — The Rat Bank - your account", "4020": "Take 10 — The Rat Bank - your account", "4021": "Take all — The Rat Bank - your account", "4022": "Deposit all Trophies — The Rat Bank - your account", "4023": "Take 1 — The Rat Bank - your account", "4024": "Take 10 — The Rat Bank - your account", "4025": "Take all — The Rat Bank - your account", "4026": "Deposit all Blood Crystals — The Rat Bank - your account", "4027": "Take 1 — The Rat Bank - your account", "4028": "Take 10 — The Rat Bank - your account", "4029": "Take all — The Rat Bank - your account", "4030": "Deposit all Ember Scales — The Rat Bank - your account", "4031": "Take 1 — The Rat Bank - your account", "4032": "Take 10 — The Rat Bank - your account", "4033": "Take all — The Rat Bank - your account", "4034": "Deposit all Void Shards — The Rat Bank - your account", "4035": "Take 1 — The Rat Bank - your account", "4036": "Take 10 — The Rat Bank - your account", "4037": "Take all — The Rat Bank - your account", "4038": "Deposit all Green Xenite — The Rat Bank - your account", "4039": "Take 1 — The Rat Bank - your account", "4040": "Take 10 — The Rat Bank - your account", "4041": "Take all — The Rat Bank - your account", "4042": "Deposit all Violet Xenite — The Rat Bank - your account", "4043": "Take 1 — The Rat Bank - your account", "4044": "Take 10 — The Rat Bank - your account", "4045": "Take all — The Rat Bank - your account", "4046": "Deposit all Cyan Xenite — The Rat Bank - your account", "4047": "Take 1 — The Rat Bank - your account", "4048": "Take 10 — The Rat Bank - your account", "4049": "Take all — The Rat Bank - your account", "4050": "Deposit all Red Xenite — The Rat Bank - your account", "4051": "Take 1 — The Rat Bank - your account", "4052": "Take 10 — The Rat Bank - your account", "4053": "Take all — The Rat Bank - your account", "5001": "$(n1) $(p1) Medallions — The Concierge", "5002": "$(n2) $(p2) Medallions — The Concierge", "5003": "$(n3) $(p3) Medallions — The Concierge", "5010": "Repair the item in my main hand 2 Medallions — The Concierge", "6001": "Go: $(t1) — Ring of Three Burrows", "6002": "Go: $(t2) — Ring of Three Burrows", "6003": "Go: $(t3) — Ring of Three Burrows", "6011": "Set burrow 1 here — Ring of Three Burrows", "6012": "Set burrow 2 here — Ring of Three Burrows", "6013": "Set burrow 3 here — Ring of Three Burrows", "7001": "Follow me — Rufus Gnaw, rat for hire", "7002": "Guard this spot — Rufus Gnaw, rat for hire", "7003": "Follow and scavenge — Rufus Gnaw, rat for hire", "7004": "Hand over the loot — Rufus Gnaw, rat for hire", "7005": "Pay a week 7 Tokens — Rufus Gnaw, rat for hire", "7006": "Call him to me — Rufus Gnaw, rat for hire", "7007": "Patch him up 2 Medallions — Rufus Gnaw, rat for hire", "7101": "Yes - start over — Key of New Beginnings", "7102": "No — Key of New Beginnings", "7201": "The Overworld — Dimension Shifter", "7202": "The Nether — Dimension Shifter", "7203": "The End — Dimension Shifter", "7301": "Speed — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7302": "Offense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7303": "Defense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7304": "Healing — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7305": "Mining — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7306": "Wardrobe — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7307": "Wraithfire Form: on / off — Emma's Ribbon · the Wraithfire Heart", "7308": "Take back the heart — Emma's Ribbon · the Wraithfire Heart", "7309": "Send her home — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7310": "Fly with me — Emma's Ribbon · the Wraithfire Heart", "7311": "Style: Guardian — Emma's Ribbon · the Wraithfire Heart", "7312": "Style: Huntress — Emma's Ribbon · the Wraithfire Heart", "7313": "Style: Tempest — Emma's Ribbon · the Wraithfire Heart", "7601": "Tier I The Copper Strongroom — Plan a Heist", "7602": "Tier II The Silver Vaults — Plan a Heist", "7603": "Tier III The Gold Reserve — Plan a Heist", "7604": "Tier IV The Diamond Deposit — Plan a Heist", "7605": "Tier V The Gutter King's Hoard — Plan a Heist", "7606": "THE ENDLESS VAULT rooms without end — Plan a Heist", "7607": "THE PIT an arena of waves — Plan a Heist", "7611": "3 TRIES +1 to +4 shares (by tier) - for the bold — How many tries?", "7612": "5 TRIES +0 to +2 shares (by tier) — How many tries?", "7613": "7 TRIES no bonus - for a first try — How many tries?", "7619": "ALARM: $(al) (click to switch) — How many tries?", "7711": "[Accept] — p73/tp/ask_bring, p73/tp/ask_go", "7712": "[Deny] — p73/tp/ask_bring, p73/tp/ask_go", "7720": "Back to the Overworld / [Back to the Overworld] — The heist is over, p101/ask_lead", "7721": "Start a new raid / [Start a new raid] — The heist is over, p101/ask_lead", "7722": "Count me in / [Count me in] — Another job?, p101/offer", "7723": "Head home / [Head home] — Another job?, p101/offer", "7724": "Leave now — Leave the heist?", "7725": "Stay — Leave the heist?", "7726": "Head home now / [Head home now] — The heist is over, p101/wait_note", "7727": "I'm in if we go again / [I'm in if we go again] — The heist is over, p101/wait_note", "7728": "The Fixer's Office — The heist is over", "7729": "Leave now — Leave the heist?", "7730": "Go to the Lounge — The heist is over", "7731": "Go to the Lounge — The heist is over", "7732": "Go to the Lounge — Another job?", "7733": "[Skip this puzzle - costs a try] — p122/offer", "7734": "Skip it (costs a try) — Skip this puzzle?", "7735": "Chatter: $(chat) (all followers) — Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Emma · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Zib · wardrobe", "7740": "« The Tailor — CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DISPLAY CASES · the Tailor, EMMA · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, ZIB · the Tailor", "7741": "Emma — THE TAILOR · outfits for your followers", "7742": "Celi — THE TAILOR · outfits for your followers", "7743": "Zib — THE TAILOR · outfits for your followers", "7744": "Cecil — THE TAILOR · outfits for your followers", "7745": "KillerWatt — THE TAILOR · outfits for your followers", "7746": "Leo — THE TAILOR · outfits for your followers", "7747": "Democratus — THE TAILOR · outfits for your followers", "7748": "Display cases — THE TAILOR · outfits for your followers", "7750": "Gold $(r_0) — EMMA · the Tailor", "7751": "Midnight $(r_1) — EMMA · the Tailor", "7752": "Mint $(r_2) — EMMA · the Tailor", "7753": "Snow $(r_3) — EMMA · the Tailor", "7754": "Crimson $(r_4) — EMMA · the Tailor", "7755": "Phantom $(r_5) — EMMA · the Tailor", "7756": "Sundress $(r_6) — EMMA · the Tailor", "7757": "Midnight Gown $(r_7) — EMMA · the Tailor", "7758": "Sakura $(r_8) — EMMA · the Tailor", "7759": "Royal Gown $(r_9) — EMMA · the Tailor", "7760": "Starlight Gown $(r_10) — EMMA · the Tailor", "7761": "Flower Top $(r_11) — EMMA · the Tailor", "7762": "Cozy Sweater $(r_12) — EMMA · the Tailor", "7763": "Aurora $(r_13) — CELI · the Tailor", "7764": "Rosehip $(r_14) — CELI · the Tailor", "7765": "Midnight $(r_15) — CELI · the Tailor", "7766": "Frostfire $(r_16) — CELI · the Tailor", "7767": "Crimson Guard $(r_17) — ZIB · the Tailor", "7768": "Forest Ranger $(r_18) — ZIB · the Tailor", "7769": "Golden Ace $(r_19) — ZIB · the Tailor", "7770": "Crimson Crusader $(r_20) — LEO · the Tailor", "7771": "Royal Purple $(r_21) — LEO · the Tailor", "7772": "Greenwood $(r_22) — LEO · the Tailor", "7773": "Golden Champion $(r_23) — LEO · the Tailor", "7774": "Crimson Reaper $(r_24) — DEMOCRATUS · the Tailor", "7775": "Ashen Shroud $(r_25) — DEMOCRATUS · the Tailor", "7776": "Royal Violet $(r_26) — DEMOCRATUS · the Tailor", "7777": "Gilded Storm $(r_27) — DEMOCRATUS · the Tailor", "7778": "Crimson $(r_28) — CECIL · the Tailor", "7779": "Midnight $(r_29) — CECIL · the Tailor", "7780": "Bone $(r_30) — CECIL · the Tailor", "7781": "Gilded $(r_31) — CECIL · the Tailor", "7782": "Midnight $(r_32) — KILLERWATT · the Tailor", "7783": "Bone $(r_33) — KILLERWATT · the Tailor", "7784": "Neon $(r_34) — KILLERWATT · the Tailor", "7785": "Golden Thunder $(r_35) — KILLERWATT · the Tailor", "7790": "Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7791": "Dark Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7792": "Quartz Display Case 5 coins — DISPLAY CASES · the Tailor", "7793": "Gilded Display Case 8 coins — DISPLAY CASES · the Tailor", "7800": "Stay on the job / « Office / « The Office / ◀ The Office — Leave the heist?, THE ARMORY · your kits, for good, THE BOND SIGILS · two at most, each heist, THE CODEX · what you've seen in the vault, THE GUTTER BANK · your coins and spoils, THE TROPHY CASE · twelve rooms, six metals, p98/crew", "7801": "« Armory / ⚒ The Armory — THE FIXER'S OFFICE · everything the vault owes you, YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own", "7802": "Gutter Bank / « Back / ⛃ The Gutter Bank — THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies, THE GUTTER BANK · take out coins, THE GUTTER BANK · take out spoils", "7803": "🏆 Trophy Case — THE FIXER'S OFFICE · everything the vault owes you", "7804": "✦ Bond Sigils — THE FIXER'S OFFICE · everything the vault owes you", "7805": "▣ The Locker Hall — THE FIXER'S OFFICE · everything the vault owes you", "7806": "⛁ The Crate Desk — THE FIXER'S OFFICE · everything the vault owes you", "7807": "« Raid Crew / ☺ Raid Crew — OUTFITS & EMMA'S BUFF · your followers, from the Ledger, THE FIXER'S OFFICE · everything the vault owes you", "7808": "◀ The Codex / 📖 The Codex — THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 23", "7809": "⚑ Plan a Heist or join your party's — THE FIXER'S OFFICE · everything the vault owes you", "7811": "⬆ Tank — THE ARMORY · your kits, for good", "7812": "⬆ Offense — THE ARMORY · your kits, for good", "7813": "⬆ Ranged — THE ARMORY · your kits, for good", "7814": "⬆ Support — THE ARMORY · your kits, for good", "7819": "none — YOUR SIGNATURE · an effect of your own", "7820": "Secondary weapon — THE ARMORY · your kits, for good", "7821": "$(r_l0) — YOUR SECONDARY · a weapon of your own", "7822": "$(r_l1) — YOUR SECONDARY · a weapon of your own", "7823": "$(r_l2) — YOUR SECONDARY · a weapon of your own", "7824": "$(r_l3) — YOUR SECONDARY · a weapon of your own", "7825": "$(r_l4) — YOUR SECONDARY · a weapon of your own", "7826": "$(r_l5) — YOUR SECONDARY · a weapon of your own", "7827": "$(r_l6) — YOUR SECONDARY · a weapon of your own", "7828": "$(r_l7) — YOUR SECONDARY · a weapon of your own", "7829": "none — YOUR SECONDARY · a weapon of your own", "7830": "Signature effect — THE ARMORY · your kits, for good", "7831": "$(r_l0) — YOUR SIGNATURE · an effect of your own", "7832": "$(r_l1) — YOUR SIGNATURE · an effect of your own", "7833": "$(r_l2) — YOUR SIGNATURE · an effect of your own", "7834": "$(r_l3) — YOUR SIGNATURE · an effect of your own", "7835": "$(r_l4) — YOUR SIGNATURE · an effect of your own", "7836": "$(r_l5) — YOUR SIGNATURE · an effect of your own", "7837": "$(r_l6) — YOUR SIGNATURE · an effect of your own", "7838": "$(r_l7) — YOUR SIGNATURE · an effect of your own", "7839": "$(r_l8) — YOUR SIGNATURE · an effect of your own", "7840": "⬇ Deposit everything — THE GUTTER BANK · your coins and spoils", "7841": "Take 16 coins — THE GUTTER BANK · take out coins", "7842": "Take 64 coins — THE GUTTER BANK · take out coins", "7843": "Take all my coins — THE GUTTER BANK · take out coins", "7844": "Buy 1 Token (32) — THE GUTTER BANK · Black Market Tokens", "7845": "Buy 10 Tokens (320) — THE GUTTER BANK · Black Market Tokens", "7846": "⬆ Take out coins — THE GUTTER BANK · your coins and spoils", "7847": "⬆ Take out spoils — THE GUTTER BANK · your coins and spoils", "7848": "✦ Buy Tokens — THE GUTTER BANK · your coins and spoils", "7851": "Copper Cogs ($(m1)) — THE GUTTER BANK · take out spoils", "7852": "Silver Seals ($(m2)) — THE GUTTER BANK · take out spoils", "7853": "Gilded Leaves ($(m3)) — THE GUTTER BANK · take out spoils", "7854": "Deep Pearls ($(m4)) — THE GUTTER BANK · take out spoils", "7855": "Hoard Embers ($(m5)) — THE GUTTER BANK · take out spoils", "7856": "Captain's Insignia ($(m6)) — THE GUTTER BANK · take out spoils", "7861": "📖 Rooms of the Vault — THE CODEX · what you've seen in the vault", "7862": "📖 Events and Secrets — THE CODEX · what you've seen in the vault", "7863": "📖 Curses Lifted — THE CODEX · what you've seen in the vault", "7864": "📖 Rare Finds — THE CODEX · what you've seen in the vault", "7865": "📖 Masterworks — THE CODEX · what you've seen in the vault", "7870": "⇄ Medallions & Trophies — THE GUTTER BANK · your coins and spoils", "7871": "Take 1 Medallion — THE GUTTER BANK · Medallions & Trophies", "7872": "Take all Medallions — THE GUTTER BANK · Medallions & Trophies", "7873": "Take 1 Trophy — THE GUTTER BANK · Medallions & Trophies", "7874": "Take all Trophies — THE GUTTER BANK · Medallions & Trophies", "7875": "16 coins → Medallion — THE GUTTER BANK · Medallions & Trophies", "7876": "128 coins → Trophy — THE GUTTER BANK · Medallions & Trophies", "7877": "Medallion → 16 coins — THE GUTTER BANK · Medallions & Trophies", "7878": "Trophy → 128 coins — THE GUTTER BANK · Medallions & Trophies", "7879": "8 Medallions → Trophy — THE GUTTER BANK · Medallions & Trophies", "7880": "⌂ The Fixer's Lounge — THE FIXER'S OFFICE · everything the vault owes you", "7881": "⏭ Skip this puzzle — THE FIXER'S OFFICE · everything the vault owes you", "7883": "Trophy → 8 Medallions — THE GUTTER BANK · Medallions & Trophies", "7899": "⏏ Leave the heist — THE FIXER'S OFFICE · everything the vault owes you", "7900": "Cecil — p103/crew/row_0", "7901": "Emma — p103/crew/row_1", "7902": "Celi — p103/crew/row_2", "7903": "Zib — p103/crew/row_3", "7904": "KillerWatt — p103/crew/row_4", "7905": "Leo — p103/crew/row_5", "7906": "Democratus — p103/crew/row_6", "7907": "Skiff Escort — p103/crew/row_7", "7908": "Apophiss — p103/crew/row_8", "7909": "Tullius — p103/crew/row_9", "7920": "The Frog — p103/crew/row_10", "7921": "Donado — p103/crew/row_11", "7931": "Knuckles — p103/crew/hire_rows", "7932": "Doc Whiskers — p103/crew/hire_rows", "7933": "Fingers — p103/crew/hire_rows", "7934": "Tick-Tock — p103/crew/hire_rows", "7935": "Boomer — p103/crew/hire_rows", "7950": "Outfits & Emma's buff — p98/crew", "7951": "Emma's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7952": "Celi's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7953": "Zib's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7954": "Cecil's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7955": "KillerWatt's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7956": "Leo's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7957": "Democratus's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7961": "Emma: Speed — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7962": "Emma: Offense — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7963": "Emma: Defense — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7964": "Emma: Healing — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7965": "Emma: Mining — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7968": "Chatter on / off — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "8301": "Wait here / follow me — Pearlman's Business Card", "8309": "Send him home — Pearlman's Business Card", "8501": "Raw Materials Crate 16 coins — THE CRATE DESK · paid from your bank and pockets", "8502": "Adventurer's Crate 32 coins — THE CRATE DESK · paid from your bank and pockets", "8503": "Mineral Crate 48 coins — THE CRATE DESK · paid from your bank and pockets", "8504": "Crimson Tip-off 64 coins — THE CRATE DESK · paid from your bank and pockets", "8505": "Vorn Signal 64 coins — THE CRATE DESK · paid from your bank and pockets", "8506": "Stone Crate 6 coins — THE CRATE DESK · paid from your bank and pockets", "8507": "Timber Crate 8 coins — THE CRATE DESK · paid from your bank and pockets", "8601": "Sit / follow — The Serpent's Oath", "8602": "Ride him — The Serpent's Oath", "8603": "Take off the saddle — The Serpent's Oath", "8608": "Call for Apophiss — The Serpent's Oath", "8609": "Send him home — The Serpent's Oath", "8621": "Sit / follow — Tullius's Frozen Doubloon", "8628": "Call for Tullius — Tullius's Frozen Doubloon", "8629": "Send him home — Tullius's Frozen Doubloon", "9701": "Duel him — Democratus' Challenge", "9702": "Call for Democratus / Send him home — Democratus' Challenge", "9703": "Wardrobe — Democratus' Challenge", "9800": "$(r_home) / « Outfits & buffs — Emma · wardrobe", "9802": "Pink ribbon $(r_ribbon0) — Emma · wardrobe", "9803": "Gold $(r_ribbon1) — Emma · wardrobe", "9804": "Midnight $(r_ribbon2) — Emma · wardrobe", "9805": "Mint $(r_ribbon3) — Emma · wardrobe", "9806": "Snow $(r_ribbon4) — Emma · wardrobe", "9807": "Crimson $(r_ribbon5) — Emma · wardrobe", "9808": "Phantom $(r_ribbon6) — Emma · wardrobe", "9812": "Her own dress $(r_dress0) — Emma · wardrobe", "9813": "Sundress $(r_dress1) — Emma · wardrobe", "9814": "Midnight Gown $(r_dress2) — Emma · wardrobe", "9815": "Sakura $(r_dress3) — Emma · wardrobe", "9816": "Royal Gown $(r_dress4) — Emma · wardrobe", "9817": "Starlight Gown $(r_dress5) — Emma · wardrobe", "9823": "Flower Top $(r_outfit1) — Emma · wardrobe", "9824": "Cozy Sweater $(r_outfit2) — Emma · wardrobe", "9840": "$(r_home) / « Outfits & buffs — Celi · wardrobe", "9842": "Own clothes $(r_celi0) — Celi · wardrobe", "9843": "Aurora $(r_celi1) — Celi · wardrobe", "9844": "Rosehip $(r_celi2) — Celi · wardrobe", "9845": "Midnight $(r_celi3) — Celi · wardrobe", "9846": "Frostfire $(r_celi4) — Celi · wardrobe", "9860": "$(r_home) / « Outfits & buffs — Zib · wardrobe", "9862": "Own clothes $(r_zib0) — Zib · wardrobe", "9863": "Crimson Guard $(r_zib1) — Zib · wardrobe", "9864": "Forest Ranger $(r_zib2) — Zib · wardrobe", "9865": "Golden Ace $(r_zib3) — Zib · wardrobe", "9880": "$(r_home) / « Outfits & buffs — Cecil · wardrobe", "9882": "Own colours $(r_cecil0) — Cecil · wardrobe", "9883": "Crimson $(r_cecil1) — Cecil · wardrobe", "9884": "Midnight $(r_cecil2) — Cecil · wardrobe", "9885": "Bone $(r_cecil3) — Cecil · wardrobe", "9886": "Gilded $(r_cecil4) — Cecil · wardrobe", "9900": "$(r_home) / « Outfits & buffs — KillerWatt · wardrobe", "9902": "Own colours $(r_kw0) — KillerWatt · wardrobe", "9903": "Midnight $(r_kw1) — KillerWatt · wardrobe", "9904": "Bone $(r_kw2) — KillerWatt · wardrobe", "9905": "Neon $(r_kw3) — KillerWatt · wardrobe", "9906": "Golden Thunder $(r_kw4) — KillerWatt · wardrobe", "9920": "$(r_home) / « Outfits & buffs — Leo · wardrobe", "9922": "Own clothes $(r_leo0) — Leo · wardrobe", "9923": "Crimson Crusader $(r_leo1) — Leo · wardrobe", "9924": "Royal Purple $(r_leo2) — Leo · wardrobe", "9925": "Greenwood $(r_leo3) — Leo · wardrobe", "9926": "Golden Champion $(r_leo4) — Leo · wardrobe", "9940": "$(r_home) / « Outfits & buffs — Democratus · wardrobe", "9942": "Own clothes $(r_demo0) — Democratus · wardrobe", "9943": "Crimson Reaper $(r_demo1) — Democratus · wardrobe", "9944": "Ashen Shroud $(r_demo2) — Democratus · wardrobe", "9945": "Royal Violet $(r_demo3) — Democratus · wardrobe", "9946": "Gilded Storm $(r_demo4) — Democratus · wardrobe"}, "now": {"1020": "Sealed Explorer's Map 3 Tokens — The Fence - Back Room", "1021": "Banker's Card 3 Medallions — The Fence - Back Room", "1022": "Smuggler's Jar 6 Medallions — The Fence - Back Room", "1040": "Fair Weather Bell 6 Tokens — Old Barnaby - Back Room", "1041": "2 Totems of Undying 4 Medallions — Old Barnaby - Back Room", "1042": "Spawner Crowbar 8 Medallions — Old Barnaby - Back Room", "1060": "Rat Gang Portrait 4 Tokens — Madame Velour - Back Room", "1061": "Donado Trophy 4 Medallions — Madame Velour - Back Room", "1062": "Brass Wing Scroll 2 Trophies — Madame Velour - Back Room", "1080": "16 Spectral Arrows 3 Tokens — Vinny 'Two-Blades' - Back Room", "1081": "Netherite Upgrade Template 3 Medallions — Vinny 'Two-Blades' - Back Room", "1082": "Showstopper Charm 2 Trophies — Vinny 'Two-Blades' - Back Room", "1100": "Lodestone Locket 8 Tokens — Sgt. Steelwhisker - Back Room", "1101": "3 Wither Skeleton Skulls 4 Medallions — Sgt. Steelwhisker - Back Room", "1102": "Market Crest Scroll 2 Trophies — Sgt. Steelwhisker - Back Room", "1120": "A Whole Cake 2 Tokens — Chef Fromage - Back Room", "1121": "Enchanted Golden Apple 6 Medallions — Chef Fromage - Back Room", "1122": "3 Enchanted Golden Apples 2 Trophies — Chef Fromage - Back Room", "1140": "16 Bottles o' Enchanting 3 Tokens — Prof. Whiskerton - Back Room", "1141": "Book of Mending 4 Medallions — Prof. Whiskerton - Back Room", "1142": "Auroral Crown 2 Trophies — Prof. Whiskerton - Back Room", "1160": "Jackpot Scratch Card 4 Lucky Tokens — Lucky Whiskers - Back Room", "1161": "Heartstone 15 Lucky Tokens — Lucky Whiskers - Back Room", "1162": "Bloomwalker Boots 2 Trophies — Lucky Whiskers - Back Room", "1180": "Buried Treasure Map 3 Tokens — Capt. Cheddarbeard - Back Room", "1181": "Heart of the Sea 3 Medallions — Capt. Cheddarbeard - Back Room", "1182": "Rat Familiar 2 Trophies — Capt. Cheddarbeard - Back Room", "1200": "Ominous Bottle 6 Blood Moon Crystals — The Bloodbroker - Back Room", "1201": "Nether Star 24 Blood Moon Crystals — The Bloodbroker - Back Room", "1202": "3 Heartstones 1 Trophy — The Bloodbroker - Back Room", "2": "Keep at it — Skip this puzzle?", "2001": "Buy a one-night pass 2 Medallions — The Dark Auction", "3100": "Open the bidding — The Dark Auction", "3101": "Bid +1 — The Dark Auction", "3102": "Bid +2 — The Dark Auction", "3105": "Bid +5 — The Dark Auction", "3110": "Bid +10 — The Dark Auction", "4010": "Deposit all Tokens — The Rat Bank - your account", "4011": "Take 1 — The Rat Bank - your account", "4012": "Take 10 — The Rat Bank - your account", "4013": "Take all — The Rat Bank - your account", "4014": "Deposit all Lucky Tokens — The Rat Bank - your account", "4015": "Take 1 — The Rat Bank - your account", "4016": "Take 10 — The Rat Bank - your account", "4017": "Take all — The Rat Bank - your account", "4018": "Deposit all Medallions — The Rat Bank - your account", "4019": "Take 1 — The Rat Bank - your account", "4020": "Take 10 — The Rat Bank - your account", "4021": "Take all — The Rat Bank - your account", "4022": "Deposit all Trophies — The Rat Bank - your account", "4023": "Take 1 — The Rat Bank - your account", "4024": "Take 10 — The Rat Bank - your account", "4025": "Take all — The Rat Bank - your account", "4026": "Deposit all Blood Crystals — The Rat Bank - your account", "4027": "Take 1 — The Rat Bank - your account", "4028": "Take 10 — The Rat Bank - your account", "4029": "Take all — The Rat Bank - your account", "4030": "Deposit all Ember Scales — The Rat Bank - your account", "4031": "Take 1 — The Rat Bank - your account", "4032": "Take 10 — The Rat Bank - your account", "4033": "Take all — The Rat Bank - your account", "4034": "Deposit all Void Shards — The Rat Bank - your account", "4035": "Take 1 — The Rat Bank - your account", "4036": "Take 10 — The Rat Bank - your account", "4037": "Take all — The Rat Bank - your account", "4038": "Deposit all Green Xenite — The Rat Bank - your account", "4039": "Take 1 — The Rat Bank - your account", "4040": "Take 10 — The Rat Bank - your account", "4041": "Take all — The Rat Bank - your account", "4042": "Deposit all Violet Xenite — The Rat Bank - your account", "4043": "Take 1 — The Rat Bank - your account", "4044": "Take 10 — The Rat Bank - your account", "4045": "Take all — The Rat Bank - your account", "4046": "Deposit all Cyan Xenite — The Rat Bank - your account", "4047": "Take 1 — The Rat Bank - your account", "4048": "Take 10 — The Rat Bank - your account", "4049": "Take all — The Rat Bank - your account", "4050": "Deposit all Red Xenite — The Rat Bank - your account", "4051": "Take 1 — The Rat Bank - your account", "4052": "Take 10 — The Rat Bank - your account", "4053": "Take all — The Rat Bank - your account", "5001": "$(n1) $(p1) Medallions — The Concierge", "5002": "$(n2) $(p2) Medallions — The Concierge", "5003": "$(n3) $(p3) Medallions — The Concierge", "5010": "Repair the item in my main hand 2 Medallions — The Concierge", "6001": "Go: $(t1) — Ring of Three Burrows", "6002": "Go: $(t2) — Ring of Three Burrows", "6003": "Go: $(t3) — Ring of Three Burrows", "6011": "Set burrow 1 here — Ring of Three Burrows", "6012": "Set burrow 2 here — Ring of Three Burrows", "6013": "Set burrow 3 here — Ring of Three Burrows", "7001": "Follow me — Rufus Gnaw, rat for hire", "7002": "Guard this spot — Rufus Gnaw, rat for hire", "7003": "Follow and scavenge — Rufus Gnaw, rat for hire", "7004": "Hand over the loot — Rufus Gnaw, rat for hire", "7005": "Pay a week 7 Tokens — Rufus Gnaw, rat for hire", "7006": "Call him to me — Rufus Gnaw, rat for hire", "7007": "Patch him up 2 Medallions — Rufus Gnaw, rat for hire", "7101": "Yes - start over — Key of New Beginnings", "7102": "No — Key of New Beginnings", "7201": "The Overworld — Dimension Shifter", "7202": "The Nether — Dimension Shifter", "7203": "The End — Dimension Shifter", "7301": "Speed — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7302": "Offense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7303": "Defense — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7304": "Healing — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7305": "Mining — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7306": "Wardrobe — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7307": "Wraithfire Form: on / off — Emma's Ribbon · the Wraithfire Heart", "7308": "Take back the heart — Emma's Ribbon · the Wraithfire Heart", "7309": "Send her home — Emma's Ribbon, Emma's Ribbon · the Wraithfire Heart", "7310": "Fly with me — Emma's Ribbon · the Wraithfire Heart", "7311": "Style: Guardian — Emma's Ribbon · the Wraithfire Heart", "7312": "Style: Huntress — Emma's Ribbon · the Wraithfire Heart", "7313": "Style: Tempest — Emma's Ribbon · the Wraithfire Heart", "7601": "Tier I The Copper Strongroom — Plan a Heist", "7602": "Tier II The Silver Vaults — Plan a Heist", "7603": "Tier III The Gold Reserve — Plan a Heist", "7604": "Tier IV The Diamond Deposit — Plan a Heist", "7605": "Tier V The Gutter King's Hoard — Plan a Heist", "7606": "THE ENDLESS VAULT rooms without end — Plan a Heist", "7607": "THE PIT an arena of waves — Plan a Heist", "7611": "3 TRIES +1 to +4 shares (by tier) - for the bold — How many tries?", "7612": "5 TRIES +0 to +2 shares (by tier) — How many tries?", "7613": "7 TRIES no bonus - for a first try — How many tries?", "7619": "ALARM: $(al) (click to switch) — How many tries?", "7711": "[Accept] — p73/tp/ask_bring, p73/tp/ask_go", "7712": "[Deny] — p73/tp/ask_bring, p73/tp/ask_go", "7720": "Back to the Overworld / [Back to the Overworld] — The heist is over, p101/ask_lead", "7721": "Start a new raid / [Start a new raid] — The heist is over, p101/ask_lead", "7722": "Count me in / [Count me in] — Another job?, p101/offer", "7723": "Head home / [Head home] — Another job?, p101/offer", "7724": "Leave now — Leave the heist?", "7725": "Stay — Leave the heist?", "7726": "Head home now / [Head home now] — The heist is over, p101/wait_note", "7727": "I'm in if we go again / [I'm in if we go again] — The heist is over, p101/wait_note", "7728": "The Fixer's Office — The heist is over", "7729": "Leave now — Leave the heist?", "7730": "Go to the Lounge — The heist is over", "7731": "Go to the Lounge — The heist is over", "7732": "Go to the Lounge — Another job?", "7733": "[Skip this puzzle - costs a try] — p122/offer", "7734": "Skip it (costs a try) — Skip this puzzle?", "7735": "Chatter: $(chat) (all followers) — Cecil · wardrobe, Celi · wardrobe, Democratus · wardrobe, Emma · wardrobe, KillerWatt · wardrobe, Leo · wardrobe, Zib · wardrobe", "7740": "« The Tailor — CECIL · the Tailor, CELI · the Tailor, DEMOCRATUS · the Tailor, DISPLAY CASES · the Tailor, EMMA · the Tailor, KILLERWATT · the Tailor, LEO · the Tailor, ZIB · the Tailor", "7741": "Emma — THE TAILOR · outfits for your followers", "7742": "Celi — THE TAILOR · outfits for your followers", "7743": "Zib — THE TAILOR · outfits for your followers", "7744": "Cecil — THE TAILOR · outfits for your followers", "7745": "KillerWatt — THE TAILOR · outfits for your followers", "7746": "Leo — THE TAILOR · outfits for your followers", "7747": "Democratus — THE TAILOR · outfits for your followers", "7748": "Display cases — THE TAILOR · outfits for your followers", "7750": "Gold $(r_0) — EMMA · the Tailor", "7751": "Midnight $(r_1) — EMMA · the Tailor", "7752": "Mint $(r_2) — EMMA · the Tailor", "7753": "Snow $(r_3) — EMMA · the Tailor", "7754": "Crimson $(r_4) — EMMA · the Tailor", "7755": "Phantom $(r_5) — EMMA · the Tailor", "7756": "Sundress $(r_6) — EMMA · the Tailor", "7757": "Midnight Gown $(r_7) — EMMA · the Tailor", "7758": "Sakura $(r_8) — EMMA · the Tailor", "7759": "Royal Gown $(r_9) — EMMA · the Tailor", "7760": "Starlight Gown $(r_10) — EMMA · the Tailor", "7761": "Flower Top $(r_11) — EMMA · the Tailor", "7762": "Cozy Sweater $(r_12) — EMMA · the Tailor", "7763": "Aurora $(r_13) — CELI · the Tailor", "7764": "Rosehip $(r_14) — CELI · the Tailor", "7765": "Midnight $(r_15) — CELI · the Tailor", "7766": "Frostfire $(r_16) — CELI · the Tailor", "7767": "Crimson Guard $(r_17) — ZIB · the Tailor", "7768": "Forest Ranger $(r_18) — ZIB · the Tailor", "7769": "Golden Ace $(r_19) — ZIB · the Tailor", "7770": "Crimson Crusader $(r_20) — LEO · the Tailor", "7771": "Royal Purple $(r_21) — LEO · the Tailor", "7772": "Greenwood $(r_22) — LEO · the Tailor", "7773": "Golden Champion $(r_23) — LEO · the Tailor", "7774": "Crimson Reaper $(r_24) — DEMOCRATUS · the Tailor", "7775": "Ashen Shroud $(r_25) — DEMOCRATUS · the Tailor", "7776": "Royal Violet $(r_26) — DEMOCRATUS · the Tailor", "7777": "Gilded Storm $(r_27) — DEMOCRATUS · the Tailor", "7778": "Crimson $(r_28) — CECIL · the Tailor", "7779": "Midnight $(r_29) — CECIL · the Tailor", "7780": "Bone $(r_30) — CECIL · the Tailor", "7781": "Gilded $(r_31) — CECIL · the Tailor", "7782": "Midnight $(r_32) — KILLERWATT · the Tailor", "7783": "Bone $(r_33) — KILLERWATT · the Tailor", "7784": "Neon $(r_34) — KILLERWATT · the Tailor", "7785": "Golden Thunder $(r_35) — KILLERWATT · the Tailor", "7790": "Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7791": "Dark Oak Display Case 3 coins — DISPLAY CASES · the Tailor", "7792": "Quartz Display Case 5 coins — DISPLAY CASES · the Tailor", "7793": "Gilded Display Case 8 coins — DISPLAY CASES · the Tailor", "7800": "Stay on the job / « Office / « The Office / ◀ The Office — Leave the heist?, THE ARMORY · your kits, for good, THE BOND SIGILS · two at most, each heist, THE CODEX · what you've seen in the vault, THE GUTTER BANK · your coins and spoils, THE TROPHY CASE · twelve rooms, six metals, p98/crew", "7801": "« Armory / ⚒ The Armory — THE FIXER'S OFFICE · everything the vault owes you, YOUR SECONDARY · a weapon of your own, YOUR SIGNATURE · an effect of your own", "7802": "Gutter Bank / « Back / ⛃ The Gutter Bank — THE ARMORY · your kits, for good, THE FIXER'S OFFICE · everything the vault owes you, THE GUTTER BANK · Black Market Tokens, THE GUTTER BANK · Medallions & Trophies, THE GUTTER BANK · take out coins, THE GUTTER BANK · take out spoils", "7803": "🏆 Trophy Case — THE FIXER'S OFFICE · everything the vault owes you", "7804": "✦ Bond Sigils — THE FIXER'S OFFICE · everything the vault owes you", "7805": "▣ The Locker Hall — THE FIXER'S OFFICE · everything the vault owes you", "7806": "⛁ The Crate Desk — THE FIXER'S OFFICE · everything the vault owes you", "7807": "« Raid Crew / ☺ Raid Crew — OUTFITS & EMMA'S BUFF · your followers, from the Ledger, THE FIXER'S OFFICE · everything the vault owes you", "7808": "◀ The Codex / 📖 The Codex — THE FIXER'S OFFICE · everything the vault owes you, 📖 Curses Lifted · $(n) of 7, 📖 Events and Secrets · $(n) of 28, 📖 Masterworks · $(n) of 4, 📖 Rare Finds · $(n) of 18, 📖 Rooms of the Vault · $(n) of 23", "7809": "⚑ Plan a Heist or join your party's — THE FIXER'S OFFICE · everything the vault owes you", "7811": "⬆ Tank — THE ARMORY · your kits, for good", "7812": "⬆ Offense — THE ARMORY · your kits, for good", "7813": "⬆ Ranged — THE ARMORY · your kits, for good", "7814": "⬆ Support — THE ARMORY · your kits, for good", "7819": "none — YOUR SIGNATURE · an effect of your own", "7820": "Secondary weapon — THE ARMORY · your kits, for good", "7821": "$(r_l0) — YOUR SECONDARY · a weapon of your own", "7822": "$(r_l1) — YOUR SECONDARY · a weapon of your own", "7823": "$(r_l2) — YOUR SECONDARY · a weapon of your own", "7824": "$(r_l3) — YOUR SECONDARY · a weapon of your own", "7825": "$(r_l4) — YOUR SECONDARY · a weapon of your own", "7826": "$(r_l5) — YOUR SECONDARY · a weapon of your own", "7827": "$(r_l6) — YOUR SECONDARY · a weapon of your own", "7828": "$(r_l7) — YOUR SECONDARY · a weapon of your own", "7829": "none — YOUR SECONDARY · a weapon of your own", "7830": "Signature effect — THE ARMORY · your kits, for good", "7831": "$(r_l0) — YOUR SIGNATURE · an effect of your own", "7832": "$(r_l1) — YOUR SIGNATURE · an effect of your own", "7833": "$(r_l2) — YOUR SIGNATURE · an effect of your own", "7834": "$(r_l3) — YOUR SIGNATURE · an effect of your own", "7835": "$(r_l4) — YOUR SIGNATURE · an effect of your own", "7836": "$(r_l5) — YOUR SIGNATURE · an effect of your own", "7837": "$(r_l6) — YOUR SIGNATURE · an effect of your own", "7838": "$(r_l7) — YOUR SIGNATURE · an effect of your own", "7839": "$(r_l8) — YOUR SIGNATURE · an effect of your own", "7840": "⬇ Deposit everything — THE GUTTER BANK · your coins and spoils", "7841": "Take 16 coins — THE GUTTER BANK · take out coins", "7842": "Take 64 coins — THE GUTTER BANK · take out coins", "7843": "Take all my coins — THE GUTTER BANK · take out coins", "7844": "Buy 1 Token (32) — THE GUTTER BANK · Black Market Tokens", "7845": "Buy 10 Tokens (320) — THE GUTTER BANK · Black Market Tokens", "7846": "⬆ Take out coins — THE GUTTER BANK · your coins and spoils", "7847": "⬆ Take out spoils — THE GUTTER BANK · your coins and spoils", "7848": "✦ Buy Tokens — THE GUTTER BANK · your coins and spoils", "7851": "Copper Cogs ($(m1)) — THE GUTTER BANK · take out spoils", "7852": "Silver Seals ($(m2)) — THE GUTTER BANK · take out spoils", "7853": "Gilded Leaves ($(m3)) — THE GUTTER BANK · take out spoils", "7854": "Deep Pearls ($(m4)) — THE GUTTER BANK · take out spoils", "7855": "Hoard Embers ($(m5)) — THE GUTTER BANK · take out spoils", "7856": "Captain's Insignia ($(m6)) — THE GUTTER BANK · take out spoils", "7861": "📖 Rooms of the Vault — THE CODEX · what you've seen in the vault", "7862": "📖 Events and Secrets — THE CODEX · what you've seen in the vault", "7863": "📖 Curses Lifted — THE CODEX · what you've seen in the vault", "7864": "📖 Rare Finds — THE CODEX · what you've seen in the vault", "7865": "📖 Masterworks — THE CODEX · what you've seen in the vault", "7870": "⇄ Medallions & Trophies — THE GUTTER BANK · your coins and spoils", "7871": "Take 1 Medallion — THE GUTTER BANK · Medallions & Trophies", "7872": "Take all Medallions — THE GUTTER BANK · Medallions & Trophies", "7873": "Take 1 Trophy — THE GUTTER BANK · Medallions & Trophies", "7874": "Take all Trophies — THE GUTTER BANK · Medallions & Trophies", "7875": "16 coins → Medallion — THE GUTTER BANK · Medallions & Trophies", "7876": "128 coins → Trophy — THE GUTTER BANK · Medallions & Trophies", "7877": "Medallion → 16 coins — THE GUTTER BANK · Medallions & Trophies", "7878": "Trophy → 128 coins — THE GUTTER BANK · Medallions & Trophies", "7879": "8 Medallions → Trophy — THE GUTTER BANK · Medallions & Trophies", "7880": "⌂ The Fixer's Lounge — THE FIXER'S OFFICE · everything the vault owes you", "7881": "⏭ Skip this puzzle — THE FIXER'S OFFICE · everything the vault owes you", "7883": "Trophy → 8 Medallions — THE GUTTER BANK · Medallions & Trophies", "7899": "⏏ Leave the heist — THE FIXER'S OFFICE · everything the vault owes you", "7900": "Cecil — p103/crew/row_0", "7901": "Emma — p103/crew/row_1", "7902": "Celi — p103/crew/row_2", "7903": "Zib — p103/crew/row_3", "7904": "KillerWatt — p103/crew/row_4", "7905": "Leo — p103/crew/row_5", "7906": "Democratus — p103/crew/row_6", "7907": "Skiff Escort — p103/crew/row_7", "7908": "Apophiss — p103/crew/row_8", "7909": "Tullius — p103/crew/row_9", "7920": "The Frog — p103/crew/row_10", "7921": "Donado — p103/crew/row_11", "7931": "Knuckles — p103/crew/hire_rows", "7932": "Doc Whiskers — p103/crew/hire_rows", "7933": "Fingers — p103/crew/hire_rows", "7934": "Tick-Tock — p103/crew/hire_rows", "7935": "Boomer — p103/crew/hire_rows", "7950": "Outfits & Emma's buff — p98/crew", "7951": "Emma's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7952": "Celi's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7953": "Zib's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7954": "Cecil's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7955": "KillerWatt's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7956": "Leo's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7957": "Democratus's wardrobe — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7961": "Emma: Speed — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7962": "Emma: Offense — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7963": "Emma: Defense — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7964": "Emma: Healing — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7965": "Emma: Mining — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "7968": "Chatter on / off — OUTFITS & EMMA'S BUFF · your followers, from the Ledger", "8000": "« The Recruiter — p137/rc/gems, p137/rc/hires", "8001": "Cecil 192 coins / Cecil IN YOUR PACK / Cecil SIGNED — p137/rc/main", "8002": "Emma 192 coins / Emma IN YOUR PACK / Emma SIGNED — p137/rc/main", "8003": "Celi 224 coins / Celi IN YOUR PACK / Celi SIGNED — p137/rc/main", "8004": "Zib 192 coins / Zib IN YOUR PACK / Zib SIGNED — p137/rc/main", "8005": "KillerWatt 320 coins / KillerWatt IN YOUR PACK / KillerWatt SIGNED — p137/rc/main", "8006": "Leo 208 coins / Leo IN YOUR PACK / Leo SIGNED — p137/rc/main", "8007": "Democratus 224 coins / Democratus IN YOUR PACK / Democratus SIGNED — p137/rc/main", "8008": "Skiff Escort 128 coins / Skiff Escort IN YOUR PACK / Skiff Escort SIGNED — p137/rc/main", "8009": "Apophiss 352 coins / Apophiss IN YOUR PACK / Apophiss SIGNED — p137/rc/main", "8010": "Tullius 336 coins / Tullius IN YOUR PACK / Tullius SIGNED — p137/rc/main", "8011": "The Frog with Mustache 192 coins / The Frog with Mustache FILED / The Frog with Mustache IN YOUR PACK — p137/rc/main", "8012": "Donado 192 coins / Donado FILED / Donado IN YOUR PACK — p137/rc/main", "8040": "Hirelings › — p137/rc/main", "8041": "Knuckles 48 coins / Knuckles FILED / Knuckles IN YOUR PACK — p137/rc/hires", "8042": "Doc Whiskers 64 coins / Doc Whiskers FILED / Doc Whiskers IN YOUR PACK — p137/rc/hires", "8043": "Fingers 48 coins / Fingers FILED / Fingers IN YOUR PACK — p137/rc/hires", "8044": "Tick-Tock 64 coins / Tick-Tock FILED / Tick-Tock IN YOUR PACK — p137/rc/hires", "8045": "Boomer 64 coins / Boomer FILED / Boomer IN YOUR PACK — p137/rc/hires", "8050": "Vault gems › — p137/rc/main", "8051": "Fire Gem 96 coins — p137/rc/gems", "8052": "Water Gem 96 coins — p137/rc/gems", "8053": "Poison Gem 96 coins — p137/rc/gems", "8054": "Earth Gem 96 coins — p137/rc/gems", "8055": "Electric Gem 96 coins — p137/rc/gems", "8056": "Rock Gem 96 coins — p137/rc/gems", "8057": "Air Gem 96 coins — p137/rc/gems", "8058": "Grass Gem 96 coins — p137/rc/gems", "8059": "Ice Gem 96 coins — p137/rc/gems", "8301": "Wait here / follow me — Pearlman's Business Card", "8309": "Send him home — Pearlman's Business Card", "8501": "Raw Materials Crate 16 coins — THE CRATE DESK · paid from your bank and pockets", "8502": "Adventurer's Crate 32 coins — THE CRATE DESK · paid from your bank and pockets", "8503": "Mineral Crate 48 coins — THE CRATE DESK · paid from your bank and pockets", "8504": "Crimson Tip-off 64 coins — THE CRATE DESK · paid from your bank and pockets", "8505": "Vorn Signal 64 coins — THE CRATE DESK · paid from your bank and pockets", "8506": "Stone Crate 6 coins — THE CRATE DESK · paid from your bank and pockets", "8507": "Timber Crate 8 coins — THE CRATE DESK · paid from your bank and pockets", "8601": "Sit / follow — The Serpent's Oath", "8602": "Ride him — The Serpent's Oath", "8603": "Take off the saddle — The Serpent's Oath", "8608": "Call for Apophiss — The Serpent's Oath", "8609": "Send him home — The Serpent's Oath", "8621": "Sit / follow — Tullius's Frozen Doubloon", "8628": "Call for Tullius — Tullius's Frozen Doubloon", "8629": "Send him home — Tullius's Frozen Doubloon", "8641": "Sit / follow — Signet of the Frog Knight", "8642": "Hand back my gear — Signet of the Frog Knight", "8648": "Call for the Frog — Signet of the Frog Knight", "8649": "Send him home — Signet of the Frog Knight", "8651": "Sit / follow — Donado's Collar Tag", "8652": "Hand back my gear — Donado's Collar Tag", "8658": "Call for Donado — Donado's Collar Tag", "8659": "Send him home — Donado's Collar Tag", "9701": "Duel him — Democratus' Challenge", "9702": "Call for Democratus / Send him home — Democratus' Challenge", "9703": "Wardrobe — Democratus' Challenge", "9800": "$(r_home) / « Outfits & buffs — Emma · wardrobe", "9802": "Pink ribbon $(r_ribbon0) — Emma · wardrobe", "9803": "Gold $(r_ribbon1) — Emma · wardrobe", "9804": "Midnight $(r_ribbon2) — Emma · wardrobe", "9805": "Mint $(r_ribbon3) — Emma · wardrobe", "9806": "Snow $(r_ribbon4) — Emma · wardrobe", "9807": "Crimson $(r_ribbon5) — Emma · wardrobe", "9808": "Phantom $(r_ribbon6) — Emma · wardrobe", "9812": "Her own dress $(r_dress0) — Emma · wardrobe", "9813": "Sundress $(r_dress1) — Emma · wardrobe", "9814": "Midnight Gown $(r_dress2) — Emma · wardrobe", "9815": "Sakura $(r_dress3) — Emma · wardrobe", "9816": "Royal Gown $(r_dress4) — Emma · wardrobe", "9817": "Starlight Gown $(r_dress5) — Emma · wardrobe", "9823": "Flower Top $(r_outfit1) — Emma · wardrobe", "9824": "Cozy Sweater $(r_outfit2) — Emma · wardrobe", "9840": "$(r_home) / « Outfits & buffs — Celi · wardrobe", "9842": "Own clothes $(r_celi0) — Celi · wardrobe", "9843": "Aurora $(r_celi1) — Celi · wardrobe", "9844": "Rosehip $(r_celi2) — Celi · wardrobe", "9845": "Midnight $(r_celi3) — Celi · wardrobe", "9846": "Frostfire $(r_celi4) — Celi · wardrobe", "9860": "$(r_home) / « Outfits & buffs — Zib · wardrobe", "9862": "Own clothes $(r_zib0) — Zib · wardrobe", "9863": "Crimson Guard $(r_zib1) — Zib · wardrobe", "9864": "Forest Ranger $(r_zib2) — Zib · wardrobe", "9865": "Golden Ace $(r_zib3) — Zib · wardrobe", "9880": "$(r_home) / « Outfits & buffs — Cecil · wardrobe", "9882": "Own colours $(r_cecil0) — Cecil · wardrobe", "9883": "Crimson $(r_cecil1) — Cecil · wardrobe", "9884": "Midnight $(r_cecil2) — Cecil · wardrobe", "9885": "Bone $(r_cecil3) — Cecil · wardrobe", "9886": "Gilded $(r_cecil4) — Cecil · wardrobe", "9900": "$(r_home) / « Outfits & buffs — KillerWatt · wardrobe", "9902": "Own colours $(r_kw0) — KillerWatt · wardrobe", "9903": "Midnight $(r_kw1) — KillerWatt · wardrobe", "9904": "Bone $(r_kw2) — KillerWatt · wardrobe", "9905": "Neon $(r_kw3) — KillerWatt · wardrobe", "9906": "Golden Thunder $(r_kw4) — KillerWatt · wardrobe", "9920": "$(r_home) / « Outfits & buffs — Leo · wardrobe", "9922": "Own clothes $(r_leo0) — Leo · wardrobe", "9923": "Crimson Crusader $(r_leo1) — Leo · wardrobe", "9924": "Royal Purple $(r_leo2) — Leo · wardrobe", "9925": "Greenwood $(r_leo3) — Leo · wardrobe", "9926": "Golden Champion $(r_leo4) — Leo · wardrobe", "9940": "$(r_home) / « Outfits & buffs — Democratus · wardrobe", "9942": "Own clothes $(r_demo0) — Democratus · wardrobe", "9943": "Crimson Reaper $(r_demo1) — Democratus · wardrobe", "9944": "Ashen Shroud $(r_demo2) — Democratus · wardrobe", "9945": "Royal Violet $(r_demo3) — Democratus · wardrobe", "9946": "Gilded Storm $(r_demo4) — Democratus · wardrobe"}, "version": "v2.77d"} -->
