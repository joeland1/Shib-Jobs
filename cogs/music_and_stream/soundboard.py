from discord.ext import commands
import youtube_dlc as youtube_dl2

class Soundboard(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

        #self.rpc_client.play()
                #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def save(self, ctx, arg1=None):
        if arg1 is None and :
            print("missing a source")
            return




def setup(bot):
    bot.add_cog(Soundboard(bot))
