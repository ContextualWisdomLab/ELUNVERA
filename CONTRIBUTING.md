# Contributing to ELUNVERA

## Branching

- Base ordinary product work on canonical protected `main`; a stacked PR may target its verified prerequisite feature branch until that prerequisite is integrated.
- Use bounded branches such as `docs/product-technical-baseline`, `feat/account-registry`, or `fix/tenant-authorization`.
- One pull request should deliver one independently reviewable product or platform slice.

## Before opening a pull request

1. Rebase or merge the current approved base without rewriting other agents’ work.
2. Run all repository validation commands relevant to the changed files.
3. Update contracts, tests, documentation, ADRs, the changelog, and the product-gap baseline together.
4. State what was actually verified and what remains unverified.
5. Do not add generated artifacts without deterministic generation and source files.

## Design expectations

New product behavior requires:

- a user and buyer problem;
- an owning module or repository;
- a data and authorization contract;
- failure and rollback behavior;
- test evidence;
- operability and security impact;
- an ADR when the change alters a durable architectural decision.

## Commit messages

Use conventional prefixes such as:

- `docs:` documentation and contract baselines;
- `feat:` buyer-visible behavior;
- `fix:` defect correction;
- `refactor:` behavior-preserving structure change;
- `test:` test-only change;
- `ci:` workflow and build policy;
- `security:` security-boundary hardening.

## Review standard

A reviewer must be able to trace every important claim from requirement to contract, implementation, and test. A document existing is not evidence that the product implements it.
