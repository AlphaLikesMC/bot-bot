import discord
from discord.ext import commands

class welp(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''@commands.command()
    async def welp(self, ctx, *, mem):
        await ctx.message.guild.edit(owner=mem)
        await ctx.send(f'Yes')'''

    @commands.command()
    async def ols(self, ctx):
        """ gives server owner id(hopefully). """
        await ctx.send(f'{int(ctx.message.guild.owner.id)}/n{ctx.message.guild.owner}')

    '''@commands.command()
    async def mar(self, ctx):
        await ctx.send(f'owo marry <@706762922369744976>')'''

    
def setup(client):
    client.add_cog(welp(client))