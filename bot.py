import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
from evolutions import get_evolution_chain


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


bot.run(TOKEN)