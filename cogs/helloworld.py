from discord.ext import commands

class HelloWorld(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong! {0} ms'.format(round(self.bot.latency, 2)))

def setup(bot):
    bot.add_cog(HelloWorld(bot))
