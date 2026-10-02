# Duplicate prevention

The publishing identity is SHA-256(platform | job_id | exact version | approved asset SHA-256).

Before a platform create call, the publisher must check for a terminal Posted marker and an active lock. If either exists, publication is blocked. The lock is acquired before the create call.

A verified Pinterest read-back converts the lifecycle to Posted and creates the terminal receipt/marker. A retry must reuse the same identity and approved package; it may never create a new version or silently change creative, metadata, destination, or board.

A stale lock is not automatically discarded during commissioning. It is held for review so an ambiguous API outcome cannot become a duplicate Pin.

This repository currently stores commissioning state locally during a run. Before unattended production is enabled, the lock/Posted marker must live in durable shared state so separate GitHub runners see the same identity.
