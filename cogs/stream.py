from discord.ext import commands

import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient



class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.api = RPCClient(JSONRPCProtocol(),ZmqClientTransport.create(zmq.Context(), 'tcp://127.0.0.1:5001')).get_proxy()
        self.api.launch()
                #@commands.Cog.listener() -> use for events like on_ready

    @commands.command()
    async def stream(self, ctx, arg1=None):
        if arg1 == 'play':
            await play(self,ctx)
        elif arg1 == 'pause':
            await pause(self,ctx)
        elif arg1 == 'resume':
            await resume(self,ctx)
        elif arg1 in ['disconnect','dc']:
            await disconnect(self,ctx)
        else:
            print("invalid peram")

    async def play(self, ctx):
        print("play livestream")

    async def pause(self, ctx):
        print("paused livestream")

    async def resume(self, ctx):
        print("resume")

    async def disconnect(self, ctx):
        print("stop mpv")
        print("disconnect from vc -> but leave discord on")

def setup(bot):
    bot.add_cog(Stream(bot))
