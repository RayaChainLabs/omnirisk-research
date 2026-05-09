---
title: "Authors' Articles"
description: "Long-form OmniRisk articles contributed by external authors, converted from source .docx for research and reuse."
---

# Authors' Articles

Long-form OmniRisk articles contributed by external authors. Source `.docx` files
are kept here for traceability; the canonical, citable version of each piece is
the corresponding `.md` file. Embedded images live under `media/<slug>/`.

## Index

| Author  | Title                                                                                              | Markdown |
| ------- | -------------------------------------------------------------------------------------------------- | -------- |
| Aleena  | Wallet Risk Score Explained: What the Numbers Actually Mean                                        | [aleens-wallet-risk-score-explained-what-the-numbers-actually-mean.md](./aleens-wallet-risk-score-explained-what-the-numbers-actually-mean.md) |
| Ema     | Onchain Analysis for Risk Management: How to Read Blockchain Data Like a Pro                       | [ema-onchain-analysis-for-risk-management-how-to-read-blockchain-data-like-a-pro.md](./ema-onchain-analysis-for-risk-management-how-to-read-blockchain-data-like-a-pro.md) |
| Hans    | Wallet Risk Score Explained: What the Numbers Actually Mean (And What Most Tools Don't Tell You)   | [hans-wallet-risk-score-explained-what-the-numbers-actually-mean-and-what-most-tools-don-t-tell-you.md](./hans-wallet-risk-score-explained-what-the-numbers-actually-mean-and-what-most-tools-don-t-tell-you.md) |
| Idris   | How OmniRisk Helps Users Detect Cross-Chain Risk Before It Becomes Visible in Token Price          | [idris-how-omnirisk-helps-users-detect-cross-chain-risk-before-it-becomes-visible-in-token-price.md](./idris-how-omnirisk-helps-users-detect-cross-chain-risk-before-it-becomes-visible-in-token-price.md) |
| Steve   | RayaChain as a Canary Layer: Broadcasting Risk and Credit Signals Across Chains                    | [steve-rayachain-test-article.md](./steve-rayachain-test-article.md) |
| Unknown | Why Most DeFi Risk Tools Have a Blind Spot                                                         | [why-most-defi-risk-tools-have-a-blind-spot-2.md](./why-most-defi-risk-tools-have-a-blind-spot-2.md) |
| Zain    | Wallet Risk Score Explained: What the Numbers Actually Mean                                        | [zain-omnirisk-wallet-risk-score-article.md](./zain-omnirisk-wallet-risk-score-article.md) |

## Conversion notes

- Source `.docx` files were converted with `pandoc 3.9.0.2` using `-f docx -t gfm --wrap=none`.
- Embedded images were extracted with `--extract-media=media/<slug>` so each article's images live in its own subdirectory.
- A YAML frontmatter block with `title`, `author`, and `source` was prepended to each `.md` to make the canonical metadata machine-readable.
- The original `.docx` files are kept alongside the markdown for diffability and rerun-ability.
- `Report.pdf` and the loose `aleena.png` image are not author articles and were left as-is in this folder.
