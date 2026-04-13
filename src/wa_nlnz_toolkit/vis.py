import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
from wordcloud import WordCloud


def plot_monthly_captures(df_records: pd.DataFrame):
    """
    Plot captures per month.

    Parameters
    ----------
    df_records : pd.DataFrame
        Pandas Dataframe containing the records to be plotted.

    Returns
    -------
    None

    Notes
    -----
    The plot is a bar chart of captures per month, with the x-axis only showing years.
    """

    # Count captures per month
    monthly_counts = df_records.resample("ME").size()

    # Plot
    plt.figure(figsize=(12, 3))

    # 1. Plot using the index values (converts them to a simple range of 0 to N)
    ax = monthly_counts.reset_index(drop=True).plot(
        kind="bar", width=1.0, color="skyblue"
    )

    # 2. Define which indices you want to show (every 12th month)
    indices = range(0, len(monthly_counts), 12)

    # 3. Create the labels based on your actual DatetimeIndex
    # This pulls the string 'YYYY-MM' from your original index
    labels = [monthly_counts.index[i].strftime("%Y-%m") for i in indices]

    # 4. Force the ticks and labels
    ax.xaxis.set_major_locator(FixedLocator(indices))
    ax.xaxis.set_major_formatter(FixedFormatter(labels))
    ax.set_ylabel("Count")

    plt.xticks(rotation=0)
    plt.show()


def create_world_cloud(list_sentences: list, output_filename: str):
    # Combine all sentences into one text
    text = " ".join(list_sentences)

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )

    # Plot and save
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_filename)
    # plt.close()
