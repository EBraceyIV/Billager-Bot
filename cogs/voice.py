import discord
from discord.ext import commands
import asyncio
from pathlib import Path

mp3s = ['honk', 'speech', 'short', 'pulp', 'navy']
vc = 0


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='vreset',
                      help="Run if Bbot won't make noise after being manually disconnected.")
    async def vreset(self, ctx):
        global vc
        vc = 0

    @commands.command(name='lines', help='A list of voice lines Billager knows.')
    async def lines(self, ctx):
        mp3_names = ''
        for mp3 in mp3s:
            mp3_names = mp3_names + mp3 + ', '
        await ctx.send('I know lots of fun words, such as: ' + mp3_names)

    @commands.command(name="join", help="Billager joins the voice chat.", pass_context=True)
    async def join(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel
            self.bot.voice_clients[0] = await voice_channel.connect()
        except AttributeError:
            await ctx.send('You get in the voice chat first.')

    @commands.command(name="speak", help="Billager will speak.", pass_context=True)
    async def speak(self, ctx, arg: str):
        global vc

        if not ctx.author.voice:
            await ctx.send('You get in the voice chat first.')
        if vc == 0:
            try:
                voice_channel = ctx.author.voice.channel
                vc = await voice_channel.connect()
            except Exception as e:
                print(e)
                print(type(e))
                await ctx.send("Something is wrong, please call for help.")

        if arg in mp3s:
            sound = arg + ".mp3"
            source = discord.FFmpegPCMAudio(Path.cwd() / 'mp3s' / sound)
            vc.play(source, after=None)
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
        else:
            await ctx.send('Try something else.')

    @commands.command(name="honk", help="Billager will do a little honk.")
    async def honk(self, ctx):
        global vc

        if not ctx.author.voice:
            await ctx.send('You get in the voice chat first.')
        if vc == 0:
            try:
                voice_channel = ctx.author.voice.channel
                vc = await voice_channel.connect()
            except Exception:
                await ctx.send("Something is wrong, please call for help.")

        source = discord.FFmpegPCMAudio(Path.cwd() / 'mp3s/honk.mp3')
        vc.play(source, after=None)
        while vc.is_playing():
            await asyncio.sleep(0.1)
        vc.stop()

    @commands.command(name="silence", help="Billager will leave the voice chat.")
    async def silence(self, ctx):
        global vc
        vc = 0
        await ctx.voice_client.disconnect()

    @speak.error
    async def speak_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('I\'m gonna need some context, buddy.\nSomething like, \'bb:speak honk\'')


def setup(bot):
    bot.add_cog(Voice(bot))
