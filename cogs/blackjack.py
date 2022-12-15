from enum import Enum
import json
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random

CARDBACK = "🂠"


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
    def __init__(self):
        super().__init__()
        self.response = None
        self.embed = None
        self.D_hand = [None]
        self.D_value = 0
        self.D_cards = []
        self.P_hand = [None]
        self.P_value = 0
        self.P_cards = []

    # Hit to take another card
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple)
    async def hit(self, interaction: discord.Interaction, button: discord.Button):
        # This is all kinds of messed up at the moment
        self.P_hand.append(random.choice(list(Cards)))
        # print(self.P_hand)
        for card in self.P_hand:
            self.P_value += card.value[0]
            self.P_cards.append(card.value[2][random.randint(0, 3)])
        self.embed.set_field_at(index=1,
                                name="Your Hand",
                                value=str(self.P_cards) + " " + str(self.P_value))
        await interaction.response.edit_message(embed=self.embed)

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

        embed = self.emb_template
        #random.choice(list(Cards)).value[2][random.randint(0, 3)]

        # Dealer data
        D_hand = [random.choice(list(Cards)),
                  random.choice(list(Cards))]
        D_value = D_hand[0].value[0] + D_hand[1].value[0]
        view.D_hand = D_hand
        #view.D_value = D_value

        # Player data
        P_hand = [random.choice(list(Cards)),
                  random.choice(list(Cards))]
        P_value = P_hand[0].value[0] + P_hand[1].value[0]
        view.P_hand = P_hand
        #view.P_value = P_value

        embed.insert_field_at(index=0,
                              name="Dealer's Hand",
                              value=D_hand[0].value[2][random.randint(0, 3)] + " " + CARDBACK + "\n" + "???")
        embed.insert_field_at(index=1,
                              name="Your Hand",
                              value=P_hand[0].value[2][random.randint(0, 3)] + " " + P_hand[1].value[2][random.randint(0, 3)] + "\n" + str(P_value))
        view.embed = embed

        await interaction.response.send_message(embed=self.emb_template, view=view)
        # view.response = await interaction.original_response()

        await view.wait()


async def setup(bot):
    await bot.add_cog(Blackjack(bot), guild=discord.Object(id=bot.guilds[0].id))
