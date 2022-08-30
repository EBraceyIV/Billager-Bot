import json
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random

mp3s = []


class Voice(commands.Cog, name="Voice"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)

    @app_commands.command(name="join")
    async def join(self, interaction: discord.Interaction):
        author = interaction.user
        await author.voice.channel.connect()

    @app_commands.command(name="leave")
    async def leave(self, interaction: discord.Interaction):
        await self.bot.voice_clients[0].disconnect(force=False)


async def setup(bot):
    await bot.add_cog(Voice(bot), guild=discord.Object(id=bot.guilds[0].id))
