from discord.ext import commands

class WordFilter(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.banned_words=[]
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.Cog.listener()
    async def on_message(self, ctx):
        for banned_word in self.banned_words:
            if (" "+banned_word+" ") in ctx.message.content:
                await ctx.message.delete()
                #add a logging portion?

    @commands.Cog.listener()
    async def on_ready(self):
        conn=sqlite3.connect(os.getcwd()+'\\lauch.db')
        cursor=conn.cursor()

        cursor.execute("SELECT word_filter FROM MOD_STUFF")

        enabled=cursor.fetchone()
        if data == 2
            words = cursor.execute("SELECT * FROM BANNED_WORDS")
            for word in words:
                self.banned_words.append(word)

def setup(bot):
    bot.add_cog(WordFilter(bot))
