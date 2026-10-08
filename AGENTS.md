# Research agent entry contract

**Start here for any research task in this repository.** This file is intended for ChatGPT, Claude, Codex and other autonomous or assisted research sessions.

1. Read [RESEARCH-ENTRY.md](RESEARCH-ENTRY.md) completely, then [research/README.md](research/README.md) and [research/routes.json](research/routes.json).
2. Load [research/catalog.json](research/catalog.json) to find existing work relevant to the user's topic. **Search before creating another report or dataset.**
3. Read [docs/EVIDENCE-STANDARDS.md](docs/EVIDENCE-STANDARDS.md) and [docs/COMPLIANCE.md](docs/COMPLIANCE.md). Public evidence only; do not reproduce expert-network/client material or private data.
4. Route the user's task across **all** applicable research routes, not just one. Create one `research/packets/YYYY-MM-DD--slug.json` research packet for a logically distinct intake event, using [the packet schema](research/schema/packet.schema.json).
5. Preserve sources, actual numerical claims, technical facts, attributable executive statements, forecasts, hypotheses, open questions, conflicts and model assumptions as **different record kinds**. Source metadata is never the same as proof of a claim.
6. Cross-link existing claim/source IDs. A new article or a newer TAM projection is a new **source vintage**, not a replacement for old evidence. Promote only reviewed records into preexisting canonical domain datasets with their denominator and license constraints.
7. Make only the smallest necessary changes. Keep the existing static dashboard functional. When a study touches multiple domains, create **one packet with multiple routes** and update the affected domain indexes/pointers, rather than copying raw data to every folder.
8. Run `npm test` and `npm run check:research` where available. Report new evidence, unresolved contradictions, what was reused, what was explicitly *not* verified, and commit SHA.
9. Preserve the single `main` integration model. Short-lived worktrees are acceptable; avoid permanent departmental branches. Don't change app hosting or deployment without a separate user request.

**If you have read only this file, the task is not yet ready to implement. Start with [RESEARCH-ENTRY.md](RESEARCH-ENTRY.md).**

This is a light governance contract, not an instruction to bulk-migrate all legacy datasets or build a new database. Existing source sets and research docs remain authoritative in their own definitions until explicitly reconciled.
