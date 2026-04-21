**Subject:** Appeal for *Fighting Rogue* — Eligibility for the Steam Deck-Building Fest

**To:** Steam Deck-Building Fest Organizing Team
**From:** The *Fighting Rogue* development team

---

Dear Steam Deck-Building Fest Team,

Thank you for taking the time to review *Fighting Rogue* (Chinese title: 肉鸽武林). We received the preliminary notice indicating that the game may not qualify for this year's Deck-Building Fest, and we would like to respectfully appeal that decision.

*Fighting Rogue* is an **inventory-based Roguelike Deckbuilder** in the same lineage as ***Backpack Battles***, which is officially tagged as *Roguelike Deckbuilder* and *Card Battler* on Steam and participated in the Steam Deckbuilders Fest (including the official "Can't Put It Down" bundle with *Balatro*). Our game follows the exact same design philosophy: **the player's deck is the collection of cards and items they have configured for combat, and every run is defined by how they build, refine, and re-shape that deck.**

At any point during a run, the player's full deck is divided into two clearly separated spaces:

- **Armory** — the cards and items the player has equipped for combat. The Armory has a strict **Equip Load** limit; only cards inside the Armory take effect during battle.
- **Inventory** — the cards and items the player owns but has *not* equipped for the current battle. Cards in the Inventory are held, visible, and inspectable, but do **not** take effect in combat.

Cards flow between these two spaces throughout a run: when the Armory's Equip Load is reached, additional items the player owns are placed in the Inventory and sit out of the next battle; between battles, the player can freely rearrange which cards are promoted into the Armory and which are returned to the Inventory.

We believe the preliminary rejection may have stemmed from the expectation that a deckbuilder must present cards as a traditional hand-and-pile UI (as in *Slay the Spire*). The Deck-Building Fest category, however, is much broader — *Backpack Battles*, *Balatro*, *Inscryption*, *Luck be a Landlord*, and others each interpret the "deck" concept in their own way. Our interpretation is an **Armory-driven deck of cards and items**, fully consistent with the Roguelike Deckbuilder genre.

As a direct precedent, we would like to point to this public announcement from the *Backpack Battles* team confirming their participation in the 2024 Steam Deckbuilders Fest:

> https://x.com/TweetFurcifer/status/1772309379842273614

*Backpack Battles* shares its core structure with *Fighting Rogue* — an inventory/Armory of owned cards and items, a bounded active loadout chosen from that pool, and run-long deck mutation through acquisition, removal, and recombination. Since a game built on exactly this template was accepted into the Deckbuilders Fest (and featured in the official *Balatro* × *Backpack Battles* "Can't Put It Down" bundle), we believe *Fighting Rogue*, which follows the same template, should be evaluated under the same standard.

We address each of the five eligibility criteria below, using the same terminology Steam uses.

---

### 1. "The ability to look at your current deck of cards at any point"

*Fighting Rogue* lets the player inspect their **entire deck** — both the **Armory** (equipped, combat-active cards) and the **Inventory** (owned but unequipped cards) — **at any time**, during combat and outside of combat (map, shops, rest sites, events). The two views sit side-by-side in the same UI so the player always sees the full picture of what they own. Each card entry shows its name, rarity, Equip Load, full effect description, and whether it is currently equipped or sitting in the Inventory.

This is functionally identical to how *Backpack Battles* lets players inspect both their active backpack and their full item stash at any point during a run.

---

### 2. "A discard pile for played cards"

*Fighting Rogue* implements this criterion through the **Inventory** — a dedicated, always-visible space that holds every card the player owns but is *not* currently playing in combat.

The mechanism works as follows:

- The **Armory** has a hard **Equip Load** limit. Once that limit is reached, any additional item the player owns is automatically placed into the **Inventory**.
- Cards sitting in the Inventory are **fully inert during battle** — they do not trigger, do not take up a slot, and do not influence combat in any way. They are, by definition, *not being played this round*.
- The Inventory is displayed as a **separate, inspectable pile** alongside the Armory, so the player can see at all times exactly which of their cards are "in play" and which are "set aside".
- Between battles, cards move between the Inventory and the Armory as the player re-equips their loadout — exactly like cards cycling between a play zone and a discard pile.

The criterion — *cards that are not currently being played are held in a visible, separate, inspectable pile* — is satisfied by the Inventory. This is the same relationship *Backpack Battles* establishes between items inside the active backpack and items sitting in the storage area outside it: the storage space is the pile of "cards not currently in play", and our Inventory performs the identical role.

---

### 3. "The ability to add and remove cards"

Deck mutation is the **core progression system** in *Fighting Rogue*, and — crucially — it happens **every single round**. Between rounds, the player visits an in-game **shop** where they can spend gold to **buy new cards/items** or **sell cards/items they already own** back for gold. This buy/sell loop is available every round, so the player's deck is constantly being reshaped throughout the run. This is the same round-by-round shop cadence used by *Backpack Battles*.

There is no stat-based leveling in *Fighting Rogue*; characters grow exclusively by adding, removing, and reshaping the cards and items in their deck.

**Ways to ADD cards to the deck:**
1. **Shop — Buy (every round)** — the primary channel. Each round the shop offers a rotating stock of cards/items the player can purchase with gold.
2. **Post-combat rewards** — after certain battles, the player chooses a new card/item from a selection of options.
3. **Elite & boss rewards** — defeating stronger enemies unlocks rarer card pools with more powerful effects.
4. **Random events** — map events offer narrative choices that can grant special cards.
5. **Crafting / fusion** — combining existing cards can produce new, higher-tier cards.

**Ways to REMOVE cards from the deck:**
1. **Shop — Sell (every round)** — the primary channel. Each round the player can sell owned cards/items back to the shop for gold, permanently removing them from the deck.
2. **Rest sites — Remove option** permanently deletes one card, available multiple times per run.
3. **Card upgrades / transformations** — upgrading a card replaces the old version with a stronger one (mechanically = remove + add).
4. **Event-driven removals** — several map events offer "sacrifice a card" choices that permanently remove a card in exchange for other benefits.

Because buying and selling are available every round, deck composition changes continuously throughout a run. A run starts with a small initial deck and typically ends with a completely different deck shape; two consecutive runs produce two visibly different decks. This is the textbook Roguelike Deckbuilder progression loop.

---

### 4. "A limit to how many cards you can play per round"

*Fighting Rogue* enforces this through a hard **Equip Load** system on the Armory.

- Only cards placed inside the **Armory** are played during a battle — the rest sit in the **Inventory** and are inert.
- The Armory has a fixed **Equip Load** capacity, and **Equip Load is the direct cap on how many cards/items the player can put into the Armory each round.** Every card/item has its own Equip Load value, and the total Equip Load of everything the player equips cannot exceed the ceiling.
- As a run progresses, the player almost always owns more cards than the Equip Load allows, which is precisely why the Inventory exists: every card that cannot fit under the cap is held in the Inventory and sits the round out.
- Within a round, each equipped card also resolves according to its own cost and cooldown rules, so **not every card the player owns — and not even every card inside the Armory — will necessarily act in a single round.**

The "cards played per round" limit is therefore both *structural* (the Equip Load ceiling) and *tactical* (per-card cost/cooldown), fully visible in the UI. This is the same structural limit seen in *Backpack Battles* (a fixed backpack grid capacity per round) and *Balatro* (a fixed number of hands per round).

---

### 5. "A limited number of cards you can hold in your hand compared to your total deck"

The separation between **Armory** and **Inventory**, combined with the **Equip Load** limit, guarantees this condition directly — and more importantly, it makes the condition **a meaningful strategic choice rather than a cosmetic cap**.

- **Total deck = Armory + Inventory.** It grows run-long as the player acquires new cards — by mid-to-late run it contains many more cards than the Armory can ever hold at once.
- **Armory ("hand in play") is strictly bounded** by the Equip Load capacity. It is always a **small subset** of the total deck.
- **Cards and items are not infinitely stackable** because each one costs Equip Load. The player genuinely cannot "just take everything": adding a heavy item forces them to drop a lighter one, and powerful items usually cost more Load, so the player has to **strategically decide** what to equip and what to leave in the Inventory this round.
- Everything that does not fit under the Equip Load cap is pushed into the **Inventory**, making the size gap between "what you can play" and "what you own" explicit and visible at all times.
- Choosing which cards to promote from the Inventory into the Armory before each battle is the **core deck-building decision** of the game — precisely the tension this criterion is designed to preserve.

This is the same relationship *Backpack Battles* enforces between a player's item stash and the fixed-size backpack grid: you own many more items than you can field, each item takes up real space, and choosing what to field is the game.

---

### Cards are the central focus of *Fighting Rogue*

The Deck-Building Fest requires cards to be *"the central focus"* of the game. For *Fighting Rogue*:

- **Every combat outcome is determined by the player's deck of cards and items** — there is no separate non-card combat system. Win or lose depends entirely on how the deck was built and arranged.
- **Progression = deck composition.** There are no standalone skill trees or stat upgrades; all growth comes from acquiring, removing, upgrading, and re-combining cards.
- **The main UI is a deck UI.** The Armory view, the Inventory view, and the card-reward screen form the spine of the player experience.
- **Roguelike randomness is expressed through cards** — random rewards, random shop stocks, random event cards, and random synergies between owned cards drive run-to-run variety.
- **The genre lineage is explicit.** The game is designed and tagged as a Roguelike Deckbuilder / Card Battler, the same category occupied by *Backpack Battles*, which has already participated in the Deckbuilders Fest.

---

### Closing

Against the five published eligibility criteria, *Fighting Rogue* satisfies every one, following the same inventory-based Roguelike Deckbuilder template already accepted into the Deckbuilders Fest through titles such as *Backpack Battles*. We would be very grateful if the review team could reconsider the game's eligibility for this year's Steam Deck-Building Fest.

We are happy to provide any of the following on request:

- A full gameplay video showing the Armory and Inventory views, Equip Load-limited loadout configuration, per-round shop buy/sell, post-combat card rewards, and card removal.
- A Steam review build / key for reviewers to experience the game directly.
- An updated store page with Roguelike Deckbuilder / Card Battler tags prioritized and screenshots that prominently feature the Armory and Inventory UI.

Thank you again for your time and for organizing the Deck-Building Fest. We would be proud to stand alongside the outstanding deckbuilders featured in the event.

Best regards,
The *Fighting Rogue* Team
