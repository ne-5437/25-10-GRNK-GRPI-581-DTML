import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from statsmodels.tsa.seasonal import seasonal_decompose
    import plotly.graph_objects as go
    import plotly.express as px

    plt.rcParams["figure.figsize"] = (10,4)

    # File paths
    DAM_FILE  = "DAM_2yrs.csv"
    GDAM_FILE = "GDAM_2yrs.csv"
    RTM_FILE  = "RTM_2yrs.csv"
    IEX_FILE  = "IEX.open_meteo_forecast.csv"
    return (
        DAM_FILE,
        GDAM_FILE,
        IEX_FILE,
        RTM_FILE,
        go,
        mo,
        np,
        pd,
        plt,
        seasonal_decompose,
    )


@app.cell
def _(DAM_FILE, GDAM_FILE, RTM_FILE, pd):
    def load_market_raw(path):
        df = pd.read_csv(path)
        df["START_TIME"] = pd.to_datetime(df["START_TIME"])
        df = df.rename(columns={"START_TIME":"timestamp", "ACTUAL":"price"})
        return df[["timestamp","price"]]

    dam_raw  = load_market_raw(DAM_FILE)
    gdam_raw = load_market_raw(GDAM_FILE)
    rtm_raw  = load_market_raw(RTM_FILE)

    dam_raw.head()
    return dam_raw, gdam_raw, rtm_raw


@app.cell
def _(IEX_FILE, pd):
    iex_raw = pd.read_csv(IEX_FILE)
    iex_raw["start_time"] = pd.to_datetime(iex_raw["start_time"])
    iex_raw = iex_raw.rename(columns={"start_time":"timestamp"})

    iex_raw.head()
    return (iex_raw,)


@app.cell
def _(iex_raw):
    solar = [
        "shortwave_radiation", "direct_radiation", "direct_normal_irradiance",
        "cloud_cover", "temperature_2m", "relative_humidity_2m"
    ]

    wind = [
        "wind_speed_80m","wind_speed_120m","wind_speed_180m",
        "wind_direction_80m","wind_direction_120m"
    ]

    hydro = ["precipitation","rain","pressure_msl","surface_pressure"]

    meteo_cols = solar + wind + hydro

    available_cols = [c for c in meteo_cols if c in iex_raw.columns]

    iex_sel = iex_raw[["timestamp"] + available_cols]

    iex_sel.head()
    return available_cols, hydro, iex_sel, solar, wind


@app.cell
def _(dam_raw, gdam_raw, iex_sel, mo, rtm_raw):
    def get_range(df):
        return df.timestamp.min(), df.timestamp.max()

    ranges = [
        get_range(dam_raw),
        get_range(gdam_raw),
        get_range(rtm_raw),
        get_range(iex_sel)
    ]

    overlap_start = max(r[0] for r in ranges)
    overlap_end   = min(r[1] for r in ranges)

    mo.md(f"### Overlap: {overlap_start} → {overlap_end}")
    return overlap_end, overlap_start


@app.cell
def _(dam_raw, gdam_raw, iex_sel, overlap_end, overlap_start, rtm_raw):
    def trim(df):
        return df[(df.timestamp >= overlap_start) & (df.timestamp <= overlap_end)].copy()

    dam_trim  = trim(dam_raw)
    gdam_trim = trim(gdam_raw)
    rtm_trim  = trim(rtm_raw)
    iex_trim  = trim(iex_sel)

    def daily(df):
        return (
            df.set_index("timestamp")
              .resample("D")
              .mean(numeric_only=True)
              .reset_index()
        )

    dam_daily  = daily(dam_trim)
    gdam_daily = daily(gdam_trim)
    rtm_daily  = daily(rtm_trim)
    iex_daily  = daily(iex_trim)

    dam_daily.head()
    return dam_daily, gdam_daily, iex_daily, rtm_daily


@app.cell
def _(dam_daily, gdam_daily, iex_daily, rtm_daily):
    merged_step1 = dam_daily.rename(columns={"price": "DAM_price"})
    merged_step2 = merged_step1.merge(
        gdam_daily.rename(columns={"price": "GDAM_price"}),
        on="timestamp",
        how="outer"
    )
    merged_step3 = merged_step2.merge(
        rtm_daily.rename(columns={"price": "RTM_price"}),
        on="timestamp",
        how="outer"
    )
    merged_all = merged_step3.merge(iex_daily, on="timestamp", how="left")
    merged_all = merged_all.sort_values("timestamp").reset_index(drop=True)

    merged_all.head()
    return (merged_all,)


@app.cell
def _(available_cols, merged_all):
    price_cols = ["DAM_price", "GDAM_price", "RTM_price"]
    weather_cols = available_cols

    corr_matrix = merged_all[price_cols + weather_cols].corr()

    corr_matrix
    return (corr_matrix,)


@app.cell
def _(corr_matrix, plt):
    # Replacement: Heatmap with unique variable name
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(12, 7))

    im_heatmap = ax_heatmap.imshow(corr_matrix, vmin=-1, vmax=1, cmap="coolwarm")

    ax_heatmap.set_xticks(range(len(corr_matrix.columns)))
    ax_heatmap.set_xticklabels(corr_matrix.columns, rotation=45, ha="right")

    ax_heatmap.set_yticks(range(len(corr_matrix.index)))
    ax_heatmap.set_yticklabels(corr_matrix.index)

    plt.colorbar(im_heatmap, ax=ax_heatmap)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(go, merged_all, mo, seasonal_decompose):

    from plotly.subplots import make_subplots

    series = merged_all.set_index("timestamp")["DAM_price"].dropna()
    res = seasonal_decompose(series, model="additive", period=7)

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.02,
                        subplot_titles=("Observed", "Trend", "Seasonal", "Residual"))

    fig.add_trace(go.Scatter(x=res.observed.index, y=res.observed.values, mode="lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x=res.trend.index,    y=res.trend.values,    mode="lines"), row=2, col=1)
    fig.add_trace(go.Scatter(x=res.seasonal.index, y=res.seasonal.values, mode="lines"), row=3, col=1)
    fig.add_trace(go.Scatter(x=res.resid.index,    y=res.resid.values,    mode="lines"), row=4, col=1)

    fig.update_layout(height=900, title="Seasonal Decompose (DAM_price)", showlegend=False)
    mo.ui.plotly(fig)
    return


@app.cell
def _(go, merged_all, mo):

    import plotly.subplots as psp

    has_shortwave = "shortwave_radiation" in merged_all.columns
    rows_local = 2 if has_shortwave else 1

    fig_prices_sw = psp.make_subplots(rows=rows_local, cols=1, shared_xaxes=True, vertical_spacing=0.06)

    fig_prices_sw.add_trace(go.Scatter(x=merged_all["timestamp"], y=merged_all["DAM_price"],  mode="lines", name="DAM_price"),  row=1, col=1)
    fig_prices_sw.add_trace(go.Scatter(x=merged_all["timestamp"], y=merged_all["GDAM_price"], mode="lines", name="GDAM_price"), row=1, col=1)
    fig_prices_sw.add_trace(go.Scatter(x=merged_all["timestamp"], y=merged_all["RTM_price"],  mode="lines", name="RTM_price"),  row=1, col=1)

    if has_shortwave:
        fig_prices_sw.add_trace(go.Scatter(x=merged_all["timestamp"], y=merged_all["shortwave_radiation"], mode="lines", name="shortwave_radiation"), row=2, col=1)

    fig_prices_sw.update_layout(height=600 if has_shortwave else 420, title="Market Prices and Shortwave Radiation")
    mo.ui.plotly(fig_prices_sw)
    return


@app.cell
def _(merged_all):
    # unique weekly aggregation (keeps original merged_all intact)
    weekly_agg_df = (
        merged_all
        .set_index("timestamp")
        .resample("W")
        .mean(numeric_only=True)
        .reset_index()
    )
    weekly_agg_df.head()
    return (weekly_agg_df,)


@app.cell
def _(go, mo, solar, weekly_agg_df):
    from plotly.subplots import make_subplots as make_subplots13

    solar_features13 = [f for f in solar if f in weekly_agg_df.columns]
    solar_rows13 = len(solar_features13) + 1

    fig13 = make_subplots13(
        rows=solar_rows13, cols=1, shared_xaxes=True, vertical_spacing=0.03
    )

    for i, ftr in enumerate(solar_features13, start=1):
        fig13.add_trace(
            go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df[ftr], mode="lines", name=ftr),
            row=i, col=1
        )

    fig13.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["DAM_price"],  mode="lines", name="DAM_price"),  row=solar_rows13, col=1)
    fig13.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["GDAM_price"], mode="lines", name="GDAM_price"), row=solar_rows13, col=1)
    fig13.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["RTM_price"],  mode="lines", name="RTM_price"),  row=solar_rows13, col=1)

    fig13.update_layout(height=300 * solar_rows13, title="Weekly Solar Features + Prices")
    mo.ui.plotly(fig13)
    return


@app.cell
def _(go, mo, weekly_agg_df, wind):

    from plotly.subplots import make_subplots as make_subplots14

    wind_features14_local = [f for f in wind if f in weekly_agg_df.columns]
    rows_wind14_local = len(wind_features14_local) + 1

    fig14 = make_subplots14(
        rows=rows_wind14_local, cols=1, shared_xaxes=True, vertical_spacing=0.03
    )

    for idx_w14, feat_w14 in enumerate(wind_features14_local, start=1):
        fig14.add_trace(
            go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df[feat_w14], mode="lines", name=feat_w14),
            row=idx_w14, col=1
        )

    final_row_w14 = rows_wind14_local
    fig14.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["DAM_price"],  mode="lines", name="DAM_price"),  row=final_row_w14, col=1)
    fig14.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["GDAM_price"], mode="lines", name="GDAM_price"), row=final_row_w14, col=1)
    fig14.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["RTM_price"],  mode="lines", name="RTM_price"),  row=final_row_w14, col=1)

    fig14.update_layout(height=300 * rows_wind14_local, title="Weekly Wind Features + Prices")
    mo.ui.plotly(fig14)
    return


@app.cell
def _(go, hydro, mo, weekly_agg_df):

    from plotly.subplots import make_subplots as make_subplots15

    hydro_features15_local = [f for f in hydro if f in weekly_agg_df.columns]
    rows_hydro15_local = len(hydro_features15_local) + 1

    fig15 = make_subplots15(rows=rows_hydro15_local, cols=1, shared_xaxes=True, vertical_spacing=0.03)

    for idx_h15, feat_h15 in enumerate(hydro_features15_local, start=1):
        fig15.add_trace(
            go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df[feat_h15], mode="lines", name=feat_h15),
            row=idx_h15, col=1
        )

    final_row_h15 = rows_hydro15_local
    fig15.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["DAM_price"],  mode="lines", name="DAM_price"),  row=final_row_h15, col=1)
    fig15.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["GDAM_price"], mode="lines", name="GDAM_price"), row=final_row_h15, col=1)
    fig15.add_trace(go.Scatter(x=weekly_agg_df["timestamp"], y=weekly_agg_df["RTM_price"],  mode="lines", name="RTM_price"),  row=final_row_h15, col=1)

    fig15.update_layout(height=300 * rows_hydro15_local, title="Weekly Hydro Features + Prices")
    mo.ui.plotly(fig15)
    return


@app.cell
def _(hydro, mo, solar, weekly_agg_df, wind):
    # Weekly correlation v2 (Marimo safe)

    solar_feats_v2 = [f for f in solar if f in weekly_agg_df.columns]
    wind_feats_v2  = [f for f in wind if f in weekly_agg_df.columns]
    hydro_feats_v2 = [f for f in hydro if f in weekly_agg_df.columns]
    price_cols_v2  = [c for c in weekly_agg_df.columns if c.endswith("_price")]

    corr_weekly_solar_v2 = weekly_agg_df[price_cols_v2 + solar_feats_v2].corr().loc[price_cols_v2, solar_feats_v2]
    corr_weekly_wind_v2  = weekly_agg_df[price_cols_v2 + wind_feats_v2].corr().loc[price_cols_v2, wind_feats_v2]
    corr_weekly_hydro_v2 = weekly_agg_df[price_cols_v2 + hydro_feats_v2].corr().loc[price_cols_v2, hydro_feats_v2]

    mo.md("### Weekly correlation (prices × solar features) — v2")
    corr_weekly_solar_v2
    return (
        corr_weekly_hydro_v2,
        corr_weekly_wind_v2,
        hydro_feats_v2,
        price_cols_v2,
        solar_feats_v2,
        wind_feats_v2,
    )


@app.cell
def _(corr_weekly_wind_v2, mo):
    mo.md("### Weekly correlation (prices × wind features) — v2")
    corr_weekly_wind_v2
    return


@app.cell
def _(corr_weekly_hydro_v2, mo):
    mo.md("### Weekly correlation (prices × hydro features) — v2")
    corr_weekly_hydro_v2
    return


@app.cell
def _(
    hydro_feats_v2,
    merged_all,
    mo,
    np,
    pd,
    price_cols_v2,
    solar_feats_v2,
    wind_feats_v2,
):
    # Monthly-level aggregation (v2)
    monthly_agg_v2 = (
        merged_all
        .set_index("timestamp")
        .resample("M")
        .mean(numeric_only=True)
        .reset_index()
    )

    monthly_agg_v2["month_num"] = monthly_agg_v2["timestamp"].dt.month


    # Seasonal index helper (v2 safe)
    def seasonal_index_v2(df_local, feature_list_local):
        result_rows_v2 = []
        for feat_local_v2 in feature_list_local:
            if feat_local_v2 not in df_local.columns:
                continue

            feat_mean_all_v2 = df_local[feat_local_v2].mean(skipna=True)
            month_means_local_v2 = df_local.groupby("month_num")[feat_local_v2].mean().reset_index()

            month_means_local_v2["feature"] = feat_local_v2
            month_means_local_v2["seasonal_index"] = (
                month_means_local_v2[feat_local_v2] / feat_mean_all_v2
                if feat_mean_all_v2 != 0 else np.nan
            )

            result_rows_v2.append(month_means_local_v2[["month_num","feature","seasonal_index"]])

        if result_rows_v2:
            return pd.concat(result_rows_v2, ignore_index=True)
        return pd.DataFrame(columns=["month_num","feature","seasonal_index"])


    # Build seasonal-index tables for each group (unique names)
    seasonal_index_solar_v2 = seasonal_index_v2(monthly_agg_v2, solar_feats_v2)
    seasonal_index_wind_v2  = seasonal_index_v2(monthly_agg_v2, wind_feats_v2)
    seasonal_index_hydro_v2 = seasonal_index_v2(monthly_agg_v2, hydro_feats_v2)
    seasonal_index_prices_v2 = seasonal_index_v2(monthly_agg_v2, price_cols_v2)

    mo.md("### Seasonal index for solar features — v2")
    seasonal_index_solar_v2
    return (
        seasonal_index_hydro_v2,
        seasonal_index_prices_v2,
        seasonal_index_solar_v2,
        seasonal_index_wind_v2,
    )


@app.cell
def _(mo, seasonal_index_wind_v2):
    mo.md("### Seasonal index for wind features — v2")
    seasonal_index_wind_v2
    return


@app.cell
def _(mo, seasonal_index_hydro_v2):
    mo.md("### Seasonal index for hydro features — v2")
    seasonal_index_hydro_v2
    return


@app.cell
def _(mo, seasonal_index_prices_v2):
    mo.md("### Seasonal index for DAM / GDAM / RTM — v2")
    seasonal_index_prices_v2
    return


@app.cell
def _(mo, seasonal_index_prices_v2, seasonal_index_solar_v2):
    def solar_seasonal_plot_v4():
        import plotly.graph_objects as go

        fig_solar_v4 = go.Figure()

        # Add all solar feature seasonal index lines
        for sol_feat_v4 in seasonal_index_solar_v2["feature"].unique():
            df_sol_feat_v4 = seasonal_index_solar_v2[seasonal_index_solar_v2["feature"] == sol_feat_v4]

            fig_solar_v4.add_trace(
                go.Scatter(
                    x=df_sol_feat_v4["month_num"],
                    y=df_sol_feat_v4["seasonal_index"],
                    mode="lines+markers",
                    name=sol_feat_v4
                )
            )

        # Add price seasonal index
        price_idx_sol_v4 = (
            seasonal_index_prices_v2.groupby("month_num")["seasonal_index"]
            .mean()
            .reset_index()
        )
        fig_solar_v4.add_trace(
            go.Scatter(
                x=price_idx_sol_v4["month_num"],
                y=price_idx_sol_v4["seasonal_index"],
                mode="lines+markers",
                name="avg_price_index",
                line=dict(width=3, color="gold")
            )
        )

        fig_solar_v4.update_layout(
            title="Solar Seasonal Index (Monthly)",
            xaxis_title="Month (1–12)",
            yaxis_title="Seasonal Index",
            height=450,
            xaxis=dict(tickmode="linear", dtick=1)
        )

        return mo.ui.plotly(fig_solar_v4)

    solar_seasonal_plot_v4()
    return


@app.cell
def _(mo, seasonal_index_prices_v2, seasonal_index_wind_v2):
    def wind_seasonal_plot_v4():
        import plotly.graph_objects as go

        fig_wind_v4 = go.Figure()

        for wnd_feat_v4 in seasonal_index_wind_v2["feature"].unique():
            df_wnd_feat_v4 = seasonal_index_wind_v2[seasonal_index_wind_v2["feature"] == wnd_feat_v4]

            fig_wind_v4.add_trace(
                go.Scatter(
                    x=df_wnd_feat_v4["month_num"],
                    y=df_wnd_feat_v4["seasonal_index"],
                    mode="lines+markers",
                    name=wnd_feat_v4
                )
            )

        price_idx_wind_v4 = (
            seasonal_index_prices_v2.groupby("month_num")["seasonal_index"]
            .mean()
            .reset_index()
        )
        fig_wind_v4.add_trace(
            go.Scatter(
                x=price_idx_wind_v4["month_num"],
                y=price_idx_wind_v4["seasonal_index"],
                mode="lines+markers",
                name="avg_price_index",
                line=dict(width=3, color="gold")
            )
        )

        fig_wind_v4.update_layout(
            title="Wind Seasonal Index (Monthly)",
            xaxis_title="Month (1–12)",
            yaxis_title="Seasonal Index",
            height=450,
            xaxis=dict(tickmode="linear", dtick=1)
        )

        return mo.ui.plotly(fig_wind_v4)

    wind_seasonal_plot_v4()
    return


@app.cell
def _(mo, seasonal_index_hydro_v2, seasonal_index_prices_v2):
    def hydro_seasonal_plot_v4():
        import plotly.graph_objects as go

        fig_hydro_v4 = go.Figure()

        for hyd_feat_v4 in seasonal_index_hydro_v2["feature"].unique():
            df_hyd_feat_v4 = seasonal_index_hydro_v2[seasonal_index_hydro_v2["feature"] == hyd_feat_v4]

            fig_hydro_v4.add_trace(
                go.Scatter(
                    x=df_hyd_feat_v4["month_num"],
                    y=df_hyd_feat_v4["seasonal_index"],
                    mode="lines+markers",
                    name=hyd_feat_v4
                )
            )

        price_idx_hyd_v4 = (
            seasonal_index_prices_v2.groupby("month_num")["seasonal_index"]
            .mean()
            .reset_index()
        )
        fig_hydro_v4.add_trace(
            go.Scatter(
                x=price_idx_hyd_v4["month_num"],
                y=price_idx_hyd_v4["seasonal_index"],
                mode="lines+markers",
                name="avg_price_index",
                line=dict(width=3, color="gold")
            )
        )

        fig_hydro_v4.update_layout(
            title="Hydro Seasonal Index (Monthly)",
            xaxis_title="Month (1–12)",
            yaxis_title="Seasonal Index",
            height=450,
            xaxis=dict(tickmode="linear", dtick=1)
        )

        return mo.ui.plotly(fig_hydro_v4)

    hydro_seasonal_plot_v4()
    return


@app.cell
def _(
    hydro_feats_v2,
    mo,
    pd,
    price_cols_v2,
    solar_feats_v2,
    weekly_agg_df,
    wind_feats_v2,
):
    # Cell 14 — Weekly lag-correlation scan (v2)
    max_lag_weeks_cell14 = 6
    lag_scan_results_cell14 = []

    feature_groups_cell14 = {
        "solar": solar_feats_v2,
        "wind": wind_feats_v2,
        "hydro": hydro_feats_v2
    }

    for group_name_cell14, feat_list_cell14 in feature_groups_cell14.items():
        for feature_cell14 in feat_list_cell14:
            if feature_cell14 not in weekly_agg_df.columns:
                continue
            for price_col_cell14 in price_cols_v2:
                best_corr_cell14 = None
                best_lag_cell14 = None

                for lag_w_cell14 in range(0, max_lag_weeks_cell14 + 1):
                    shifted_feat_cell14 = weekly_agg_df[feature_cell14].shift(lag_w_cell14)
                    corr_val_cell14 = shifted_feat_cell14.corr(weekly_agg_df[price_col_cell14])

                    if pd.isna(corr_val_cell14):
                        continue
                    if (best_corr_cell14 is None) or (abs(corr_val_cell14) > abs(best_corr_cell14)):
                        best_corr_cell14 = corr_val_cell14
                        best_lag_cell14 = lag_w_cell14

                lag_scan_results_cell14.append({
                    "group": group_name_cell14,
                    "feature": feature_cell14,
                    "price_col": price_col_cell14,
                    "best_lag_weeks": best_lag_cell14,
                    "best_corr": best_corr_cell14
                })

    lag_scan_df_cell14 = pd.DataFrame(lag_scan_results_cell14)
    lag_scan_df_cell14["abs_corr"] = lag_scan_df_cell14["best_corr"].abs()

    # Sort strongest first
    lag_scan_sorted_cell14 = lag_scan_df_cell14.sort_values(
        "abs_corr", ascending=False
    ).reset_index(drop=True)

    mo.md("### Top Lag-Correlation Results (Cell 14)")
    lag_scan_sorted_cell14.head(20)
    return (lag_scan_sorted_cell14,)


@app.cell
def _(
    lag_scan_sorted_cell14,
    mo,
    np,
    pd,
    seasonal_index_hydro_v2,
    seasonal_index_solar_v2,
    seasonal_index_wind_v2,
):
    # Cell 15 — Summary table (v2 safe)
    summary_rows_cell15 = []

    def peak_month_cell15(season_df_cell15, feat_cell15):
        tmp_cell15 = season_df_cell15[season_df_cell15["feature"] == feat_cell15]
        if tmp_cell15.empty:
            return np.nan
        row_peak_cell15 = tmp_cell15.loc[tmp_cell15["seasonal_index"].idxmax()]
        return int(row_peak_cell15["month_num"])

    for feat_cell15 in lag_scan_sorted_cell14["feature"].unique().tolist():
        sub_cell15 = lag_scan_sorted_cell14[lag_scan_sorted_cell14["feature"] == feat_cell15]
        if sub_cell15.empty:
            continue

        top_row_cell15 = sub_cell15.iloc[0]
        corr_sign_cell15 = "positive" if top_row_cell15["best_corr"] >= 0 else "negative"

        # find seasonal peak
        if feat_cell15 in seasonal_index_solar_v2["feature"].values:
            peak_cell15 = peak_month_cell15(seasonal_index_solar_v2, feat_cell15)
        elif feat_cell15 in seasonal_index_wind_v2["feature"].values:
            peak_cell15 = peak_month_cell15(seasonal_index_wind_v2, feat_cell15)
        elif feat_cell15 in seasonal_index_hydro_v2["feature"].values:
            peak_cell15 = peak_month_cell15(seasonal_index_hydro_v2, feat_cell15)
        else:
            peak_cell15 = np.nan

        summary_rows_cell15.append({
            "feature": feat_cell15,
            "top_price_col": top_row_cell15["price_col"],
            "best_lag_weeks": top_row_cell15["best_lag_weeks"],
            "best_corr": top_row_cell15["best_corr"],
            "corr_sign": corr_sign_cell15,
            "seasonal_peak_month": peak_cell15
        })

    summary_df_cell15 = pd.DataFrame(summary_rows_cell15).sort_values(
        "best_corr", key=lambda s: s.abs(), ascending=False
    ).reset_index(drop=True)

    mo.md("### Summary Table (Cell 15)")
    summary_df_cell15
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
