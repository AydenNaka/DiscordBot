import random
import json
import datetime
from datetime import date, timedelta

eventdata = "eventdata.json"
userdata = "data.json"

import discord
from discord import app_commands
from discord.ext import commands
import config

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import bottoken

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"initiated as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(f"unable to sync {e}")

@bot.event
@commands.has_permissions(moderate_members=True)
async def on_message(message):
    if message.author == bot.user:
        return
    
    with open(eventdata, "r") as file:
        active = json.load(file)
    if date.fromisoformat(active["purge"]["enddate"]) > date.today():
        with open(userdata, "r") as file:
            userlist = json.load(file)
        if str(message.author) not in userlist:
            userlist[str(message.author)] = {
                "purgelives": 0,
                "badletters": 0,
                "fineletters": 0
            }
        content = message.content.lower()
        badletters = content.count(active["purge"]["letter"])
        fineletters = len(content) - badletters
        userlist[str(message.author)]["badletters"] = badletters
        userlist[str(message.author)]["fineletters"] = fineletters
        with open(userdata, "w") as file:
            json.dump(userlist, file, indent=4)
        if badletters > 0:
            timeouttime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=random.randint(1, 300))
            await message.author.timeout(timeouttime, reason="You have spoken against god (Jackson) himself")
            await message.add_reaction('<:banned:1438051448683495515>')

@bot.tree.command(name="confess", description="send anonymous confession")
@app_commands.describe(text="confession here")
async def confess(interaction: discord.Interaction, text: str):
    confessionChannel = bot.get_channel(config.confession)
    await interaction.response.defer(ephemeral=True)
    if not confessionChannel:
        await interaction.response.send_message("wrong channel", ephemeral=True)
        return

    await confessionChannel.send(f"**confession**\n{text}")
    await interaction.followup.send("sent", ephemeral=True)

@bot.tree.command(name="purge", description="initiate banned letter")
async def purge(interaction: discord.Interaction):
    if interaction.user.id in config.users:

        # Generate New Letter
        letters = "abcdefghijklmnopqrstuvwxyz"
        with open(eventdata, "r") as file:
            eventtemp = json.load(file)
        eventtemp["purge"]["letter"] = letters[random.randint(0, len(letters) - 1)]
        eventtemp["purge"]["enddate"] = (date.today() + timedelta(days=1)).isoformat()
        with open(eventtemp, "w") as file:
            json.dump(eventtemp, file, indent=4)
        
        # Clear Past User Data
        with open(userdata, "r") as file:
            usertemp = json.load(file)
        for key in usertemp:
            usertemp[key]["badletters"] = 0
            usertemp[key]["fineletters"] = 0
        with open(userdata, "w") as file:
            json.dump(usertemp, file, indent=4)

        await interaction.response.send_message(
            f"# The letter {eventtemp['purge']['letter'].upper()} is banned for the next 24 hours",
            ephemeral=True
        )

bot.run(bottoken.token)
