import datetime
import random
import discord
from discord.ext import commands
from discord import app_commands
import shelve
import typing

# lore_keeper stores all of the discord.Embed objects for read/write
lore_list = shelve.open("loreKeeper")
all_lore = list(lore_list.keys())
lore_list.close()


# Lore management function
#   action: Add to or remove from lore record, or retrieve a lore entry to alter/display
#   member: Which lore entry to manage
#   embed: The discord.Embed content for the designated lore entry
def lore_access(action, lore_title_, embed_):
    global all_lore
    lore_keeper = shelve.open("loreKeeper")
    if action == "add":
        lore_keeper[lore_title_] = embed_
    elif action == "remove":
        del lore_keeper[lore_title_]
    elif action == "edit":
        lore_access("remove", lore_title_, None)
        lore_access("add", lore_title_, embed_)
    elif action == "retrieve":
        embed = lore_keeper[lore_title_]
        return embed
    all_lore = list(lore_keeper.keys())
    lore_keeper.close()


# Embed constructor to clear up code
#   lore_title: The name of the lore entry
#   lore_desc: The description / content of the lore entry
def embed_init(lore_title, lore_desc):
    # embed is the object that contains all the lore info, can be edited easily as an object
    embed = discord.Embed(title=lore_title,
                          description=lore_desc,
                          color=0x7289da)
    # Generate date the lore was added to add to footer
    date = datetime.date.today()
    # A randomly chosen number is given to the lore entry for show on construction
    embed.set_author(name="Lore Nugget #" + str(random.randint(1000, 9999)))
    embed.set_footer(text="Lore added: " + str(date) + "\n"
                          "More Lore? Tell BBot what needs to be remembered.")
    return embed


class Lore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Display the requested piece of lore, or a random piece if none is specified
    @commands.command(name='lore', description="View some enjoyable server lore.",
                      help="This is for lore reading.")
    async def lore(self, interaction: discord.Interaction, *, lore_title: typing.Optional[str]):
        lore_title = random.choice(all_lore) if lore_title is None else lore_title
        if lore_title not in all_lore:
            await interaction.response.send_message(
                "You must be from a different timeline (or really bad at spelling) because we don't have "
                "that lore on record.")
            return
        embed = lore_access("retrieve", lore_title, None)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Lore(bot), guild=discord.Object(id=627279552481067030))
