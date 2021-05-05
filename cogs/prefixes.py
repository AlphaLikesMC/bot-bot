import discord
from discord.ext import commands
import json

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('jsons/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = ".",

        with open('jsons/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        with open('jsons/welmsgs.json', 'r') as f:
            msg = json.load(f)

        msg[str(guild.id)] = "has joined the server! Welcome!"

        with open('jsons/welmsgs.json', 'w') as f:
            json.dump(msg, f, indent=4)

        with open('jsons/levmsgs.json', 'r') as f:
            msg = json.load(f)

        msg[str(guild.id)] = "has left the server! Goodbye!"

        with open('jsons/levmsgs.json', 'w') as f:
            json.dump(msg, f, indent=4)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('jsons/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('jsons/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        with open('jsons/welmsgs.json', 'r') as f:
            msg = json.load(f)

        msg.pop(str(guild.id))

        with open('jsons/welmsgs.json', 'w') as f:
            json.dump(msg, f, indent=4)

        with open('jsons/levmsgs.json', 'r') as f:
            msg = json.load(f)
        
        msg.pop(str(guild.id))

        with open('jsons/levmsgs.json', 'w') as f:
            json.dump(msg, f, indent=4)

    @commands.command()
    async def prefix(self, ctx, prefix):
        """ Set a custom prefix for your server"""
        with open('jsons/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix ,

        with open('jsons/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        emb = discord.Embed(title='Prefix changed!', colour=discord.Colour.green())
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(prefix(client))