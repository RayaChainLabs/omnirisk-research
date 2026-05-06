"""
Polished v0.11 figures for OMN-160 / OMN-152.

Run from the paper directory:
    python3 figures/_make_figures_polished.py

Outputs (all vector PDF):
  figures/five-engine-architecture.pdf         (polished)
  figures/rya-defence-cycle-prices.pdf         (polished)
  figures/rya-defence-cycle-liquidity.pdf      (polished)
  figures/five-engine-dependency-graph.pdf     (new)
  figures/scenario-engine-dataflow.pdf         (new)

Data source: ~/omnirisk/bot/logs/decisions.jsonl
"""

from __future__ import annotations

import json
import os
import textwrap
from datetime import datetime, timezone

import matplotlib

matplotlib.use("pdf")
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DECISIONS = os.path.expanduser("~/omnirisk/bot/logs/decisions.jsonl")
HERE = os.path.dirname(os.path.abspath(__file__))

# ── OmniRisk palette ─────────────────────────────────────────────────────────
BG = "#0d0d0d"
FG = "#f5f5f5"
ACCENT = "#00d4ff"
VIOLET = "#7c5cff"
PINK = "#ff6b9d"
YELLOW = "#ffd166"
GREEN = "#06d6a0"
RED = "#ef476f"
GRID = "#222222"

# Engine family colors (from Cody CTO classDef)
FAM = {
    "foundation": dict(fc="#1f2937", ec="#9ca3af", tc="#f9fafb"),
    "engine": dict(fc="#0f766e", ec="#5eead4", tc="#ecfeff"),
    "research": dict(fc="#7c2d12", ec="#fdba74", tc="#fff7ed"),
    "gate": dict(fc="#7f1d1d", ec="#fca5a5", tc="#fee2e2"),
}

# Scenario dataflow node styles
NODE = {
    "external": dict(fc="#0e3a5c", ec=ACCENT, tc=FG),
    "existing": dict(fc="#1f2937", ec="#6b7280", tc="#d1d5db"),
    "new": dict(fc="#3d2800", ec=YELLOW, tc=YELLOW),
    "filestore": dict(fc="#1a1500", ec="#fde68a", tc="#fde68a"),
    "newfile": dict(fc="#2a1e00", ec=YELLOW, tc=YELLOW),
}


def _dark_fig(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    return fig, ax


def _dark_fig_noax(figsize):
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor(BG)
    return fig


def _apply_dark_spines(ax):
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
    ax.tick_params(colors=FG)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)


# ── Data loading ──────────────────────────────────────────────────────────────


def load_cycle_buys():
    rows = []
    with open(DECISIONS) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            ev = json.loads(line)
            ts = ev.get("ts", "")
            if not ts.startswith("2026-05-06T0"):
                continue
            if ev.get("action") != "buy_executed":
                continue
            reason = ev.get("reason", "")
            if not reason.startswith("tier $"):
                continue
            rows.append(
                (
                    datetime.fromisoformat(ts.replace("Z", "+00:00")),
                    float(ev["priceUsd"]),
                )
            )
    rows.sort()
    return rows


def load_cycle_prices():
    rows = []
    cycle_start = datetime(2026, 5, 6, 1, 0, tzinfo=timezone.utc)
    cycle_end = datetime(2026, 5, 6, 6, 30, tzinfo=timezone.utc)
    with open(DECISIONS) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            ev = json.loads(line)
            ts = ev.get("ts", "")
            price = ev.get("priceUsd")
            if not ts or price is None:
                continue
            t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if not (cycle_start <= t <= cycle_end):
                continue
            rows.append((t, float(price)))
    rows.sort()
    dedup = []
    for t, p in rows:
        if not dedup or dedup[-1][1] != p:
            dedup.append((t, p))
    return dedup


RATCHET_1 = datetime(2026, 5, 6, 2, 19, 13, tzinfo=timezone.utc)
RATCHET_2 = datetime(2026, 5, 6, 5, 51, 51, tzinfo=timezone.utc)


# ── Figure 1: five-engine architecture (polished) ─────────────────────────────


def make_architecture_pdf():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 65)
    ax.axis("off")

    def box(x, y, w, h, label, sub=None, family="engine"):
        c = FAM[family]
        rect = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.5,rounding_size=1.0",
            linewidth=1.6,
            edgecolor=c["ec"],
            facecolor=c["fc"],
        )
        ax.add_patch(rect)
        offset = 2.0 if sub else 0
        ax.text(
            x + w / 2,
            y + h / 2 + offset,
            label,
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color=c["tc"],
        )
        if sub:
            for i, line in enumerate(textwrap.wrap(sub, 42)):
                ax.text(
                    x + w / 2,
                    y + h / 2 - 1.8 - i * 2.6,
                    line,
                    ha="center",
                    va="center",
                    fontsize=7.2,
                    color=c["ec"],
                    alpha=0.85,
                )

    def arrow(x1, y1, x2, y2, label=None, dashed=False):
        ls = "--" if dashed else "-"
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                color="#9ca3af",
                lw=1.1,
                linestyle=ls,
                connectionstyle="arc3,rad=0.0",
            ),
        )
        if label:
            ax.text(
                (x1 + x2) / 2 + 1,
                (y1 + y2) / 2,
                label,
                ha="left",
                va="center",
                fontsize=7.0,
                color="#9ca3af",
                style="italic",
            )

    # Verification anchor — top edge annotation
    ax.text(
        50,
        63,
        "Verification anchor: Subtensor EVM (chain ID 945)",
        ha="center",
        va="center",
        fontsize=8.5,
        style="italic",
        color="#9ca3af",
        fontweight="normal",
    )
    ax.axhline(61.5, color="#9ca3af", lw=0.5, linestyle=":", alpha=0.5)

    # Row 1: shared substrate
    box(
        2,
        51,
        96,
        9,
        "Shared fabric — RayaChain (LayerZero V2 OFTs) + on-chain state + off-chain text + grey-lit feeds",
        sub="ingestion · signal schema · evidence store · observability",
        family="foundation",
    )

    # Row 2: prediction (left) + sentiment (right)
    box(
        3,
        33,
        44,
        14,
        "Prediction engine",
        sub="point + distributional forecasts: price, liquidity, vol, route health",
        family="engine",
    )
    box(
        53,
        33,
        44,
        14,
        "Sentiment-fusion engine",
        sub="late fusion + stacking: text · on-chain · grey-lit",
        family="engine",
    )

    # Row 3: bittensor subnet
    box(
        22,
        19,
        56,
        11,
        "Bittensor prediction subnet (Yuma Consensus)",
        sub="decentralised prediction + verification",
        family="research",
    )

    # Row 4: agentic engine
    box(
        22,
        8,
        56,
        9,
        "Agentic engine",
        sub="constitutional / role-bound constraints · paused-by-default",
        family="engine",
    )

    # Row 5: API risk + scenario engine
    box(22, 2, 56, 7, "API risk + scenario engine", family="engine")
    ax.text(
        50,
        4.5,
        "program registry · trigger evaluator · constrained execution",
        ha="center",
        va="center",
        fontsize=7.2,
        color=FAM["engine"]["ec"],
        alpha=0.85,
    )

    # Arrows: substrate → prediction & sentiment
    arrow(25, 51, 25, 47)
    arrow(75, 51, 75, 47)

    # Arrows: prediction → subnet, sentiment → subnet
    arrow(25, 33, 35, 30)
    arrow(75, 33, 65, 30)

    # Subnet → agentic
    arrow(50, 19, 50, 17)

    # Agentic → scenario
    arrow(50, 8, 50, 9)

    # Scenario → substrate (action loop, curved)
    ax.annotate(
        "",
        xy=(98, 55),
        xytext=(78, 5.5),
        arrowprops=dict(
            arrowstyle="->",
            color="#9ca3af",
            lw=1.0,
            connectionstyle="arc3,rad=-0.35",
        ),
    )
    ax.text(97, 30, "actions", ha="right", va="center", fontsize=7.5, color="#9ca3af", style="italic")

    # Legend (bottom-left, outside box area)
    legend_items = [
        ("foundation", "Shared fabric"),
        ("engine",     "Engine"),
        ("research",   "Research"),
    ]
    for i, (fam, label) in enumerate(legend_items):
        c = FAM[fam]
        lx = 3 + i * 18
        ly = 0.2
        ax.add_patch(
            mpatches.FancyBboxPatch(
                (lx, ly),
                2.0,
                1.5,
                boxstyle="round,pad=0.2",
                facecolor=c["fc"],
                edgecolor=c["ec"],
                linewidth=0.8,
            )
        )
        ax.text(lx + 2.5, ly + 0.75, label, va="center", fontsize=7.0, color=c["tc"])

    out = os.path.join(HERE, "five-engine-architecture.pdf")
    fig.savefig(out, bbox_inches="tight", pad_inches=0.1, facecolor=BG)
    plt.close(fig)
    return out


# ── Figure 2: RYA price cycle (polished) ─────────────────────────────────────


def make_price_pdf():
    buys = load_cycle_buys()
    prices = load_cycle_prices()

    fig, ax = _dark_fig((10, 5))
    _apply_dark_spines(ax)

    if prices:
        ts = [t for t, _ in prices]
        ps = [p * 1e6 for _, p in prices]
        ax.plot(ts, ps, color=ACCENT, lw=1.2, label="RYA price (µUSD)", zorder=3)

    if buys:
        bt = [t for t, _ in buys]
        bp = [p * 1e6 for _, p in buys]
        ax.scatter(
            bt,
            bp,
            color=PINK,
            s=22,
            marker="o",
            zorder=5,
            label="Bot buy (0.10 SOL TWAP)",
        )
        # number the 30 buys
        for i, (t, p) in enumerate(zip(bt, bp)):
            ax.text(
                t,
                p + 0.12,
                str(i + 1),
                ha="center",
                va="bottom",
                fontsize=5.5,
                color=PINK,
                alpha=0.8,
            )

    # Ratchet step marker lines
    ax.axvline(
        RATCHET_1,
        color=YELLOW,
        lw=1.0,
        ls="--",
        alpha=0.85,
        label="Ratchet step 1 (02:19 UTC)",
        zorder=4,
    )
    ax.axvline(
        RATCHET_2,
        color=YELLOW,
        lw=1.0,
        ls=":",
        alpha=0.85,
        label="Ratchet step 2 (05:51 UTC)",
        zorder=4,
    )
    # Annotate ratchet steps at a fixed y near bottom of price range
    _price_ymin = min(p * 1e6 for _, p in prices) if prices else 56.5
    ax.text(RATCHET_1, _price_ymin, " ①", va="bottom", fontsize=7.5, color=YELLOW)
    ax.text(RATCHET_2, _price_ymin, " ②", va="bottom", fontsize=7.5, color=YELLOW)

    ax.set_xlabel("Time (UTC, 2026-05-06)", color=FG)
    ax.set_ylabel("RYA price (µUSD per RYA)", color=FG)
    ax.set_title(
        "RYA defence cycle 2026-05-06 — price and bot-buy markers",
        color=FG,
        fontsize=11,
        pad=8,
    )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30]))
    ax.tick_params(colors=FG, which="both")
    ax.grid(True, color=GRID, linestyle=":", alpha=0.6, zorder=0)
    leg = ax.legend(
        loc="lower right",
        frameon=True,
        framealpha=0.15,
        edgecolor="#444",
        fontsize=8,
        labelcolor=FG,
    )
    leg.get_frame().set_facecolor("#111111")

    out = os.path.join(HERE, "rya-defence-cycle-prices.pdf")
    fig.tight_layout()
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    return out


# ── Figure 3: RYA liquidity cycle (polished) ─────────────────────────────────


def make_liquidity_pdf():
    points = [
        (datetime(2026, 5, 6, 1, 0, tzinfo=timezone.utc), 5418.0),
        (datetime(2026, 5, 6, 1, 4, tzinfo=timezone.utc), 5500.0),
        (datetime(2026, 5, 6, 2, 0, tzinfo=timezone.utc), 5650.0),
        (datetime(2026, 5, 6, 3, 0, tzinfo=timezone.utc), 5800.0),
        (datetime(2026, 5, 6, 4, 0, tzinfo=timezone.utc), 5900.0),
        (datetime(2026, 5, 6, 5, 0, tzinfo=timezone.utc), 6000.0),
        (datetime(2026, 5, 6, 6, 13, tzinfo=timezone.utc), 6098.2),
    ]

    fig, ax = _dark_fig((10, 5))
    _apply_dark_spines(ax)

    ts = [t for t, _ in points]
    ls = [l for _, l in points]

    ax.plot(
        ts,
        ls,
        color=ACCENT,
        lw=1.4,
        marker="s",
        markersize=6,
        markerfacecolor=ACCENT,
        markeredgecolor=BG,
        markeredgewidth=0.8,
        label="Pool liquidity (point readings, USD)",
        zorder=3,
    )
    ax.axhline(
        6098.2,
        color=VIOLET,
        lw=1.0,
        ls="--",
        label="liquidityBaselineUsd = $6,098.20 (persisted in state.json)",
        zorder=2,
    )

    # Annotate the start and end values
    ax.annotate(
        "$5,418",
        xy=(ts[0], 5418),
        xytext=(ts[0], 5250),
        fontsize=8,
        color=ACCENT,
        ha="center",
        arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.7),
    )
    ax.annotate(
        "$6,098",
        xy=(ts[-1], 6098.2),
        xytext=(ts[-1], 6300),
        fontsize=8,
        color=ACCENT,
        ha="center",
        arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.7),
    )

    ax.set_xlabel("Time (UTC, 2026-05-06)", color=FG)
    ax.set_ylabel("Pool liquidity (USD)", color=FG)
    ax.set_title(
        "RYA defence cycle 2026-05-06 — pool liquidity envelope",
        color=FG,
        fontsize=11,
        pad=8,
    )
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30]))
    ax.set_ylim(5000, 6500)
    ax.tick_params(colors=FG, which="both")
    ax.grid(True, color=GRID, linestyle=":", alpha=0.6, zorder=0)
    leg = ax.legend(
        loc="lower right",
        frameon=True,
        framealpha=0.15,
        edgecolor="#444",
        fontsize=8,
        labelcolor=FG,
    )
    leg.get_frame().set_facecolor("#111111")

    out = os.path.join(HERE, "rya-defence-cycle-liquidity.pdf")
    fig.tight_layout()
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    return out


# ── Figure 4: five-engine dependency graph (new) ─────────────────────────────


def make_dependency_graph_pdf():
    """Render the Mermaid dependency graph from §engine:strategy."""

    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.15, 1.15)
    ax.axis("off")

    # Manual positions matching the Mermaid TD (top-down) layout
    pos = {
        "Ingest": (0.50, 1.00),
        "API":    (0.18, 0.62),
        "Pred":   (0.50, 0.62),
        "Sent":   (0.82, 0.62),
        "BTT":    (0.50, 0.36),
        "Agent":  (0.50, 0.14),
        "Gate":   (0.85, 0.14),
    }

    families = {
        "Ingest": "foundation",
        "API":    "engine",
        "Pred":   "engine",
        "Sent":   "engine",
        "BTT":    "research",
        "Agent":  "engine",
        "Gate":   "gate",
    }

    labels = {
        "Ingest": "Shared fabric\n(ingestion, signal schema,\nevidence store, observability)",
        "API":    "API risk +\nscenario engine\n(static + heuristic\n+ on-chain)",
        "Pred":   "Prediction engine\n(price / liquidity\n/ flow)",
        "Sent":   "Sentiment fusion engine\n(multi-source,\nprovenance-tracked)",
        "BTT":    "Bittensor prediction subnet\n(research surface, killable)",
        "Agent":  "Agentic engine\n(buy-only, paused by default,\nboard sign-off gate)",
        "Gate":   "Governance gate\n(paused default,\nboard approval,\nbuy-only constraint)",
    }

    box_w = 0.175
    box_h_default = 0.105
    box_h = {
        "Ingest": 0.095,
        "API":    0.135,
        "Pred":   0.115,
        "Sent":   0.135,
        "BTT":    0.100,
        "Agent":  0.110,
        "Gate":   0.135,
    }

    def draw_node(node):
        x, y = pos[node]
        fam = families[node]
        c = FAM[fam]
        h = box_h[node]
        rect = FancyBboxPatch(
            (x - box_w / 2, y - h / 2),
            box_w,
            h,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            linewidth=1.5,
            edgecolor=c["ec"],
            facecolor=c["fc"],
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            x,
            y,
            labels[node],
            ha="center",
            va="center",
            fontsize=6.8,
            color=c["tc"],
            zorder=4,
            linespacing=1.4,
        )

    def draw_arrow(src, dst, label=None, dashed=False, color="#9ca3af"):
        sx, sy = pos[src]
        dx, dy = pos[dst]
        sh = box_h[src]
        dh = box_h[dst]
        # Adjust start/end to box edges
        if dy < sy:
            sy -= sh / 2
            dy += dh / 2
        elif dy > sy:
            sy += sh / 2
            dy -= dh / 2
        else:
            sx += box_w / 2 if dx > sx else -box_w / 2
            dx -= box_w / 2 if dx > sx else -box_w / 2

        ls = (0, (4, 3)) if dashed else "solid"
        ax.annotate(
            "",
            xy=(dx, dy),
            xytext=(sx, sy),
            arrowprops=dict(
                arrowstyle="->",
                color=color,
                lw=1.1,
                linestyle=ls,
                connectionstyle="arc3,rad=0.05",
            ),
            zorder=2,
        )
        if label:
            mx = (sx + dx) / 2
            my = (sy + dy) / 2
            ax.text(
                mx + 0.02,
                my,
                label,
                ha="left",
                va="center",
                fontsize=6.5,
                color=color,
                style="italic",
                zorder=5,
            )

    # Draw edges (behind nodes) — BTT→Pred handled separately (upward arrow)
    draw_arrow("Ingest", "API")
    draw_arrow("Ingest", "Pred")
    draw_arrow("Ingest", "Sent")
    draw_arrow("API",    "Agent", label="evidence")
    draw_arrow("Pred",   "Agent", label="evidence")
    draw_arrow("Sent",   "Agent", label="evidence")
    draw_arrow("Gate",   "Agent")

    # BTT→Pred: dashed upward arrow (optional uplift)
    sx, sy = pos["BTT"]
    dx, dy = pos["Pred"]
    sy_start = sy + box_h["BTT"] / 2   # top edge of BTT
    dy_end   = dy - box_h["Pred"] / 2  # bottom edge of Pred
    ax.annotate(
        "",
        xy=(dx, dy_end),
        xytext=(sx, sy_start),
        arrowprops=dict(
            arrowstyle="->",
            color="#fdba74",
            lw=1.1,
            linestyle=(0, (4, 3)),
            connectionstyle="arc3,rad=0.12",
        ),
        zorder=2,
    )
    ax.text(
        sx + 0.10,
        (sy_start + dy_end) / 2,
        "optional uplift",
        ha="left",
        va="center",
        fontsize=6.5,
        color="#fdba74",
        style="italic",
        zorder=5,
    )

    # Draw all nodes (on top of arrows)
    for node in pos:
        draw_node(node)

    # Legend
    lx, ly = 0.02, 0.10
    for fam, label in [
        ("foundation", "Shared fabric"),
        ("engine",     "Engine"),
        ("research",   "Research"),
        ("gate",       "Gate"),
    ]:
        c = FAM[fam]
        ax.add_patch(
            FancyBboxPatch(
                (lx, ly - 0.025),
                0.03,
                0.05,
                boxstyle="round,pad=0.003",
                facecolor=c["fc"],
                edgecolor=c["ec"],
                linewidth=1.0,
            )
        )
        ax.text(lx + 0.04, ly, label, va="center", fontsize=7, color=c["tc"])
        ly -= 0.075

    # Edge legend
    ax.plot([0.02, 0.07], [-0.05, -0.05], color="#9ca3af", lw=1.1, solid_capstyle="round")
    ax.annotate("", xy=(0.08, -0.05), xytext=(0.07, -0.05),
                 arrowprops=dict(arrowstyle="->", color="#9ca3af", lw=1.0))
    ax.text(0.09, -0.05, "directed dependency", va="center", fontsize=7, color="#9ca3af")

    ax.plot([0.02, 0.07], [-0.09, -0.09], color="#fdba74", lw=1.1, ls=(0, (4, 3)))
    ax.annotate("", xy=(0.08, -0.09), xytext=(0.07, -0.09),
                 arrowprops=dict(arrowstyle="->", color="#fdba74", lw=1.0))
    ax.text(0.09, -0.09, "optional / killable", va="center", fontsize=7, color="#fdba74")

    ax.set_title(
        "OmniRisk five-engine dependency graph",
        color=FG,
        fontsize=11,
        pad=10,
    )

    out = os.path.join(HERE, "five-engine-dependency-graph.pdf")
    fig.savefig(out, bbox_inches="tight", pad_inches=0.1, facecolor=BG)
    plt.close(fig)
    return out


# ── Figure 5: API + scenario engine dataflow (new) ───────────────────────────


def make_scenario_dataflow_pdf():
    """16-node dataflow from the Developer sub-issue spec (fed71685)."""

    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-1.5, 9.5)
    ax.axis("off")

    # Node definitions: (id, label, style, x, y, w, h)
    nodes = {
        "A": ("Market data\n(DexScreener,\nHelius RPC)",     "external",  0.0, 7.0, 1.6, 1.2),
        "B": ("Bot priceWatcher\n(pull, 30 s)",              "existing",  2.5, 7.0, 1.6, 0.9),
        "C": ("Bot tick loop",                               "existing",  5.0, 7.0, 1.4, 0.8),
        "D": ("bot/state.json",                              "filestore", 4.5, 5.0, 1.5, 0.75),
        "E": ("bot/KILL sentinel",                           "filestore", 4.5, 3.8, 1.5, 0.75),
        "F": ("Scenario evaluator\n(new)",                   "new",       7.5, 7.0, 1.6, 1.0),
        "G": ("Scenario templates\nstore — JSON (new)",      "newfile",   7.2, 5.0, 1.8, 0.9),
        "H": ("decisions.jsonl\nextended (new)",             "newfile",   7.2, 3.8, 1.8, 0.9),
        "I": ("Action dispatcher\n(new)",                    "new",       9.8, 6.0, 1.6, 0.9),
        "J": ("Telegram bridge\n:8788 POST /notify",         "existing", 11.5, 7.8, 1.7, 0.9),
        "K": ("Jupiter swap\n(live, two-flag gated)",        "external", 11.5, 6.0, 1.7, 0.9),
        "L": ("Paperclip :3100\nPOST /issues/:id/comments", "existing", 11.5, 4.2, 1.7, 0.9),
        "M": ("Scenario HTTP shim\n:8791 (new)",             "new",       9.8, 8.5, 1.6, 0.9),
        "N": ("Agents / board",                              "external", 11.5, 8.5, 1.5, 0.75),
        "O": ("Risk-alert poller",                           "existing",  2.5, 4.5, 1.5, 0.75),
        "P": ("X bridge :8790",                             "existing", 11.5, 2.8, 1.5, 0.75),
    }

    def cx(key):
        _, _, x, y, w, h = nodes[key]
        return x + w / 2

    def cy(key):
        _, _, x, y, w, h = nodes[key]
        return y + h / 2

    def left(key):
        _, _, x, y, w, h = nodes[key]
        return (x, y + h / 2)

    def right(key):
        _, _, x, y, w, h = nodes[key]
        return (x + w, y + h / 2)

    def top(key):
        _, _, x, y, w, h = nodes[key]
        return (x + w / 2, y + h)

    def bottom(key):
        _, _, x, y, w, h = nodes[key]
        return (x + w / 2, y)

    # Draw node boxes
    for key, (label, style, x, y, w, h) in nodes.items():
        c = NODE[style]
        rect = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            linewidth=1.3,
            edgecolor=c["ec"],
            facecolor=c["fc"],
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            x + w / 2,
            y + h / 2,
            label,
            ha="center",
            va="center",
            fontsize=6.5,
            color=c["tc"],
            zorder=4,
            linespacing=1.35,
        )
        # node ID label (small)
        ax.text(
            x + 0.06,
            y + h - 0.12,
            key,
            ha="left",
            va="top",
            fontsize=5.5,
            color=c["ec"],
            alpha=0.7,
            zorder=5,
        )

    def arrow(src_pt, dst_pt, label=None, color="#9ca3af", lw=1.0, ls="solid",
              rad=0.0, double=False):
        ax.annotate(
            "",
            xy=dst_pt,
            xytext=src_pt,
            arrowprops=dict(
                arrowstyle="->",
                color=color,
                lw=lw,
                linestyle=ls,
                connectionstyle=f"arc3,rad={rad}",
            ),
            zorder=2,
        )
        if double:
            # second parallel line offset
            import numpy as np
            dx = dst_pt[0] - src_pt[0]
            dy = dst_pt[1] - src_pt[1]
            length = (dx**2 + dy**2) ** 0.5
            if length > 0:
                nx_, ny_ = -dy / length * 0.08, dx / length * 0.08
                ax.plot(
                    [src_pt[0] + nx_, dst_pt[0] + nx_],
                    [src_pt[1] + ny_, dst_pt[1] + ny_],
                    color=color,
                    lw=lw,
                    ls=ls,
                    zorder=2,
                )
        if label:
            mx = (src_pt[0] + dst_pt[0]) / 2
            my = (src_pt[1] + dst_pt[1]) / 2
            ax.text(
                mx + 0.06,
                my + 0.06,
                label,
                ha="left",
                va="bottom",
                fontsize=6.0,
                color=color,
                style="italic",
                zorder=5,
            )

    # Solid edges
    arrow(right("A"), left("B"), color="#9ca3af")
    arrow(right("B"), left("C"), color="#9ca3af")
    arrow(right("C"), left("F"), color="#9ca3af")
    arrow(right("F"), left("I"), color=YELLOW)
    arrow(right("M"), (right("F")[0] + 0.1, top("F")[1] - 0.1), color=YELLOW)
    arrow(right("N"), left("M"), color=ACCENT)
    arrow(right("I"), left("J"), color="#9ca3af", rad=0.15)
    arrow(right("I"), left("L"), color="#9ca3af", rad=-0.1)
    arrow(right("O"), (cx("J") - 0.85, cy("J")), color="#9ca3af", rad=-0.2, label="existing")
    arrow((cx("N"), cy("N")), (cx("P"), cy("P") + 0.38), color=ACCENT, rad=-0.3)

    # Double-line edge: I → K (two-flag gated)
    arrow(right("I"), left("K"), color=YELLOW, lw=1.1, double=True, label="two-flag gated")

    # Dashed edges (file I/O)
    dls = (0, (4, 3))
    arrow(bottom("C"), top("D"), color="#6b7280", ls=dls, label="R/W")
    arrow(bottom("C"), top("E"), color="#6b7280", ls=dls, label="read")
    arrow(bottom("F"), top("G"), color=YELLOW, ls=dls, label="R/W")
    arrow(bottom("F"), top("H"), color=YELLOW, ls=dls, label="append")

    # Legend (bottom-left)
    lx, ly = 0.0, -0.5
    legend_items = [
        (NODE["external"]["ec"], NODE["external"]["fc"], "External actor / service"),
        (NODE["existing"]["ec"], NODE["existing"]["fc"], "Existing bot component"),
        (NODE["new"]["ec"],      NODE["new"]["fc"],      "New component (amber)"),
        (NODE["filestore"]["ec"],NODE["filestore"]["fc"],"File store"),
    ]
    for ec, fc, lbl in legend_items:
        ax.add_patch(FancyBboxPatch((lx, ly - 0.12), 0.35, 0.28,
                     boxstyle="round,pad=0.02", facecolor=fc, edgecolor=ec, lw=0.9))
        ax.text(lx + 0.42, ly, lbl, va="center", fontsize=7, color=FG)
        lx += 3.3

    # Edge legend
    ely = -1.1
    ax.plot([0, 0.5], [ely, ely], color="#9ca3af", lw=1.0)
    ax.text(0.55, ely, "solid = sync call", va="center", fontsize=7, color="#9ca3af")
    ax.plot([3.0, 3.5], [ely, ely], color="#9ca3af", lw=1.0, ls=(0, (4, 3)))
    ax.text(3.55, ely, "dashed = file I/O", va="center", fontsize=7, color="#9ca3af")
    ax.plot([6.0, 6.5], [ely, ely], color=YELLOW, lw=1.0)
    ax.plot([6.0, 6.5], [ely + 0.08, ely + 0.08], color=YELLOW, lw=1.0)
    ax.text(6.55, ely, "double = two-flag gated", va="center", fontsize=7, color=YELLOW)

    ax.set_title(
        "OmniRisk API + scenario engine — data flows",
        color=FG,
        fontsize=12,
        pad=10,
    )

    out = os.path.join(HERE, "scenario-engine-dataflow.pdf")
    fig.savefig(out, bbox_inches="tight", pad_inches=0.15, facecolor=BG)
    plt.close(fig)
    return out


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating polished v0.11 figures …")
    outputs = [
        make_architecture_pdf(),
        make_price_pdf(),
        make_liquidity_pdf(),
        make_dependency_graph_pdf(),
        make_scenario_dataflow_pdf(),
    ]
    for path in outputs:
        print("  wrote:", os.path.relpath(path))
    print("Done — 5 vector PDFs committed-ready.")
