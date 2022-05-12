import discord
from discord.ext import commands
import json


class More(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)

        # Load the channel to output to from the config
        with open("config.json") as config_json:
            config = json.load(config_json)
        # Extract just the id int from the channel call string (<#XXXXXX>)
        self.star_channel = int(config[self.GUILD]["star_channel"][2:-1])

    # Listen for reactions and perform the specified post when the threshold is passed
    @commands.Cog.listener("on_reaction_add")
    async def star(self, reaction, user):
        if reaction.message.channel == self.star_channel:
            return
        for react in reaction.message.reactions:
            if react.emoji == "⭐" and react.count == 3:  # Three star reacts are needed to cause a post
                embed = discord.Embed(description=reaction.message.content,
                                      color=0xffd926)
                embed.set_author(name=reaction.message.author.display_name,
                                 icon_url=reaction.message.author.avatar)
                embed.add_field(name="**Original**",
                                value="[Jump!](" + reaction.message.jump_url + ")")
                if reaction.message.attachments:
                    embed.set_image(url=reaction.message.attachments[0].url)
                    if len(reaction.message.attachments) > 1:
                        embed.set_footer(text="Plus " + str(len(reaction.message.attachments) - 1)
                                              + " other attachments.")
                embed.timestamp = reaction.message.created_at

                await self.bot.get_channel(self.star_channel).send(embed=embed)


async def setup(bot):
    await bot.add_cog(More(bot), guild=discord.Object(id=bot.guilds[0].id))
