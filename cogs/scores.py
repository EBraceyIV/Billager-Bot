import discord
from discord.ext import commands
from discord import app_commands
import shelve
import typing

# # Initialize the scoreboard list of all currently scored members
# scores = shelve.open("plusMinus")
# scored_members = list(scores.keys())
# scores.close()


# # Member score management function
# #   action: Add to or subtract from a score, or see what the score is
# #   member: Which user's score to manage
# #   amount: What score to add/remove
# def score_func(action, member, amount):
#     global scored_members
#     plus_minus = shelve.open("plusMinus")
#     if action == "init":
#         plus_minus[member] = amount
#     elif action == "add":
#         plus_minus[member] = plus_minus.get(member) + amount
#     elif action == "get":
#         return plus_minus.get(member)
#     elif action == "subtract":
#         plus_minus[member] = plus_minus.get(member) - amount
#     scored_members = list(plus_minus.keys())
#     plus_minus.close()


# This is here to use
beefBrain = '<:BeefBrain:631694337549271050>'


class Scores(commands.Cog, name="Scores"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Let users add to other user's scores
    @app_commands.command(name="plus", description="Add to a user's score")
    async def plus(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(member.display_name + " +1 ")

    # Some general error processing for some of the score commands

    # @plus.error
    # @minus.error
    # async def plus_error(self, ctx, error):
    #     if isinstance(error, commands.BadArgument):
    #         await ctx.send("You can't do that " + beefBrain)
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('You forgot to give me a name ' + beefBrain)
    #
    # @score.error
    # async def score_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('You forgot to give me a name ' + beefBrain)


async def setup(bot):
    await bot.add_cog(Scores(bot), guild=discord.Object(id=627279552481067030))
