import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
from evolutions import get_evolution_chain
from moves import get_moveset
from encounters import get_encounter_locations
from abilities import get_abilities
from typeinfo import get_type_effectiveness



load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event

async def on_ready():
    print(f'{bot.user.name} is now connected to Discord!')

@bot.command(name='stats')

async def pokemon_stats(ctx, *, pokemon_name: str):
    pokemon_name = pokemon_name.lower()
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")

    if response.status_code != 200:
        await ctx.send(f"Could not find Pokémon: `{pokemon_name}`. Please try again!")
        return

    data = response.json()

    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    total_stats = sum(stats.values())

    stats_message = (
        f"**{data['name'].title()}** Base Stats:\n"
        f"**HP**: {stats['hp']}\n"
        f"**Attack**: {stats['attack']}\n"
        f"**Defense**: {stats['defense']}\n"
        f"**Special Attack**: {stats['special-attack']}\n"
        f"**Special Defense**: {stats['special-defense']}\n"
        f"**Speed**: {stats['speed']}\n\n"
        f"**Total**: {total_stats}"
    )





    await ctx.send(stats_message)



@bot.command(name='evolution')
async def evolution_command(ctx, *, pokemon_name: str):
    chains, error = get_evolution_chain(pokemon_name)

    if error:
        await ctx.send(error)
        return

    formatted = "\n".join(" → ".join(step) for step in chains)
    await ctx.send(f"**Evolution lines for {pokemon_name.title()}:**\n{formatted}")


@bot.command(name='moveset')
async def moveset_command(ctx, *, pokemon_name: str):
    moves, error = get_moveset(pokemon_name)

    if error:
        await ctx.send(error)
        return

    if not moves:
        await ctx.send(f"{pokemon_name.title()} doesn't learn any moves by level-up.")
        return

    message = f"**Moveset for {pokemon_name.title()}:**\n"
    for move in moves:
        message += (
            f"🟢 **{move['name']}** (Lv {move['level']}): "
            f"{move['type']} • {move['class']} • "
            f"Power: {move['power']} • Acc: {move['accuracy']}\n"
        )

    # If message too long for Discord, send in chunks
    for chunk in [message[i:i+1900] for i in range(0, len(message), 1900)]:
        await ctx.send(chunk)


@bot.command(name='encounters')
async def encounters_command(ctx, *, args: str):
    parts = args.split()
    if len(parts) == 0:
        await ctx.send("Please provide a Pokémon name.")
        return

    pokemon_name = parts[0]
    version = parts[1] if len(parts) > 1 else None

    data, error = get_encounter_locations(pokemon_name, version)

    if error:
        await ctx.send(error)
        return

    if not data:
        await ctx.send(f"{pokemon_name.title()} does not appear in the wild.")
        return

    version_label = f" ({version.title()})" if version else ""
    response = f"**Wild Encounter Locations for {pokemon_name.title()}{version_label}:**\n"
    for i, entry in enumerate(data[:10]):
        response += (
            f"📍 **{entry['location']}** ({entry['version']})\n"
            f"Method: {entry['method']} • Chance: {entry['chance']}%\n\n"
        )

    await ctx.send(response)


@bot.command(name='abilities')
async def abilities_command(ctx, *, pokemon_name: str):
    data, error = get_abilities(pokemon_name)

    if error:
        await ctx.send(error)
        return

    message = f"**Abilities for {pokemon_name.title()}:**\n"

    if data['standard']:
        message += "\n🧠 **Standard Abilities:**\n"
        for ability in data['standard']:
            message += f"- **{ability['name']}**: {ability['description']}\n"

    if data['hidden']:
        message += "\n🌟 **Hidden Ability:**\n"
        for ability in data['hidden']:
            message += f"- **{ability['name']}**: {ability['description']}\n"

    await ctx.send(message[:2000])  # Just in case it's long


@bot.command(name='types')
async def types_command(ctx, *, pokemon_name: str):
    info, error = get_type_effectiveness(pokemon_name)

    if error:
        await ctx.send(error)
        return

    msg = f"**{pokemon_name.title()}** is {info['types']}\n\n"

    if info['weaknesses']:
        msg += f"❌ **Weak to:** {', '.join(info['weaknesses'])}\n"
    if info['resistances']:
        msg += f"✅ **Resistant to:** {', '.join(info['resistances'])}\n"
    if info['immunities']:
        msg += f"🛡️ **Immune to:** {', '.join(info['immunities'])}\n"

    await ctx.send(msg)


@bot.command(name='sprite')
async def sprite_command(ctx, *, pokemon_name: str):
    res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
    if res.status_code != 200:
        await ctx.send(f"Could not find Pokémon: `{pokemon_name}`")
        return

    data = res.json()

    name = data['name'].title()
    types = [t['type']['name'].title() for t in data['types']]
    type_str = ' / '.join(types)

    # Sprites
    front_default = data['sprites']['front_default']
    front_shiny = data['sprites']['front_shiny']
    artwork = data['sprites']['other']['official-artwork']['front_default']

    embed = discord.Embed(
        title=f"{name}",
        description=f"Type: {type_str}",
        color=discord.Color.gold()
    )

    if artwork:
        embed.set_thumbnail(url=artwork)

    if front_default and front_shiny:
        embed.add_field(name="🧍 Regular", value="[Sprite Link]({})".format(front_default), inline=True)
        embed.add_field(name="✨ Shiny", value="[Sprite Link]({})".format(front_shiny), inline=True)
        embed.set_image(url=front_shiny)  # Highlight shiny version
    elif front_default:
        embed.set_image(url=front_default)

    await ctx.send(embed=embed)



@bot.command(name="rules")
async def rules_command(ctx):
    help_message = (
        "**Available Pokébot Commands:**\n\n"
        "`!stats <pokemon>` → Show base stats and total\n"
        "`!evolution <pokemon>` → Show evolution chain + method\n"
        "`!moveset <pokemon>` → List moves learned by level\n"
        "`!encounters <pokemon>` → Where it can be found (wild)\n"
        "`!abilities <pokemon>` → Shows abilities + what they do\n"
        "`!types <pokemon>` → Type effectiveness chart\n"
        "`!sprite <pokemon>` → Show front sprite, shiny, and art\n"
    )
    await ctx.send(help_message)






bot.run(TOKEN)