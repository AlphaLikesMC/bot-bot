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

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'Whoa there' in message.content:
            await message.channel.send("<@437044361528737812>")

    '''@commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.id != message.author.id:
            if 'foo' in message.content:
                await ctx.send(message.channel, 'bar')

        await self.client.process_commands(message)'''


def setup(client):
    client.add_cog(ping(client))