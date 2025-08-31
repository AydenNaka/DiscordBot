import discord
from discord import app_commands
from discord.ext import commands
import config

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import bottoken

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
    confessionChannel = bot.get_channel(config.confession)
    print(config.confession)
    if not confessionChannel:
        await interaction.response.send_message("wrong channel", ephemeral=True)
        return

    await confessionChannel.send(f"**confession**\n{text}")
    await interaction.followup.send("sent", ephemeral=True)

bot.run(bottoken.token)
