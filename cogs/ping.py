import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """ Displays the bot ping."""
        embed = discord.Embed(colour=discord.Colour.dark_magenta())
        embed.add_field(name='Pong!', value=f'**{round(self.client.latency * 1000)}ms**')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ping(client))