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
# all_lore = list((map(lambda lore_title: lore_title.lower(), all_lore)))  # map each key to lowercase
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


class LoreTabs(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.page = 1
        self.timeout = 60
        self.response = None

    all_options = []
    for lore in all_lore:
        all_options.append(discord.SelectOption(label=lore_access("retrieve", lore, None).title))

    @discord.ui.select(placeholder="Pick your lore! 10 listed per page.", min_values=1, max_values=1, row=1,
                       custom_id="lore_dropdown", options=all_options[0:10])
    async def lore_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_message(embed=lore_access("retrieve", select.values[0].lower(), None))

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="◀", custom_id="left_button", row=2, disabled=True)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= 1
        self.lore_select.options = LoreTabs.all_options[(self.page - 1) * 10: self.page * 10]
        if self.page == 1:
            self.left.disabled = True
        if self.right.disabled:
            self.right.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="▶", custom_id="right_button", row=2)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        if self.page > 1:
            self.left.disabled = False
        self.lore_select.options = LoreTabs.all_options[(self.page - 1) * 10: self.page * 10]
        if len(self.lore_select.options) < 10:
            self.right.disabled = True
        await interaction.response.edit_message(view=self)

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        self.lore_select.placeholder = "Timed out."
        await self.response.edit(view=self)


# Use a modal to make lore entry more user friendly than typing everything in the message line as arguments
class AddLoreModal(discord.ui.Modal, title="Add Lore"):
    # TextInputs to accept the lore title and description, both required
    lore_title = discord.ui.TextInput(label="Lore Title:", style=discord.TextStyle.short,
                                      placeholder="What will you call the lore?", required=True)
    lore_desc = discord.ui.TextInput(label="Lore Description:", style=discord.TextStyle.long,
                                     placeholder="What IS the lore?", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        # Have to add .value to get string, otherwise uses TextInput object
        embed = embed_init(lore_title=self.lore_title.value, lore_desc=self.lore_desc.value)
        # The lore is stored as the type embed in the shelf file
        lore_access("add", self.lore_title.value.lower(), embed)
        await interaction.response.send_message(embed=embed)


class EditLoreModal(discord.ui.Modal, title="Edit Lore"):
    def __init__(self):
        super().__init__()
        self.embed = None

    edit_field = discord.ui.Select(options=[discord.SelectOption(label="Title", value="title"),
                                            discord.SelectOption(label="Description", value="desc"),
                                            discord.SelectOption(label="Number", value="num")],
                                   min_values=1, max_values=1,
                                   placeholder="Pick a field to edit!")

    edit_content = discord.ui.TextInput(label="Change above content for the lore:",
                                        style=discord.TextStyle.long,
                                        placeholder="Type Here!", required=True)

    # Update the label to include the lore title if it fits, for improved user experience
    def add_label(self):
        label = "Change above content for " + str(self.embed.title) + ":"
        # Labels longer than 45 characters throw an error, CommandInvoke because of HTTPException or something like that
        if len(label) > 45:
            pass
        else:
            self.edit_content.label = label

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed
        lore_title = embed.title
        if self.edit_field.values[0] == "title":
            embed.title = self.edit_content.value.rstrip('\n')
            lore_access("remove", lore_title.lower(), None)
            lore_access("add", embed.title.lower(), embed)
        elif self.edit_field.values[0] == "desc":
            embed.description = self.edit_content.value
            lore_access("edit", lore_title.lower(), embed)
        elif self.edit_field.values[0] == "num":
            # Validate that users have entered a valid number (int or float)
            try:
                edit_content = int(self.edit_content.value)
            except ValueError:
                try:
                    edit_content = float(self.edit_content.value)
                except ValueError:
                    await interaction.response.send_message(
                        "Since my brain is a computer, it'll help if you make that a number instead.")
                    return
                else:
                    # Assign the manual ID number to the lore
                    embed.set_author(name="Lore Nugget #" + str(edit_content))
                    lore_access("edit", lore_title.lower(), embed)
            else:
                # Assign the manual ID number to the lore
                embed.set_author(name="Lore Nugget #" + str(edit_content))
                lore_access("edit", lore_title.lower(), embed)
        await interaction.response.send_message(embed=embed)


class Lore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Display the requested piece of lore, or a random piece if none is specified
    @app_commands.command(name='lore', description="View some enjoyable server lore.")
    async def lore(self, interaction: discord.Interaction): #, *, lore_title: typing.Optional[str]):
        # lore_title = random.choice(all_lore) if lore_title is None else lore_title.lower()
        # if lore_title not in all_lore:
        #     await interaction.response.send_message(
        #         "You must be from a different timeline (or really bad at spelling) because we don't have "
        #         "that lore on record.")
        #     return
        # embed = lore_access("retrieve", lore_title, None)
        # await interaction.response.send_message(embed=embed)
        view = LoreTabs()
        await interaction.response.send_message(view=view)
        view.response = await interaction.original_message()
        await view.wait()

    # Display a list of all lore currently stored
    @app_commands.command(name="lore_board", description="See a list of all available lore.")
    async def lore_board(self, interaction: discord.Interaction):
        # Initialize the embed
        embed = discord.Embed(title="Billager's Lore Compository", color=0x7289da)
        embed.set_footer(text="More Lore? Tell BBot what needs to be remembered.")
        # To iterate on the description for the embed, start as a normal string
        description = "Here you can see the full archive of all lore currently on record.\n" \
                      "Use `/lore <lore title>` to read more about any entry.\n\n" \
                      "------------------------------\n\n"
        # Then add each lore by title to the description
        for lore_title in all_lore:
            description = description + "> " + lore_access("retrieve", lore_title, None).title + "\n"
        embed.description = description
        await interaction.response.send_message(embed=embed)

    # Add a new piece of lore to the records
    @app_commands.command(name="add_lore",
                          description="Add a new piece of lore to the records. Title and then description.")
    async def add_lore(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddLoreModal())

    @app_commands.command(name="edit_lore",
                          description="Edit a piece of lore on the records.")
    async def edit_lore(self, interaction: discord.Interaction, lore_title: str):
        if lore_title.lower() not in all_lore:
            await interaction.response.send_message("Can't find that lore!")
            return
        # Load the embed object once we know it exists so it can be edited
        embed = lore_access("retrieve", lore_title.lower(), None)

        # Bring up edit modal and send response
        edit_modal = EditLoreModal()
        edit_modal.embed = embed
        edit_modal.add_label()
        await interaction.response.send_modal(edit_modal)

    # Remove a piece of lore from the records
    @app_commands.command(name="kill_lore", description="Remove a piece of lore from the records.")
    async def kill_lore(self, interaction: discord.Interaction, lore_title: str):
        view = Confirm()
        # Check to see if the lore exists
        if lore_title.lower() not in all_lore:
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
            lore_access("remove", lore_title.lower(), None)
            await interaction.edit_original_message(content="The deed is done.", view=None)
        else:
            await interaction.edit_original_message(content="LAME", view=None)

    # # AUTOCOM LIST ONLY SUPPORTS UP TO 25 ENTRIES
    # # SO THIS MAY NEED TO BE REMOVED OR FIXED WITH A WEIRD WORKAROUND
    # # Consider breaking total number into sets of 25 and navigate "pages" using UI kit buttons
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
