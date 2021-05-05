import discord
from discord.ext import commands
import timeago
from datetime import datetime

class memberinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['mi', 'ui'])
    async def memberinfo(self, ctx, member: discord.Member):
        """ fetches member info (must be in server). """
        name = member.name
        discrim = member.discriminator
        nickname = member.nick
        roles = member.roles
        joinedser = member.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        created = member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        pic = member.avatar_url_as(format=None, static_format='webp', size=128)

        createdago = member.created_at
        now = datetime.now()
        nowstr = now - createdago

        joinedago = member.joined_at
        now1 = datetime.now()
        now1str = now - joinedago

        embed = discord.Embed(title='User Info', colour=discord.Colour.dark_magenta())
        embed.add_field(name='Username:', value=f'{name}',inline = True)
        embed.add_field(name='Discriminator:', value=f'{discrim}',inline=True)
        embed.add_field(name='Nickname:', value=f'{nickname}', inline=True)
        embed.add_field(name='Account Created on:', value=f'{created} ({timeago.format(nowstr)})')
        embed.add_field(name='Joined Server on:', value=f'{joinedser} ({timeago.format(now1str)})', inline=True)
        embed.set_thumbnail(url=f'{pic}')
        await ctx.send(embed=embed)

    @memberinfo.error
    async def memberinfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f'**Unable to find member...**')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'**Please Mention a member!**')
    
def setup(client):
    client.add_cog(memberinfo(client))