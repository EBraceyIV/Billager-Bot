import datetime
import random
import discord
from discord.ext import commands
from discord import app_commands
import shelve
import typing
# TODO: Fix lore_title references to be case insensitive

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
#   lore_content: The description / content of the lore entry
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


# UI View to display buttons for the kill_lore command
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = 10  # View times out after 10 seconds

    # Button to delete the lore from the record
    @discord.ui.button(style=discord.ButtonStyle.red, emoji="🗑")
    # All three arguments are required, function must pass self.view, interaction, self.item
    async def kill(self, interaction: discord.Interaction, button: discord.Button):
        self.value = True
        self.stop()

    # Button to cancel the lore delete request
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    # All three arguments are required, function must pass self.view, interaction, self.item
    async def cancel(self, interaction: discord.Interaction, button: discord.Button):
        self.value = False
        self.stop()


class Lore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Display the requested piece of lore, or a random piece if none is specified
    @app_commands.command(name='lore', description="View some enjoyable server lore.")
    async def lore(self, interaction: discord.Interaction, *, lore_title: typing.Optional[str]):
        lore_title = random.choice(all_lore) if lore_title is None else lore_title
        if lore_title not in all_lore:
            await interaction.response.send_message(
                "You must be from a different timeline (or really bad at spelling) because we don't have "
                "that lore on record.")
            return
        embed = lore_access("retrieve", lore_title, None)
        await interaction.response.send_message(embed=embed)

    # Display a list of all lore currently stored
    @app_commands.command(name="lore_list", description="See a list of all available lore.")
    async def lore_list(self, interaction: discord.Interaction):
        # Initialize the embed
        embed = discord.Embed(title="Billager's Lore Compository", color=0x7289da)
        embed.set_footer(text="More Lore? Tell BBot what needs to be remembered.")
        # To iterate on the description for the embed, start as a normal string
        description = "Here you can see the full archive of all lore currently on record.\n" \
                      "Use `/lore <lore title>` to read more about any entry.\n\n" \
                      "------------------------------\n\n"
        # Then add each lore by title to the description
        for lore_title in all_lore:
            description = description + "> " + lore_title + "\n"
        embed.description = description
        await interaction.response.send_message(embed=embed)

    # Add a new piece of lore to the records
    @app_commands.command(name="add_lore",
                          description="Add a new piece of lore to the records. Title and then description.")
    async def add_lore(self, interaction: discord.Interaction, lore_title: str, *, lore_description: str):
        # Pass the relevant info to the embed builder
        embed = embed_init(lore_title, lore_description)
        # The lore is stored as the type embed in the shelf file
        lore_access("add", lore_title, embed)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="edit_lore",
                          description="Edit a piece of lore on the records.")
    async def edit_lore(self, interaction: discord.Interaction,
                        lore_title: str,
                        edit_field: typing.Literal["title", "content", "number"],
                        edit_content: str):
        if lore_title not in all_lore:
            await interaction.response.send_message("Can't find that lore!")
            return
        # Load the embed object once we know it exists so it can be edited
        embed = lore_access("retrieve", lore_title, None)

        if edit_field.lower() == "title":
            # Assign the edited embed to a new entry in lore_list and remove the old one
            # Easiest way I could conjure of replacing the key of a shelve entry
            embed.title = edit_content
            lore_access("remove", lore_title, None)
            lore_access("add", edit_content, embed)
        elif edit_field.lower() == "content":
            # Reassign the content and reassign the value to the key
            embed.description = edit_content
            lore_access("edit", lore_title, embed)
        elif edit_field.lower() == "number":
            # Validate that users have entered a valid number (int or float)
            try:
                edit_content = int(edit_content)
            except ValueError:
                try:
                    edit_content = float(edit_content)
                except ValueError:
                    await interaction.response.send_message(
                        "Since my brain is a computer, it'll help if you make that a number instead.")
                    return
                else:
                    # Assign the manual ID number to the lore
                    embed.set_author(name="Lore Nugget #" + str(edit_content))
                    lore_access("edit", lore_title, embed)
            else:
                # Assign the manual ID number to the lore
                embed.set_author(name="Lore Nugget #" + str(edit_content))
                lore_access("edit", lore_title, embed)
        else:
            await interaction.response.send_message("That's not an editable field for the lore.")
            return

        await interaction.response.send_message(embed=embed)

    # Remove a piece of lore from the records
    @app_commands.command(name="kill_lore", description="Remove a piece of lore from the records.")
    async def kill_lore(self, interaction: discord.Interaction, lore_title: str):
        view = Confirm()
        # Check to see if the lore exists
        if lore_title not in all_lore:
            await interaction.response.send_message("Can't find that lore!")
            return

        # Ask for confirmation to delete the lore, confirmation/cancel buttons used to decide
        await interaction.response.send_message("Are you sure you want to destroy the \"" + lore_title +
                                                "\" lore? Click 🗑 to confirm.", view=view)

        # Wait for a response from the UI view, button click or timeout
        await view.wait()

        # Replace original response to command with the relevant result
        if view.value is None:
            await interaction.edit_original_message(content="Too late! Next time, be ready to pull the trigger.",
                                                    view=None)
        elif view.value:
            lore_access("remove", lore_title, None)
            await interaction.edit_original_message(content="The deed is done.", view=None)
        else:
            await interaction.edit_original_message(content="LAME", view=None)

    # # AUTOCOM LIST ONLY SUPPORTS UP TO 25 ENTRIES
    # # SO THIS MAY NEED TO BE REMOVED OR FIXED WITH A WEIRD WORKAROUND
    # @lore.autocomplete("lore_title")
    # @edit_lore.autocomplete("lore_title")
    # async def lore_title_autocomplete(self,
    #                                   interaction: discord.Interaction,
    #                                   current: str) -> list[app_commands.Choice[str]]:
    #     lore_titles = all_lore
    #     return [app_commands.Choice(name=lore_title, value=lore_title)
    #             for lore_title in lore_titles if current.lower() in lore_title.lower()]


async def setup(bot):
    await bot.add_cog(Lore(bot), guild=discord.Object(id=bot.guilds[0].id))
