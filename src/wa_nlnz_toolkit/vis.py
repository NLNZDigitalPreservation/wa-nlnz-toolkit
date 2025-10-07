import pandas as pd
import matplotlib.pyplot as plt
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
    monthly_counts = df_records.resample('ME').size()

    # Plot
    fig, ax = plt.subplots(figsize=(12, 3))
    monthly_counts.plot(kind='bar', width=1.0, color='skyblue', ax=ax)

    # Format x-axis to only show years
    ax.set_xticks([i for i, d in enumerate(monthly_counts.index) if d.month == 1])
    ax.set_xticklabels([d.year for d in monthly_counts.index if d.month == 1], rotation=0)

    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.show()


def create_world_cloud(list_sentences: list, output_filename: str):
    # Combine all sentences into one text
    text = " ".join(list_sentences)

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Plot and save
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_filename)
    # plt.close()
