import config
import discord

def checkmodrole(ctx):
    role_status=[]
    for role in config.MOD_ROLES:
        role_status.append(discord.utils.get(ctx.guild.roles, name=role))

    for mod_role in role_status:
        if mod_role in ctx.author.roles:
            return True
    return False

def is_a_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False
