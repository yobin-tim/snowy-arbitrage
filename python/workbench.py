# %% [markdown]
# # Snowy 2.0 workbench
#
# A scratchpad for quick questions about the price data and the backtest's results,
# WITHOUT re-running the model. Open this file in VS Code and run cells with
# shift-enter (each `# %%` line starts a cell), or run the whole thing as a plain
# script: `python workbench.py`.
#
# It reads two things, both committed to the repository:
#   - `data/`     the four price snapshots (the model's inputs)
#   - `results/`  the model's outputs, written fresh by every render of the report
#
# Add your own questions at the bottom. `export(df, "name")` drops any table you
# build into `exports/` as a CSV (and optionally .xlsx) ready for Excel.

# %% Load everything the store holds (fast: no solving, just file reads)
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA, RESULTS, EXPORTS = HERE / "data", HERE / "results", HERE / "exports"

# The four years of half-hourly NSW spot prices, stacked into one tidy frame.
prices = pd.concat(
    [pd.read_parquet(p).assign(year=int(p.stem.split("_")[2])) for p in sorted(DATA.glob("nsw1_prices_*_30min.parquet"))]
).reset_index()

# The model outputs: every scheme's half-hourly dispatch, the annual summary,
# and the frozen parameters. See the report's appendix (Results store) for how
# these are produced and checked.
dispatch   = pd.read_parquet(RESULTS / "dispatch.parquet")
summary    = pd.read_csv(RESULTS / "summary.csv")
parameters = pd.read_csv(RESULTS / "parameters.csv")

print(f"{len(prices):,} price rows | {len(dispatch):,} dispatch rows | "
      f"schemes: {', '.join(dispatch['scheme'].unique())}")


# %% Helper: send any table to Excel
def export(df: pd.DataFrame, name: str, xlsx: bool = False) -> Path:
    """Write a dataframe to exports/<name>.csv (and .xlsx if asked) and return the path.
    CSV opens directly in Excel; use xlsx=True when you want types/dates preserved."""
    EXPORTS.mkdir(exist_ok=True)
    out = EXPORTS / f"{name}.csv"
    df.to_csv(out, index=isinstance(df.index, pd.MultiIndex) or df.index.name is not None)
    if xlsx:
        df.to_excel(EXPORTS / f"{name}.xlsx")
    print(f"wrote {out}")
    return out


# %% Example 1 — what does the average day look like, year by year?
# Mean price for each half hour of the day: the daily cycle the whole trade lives on.
avg_day = (prices.assign(time=prices["interval_start"].dt.time)
           .pivot_table(index="time", columns="year", values="price", aggfunc="mean")
           .round(1))
print(avg_day.loc[[pd.Timestamp(f"2024-01-01 {h:02d}:00").time() for h in (4, 12, 18, 21)]])

# %% Example 2 — the evening peak (5 pm to 9 pm): mean price by year
evening = prices[prices["interval_start"].dt.hour.between(17, 20)]
print(evening.groupby("year")["price"].mean().round(1))

# %% Example 3 — how negative does midday get, and how often?
midday = prices[prices["interval_start"].dt.hour.between(10, 14)]
neg_share = midday.groupby("year")["price"].apply(lambda s: (s < 0).mean())
print((neg_share * 100).round(1).astype(str) + "% of 10am-3pm half-hours below $0")

# %% Example 4 — the headline table, straight from the store
print(summary.pivot(index="year", columns="scheme", values="profit_bn").round(2))

# %% Example 5 — the forecaster's 2025 profit, month by month (for the Excel model)
s3_2025 = dispatch.query("scheme == 'S3 forecaster' and year == 2025").copy()
s3_monthly = (s3_2025.assign(month=s3_2025["interval_start"].dt.strftime("%Y-%m"))
              .groupby("month", as_index=False)["profit_dollars"].sum()
              .assign(profit_m=lambda d: (d["profit_dollars"] / 1e6).round(1)))
print(s3_monthly[["month", "profit_m"]].to_string(index=False))
# export(s3_monthly, "s3-2025-monthly")          # uncomment to send it to Excel

# %% Example 6 — what were the forecaster's ten best days in 2025?
best_days = (s3_2025.assign(date=s3_2025["interval_start"].dt.date)
             .groupby("date")["profit_dollars"].sum().div(1e6).round(2)
             .nlargest(10).rename("profit_m"))
print(best_days)

# %% Your questions — add cells below and run them
# The frames you have: prices, dispatch, summary, parameters.
# Send anything to Excel with: export(your_table, "some-name")
