import requests
import re

ORCID_ID = "0009-0000-1697-1424"
URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

headers = {
    "Accept": "application/json"
}

response = requests.get(URL, headers=headers)
data = response.json()

works = data.get("group", [])

publications = []

def format_authors(summary):
    # ORCID public API usually doesn't give full author list reliably
    # So we fallback to "Author(s) unavailable" unless expanded later
    return "Author(s)"

for work in works:
    summary = work["work-summary"][0]

    title = summary["title"]["title"]["value"]

    year = summary.get("publication-date", {}).get("year", {}).get("value", "N/A")

    journal = summary.get("journal-title", {}).get("value", "")

    # Extract DOI if available
    doi = None
    external_ids = summary.get("external-ids", {}).get("external-id", [])
    for ext in external_ids:
        if ext.get("external-id-type") == "doi":
            doi = ext.get("external-id-value")

    doi_link = f"https://doi.org/{doi}" if doi else None

    # IEEE-style-ish formatting
    citation = f"- {format_authors(summary)}, \"{title},\" *{journal}*, {year}."
    
    if doi_link:
        citation += f" [DOI]({doi_link})"

    publications.append((year, citation))

# Sort newest first
publications.sort(reverse=True, key=lambda x: x[0] if x[0] != "N/A" else "0")

# Extract formatted lines
formatted_pubs = [pub[1] for pub in publications[:10]]  # limit to 10

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Replace between markers
updated_content = re.sub(
    r"<!-- PUBLICATIONS:START -->(.*?)<!-- PUBLICATIONS:END -->",
    "<!-- PUBLICATIONS:START -->\n"
    + "\n".join(formatted_pubs) +
    "\n<!-- PUBLICATIONS:END -->",
    content,
    flags=re.DOTALL
)

# Write back
with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_content)

print("✅ Publications updated successfully.")
