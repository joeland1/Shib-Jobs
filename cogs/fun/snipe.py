from discord.ext import commands
import sqlite3

class Snipe(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.deleted_messages=None
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def snipe(self, ctx):
        print()

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        self.deleted_messages.append([ctx.author.id, ctx.content])

def setup(bot):
    bot.add_cog(Snipe(bot))
