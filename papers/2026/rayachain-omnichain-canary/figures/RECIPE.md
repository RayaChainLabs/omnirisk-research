# RECIPE — canary-signal-flow (OMN-175)  v2

> **v2 supersedes v1.** v1 archived at `_archived/v1-canary-signal-flow.*`
> v2 spec locked by CEO 2026-05-08 (comment bc03630b on OMN-175).

## What the diagram says

End-to-end RayaChain canary signal flow across 13 activities and four
swimlanes (Detect / Transform / Propagate / Decide+Respond), plus an
Audit sub-rail.

**Phase summary:**
- **Detect (A1–A3, L1):** anomalous on-chain event observed → normalized to
  typed `WalletSignal` → posted to subnet feed.
- **Transform (A4–A6):** L1 — miners emit `(pᵢ, cᵢ, rᵢ)` forecasts (A4);
  validator scores against realized E1–E4 outcomes — Brier + Inconsistency +
  Calibration loss (A5); decision diamond D1 (score ≥ θ?) gates continuation.
  L2 — signed envelope `{signal_id, source_chain, asset, score, confidence,
  anomaly_flag, evidence_hash, ts}` produced (A6).
- **Propagate (A7–A9, L2):** route via OFT lanes (A7) → broadcast topic
  fan-out (A8) → receivers verify validator-quorum signature (A9); decision
  diamond D2 (sig valid?) gates onward flow.
- **Decide+Respond (A10–A13, L1):** envelope ingested (A10) → role-bound
  policy applied under constitutional constraints (A11); decision diamond D3
  (role permits?) routes to committed action (A12) or governance queue.
  Outcome event fed back to validator as ground truth (A13).

**Feedback loop:** A13 → A4 curved return arrow (economic self-correction).

**Audit sub-rail:** A2, A6, A12 each emit a signed record; Merkle-root
anchored on Subtensor EVM.

**OMN-176 hook:** A5 carries the feature-input insertion point (Table N).

**Honesty marker:** Layer-1 nodes (A1–A5, A10–A13) solid black border;
Layer-2 nodes (A6–A9: validator-quorum signing, OFT routing, receivers)
dashed layerblue border + tinted fill. Muted blue is the *only* accent
colour so the L1/L2 distinction is visually load-bearing.

## Data behind it

Static architecture derived from the locked CEO design spec (OMN-175 comment
bc03630b, 2026-05-08) and §Architecture / §Verifiable Risk Intelligence of
`papers/2026/rayachain-omnichain-canary/manuscript.tex`.
No fabricated numbers.

## Tool

TikZ (LaTeX-native), `article` class + tight-page trick.

## Source files

- `canary-signal-flow.tex` — TikZ source of truth (v2)
- `canary-signal-flow.pdf` — vector PDF for IEEEtran inclusion (~125 KB)
- `canary-signal-flow.svg` — scalable vector for web (~224 KB)
- `canary-signal-flow.png` — 200 DPI raster (~220 KB)
- `_archived/v1-canary-signal-flow.*` — superseded v1 (5-activity version)

## Render command

```bash
cd papers/2026/rayachain-omnichain-canary/figures

pdflatex -interaction=nonstopmode canary-signal-flow.tex
pdf2svg canary-signal-flow.pdf canary-signal-flow.svg
pdftoppm -r 200 -png canary-signal-flow.pdf canary-signal-flow-p
mv canary-signal-flow-p-1.png canary-signal-flow.png
```

Requires: TeX Live with TikZ (`pgf`), `lmodern`, `amsmath`, `geometry`.

## Palette

| Element            | Colour                     |
|--------------------|----------------------------|
| L1 activity border | black, solid               |
| L2 activity border | `layerblue` = RGB(90,130,175), dashed |
| L2 activity fill   | `layerblue!9` (~9% tint)   |
| All other elements | black / gray               |

Single accent colour. No corporate branding.

## Dimensions

- TikZ canvas: ~41.5 × 13.5 cm (natural coordinates before page-crop)
- Full-width include: `\includegraphics[width=\textwidth]{figures/canary-signal-flow}`
- IEEEtran `figure*` → spans both columns at 7.16 in

## Suggested caption (copy-paste ready)

```latex
\caption{End-to-end RayaChain canary signal flow. Anomalous on-chain events
(Detect, A1--A3) are normalized to typed \texttt{WalletSignal} envelopes,
scored by the OmniRisk subnet under a Brier\,+\,Inconsistency\,+\,Calibration
validator loss (Transform, A4--A5), and propagated cross-chain via signed OFT
envelopes (Propagate, A7--A9). Consumer systems ingest envelopes and act under
role-bound constitutional constraints (Decide\,+\,Respond, A10--A13). \emph{Solid}
nodes (Layer-1) are orchestration-validated by the 5{,}097-round shadow soak;
\emph{dashed blue} nodes (Layer-2)---validator-quorum signing, OFT routing, and
quorum-verifying receivers---are designed but deferred. The curved feedback arrow
(A13$\to$A4) closes the economic self-correction loop: realized outcomes are the
ground-truth signal for the validator loss. Decision diamonds gate the flow at
score threshold (D1), envelope-signature verification (D2), and role-permission
check (D3). Cross-reference Table~N (feature inventory, \cite{omn176}) for the
per-score input decomposition at A5.}
\label{fig:canary-signal-flow}
```

## Manuscript insertion point

Insert as `\begin{figure*}[t]` at the top of §Architecture
(`\section{Architecture}`) before the `WalletSignal` IDL listing.
Reference in text as `Figure~\ref{fig:canary-signal-flow}`.
A secondary reference in §Verifiable Risk Intelligence is appropriate when
discussing the validator scoring pipeline.

## Last reviewed

2026-05-08 / OMN-175 v2 / Designer agent (pdflatex, TeX Live 2026, TikZ pgf 3.x)
