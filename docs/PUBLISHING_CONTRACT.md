# MI Party Prints Pinterest Publishing Contract

## Hard gates
1. Organic Pins only. Paid, promoted, boosted, ad, purchase, and fee-generating actions are forbidden.
2. A job must contain the owner's explicit `Approved` decision for the exact version being published.
3. The asset SHA-256 must match the approved manifest before publication.
4. Title, description, alt text, destination link, and Pinterest board ID are locked publishing fields.
5. The publisher never generates, redraws, edits, substitutes, or optimizes creative.
6. Failure leaves the item approved/unpublished. It must not silently substitute content.
7. A successful API creation must be verified by reading the created Pin before the lifecycle may advance to Posted.
8. Tokens and app secrets belong only in encrypted runtime secrets, never in this repository, Notion, job manifests, or logs.

## Lifecycle
Pending Approval → Approved for Publishing → Publish → Verify → Posted.

## Current commissioning state
The repository is intentionally fail-closed. Real Pinterest execution is disabled until Pinterest developer access is available and OAuth, exact board routing, and stable media delivery have been commissioned.
