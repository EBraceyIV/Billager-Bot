import asyncio

import discord
from discord.ext import commands
from discord import app_commands
import shelve
import typing

# Initialize the scoreboard list of all currently scored members
scores = shelve.open("plusMinus")
scored_members = list(scores.keys())
scores.close()


# Member score management function
#   action: Add to or subtract from a score, or see what the score is
#   member: Which user's score to manage
#   amount: What score to add/remove
def score_func(action, member, amount):
    global scored_members
    plus_minus = shelve.open("plusMinus")
    if action == "init":
        plus_minus[member] = amount
    elif action == "add":
        plus_minus[member] = plus_minus.get(member) + amount
    elif action == "get":
        return plus_minus.get(member)
    elif action == "subtract":
        plus_minus[member] = plus_minus.get(member) - amount
    scored_members = list(plus_minus.keys())
    plus_minus.close()


# This is here to use
beefBrain = '<:BeefBrain:631694337549271050>'


class Scores(commands.Cog, name="Scores"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Let users add to other user's scores
    @app_commands.command(name="plus", description="Add to a user's score")
    async def plus(self, interaction: discord.Interaction, member: discord.Member, num: typing.Optional[int] = 1):
        if member.mention == interaction.user.mention:
            await interaction.response.send_message("Trying to boost your own numbers? Shameful!")
        else:
            if member.mention not in scored_members:
                score_func("init", member.mention, num)
            else:
                score_func("add", member.mention, num)
            await interaction.response.send_message(str(member.display_name) + ' +' + str(num))

    # Let users subtract from other user's scores
    @app_commands.command(name="minus", description="Subtract from a user's score")
    async def minus(self, interaction: discord.Interaction, member: discord.Member, num: typing.Optional[int] = 1):
        if member.mention not in scored_members:
            score_func("init", member.mention, -num)
        else:
            score_func("subtract", member.mention, num)
        if member.mention == interaction.user.mention:
            await interaction.response.send_message("I mean, if really want to...")
            await asyncio.sleep(2)
            await interaction.edit_original_message(content="I mean, if you really want to...\n" +
                                                    member.display_name + " -" + str(num))
        else:
            await interaction.response.send_message(str(member.display_name) + ' -' + str(num))

    # Show a scoreboard from highest to lowest for all users with a score
    @app_commands.command(name="scoreboard", description="Scoreboard of the highest and lowest scores.")
    async def score(self, interaction: discord.Interaction):
        # Initialize scoreboard embed message and embed description
        embed = discord.Embed(title="Scoreboard")
        desc = ""
        score_list = shelve.open("plusMinus")
        # Sort the current user scores from highest to lowest
        score_sorted = sorted(score_list.items(), key=lambda x: x[1])
        # Iterate through the scores and build the embed content
        for score in score_sorted:
            # Here "score" is a tuple, containing the user and score, adding each to a new line
            desc = str(score[0]) + ": " + str(score[1]) + "\n" + desc
        score_list.close()
        # Add some flavor text and send the message
        embed.description = "Here's the current scoreboard. Honestly can't believe these numbers: \n\n" + desc
        embed.set_footer(text="Be sure to use /plus and /minus to keep our scoreboard up to date.")
        await interaction.response.send_message(embed=embed)

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
    await bot.add_cog(Scores(bot), guild=discord.Object(id=bot.guilds[0].id))
