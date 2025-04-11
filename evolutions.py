import requests

def get_evolution_chain(pokemon_name: str):
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}"
    species_res = requests.get(species_url)

    if species_res.status_code != 200:
        return None, f"Could not find Pokémon: `{pokemon_name}`"

    species_data = species_res.json()
    evolution_chain_url = species_data['evolution_chain']['url']

    evolution_res = requests.get(evolution_chain_url)
    if evolution_res.status_code != 200:
        return None, "Failed to fetch evolution chain."

    chain = evolution_res.json()['chain']
    evolution_paths = []

    def parse_trigger(trigger):
        if trigger['trigger']['name'] == "level-up":
            if trigger.get('min_happiness') is not None:
                if trigger.get('time_of_day') == 'day':
                    return "High Friendship (Day)"
                elif trigger.get('time_of_day') == 'night':
                    return "High Friendship (Night)"
                return "High Friendship"
            if trigger.get('known_move_type'):
                return f"Knowing {trigger['known_move_type']['name'].title()}-type move"
            if trigger.get('location'):
                return f"Level near {trigger['location']['name'].replace('-', ' ').title()}"
            if trigger.get('min_level'):
                return f"Level {trigger['min_level']}"
            return "Level up"
        elif trigger['trigger']['name'] == "use-item":
            item = trigger.get('item', {}).get('name', 'an item').replace('-', ' ').title()
            return f"Use {item}"
        elif trigger['trigger']['name'] == "trade":
            return "Trade"
        else:
            return trigger['trigger']['name'].replace('-', ' ').title()

    def walk_chain(node, path):
        current_name = node['species']['name'].title()
        new_path = path + [current_name]

        if not node['evolves_to']:
            evolution_paths.append(new_path)
            return

        for evo in node['evolves_to']:
            trigger = evo['evolution_details'][0] if evo['evolution_details'] else {}
            method = parse_trigger(trigger)
            walk_chain(evo, new_path + [f"({method})"])

    walk_chain(chain, [])

    return evolution_paths, None
