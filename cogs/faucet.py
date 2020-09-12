from discord.ext import commands
import crypto_perams
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

import discord

import sqlite3
import os
import global_functions

from captcha.image import ImageCaptcha #for captcha

import time
import random

import asyncio

from io import BytesIO

class Faucet(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def register(self,ctx, arg1=None):
        if arg1 is None:
            await ctx.channel.send("You need to register a "+crypto_perams.CRYPTO_TICKER+" address")
            return

        rpc_connection_CRYPTO = 'http://{0}:{1}@{2}:{3}'.format(crypto_perams.CRYPTO_RPC_USER, crypto_perams.CRYPTO_RPC_PW, crypto_perams.CRYPTO_RPC_IP, crypto_perams.CRYPTO_RPC_PORT)
        wallet = AuthServiceProxy(rpc_connection_CRYPTO)

        if wallet.validateaddress(arg1)["isvalid"] is False:
            await ctx.channel.send("["+arg1+"] is not a valid address")
            return

        modify_db_address(ctx.author.id,arg1)

    #sets up address db for faucet along with a db for captcha recording
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
            conn.execute('''CREATE TABLE FAUCET_ADDRESSES
            (ROW_ID   INTEGER PRIMARY KEY,
            USER_ID    INT    NOT NULL,
            TIME    INT    NOT NULL,
            BALANCE    REAL    NOT NULL,
            ADDRESS    CHAR(50)    NOT NULL);''')
            conn.commit()
            conn.close()

            print("created a new faucet_address table")

        except sqlite3.OperationalError:
            print("old table found for faucet addresses -> using old db")
            print("if you want to use a new one, delete faucet_info.db")
            conn.close()

    #remove when done or add mod
    @commands.command()
    async def print_out(self,ctx):
        if global_functions.checkmodrole(ctx) is True:
            print("is admin")
            conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
            cursor=conn.cursor()

            print("getting data")
            all_data=cursor.execute("SELECT * FROM FAUCET_ADDRESSES")

            for data in all_data:
                print(data)

            cursor.close()
            conn.close()
        else:
            print(ctx.author.name+" tried to print out a faucet table")

    @commands.command()
    async def withdraw(self,ctx,amount=None):
        #everything is done in seconds here
        conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
        cursor=conn.cursor()

        search_command= 'SELECT * FROM FAUCET_ADDRESSES WHERE USER_ID = ?'
        cursor.execute(search_command,(ctx.author.id,))

        user_entry = cursor.fetchone()
        if user_entry is None:
            print("register first")
            cursor.close()
            conn.close()
            return
            
        cursor.close()
        conn.close()

        # has [row,discord_id,last time redeemed,balance,address]

        answer = await generate_captcha(ctx.author)
        print(answer)

        user_captcha_response= await get_response(self,ctx)
        if user_captcha_response is False:
            return
        else:
            if str(answer) == str(user_captcha_response.replace(" ","").replace("\n","")):
                async with ctx.author.typing():
                    confirmation_message = await ctx.author.send("Catcha is correct... attempting to withdraw now")

                    if amount is not None and global_functions.is_a_number(amount) is False:
                        await ctx.author.send("You have inputed an invalid amount")
                        return

                    current_balance=get_db_balance(ctx.author.id)
                    to_address=get_db_address(ctx.author.id)
                    print("balance="+str(current_balance))
                    print("to_address="+to_address)

                    if amount is None:
                        if(current_balance < crypto_perams.FAUCET_MIN_WITHDRAW):
                            print("you need to be above minimum withdraw balance")
                            return

                        print("sending whole balance")
                        rpc_connection_CRYPTO = 'http://{0}:{1}@{2}:{3}'.format(crypto_perams.CRYPTO_RPC_USER, crypto_perams.CRYPTO_RPC_PW, crypto_perams.CRYPTO_RPC_IP, crypto_perams.CRYPTO_RPC_PORT)
                        wallet = AuthServiceProxy(rpc_connection_CRYPTO)
                        txid = wallet.sendfrom(crypto_perams.FAUCET_SOURCE,to_address, current_balance)
                        await confirmation_message.edit(content=txid)

                        modify_db_balance(ctx.author.id, -1*current_balance)

                    elif global_functions.is_a_number(amount) is True:
                        amount=float(amount)
                        if(amount < crypto_perams.FAUCET_MIN_WITHDRAW):
                            print("you need to be above minimum withdraw balance")
                            return

                        if(amount > current_balance):
                            print("amount is larger than current withdrawable balance")
                            return

                        rpc_connection_CRYPTO = 'http://{0}:{1}@{2}:{3}'.format(crypto_perams.CRYPTO_RPC_USER, crypto_perams.CRYPTO_RPC_PW, crypto_perams.CRYPTO_RPC_IP, crypto_perams.CRYPTO_RPC_PORT)
                        wallet = AuthServiceProxy(rpc_connection_CRYPTO)
                        txid = wallet.sendfrom(crypto_perams.FAUCET_SOURCE,to_address, amount)
                        await confirmation_message.edit(content=txid)

                        modify_db_balance(ctx.author.id, -1*amount)

            else:
                await ctx.author.send("The catchpa is incorrect, please run the command again")
                return

    @commands.command()
    async def claim(self,ctx):
        conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
        cursor=conn.cursor()

        search_command= 'SELECT * FROM FAUCET_ADDRESSES WHERE USER_ID = ?'
        cursor.execute(search_command,(ctx.author.id,))

        user_entry = cursor.fetchone()
        if user_entry is None:
            print("register first")
            return

        last_claimed_time = get_db_time(ctx.author.id)
        current_time = int(time.time())

        if current_time - last_claimed_time <= crypto_perams.FAUCET_TIME_DELAY:
            await ctx.channel.send("You are still too early")
            return

        captcha_answer = await generate_captcha(ctx.author)

        user_captcha_response= await get_response(self,ctx)

        if user_captcha_response == False:
            await ctx.channel.send("You did not reply in time")
            return
        elif str(user_captcha_response)==str(captcha_answer):
            modify_db_balance(ctx.author.id,crypto_perams.FAUCET_REWARD)
            print("balance addded")




#can be used to modify address and set up entry
def modify_db_address(discord_id,crypto_address):
    conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
    cursor=conn.cursor()

    #check to see if there are entries
    search_command= 'SELECT * FROM FAUCET_ADDRESSES WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    faucet_address_entries=len(cursor.fetchall())
    cursor.close()

    # update if there is 1 entry
    if faucet_address_entries == 1:
        updating_command='UPDATE FAUCET_ADDRESSES SET ADDRESS = ? WHERE USER_ID = ?'
        updating_address = (crypto_address,discord_id)
        conn.execute(updating_command,updating_address)
        conn.commit()

    #add if no entires
    elif faucet_address_entries == 0:
        add_command = 'INSERT INTO FAUCET_ADDRESSES (USER_ID,ADDRESS,TIME,BALANCE) VALUES (?,?,?,?)'
        input_data= (discord_id,crypto_address,0,0)
        conn.execute(add_command,input_data)
        conn.commit()
    else:
        print("more than 1 entry somehow")
    conn.close()

    print("registered")

def modify_db_balance(discord_id,amount_to_add):
    conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
    cursor=conn.cursor()

    add_command = 'UPDATE FAUCET_ADDRESSES SET BALANCE = ? WHERE USER_ID = ?'

    current_balance=get_db_balance(discord_id)
    conn.execute(add_command,(current_balance+amount_to_add,discord_id))
    conn.commit()


    cursor.close()
    conn.close()

def modify_db_time(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
    cursor=conn.cursor()

    add_command = 'UPDATE FAUCET_ADDRESSES SET TIME = ? WHERE USER_ID = ?'

    current_time=int(time.time())
    conn.execute(add_command,current_time)
    conn.commit()

    cursor.close()
    conn.close()

def get_db_balance(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
    cursor=conn.cursor()

    search_command= 'SELECT * FROM FAUCET_ADDRESSES WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    balance = cursor.fetchone()[3]

    cursor.close()
    conn.close()

    return balance

def get_db_address(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
    cursor=conn.cursor()

    search_command= 'SELECT * FROM FAUCET_ADDRESSES WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    addie = cursor.fetchone()[4]

    cursor.close()
    conn.close()

    return addie

def get_db_time(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\faucet_info.db')
    cursor=conn.cursor()

    search_command= 'SELECT * FROM FAUCET_ADDRESSES WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    unix_time = cursor.fetchone()[2]

    cursor.close()
    conn.close()

    return unix_time

async def generate_captcha(user):
    letters = "0123456789abcdefghijklmnopqrstuvwxyz?!()@"
    captcha_answer=''.join(random.choice(letters) for i in range(crypto_perams.FAUCET_CAPTCHALENGTH))

    image_captcha = ImageCaptcha()

    captcha_image_file_name = os.getcwd()+"\\faucet_images\\"+str(user.id)+"_captcha_image.png"
    image = image_captcha.generate_image(captcha_answer)



    arr=BytesIO()
    image.save(arr, format='png',optimize=True)
    arr.seek(0)

    await user.send(file=discord.File(arr, "captcha.png"))

    return captcha_answer

async def get_response(self,ctx):
    def check(message):
        return message.guild is None and message.author.id is ctx.author.id

    try:
        print("waiting for message")
        message = await self.bot.wait_for('message', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        return False;
    else:
        print("replied in time and is from same user")
        print("message content="+message.content)
        return message.content

def setup(bot):
    bot.add_cog(Faucet(bot))
