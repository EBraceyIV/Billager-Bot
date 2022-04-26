import typing

import discord
from discord.ext import commands
from discord import app_commands
import json


class Config(commands.Cog, name="Config"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)

    @app_commands.command(name="set_config", description="Set one of BBot's configurations.")
    @app_commands.describe(config="The bot config setting to define.")
    @app_commands.describe(value="The channel to set the config for.")
    async def set_config(self, interaction: discord.Interaction,
                         config: typing.Literal["test", "star_channel", "callout_channel"],
                         value: str):

        try:
            with open("config.json") as config_json:
                config_json = json.load(config_json)
        except FileNotFoundError:
            with open("config.json", "w") as config_json:
                json.dump({self.GUILD: {"test": "", "star_channel": "", "callout_channel": ""}}, config_json)
            with open("config.json") as config_json:
                config_json = json.load(config_json)

        try:
            config_json[self.GUILD][config] = value
        except KeyError:
            config_json[self.GUILD] = {"test": "", "star_channel": "", "callout_channel": ""}
            config_json[self.GUILD][config] = value

        with open("config.json", "w") as outfile:
            json.dump(config_json, outfile)

        await interaction.response.send_message("Config for `" + config + "` set to " + value)


async def setup(bot):
    await bot.add_cog(Config(bot), guild=discord.Object(id=bot.guilds[0].id))
