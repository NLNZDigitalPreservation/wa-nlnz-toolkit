# 🧰 NLNZ Web Archive Analysis Toolkit

This toolkit provides utilities for querying and extracting data from the National Library of New Zealand's Web Archive collections. It is designed to support researchers, curators, and developers working with large-scale web archive datasets, particularly in WARC format.

## 🔍 Features

- Query web archive metadata and content
- Extract and filter WARC records
- Support for common formats (WARC, CDX, JSON)
- CLI and Python API access
- Modular design for integration with other tools

## 🚀 Installation

```bash
# Install dev mode with extras
pip install -e .[dev]
```

```bash
pip install -i https://test.pypi.org/simple/ wa-nlnz-toolkit
```

## 📦 Jupyter Notebooks

The Jupyter notebooks for iPRES-2025 workshop can be found in ``notebook/iPRES2025` folder. To run the Jupyter notebooks on Google Colab, simply follow the following two steps,

1. Get the GitHub URL of the notebook (the raw .ipynb file).

```
Example: https://github.com/NLNZDigitalPreservation/wa-nlnz-toolkit/blob/main/notebook/iPRES2025/exp-01_WebArchive_Access_Fundamentals.ipynb
```

2. Modify the URL for Colab - Replace github.com with colab.research.google.com/github

```
Example:

GitHub URL:https://github.com/NLNZDigitalPreservation/wa-nlnz-toolkit/blob/main/notebook/iPRES2025/exp-01_WebArchive_Access_Fundamentals.ipynb

Colab URL: https://colab.research.google.com/github/NLNZDigitalPreservation/wa-nlnz-toolkit/blob/main/notebook/iPRES2025/exp-01_WebArchive_Access_Fundamentals.ipynb
```

## 📁 Data Sources

This toolkit interfaces with NLNZ's web archive infrastructure and supports local WARC file analysis. Access to NLNZ datasets may require appropriate permissions.

## 🛠 Requirements

- Python 3.8+
- warcio, requests, pandas, and other dependencies (see requirements.txt)

## 📄 License

This project is licensed under the MIT License.

