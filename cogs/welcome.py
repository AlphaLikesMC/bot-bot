import discord
from discord.ext import commands
import json

class WelcomeMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases= ['swm', 'welmsg'])
    async def setwelcomemessage(self, ctx, *, welmsg):
        """ Set your server's welcome message. """
        with open('jsons/welmsgs.json', 'r') as f:
            msg = json.load(f)

        msg[str(ctx.message.guild.id)] = welmsg

        with open('jsons/welmsgs.json', 'w') as f:
            json.dump(msg, f, indent=4)

        em = discord.Embed(title='Welcome message successfully set!', colour=discord.Colour.magenta())
        em.add_field(name='Welcome Message set to:', value=f'{welmsg}')
        await ctx.send(embed=em)

    @commands.command(aliases= ['lm'])
    async def setleavemsg(self, ctx, *, levmsg):
        """ Set your server's goodbye message. """
        with open('jsons/levmsgs.json', 'r') as f:
            msg = json.load(f)

        msg[str(ctx.message.guild.id)] = levmsg

        with open('jsons/levmsgs.json', 'w') as f:
            json.dump(msg, f, indent=4)

        em = discord.Embed(title='Leave message succesfully set!', colour=discord.Colour.green())
        em.add_field(name='Leave Message set to:', value=f'{levmsg}')
        await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="join-and-leave")

        def get_joinmsg():
            with open('jsons/welmsgs.json', 'r') as f:
                msg = json.load(f)

            return msg[str(member.guild.id)]

        fmt = f'<@{member.id}> {get_joinmsg()}'
        await channel.send(fmt)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name="join-and-leave")

        def get_leavemsg():
            with open('jsons/levmsgs.json', 'r') as f:
                msg = json.load(f)

            return msg[str(member.guild.id)]

        fmt = f'<@{member.id}> {get_leavemsg()}'
        await channel.send(fmt)

    

async def setup(client):
    await client.add_cog(WelcomeMessage(client))