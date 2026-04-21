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

We believe the preliminary rejection may have stemmed from the expectation that a deckbuilder must present cards as a traditional hand-and-pile UI (as in *Slay the Spire*). The Deck-Building Fest category is much broader, and our interpretation — an **Armory-driven deck of cards and items** — is fully consistent with the Roguelike Deckbuilder genre.

As a direct precedent, *Backpack Battles* — which shares our exact structure (an Armory/Inventory of owned cards and items, a bounded active loadout, and run-long deck manipulation) — was accepted into the 2024 Steam Deckbuilders Fest and featured in the official *Balatro* × *Backpack Battles* "Can't Put It Down" bundle. The developer's own announcement:

> https://x.com/TweetFurcifer/status/1772309379842273614

Since a game built on exactly this template was accepted, we believe *Fighting Rogue* should be evaluated under the same standard. We address each of the five eligibility criteria below, using the same terminology Steam uses.

---

### 1. "The ability to look at your current deck of cards at any point"

*Fighting Rogue* lets the player inspect their **entire deck** — both the **Armory** and the **Inventory** — **at any time**, during combat and outside of combat. The two views sit side-by-side in the same UI so the player always sees the full picture of what they own. Each card entry shows its name, rarity, Equip Load, full effect description, and whether it is currently equipped or sitting in the Inventory.

---

### 2. "A discard pile for played cards"

*Fighting Rogue* implements this criterion through the **Inventory** — a dedicated, always-visible space that holds every card the player owns but is *not* currently playing in combat.

- Any card/item the player owns beyond the Armory's Equip Load cap is automatically held in the **Inventory**, and every card in the Inventory is **fully inert during battle** — it does not trigger, does not take up a slot, and does not influence combat in any way.
- The Inventory is displayed as a **separate, inspectable pile** alongside the Armory, so the player can see at all times exactly which cards are "in play" and which are "set aside".
- Between battles, cards move between the Inventory and the Armory as the player re-equips their loadout — exactly like cards cycling between a play zone and a discard pile.

This is the same relationship *Backpack Battles* establishes between items inside the active backpack and items sitting in the storage area outside it: the storage space is the pile of "cards not currently in play", and our Inventory performs the identical role.

---

### 3. "The ability to add and remove cards"

Deck manipulation is the **core progression system** in *Fighting Rogue*, and it happens **every single round** through a single, unified channel: the in-game **shop**.

Between rounds, the player visits the shop and can freely:

- **ADD cards** — spend gold to buy new cards/items from a rotating stock, which are added directly to the player's deck (Armory or Inventory).
- **REMOVE cards** — sell any card/item they already own back to the shop for gold, permanently removing it from the deck.

Because buy and sell are both available **every round**, the player's deck is constantly being reshaped throughout the run. A run starts with a small initial deck and typically ends with a completely different deck shape; two consecutive runs produce two visibly different decks.

This is the same round-by-round shop cadence used by *Backpack Battles*, and it is the textbook Roguelike Deckbuilder progression loop.

---

### 4. "A limit to how many cards you can play per round"

*Fighting Rogue* enforces this through a hard **Equip Load** system on the Armory.

- The Armory has a fixed **Equip Load** capacity. Every card/item has its own Equip Load value, and the total Equip Load of everything the player equips cannot exceed the ceiling — so Equip Load is the direct cap on how many cards/items the player can bring into a round. Anything that cannot fit is held in the Inventory and sits the round out.
- Within a round, each equipped card also resolves according to its own cost and cooldown rules, so **not every card inside the Armory will necessarily act in a single round.**

The "cards played per round" limit is therefore both *structural* (the Equip Load ceiling) and *tactical* (per-card cost/cooldown). This is the same structural limit seen in *Backpack Battles* (a fixed backpack grid capacity per round) and *Balatro* (a fixed number of hands per round).

---

### 5. "A limited number of cards you can hold in your hand compared to your total deck"

The separation between **Armory** and **Inventory**, combined with the **Equip Load** limit, guarantees this condition directly — and more importantly, it makes the condition **a meaningful strategic choice rather than a cosmetic cap**.

- **Total deck = Armory + Inventory**, and it grows run-long as the player acquires new cards; by mid-to-late run it contains many more cards than the Armory can ever hold at once.
- **Armory ("hand in play") is strictly bounded** by the Equip Load capacity — always a small subset of the total deck.
- **Cards and items are not infinitely stackable** because each one costs Equip Load. Adding a heavy item forces the player to drop a lighter one, and powerful items usually cost more Load, so the player has to **strategically decide** what to equip and what to leave in the Inventory this round.
- Choosing which cards to promote from the Inventory into the Armory before each battle is the **core deck-building decision** of the game — precisely the tension this criterion is designed to preserve.

---

### Cards are the central focus of *Fighting Rogue*

The Deck-Building Fest requires cards to be *"the central focus"* of the game. For *Fighting Rogue*:

- **Every combat outcome is determined by the player's deck of cards and items** — there is no separate non-card combat system. Win or lose depends entirely on how the deck was built and arranged.
- **Progression = deck composition.** There are no standalone skill trees or stat upgrades; all growth comes from acquiring, removing, and re-combining cards.
- **The main UI is a deck UI.** The Armory view, the Inventory view, and the card-reward screen form the spine of the player experience.
- **Roguelike randomness is expressed through cards** — random shop stocks, random rewards, and random synergies between owned cards drive run-to-run variety.

---

### Closing

Against the five published eligibility criteria, *Fighting Rogue* satisfies every one. We would be very grateful if the review team could reconsider the game's eligibility for this year's Steam Deck-Building Fest.

We are happy to provide any of the following on request:

- A full gameplay video showing the Armory and Inventory views, Equip Load-limited loadout configuration, and per-round shop buy/sell.
- A Steam review build / key for reviewers to experience the game directly.
- An updated store page with Roguelike Deckbuilder / Card Battler tags prioritized and screenshots that prominently feature the Armory and Inventory UI.

Thank you again for your time and for organizing the Deck-Building Fest. We would be proud to stand alongside the outstanding deckbuilders featured in the event.

Best regards,
The *Fighting Rogue* Team
