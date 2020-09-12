from discord.ext import commands

class Stream(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def watch(self, ctx):
        watched_show = ctx.content.replace(config.PREFIX+"watch", "")
        print(watched_show)

def setup(bot):
    bot.add_cog(Stream(bot))
