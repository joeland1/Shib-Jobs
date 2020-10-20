from discord.ext import commands

class WordFilter(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.banned_words=[]
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.Cog.listener()
    async def on_message(self, ctx):
        for banned_word in self.banned_words:
            if ctx.message.includes(" "+banned_word+" "):
                await ctx.message.delete()
                #add a logging


        print("check for ' word '  -> make sure that there are spaces")

    @commands.Cog.listener()
    async def on_ready(self):
        conn=sqlite3.connect(os.getcwd()+'\\lauch.db')
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM MOD_STUFF")
        data=cursor.fetchall()

        for word in data:
            self.banned_words.append(word)

def setup(bot):
    bot.add_cog(WordFilter(bot))
