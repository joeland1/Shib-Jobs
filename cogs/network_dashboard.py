from discord.ext import commands
import crypto_perams
from discord.ext import tasks
import discord
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time
import datetime
from pytz import timezone
import config

#is there way to remove all this

from pycoingecko import CoinGeckoAPI

class Network_dashboard(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.cg=CoinGeckoAPI()
        self.price_usd=0.0
        self.price_btc=0.0
    #@commands.Cog.listener() -> use for events like on_ready

    @commands.Cog.listener()
    async def on_ready(self):
        dashboard_channel=self.bot.get_channel(crypto_perams.CRYPTO_DASHBOARD_CHANNEL)
        dashboard_message = await dashboard_channel.send("------------Starting Dashboard------------")
        self.update_dashboard_network.start(dashboard_message)

        coingecko_message = await dashboard_channel.send("------------Starting Price Monitoring------------")
        self.update_dashboard_coingecko_pricing.start(coingecko_message)

        masternode_message = await dashboard_channel.send("------------Starting Masternode Stats------------")
        self.update_dashboard_masternode_stats.start(masternode_message)

    @tasks.loop(seconds=5.0)
    async def update_dashboard_network(self, message):
        rpc_connection_CRYPTO = 'http://{0}:{1}@{2}:{3}'.format(crypto_perams.CRYPTO_RPC_USER, crypto_perams.CRYPTO_RPC_PW, crypto_perams.CRYPTO_RPC_IP, crypto_perams.CRYPTO_RPC_PORT)
        wallet = AuthServiceProxy(rpc_connection_CRYPTO)

        getmininginfo_response = wallet.getmininginfo()

        embed=discord.Embed(title="Shib Stats")

        #1440 blocksper day
        #7.2 mn reward

        #row 1
        embed.add_field(name="Version", value=str(wallet.getnetworkinfo()["subversion"]).replace("/",""), inline=True)
        embed.add_field(name="Connections", value=str(wallet.getconnectioncount()), inline=True)
        embed.add_field(name="Block Count", value=getmininginfo_response["blocks"], inline=True)

        embed.add_field(name="Difficulty", value=round(getmininginfo_response["difficulty"], 2), inline=True)
        embed.add_field(name="Nethash", value=calc_converted_nethash(getmininginfo_response["networkhashps"]), inline=True)
        best_hash=wallet.getbestblockhash()

        #print("best hash = "+best_hash)

        embed.add_field(name="Blockhash",value=best_hash[:5]+"..."+best_hash[-5:],inline=True)

        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="Last updated")
        #row 2
        embed.set_author(name=self.bot.user.name, url="https://github.com", icon_url=self.bot.user.avatar_url)

        await message.edit(content="", embed=embed)
        #await message.channel.send(self.ctr)
        #self.ctr=self.ctr+5

    @tasks.loop(seconds=5.0)
    async def update_dashboard_coingecko_pricing(self, message):

        embed=discord.Embed(title="Price Stats")

        coin_info=self.cg.get_coin_by_id(id=crypto_perams.COINGECKO_API_CRYPTO_NAME,localization="false", tickers=False, market_data=True,community_data=False,developer_data=False,sparkline=False)
        self.price_usd=coin_info["market_data"]["current_price"]["usd"]
        self.price_btc=coin_info["market_data"]["current_price"]["btc"]
        #print(price_info)
        embed.add_field(name="Price (USD)", value="$"+str(round(self.price_usd,2)), inline=True)
        embed.add_field(name="Price (BTC)", value=("{:.8f}฿").format(self.price_btc), inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        #embed.add_field(name="ATH", value=str(coin_info["market_data"]["ath"]["usd"]), inline=True)
        #print("pass")
        embed.add_field(name="1 Day", value=str(round(coin_info["market_data"]["price_change_percentage_24h"],2))+"%", inline=True)
        embed.add_field(name="1 Week", value=str(round(coin_info["market_data"]["price_change_percentage_7d"],2))+"%", inline=True)
        embed.add_field(name="1 Month", value=str(round(coin_info["market_data"]["price_change_percentage_30d"],2))+"%", inline=True)

        embed.add_field(name="Market Cap (USD)", value="$"+str(coin_info["market_data"]["market_cap"]["usd"]), inline=True)
        embed.add_field(name="Market Cap (BTC)", value=str(round(coin_info["market_data"]["market_cap"]["btc"],3))+"฿", inline=True)
        embed.add_field(name="Trading Volume (24 Hr)", value="$"+str(coin_info["market_data"]["total_volume"]["usd"]), inline=True)

        embed.timestamp=datetime.datetime.utcnow()
        embed.set_footer(text="Last updated")

        embed.set_author(name=self.bot.user.name, url="https://github.com", icon_url=self.bot.user.avatar_url)

        await message.edit(content="", embed=embed)

    @tasks.loop(seconds=10.0)
    async def update_dashboard_masternode_stats(self, message):
        embed=discord.Embed(title="Masternode Stats")

        rpc_connection_CRYPTO = 'http://{0}:{1}@{2}:{3}'.format(crypto_perams.CRYPTO_RPC_USER, crypto_perams.CRYPTO_RPC_PW, crypto_perams.CRYPTO_RPC_IP, crypto_perams.CRYPTO_RPC_PORT)
        wallet = AuthServiceProxy(rpc_connection_CRYPTO)

        masternode_count_data= wallet.getmasternodecount()


        embed.add_field(name="Total Masternodes", value=str(masternode_count_data["total"]), inline=True)
        embed.add_field(name="MN Reward", value=str(crypto_perams.CRYPTO_REWARD)+" "+crypto_perams.CRYPTO_TICKER, inline=True)
        amount_of_rewards_per_day=86400/crypto_perams.CRYPTO_BLOCKTIME/masternode_count_data["total"]
        avg_reward=round(pow(amount_of_rewards_per_day,-1)*24,1) #change the * factor to change, base is in days per reward, solve from there
        embed.add_field(name="MN Frequency", value=str(avg_reward)+" hours", inline=True)

        reward_per_day=round(amount_of_rewards_per_day*crypto_perams.CRYPTO_REWARD,2)

        embed.add_field(name="Daily Income", value="${:.2f}\n{:.2f}".format(reward_per_day*self.price_usd,reward_per_day)+" "+crypto_perams.CRYPTO_TICKER+"\n{:.8f}฿".format(reward_per_day*self.price_btc), inline=True)
        embed.add_field(name="Monthly Income", value="${:.2f}\n{:.2f}".format(reward_per_day*self.price_usd*31,reward_per_day*31)+" "+crypto_perams.CRYPTO_TICKER+"\n{:.8f}฿".format(reward_per_day*self.price_btc*31), inline=True)
        embed.add_field(name="Yearly Income", value="${:.2f}\n{:.2f}".format(reward_per_day*self.price_usd*365,reward_per_day*365)+" "+crypto_perams.CRYPTO_TICKER+"\n{:.8f}฿".format(reward_per_day*self.price_btc*365), inline=True)

        embed.timestamp=datetime.datetime.utcnow()

        embed.set_footer(text="Last updated")
        embed.set_author(name=self.bot.user.name, url="https://github.com", icon_url=self.bot.user.avatar_url)

        await message.edit(content="",embed=embed)


def calc_converted_nethash(hash_per_sec):
    if len(str(hash_per_sec)) <= 4:
        return str(hash_per_sec)+" h/s"
    else:
        calculation = calc_suffix(len(str(hash_per_sec)))
        return str(round(hash_per_sec/float(calculation[1]), 2))+" "+calculation[0]

    return modified_value

def calc_suffix(ten_place):
    if ten_place >=5 and ten_place <=7:
        return ["kh/s", 10**3]
    elif ten_place >=8 and ten_place <=10:
        return ["Mh/s",10**6]
    elif ten_place >=11 and ten_place <=13:
        return ["Gh/s",10**9]
    elif ten_place >=14 and ten_place <=16:
        return ["Th/s",10**12]
    elif ten_place >=17 and ten_place <=19:
        return ["Th/s",10**15]
    elif ten_place >=20 and ten_place <=22:
        return ["Ph/s",10**18]
    elif ten_place >=23 and ten_place <=25:
        return ["Eh/s",10**21]
    elif ten_place >=26 and ten_place <=28:
        return ["Zh/s",10**24]
    else:
        return "ooof/s"


    return return_list


def setup(bot):
    bot.add_cog(Network_dashboard(bot))
