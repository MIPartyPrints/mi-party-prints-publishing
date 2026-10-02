# Durable publishing state

For the initial MI Party Prints publisher, durable idempotency state is a small JSON ledger committed to the private publishing repository. It contains publishing identities and lifecycle state only. It contains no OAuth tokens, app secrets, customer data, or creative bytes.

The identity is derived from platform, job ID, exact approved version, and approved asset SHA-256.

Production sequence:
1. Read the latest ledger.
2. If the identity is Posted or Publishing, do not create a Pin.
3. Acquire Publishing state before the Pinterest create request.
4. Create the Pin.
5. Read the exact Pin back from Pinterest.
6. Only after verification, replace Publishing with terminal Posted state containing Pin ID and URL.
7. An ambiguous outcome keeps Publishing state and requires reconciliation. It is not automatically released.
8. A known pre-create failure may release the lock.
9. Posted is terminal.

Concurrency requirement: the workflow that mutates this ledger must serialize publisher executions. GitHub Actions concurrency is used as an additional guard, and the ledger commit must be based on current repository state. A conflict must fail closed and be retried only after refreshing state.

This is intentionally lightweight for the initial 3–5 Pins/day volume. If publishing later spans multiple platforms/runners at materially higher volume, migrate the same state contract to a transactional store rather than weakening duplicate protection.
