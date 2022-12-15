from enum import Enum
import json
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random


class Cards(Enum):
    Ace = [1, "ACE", ["🂡", "🂱", "🃁", "🃑"]]  # Suit order is spade, heart, diamond, club
    Two = [2, "TWO", ["🂢", "🂲", "🃂", "🃒"]]
    Three = [3, "THREE", ["🂣", "🂳", "🃃", "🃓"]]
    Four = [4, "FOUR", ["🂤",  "🂴", "🃄",	"🃔"]]
    Five = [5, "FIVE", ["🂥", "🂵", "🃅", "🃕"]]
    Six = [6, "SIX", ["🂦", "🂶", "🃆", "🃖"]]
    Seven = [7, "SEVEN", ["🂧",	"🂷", "🃇", "🃗"]]
    Eight = [8, "EIGHT", ["🂨",	"🂸", "🃈", "🃘"]]
    Nine = [9, "NINE", ["🂩", "🂹", "🃉", "🃙"]]
    Ten = [10, "TEN", ["🂪",	"🂺", "🃊", "🃚"]]
    Jack = [10, "JACK", ["🂫", "🂻", "🃋", "🃛"]]
    Queen = [10, "QUEEN", ["🂭",	"🂽", "🃍", "🃝"]]
    King = [10, "KING", ["🂮", "🂾", "🃎", "🃞"]]


# class Cards(Enum):
#     SA = [1, "🂡"]
#     S2 = [2, "🂢"]
#     S3 = [3, "🂣"]
#     S4 = [4, "🂤"]
#     S5 = [5, "🂥"]
#     S6 = [6, "🂦"]
#     S7 = [7, "🂧"]
#     S8 = [8, "🂨"]
#     S9 = [9, "🂩"]
#     ST = [10, "🂪"]
#     SJ = [10, "🂫"]
#     SQ = [10, "🂭"]
#     SK = [10, "🂮"]
#     HA = [1, "🂱"]
#     H2 = [2, "🂲"]
#     H3 = [3, "🂳"]
#     H4 = [4. "🂴"]
#     H5 = [5, "🂵"]
#     H6 = [6, "🂶"]
#     H7 = [7, "🂷"]
#     H8 = [8, "🂸"]
#     H9 = [9, "🂹"]
#     HT = [10, "🂺"]
#     HJ = [10, "🂻"]
#     HQ = [10, "🂽"]
#     HK = [10, "🂾"]


# Play a game of blackjack with Bbot
class Controls(discord.ui.View):
    # Hit to take another card
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def hit(self, interaction: discord.Interaction, button: discord.Button):
        print("Hit!")
        self.stop()

    # Stand to end game
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def stand(self, interaction: discord.Interaction, button: discord.Button):
        print("Stand!")
        self.stop()


class Blackjack(commands.Cog, name="Blackjack"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)
        self.emb_template = discord.Embed(title="Billager's Big Baller Blackjack Table",
                                          description="Hit, Stand, Win, Lose, it's all the same to me.",
                                          color=0x7289da)

    @app_commands.command(name="blackjack", description="Play a game of blackjack with Billager.")
    async def blackjack(self, interaction: discord.Interaction):
        view = Controls()
        await interaction.response.send_message(embed=self.emb_template, view=view)
        await view.wait()


async def setup(bot):
    await bot.add_cog(Blackjack(bot), guild=discord.Object(id=bot.guilds[0].id))
