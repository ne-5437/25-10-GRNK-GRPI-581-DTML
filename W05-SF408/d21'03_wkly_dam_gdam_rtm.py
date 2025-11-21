import marimo

__generated_with = "0.18.0"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import plotly.graph_objects as go
    import marimo as mo
    return go, mo, pd


@app.cell
def _(pd):
    dam_raw  = pd.read_csv("DAM_2yrs.csv")
    gdam_raw = pd.read_csv("GDAM_2yrs.csv")
    rtm_raw  = pd.read_csv("RTM_2yrs.csv")
    return dam_raw, gdam_raw, rtm_raw


@app.cell
def _(dam_raw, gdam_raw, pd, rtm_raw):
    def to_naive(series):
        ts = pd.to_datetime(series, errors="coerce", utc=True)
        return ts.dt.tz_convert(None)

    def clean_df(df):
        out = df.copy()
        out["START_TIME"] = to_naive(out["START_TIME"])
        out["ACTUAL"] = pd.to_numeric(out["ACTUAL"], errors="coerce")
        out.dropna(subset=["START_TIME", "ACTUAL"], inplace=True)
        out.reset_index(drop=True, inplace=True)
        return out

    dam_clean  = clean_df(dam_raw)
    gdam_clean = clean_df(gdam_raw)
    rtm_clean  = clean_df(rtm_raw)
    return dam_clean, gdam_clean, rtm_clean


@app.cell
def _(dam_clean, gdam_clean, pd, rtm_clean):
    clip_start = pd.Timestamp("2024-10-01")
    clip_end   = pd.Timestamp("2025-09-30")

    def clip_range(df):
        return df[(df["START_TIME"] >= clip_start) & (df["START_TIME"] <= clip_end)].copy()

    dam_clip  = clip_range(dam_clean)
    gdam_clip = clip_range(gdam_clean)
    rtm_clip  = clip_range(rtm_clean)

    def weekly_agg(df, label):
        wk = (
            df.set_index("START_TIME")
              .resample("1W")
              .mean(numeric_only=True)
              .reset_index()
        )
        wk["MARKET"] = label
        return wk

    dam_weekly  = weekly_agg(dam_clip,  "DAM")
    gdam_weekly = weekly_agg(gdam_clip, "GDAM")
    rtm_weekly  = weekly_agg(rtm_clip,  "RTM")

    all_weekly = pd.concat([dam_weekly, gdam_weekly, rtm_weekly], ignore_index=True)
    return dam_weekly, gdam_weekly, rtm_weekly


@app.cell
def _(dam_weekly, gdam_weekly, go, mo, rtm_weekly):
    fig = go.Figure()

    # Add DAM
    fig.add_trace(go.Scatter(
        x=dam_weekly["START_TIME"],
        y=dam_weekly["ACTUAL"],
        mode="lines+markers",
        name="DAM"
    ))

    # Add GDAM
    fig.add_trace(go.Scatter(
        x=gdam_weekly["START_TIME"],
        y=gdam_weekly["ACTUAL"],
        mode="lines+markers",
        name="GDAM"
    ))

    # Add RTM
    fig.add_trace(go.Scatter(
        x=rtm_weekly["START_TIME"],
        y=rtm_weekly["ACTUAL"],
        mode="lines+markers",
        name="RTM"
    ))

    seasons = [
        ("Autumn",  "2024-10-01", "2024-12-31", "rgba(255,165,0,0.15)"),
        ("Winter",  "2025-01-01", "2025-02-28", "rgba(135,206,250,0.15)"),
        ("Summer",  "2025-03-01", "2025-05-31", "rgba(255,99,71,0.15)"),
        ("Monsoon","2025-06-01", "2025-09-30", "rgba(0,128,128,0.15)")
    ]

    for name, s, e, color in seasons:
        fig.add_vrect(
            x0=s, x1=e, fillcolor=color, opacity=0.25, line_width=0,
            annotation_text=name, annotation_position="top left"
        )

    fig.update_layout(
        title="DAM / GDAM / RTM — Weekly Avg ACTUAL (Autumn 2024 → Monsoon 2025)",
        xaxis_title="Week",
        yaxis_title="Weekly Avg ACTUAL",
        height=500
    )

    mo.ui.plotly(fig)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
