from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks
import random
import datetime
import shelve


class Auto(commands.Cog, name="Auto"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.callout.start()
        self.score_reset.start()

    # Check every message that comes through and perform a hog-check
    @commands.Cog.listener("on_message")
    async def hog_check(self, message):
        # Do not reply to BB's own messages
        if message.author == self.bot.user:
            return

        # Reply to the secret word with 1/10 chance
        if 'hog' in message.clean_content.lower() and 1 == random.randint(1, 10):
            await message.channel.send('HYPEROMEGAHOGGERS')

    # Weekly Bad Score Callout Post
    # Publicly humiliate whoever has the lowest score with an automated post each Friday
    @tasks.loop(time=datetime.time(23, 0, 0))  # This represents 7:00 P.M. EST (11:00 P.M. UTC)
    async def callout(self):
        # If today is Friday (noted as 5 by isoweekday(), monday-sunday: 1-7), send the callout post
        if datetime.date.isoweekday(datetime.date.today()) == 5:
            callout_channel = 720833461329461347 if self.bot.user.name == "BotTest" else 743616007435976754
            # Sort the current user scores from highest to lowest
            plus_minus = shelve.open("plusMinus")
            score_sorted = sorted(plus_minus.items(), key=lambda x: x[1])
            plus_minus.close()

            # Send our fun little message letting our friend know they should try making better jokes
            callout_post = await self.bot.get_channel(callout_channel).send(
                "This is your weekly Bad Score Callout Post, a public "
                "service brought to you by Billager Bot. This week, " +
                str(score_sorted[0][0]) + " has the worst score so far. All "
                "the way down at a fat " + str(score_sorted[0][1]) + "!")
            # Derive the called out role by name
            # TODO: make this more robust later on
            callout_role = discord.utils.get(self.bot.get_guild(self.bot.guilds[0].id).roles, name="Called Out")
            # Apply the called out role to the user mentioned in the callout post
            await callout_post.mentions[0].add_roles(callout_role)
        else:
            return

    # Reset the scoreboard at midnight after the last callout post of the month
    @tasks.loop(time=datetime.time(4, 0, 0))
    async def score_reset(self):
        # Get the day of the month of the next friday
        next_friday = datetime.date.today() + datetime.timedelta(days=6)
        # If the loop runs on a Saturday (midnight following callout post on Friday evening,
        # and the next Friday's day is a lower number than yesterday's Friday,
        # then reset the scoreboard since that was the last friday of the month.
        if datetime.date.isoweekday(datetime.date.today()) == 6 and datetime.date.today().day - 1 > next_friday.day:
            plus_minus = shelve.open("plusMinus")
            plus_minus.clear()
            plus_minus.close()
        else:
            return


async def setup(bot):
    await bot.add_cog(Auto(bot), guild=discord.Object(id=bot.guilds[0].id))
