from enum import Enum
import json
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random


class Cards(Enum):
    SA = [1, "🂡"]
    S2 = [2, "🂢"]
    S3 = [3, "🂣"]
    S4 = [4, "🂤"]
    S5 = [5, "🂥"]
    S6 = [6, "🂦"]
    S7 = [7, "🂧"]
    S8 = [8, "🂨"]
    S9 = [9, "🂩"]
    ST = [10, "🂪"]
    SJ = [10, "🂫"]
    SQ = [10, "🂭"]
    SK = [10, "🂮"]


# Play a game of blackjack with Bbot
class Blackjack(commands.Cog, name="Blackjack"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)



async def setup(bot):
    await bot.add_cog(Blackjack(bot), guild=discord.Object(id=bot.guilds[0].id))
