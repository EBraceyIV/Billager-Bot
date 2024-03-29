import asyncio

import discord
from discord.ext import commands
from discord import app_commands
import shelve
import datetime
import pytz
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


# Check performed on thumb reactions to prevent affecting scores using old posts
def thumb_recency(reaction) -> bool:
    # Get the time between the message being posted and the thumb being given
    react_delta = datetime.datetime.utcnow() - reaction.message.created_at.replace(tzinfo=None)
    # The recency defines how old a message has to be to not be valid for thumb reactions
    recency_delta = datetime.timedelta(hours=12)
    return react_delta < recency_delta


# This function cleans up the rest of the cog by condensing repeat code that would appear
# The source variable can accept multiple types to support commands, context menu (user/message), etc
def score_process(interaction, source: typing.Union[discord.Member, discord.Message], action):
    # The discord.Message type supports score changes that come from context menus on messages
    if type(source) is discord.Message:
        message = source
        if action == "add":
            if message.author.mention not in scored_members:
                score_func("init", message.author.mention, 1)
            else:
                score_func("add", message.author.mention, 1)
            print(interaction.user.display_name + " +1 to " + message.author.display_name +
                  " @ " + str(datetime.datetime.now()))
        else:
            if message.author.mention not in scored_members:
                score_func("init", message.author.mention, -1)
            else:
                score_func("subtract", message.author.mention, 1)
            print(interaction.user.display_name + " -1 to " + message.author.display_name +
                  " @ " + str(datetime.datetime.now()))
    # The discord.Member type supports the app commands and context menus on users
    elif type(source) is discord.Member:
        member = source
        if action == "add":
            if member.mention not in scored_members:
                score_func("init", member.mention, 1)
            else:
                score_func("add", member.mention, 1)
            print(interaction.user.display_name + " +1 to " + member.display_name +
                  " @ " + str(datetime.datetime.now()))
        else:
            if member.mention not in scored_members:
                score_func("init", member.mention, -1)
            else:
                score_func("subtract", member.mention, 1)
            print(interaction.user.display_name + " -1 to " + member.display_name +
                  " @ " + str(datetime.datetime.now()))
    else:
        print("Something is wrong with the scoring system!")


# This is here to use
beefBrain = '<:BeefBrain:631694337549271050>'


@app_commands.checks.cooldown(rate=1, per=60)
async def ctx_plus_msg(interaction: discord.Interaction, message: discord.Message):
    if message.author.mention == interaction.user.mention:
        await interaction.response.send_message("Trying to boost your own numbers? Shameful!")
    else:
        score_process(interaction, message, "add")
    await interaction.response.send_message(str(message.author.display_name) + " +1")


@app_commands.checks.cooldown(rate=1, per=60)
async def ctx_minus_msg(interaction: discord.Interaction, message: discord.Message):
    score_process(interaction, message, "subtract")
    if message.author.mention == interaction.user.mention:
        await interaction.response.send_message("I mean, if you really want to...")
        await asyncio.sleep(2)
        await interaction.edit_original_response(content="I mean, if you really want to...\n" +
                                                 message.author.display_name + " -1")
    else:
        await interaction.response.send_message(str(message.author.display_name) + " -1")


@app_commands.checks.cooldown(rate=1, per=60)
async def ctx_plus_usr(interaction: discord.Interaction, member: discord.Member):
    if member.mention == interaction.user.mention:
        await interaction.response.send_message("Trying to boost your own numbers? Shameful!")
    else:
        score_process(interaction, member, "add")
    await interaction.response.send_message(str(member.display_name) + " +1")


@app_commands.checks.cooldown(rate=1, per=60)
async def ctx_minus_usr(interaction: discord.Interaction, member: discord.Member):
    score_process(interaction, member, "subtract")
    if member.mention == interaction.user.mention:
        await interaction.response.send_message("I mean, if you really want to...")
        await asyncio.sleep(2)
        await interaction.edit_original_response(content="I mean, if you really want to...\n" +
                                                 member.display_name + " -1")
    else:
        await interaction.response.send_message(str(member.display_name) + " -1")


class Scores(commands.Cog, name="Scores"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ctx_menu_plus_msg = app_commands.ContextMenu(name="+1",
                                                          callback=ctx_plus_msg,
                                                          guild_ids=[self.bot.guilds[0].id])
        self.ctx_menu_minus_msg = app_commands.ContextMenu(name="-1",
                                                           callback=ctx_minus_msg,
                                                           guild_ids=[self.bot.guilds[0].id])
        self.ctx_menu_plus_usr = app_commands.ContextMenu(name="+1",
                                                          callback=ctx_plus_usr,
                                                          guild_ids=[self.bot.guilds[0].id])
        self.ctx_menu_minus_usr = app_commands.ContextMenu(name="-1",
                                                           callback=ctx_minus_usr,
                                                           guild_ids=[self.bot.guilds[0].id])
        self.bot.tree.add_command(self.ctx_menu_plus_msg)
        self.bot.tree.add_command(self.ctx_menu_minus_msg)
        self.bot.tree.add_command(self.ctx_menu_plus_usr)
        self.bot.tree.add_command(self.ctx_menu_minus_usr)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu_plus_msg.name, type=self.ctx_menu_plus_msg.type)
        self.bot.tree.remove_command(self.ctx_menu_minus_msg.name, type=self.ctx_menu_minus_msg.type)
        self.bot.tree.remove_command(self.ctx_menu_plus_usr.name, type=self.ctx_menu_plus_usr.type)
        self.bot.tree.remove_command(self.ctx_menu_minus_usr.name, type=self.ctx_menu_minus_usr.type)

    # Let users add to other user's scores
    @app_commands.command(name="plus", description="Add to a user's score")
    @app_commands.checks.cooldown(rate=1, per=60)
    async def plus(self, interaction: discord.Interaction, member: discord.Member):
        if member.mention == interaction.user.mention:
            await interaction.response.send_message("Trying to boost your own numbers? Shameful!")
        else:
            score_process(interaction, member, "add")
            await interaction.response.send_message(str(member.display_name) + " +1")

    # Let users subtract from other user's scores
    @app_commands.command(name="minus", description="Subtract from a user's score")
    @app_commands.checks.cooldown(rate=1, per=60)
    async def minus(self, interaction: discord.Interaction, member: discord.Member):
        score_process(interaction, member, "subtract")
        if member.mention == interaction.user.mention:
            await interaction.response.send_message("I mean, if you really want to...")
            await asyncio.sleep(2)
            await interaction.edit_original_response(content="I mean, if you really want to...\n" +
                                                     member.display_name + " -1")
        else:
            await interaction.response.send_message(str(member.display_name) + " -1")

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

    # Users can be +/- 1'd with a corresponding thumb reaction
    @commands.Cog.listener("on_reaction_add")
    async def thumbs(self, reaction, user):
        # Initialize user's score if needed
        if reaction.message.author.mention not in scored_members:
            score_func("init", reaction.message.author.mention, 0)
        # Recency check for reaction so you can't thumb down an old message
        if not thumb_recency(reaction):
            return
        # Thumbs down is a -1
        if reaction.emoji == "👎":
            print(user.display_name + " -1" + " to " + reaction.message.author.display_name +
                  " @ " + str(datetime.datetime.now()))
            if reaction.message.author.mention not in scored_members:
                score_func("init", reaction.message.author.mention, -1)
            else:
                score_func("subtract", reaction.message.author.mention, 1)
        # Thumbs up is a +1
        elif reaction.emoji == "👍":
            if user == reaction.message.author:  # Can't +1 yourself here either
                pass
            else:
                print(user.display_name + " +1" + " to " + reaction.message.author.display_name +
                      " @ " + str(datetime.datetime.now()))
                if reaction.message.author.mention not in scored_members:
                    score_func("init", reaction.message.author.mention, 1)
                else:
                    score_func("add", reaction.message.author.mention, 1)
        else:
            return

    @commands.Cog.listener("on_reaction_remove")
    async def unthumbs(self, reaction, user):
        # Initialize user's score if needed
        if reaction.message.author.mention not in scored_members:
            score_func("init", reaction.message.author.mention, 0)
        # Thumbs down is a -1
        if reaction.emoji == "👎":
            print(user.display_name + " undid -1" + " to " + reaction.message.author.display_name +
                  " @ " + str(datetime.datetime.now()))
            score_func("add", reaction.message.author.mention, 1)
        # Thumbs up is a +1
        elif reaction.emoji == "👍":
            print(user.display_name + " undid +1" + " to " + reaction.message.author.display_name +
                  " @ " + str(datetime.datetime.now()))
            score_func("subtract", reaction.message.author.mention, 1)
        else:
            return

    @plus.error
    @minus.error
    async def on_score_change_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("Too quick, chuckle nuts!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Scores(bot), guild=discord.Object(id=bot.guilds[0].id))
