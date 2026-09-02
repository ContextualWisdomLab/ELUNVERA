# ADR-0013: Preserve ELUNVERA brand and license original source under Apache-2.0

- **Status:** Accepted
- **Date:** 2026-09-02
- **Decision owners:** ELUNVERA maintainers

## Context

The ELUNVERA brand was selected through preliminary domain and clearance review, but trademark status and source-code licensing are separate legal boundaries. The repository is ContextualWisdomLab-owned, public, non-fork, and begins from an independent owner initialization commit. The current foundation contains repository-authored documentation, schemas, configuration, and contract artifacts rather than imported runtime source or package dependencies. Repository review found no inherited outbound source license, copied-source notice, submodule, GPL/LGPL/AGPL marker, noncommercial restriction, or other provenance evidence requiring a different repository-level grant.

A public repository without a source grant leaves prospective users and contributors unable to determine what rights are actually offered. Conversely, choosing a repository license must not be used to absorb third-party terms or imply trademark registration.

## Decision

Use `ELUNVERA`/`Elunvera` and Korean `엘룬베라` consistently without claiming trademark registration.

License ContextualWisdomLab-authored ELUNVERA source and documentation under the Apache License 2.0 through the root `LICENSE`. Apache-2.0 is selected as the commercial-friendly permissive baseline for this enterprise product because it permits commercial use and distribution while providing an explicit patent grant and preserving notice obligations.

The repository grant does not relicense standards, dependencies, generated assets, datasets, models, provider services, trademarks, or future imported material. Every such component requires independent provenance, commercial-license compatibility, and attribution/NOTICE review before incorporation or distribution.

## Consequences

- ELUNVERA-authored repository source and documentation have an explicit commercial-use-compatible grant.
- Brand and trademark rights remain separate from source licensing; no trademark registration or broader brand permission is claimed.
- Future package/dependency/source/asset additions must be checked independently and cannot rely on Apache-2.0 to override their original terms.
- A future incompatible inbound obligation requires replacement/removal or a superseding, evidence-backed repository decision rather than a silent exception.

## Compliance and verification

The root `LICENSE`, README license section, documentation landing, product-gap ledger, changelog, and SHA-256 repository manifest must agree on this decision. Contract validation continues to require exact tracked-file inventory and byte hashes. A conflicting license or provenance change requires explicit review and, when it changes this decision, a superseding ADR before integration.
