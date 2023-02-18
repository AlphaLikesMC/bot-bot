import discord
from discord.ext import commands
import timeago
from datetime import datetime, timezone

class userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ui'])
    async def getuser(self, ctx, *, user: discord.User=None):
        """ fetches username and info from id. """
        try:
            if not user:
                usr = ctx.author.name
                idr = ctx.author.id
                descr = ctx.author.discriminator
        
                created = ctx.author.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
                pic = ctx.author.avatar

                createdago = ctx.author.created_at
                now = datetime.now(timezone.utc)
                nowstr = now - createdago

                embed = discord.Embed(title='User Info', colour=discord.Colour.dark_magenta())
                embed.add_field(name='Username:', value=f'{usr}',inline = True)
                embed.add_field(name='Discriminator:', value=f'{descr}',inline=True)
                embed.add_field(name='ID:', value=f'{idr}', inline=True)
                embed.add_field(name='Account Created on:', value=f'{created} ({timeago.format(nowstr)})')
                
                if pic is None:
                    embed.set_thumbnail(url='https://archive.org/download/discordprofilepictures/discordblue.png')
                else:
                    pic = ctx.author.avatar.replace(format=None, static_format='webp', size=128)
                    embed.set_thumbnail(url=f'{pic}')
                await ctx.send(embed=embed)
            else:
                usr = user.display_name
                idr = user.id
                descr = user.discriminator

                created = user.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
                pic = user.avatar

                createdago = user.created_at
                now = datetime.now(timezone.utc)
                nowstr = now - createdago

                embed = discord.Embed(title='User Info', colour=discord.Colour.dark_magenta())
                embed.add_field(name='Username:', value=f'{usr}',inline = True)
                embed.add_field(name='Discriminator:', value=f'{descr}',inline=True)
                embed.add_field(name='ID:', value=f'{idr}', inline=True)
                embed.add_field(name='Account Created on:', value=f'{created} ({timeago.format(nowstr)})')
                if pic is None:
                    embed.set_thumbnail(url='https://archive.org/download/discordprofilepictures/discordblue.png')
                else:
                    pic = user.avatar.replace(format=None, static_format='webp', size=128)
                    embed.set_thumbnail(url=f'{pic}')
                await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(err)

    @getuser.error
    async def getuser_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('**Error finding user...**')

async def setup(client):
    await client.add_cog(userinfo(client))
