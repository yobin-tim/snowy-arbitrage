# The Arbitrage Value of Snowy 2.0

A backtesting simulation that estimates what energy arbitrage (buy cheap electricity,
store it, sell it back when it is expensive) could be worth to a Snowy 2.0-sized
pumped-hydro plant, using four years of real half-hourly NSW spot prices (2022 to
2025). Three dispatch schemes frame the answer: a perfect-foresight ceiling, a deployable
rule of thumb whose two trigger prices are frozen on the training years, and a forecaster
who knows the market's statistical pattern but never the future, scored on a held-out year.
The report is written for non-technical readers; all code is folded away by default.

**Read the report:**
[yobin-tim.github.io/snowy-arbitrage](https://yobin-tim.github.io/snowy-arbitrage/python/snowy-arbitrage.html)

## How to use it

### Read it (no install)

The rendered report is served at
[yobin-tim.github.io/snowy-arbitrage/python/snowy-arbitrage.html](https://yobin-tim.github.io/snowy-arbitrage/python/snowy-arbitrage.html);
every figure, number, and folded code block is baked in. Its small interactive companion
lives at
[yobin-tim.github.io/snowy-arbitrage/python/snowy-arbitrage-demo.html](https://yobin-tim.github.io/snowy-arbitrage/python/snowy-arbitrage-demo.html),
where you can drag the two trigger prices of the rule-of-thumb scheme and watch the
profit respond. (Both pages are the files `snowy-arbitrage.html` and
`snowy-arbitrage-demo.html` in this repository, served as-is.)

### Run it in the cloud (no install, live code)

Click the **Open in Colab** badge at the top of the report or the notebook. The first
cell installs the pinned packages from `requirements.txt` and fetches the four committed
price snapshots from the repository, so the cloud run reproduces the same numbers offline
rather than pulling live data from AEMO. Everything else the report needs is defined in
the notebook itself, so there is nothing more to fetch. No account setup beyond a Google
login.

### Run it locally (full control)

```bash
# from the repository root
cd python
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt          # pinned, known-good versions
.venv/bin/python -m ipykernel install --user --name snowy-arbitrage \
    --display-name "Python (snowy-arbitrage)"      # register the kernel

# execute everything and rebuild the HTML report in one step
# (requires Quarto, https://quarto.org)
quarto render snowy-arbitrage.qmd --to html
```

Rendering **is** the full run: Quarto executes every cell fresh through the
`snowy-arbitrage` kernel each time, so the HTML can never show stale numbers, and any
raised assertion aborts the render. To work cell by cell instead, open
`snowy-arbitrage.qmd` in VS Code with the Quarto extension, or open the derived
`snowy-arbitrage.ipynb` in Jupyter.

## Files

| File | Role |
| --- | --- |
| `snowy-arbitrage.qmd` | **The single source of truth.** The full report as plain-text Quarto markdown: prose, code, YAML header. Edit this; render this. |
| `snowy-arbitrage.ipynb` | Derived copy for Colab and Jupyter, regenerated from the source with `quarto convert snowy-arbitrage.qmd --output snowy-arbitrage.ipynb`. Do not edit it directly; changes made here do not flow back. |
| `snowy-arbitrage.html` | The rendered, self-contained report. Read this if you only read one thing. |
| `snowy-arbitrage-demo.html` | Server-free interactive demo of the threshold scheme (vanilla JS, opens in any browser). |
| `requirements.txt` | Pinned dependencies for the venv, Colab, and Binder. The repo-root `binder/requirements.txt` simply includes this file, since Binder does not look inside `python/`. |
| `data/nsw1_prices_*_30min.parquet` | Committed price snapshots, one per year. **This is why the notebook reproduces exact numbers offline.** Public AEMO data, tidied to 30-minute steps. Delete a snapshot to force a fresh download from AEMO (via the open-source NEMOSIS package). |
| `figures/*.png` | Every figure, saved on each run, ready for presentation slides. |

## Maintainer workflow: review and publish a change

The plain-text `snowy-arbitrage.qmd` is the Quarto source; Quarto executes and renders it
in one step. Every change therefore starts and ends in the `.qmd`.

**1. Review.** Read `snowy-arbitrage.html` for the reader experience (folded code,
collapsed notes, hover definitions) and the `.qmd` for code and prose. Things to
hunt: contractions, em dashes, any mention of the Excel model outside the one collapsed
note, numbers presented as the headline rather than as support, stale figures after a
methods change.

**2. Edit** the `.qmd` in any text editor. Prose is plain markdown; code lives in
` ```{python} ` blocks. The document is fully self-contained: every function the report
uses is defined in its own block (folded away by default in the rendered HTML), so there
is no separate module to keep in sync.

**3. Render.** From `python/`:

```bash
quarto render snowy-arbitrage.qmd --to html
```

This executes every cell fresh through the `snowy-arbitrage` kernel (pinned in the YAML
header), so a successful render proves the whole analysis ran; any raised assertion
aborts it. Benign stderr noise (numpy overflow warnings from cvxpy scaling) is suppressed
by `warning: false` in the YAML header. (`strip_stderr.py` belonged to the old
notebook-as-source pipeline and is no longer part of the workflow.)

**4. Refresh the Colab copy** whenever the source changed:

```bash
quarto convert snowy-arbitrage.qmd --output snowy-arbitrage.ipynb
```

**5. Verify before committing.** Open the rendered `snowy-arbitrage.html` and skim as a
reader. After any change that moves numbers, search the HTML for the old values to catch
stale copies in prose, figure annotations, alt text, and the demo (note: the rendered HTML
escapes apostrophes as `&#39;`, so search for numbers, not phrases containing quotes).
Figures in `figures/` regenerate on execution; confirm their timestamps moved.

**6. Commit** only the files that changed together: the `.qmd`, the derived notebook, the
rendered HTML, and regenerated figures. Data snapshots only change when a year is
re-downloaded on purpose.

**7. A note on where edits land.** This repository is a one-way mirror of the
maintainer's private working folder: changes land there first and are pushed here with
each render. Pull requests and direct edits here are welcome; the maintainer folds them
back into the working folder, re-renders, and pushes the result forward.

## Collaborating on the report

Three lanes, depending on the collaborator's tooling comfort. All end with the change
landing in `snowy-arbitrage.qmd`, the single source.

**Lane 1: edit the source directly.** The `.qmd` is plain text, so any editor works and
diffs are clean line-by-line. Edit prose in place (GitHub's web editor is enough; no
Python required), commit or send the file back, and the maintainer re-renders with the
one command above. Nothing else needs touching: the render regenerates the HTML, the
figures, and every number.

**Lane 2: review copy in Google Docs.** For collaborators who prefer suggestion-mode
editing: the maintainer pastes the report's prose into a Google Doc, collaborators
suggest edits there, and the maintainer folds accepted suggestions back into the `.qmd`
and re-renders. The Doc is a review surface, not a source; it goes stale the moment the
`.qmd` moves on, so retire each Doc once its round of comments is folded in.

**Lane 3: live co-editing in a working session.** For a meeting where several people edit
at once: the maintainer opens this repository in VS Code and starts a **Live Share**
session (install the free "Live Share" extension, click its Share button, send the link).
Collaborators join from their own laptops, in VS Code or in a browser, and type directly
into `snowy-arbitrage.qmd` with live cursors, Google-Docs style. Every keystroke lands in
the real file on the maintainer's machine, so there is nothing to fold back afterwards;
the maintainer re-renders during the session to show the result, and guest access ends
when the session closes.

House style for prose edits in either lane: no contractions anywhere in the report, and
avoid em dashes (prefer commas, colons, semicolons, or parentheses).

## Data provenance

Prices are the AEMO dispatch price for the NSW1 region, downloaded from AEMO's public
NEMWeb archive with [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS), filtered to
non-intervention runs, and averaged from 5-minute to 30-minute steps. The loader in the
notebook is download-once: it uses the committed snapshot when present and only touches
the network when a snapshot is missing. Raw downloads cache in
`.nemosis_cache/` (git-ignored).

## Independence

This is independent, clean-room work: open-literature methods (linear programming,
Markov price models, stochastic dynamic programming) applied to public AEMO price data
and public Snowy 2.0 specifications. It contains no University of Melbourne course
material.
