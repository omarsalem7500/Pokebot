import requests

def get_moveset(pokemon_name: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    res = requests.get(url)

    if res.status_code != 200:
        return None, f"Could not find Pokémon: `{pokemon_name}`"

    data = res.json()
    moves = []

    for move_entry in data['moves']:
        move_name = move_entry['move']['name'].replace("-", " ").title()
        
        # Only include moves learned by level-up
        for version_detail in move_entry['version_group_details']:
            if version_detail['move_learn_method']['name'] == 'level-up':
                level = version_detail['level_learned_at']

                # Now fetch full move info (type, power, etc.)
                move_url = move_entry['move']['url']
                move_res = requests.get(move_url)

                if move_res.status_code != 200:
                    continue  # Skip if we can't get move details

                move_data = move_res.json()

                move_info = {
                    'name': move_name,
                    'level': level,
                    'type': move_data['type']['name'].title(),
                    'class': move_data['damage_class']['name'].title(),
                    'power': move_data['power'] if move_data['power'] is not None else "—",
                    'accuracy': move_data['accuracy'] if move_data['accuracy'] is not None else "—"
                }

                moves.append(move_info)
                break  # Only keep one version's data

    # Sort moves by level
    moves.sort(key=lambda m: m['level'])

    return moves, None