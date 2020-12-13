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
    @commands.Cog.listener()
    async def on_ready(self):
        self.rpc_client.set_login("username", "password")

    @commands.command()
    async def stream(self, ctx, arg1=None, arg2=None, local_specifications=None):
        print(arg1)
        if arg1 == 'play':
            await play(self,arg2,ctx, local_specifications)
        elif arg1 == 'pause':
            self.rpc_client.pause()
        elif arg1 == 'resume':
            self.rpc_client.resume()
        elif arg1 == 'next':
             self.rpc_client.next_vid()
        elif arg1 in ['disconnect','dc']:
            self.rpc_client.dc()
        else:
            print("invalid peram")

def setup(bot):
    bot.add_cog(Stream(bot))

async def play(cog,arg, ctx, local_specifications=None):
    if ctx.guild is None:
        print("cannot stream in dm")
        return
    if ctx.message.author.voice is None:
        print('not in vc')
        return

    if arg.startswith('https://youtube.com/') or arg.startswith('https://www.youtube.com') or arg.startswith('https://youtu.be'):
        cog.rpc_client.play(arg, ctx.guild.name, ctx.author.voice.channel.name)
