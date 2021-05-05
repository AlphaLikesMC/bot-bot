import discord
import random
import json
from discord.ext import commands
from youtubesearchpython import searchYoutube
import time
from pytube import YouTube
import youtube_dl

import os
import fnmatch
import subprocess

from discord.utils import get
from discord import FFmpegPCMAudio

def get_prefix(client, message):
    with open('jsons/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]
     
client = commands.Bot(command_prefix = get_prefix)
token = "NzM0NTA3Mjg3NTk4NzI3Mjcw.XxSvsA.uwnOQJoL-Hl4izoJNduaqhtperg"

for filename in os.listdir(f'cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


'''@client.event
async def on_ready():
    user = client.get_user(437044361528737812)
    await user.send('👀')
    #channel = client.get_channel("705791844356718594")
    #await channel.send('bot bot on!')
'''

client.run(token)