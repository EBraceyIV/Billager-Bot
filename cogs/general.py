import discord
from discord.ext import commands
from discord import app_commands
import random
from mcstatus import JavaServer

# Define emotes
dwayneBlock = '<:dwayneBlock:578999476824440852>'
depression = '<:depression:605507923619086349>'
billagermine = '<:billagermine:679882568740503648>'
beefBrain = '<:BeefBrain:631694337549271050>'
hellHog_RAGE = '<:hellHog_RAGE:610668471520460817>'
WillBrain = '<:WillBrain:688918968785829894>'
ZBillagerChop = '<a:ZBillagerChop:619169326829928449>'
monkaGun = '<:monkaGun:650922885627772949>'
fortCry = '<:fortCry:600190388241694770>'

# mcstatus init
server = JavaServer.lookup("51.81.206.215:25589")  # my minecraft server


class General(commands.Cog, name="General"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # # This currently serves no real purpose. Just learning the channels and utils functionality.
    # @commands.command(name='channels', help='Dev only, does nothing (that you can see).', hidden=True)
    # async def channels(self, ctx):
    #     # All channels in the guild
    #     for channel in ctx.guild.channels:
    #         print(channel)
    #     # Display id of specific channel, given the name in the guild
    #     ct = discord.utils.get(ctx.guild.text_channels, name="command-terminal")
    #     print(str(ct.id) + ' ' + ct.name + ' ' + ct.topic)

    # An early test reply command with an Animal Crossing twist
    @app_commands.command(name='nook', description='That two-bit Tanooki.')
    async def nook(self, interaction: discord.Interaction):
        response = "I will send Kicks to break Tom Nook's kneecaps."
        await interaction.response.send_message(response)

    # Basic send a message command
    @app_commands.command(name='watch', description='He likes to watch.')
    async def watch(self, interaction: discord.Interaction):
        response = 'I like to watch.'
        await interaction.response.send_message(response)

    # Randomly picks a Will-thing to say
    @app_commands.command(name='will', description='Will Simulator')
    async def will(self, interaction: discord.Interaction):
        willReplies = ["pepehands " + depression,
                       "oh yeah?",
                       "die in a fire " + hellHog_RAGE,
                       "smile",
                       "i've got a galaxy brain idea " + WillBrain,
                       "**NO ANIME** " + ZBillagerChop,
                       "?????????????",
                       "oh, i see",
                       "you know what? i'll take it",
                       "and **LIE**",
                       "c!play surf rock anthology volume 1",
                       "c!play sounds of the supermarket",
                       "c!play a girl worth fighting for",
                       "c!play yankee doodle swag remix",
                       monkaGun,
                       "GET IN THE CAR HORATIO",
                       "I can't believe this",
                       "you wanna win",
                       "i'm so tired bro",
                       "secretly i'm vulnerable and that's why i'm aggressive " + fortCry,
                       "Please bro",
                       "I went to Wendy’s",
                       "I went to Steak & Shake",
                       "PLEASE",
                       "And uh",
                       "*one of those wacky purple emotes*",
                       "YES",
                       "HOG",
                       "it's time to end this",
                       "Never say that to me ever again",
                       "Gachi",
                       "NICE BOAT",
                       "I bought more shoes",
                       "Dunston checks in",
                       "I cannot believe you",
                       "I will remember this",
                       "I don't remember the touch of a woman " + fortCry,
                       "you're gonna lose your JOB",
                       "doodoo ass",
                       "no ball shaming allowed",
                       "show me balls, Steve!",
                       "No, I'm Will"]
        response = random.choice(willReplies)
        await interaction.response.send_message(response)

    # Basic reply using an emote id
    @app_commands.command(name="dwayne", description='Dwayne himself')
    async def block(self, interaction: discord.Interaction):
        response = '<:dwayneBlock:578999476824440852>'
        await interaction.response.send_message(response)

    # Provides current player count and latency to the Minecraft server
    @app_commands.command(name="blocks", description='Minecraft Server Info')
    async def blocks(self, interaction: discord.Interaction):
        try:
            # Get all of the server information
            status = server.status()
        except Exception:
            await interaction.response.send_message("Server is down :(")
            return

        # Build the embed message using the server query
        embed = discord.Embed(title='Dwayneblock Memorial Minecraft Server',
                              color=0xdd3333,
                              description='{0} Come play with blocks at {1}:{2}\n'
                              .format(dwayneBlock, server.host, server.port))
        embed.add_field(name='Players Online:', value=status.players.online)
        embed.add_field(name='Latency:', value=str(status.latency) + ' ms')
        embed.add_field(name='Game Version:', value=status.version.name)
        # embed.add_field(name="Modpack", value="The 1.12.2 Pack, v. 1.3.4")
        embed.set_footer(text='This server is hosted in the USA by Shockbyte.')
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot), guild=discord.Object(id=bot.guilds[0].id))
