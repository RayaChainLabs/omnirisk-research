# arXiv Submission Bundle

**Title:** A Five-Engine Architecture for Agentic, Context-Aware Risk
Prediction in the Internet of Value (Focused companion to the
OmniRisk--RayaChain--Bittensor technical report).

**Authors:** Basel Magableh (Technological University Dublin), OmniRisk
Research (Rayachain Lab).

**Abstract category split.** arXiv categories:

- **Primary:** `cs.CR` (Cryptography and Security)
- **Cross-list:** `q-fin.RM` (Risk Management)

**Comment field (≤120 chars):**

```
Companion to follow-up technical report; reproducibility data
committed at git commits b419338, e726153.
```

**MSC 2020:** `68M14`, `68T05`, `91G70`.

**ACM CCS:** Security and privacy → Distributed systems security →
Distributed algorithms (primary); Computing methodologies → Artificial
intelligence → Multi-agent systems; Applied computing → Electronic
commerce → Digital cash.

**License:** arXiv non-exclusive license to distribute (default).

**Bundle contents (.tar.gz to upload):**

| Path (relative to bundle root) | Source |
|---|---|
| `manuscript.tex` | `papers/2026/agentic-iov-risk-focused/manuscript.tex` |
| `references.bib` | `_bib/references.bib` (de-symlinked, copied as a regular file) |
| `figures/five-engine-dependency-graph.pdf` | `papers/2026/omnirisk-rayachain-bittensor/figures/five-engine-dependency-graph.pdf` (copied; arXiv does not allow `..` paths) |
| `00README.md` | this directory |

**Build instructions for arXiv:**

arXiv runs `pdflatex` automatically. The manuscript builds cleanly with
`latexmk -pdf manuscript.tex` against any TeX Live 2024+ install. The
`seqsplit` package is referenced via a `\providecommand` fallback so
the build succeeds whether or not the package is installed on the
target TeX system (arXiv ships a recent texlive that includes it).
Bibliography is `numeric-comp` style (renders IEEE-compatible numbered
citations); switch to `style=ieee` on the camera-ready cut for IEEE TIFS
submission if `biblatex-ieee` is available.

**Withdrawal policy:** the corresponding author retains the right to
withdraw or replace the preprint at any time per arXiv's standard
submission policy.
