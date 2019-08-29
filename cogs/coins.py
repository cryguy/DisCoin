import discord
from discord.ext import commands
import inc
import mysqlhandler


class CoinCog(commands.Cog, name="Reward Stuffs"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='balance', aliases=['bal'])
    async def bal(self, ctx, *, user: discord.Member):
    # do some checks for user
        if user is not None:
            coins = mysqlhandler.getuser(user.id)
            print(coins)
        else:
            user = ctx.message.author
            coins = mysqlhandler.getuser(ctx.message.author.id)
        if coins == "ERROR":
            coins = 0
        await ctx.send(embed=inc.embednorm(str(user) + " currently has " + str(coins) + " coins left"))
    @bal.error
    async def balerr(self, ctx, error):
        user = ctx.message.author
        coins = mysqlhandler.getuser(ctx.message.author.id)
        if coins == "ERROR":
            coins = 0
        await ctx.send(embed=inc.embednorm(str(user) + " currently has " + str(coins) + " coins left"))

    @commands.command(name='pay')
    async def pay(self, ctx, user: discord.Member, amount: int):
    # do some checks for user
        coins = mysqlhandler.getuser(ctx.message.author.id)

        if coins == "ERROR":
            coins = 0
        else:
            coins = int(coins)
        if amount < 1:
            await ctx.send(
                embed=inc.embederr(str(ctx.message.author) + " You cannot send a value less than 1"))
        else:
            if coins < amount:
                await ctx.send(embed=inc.embederr(str(ctx.message.author) + " You do not have enough coins to send"))
            else:
                if mysqlhandler.changebal(ctx.message.author.id, -amount):
                    print("deducted", "giving now")
                    if mysqlhandler.changebal(user.id, amount):
                        print("gave")
                        await ctx.send(
                            embed=inc.embednorm(str(user) + " Sent " + str(amount) + " to " + user.mention))
                    else:
                        if mysqlhandler.changebal(ctx.message.author.id, amount):
                            await ctx.send(embed=inc.embederr(str(user) + " Failed to send coins to " + str(user) + " , Refunded the coins sent"))
                        else:
                            await ctx.send(embed=inc.embederr(
                                str(user) + " Something went terribly wrong, contact one of our admins to get your coins back (if you lost any)"))
    @pay.error
    async def payerr(self, ctx, error):
        await ctx.send(embed=inc.embederr(str(error)))


    @commands.command(name='addremove')
    @commands.has_any_role('taxadmin')
    async def give(self, ctx, user: discord.Member, amount: int):
    # do some checks for user
        if user is None or amount is None:
            await ctx.send(embed=inc.embederr(str(user) + " The correct parameter for this command is !!addremove @user amount"))
        else:
            if mysqlhandler.changebal(user.id, amount):
                await ctx.send(
                    embed=inc.embednorm(str(user) + " added/removed " + str(amount) + " from " + user.mention + "'s account"))

def setup(bot):
    bot.add_cog(CoinCog(bot))
