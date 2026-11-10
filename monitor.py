
from urllib.request import Request, urlopen

HMRC_URL = (
    "https://www.gov.uk/government/publications/"
    "rates-and-allowances-beneficial-loan-arrangements-hmrc-official-rates/"
    "beneficial-loan-arrangements-hmrc-official-rates"
)

request = Request(
    HMRC_URL,
    headers={"User-Agent": "HMRC-ORI-Monitor/1.0"}
)

with urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8")
    print("HTTP status:", response.status)
    print("Page size:", len(html), "characters")

print("HMRC webpage retrieved successfully.")
