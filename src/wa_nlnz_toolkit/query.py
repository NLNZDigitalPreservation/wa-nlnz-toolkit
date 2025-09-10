import requests
import json
import datetime
import pandas as pd


# NLNZ selective web archive
MEMENTO_URL = "https://ndhadeliver.natlib.govt.nz/webarchive"
CDX_API_URL = f"{MEMENTO_URL}/cdx"

header = {"User-Agent": "NLNZWebArchiveAccessBot/1.0 (wa-nlnz-toolkit)"}


def query_cdx_index(url: str, timeout: int = 60, **params) -> requests.Response:
    """
    Query the National Library of New Zealand's Web Archive CDX index for captures of a given URL.

    >> This is actually using pywb to redirect to the outbackCDX server, which can only be accessed internally.
    >> As a result, some params are not supported, such as cdx output format.

    Parameters:
        url (str): The target URL to search for in the CDX index.
        timeout (int): Timeout for the HTTP request in seconds. Default is 60.
        **params: Additional query parameters supported by the CDX API (e.g., matchType, limit, filter).

    Returns:
        pd.Dataframe: A Pandas Dataframe for the retrieved records.

    Raises:
        requests.HTTPError: If the request fails due to an HTTP error.
    """
    query_params = {"url": url, "output": "json", **params}

    response = requests.get(CDX_API_URL, params=query_params, timeout=timeout, headers=header)
    response.raise_for_status()

    records = [json.loads(line) for line in response.text.strip().splitlines()]
    df_records = pd.DataFrame(records)
    df_records["timestamp"] = pd.to_datetime(df_records["timestamp"])
    df_records.set_index("timestamp", inplace=True)
    # sort by index
    df_records.sort_index(inplace=True)

    # Replace the URL format
    df_records["access_url"] = df_records["load_url"].str.replace(
        r"https://wlgprdowapp01\.natlib\.govt\.nz/nlnzwebarchive_PROD/ap/(\d+)id_/((https?://.+))",
        r"https://ndhadeliver.natlib.govt.nz/webarchive/\1/\2",
        regex=True,
    )
    # remove "load_url" column
    df_records.drop("load_url", axis=1, inplace=True)

    return df_records


def query_memento(
    url: str,
    dt: datetime.datetime = None,
    allow_redirects: bool = True,
) -> requests.Response:
    """
    Query the National Library of New Zealand's Web Archive Memento API for captures of a given URL.

    Parameters:
        url (str): The target URL to search for in the Memento API.
        timeout (int): Timeout for the HTTP request in seconds. Default is 60.

    Returns:
        pd.Dataframe: A Pandas Dataframe for the retrieved records.

    Raises:
        requests.HTTPError: If the request fails due to an HTTP error.
    """
    if not url.endswith("/"):
        url += "/"
    query_url = MEMENTO_URL + "/" + url

    if dt != None:
        header["Accept-Datetime"] = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    response = requests.get(
        query_url, headers=header, allow_redirects=allow_redirects, verify=False
    )
    response.raise_for_status()

    return response


def get_memento_urls(url: str, dt: datetime.datetime = None):
    """
    Retrieve a dictionary of URLs for a given URL from the National Library of New Zealand's Web Archive.

    Parameters:
        url (str): The target URL to retrieve the URLs for.

    Returns:
        dict: A dictionary of URLs with the following keys:
            - original: The original URL.
            - memento: The URL of the archived snapshot.
            - first_memento: The URL of the first archived snapshot.
            - last_memento: The URL of the last archived snapshot.
            - timegate: The URL of the TimeGate.
            - timemap: The URL of the TimeMap.

    Notes:
        The returned dictionary may not contain all keys, depending on the availability of the URLs.

    Raises:
        requests.HTTPError: If the request fails due to an HTTP error.
    """
    response = query_memento(url, dt)
    
    dict_urls = {}
    for key in response.links.keys():
        dict_urls[key] = response.links[key]["url"]

    return dict_urls


def get_timemap(url: str, format: str="json"):
    """
    Retrieve the timemap of a given URL from the National Library of New Zealand's Web Archive.

    Parameters:
        url (str): The target URL to retrieve the timemap for.

    Returns:
        pd.Dataframe: A Pandas Dataframe for the timemap records.

    Notes:
        The timemap is a JSON object that contains a list of Memento objects.
        Each Memento object contains the following properties:

            - uri: The URI of the memento.
            - datetime: The datetime of the memento in ISO 8601 format.
            - rel: The relationship of the memento to the original resource.

    Raises:
        requests.HTTPError: If the request fails due to an HTTP error.
    """
    query_url = MEMENTO_URL + "/" + f"timemap/{format}/{url}"
    print(query_url)

    response = requests.get(query_url, allow_redirects=True, headers=header, verify=False)
    response.raise_for_status()

    if response.headers["content-type"] == "text/x-ndjson":
        data = [json.loads(line) for line in response.text.splitlines()]
    else:
        data = response.text

    df_records = pd.DataFrame(data)
    df_records["timestamp"] = pd.to_datetime(df_records["timestamp"])
    df_records.set_index("timestamp", inplace=True)
    # sort by index
    df_records.sort_index(inplace=True)

    # Replace the URL format
    df_records["access_url"] = df_records["load_url"].str.replace(
        r"https://wlgprdowapp01\.natlib\.govt\.nz/nlnzwebarchive_PROD/ap/(\d+)id_/((https?://.+))",
        r"https://ndhadeliver.natlib.govt.nz/webarchive/\1/\2",
        regex=True,
    )
    # remove "load_url" column
    df_records.drop("load_url", axis=1, inplace=True)


    return df_records
