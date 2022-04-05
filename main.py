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


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("PONG!")


async def main():
    async with bot:
        # Load the command cogs
        # await cog_loader("load")

        # Start up the bot
        await bot.start(TOKEN)


asyncio.run(main())