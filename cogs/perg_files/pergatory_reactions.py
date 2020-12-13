from discord.ext import commands
import discord

class Pergatory_reactions(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.verify_all=None
    #@commands.Cog.listener() -> use for events like on_ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("perg reactions loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.verify_all is None:
            print("error verify cog")
            sys.exit(4)
        elif self.verify_all is True:
            perg_add_role=discord.utils.get(member.guild.roles, id=config.PERG_ROLE_ID)
            await member.add_roles(perg_add_role)
            await self.bot.get_channel(config.PERG_LOG).send(member.mention+" is locked in perg")
        elif self.verify_all is False:
            time_difference = datetime.utcnow()-member.created_at
            if time_difference.days > config.PERG_DAY and time_difference.seconds//3600 > config.PERG_HOUR:
                #old account
                await self.bot.get_channel(config.PERG_LOG).send(member.mention+" has joined")

            else:
                perg_add_role=discord.utils.get(member.guild.roles, id=config.PERG_ROLE_ID)
                await member.add_roles(perg_add_role)
                await self.bot.get_channel(config.PERG_LOG).send(member.mention+" is locked in perg")

        
def setup(bot):
    bot.add_cog(Pergatory_reactions(bot))
