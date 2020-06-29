from discord.ext import commands
import sqlite3
import os
import time
import random

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
            (GLOBAL_RANK   INTEGER PRIMARY KEY,
            USER_ID    INT    NOT NULL,
            LAST_MESSAGE_TIME    INT    NOT NULL,
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
        if ctx.author.bot is True:
            return
        #gotta do this part
    #@commands.command()
    #async def remove(self,ctx):


def modify_xp_value(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
    cursor=conn.cursor()

    #check to see if there are entries
    search_command= 'SELECT * FROM LEVELS WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    user_entries=len(cursor.fetchall())
    cursor.close()

    # update if there is 1 entry
    if user_entries == 1:
        updating_command='UPDATE LEVELS SET LAST_MESSAGE_TIME = ? XP = ? WHERE USER_ID = ?'
        updated_level = (int(time.time()), get_xp_value(discord_id)+random.randint(1,config.XP_INCRAMENT),discord_id)
        conn.execute(updating_command,updating_address)
        conn.commit()

    #add if no entires
    elif faucet_address_entries == 0:
        add_command = 'INSERT INTO LEVELS (USER_ID,LAST_MESSAGE_TIME,XP) VALUES (?,?,?)'
        input_data= (discord_id,)
        conn.execute(add_command,input_data)
        conn.commit()
    else:
        print("more than 1 entry somehow")
    conn.close()

def get_xp_value(discord_id):
    conn=sqlite3.connect(os.getcwd()+'faucet_info.db')
    cursor=conn.cursor()

    search_command= 'SELECT XP FROM LEVELS WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    xp = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return xp

def get_last_time(discord_id):
    conn=sqlite3.connect(os.getcwd()+'faucet_info.db')
    cursor=conn.cursor()

    search_command= 'SELECT LAST_MESSAGE_TIME FROM LEVELS WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    last_time = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return last_time


def setup(bot):
    bot.add_cog(Level_system(bot))
