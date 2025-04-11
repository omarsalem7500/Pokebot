import requests
from collections import defaultdict

def get_type_effectiveness(pokemon_name: str):
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if res.status_code != 200:
        return None, f"Could not find Pokémon: `{pokemon_name}`"

    data = res.json()
    types = [t['type']['name'] for t in data['types']]

    # Each type has damage relations we need to combine
    multipliers = defaultdict(lambda: 1.0)

    for type_name in types:
        type_res = requests.get(f"https://pokeapi.co/api/v2/type/{type_name}")
        if type_res.status_code != 200:
            continue
        type_data = type_res.json()
        relations = type_data['damage_relations']

        for t in relations['double_damage_from']:
            multipliers[t['name']] *= 2.0
        for t in relations['half_damage_from']:
            multipliers[t['name']] *= 0.5
        for t in relations['no_damage_from']:
            multipliers[t['name']] *= 0.0

    # Classify into categories
    weaknesses = []
    resistances = []
    immunities = []

    for t, multiplier in multipliers.items():
        if multiplier == 0:
            immunities.append(t.title())
        elif multiplier >= 4:
            weaknesses.append(f"{t.title()} (4x)")
        elif multiplier > 1:
            weaknesses.append(f"{t.title()}")
        elif multiplier < 1:
            resistances.append(t.title())

    type_display = " / ".join([t.title() for t in types])

    return {
        'types': type_display,
        'weaknesses': weaknesses,
        'resistances': resistances,
        'immunities': immunities
    }, None
