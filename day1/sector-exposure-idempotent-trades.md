## Practice prompt: Sector exposure & idempotent trade ingestion

**Scenario:** You’re building a small internal API that ingests executed trades for discretionary accounts and answers: “What is my USD notionals by sector right now?”

### Part 1 — Core model & updates

**Requirements**

- Represent **instruments** with at least: `symbol`, `sector` (string), `currency` (ISO code, e.g. `"USD"`, `"EUR"`).
- Represent **positions** as a map `symbol -> quantity` (integer shares; no fractional for simplicity).
- Implement **`apply_trade(position, trade) -> position`** where each trade has:
  - `symbol`, `side` (`BUY`/`SELL`), `qty` (positive int), optional **`client_order_id`** (string) for deduplication.
- **Rules**
  - `SELL` cannot reduce a position below zero.
  - Applying the **same** `client_order_id` twice must **not** double-count (idempotent updates).

**Deliverable:** Working Python with a couple of unit-style assertions or `if __name__ == "__main__"` checks.

---

### Part 2 — FX + sector aggregation

**Requirements**

You’re given:

- `instrument_by_symbol: dict[str, Instrument]`
- `fx_to_usd: dict[str, Decimal]` mapping currency → USD rate (assume `"USD"` maps to `1`)

Implement:

- **`sector_exposure_usd(position, instrument_by_symbol, fx_to_usd) -> dict[str, Decimal]`**

For each held symbol, compute **USD market exposure** as:

\[
\text{qty} \times \text{last\_price\_in\_native\_ccy} \times \text{fx\_to\_usd[native\_ccy]}
\]

Aggregate sums **by `sector`**.

**Stretch (pick one)**

- Return **top-k sectors** by exposure without sorting the full dict (use a heap), or
- Handle **missing FX** / **unknown symbol** with explicit errors (don’t silently drop).

---

### Part 3 — EM / architecture discussion (verbal, light code)

- **Ordering & replay:** trades may arrive out-of-order or be corrected later (cancel/replace). How do you model state so you can rebuild positions deterministically?
- **Scale:** 10k accounts, steady trade stream—how would you separate **write path** (ingest) vs **read path** (precomputed exposures)? What would you cache, and what’s your invalidation story?
- **Testing strategy:** what invariants must hold after every trade application?

---

### What “good” looks like (self-score)

- **Correctness:** sells bounded by inventory; idempotency actually works
- **Money safety:** prefer `Decimal` for money/rates; avoid float drift
- **Complexity:** position updates O(1) per trade; aggregation O(positions)
- **EM signal:** clear tradeoffs (event log + projections vs mutable state; at-least-once ingestion + idempotency keys)

