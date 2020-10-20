from discord.ext import commands

import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient

ctx = zmq.Context()



class Stream(commands.Cog):
    def __init__(self, bot):
            self.bot=bot
    #@commands.Cog.listener() -> use for events like on_ready

rpc_client = RPCClient(JSONRPCProtocol(),ZmqClientTransport.create(ctx, 'tcp://127.0.0.1:5001'))
remote_server = rpc_client.get_proxy()

result = remote_server.join()
print("Server answered: "+str(result))


    @commands.command()
    async def watch(self, ctx):
        watched_show = ctx.content.replace(config.PREFIX+"watch", "")
        print(watched_show)

def setup(bot):
    bot.add_cog(Stream(bot))
