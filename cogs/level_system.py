from discord.ext import commands
import sqlite3
import os
import time
import random
import config
import global_functions
from io import BytesIO
import os
import discord

from PIL import Image, ImageDraw, ImageFont

class Level_system(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def rank(self, ctx, arg1=None):
        #level up algo: x^2+10-> will determine level rank for level "x" so level 0 requires 10 pts before getting to lv 1
        if arg1 is None:
            display_level=1
            #whatever equation you want, but minus 1, idk y it jsut works
            while display_level**2+99 < get_xp_value(ctx.author.id):
                display_level+=1
            #use while to get Levels
            #use for to get role
            display_level-=1

            remaining_xp= get_xp_value(ctx.author.id)-(display_level**2+99)
            if remaining_xp < 0:
                remaining_xp = get_xp_value(ctx.author.id)

            print(str(get_xp_value(ctx.author.id)))
            print(str(remaining_xp))

            final_display = Image.new('RGB', (3000, 1000), color = (73, 109, 137))

            #d = ImageDraw.Draw(img)
            #d.text((10,10), "Hello World", fill=(255,255,0))

            upscale_factor=10
            base_size_pfp=700
            base_size_outside=base_size_pfp+30

            asset = ctx.author.avatar_url_as(format="png",size=1024)
            discord_pfp_source = Image.open(BytesIO(await asset.read()))
            #print(discord_pfp_source.size[0])
            discord_pfp_source=discord_pfp_source.resize((base_size_pfp,base_size_pfp), resample=Image.LANCZOS)
            discord_pfp_source.save('discord_pfp_source.png')

            #gets the shape of the profile picture
            discord_pfp_shape = Image.new("L", (base_size_pfp*upscale_factor,base_size_pfp*upscale_factor), 0)
            draw1 = ImageDraw.Draw(discord_pfp_shape)
            draw1.ellipse(((0,0), discord_pfp_shape.size), fill=255)
            discord_pfp_shape = discord_pfp_shape.resize((base_size_pfp,base_size_pfp), Image.LANCZOS)
            discord_pfp_shape.save('downlscale_discord_pfp_shape.png')

            #get outline for the shape of the pfp
            discord_pfp_outer_circle = Image.new("RGB", (base_size_outside,base_size_outside), color=(193,151,79))
            discord_pfp_outer_circle.save('downlscale_discord_pfp_outline_start.png')
            discord_pfp_outside_shape = discord_pfp_shape.resize((base_size_outside,base_size_outside), Image.LANCZOS)
            discord_pfp_outer_circle.save('downlscale_discord_pfp_outline.png')

            #we only need y, can set x manually
            background_offset_x=100
            background_offset_y = int(  (final_display.size[1]-discord_pfp_outside_shape.size[1])*0.5)
            print("background"+str(background_offset_y))

            pfp_offset_x= background_offset_x + int((discord_pfp_outside_shape.size[0]-discord_pfp_source.size[0])*0.5)
            pfp_offset_y= background_offset_y + int((discord_pfp_outside_shape.size[0]-discord_pfp_source.size[0])*0.5)

            #calculates the distance down + right based on the pfp location
            #offset_pfp_outline=pfp_both_offset + int(  (discord_pfp_outside_shape.size[0]-discord_pfp_shape.size[0])*0.5)

            final_display.paste(discord_pfp_outer_circle,(background_offset_x,background_offset_y),discord_pfp_outside_shape)
            final_display.paste(discord_pfp_source,(pfp_offset_x,pfp_offset_y),discord_pfp_shape)

            final_display_text = ImageDraw.Draw(final_display)

            font_size = 300
            discriminator_size=font_size-35
            min_font_size = 30

            name_font = ImageFont.truetype(os.getcwd()+'\\fonts\\Montserrat\\Montserrat-Regular.ttf', font_size)
            descriminator_font = ImageFont.truetype(os.getcwd()+'\\fonts\\Montserrat\\Montserrat-Regular.ttf', font_size-35)

            max_total_length = 2000

            name_length = name_font.getsize(ctx.author.name)
            discriminator_length = descriminator_font.getsize("#"+str(ctx.author.discriminator))
            while name_length[0]+discriminator_length[0] >= max_total_length:
                font_size -= 10
                print(str(font_size))
                name_font = ImageFont.truetype(os.getcwd()+'\\fonts\\Montserrat\\Montserrat-Regular.ttf', font_size)
                name_length = name_font.getsize(ctx.author.name)

                while discriminator_length[1]/name_length[1]*100 >= 70:
                    discriminator_size -=5
                    descriminator_font = ImageFont.truetype(os.getcwd()+'\\fonts\\Montserrat\\Montserrat-Regular.ttf', discriminator_size)

                    discriminator_length = descriminator_font.getsize("#"+str(ctx.author.discriminator))


            name_displacement_x=background_offset_x+discord_pfp_outside_shape.size[0]+150
            final_display_text.text((name_displacement_x,final_display.height/4), ctx.author.name, font=name_font, fill=(255, 255, 0))
            base_height = name_font.getsize('l')

            final_display_text.text((name_displacement_x+name_length[0], final_display.height/4+base_height[1]-discriminator_length[1]), "#{0}".format(ctx.author.discriminator), font=descriminator_font, fill=(255,255,0))


            current_font = ImageFont.truetype(os.getcwd()+'\\fonts\\Open_Sans\\OpenSans-Regular.ttf', 100)
            final_display_text.text( (name_displacement_x+175, final_display.height/4+name_length[1]),"Level: "+str(display_level)+" XP: "+str(remaining_xp) , font=current_font, fill=(255, 255, 0))
            #final_display.resize((900,300), resample=Image.LANCZOS)

            arr=BytesIO()
            final_display.save(arr, format='png',optimize=True)
            arr.seek(0)

            await ctx.channel.send(file=discord.File(arr, "my_rank.png"))

            final_display.save(os.getcwd()+"\\"+str(ctx.author.id)+'_sent_card.png')

            level_up_bar=Image.open(os.getcwd()+"\\level_pictures\\1.jpg")
            level_up_bar.paste(Image.open(os.getcwd()+"\\level_pictures\\2.jpg"),(0,0))
            level_up_bar.save(os.getcwd()+"\\bar_picture.jpg")

            #final_display.save(imgByteArr, format='PNG')
            #imgByteArr=imgByteArr.getvalue()





    # for the table
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
            conn.execute('''CREATE TABLE LEVELS
            (GLOBAL_RANK   INTEGER PRIMARY KEY,
            USER_ID    INT    NOT NULL,
            LAST_MESSAGE_TIME    INT    NOT NULL,
            XP    INT    NOT NULL);''')
            conn.commit()
            conn.close()

            print("created a new rank_recording table")

        except sqlite3.OperationalError:
            print("old table found for levels -> using old db")
            print("if you want to use a new one, delete rank_recording.db")
            conn.close()

    @commands.Cog.listener()
    async def on_member_join(self,member):
        conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
        cur=conn.cursor()

        search_command= 'SELECT * FROM LEVELS WHERE USER_ID = ?'
        cur.execute(search_command,(member.id,))
        user_entries=cur.fetchone()

        if user_entries is None:
            add_command = 'INSERT INTO LEVELS (USER_ID,LAST_MESSAGE_TIME,XP) VALUES (?,?,?)'
            input_data = (member.id,0,random.randint(1,config.XP_INCRAMENT))
            conn.execute(add_command,input_data)
            conn.commit()

        cur.close()
        conn.close()
        print("added new user")

    @commands.Cog.listener()
    async def on_message(self,ctx):
        if ctx.author.bot is True:
            print("is bot")
            return
        if ctx.content.startswith(self.bot.command_prefix):
            print("is a command so not giving xp")
            return
        current_time = int(time.time())
        if current_time - get_last_time(ctx.author.id) <= config.XP_TIME_MIN:
            return

        print("author id="+str(ctx.author.id))
        modify_xp_value(ctx.author.id)
    #@commands.command()
    #async def remove(self,ctx):

    #should implement removal for leaving own own?
    @commands.Cog.listener()
    async def on_member_ban(self, guild, banned_member):
        print("membver banning occuring")
        conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
        conn.execute('DELETE FROM LEVELS WHERE USER_ID = ?',(banned_member.id,))
        conn.commit()
        conn.close()

        print("deleted")

    #async def on_member_remove(member_left):
    #    conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
    #    conn.execute('DELETE FROM LEVELS WHERE USER_ID = ?',(member_left.id))
    #    conn.commit()
    #    conn.close()

    @commands.command()
    async def print_out_levels(self,ctx):
        if global_functions.checkmodrole(ctx) is True:
            print("is admin")
            conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
            cursor=conn.cursor()

            print("getting data")
            all_data=cursor.execute("SELECT * FROM LEVELS")

            for data in all_data:
                print(data)

            cursor.close()
            conn.close()
        else:
            print(ctx.author.name+" tried to print out a level table")


def modify_xp_value(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
    cursor=conn.cursor()

    #check to see if there are entries
    search_command= 'SELECT * FROM LEVELS WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    user_entries=len(cursor.fetchall())
    cursor.close()

    # update if there is 1 entry
    if user_entries == 1:
        updating_command='UPDATE LEVELS SET LAST_MESSAGE_TIME = ?, XP = ? WHERE USER_ID = ?'
        updated_level_data = (int(time.time()), get_xp_value(discord_id)+random.randint(1,config.XP_INCRAMENT),discord_id)
        conn.execute(updating_command,updated_level_data)
        conn.commit()
        print("added xp")

    #add if no entires, should not happen because the user should be added
    elif user_entries == 0:
        add_command = 'INSERT INTO LEVELS (USER_ID,LAST_MESSAGE_TIME,XP) VALUES (?,?,?)'
        input_data = (discord_id,int(time.time()),random.randint(1,config.XP_INCRAMENT))
        conn.execute(add_command,input_data)
        conn.commit()
        print("added new user")

    else:
        print("more than 1 entry somehow")


    conn.close()

def get_xp_value(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
    cursor=conn.cursor()

    search_command= 'SELECT XP FROM LEVELS WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    xp = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return xp

def get_last_time(discord_id):
    conn=sqlite3.connect(os.getcwd()+'\\rank_recording.db')
    cursor=conn.cursor()

    search_command= 'SELECT * FROM LEVELS WHERE USER_ID = ?'
    cursor.execute(search_command,(discord_id,))
    entry = cursor.fetchone()
    cursor.close()
    conn.close()

    if entry is None:
        return 0
    else:
        return entry[2]


def setup(bot):
    bot.add_cog(Level_system(bot))
