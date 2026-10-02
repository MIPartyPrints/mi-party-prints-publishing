# MI Party Prints — Organic Publishing Runbook

## Normal path
Owner-approved exact package enters Approved for Publishing. Scheduler selects an eligible package at an approved slot. Validator checks approval/version and exact asset. Durable state is checked and a Publishing lock is acquired. Publisher creates the organic Pin. The created Pin is read back and verified. A receipt is written, durable state becomes Posted, the control plane is updated, and the exact creative is archived as Posted.

## Stop conditions
Stop without substitution if: approval/version mismatch; asset hash mismatch; unresolved board; OAuth unavailable; existing Publishing/Posted identity; ambiguous API result; verification failure; or a paid/fee-generating action is requested.

## Reconciliation
Any identity left in Publishing is an exception. Before retrying, query Pinterest for the expected result. If found and verified, finalize Posted. If definitively absent and the failure occurred before creation, release the lock. If outcome remains ambiguous, keep the lock and surface one owner exception.

## Notifications
Routine generation, queue selection, scheduling, successful retries, and successful publication do not require owner interruption. Notify the owner for the combined approval package or a genuine unresolved exception.

## Analytics handoff
Posted receipts are the canonical join key between approved creative and Pinterest performance. Future analytics ingestion should attach impressions, saves, outbound clicks, and other available organic metrics to the receipt/job identity without changing the historical approved package.
