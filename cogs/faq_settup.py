from discord.ext import commands
import discord
import json
import os
import config
import sys

class FAQ(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.faq_questions=json.loads(open(os.getcwd()+"\\faq.json").read())
            self.faq_message=None
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def set_faq(self, ctx):
        faq_data = ctx.message.content.replace(self.bot.command_prefix+"set_faq ", "").split("|")
        for x in faq_data:
            print(x)

        embed=discord.Embed(title="FAQ",color=discord.Color.from_rgb(193,151,79))

    @commands.command()
    async def add_faq(self,ctx):
        print("add q+a to faq")

    @commands.command()
    async def remove_faq(self,ctx,arg1=None):
        print("removing question # arg1")

        if arg1 is None:
            ctx.channel.send("You need to specify which question you want removed")

    @commands.Cog.listener()
    async def on_ready(self):
        embed=discord.Embed(title="Shib FAQ")

        if len(self.faq_questions) == 0:
            print("faq not set up properly")
            return sys.exit(4)

        for question,answer in self.faq_questions.items():
            embed.add_field(name=question, value=answer, inline=False)
        faq_channel=self.bot.get_channel(config.FAQ_CHAT_ID)
        await faq_channel.send(content="",embed=embed)

def setup(bot):
    bot.add_cog(FAQ(bot))
