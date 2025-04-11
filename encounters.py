import requests

def get_encounter_locations(pokemon_name: str, version_filter=None):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/encounters"
    res = requests.get(url)

    if res.status_code != 200:
        return None, f"Could not find encounters for `{pokemon_name}`"

    data = res.json()
    if not data:
        return [], f"{pokemon_name.title()} cannot be found in the wild."

    encounters_map = {}

    for entry in data:
        location = entry['location_area']['name'].replace('-', ' ').title()

        for version_detail in entry['version_details']:
            version = version_detail['version']['name'].title()
            if version_filter and version.lower() != version_filter.lower():
                continue

            for encounter in version_detail['encounter_details']:
                method = encounter['method']['name'].replace('-', ' ').title()
                chance = encounter['chance']

                key = (location, version, method)

                if key not in encounters_map or chance > encounters_map[key]['chance']:
                    encounters_map[key] = {
                        'location': location,
                        'version': version,
                        'method': method,
                        'chance': chance
                    }

    # Return just the values, deduplicated
    return list(encounters_map.values()), None



