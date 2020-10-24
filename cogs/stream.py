from discord.ext import commands

import zmq

from tinyrpc import RPCClient
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport



class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.rpc_client = RPCClient(JSONRPCProtocol(),ZmqClientTransport.create(zmq.Context(), 'tcp://127.0.0.1:5001')).get_proxy()

        #self.rpc_client.play()
                #@commands.Cog.listener() -> use for events like on_ready
    @commands.command()
    async def stream(self, ctx, arg1=None, arg2=None):
        print(arg1)
        if arg1 == 'play':
            await play(self,arg2,ctx)
        elif arg1 == 'pause':
            await pause(self,ctx)
        elif arg1 == 'resume':
            await resume(self,ctx)
        elif arg1 == 'join':
            await join(self,ctx)
        elif arg1 in ['disconnect','dc','fuckoff']:
            await disconnect(self,ctx)
        else:
            print("invalid peram")

def setup(bot):
    bot.add_cog(Stream(bot))

async def play(cog,arg, ctx):
    '''if ctx.guild is None:
        print("cannot stream in dm")
        return
    if ctx.message.author.voice.channel is None:
        print('not in vc')
        return'''
    if arg.startswith('https://youtube.com/') or arg.startswith('https://www.youtube.com') or arg.startswith('http://youtu.be'):
        cog.rpc_client.play(arg)

async def pause(cog, ctx):
    cog.rpc_client.pause()

async def resume(cog, ctx):
    cog.rpc_client.resume()

async def join(cog,ctx):
    cog.rpc_client.join()

async def disconnect(cog, ctx):
    cog.rpc_client.dc()
