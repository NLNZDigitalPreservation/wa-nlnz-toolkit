header = {"User-Agent": "NLNZWebArchiveAccessBot/1.0 (wa-nlnz-toolkit)"}

INTERNAL_URL_PATTERN = r"https://wlgprdowapp01\.natlib\.govt\.nz/nlnzwebarchive_PROD/ap/(\d+)id_/((https?://.+))"
EXTERNAL_URL_REPLACEMENT = r"https://ndhadeliver.natlib.govt.nz/webarchive/\1/\2"
