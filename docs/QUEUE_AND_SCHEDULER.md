# Queue and scheduler policy

Only an exact-version owner-approved organic package may enter the Approved queue. Generation, editing, and metadata rewriting remain outside the publisher.

Selection is deterministic: eligible jobs are ordered by numeric priority, then approval time. A future not-before timestamp blocks early execution.

A job/version with a verified Posted receipt is terminal and must never be selected again. A publishing lock must exist before any future platform create call.

Temporary server/rate-limit failures may retry with bounded backoff. Other failures, or exhausted retries, go to hold-for-review. Retries never substitute content, change metadata, or select another board.

A successful platform response is not enough by itself. The created item must be read back and verified before a Posted receipt can be created.

The Posted receipt records job/version, exact approved asset SHA-256, platform item ID/URL, board ID, destination URL, verification state, publication time, and a receipt hash.

Automatic cadence is intentionally not hard-coded yet because the owner has not approved a final posting schedule. Scheduled execution remains disabled during commissioning.

Paid, promoted, boosted, advertising, purchase, and fee-generating actions remain outside this scheduler and require separate explicit approval.
