from discord.ext import commands

class MusicCog(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def music(self, ctx, arg1=None):
        if arg1 == '':
            await play(self,ctx)
        elif arg1 == 'pause':
            await pause(self,ctx)
        elif arg1 == 'resume':
            await resume(self,ctx)
        elif arg1 in ['disconnect','dc']:
            await disconnect(self,ctx)

    async def play(self, ctx):
        print("play livestream")
    async def pause(self, ctx):
        print("play livestream")
    async def resume(self, ctx):
        print("play livestream")
    async def disconnect(self, ctx):
        print("play livestream")

def setup(bot):
    bot.add_cog(MusicCog(bot))
