import datetime
import typing
import discord
from discord.ext import commands, tasks
from discord import app_commands
import typing


class PollEmbed(discord.ui.Modal, title="Build-A-Poll: Embed Title & Description"):
    title_ = discord.ui.TextInput(label="Title:", style=discord.TextStyle.short, required=True)
    description = discord.ui.TextInput(label="Description:", style=discord.TextStyle.long, required=True)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()


class PollModal(discord.ui.Modal, title="Build-A-Poll: Choices"):
    # TextInputs to accept the lore title and description, both required
    # poll_prompt = discord.ui.TextInput(label="Poll Prompt:", style=discord.TextStyle.short, required=True)
    opt1 = discord.ui.TextInput(label="Option 1:", style=discord.TextStyle.short, required=True)
    opt2 = discord.ui.TextInput(label="Option 2:", style=discord.TextStyle.short, required=True)
    opt3 = discord.ui.TextInput(label="Option 3:", style=discord.TextStyle.short, required=False)
    opt4 = discord.ui.TextInput(label="Option 4:", style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # embed = discord.Embed(title=self.poll_prompt.value)
        # embed.add_field(name="First choice:", value=self.opt1, inline=False)
        # embed.add_field(name="Second choice:", value=self.opt2, inline=False)
        # if self.opt3.value != "":
        #     embed.add_field(name="Third choice:", value=self.opt3, inline=False)
        # if self.opt4.value != "":
        #     if self.opt3.value == "":
        #         embed.add_field(name="Third choice:", value=self.opt4, inline=False)
        #     else:
        #         embed.add_field(name="Fourth choice", value=self.opt4, inline=False)
        # await interaction.response.send_message(embed=embed)


# UI View
class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.title = None
        self.desc = None
        self.opt1 = None
        self.opt2 = None
        self.opt3 = None
        self.opt4 = None
        # self.value = ["", ""]
        self.timeout = 10  # View times out after 20 seconds

    def build_embed(self):
        embed = discord.Embed(title=self.title,
                              description=self.desc)
        embed.add_field(name="First choice:", value=self.opt1, inline=False)
        embed.add_field(name="Second choice:", value=self.opt2, inline=False)
        if self.opt3 != "":
            embed.add_field(name="Third choice:", value=self.opt3, inline=False)
        if self.opt4 != "":
            if self.opt3 == "":
                embed.add_field(name="Third choice:", value=self.opt4, inline=False)
            else:
                embed.add_field(name="Fourth choice", value=self.opt4, inline=False)
        return embed

    # Button to delete the lore from the record
    @discord.ui.button(label="Title & Description", style=discord.ButtonStyle.green, custom_id="title_desc")
    # All three arguments are required, function must pass self.view, interaction, self.item
    async def embed_setup(self, interaction: discord.Interaction, button: discord.Button):
        modal = PollEmbed()
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.title = modal.title_.value
        self.desc = modal.description.value

        await interaction.edit_original_message(embed=self.build_embed())

    @discord.ui.button(label="Choices", style=discord.ButtonStyle.blurple, custom_id="choices")
    async def choices(self, interaction: discord.Interaction, button: discord.Button):
        modal = PollModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.opt1 = modal.opt1.value
        self.opt2 = modal.opt2.value
        self.opt3 = modal.opt3.value
        self.opt4 = modal.opt4.value

        await interaction.edit_original_message(embed=self.build_embed())


class Poll(commands.Cog, name="Poll"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="poll",
                          description="Start a poll! Enter how long it should last and the options to pick from.")
    async def poll(self, interaction: discord.Interaction):
        view = Buttons()
        embed = discord.Embed(title="Build-A-Poll",
                              description="Use the buttons to build your poll!")
        await interaction.response.send_message("What your poll will look like:", embed=embed, view=view)
        await view.wait()


    # @tasks.loop()
    # async def test(self):
    #     print("E?")


async def setup(bot):
    await bot.add_cog(Poll(bot), guild=discord.Object(id=bot.guilds[0].id))
