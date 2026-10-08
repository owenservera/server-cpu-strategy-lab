# Seed contents

`foundation.json` contains **classification definitions**, not observed market shares.

`python db/scripts/research_db.py seed` deterministically **reads existing** `data/demand-2030/*` and `data/claims/*` from the repository and builds a local SQLite database. There is no divergent hand-copied clone of the 41 observations, nine TAM vintages, or keynote claims.

All legacy entries are explicitly assigned a provenance/access status. A public source URL is not itself verification. Vendor demos and auto-caption extracts remain **claims**, not audited observations. The 2025–2030 model is imported exclusively into the **synthetic** model namespace. Unknown architecture shares and net CPU ASP remain NULL. New packet records are not promoted without editorial review.

A seeded database is a reproducible local **materialized research mirror** until verified against legacy datasets and the dashboard's export contract. Do not commit SQLite files, private transcripts, or confidential expert-screening material.
