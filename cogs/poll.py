import datetime
import typing
import discord
from discord.ext import commands, tasks
from discord import app_commands
import typing


class PollModal(discord.ui.Modal, title="Build-A-Poll"):
    # TextInputs to accept the lore title and description, both required
    poll_prompt = discord.ui.TextInput(label="Poll Prompt:", style=discord.TextStyle.short, required=True)
    opt1 = discord.ui.TextInput(label="Option 1:", style=discord.TextStyle.short, required=True)
    opt2 = discord.ui.TextInput(label="Option 2:", style=discord.TextStyle.short, required=True)
    opt3 = discord.ui.TextInput(label="Option 3:", style=discord.TextStyle.short, required=False)
    opt4 = discord.ui.TextInput(label="Option 4:", style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.poll_prompt.value)
        embed.add_field(name="First choice:", value=self.opt1, inline=False)
        embed.add_field(name="Second choice:", value=self.opt2, inline=False)
        if self.opt3.value != "":
            embed.add_field(name="Third choice:", value=self.opt3, inline=False)
        if self.opt4.value != "":
            if self.opt3.value == "":
                embed.add_field(name="Third choice:", value=self.opt4, inline=False)
            else:
                embed.add_field(name="Fourth choice", value=self.opt4, inline=False)
        await interaction.response.send_message(embed=embed)


class Poll(commands.Cog, name="Poll"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="poll",
                          description="Start a poll! Enter how long it should last and the options to pick from.")
    async def poll(self, interaction: discord.Interaction):
        await interaction.response.send_modal(PollModal())

    # @tasks.loop()
    # async def test(self):
    #     print("E?")


async def setup(bot):
    await bot.add_cog(Poll(bot), guild=discord.Object(id=bot.guilds[0].id))
