import discord
from discord.ext import commands

class avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, user: discord.User=None):
        """ Fetches a user's avatar (Must be in server- no need anymore)."""
        try:
            if not user:
                usr = ctx.author.name
                idr = ctx.author.id
                descr = ctx.author.discriminator
                embed = discord.Embed(colour=discord.Colour.green())
                embed.add_field(name=f'{usr}#{descr}', value=f'ID: {idr}')
                img=ctx.author.avatar
                if img is None:
                    embed.set_image(url='https://archive.org/download/discordprofilepictures/discordblue.png')
                else:
                    embed.set_image(url=f'{img}')
                
                await ctx.send(embed=embed)
            else:
                usr = user.display_name
                idr = user.id
                descr = user.discriminator
                embed = discord.Embed(colour=discord.Colour.green())
                embed.add_field(name=f'{usr}#{descr}', value=f'ID: {idr}')
                #img = user.avatar_url_as(format=None, static_format='webp', size=1024)
                img = user.avatar
                if img is None:
                    embed.set_image(url='https://archive.org/download/discordprofilepictures/discordblue.png')
                else:
                    img = user.avatar.replace(format=None, static_format='webp', size=1024)
                    embed.set_image(url=f'{img}')
                #embed.set_image(url=f'{img}')
                await ctx.send(embed=embed)
        except Exception as err:
            await ctx.send(err)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('**Error finding user...**')

async def setup(client):
    await client.add_cog(avatar(client))