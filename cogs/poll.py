import datetime
import typing
import discord
from discord.ext import commands
from discord import app_commands
import typing


class Poll(commands.Cog, name="Poll"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="poll",
                          description="Start a poll! Enter how long it should last and the options to pick from.")
    @app_commands.describe(duration="How long should the poll be open?", interval="There is a 7 day (168 hour) limit.")
    async def poll(self, interaction: discord.Interaction,
                   title: str, description: str,
                   duration: str, interval: typing.Literal["hours", "days"],
                   opt1: str, opt2: str, opt3: typing.Optional[str], opt4: typing.Optional[str]):
        embed = discord.Embed(title=title, description=description)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Poll(bot), guild=discord.Object(id=bot.guilds[0].id))
