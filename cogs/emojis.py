import discord
from discord.ext import commands
from discord import utils

class emote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['e'])        
    async def emoji(self, ctx, emote):
        '''
        Sends the given nitro emote. ex- ".emote :pepega:
        :param guild: The guild to search.
        :type guild: discord.Guild
        :param emote: The full emote string to look for.
        :type emote: str
        :return:
        :rtype: discord.Emoji
        '''
        emote_name = emote.split(':')[1]
        matching_emote = None
        for emote in ctx.message.guild.emojis:
            if emote.name == emote_name:
                matching_emote = emote
        f = matching_emote 
        await ctx.send(f)

def setup(client):
    client.add_cog(emote(client))
