import requests
import re

ORCID_ID = "0009-0000-1697-1424"
BASE_URL = "https://pub.orcid.org/v3.0"

headers = {
    "Accept": "application/json"
}

works_data = requests.get(f"{BASE_URL}/{ORCID_ID}/works", headers=headers).json()

publications = []

for group in works_data.get("group", []):
    summary = group["work-summary"][0]

    put_code = summary["put-code"]

    work_detail = requests.get(
        f"{BASE_URL}/{ORCID_ID}/work/{put_code}",
        headers=headers
    ).json()

    title = work_detail.get("title", {}).get("title", {}).get("value", "No title")

    year = work_detail.get("publication-date", {}).get("year", {}).get("value", "N/A")

    journal = work_detail.get("journal-title", {}).get("value", "")

    # DOI
    doi = None
    external_ids = work_detail.get("external-ids", {}).get("external-id", [])
    for ext in external_ids:
        if ext.get("external-id-type") == "doi":
            doi = ext.get("external-id-value")

    doi_link = f"https://doi.org/{doi}" if doi else None

    # Clean citation
    citation = f"- \"{title},\" *{journal}*, {year}."

    if doi_link:
        citation += f" [Read Paper]({doi_link})"

    publications.append((year, citation))

# Sort newest first
publications.sort(reverse=True, key=lambda x: x[0] if x[0] != "N/A" else "0")

formatted_pubs = [pub[1] for pub in publications[:10]]

# Replace README section
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

updated = re.sub(
    r"<!-- PUBLICATIONS:START -->(.*?)<!-- PUBLICATIONS:END -->",
    "<!-- PUBLICATIONS:START -->\n"
    + "\n".join(formatted_pubs)
    + "\n<!-- PUBLICATIONS:END -->",
    content,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)

print("✅ Publications updated (no authors).")
