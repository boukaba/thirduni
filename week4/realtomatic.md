# Realtomatic

## The problem

Real estate is a $33T industry still running on spreadsheets and PDFs. Brokers burn ~60% of their time on data entry instead of closing deals. And the data itself — PII, financial records, lease terms — sits in ordinary shared containers, which is exactly what regulators have been closing in on (GLBA, FTC Safeguards Rule, CAN-SPAM/TCPA, plus a dozen state privacy laws granting access/correct/delete/opt-out rights).

## The product

AI agents that do the actual work of real estate:

- Read a lease and extract structured terms
- Compute valuations
- Analyze markets
- Score and respond to leads
- Screen tenants
- Predict maintenance
- Handle email outreach to landlords

## Why it's built differently

| Most AI tools | Realtomatic |
|---|---|
| Shared containers | Every agent task runs in its own Firecracker microVM — separate kernel, no escape path |
| RAG over documents | PostgreSQL (transactions) + PGVector (semantic search) + Neo4j (ownership/market graphs) + ClickHouse (analytics) |
| "Ask it anything" | City-specific compliance baked in; math is computed, not guessed |

The RAG point matters: retrieval-augmented generation hallucinates 30–40% of the time on complex calculations that depend on local regulations and lease structures. That's fine for summarizing a document and unacceptable for deciding whether a lease is worth $2.3M.

## The moat

Built on Pullrun, an open-source sandbox runtime by the founder — microVMs boot in ~200ms, policy engine gates every execution (Cosign signatures, SBOM vulnerability scans, seccomp profiles, network egress allowlists). Agents hibernate when idle and wake at the same state, so compute costs run ~90% below always-on VM fleets.

## Status

Pre-seed, applying to YC Winter 2027. Solo founder (Mohammed Boukaba). Looking for an enterprise sales co-founder with real US PropTech relationships — because that vertical runs on trust and relationships with NAR, MLS systems, and brokerages like Compass and CBRE, and no generic B2B salesperson cracks it.

## Human in the loop

The agents propose; people approve. High-stakes outputs route to a HITL approval queue with an audit trail.

## Pitch deck

https://youtu.be/XOVQaGCzYHg
