from discord.ext import commands
import discord
import config
import global_functions

class ban_command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.mod_banner=None
        self.mod_reason=""
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.Cog.listener()
    async def on_member_ban(self, guild, banned_member):
        embed=discord.Embed(title="Ban Report", description="Shib Jobs Ban Hammer")
        embed.add_field(name="User:", value=banned_member.name+"#"+str(banned_member.discriminator), inline=True)
        embed.add_field(name="Reason:", value=self.mod_reason, inline=True)
        embed.add_field(name="ID:", value=banned_member.id, inline=False)
        embed.set_thumbnail(url=banned_member.avatar_url)
        respectable_mod=self.mod_banner.name+"#"+str(self.mod_banner.discriminator)
        embed.set_footer(text="Banned by: "+respectable_mod)

        await self.bot.get_channel(config.BAN_LOG).send(embed=embed)

    @commands.command()
    async def ban(self, ctx, members: commands.Greedy[discord.Member], hatban: commands.Greedy[int], *, reason=None):
        if global_functions.checkmodrole(ctx) is True:
            #bans based on id in text
            for offending_user in hatban:
                if reason is None:
                    await ctx.channel.send("You forgot a reason to ban")
                    break
                else:
                    self.mod_banner=ctx.author
                    self.mod_reason=reason
                    await ctx.guild.ban(discord.Object(id=offending_user))
                    print("hatban executed")

            #bans based on a ping
            for offending_user in members:
                if reason is None:
                    await ctx.channel.send("You forgot a reason to ban")
                    break
                else:
                    self.mod_banner=ctx.author
                    self.mod_reason=reason
                    await ctx.guild.ban(discord.Object(id=offending_user.id))
                    print("pingban executed")
        else:
            await ctx.channel.send("You do not have permission.")
def setup(bot):
    bot.add_cog(ban_command(bot))
