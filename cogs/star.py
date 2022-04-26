import discord
from discord.ext import commands
import json


class Star(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)

        with open("config.json") as config_json:
            config = json.load(config_json)
        self.star_channel = int(config[self.GUILD]["star_channel"][2:-1])

    @commands.Cog.listener("on_reaction_add")
    async def star(self, reaction, user):
        for react in reaction.message.reactions:
            if react.emoji == "⭐":
                embed = discord.Embed(description=reaction.message.content,
                                      color=0xffd926)
                embed.set_author(name=reaction.message.author.display_name,
                                 icon_url=reaction.message.author.avatar)
                embed.add_field(name="**Original**",
                                value="[Jump!](" + reaction.message.jump_url + ")")
                embed.timestamp = reaction.message.created_at

                await self.bot.get_channel(self.star_channel).send(embed=embed)


async def setup(bot):
    await bot.add_cog(Star(bot), guild=discord.Object(id=bot.guilds[0].id))
