import datetime
import random
import discord
from discord.ext import commands
from discord import app_commands
import shelve
import typing


class Star(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_reaction_add")
    async def star(self, reaction, user):
        print(reaction.message.reactions)
        for react in reaction.message.reactions:
            if react.emoji == "⭐":
                print("CHECK " + str(react.count))
                # await discord.Message.pin(reaction.message)


async def setup(bot):
    await bot.add_cog(Star(bot), guild=discord.Object(id=bot.guilds[0].id))
