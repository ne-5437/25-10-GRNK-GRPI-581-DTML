import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from pymongo import MongoClient

    # connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["raw_combined_psp"]
    collection = db["psp_dataflow"]

    # get all channel IDs for dropdown
    channels = sorted(collection.distinct("id"))

    # UI controls
    channel_selector = mo.ui.dropdown(
        options=channels,
        label="Select PSP Channel",
        value=channels[0]
    )

    limit_selector = mo.ui.number(label="Number of records to fetch", value=50000)

    # Display both side-by-side
    mo.hstack([channel_selector, limit_selector])

    return channel_selector, collection, limit_selector


@app.cell
def _(channel_selector, collection, limit_selector):
    import pandas as pd

    # access UI values safely in another cell
    selected_channel = channel_selector.value
    record_limit = int(limit_selector.value)

    # query MongoDB
    query = {"id": selected_channel}
    data = list(collection.find(query, {"_id": 0}).limit(record_limit))
    df = pd.DataFrame(data)

    print(f"✅ Loaded {len(df)} records for channel: {selected_channel}")
    df.head()

    return df, pd, selected_channel


@app.cell
def _(df, pd, selected_channel):
    import matplotlib.pyplot as plt
    import seaborn as sns

    # convert dt (milliseconds) to datetime
    df["datetime"] = pd.to_datetime(df["dt"], unit="ms")

    # sort by time to ensure proper line plot
    df_copy = df.sort_values("datetime")

    # basic trend plot
    plt.figure(figsize=(12, 5))
    sns.lineplot(x="datetime", y="v", data=df)
    plt.title(f"PSP Value Trend — {selected_channel}")
    plt.xlabel("Timestamp")
    plt.ylabel("Value (v)")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
