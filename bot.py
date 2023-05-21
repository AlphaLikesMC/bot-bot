import discord
import random
import json
from discord.ext import commands
from youtubesearchpython import searchYoutube
import time
from pytube import YouTube
import youtube_dl

import asyncio

import os
import fnmatch
import subprocess

from discord.utils import get
from discord import FFmpegPCMAudio

from aiohttp import web

def get_prefix(client, message):
    with open('jsons/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

#intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
intents = discord.Intents().all()     
 
client = commands.Bot(command_prefix = get_prefix, intents=intents)
token = "NzM0NTA3Mjg3NTk4NzI3Mjcw.GwyJgq.8QbFgW6bLabMeZW4BuIMB8ygk8Ben_dZVy9O-U"
port = 80



async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")


'''@client.event
async def on_ready():
    user = client.get_user(437044361528737812)
    await user.send('👀')
    #channel = client.get_channel("705791844356718594")
    #await channel.send('bot bot on!')
'''

async def main():
    async with client:
        await load_extensions()
        
        # Create an HTTP server to bind to the desired port
        app = web.Application()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        
        # Start the HTTP server and the Discord bot together
        await asyncio.gather(
            client.start(token),
            site.start()
        )

asyncio.run(main())

