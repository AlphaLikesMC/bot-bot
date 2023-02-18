import discord 
from discord.ext import commands
import time

class announce(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['say'])
    async def announce(self, ctx, *, announcement):
        """ Announces your desired message """
        await ctx.message.delete()
        await ctx.send(f'{announcement}')
        

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            say = await ctx.send(f'Nothing to announce')
            time.sleep(1)
            await say.delete()
        else:
            await ctx.send(error)

async def setup(client):
    await client.add_cog(announce(client))