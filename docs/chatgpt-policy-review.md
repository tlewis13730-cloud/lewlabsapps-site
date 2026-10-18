# ChatGPT handoff policy drafts

Unpublished feature branch only, October 18, 2026. Do not merge to main or publish
without owner approval. Existing styles, app icon, assetlinks, fallback, app-ads,
Family Games links and product pages are untouched.

Privacy adds transient MCP validation/encoding and clearly distinguishes it from
Scan/Describe, local-only lists, provider telemetry and ChatGPT history. Complete
links are readable, non-expiring content, not encrypted credentials. Existing
report TTL and ad disclosures are preserved. Support adds accurate private-test
availability and safe troubleshooting without asking for full private links.

`terms.html` is a new proposed destination, not yet a live legal policy. It keeps
existing site styling and contains no invented price, jurisdiction, legal entity,
arbitration, fixed retention guarantee or liability waiver. Owner/legal review
must confirm provider identity, markets, effective date, age/access requirements,
consumer-law obligations and any further legally required terms. Remove the draft
notice/noindex only after approval. Verify the contact inboxes are monitored.

Before publication, review against the actual deployed service, confirm Pro or
Free access policy, validate all links and obtain separate authorization. No site
tracking, forms, scripts, MCP calls or DNS/routing changes are added. Marketing
concepts live separately in the application repo's plugin publication branch.

Checks: `python tools/test_handoff.py` and `python tools/test_policy_drafts.py`.
