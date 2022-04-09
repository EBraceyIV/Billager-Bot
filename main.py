#!python 3.10
import os
import discord
from discord.ext import commands
from discord import app_commands
import TOKEN
import shelve
import asyncio
import json
import sys

# # Load config to get token and guild id
# try:
#     with open("config.json") as config:
#         config = json.load(config)
#     # Use argument on launch to determine test bot or live bot
#     if sys.argv[1] == "test":
#         TOKEN = config["test"]["TOKEN"]
#         GUILD = config["test"]["GUILD"]
#     elif sys.argv[1] == "live":
#         TOKEN = config["live"]["TOKEN"]
#         GUILD = config["live"]["GUILD"]
#     else:
#         print("Invalid launch argument. \"test\" or \"test\"")
#
# except IndexError:  # If no argument is provided
#     print("No launch argument provided.\n"
#           "Canceling launch.")
#     sys.exit(0)
#
# except FileNotFoundError:  # If the config could not be loaded
#     print("Could not find \"config.json\"\n"
#           "Canceling launch.")
#     sys.exit(0)
TOKEN = TOKEN.token()

bot = commands.Bot(command_prefix=['bb:', 'BB:', 'Bb:', 'Bb:'],
                   description="Your very good friend, the Billager.",
                   case_insensitive=True,
                   intents=discord.Intents.all())


# Conduct on startup
@bot.event
async def on_ready():
    print('Billager has logged in as {0}.'.format(bot.user.name))

    # Load the command cogs
    await cog_loader("load")

    # Initialize BBux bank and user prize collections
    bbux_bank = shelve.open("bbux_bank")
    member_collections = shelve.open("member_collection")
    for guild in bot.guilds:
        for member in guild.members:
            if member.mention not in bbux_bank:
                bbux_bank[member.mention] = 0
            if member.mention not in member_collections:
                member_collections[member.mention] = {}
    bbux_bank.close()
    member_collections.close()

    # Breathe a bit of life into our creation with some fun activity
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with his axe."))


# Print list of synced slash commands
@bot.command(name="coms", hidden=True)
async def coms(ctx):
    print(await bot.tree.fetch_commands(guild=ctx.guild))
    await ctx.send(await bot.tree.fetch_commands(guild=ctx.guild))


# In case there are any unforeseen issues, the cogs can all be reloaded by a mod/admin
@bot.command(name="cogReload", help="Reload them cogs", hidden=True)
@commands.check(commands.has_guild_permissions(manage_guild=True))
async def cog_reload(ctx):
    await cog_loader("reload")
    await ctx.send("Cogs Reloaded. KACHOW!")


@bot.command(name="sync", help="Sync the slash commands", hidden=True)
async def sync(ctx):
    await bot.tree.sync(guild=ctx.guild)
    print("Slash commands synced: " + str(await bot.tree.fetch_commands(guild=ctx.guild)))
    await ctx.send("Slashes synced.")


@bot.command(name="ping", hidden=True)
async def ping(ctx):
    await ctx.send("PONG!")


# Function to load/reload cogs depending on whether the bot is starting up or if bb:cogreload has been used
async def cog_loader(load_style):
    # Load each cog included in the "cogs" directory
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):  # Safety check to not process any non-cog files
            try:
                # Load or reload, depending on the load_style defined
                if load_style == "load":
                    await bot.load_extension(f'cogs.{cog[:-3]}')
                    print(f"Loaded cog: {cog}")
                else:
                    await bot.reload_extension(f'cogs.{cog[:-3]}')
                    print(f"Reloaded cog: {cog}")
            except Exception as e:  # Report any cog loading errors to the console
                print("Couldn't load cog \"{0}\"".format(cog))
                print("Error: {0}".format(e))


async def main():
    async with bot:

        # Start up the bot
        await bot.start(TOKEN)


asyncio.run(main())
