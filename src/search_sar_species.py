import requests

def search_sar_species(species_name):
    url = f"https://species-registry.canada.ca/index-en.html#/species?sortBy=commonNameSort&sortDirection=asc&pageSize=10&keywords={species_name}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    if data and len(data['results']) > 0:
        # We'll just use the first result
        return data['results'][0]
    else:
        return None