from discord.ext import commands
import inc

class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot):
        self.bot = bot

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(embed=inc.embederr(f'Failed to load extension {type(e).__name__} - {e}'))
        else:
            await ctx.send(embed=inc.embednorm("Successfully loaded extension"))

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(embed=inc.embederr(f'Failed to unload extension {type(e).__name__} - {e}'))
        else:
            await ctx.send(embed=inc.embednorm("Successfully unloaded extension"))

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(embed=inc.embederr(f'Failed to reload extension {type(e).__name__} - {e}'))
        else:
            await ctx.send(embed=inc.embednorm("Successfully reloaded extension"))


def setup(bot):
    bot.add_cog(OwnerCog(bot))
