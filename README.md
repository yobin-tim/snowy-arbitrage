# The Arbitrage Value of Snowy 2.0

A backtesting simulation that estimates what energy arbitrage (buy cheap electricity,
store it, sell it back when it is expensive) could be worth to a Snowy 2.0-sized
pumped-hydro plant, using four years of real half-hourly NSW spot prices (2022 to
2025). Three dispatch schemes frame the answer: a perfect-foresight ceiling, a
deployable rule of thumb whose two trigger prices are frozen on the training years,
and a forecaster that knows the market's statistical pattern but never the future,
scored on a held-out year. The report is written for non-technical readers; all code
is folded away by default.

## Read it

- **[The report](https://yobin-tim.github.io/snowy-arbitrage/python/snowy-arbitrage.html)** — the full analysis, self-contained in one page.
- **[The interactive demo](https://yobin-tim.github.io/snowy-arbitrage/python/snowy-arbitrage-demo.html)** — drag the rule-of-thumb trigger prices and watch the profit respond.

## Run it

**In the cloud (no install):**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yobin-tim/snowy-arbitrage/blob/main/python/snowy-arbitrage.ipynb)
then "Run all". The first cell installs the few packages Colab lacks; the committed
price snapshots do the rest, so the cloud run reproduces the report's exact numbers
without touching the network.

**Locally** (requires [Quarto](https://quarto.org)):

```bash
cd python
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m ipykernel install --user --name snowy-arbitrage \
    --display-name "Python (snowy-arbitrage)"
quarto render snowy-arbitrage.qmd --to html
```

Rendering is the full run: every cell executes fresh through the pinned kernel, so
the HTML can never show stale numbers, and any failed in-document assertion aborts
the render.

## What is here

| Path | Role |
| --- | --- |
| `python/snowy-arbitrage.qmd` | The single source: prose, code, and assumptions in one Quarto document. Edit this. |
| `python/snowy-arbitrage.ipynb` | Derived notebook copy for Colab and Jupyter. |
| `python/snowy-arbitrage.html` | The rendered, self-contained report. |
| `python/snowy-arbitrage-demo.html` | Server-free interactive demo (vanilla JS, opens in any browser). |
| `python/data/` | Committed price snapshots, one per year. These are why every number reproduces offline. |
| `python/figures/`, `python/results/` | Every figure and output table (dispatch, annual summary, parameters), regenerated on each render. |
| `python/workbench.py` | Scratchpad that loads `data/` and `results/` instantly for ad-hoc questions. |

## Data

Prices are the AEMO dispatch price for the NSW1 region, downloaded from AEMO's
public NEMWeb archive with [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS), filtered
to non-intervention runs, and averaged from 5-minute to 30-minute steps. The
committed snapshots mean nothing is fetched at run time; delete one to force a fresh
download.

## Contributing and provenance

This repository is a one-way mirror of a private workspace. Issues and pull requests
are welcome: the `.qmd` is the file to edit (prose changes need no Python), and the
maintainer folds accepted changes back into the source, re-renders, and pushes the
mirror forward.

This is independent work: open-literature methods (linear programming, Markov price
models, stochastic dynamic programming) applied to public AEMO price data and public
Snowy 2.0 specifications. More about the project:
[yobin-tim.github.io/projects/snowy-arbitrage](https://yobin-tim.github.io/projects/snowy-arbitrage/).
