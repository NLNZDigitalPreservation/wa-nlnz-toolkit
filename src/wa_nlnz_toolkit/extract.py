import boto3
from botocore import UNSIGNED
from warcio.archiveiterator import ArchiveIterator
from urllib.parse import urlparse
from bs4 import BeautifulSoup



def extract_payload(path: str, offset: int) -> bytes | None:
    """
    Extracts the payload from a WARC (Web ARChive) file starting at a given byte offset.
    Supports both local files and files stored on S3.

    Parameters
    ----------
    path : str
        Path to the WARC file. Can be a local path or an S3 URI (s3://bucket/key).
    offset : int
        Byte offset in the file where the desired record is expected to begin.

    Returns
    -------
    bytes or None
        The payload content of the first 'response' record found at the given offset,
        or None if no such record is found.
    """

    if path.startswith("s3://"):
        parsed = urlparse(path)
        bucket, key = parsed.netloc, parsed.path.lstrip("/")
        s3 = boto3.client("s3", config=boto3.session.Config(signature_version=UNSIGNED))

        # Use Range request to start at offset, but don't set an upper bound
        obj = s3.get_object(Bucket=bucket, Key=key, Range=f"bytes={offset}-")
        stream = obj["Body"]  # StreamingBody, behaves like a file
    else:
        stream = open(path, "rb")
        stream.seek(offset)

    try:
        for record in ArchiveIterator(stream):
            if record.rec_type == "response":
                return record.content_stream().read()
            break
    finally:
        # Only close if it's a local file
        if not path.startswith("s3://"):
            stream.close()

    return None
    

def extract_content_html(html_payload):
    # Parse HTML
    soup = BeautifulSoup(html_payload, "html.parser")

    # Focus on the main content section
    main_section = soup.find("main")
    if not main_section:
        main_section = soup.find("main-container")
        if not main_section:
            main_section = soup

    # Remove header sections if any
    # for header in main_section.find_all(class_="header"):
    #     header.decompose()

    # Find all <section> elements within main
    sections = main_section.find_all("section", recursive=True)
    content_list = []

    # If there are no explicit <section>s, just treat main as one section
    if not sections:
        sections = [main_section]

    # Extract text section by section
    for i, section in enumerate(sections):
        section_paragraphs = []

        # Extract <p> and <li> text
        for el in section.find_all(["p", "li"]):
            text = el.get_text(" ", strip=True)
            if text:
                section_paragraphs.append(text)

        if section_paragraphs:
            # Optionally, add a section header or separator
            if i > 0:
                content_list.append("--- Section Separator ---")
            content_list.extend(section_paragraphs)

    return content_list
