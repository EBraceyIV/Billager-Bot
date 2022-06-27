import typing
import discord
from discord.ext import commands
from discord import app_commands
import json


class Config(commands.Cog, name="Config"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.GUILD = str(bot.guilds[0].id)

        # If the config file cannot be found, generate a new blank one.
        try:
            with open("config.json") as config_json:
                config_json = json.load(config_json)
        except FileNotFoundError:
            with open("config.json", "w") as config_json:
                json.dump({self.GUILD: {"test": "",
                                        "star_channel": "",
                                        "callout_channel": "",
                                        "poll_channel": ""}}, config_json)

    # Set the config setting for various BBot actions, such as the channel certain messages are sent to.
    @app_commands.command(name="set_config", description="Set one of BBot's configurations.")
    @app_commands.describe(config="The bot config setting to define.")
    @app_commands.describe(value="The channel to set the config for.")
    async def set_config(self, interaction: discord.Interaction,
                         config: typing.Literal["test", "star_channel", "callout_channel", "poll_channel"],
                         value: str):

        # Start by loading the config json as a dictionary
        with open("config.json") as config_json:
            config_json = json.load(config_json)

        # Set the chosen config value to that specified
        config_json[self.GUILD][config] = value

        # Write the updated dictionary to the json file
        with open("config.json", "w") as new_config:
            json.dump(config_json, new_config)

        # Send message to confirm the config has been updated
        await interaction.response.send_message("Config for `" + config + "` set to " + value)

        # Reload relevant cog for changed config to implement change immediately
        if config == "star_channel":
            await self.bot.reload_extension("cogs.more")
            print("Reloaded cog: more.py")
        elif config == "callout_channel":
            await self.bot.reload_extension("cogs.auto")
            print("Reloaded cog: auto.py")
        elif config == "poll_channel":
            await self.bot.reload_extension("cogs.poll")
            print("Reloaded cog: poll.py")


async def setup(bot):
    await bot.add_cog(Config(bot), guild=discord.Object(id=bot.guilds[0].id))
