# Live research intake packets

Add a file only after a specific **authorized public-research** task is being ingested: `YYYY-MM-DD--slug.json` with a matching `packet_id`. The complete contract is [../schema/packet.schema.json](../schema/packet.schema.json), and the worked demonstration is at [../templates/packet.example.json](../templates/packet.example.json).

Packets are **staging records**, not approved observed market data. A new packet may route the same source to several research questions, existing domain datasets, future forecasts, disputes and next measurements. Always search existing topic records before writing, and preserve source/date/definition.

Do not put raw third-party full-text material, consulting-client information, NDA materials or credentials here. Use public URLs and line/page pointers.

Review and record promotion decisions explicitly. Run `npm run check:research` and `npm test`. Do not copy already-recorded claims simply to make a packet look fuller; use `legacy_ref` pointers.

See [../INTAKE-AND-PROMOTION.md](../INTAKE-AND-PROMOTION.md).
