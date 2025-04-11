# Pokébot 🎮

A feature-rich Discord bot powered by the [PokéAPI](https://pokeapi.co) that brings real-time Pokémon data directly into your server! Built with `discord.py`.

---

## 🧠 Features

- `!stats <pokemon>` – View a Pokémon's base stats and total
- `!evolution <pokemon>` – See full evolution lines with level/item/method details
- `!moveset <pokemon>` – List all moves learned by level-up with type, power, and accuracy
- `!encounters <pokemon> [version]` – See where the Pokémon can be found in the wild (optional game filter)
- `!abilities <pokemon>` – Show standard + hidden abilities, with effect descriptions
- `!types <pokemon>` – View type weaknesses, resistances, and immunities
- `!sprite <pokemon>` – See front/shiny sprites and official artwork

---

## 📦 Requirements

- Python 3.8+
- `discord.py`
- `requests`
- A Discord bot token

Install dependencies with:

```bash
pip install -r requirements.txt
