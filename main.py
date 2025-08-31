import discord
from discord import app_commands
from discord.ext import commands

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import bottoken
print(bottoken.token)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"initiated as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(f"unable to sync {e}")

@bot.tree.command(name="confess", description="send anonymous confession")
@app_commands.describe(text="confession here")
async def confess(interaction: discord.Interaction, text: str):
    confession_channel = bot.get_channel(config.CONFESSION_CHANNEL_ID)
    if not confession_channel:
        await interaction.response.send_message("message cannot be blank", ephemeral=True)
        return

    await confession_channel.send(f"confession\n{text}")

bot.run(bottoken.token)
