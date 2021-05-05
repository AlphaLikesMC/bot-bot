import discord
from discord.ext import commands
import time
from datetime import datetime

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''@commands.command(aliases=['bu'])
    async def banlist(self, ctx):
        bans = await ctx.message.guild.bans()
        banscount = int(len(bans))
        for i in range(banscount):
            l = i + 1

        for ban in bans:
            x = f'{l}'.join(str(ban.user))
            embed = discord.Embed(title=f'Banned users', description=x, colour=discord.Colour.orange())
            await ctx.send(embed=embed)'''

    @commands.command()
    @commands.is_owner()
    async def ban(self, ctx, *, member: discord.Member):
        """ bans given member """
        ban = await ctx.message.guild.ban(user=member)
        await ctx.send(f'banned ``{member}`` from {ctx.message.guild}')

    @commands.command()
    @commands.is_owner()
    async def unban(self, ctx, *, member):
        """ unbans given member """
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'unbanned ``{user}`` from the server!')
            else:
                await ctx.send(f'Member not found in banned users list!')

    """@commands.command(aliases=['t'])
    async def _test(self, ctx):
        bans = await ctx.message.guild.bans()
        await ctx.send(bans)"""

    @commands.command(aliases=['bl'])
    async def banlist(self, ctx):
        """shows all the members banned from server."""
        x = await ctx.message.guild.bans()
        xcount = int(len(x))
        a = (str(y.user) for y in x)
        b = (str(int(y.user.id)) for y in x)
        
        x = f'\n'.join(a)
        embed = discord.Embed(title = "List of Banned Members", description=x, color = 0xffd700)
        await ctx.send(embed = embed)
        
def setup(client):
    client.add_cog(admin(client))