import requests

import requests

def get_abilities(pokemon_name: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    res = requests.get(url)

    if res.status_code != 200:
        return None, f"Could not find Pokémon: `{pokemon_name}`"

    data = res.json()
    abilities = {
        'standard': [],
        'hidden': []
    }

    for entry in data['abilities']:
        ability_name = entry['ability']['name']
        is_hidden = entry['is_hidden']

        # Get full ability info from /ability/{name}
        ability_url = entry['ability']['url']
        ability_res = requests.get(ability_url)
        if ability_res.status_code != 200:
            description = "No description available."
        else:
            ability_data = ability_res.json()
            # Get the English effect text
            effect_entries = ability_data['effect_entries']
            description = next(
                (e['short_effect'] for e in effect_entries if e['language']['name'] == 'en'),
                "No description available."
            )

        formatted_name = ability_name.replace('-', ' ').title()
        ability_info = {
            'name': formatted_name,
            'description': description
        }

        if is_hidden:
            abilities['hidden'].append(ability_info)
        else:
            abilities['standard'].append(ability_info)

    return abilities, None
