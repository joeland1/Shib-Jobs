#https://github.com/PIVX-Project/PIVX/wiki/API-Calls-List


from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from discord.ext import commands
import discord
import crypto_perams

class Masternode_status_getter(commands.Cog):
    def __init__(self, bot):
            self.bot=bot

    @commands.command()
    async def getstatus(self, ctx, masternode_peram1, masternode_peram2=None):
        message_content=ctx.message.content.split(" ")
        if len(message_content) == 2:
            rpc_connection_CRYPTO = 'http://{0}:{1}@{2}:{3}'.format(crypto_perams.CRYPTO_RPC_USER, crypto_perams.CRYPTO_RPC_PW, crypto_perams.CRYPTO_RPC_IP, crypto_perams.CRYPTO_RPC_PORT)
            wallet = AuthServiceProxy(rpc_connection_CRYPTO)
            #print(wallet.listmasternodes(masternode_peram))
            #call rpc

            #try:
                #if ==2, then validateaddress

            if wallet.validateaddress(masternode_peram1)["isvalid"] == False:
                embed=discord.Embed(title="Masternode Status", description="Invalid address", color=0xff4646)
                await ctx.channel.send(embed=embed)
            else:
                listmasternodes_response=wallet.listmasternodes(masternode_peram1)
                if len(listmasternodes_response) == 0:
                    embed=discord.Embed(title="Masternode Status", description="There are no masternodes tied to this address", color=0xff4646)
                    await ctx.channel.send(embed=embed)

                else:
                    await send_masternodestatus_message(ctx, listmasternodes_response)
                            #real address crap

                #if ==3, then check tx
                #!getstatus txhash index

        elif len(message_content) == 3:
            rpc_connection_CRYPTO = 'http://{0}:{1}@{2}:{3}'.format(crypto_perams.CRYPTO_RPC_USER, crypto_perams.CRYPTO_RPC_PW, crypto_perams.CRYPTO_RPC_IP, crypto_perams.CRYPTO_RPC_PORT)
            wallet = AuthServiceProxy(rpc_connection_CRYPTO)

            if masternode_peram2.isdigit() is True:
                tx_verification=wallet.gettxout(masternode_peram1, int(masternode_peram2))
                if tx_verification is not None:
                    listmasternodes_response=wallet.listmasternodes(masternode_peram1)

                    if len(listmasternodes_response) == 0:
                        embed=discord.Embed(title="Masternode Status", description="False", color=0xff4646)
                        embed.add_field(name="Reason", value="Transaction is not associated with masternode", inline=False)
                        await ctx.channel.send(embed=embed)
                    else:
                        await send_masternodestatus_message(ctx, listmasternodes_response)

                else:
                    embed=discord.Embed(title="TX Status", description="Transaction doesn't exist", color=0xff4646)
                    await ctx.channel.send(embed=embed)
            else:
                embed=discord.Embed(title="TX Status", description="Output index is a number", color=0xff4646)
                await ctx.channel.send(embed=embed)

            #except:
            #    print("ya done fucked it up")
            #listmasternodes
            #validateaddress


            #send
async def send_masternodestatus_message(ctx, listmasternodes_output):
    for masternode_respose_index in listmasternodes_output:
        if masternode_respose_index["status"] == "ENABLED":
            #change to embed
            embed=discord.Embed(title="Masternode Status", description="Enabled", color=0x00e60c)
            await ctx.channel.send(embed=embed)


        elif masternode_respose_index["status"] == "ACTIVE":
            embed=discord.Embed(title="Masternode Status", description="Active", color=0x00e60c)
            await ctx.channel.send(embed=embed)

        elif masternode_respose_index["status"] == "EXPIRED":
            embed=discord.Embed(title="Masternode Status", description="Expired", color=0xff4646)
            await ctx.channel.send(embed=embed)

        elif masternode_respose_index["status"] == "MISSING":
            embed=discord.Embed(title="Masternode Status", description="Missing", color=0xff4646)
            await ctx.channel.send(embed=embed)

        elif masternode_respose_index["status"] == "REMOVE":
            embed=discord.Embed(title="Masternode Status", description="Remove", color=0xff4646)
            await ctx.channel.send(embed=embed)
def setup(bot):
    bot.add_cog(Masternode_status_getter(bot))
