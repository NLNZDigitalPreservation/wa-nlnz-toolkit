# comparison_view.py
import os
import re
from html import escape


def get_content_by_url(df, target_url, fallback):
    matches = df.loc[df["url"].eq(target_url), "content"]
    return matches.iat[0] if not matches.empty else fallback


def normalize(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^[>\-\#\s]+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_phrases(b: str, min_len: int = 25) -> list[str]:
    lines = b.splitlines()
    phrases = []

    for line in lines:
        line = line.strip()
        if not line or "---" in line:
            continue

        line = normalize(line)
        if len(line) < min_len:
            continue

        phrases.append(line)

    return sorted(set(phrases), key=len, reverse=True)


def highlight_phrases(a: str, b: str) -> str:
    phrases = extract_phrases(b)

    a_html = a.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    highlighted = a_html

    for phrase in phrases:
        pattern = re.escape(phrase).replace(r"\ ", r"\s+")
        highlighted = re.sub(
            pattern,
            lambda m: f"<mark>{m.group(0)}</mark>",
            highlighted,
            flags=re.IGNORECASE,
        )

    return highlighted


def build_content_comparison_html(
    url: str,
    dfs: dict,
    res_folder: str = "./sample_data",
    output_filename: str = "content_comparison.html",
    show: bool = True,
) -> tuple[str, str]:
    """
    dfs expected keys:
      - 'markitdown' (baseline)
      - 'default'
      - 'trafilatura'
      - 'justext'
    """
    required = ["markitdown", "default", "trafilatura", "justext"]
    missing = [k for k in required if k not in dfs]
    if missing:
        raise KeyError(f"Missing keys in dfs: {missing}")

    content_markitdown = get_content_by_url(
        dfs["markitdown"], url, "No content extracted with markitdown method."
    )
    content_default = get_content_by_url(
        dfs["default"], url, "No content extracted with default method."
    )
    content_trafilatura = get_content_by_url(
        dfs["trafilatura"], url, "No content extracted with trafilatura method."
    )
    content_justext = get_content_by_url(
        dfs["justext"], url, "No content extracted with justext method."
    )

    html_output = f"""
<style>
.dim {{
    color: #999;
}}
</style>
<div style="margin-bottom: 12px;">
    <h2 style="margin: 0 0 12px 0;">HTML Page: {escape(url)}</h2>
</div>

<div style="display: flex; gap: 20px; overflow-x: auto;">

    <div style="flex: 1; min-width: 300px;">
        <h3>Default</h3>
        <pre style="white-space: pre-wrap; word-wrap: break-word;">{highlight_phrases(content_markitdown, content_default)}</pre>
    </div>
    <div style="flex: 1; min-width: 300px;">
        <h3>Trafilatura</h3>
        <pre style="white-space: pre-wrap; word-wrap: break-word;">{highlight_phrases(content_markitdown, content_trafilatura)}</pre>
    </div>
    <div style="flex: 1; min-width: 300px;">
        <h3>Justext</h3>
        <pre style="white-space: pre-wrap; word-wrap: break-word;">{highlight_phrases(content_markitdown, content_justext)}</pre>
    </div>

</div>
"""

    if show:
        from IPython.display import display, HTML

        display(HTML(html_output))

    os.makedirs(res_folder, exist_ok=True)
    output_path = os.path.join(res_folder, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    return html_output, output_path
