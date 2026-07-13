# Je m'appelle Rapide et je suis la myrtille la plus rapide du monde…



# Developer Notes

Log of design decisions and reasoning, in chronological order.

---

## Entry #1: Reward system

**Map:** 3x4 grid world, one wall cell, one diamond, one pit, one goal. Shortest path start->goal: **5 steps**. Shortest path including the diamond: also **5 steps** (no detour needed).

**Rewards:**

| Event | Reward |
|---|---|
| Each step | -1 |
| Diamond | +30 |
| Goal | +100 |
| Pit | -100 |

**Reasoning:**
- Step penalty pushes the agent toward the shortest path instead of wandering.
- Goal and pit are roughly equal in magnitude. Making the pit penalty much larger than the goal reward (e.g. -200 vs +100) risks making the agent overly cautious around cells merely adjacent to the pit.
- Diamond reward is picked to clearly outweigh any reasonable detour cost. Rule of thumb: detour_steps * (-1) must be smaller than the diamond reward, or the agent won't bother collecting it. On this map there's no detour, so any positive value works, but +30 gives a strong, easily distinguishable signal.

**Check:** path through diamond = 5*(-1) + 30 + 100 = 125. Comfortably higher than a same-length path without it (95).

---