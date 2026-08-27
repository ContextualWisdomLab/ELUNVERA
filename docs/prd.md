# ELUNVERA PRD — first slice

**Product:** ELUNVERA  
**Tagline:** Every Link, Understood. Every Relationship, Activated.  
**Date:** 2026-08-27  
**Status:** First shippable surface

## Problem

A known relationship goes quiet because no product owns the *next move*. LineageWeave can show how a thing is connected. RankWeave can find text. Ontology/SDP can name the type. Orgmetra can say who holds a job. None of them put a dated, dismissible action in front of the person who must take it.

## Person and job

Someone who already knows the parties and must keep the link alive: a follow-up, an introduction, a scheduled check-in. Not a recruiter payroll flow. Not a catalog curator. Not a graph analyst.

## In scope (this slice)

1. Open a local activation queue (the product home).
2. See each relationship as: parties, kind, next move, due date, why now.
3. **Activate** (record the move happened), **Reschedule** (new due date), or **Dismiss** (not now, and not a delete of the link).
4. Queue orders due items first. Activated and dismissed rows leave the home list.

## Out of scope

- Lineage DAG editing or visualization (LineageWeave)
- Retrieval / fusion search (RankWeave)
- Type catalog editing (Ontology / SDP)
- Employment, posts, or org charts (Orgmetra)
- Mail chrome, GNB calendar, or customer-master clones
- Multi-tenant cloud hosting, identity, or payments

## Success

A person can run `python3 scripts/serve.py`, open the home, and complete one real next move against seed relationships without leaving ELUNVERA.
