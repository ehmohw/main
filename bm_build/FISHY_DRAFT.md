# Fishy: role ideas (draft for approval)

Fishy is a gentleman goldfish (top hat, monocle) living in a fishbowl that rides on robot legs, with robot arms. His draft model and animations are in
`fishy_art.py`; render them with `python3 tools/preview/fishy.py`. The poses are idle, walk, wave, bow, point, shock (the monocle pops), sit and tired, and the swim laps show him circling his bowl.

None of this is built yet. Pick one, or combine the first with one of the others.

## The rule: no overlap

Each idea was checked against what the pack already does:
- **Pearlman** appraises and sells gems.
- **The Codex** records raid rooms and raid mobs.
- **The grave charm** keeps items on death.
- **Fishing** already pays out tokens and crates, and has Mike the Spikefish and the Blue Marlin.
- **Messages in a Bottle**, **Leo's** water breathing and the **Fishbowl Helmet** already exist.
- **The coat check, the Tailor, the Recruiter and Goldtooth** already run the Lounge's services.

## 1. The Curator: Fishy's Cabinet of Curiosities (recommended)

Fishy keeps a small museum, which appears in the Black Market as a new wing off the Fixer's Lounge. Every custom thing in the pack has a plinth waiting for it there.

- **Donate** one of each thing: boss relics, rare raid finds, music discs, dolls, gems, alien parts and Hollow treasures. Hand it to Fishy and it goes on its plinth, behind glass, labelled in his flowery hand.
  - Donated items are kept for good; that is the point.
  - Plinths for things you haven't found show only a silhouette and a riddle, which doubles as a hint for players hunting the pack's secrets.
- **Wings fill up:** the Hollow, the Gutter, the Skies (aliens), the Deep (Tullius and the sea), the Wilds (the overworld bosses) and the Court (followers' things).
  - A finished wing earns its own advancement and a display reward: a stained-glass window of that wing for your base, and a title Fishy uses for you.
  - The whole cabinet earns Fishy himself as a follower.
- **Why it doesn't overlap:** no system collects or catalogues items outside raids. The Codex logs raid rooms and mobs only, and it fills itself. The Cabinet is the first sink for duplicate rare items, and the first guide to what you haven't found.
- **Fishy's part:**
  - he walks you round the plinths (the point pose);
  - he gasps at a rare donation (shock, monocle popping);
  - he bows when a wing is complete;
  - he swims laps in his bowl while he waits.

## 2. The Butler: a follower who keeps house

Fishy as a non-combat follower who looks after the base rather than the fight (like Pearlman, he wouldn't count as a fighter).

- **Tidy:** dropped items within 16 blocks are gathered into the nearest chest, sorted by kind.
- **Tea:** right-click him at sunset and he serves a cup that gives a small, long buff (Haste I or Luck I, your pick, for 10 minutes); once a day.
- **The bell:** he gives you a little silver bell. Ring it anywhere in the overworld and he says where your last bed, your last death and your nearest follower are, as directions ("North-east, about 300 paces, sir").
- **Why it doesn't overlap:** no follower does chores, and nothing points the way home or to a death. The grave charm keeps your items but doesn't say where you died.
- **Risk:** item tidying must ignore raid kits, coat-check items and items in display cases.

## 3. The Tournament Host: the Gentleman's Fishing Derby

Fishy hosts a timed fishing contest at the Black Market docks, once per in-game week.

- **Entry:** one medallion. For ten minutes, every catch is weighed and scored, with rare fish worth more.
- **Prize:** the best weight takes the pot, plus a Derby trophy that can sit in a display case.
  - In multiplayer, players compete against each other.
  - Solo, you race Fishy's own record, which rises each time you beat it.
- **Why it doesn't overlap:** fishing already pays, but there is no competitive fishing and nothing timed at the docks.
- **Risk:** it leans on fishing, which already has a lot going on. It's the weakest of the three for "no overlap".

## Rejected, and why

- **An appraiser or pawnbroker:** Pearlman and the Fence cover it.
- **A tide or weather forecaster:** the weather potions cover it.
- **An underwater guide or dive bell:** Leo's water breathing and the Fishbowl Helmet cover it.
- **A message or letter courier:** mailboxes and Messages in a Bottle cover it.

## Recommendation

**Idea 1, the Curator**, with Fishy as the reward for finishing the cabinet: a follower who carries his bowl into battle and fights with his robot arms. It gives the pack's collectors a long goal, gives every rare item a reason to exist twice, and suits his gentleman-scholar look.
