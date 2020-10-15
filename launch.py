import discord
import config
import os
import sys
import secure_tokens
import sqlite3

from discord.ext import commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

conn=sqlite3.connect(os.getcwd()+'\\lauch.db')
cursor=conn.cursor()
cursor.execute("SELECT * FROM MOD_STUFF")
data=cursor.fetchone()
cog_names = [description[0] for description in cursor.description]

if data[0] == 1:
    for index, command in enumerate(data[1:], start=1):
        if command == 2:
            client.load_extension(f'cogs.mod_tools.{cog_names[index]}')

token_entry=cursor.execute("SELECT * FROM DISCORD_TOKEN")

token = token_entry.fetchone()[0]

client.run(str(token))
