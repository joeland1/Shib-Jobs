from discord.ext import commands
import youtube_dl
import discord
import asyncio
import os


class MusicCog(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
            self.link_id=[]
            self.voice_chat=None
            #self.rpc_client = RPCClient(JSONRPCProtocol(),ZmqClientTransport.create(zmq.Context(), 'tcp://127.0.0.1:5002')).get_proxy()
    #@commands.Cog.listener() -> use for events like on_ready
    def continue_voice(error, self):
        if len(self.link_id) == 0:
            print('end of line')
            self.voice_chat = None
            return

        ydl_opts = {
            'format': 'bestaudio/best[ext=webm]',
            'before_options':'-reconnect 5 -reconnect_streamed 5 -reconnect_delay_max 6000',
            'continuedl': True,
            'outtmpl': 'music_source'}
        os.remove('music_source')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info('https://www.youtube.com/watch?v='+self.link_id[0], download=True)

        self.voice_chat.play(discord.FFmpegPCMAudio('music_source'), after=lambda e: self.continue_voice(self))

    @commands.command()
    async def music(self, ctx, arg1=None, arg2=None):
        if arg1 == 'play':
            #this only adds to the list and starts going through the list of links
            link=arg2

                #source = discord.FFmpegOpusAudio(info['formats'][0]['url'])
                #source = await discord.FFmpegOpusAudio.from_probe('music_source')
                #source = discord.FFmpegPCMAudio(info['formats'][0]['url'])
            self.link_id.append(link.split('v=')[1])
            print('addedurl='+link.split('v=')[1])

            #need to start a vc chain
            if self.voice_chat is None:
                try:
                    os.remove('music_source')
                except:
                    pass
                ydl_opts = {
                    'format': 'bestaudio/best[ext=webm]',
                    'before_options':'-reconnect 5 -reconnect_streamed 5 -reconnect_delay_max 6000',
                    'continuedl': True,
                    'outtmpl': 'music_source'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info('https://www.youtube.com/watch?v='+self.link_id[0], download=True)
                source =  discord.FFmpegPCMAudio('music_source')
                del self.link_id[0]

                self.voice_chat = await ctx.author.voice.channel.connect()
                self.voice_chat.play(source, after=lambda e: self.continue_voice(self))

        elif arg1 == 'pause':
            ctx.voice_chat.pause()
        elif arg1 == 'resume':
            ctx.voice_chat.resume()
        elif arg1 == 'next':
            if len(self.link_id) == 0:
                await self.voice_chat.disconnect()
                self.voice_chat=None
                print('skipped last track')
                return

            try:
                os.remove('music_source')
            except:
                pass
            ydl_opts = {
                'format': 'bestaudio/best[ext=webm]',
                'before_options':'-reconnect 5 -reconnect_streamed 5 -reconnect_delay_max 6000',
                'continuedl': True,
                'outtmpl': 'music_source'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info('https://www.youtube.com/watch?v='+self.link_id[0], download=True)
            source =  discord.FFmpegPCMAudio('music_source')
            del self.link_id[0]

            self.voice_chat.play(source, after=lambda e: self.continue_voice(self))
        elif arg1 in ['disconnect','dc']:
            await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(MusicCog(bot))


'''else:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        for id in info['entries']:
            link_id.append(id['url'])'''
'''extract_flat': True'''
'''ydl_opts = {
    'format': 'bestaudio/best[ext=webm]',
    'before_options':'-reconnect 5 -reconnect_streamed 5 -reconnect_delay_max 6000',
    'continuedl': True,
    'outtmpl': 'music_source'}
if 'v=' in link:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            os.remove('music_source')
        except:
            pass
        info = ydl.extract_info(link, download=False)'''
        #source = await discord.FFmpegOpusAudio.from_probe(info['formats'][self.playlist_ctr]['url'])
        #vc = await ctx.author.voice.channel.connect()
        #vc.play(source)
