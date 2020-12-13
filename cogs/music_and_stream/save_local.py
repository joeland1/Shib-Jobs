from discord.ext import commands

class Save_local(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

        #self.rpc_client.play()
                #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def save(self, ctx, arg1=None):
        if arg1 is None:
            print("missing a source")

def setup(bot):
    bot.add_cog(Save_local(bot))
