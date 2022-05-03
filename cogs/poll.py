import datetime

import discord
from discord.ext import commands
from discord import app_commands
import typing


class Poll(commands.Cog, name="Poll"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="poll",
                          description="Start a poll! Enter how long it should last and the options to pick from.")
    @app_commands.describe(duration="How long should the poll be open?", opt1="First Option")
    async def poll(self, interaction: discord.Interaction, duration: str, interval: str,
                   opt1: str, opt2: str, opt3: typing.Optional[str], opt4: typing.Optional[str]):
        pass


async def setup(bot):
    await bot.add_cog(Poll(bot), guild=discord.Object(id=bot.guilds[0].id))
