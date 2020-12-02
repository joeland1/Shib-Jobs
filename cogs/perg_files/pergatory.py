from discord.ext import commands
import discord
from datetime import datetime
import config

import global_functions

#add a captcha as a way for users to verify themselves

class Pergatory(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.verify_all=None
    #@commands.Cog.listener() -> use for events like on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        if config.PERG_HOUR>=24:
            print("Change your pergatory hours to proper conversion. It's too big") #niceeeeeeeeeee
            sys.exit(4)

    #based on time
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.verify_all is None:
            print("error verify cog")
            sys.exit(4)
        if self.verify_all=True:
            perg_add_role=discord.utils.get(member.guild.roles, id=config.PERG_ROLE_ID)
            await member.add_roles(perg_add_role)
            await self.bot.get_channel(config.PERG_LOG).send(member.mention+" is locked in perg")

        elif:
            time_difference = datetime.utcnow()-member.created_at
            if time_difference.days > config.PERG_DAY and time_difference.seconds//3600 > config.PERG_HOUR:
                #old account
                await self.bot.get_channel(config.PERG_LOG).send(member.mention+" has joined")

            else:
                perg_add_role=discord.utils.get(member.guild.roles, id=config.PERG_ROLE_ID)
                await member.add_roles(perg_add_role)
                await self.bot.get_channel(config.PERG_LOG).send(member.mention+" is locked in perg")

    @commands.command()
    async def verify(self, ctx, members: commands.Greedy[discord.Member]):
        if global_functions.checkmodrole(ctx) is True:
            restricted_role = discord.utils.get(ctx.guild.roles, id=config.PERG_ROLE_ID)
            for going_to_be_verified in members:
                if restricted_role in going_to_be_verified.roles:
                    await going_to_be_verified.remove_roles(restricted_role)
                    print("removed")
                else:
                    print(going_to_be_verified.name+" is not restricted")
        else:
            await ctx.channel.send("You have no perms")

    #need something so that users can verify on their own ,captcha?

def setup(bot):
    bot.add_cog(Pergatory(bot))
