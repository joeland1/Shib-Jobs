from discord.ext import commands
import discord
import config

import global_functions

class unban_command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.mod_banner=None
        self.mod_reason=""
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.Cog.listener()
    async def on_member_unban(self, guild, banned_member):
        embed=discord.Embed(title="Unban Report", description="Shib Jobs's Kind Heart")
        embed.add_field(name="User:", value=banned_member.name+"#"+str(banned_member.discriminator), inline=True)
        embed.add_field(name="Reason:", value=self.mod_reason, inline=True)
        embed.add_field(name="ID:", value=banned_member.id, inline=False)
        embed.set_thumbnail(url=banned_member.avatar_url)
        respectable_mod=self.mod_banner.name+"#"+str(self.mod_banner.discriminator)
        embed.set_footer(text="Revived by: "+respectable_mod)

        await self.bot.get_channel(config.BAN_LOG).send(embed=embed)

    @commands.command()
    async def unban(self, ctx, members: commands.Greedy[discord.Member], hatban: commands.Greedy[int], *, reason=None):
        if global_functions.checkmodrole(ctx) is True:
            #bans based on id in text
            for offending_user in hatban:
                if reason is None:
                    await ctx.channel.send("You forgot a reason to unban")
                    break
                else:
                    self.mod_banner=ctx.author
                    self.mod_reason=reason
                    await ctx.guild.unban(discord.Object(id=offending_user))
                    print("hat-unban pass")

            #bans based on a ping
            for offending_user in members:
                if reason is None:
                    await ctx.channel.send("You forgot a reason to unban")
                    break
                else:
                    self.mod_banner=ctx.author
                    self.mod_reason=reason
                    await ctx.guild.unban(discord.Object(id=offending_user.id))
                    print("ping-unban pass")
        else:
            await ctx.channel.send("You do not have permission.")



def setup(bot):
    bot.add_cog(unban_command(bot))
