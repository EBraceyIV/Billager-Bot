#!python 3.10
import os
import discord
from discord.ext import commands
from discord import app_commands
import TOKEN
import shelve
import asyncio

# TOKEN retrieved from a separate file
TOKEN = TOKEN.TOKEN

bot = commands.Bot(command_prefix=['bb:', 'BB:', 'Bb:', 'Bb:'],
                   description="Your very good friend, the Billager.",
                   case_insensitive=True,
                   intents=discord.Intents.all())


# Conduct on startup
@bot.event
async def on_ready():
    print('Billager has logged in as {0}.'.format(bot.user.name))

    # Breathe a bit of life into our creation with some fun activity
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with his axe."))


# Print list of synced slash commands
@bot.command(name="coms")
async def coms(ctx):
    print(await bot.tree.fetch_commands(guild=ctx.guild))
    await ctx.send(await bot.tree.fetch_commands(guild=ctx.guild))


# In case there are any unforeseen issues, the cogs can all be reloaded by a mod/admin
@bot.command(name="cogReload", help="Reload them cogs", hidden=True)
@commands.check(commands.has_guild_permissions(manage_guild=True))
async def cog_reload(ctx):
    await cog_loader("reload")
    await ctx.send("Cogs Reloaded. KACHOW!")


@bot.command(name="sync", help="Sync the slash commands")
async def sync(ctx):
    await bot.tree.sync(guild=ctx.guild)
    print("Slash commands synced: " + str(await bot.tree.fetch_commands(guild=ctx.guild)))
    await ctx.send("Slashes synced.")


@bot.command(name="ping")
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
        # Load the command cogs
        await cog_loader("load")

        # Start up the bot
        await bot.start(TOKEN)


asyncio.run(main())
