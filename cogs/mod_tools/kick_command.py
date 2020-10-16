from discord.ext import commands
import discord
import config
import global_functions

class kick_command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.mod_kicker=None
        self.mod_reason=""
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.Cog.listener()
    async def on_member_kick(self, guild, kicked_member):
        embed=discord.Embed(title="Kick Report")
        embed.add_field(name="User:", value=kicked_member.name+"#"+str(kicked_member.discriminator), inline=True)
        embed.add_field(name="Reason:", value=self.mod_reason, inline=True)
        embed.add_field(name="ID:", value=kicked_member.id, inline=False)
        embed.set_thumbnail(url=kicked_member.avatar_url)
        respectable_mod=self.mod_kicker.name+"#"+str(self.mod_kicker.discriminator)
        embed.set_footer(text="Banned by: "+respectable_mod)

        await self.bot.get_channel(config.BAN_LOG).send(embed=embed)

    @commands.command()
    async def kick(self, ctx, members: commands.Greedy[discord.Member], hatban: commands.Greedy[int], *, reason=None):
        if global_functions.checkmodrole(ctx) is True:
            #bans based on id in text
            for offending_user in hatban:
                if reason is None:
                    await ctx.channel.send("You forgot a reason to kick")
                    break
                else:
                    self.mod_kicker=ctx.author
                    self.mod_reason=reason
                    await ctx.guild.kick(discord.Object(id=offending_user))
                    print("hatkick executed")

            #bans based on a ping
            for offending_user in members:
                if reason is None:
                    await ctx.channel.send("You forgot a reason to kick")
                    break
                else:
                    self.mod_kicker=ctx.author
                    self.mod_reason=reason
                    await ctx.guild.kick(discord.Object(id=offending_user.id))
                    print("pingkick executed")
        else:
            await ctx.channel.send("You do not have permission.")
def setup(bot):
    bot.add_cog(kick_command(bot))
