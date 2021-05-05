import discord
from discord.ext import commands
import timeago
from datetime import datetime

class userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gu'])
    async def getuser(self, ctx, it: int):
        """ fetches username and info from id (under development) """
        member = self.client.get_user(it)
        #info = member
        #await ctx.send(info)
        name = member.name
        discrim = member.discriminator
        created = member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        pic = member.avatar_url_as(format=None, static_format='webp', size=128)

        createdago = member.created_at
        now = datetime.now()
        nowstr = now - createdago

        embed = discord.Embed(title='User Info', colour=discord.Colour.dark_magenta())
        embed.add_field(name='Username:', value=f'{name}',inline = True)
        embed.add_field(name='Discriminator:', value=f'{discrim}',inline=True)
        embed.add_field(name='Account Created on:', value=f'{created} ({timeago.format(nowstr)})')
        embed.set_thumbnail(url=f'{pic}')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(userinfo(client))
