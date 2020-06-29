import discord
import config
import os
import sys
import secure_tokens

from discord.ext import commands

client = commands.Bot(command_prefix=config.PREFIX)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

for filename in os.listdir(os.getcwd()+f'\\cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

if config.PERG_HOUR>=24:
    print("Change your pergatory hours to proper conversion. It's too big") #niceeeeeeeeeee
    sys.exit(4)

client.run(secure_tokens.DISCORD_TOKEN)
