# omnirisk-papers

Academic publications from the **OmniRisk Academic Writer** agent. Source of truth lives here in git; published PDFs replicate to the `omnirisk-insights-bucket` S3 bucket and are served at `https://green.omnirisk.io/media/papers/<year>/<slug>/manuscript.pdf`.

## Layout

```
papers/                           top-level papers root
├── _bib/
│   └── references.bib            MASTER bibliography, shared across every paper
├── _templates/
│   └── article/                  default LaTeX scaffold (article class + biblatex)
├── bin/
│   ├── new                       scaffold a new paper from _templates
│   └── publish                   build + replicate to S3 + stamp meta.yaml
├── papers/<year>/<slug>/         one directory per paper
│   ├── manuscript.tex            canonical source
│   ├── references.bib            symlink → ../../../_bib/references.bib
│   ├── figures/                  vector PDFs / SVGs only
│   ├── Makefile                  `make pdf`, `make watch`, `make clean`
│   ├── meta.yaml                 catalog index entry (title, venue, status, URL, DOI)
│   └── build/                    gitignored; latexmk output
└── Makefile                      top-level: `new`, `publish`, `list`, `help`
```

## Workflow

```bash
# 1. Scaffold a new paper (defaults year to current calendar year)
make new SLUG=risky-subnets

# 2. Edit the manuscript
$EDITOR papers/2026/risky-subnets/manuscript.tex

# 3. Build locally and watch
cd papers/2026/risky-subnets && make pdf
# or `make watch` for continuous rebuild

# 4. Add citations to the master bibliography
$EDITOR _bib/references.bib

# 5. Publish — builds + uploads to S3 + stamps canonical_url in meta.yaml
make publish PAPER=papers/2026/risky-subnets

# 6. Commit source changes (git ignores PDFs)
git add -A && git commit -m "publish risky-subnets"
```

## Storage roles

| Role | Where | Why |
| --- | --- | --- |
| **Source of truth** | this git repo | full diff history, peer-review trail, recovery if the host dies |
| **Build artefacts** | `papers/.../build/` | gitignored, reproducible from source |
| **Published artefacts** | `s3://omnirisk-insights-bucket/papers/<year>/<slug>/` | distribution, archival, citation-stable URL via `green.omnirisk.io` |

The replication is **explicit**, not automatic — only `make publish` pushes to S3. Drafts never leak.

## Bibliography rules

`_bib/references.bib` is the **single** bibliography. Every paper symlinks to it (the `bin/new` script does this for you). When you cite a new work:

1. Add the entry to `_bib/references.bib` with a stable identifier (DOI when available; otherwise a stable URL + an `urldate`).
2. Cite key convention: `<firstauthorlastname><year><firstmeaningfulwordoftitle>` (e.g. `nakamoto2008bitcoin`).
3. Never include an entry you have not verified resolves.
4. Cite keys are reused across papers — that's the whole point of a shared bib.

## S3 replication

`bin/publish` runs:

```bash
aws --profile $AWS_PROFILE --region $AWS_REGION s3 cp \
  papers/<year>/<slug>/build/manuscript.pdf \
  s3://omnirisk-insights-bucket/papers/<year>/<slug>/manuscript.pdf
```

Plus a source bundle (`<slug>-source.tar.gz`) so the venue-formatted source ships alongside the PDF.

Required env (defaults work if you already have risk-intel's env loaded):
- `AWS_PROFILE` (default: `default`)
- `AWS_REGION` (default: `eu-west-1`)
- `INSIGHTS_MEDIA_BUCKET_NAME` (default: `omnirisk-insights-bucket`)
- `INSIGHTS_MEDIA_BASE_URL` (default: `https://green.omnirisk.io/media`)

## Catalog (meta.yaml)

Each paper carries a `meta.yaml` that the CEO and Broadcaster read to know what's been published. `bin/publish` updates `canonical_url` and `published_at` automatically on success.

```yaml
title: "Risky Subnets in Bittensor: A Survey"
slug: "risky-subnets"
authors:
  - name: "OmniRisk"
    email: "research@omnirisk.io"
target_venue: "arxiv"
status: "published"
created_at: "2026-05-03"
submitted_at: "2026-05-12"
published_at: "2026-05-15T10:30:00Z"
doi: "10.48550/arXiv.2509.12345"
arxiv_id: "2509.12345"
canonical_url: "https://green.omnirisk.io/media/papers/2026/risky-subnets/manuscript.pdf"
tags: ["bittensor","risk","subnets"]
```

## Owner

The OmniRisk **Academic Writer** agent owns this repo. The CEO approves venue + submission timing. Cross-referenced from the Academic Writer's `AGENTS.md` storage section.
