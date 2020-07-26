from discord.ext import commands

class FAQ(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def set_faq(self, ctx):
        faq_data = ctx.message.content.replace(self.bot.command_prefix+"set_faq ", "").split("|")
        for x in faq_data:
            print(x)

        embed=discord.Embed(title="FAQ",color=discord.Color.from_rgb(193,151,79))

    @commands.command()
    async def add_faq(self,ctx):
        print("add q+a to faq")

    @commands.command()
    async def remove_faq(self,ctx,arg1=None):
        print("removing question # arg1")

        if arg1 is None:
            ctx.channel.send("You need to specify which question you want removed")

def setup(bot):
    bot.add_cog(FAQ(bot))
