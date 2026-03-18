import requests

ORCID_ID = "0009-0000-1697-1424"
URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"

headers = {
    "Accept": "application/json"
}

response = requests.get(URL, headers=headers)
data = response.json()

works = data.get("group", [])

publications = []

for work in works:
    summary = work["work-summary"][0]
    title = summary["title"]["title"]["value"]
    year = summary.get("publication-date", {}).get("year", {}).get("value", "N/A")

    publications.append(f"- {title} ({year})")

# Write to README or a separate file
with open("PUBLICATIONS.md", "w") as f:
    f.write("# Publications\n\n")
    f.write("\n".join(publications))
