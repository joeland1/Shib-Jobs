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
    async def rm_faq(self,ctx,skip_question_number=None):
        print("removing question # skip_question_number")

        if global_functions.checkmodrole(ctx) is False:
            print("not admin, cannot modify faq")
            return

        if skip_question_number is None:
            ctx.channel.send("You need to specify which question you want removed")

        if global_functions.is_a_number(skip_question_number) is False:
            ctx.channel.send("Not valid input")

        with open(os.getcwd()+"\\faq.json") as faq_questions:
            faq_questions_data = json.loads(faq_questions.read()).items()

            faq_question_data_final = {}
            for iteration,question_set in enumerate(faq_questions_data):
                print(str(iteration))

                if iteration == int(skip_question_number) - 1:
                    print("skipped question at index "+str(iteration))
                    continue
                faq_question_data_final[question_set[0]] = question_set[1]

            if len(faq_question_data_final) == 0:
                embed=discord.Embed(title="Shib FAQ", description="You have removed the last faq question")
                await self.faq_message.delete()
                faq_channel=self.bot.get_channel(config.FAQ_CHAT_ID)
                self.faq_message = await faq_channel.send(content="", embed=embed)
                return

            else:
                embed=discord.Embed(title="Shib FAQ")
                await self.faq_message.delete()
                faq_channel=self.bot.get_channel(config.FAQ_CHAT_ID)

                for question,answer in faq_question_data_final.items():
                    embed.add_field(name=question, value=answer, inline=False)
                self.faq_message = await faq_channel.send(content="", embed=embed)

                print(faq_question_data_final)
                #json_object = json.dumps(faq_question_data_final, indent = 4)
                with open(os.getcwd()+"\\faq.json", "w") as outfile:
                    json.dump(faq_question_data_final, outfile)

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
