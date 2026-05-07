# Reviewer Response — v1.0 → v1.1

**Manuscript:** *Agentic, Context-Aware Risk Intelligence in the Internet of Value*
**Revision:** v1.0 → v1.1 (2026-05-07)
**Source feedback:** CEO-forwarded peer-review note (Paperclip OMN-152
comment `6e86b889`, 2026-05-07T07:16Z).

This document records, point-by-point, how each reviewer comment was
handled in the v1.0 → v1.1 revision. Points are addressed in the
reviewer's order. "Addressed" = change landed in the manuscript;
"partial" = handled in part, with the residual deliberately deferred
and the reason given; "deferred" = explicitly accepted as v2.0+
follow-up work per the reviewer's own deferral list.

---

## 1. Reframe §case-study from "token defence" to "policy-constrained stress-response experiment"

**Status:** addressed.

Section heading rewritten from *"The RYA Liquidity-Defence Cycle"* to
*"A Policy-Constrained Liquidity Stress-Response Experiment"*.
Sub-headings: *"Act I --- 2026-05-06, dump and defence"* →
*"Phase I --- 2026-05-06, first stress event and policy-bound
intervention"*; *"Act II --- second sell wave and ratchet 3"* →
*"Phase II --- second stress event and ratchet step 3"*; *"Act III ---
the stop-loss event"* kept (already neutral). Throughout the prose, the
reviewer's vocabulary swap table was applied (dump → stress event;
defence → policy-bound intervention; CEO override → manual governance
escalation; CEO sign-off → manual governance escalation/out-of-band
escalation; recovery → reconverged). Wall-clock-verb anchors rewritten
as $T_0$, $T_0+\Delta$, $T_1$ where appropriate. Vocabulary swaps
propagated to the abstract, §intro, §conclusion, §funding, and §ethics
so the reframe is consistent across the manuscript, not only inside
§case-study. Numerical claims and timestamps are unchanged: this is a
language pass, not a data pass.

## 2. Validation-status table

**Status:** addressed.

Inserted as `tab:validation-status` at the end of §arch (under a new
*Validation status* subsection) with the five rows the reviewer
specified: Prediction (YES), Sentiment fusion (PARTIAL), Bittensor
verification (SHADOW ONLY), Agentic (POLICY VALIDATED), API-risk /
scenario (YES). Caption explicitly defines the four measurement levels
to preempt the *"this is mostly a systems proposal with anecdotal
evidence"* attack.

## 3. §threat-model section

**Status:** addressed.

New `\section{Threat Model and Trust Assumptions}` (`sec:threat`)
inserted between §arch and §formal. Realised as a single tabularx
(`tab:threat-model`) with seven rows over Adversary / Capability /
Defence / Residual risk: malicious miner, colluding validators,
sentiment poisoning, oracle/route manipulation, replay attacker,
governance bypass, compromised runtime node. The table format is
denser than the reviewer's per-paragraph structure but matches the
reviewer's explicit row template (*"Each row: Adversary | Capability |
Defence | Residual risk"*) and keeps the section to ~1 page as
requested. Two new citations added inline in the table:
`cong2022crypto` (wash trading defeats fusion-divergence detector under
sentiment-poisoning row) and `daian2020flash` (sandwiching capability
under oracle/route-manipulation row).

## 4. Mathematical formalisation ($L_i$ decomposition)

**Status:** addressed.

New `\section{Formal Validator-Loss Specification}` (`sec:formal`)
inserted between §threat-model and §case-study. Defines: miner output
$m_i = (p_i, c_i)$; realised event indicator $y \in \{0,1\}$ over four
event classes $E_1$--$E_4$ (route-level liquidity contraction; price
drop; bridge/oracle anomaly; governance state change); validator loss
$L_i = \alpha \cdot \mathrm{Brier}(p_i, y) + \beta \cdot
\mathrm{Inconsistency}(m_i) + \gamma \cdot \mathrm{Calibration}(c_i)$
with $\alpha + \beta + \gamma = 1$; defaults
$\alpha = 0.6, \beta = 0.2, \gamma = 0.2$. Every symbol declared on
first use ($m_i, p_i, c_i, y, \Delta, \alpha, \beta, \gamma, W,
E_1$--$E_4$). Killable-uplift property formally re-stated. Section
explicitly flags the specification as a design proposal; this paper
does not measure $L_i$ against a live multi-miner metagraph (deferred
per §limits).

## 5. Bittensor scoring-spec paragraph (precision specifications)

**Status:** addressed.

New `\paragraph{Scoring specification (design proposal)}` paragraph
inside the Bittensor verification subnet subsection of §arch. Replaces
the loose phrase *"economically scores outputs against realised
cross-chain events"* with the four explicit values the reviewer
requested: scoring window $\Delta = 24$ hours; binary event resolution
$y \in \{0,1\}$ with classes $E_1$--$E_4$ defined in §formal; reward
lag = prediction $\to$ resolution $\to$ score $\to$ next epoch's reward
distribution (one-epoch lag); calibration window $W = 1{,}000$ paired
$(c_i, y)$ samples with bin width $0.1$. All four are stated explicitly
as design proposals, not measurements.

## 6. Writing-level passes

**Status:** addressed.

- *Repeated phrases.* "fully-public empirical artefacts" (was 3x in
  v1.0) → 0 in v1.1; "paused-by-default" (was 5x) softened in two
  locations to "begins each session in a paused state that only an
  out-of-band approval can flip" and "the paused-by-default stance"
  (3 occurrences kept where load-bearing); "role contract" (was 12x)
  is the load-bearing object name and was varied between *Trader-role
  contract*, *role contract*, *constitution*, *Trader-role policy*,
  *Trader-role constitution*, *policy contract* — not artificially
  cut.
- *Abstract length.* Trimmed from ~242 words (v1.0) to ~156 words
  (v1.1), well under the reviewer's ~165 target. Implementation
  specifics dropped (52-buy / 5.2-SOL / role-contract details). The
  IoV-thesis opener is kept per the CEO's "do NOT change" list.
- *"Why now" paragraph.* New `\paragraph{Why now.}` in §intro names the
  four failure modes the reviewer specified, each in one sentence with
  one citation: bridge fragmentation (`augusto2024sok`); liquidity
  fragmentation (`zhang2023sok`); narrative contagion
  (`schumaker2009textual`); agentic execution risk
  (`bai2022constitutional`).

## 7. "Do NOT change" list

**Status:** honoured.

Title kept as *Agentic, Context-Aware Risk Intelligence in the Internet
of Value* (the rename landed at commit `d1938c5` and is preserved).
Author block kept verbatim. Five-engine framing kept as the headline
contribution. OmniRisk Architecture figure (Figure~1, commit `281da40`)
kept; only its `width=\linewidth` was reduced to `width=0.92\linewidth`
and `[ht]` placement was changed to `[t]` to fix a float-cascade that
was deferring both figures to the end of the document and pushing the
page count to 17. Caption text and content unchanged. The IoV abstract
opener is preserved; the abstract was trimmed in length but its leading
sentence (the IoV thesis) is unchanged. §metrics calibration arc with
class-imbalance honesty kept verbatim. §langgraph 3-paragraph
compression kept verbatim modulo one phrase swap (*"role contracts,
paused-by-default policy"* → *"role contracts, the paused-by-default
stance"*) to satisfy the repeated-phrase audit.

## 8 (output gate). Output gates

**Status:** all met.

| Gate | Target | Result |
|---|---|---|
| 1. revision | 1.0 → 1.1 | met (`meta.yaml` revision: "1.1") |
| 2. status | submission-ready | met (unchanged from v1.0) |
| 3. §case-study reframe | no *defence/dump/override/buy ladder* in headings or topic sentences | met (single residual occurrence of "defence" in the keyword line is the reframed *policy-constrained liquidity intervention*; "defence" elsewhere refers to architectural defence-in-depth, not bot action) |
| 4. §threat-model | new section, ~1 page | met (single-table page) |
| 5. §formal | $L_i$ decomposition with every symbol declared | met |
| 6. Bittensor scoring spec | $\Delta=24$h, $y\in\{0,1\}$, one-epoch lag, $W=1{,}000$, bin width $0.1$ | met (all five values stated explicitly) |
| 7. validation-status table | inserted | met (`tab:validation-status`) |
| 8. abstract length | ~165 words | met (~156 words) |
| 9. "why now" paragraph | added to §intro | met |
| 10. zero warnings, ≤15 pages | zero, 15 | met (15 pages, zero warnings, zero overfull hboxes, zero underfull hboxes, no missing-font-shape notices) |
| 11. submission/reviewer-response.md | this file | met |

## Deferred for v2.0+ (per reviewer's own deferral list)

- A second-pool / second-token replication study.
- A miner-competition experiment on a multi-miner metagraph (would
  let us actually measure $L_i$ against realised events, lifting the
  validator-loss claim from architectural to empirical).
- An ablation study (drop each engine, measure delta).

These are explicitly out of scope for v1.1, which is the cleanest
possible v1.0 cut, not a v2.0 attempt.
