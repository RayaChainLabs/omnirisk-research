# SEED — RayaChain Omnichain Canary Layer paper

This file is the **AW seeding brief** for the new IEEE Transactions paper.
Verbatim or near-verbatim text from the source seed in
`/Users/bazmini/omnirisk-papers/shard/main2.tex` is included below so the
Academic Writer can lift, tighten, and integrate without re-deriving.

## CEO directive (verbatim, 2026-05-07)

> ask the AWS to create a new article "RayaChain: An Omnichain Canary
> Layer for Cross-Chain Risk and Credit Signal Propagation in
> Decentralized Agentic Finance" i will provide you with seeding text

> this paper will be submited to https://www.computer.org/csdl/journal/tq
> /Users/bazmini/omnirisk-papers/shard study the journal latext template
> and stud the papers i shard folder to seed the new artilce. Act a Top
> ieee journal and use the same author block and add a 2nd authoer Ahod

## Working assumptions (gated on CEO confirmation)

- **Title:** *RayaChain: An Omnichain Canary Layer for Cross-Chain Risk
  and Credit Signal Propagation in Decentralized Agentic Finance.*
  Note: title was extended from the seed (`...in Decentralized Finance`)
  to `...in Decentralized Agentic Finance` per the CEO directive — the
  agentic framing is what differentiates this paper from the seed draft.
- **Venue:** Journal slug `tq` resolves to *IEEE Transactions on Quantum
  Engineering*, which is not a topic fit. **Awaiting CEO confirmation**
  on the actual target — likely candidates are TDSC (Transactions on
  Dependable and Secure Computing) or TNSM (Transactions on Network and
  Service Management). Manuscript class is `IEEEtran[journal]`, which is
  the correct base for any of TDSC/TNSM/TII.
- **Author 1:** Basel Magableh, School of Computer Science, Technological
  University Dublin, Dublin, Ireland. Email basel.magableh@tudublin.ie.
  ORCID 0000-0003-2337-637X. IEEE Member.
- **Author 2:** *Ahod [surname TBD]*. Affiliation, email, ORCID, IEEE
  membership all **TBD** — placeholders in `manuscript.tex` `\thanks{}`
  must be filled before submission.

## Provenance and lift rules

The seed `shard/main2.tex` is **lift-grade** for the *Background and
Motivation* and *Related Work* sections. AW should:

1. Copy the §Cross-Chain Value vs. Cross-Chain Intelligence,
   §Problem Statement, §Related Work, §Research Gap, and the RQ/H block
   verbatim into `manuscript.tex` and tighten for IEEE journal voice
   (active, single-spaced declarations; no hedging adjectives).
2. Add a new §Decentralised Validation Networks subsection under
   Related Work, briefly summarising the focused paper's Bittensor
   framing (`agentic-iov-risk-focused/manuscript.tex` v1.2). Use 4-6
   citations (the existing focused-paper bib has bittensor/TAO/proof-of-stake refs).
3. Add a new §Verifiable Risk Intelligence section between Architecture
   and Use Cases. Pull the validator-loss decomposition from the
   focused paper's §validator-loss (one paragraph; cite the focused
   paper as in-press companion). State the layer-1 (orchestration:
   5,097 rounds, 0 auth failures) vs layer-2 (economic verification —
   not yet) split honestly.
4. Re-cast all section bodies for the *agentic-finance* framing — RQ
   wording in the seed is decentralized-finance only; the published
   paper's framing must be agentic-finance (autonomous agents acting
   on cross-chain signals, not just traders).
5. Use IEEEtran two-column journal format (`\documentclass[journal]{IEEEtran}`).
   The seed used `[conference]` — already corrected in `manuscript.tex`.
6. The bibliography is already seeded (`references.bib`, copied from
   shard). Bittensor / Validator-loss / focused-paper cite keys may
   need to be ported in from `_bib/references.bib` — port only the
   ones actually cited in this manuscript; do **not** wholesale-merge
   the bib.

## Page budget

IEEE Transactions journal — typical 12--16 two-column pages. Target 14.

## Status discipline

- `meta.yaml` `status: scaffold` until AW first compile passes; then
  `status: draft`.
- Do **not** flip past `draft` without explicit CEO sign-off.
- No newsletter / no Paragraph push of this paper at any time. (The
  Paragraph drafts already exist for the accessible-register summaries;
  this is the IEEE-Transactions venue paper and stays in the
  `omnirisk-papers` repo.)

## Output gates

1. `make pdf` succeeds with zero warnings, zero overfull hboxes.
2. Page count ≤ 16 (target 14).
3. Status == `draft`, revision_log entry naming the CEO directive of
   2026-05-07.
4. The `\thanks{...}` placeholders for Ahod are still placeholders
   (CEO will fill once author 2 is confirmed).
5. Post a summary on the AW issue thread when done: page count,
   abstract verbatim, section-by-section page split, and a list of any
   citations the AW added beyond the seed bib.
