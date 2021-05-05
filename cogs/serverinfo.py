import discord
from discord.ext import commands

class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['si'])
    async def serverinfo(self, ctx):
        """ Shows server details. """

        def filterBotsOnly(member):
            return member.bot

        Name = ctx.message.guild.name
        Reg = ctx.message.guild.region
        Server_id = ctx.message.guild.id

        People = int(len(ctx.message.guild.members))
        MembersInServ = ctx.message.guild.members
        botsinserv = list(filter(filterBotsOnly, MembersInServ))
        botsinserv_count = len(botsinserv)
        usersinserv = People - botsinserv_count

        desc = ctx.message.guild.description
        ch = int(len(ctx.message.guild.text_channels))
        voicech = int(len(ctx.message.guild.voice_channels))
        own = ctx.message.guild.owner
        create = ctx.message.guild.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p")
        roles = int(len(ctx.message.guild.roles))
        banners = ctx.message.guild.icon_url_as(format=None, static_format='webp', size=128)

        e = discord.Embed(title='Server Info',colour=discord.Colour.red())
        e.set_thumbnail(url=f'{banners}')
        e.add_field(name=u"\u200B", value=f'Name: {Name}\nRegion: {Reg}\nID: {Server_id}\nDescription: {desc}\nCreated on: {create} UTC\nCreated by: {own}\nNo. of channels: {ch}\nNo. of voice channels: {voicech}\nNo. of members: {People} ({usersinserv} Users, {botsinserv_count} Bots)\nNo. of roles: {roles}')
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(serverinfo(client))