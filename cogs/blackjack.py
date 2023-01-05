import asyncio
from enum import Enum
import json
import typing
import discord
from discord.ext import commands
from discord import app_commands
import random

CARDBACK = "🂠"


class Cards(Enum):
    Ace = [11, "ACE", ["🂡", "🂱", "🃁", "🃑"]]  # Suit order is spade, heart, diamond, club
    Two = [2, "TWO", ["🂢", "🂲", "🃂", "🃒"]]
    Three = [3, "THREE", ["🂣", "🂳", "🃃", "🃓"]]
    Four = [4, "FOUR", ["🂤", "🂴", "🃄", "🃔"]]
    Five = [5, "FIVE", ["🂥", "🂵", "🃅", "🃕"]]
    Six = [6, "SIX", ["🂦", "🂶", "🃆", "🃖"]]
    Seven = [7, "SEVEN", ["🂧", "🂷", "🃇", "🃗"]]
    Eight = [8, "EIGHT", ["🂨", "🂸", "🃈", "🃘"]]
    Nine = [9, "NINE", ["🂩", "🂹", "🃉", "🃙"]]
    Ten = [10, "TEN", ["🂪", "🂺", "🃊", "🃚"]]
    Jack = [10, "JACK", ["🂫", "🂻", "🃋", "🃛"]]
    Queen = [10, "QUEEN", ["🂭", "🂽", "🃍", "🃝"]]
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


# def deal():
#     card_data = random.choice(list(Cards))
#     card_icon = card_data.value[2][random.randint(0, 3)]
#     card_value = card_data.value[0]
#     return card_icon, card_value


class State:
    def __init__(self):
        self.hand = []
        self.value = []

    def deal(self):
        card_data = random.choice(list(Cards))
        self.hand.append(card_data.value[2][random.randint(0, 3)])
        self.value.append(card_data.value[0])


class Controls(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.firstHandBool = False
        self.timeout = 30
        self.response = None
        self.embed = None
        self.DealerState = None
        self.PlayerState = None
        self.winner = None
        self.condition = ""
        self.cards_output = ""

    def checkGameCondition(self, _State_value):
        # Check for game-end condition
        if sum(_State_value) > 21:
            self.condition = "**BUST!**"
        elif sum(_State_value) == 21:
            self.condition = "**BLACKJACK!**"

    def checkWinner(self):
        if sum(self.PlayerState.value) < sum(self.DealerState.value):
            self.winner = "DEALER"
        elif sum(self.PlayerState.value) == sum(self.DealerState.value):
            pass
        elif sum(self.PlayerState.value) > sum(self.DealerState.value):
            self.winner = "PLAYER"

    def endGame(self):
        self.PlayerState = None
        self.DealerState = None
        for child in self.children:
            child.disabled = True
        self.stop()

    # Hit to take another card
    # TODO: Ace 1/11 handling
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple, custom_id="hit")
    async def hit(self, interaction: discord.Interaction, button: discord.Button):
        # Deal new card to player
        self.PlayerState.deal()

        # Check for game-end condition
        self.checkGameCondition(self.PlayerState.value)

        # Add new card to hand display
        for card in self.PlayerState.hand:
            self.cards_output += card

        # Update embed with new hand and value + game-end condition (conditional)
        self.embed.set_field_at(index=1,
                                name="Your Hand",
                                value=self.cards_output + " " + str(sum(self.PlayerState.value)) + " " + self.condition)
        await interaction.response.edit_message(embed=self.embed)
        # Reset hand to display
        self.cards_output = ""

        # If game has ended, clean up variables and stop the view from taking new input
        if self.condition != "":
            self.PlayerState = None
            self.DealerState = None
            for child in self.children:
                child.disabled = True
            await self.response.edit(view=self)
            self.stop()

    # Stand to end game
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple, custom_id="stand")
    async def stand(self, interaction: discord.Interaction, button: discord.Button):
        # Add cards to hand display
        for card in self.DealerState.hand:
            self.cards_output += card

        # Check for game-end condition
        self.checkGameCondition(self.DealerState.value)

        # Update embed to reveal dealer's hidden card and hand value
        self.embed.set_field_at(index=0,
                                name="Dealer's Hand",
                                value=self.cards_output + " " + str(sum(self.DealerState.value)) + " " + self.condition)
        await interaction.response.edit_message(embed=self.embed)

        # Reset hand to display
        self.cards_output = ""

        # Brief pause for "realism"
        await asyncio.sleep(0.5)

        # Dealer gets another card if player stands and their hand is valued higher than dealer's revealed hand
        if sum(self.DealerState.value) < sum(self.PlayerState.value):
            self.DealerState.deal()

            # Add new card to hand display
            for card in self.DealerState.hand:
                self.cards_output += card

            # Check for game-end condition
            self.checkGameCondition(self.DealerState.value)

            # Update embed with added card
            self.embed.set_field_at(index=0,
                                    name="Dealer's Hand",
                                    value=self.cards_output + " " + str(sum(self.DealerState.value)) + " " +
                                    self.condition)
            await interaction.edit_original_response(embed=self.embed)

            self.cards_output = ""
            await asyncio.sleep(0.5)
        elif sum(self.DealerState.value) == sum(self.PlayerState.value):
            self.embed.insert_field_at(index=2,
                                       name="**PUSH**",
                                       value="Good news, you didn't lose. Bad news, you didn't win.")
            await interaction.edit_original_response(embed=self.embed)
            self.endGame()
            await self.response.edit(view=self)
            return
        elif sum(self.DealerState.value) > sum(self.PlayerState.value):
            self.embed.insert_field_at(index=2,
                                       name="**YOU LOSE.**",
                                       value="Go back to playing Yu-Gi-Oh.")
            await interaction.edit_original_response(embed=self.embed)
            self.endGame()
            await self.response.edit(view=self)
            return

        if self.condition == "**BUST!**":
            self.embed.insert_field_at(index=2,
                                       name="**YOU WIN!**",
                                       value="Counting cards pays off.")
            await interaction.edit_original_response(embed=self.embed)
            self.endGame()
            await self.response.edit(view=self)
            return

        if sum(self.DealerState.value) < sum(self.PlayerState.value):
            self.embed.insert_field_at(index=2,
                                       name="**YOU WIN!**",
                                       value="Counting cards pays off.")
            await interaction.edit_original_response(embed=self.embed)
        elif sum(self.DealerState.value) == sum(self.PlayerState.value):
            self.embed.insert_field_at(index=2,
                                       name="**PUSH**",
                                       value="Good news, you didn't lose. Bad news, you didn't win.")
            await interaction.edit_original_response(embed=self.embed)
        elif sum(self.DealerState.value) > sum(self.PlayerState.value):
            self.embed.insert_field_at(index=2,
                                       name="**YOU LOSE.**",
                                       value="Go back to playing Yu-Gi-Oh.")
            await interaction.edit_original_response(embed=self.embed)

        self.endGame()
        await self.response.edit(view=self)


class Blackjack(commands.Cog, name="Blackjack"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)
        self.emb_template = discord.Embed(title="Billager's Big Baller Blackjack Table",
                                          description="Hit, Stand, Win, Lose, it's all the same to me.",
                                          color=0x7289da)

    # TODO: Handling for getting blackjack on first deal
    @app_commands.command(name="blackjack", description="Play a game of blackjack with Billager.")
    async def blackjack(self, interaction: discord.Interaction):
        view = Controls()

        embed = self.emb_template
        # Clearing the fields prevents multiple new fields being added to the initially summoned embed by
        # running the command again
        embed.clear_fields()

        # Deal first two cards to dealer and player
        # # Dealer data
        DealerState = State()
        DealerState.deal()
        DealerState.deal()

        # # Player data
        PlayerState = State()
        PlayerState.deal()
        PlayerState.deal()

        # Check for chance that player was dealt a blackjack, disable buttons prior to display if true
        view.checkGameCondition(PlayerState.value)
        # Game condition is used instead of just equating the value to 21 so that it can be used in the embed below
        if view.condition != "":
            view.hit.disabled = True
            view.stand.disabled = True

        # Dealer's second card obscured to start
        embed.insert_field_at(index=0,
                              name="Dealer's Hand",
                              value=DealerState.hand[0] + " " + CARDBACK + " " + "???")

        # Display player's dealt hand and current value (plus condition if dealt a blackjack)
        embed.insert_field_at(index=1,
                              name="Your Hand",
                              value=PlayerState.hand[0] + PlayerState.hand[1] + " " + str(sum(PlayerState.value)) +
                              " " + view.condition)

        # Pass states to view for button handling
        view.embed = embed
        view.DealerState = DealerState
        view.PlayerState = PlayerState
        await interaction.response.send_message(embed=self.emb_template, view=view)
        view.response = await interaction.original_response()
        await view.wait()


async def setup(bot):
    await bot.add_cog(Blackjack(bot), guild=discord.Object(id=bot.guilds[0].id))
