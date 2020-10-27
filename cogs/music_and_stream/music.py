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
        del self.link_id[0]
        for file in os.listdir():
            if file.endswith('.stream'):
                os.remove(file)

        if len(self.link_id) == 0:
            print('end of line for continue_voice')
            self.voice_chat = None
            return

        if self.voice_chat.is_connected() is False:
            print('vc disconnected, no longer playing')
            self.voice_chat = None
            self.link_id.clear()
            return

        if self.get_youtube_file_download(self.link_id[0]) is False:
            self.continue_voice(None, self)

        self.voice_chat.play(discord.FFmpegPCMAudio(self.link_id[0]+'.stream'), after=lambda e: self.continue_voice(self))

    @commands.command()
    async def music(self, ctx, arg1=None, arg2=None):
        #source = discord.FFmpegOpusAudio(info['formats'][0]['url'])
        #source = await discord.FFmpegOpusAudio.from_probe('music_source')
        #source = discord.FFmpegPCMAudio(info['formats'][0]['url'])
        if arg1 == 'play':
            #this only adds to the list and starts going through the list of links
            link=arg2

            if 'list=' in link:
                ydl_opts_for_playlist = {
                    'format': 'bestaudio/best[ext=webm]',
                    'before_options':'-reconnect 5 -reconnect_streamed 5 -reconnect_delay_max 6000',
                    'continuedl': True,
                    'extract_flat':True}
                with youtube_dl.YoutubeDL(ydl_opts_for_playlist) as ydl:
                    info = ydl.extract_info(link, download=False)
                    for index,entry in enumerate(info['entries']):
                        self.link_id.append(entry['id'])
                        print('added -> '+entry['id'])

                if self.voice_chat is None:
                    for file in os.listdir():
                        if file.endswith('.stream'):
                            os.remove(file)
                            
                    if self.get_youtube_file_download(self.link_id[0]) is False:
                        self.continue_voice(None, self)

                    source =  discord.FFmpegPCMAudio(self.link_id[0]+'.stream')

                    self.voice_chat = await ctx.author.voice.channel.connect()
                    self.voice_chat.play(source, after=lambda e: self.continue_voice(self))

            elif 'v=' in link and 'list=' not in link:
                self.link_id.append(link.split('v=')[1])
                print('addedurl='+link.split('v=')[1])

                #need to start a vc chain
                if self.voice_chat is None:
                    for file in os.listdir():
                        if file.endswith('.stream'):
                            os.remove(file)

                    if self.get_youtube_file_download(self.link_id[0]) is False:
                        self.continue_voice(None, self)

                    source =  discord.FFmpegPCMAudio(self.link_id[0]+'.stream')

                    self.voice_chat = await ctx.author.voice.channel.connect()
                    self.voice_chat.play(source, after=lambda e: self.continue_voice(self))

        elif arg1 == 'pause':
            self.voice_chat.pause()
        elif arg1 == 'resume':
            self.voice_chat.resume()
        elif arg1 == 'next':
            if len(self.link_id) == 0:
                await self.voice_chat.disconnect()
                self.voice_chat.cleanup()
                self.voice_chat=None
                print('skipped while on last track')
                return

            self.voice_chat.stop()
        elif arg1 in ['disconnect','dc','fuckoff']:
            self.voice_chat.disconnect()
            self.voice_chat.cleanup()

            for file in os.listdir():
                if file.endswith('.stream'):
                    os.remove(file)

    def get_youtube_file_download(self,name):
        ydl_opts = {
            'format': 'bestaudio/best[ext=webm]',
            'before_options':'-reconnect 5 -reconnect_streamed 5 -reconnect_delay_max 6000',
            'continuedl': True,
            'outtmpl': name+'.stream'}
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info('https://www.youtube.com/watch?v='+name, download=True)
            print('download worked 1st try')
        except:
            print('error on try 1, trying again')
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info('https://www.youtube.com/watch?v='+name, download=True)
            except:
                print('both tries failed, booking it')
                return False
        return True

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
'''ydl_opts = {
                'format': 'bestaudio/best[ext=webm]',
                'before_options':'-reconnect 5 -reconnect_streamed 5 -reconnect_delay_max 6000',
                'continuedl': True,
                'outtmpl': self.link_id[0]+'.stream'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info('https://www.youtube.com/watch?v='+self.link_id[1], download=True)
            source =  discord.FFmpegPCMAudio(self.link_id[1]+'.stream')
            for file in os.listdir():
                if file == self.link_id[0]+'.stream':
                    os.remove(file)
            del self.link_id[0]

            self.voice_chat.play(source, after=lambda e: self.continue_voice(self))
        elif arg1 in ['disconnect','dc']:
            await self.voice_chat.disconnect()
            self.voice_chat.cleanup()
            self.voice_chat = None'''
