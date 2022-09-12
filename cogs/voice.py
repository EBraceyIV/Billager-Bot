import asyncio
import json
import typing
import os
from pathlib import Path
import discord
from discord.ext import commands
from discord import app_commands
import random

mp3s = []
for file in os.listdir(Path.cwd() / "mp3s"):
    mp3s.append(file[:-4])
# for file in os.listdir(Path("/mnt/music/Big Daddy Graham CD")):  #this works
#     mp3s.append(file[:-4])
# for file in os.listdir(Path("//BillagerCloud/music/Big Daddy Graham CD")):
#     mp3s.append(file[:-4])

vc = 0


class Voice(commands.Cog, name="Voice"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)

    @app_commands.command(name="join")
    async def join(self, interaction: discord.Interaction):
        global vc
        author = interaction.user
        vc = await author.voice.channel.connect()

    @app_commands.command(name="play")
    async def play(self, interaction: discord.Interaction, sound: str):
        global vc
        if sound in mp3s:
            sound = sound + ".mp3"
        else:
            await interaction.response.send_message("Try something else.")

        if vc == 0:
            try:
                vc = await interaction.user.author.voice.channel.connect()
            except:
                pass

        source = discord.FFmpegPCMAudio(str(Path.cwd() / 'mp3s' / sound))
        # if os.path.exists(Path.cwd() / 'mp3s' / sound):
        #     source = discord.FFmpegPCMAudio(str(Path.cwd() / 'mp3s' / sound))
        # elif os.path.exists((Path("//BillagerCloud/music/Big Daddy Graham CD") / sound)):
        #     source = discord.FFmpegPCMAudio(str(Path("//BillagerCloud/music/Big Daddy Graham CD") / sound))
        # else:
        #     return

        # source = discord.FFmpegPCMAudio(str("/mnt/music/Big Daddy Graham CD/" + sound))
        vc.play(source, after=None)
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()

    @app_commands.command(name="leave")
    async def leave(self, interaction: discord.Interaction):
        await self.bot.voice_clients[0].disconnect(force=False)


async def setup(bot):
    await bot.add_cog(Voice(bot), guild=discord.Object(id=bot.guilds[0].id))
