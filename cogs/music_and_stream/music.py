from discord.ext import commands
import youtube_dl
import discord

class MusicCog(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.music_list=[]
            #self.rpc_client = RPCClient(JSONRPCProtocol(),ZmqClientTransport.create(zmq.Context(), 'tcp://127.0.0.1:5002')).get_proxy()
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def music(self, ctx, arg1=None, arg2=None):
        if arg1 == 'play':
            await play(self,ctx,arg2)
        elif arg1 == 'pause':
            await pause(self,ctx)
        elif arg1 == 'resume':
            await resume(self,ctx)
        elif arg1 in ['disconnect','dc']:
            await disconnect(self,ctx)

def setup(bot):
    bot.add_cog(MusicCog(bot))

async def play(self, ctx, link):
    '''ydl_opts = {'format': 'bestaudio[ext=webm]'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        URL = info['formats'][0]['url']
    voice = await ctx.author.voice.channel.connect()
    voice.play(discord.FFmpegPCMAudio(URL))'''

    ydl_opts = {'format': 'bestaudio[ext=webm]', 'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        URL = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(URL)
    vc = await ctx.author.voice.channel.connect()
    vc.play(source)


async def pause(self, ctx):
    print("play livestream")
async def resume(self, ctx):
    print("play livestream")
async def disconnect(self, ctx):
    print("play livestream")
