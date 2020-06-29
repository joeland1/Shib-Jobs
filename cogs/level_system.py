from discord.ext import commands

class Level_system(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def rank(self, ctx):
        print("here is ranks")

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
            conn.execute('''CREATE TABLE LEVELS
            (ROW_ID   INTEGER PRIMARY KEY,
            USER_ID    INT    NOT NULL,
            LAST_MESSAGE    INT    NOT NULL,
            XP    INT    NOT NULL);''')
            conn.commit()
            conn.close()

            print("created a new rank_recording table")

        except sqlite3.OperationalError:
            print("old table found for levels -> using old db")
            print("if you want to use a new one, delete rank_recording.db")
            conn.close()
        #level up algo: x^2+10-> will determine level rank for level "x" so level 0 requires 10 pts before getting to lv 1

    @commands.Cog.listener()
    async def on_message(self,ctx):
        if ctx.author.bot == True:
            return
        #gotta do this part

def setup(bot):
    bot.add_cog(Level_system(bot))
