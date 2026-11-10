
import re
from html.parser import HTMLParser
from urllib.request import Request, urlopen


HMRC_URL = (
    "https://www.gov.uk/government/publications/"
    "rates-and-allowances-beneficial-loan-arrangements-hmrc-official-rates/"
    "beneficial-loan-arrangements-hmrc-official-rates"
)


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            value = " ".join("".join(self.cell).split())
            self.row.append(value)
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row:
                self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.tables.append(self.table)
            self.table = None


request = Request(
    HMRC_URL,
    headers={"User-Agent": "HMRC-ORI-Monitor/1.0"}
)

with urlopen(request, timeout=30) as response:
    html = response.read().decode("utf-8")
    print("HTTP status:", response.status)

parser = TableParser()
parser.feed(html)

print("Number of tables found:", len(parser.tables))

for number, table in enumerate(parser.tables, start=1):
    print(f"\nTABLE {number}")

    for row in table[:5]:
        print(" | ".join(row))

# Extract the latest Average Official Rate
average_table = parser.tables[0]
average_row = average_table[1]

average_period = average_row[0]
average_rate = float(average_row[1])

# Extract the latest Actual Official Rate
actual_table = parser.tables[1]
actual_row = actual_table[1]

actual_effective_date = actual_row[0]
actual_rate = float(actual_row[-1])

print("\n--- HMRC ORI MONITOR ---")
print(f"Average Rate: {average_rate:.2f}%")
print(f"Average Period: {average_period}")
print(f"Actual Rate: {actual_rate:.2f}%")
print(f"Actual Effective Date: {actual_effective_date}")
