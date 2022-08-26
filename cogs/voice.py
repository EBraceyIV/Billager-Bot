import json
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random
from mcstatus import JavaServer

mp3s = []


class Voice(commands.Cog, name="Voice"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)


async def setup(bot):
    await bot.add_cog(Voice(bot), guild=discord.Object(id=bot.guilds[0].id))
