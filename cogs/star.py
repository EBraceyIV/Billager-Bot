import discord
import datetime
from discord.ext import commands
import json

with open("config.json") as config_json:
    config = json.load(config_json)
star_channel = config["star_channel"]


class Star(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener("on_reaction_add")
    async def star(self, reaction, user):
        for react in reaction.message.reactions:
            if react.emoji == "⭐":
                embed = discord.Embed(title=reaction.message.author.display_name,
                                      description=reaction.message.content)
                embed.add_field(name="**Original**",
                                value="[Jump!](" + reaction.message.jump_url + ")")
                # embed.timestamp = datetime.datetime.day

                # print("CHECK " + str(react.count))
                # await discord.Message.pin(reaction.message)
                await reaction.message.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Star(bot), guild=discord.Object(id=bot.guilds[0].id))
