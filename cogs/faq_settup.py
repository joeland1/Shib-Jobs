from discord.ext import commands
import discord
import json
import os
import config
import sys
import global_functions

class FAQ(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.faq_message=None
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def set_faq(self, ctx):
        faq_data = ctx.message.content.replace(self.bot.command_prefix+"set_faq ", "").split("|")
        for x in faq_data:
            print(x)

        embed=discord.Embed(title="FAQ",color=discord.Color.from_rgb(193,151,79))

    @commands.command()
    # !add_faq <question> <answer> <optional for location>
    async def add_faq(self,ctx):
        if global_functions(ctx.author) is False:
            print("not admin, cannot modify faq")
            return

        print("add q+a to faq")

    @commands.command()
    async def rm_faq(self,ctx,arg1=None):
        print("removing question # arg1")

        if global_functions(ctx.author) is False:
            print("not admin, cannot modify faq")
            return

        if arg1 is None:
            ctx.channel.send("You need to specify which question you want removed")

        with open(os.getcwd()+"\\faq.json", 'w') as faq_questions:
            for iteration,question,answer in enumerate(json.loads(faq_questions.read()).items()):
                print(str(iteration)+" "+question)

            json.dump(data, f, ensure_ascii=False, indent=4)

            if len(faq_questions) == 0:
                embed=discord.Embed(title="Shib FAQ", description="There are no questions in the FAQ")
                await self.faq_message.edit(content="", embed=embed)
                return



    @commands.Cog.listener()
    async def on_ready(self):
        with open(os.getcwd()+"\\faq.json") as faq_questions:

            faq_quetions_data = json.loads(faq_questions.read())

            if len(faq_quetions_data) == 0:
                embed=discord.Embed(title="Shib FAQ", description="There are no questions in the FAQ")

            else:
                embed=discord.Embed(title="Shib FAQ")
                for question,answer in faq_quetions_data.items():
                    embed.add_field(name=question, value=answer, inline=False)

        faq_channel=self.bot.get_channel(config.FAQ_CHAT_ID)
        self.faq_message =  await faq_channel.send(content="",embed=embed)

def setup(bot):
    bot.add_cog(FAQ(bot))
