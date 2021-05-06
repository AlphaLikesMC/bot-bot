"""
This example cog demonstrates basic usage of Lavalink.py, using the DefaultPlayer.
As this example primarily showcases usage in conjunction with discord.py, you will need to make
modifications as necessary for use with another Discord library.

Usage of this cog requires Python 3.6 or higher due to the use of f-strings.
Compatibility with Python 3.5 should be possible if f-strings are removed.
"""
import re

import discord
import lavalink
from discord.ext import commands
import time
from pytube import YouTube
import math
from discord import utils
from discord import Embed

url_rx = re.compile(r'https?://(?:www\.)?.+')


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.lavalink = lavalink.Client(734507287598727270)
        self.client.lavalink.add_node('idekidek2.herokuapp.com', 80, 'youshallnotpass', 'eu', 'default-node')  # Host, Port, Password, Region, Name
        self.client.add_listener(client.lavalink.voice_update_handler, 'on_socket_response')
        self.client.lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.client.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.client.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise commands.CommandInvokeError('You are not in a voice channel.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voice channel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            channel = guild_id
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.client._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """ Searches and plays the given song. """
        # Get the player for this guild from cache.
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        #query = query.strip('<>')
        state = player.paused

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.purple())

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        queue = player.queue
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
            embed.add_field(name=f'Default volume set to: 50', value=f'**Track played by {ctx.author}**')
        elif not player.is_playing:
            track = results['tracks'][0]
            link = track["info"]["uri"]
            yt = YouTube(f'{link}')
            thumb = yt.thumbnail_url
            min, sec = divmod(yt.length, 60) 
            
            '''remove_character = ["."]
            for c in remove_character:
                duration = duration.replace(c, ":")'''
            embed.title = 'Playing track'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            embed.add_field(name='Duration:', value=f'{"%02d:%02d" % (min, sec)}')
            embed.add_field(name=f'Default volume set to:', value=50)
            embed.set_footer(text=f'Track played by {ctx.author}')
            embed.set_thumbnail(url=f'{thumb}')
            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)
        else:
            track = results['tracks'][0]
            link = track["info"]["uri"]
            yt = YouTube(f'{link}')
            thumb = yt.thumbnail_url
            min, sec = divmod(yt.length, 60)
            embed.title = 'Track queued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            embed.add_field(name='Duration:', value=f'{"%02d:%02d" % (min, sec)}')
            embed.set_thumbnail(url=f'{thumb}')
            embed.set_footer(text=f'Track played by {ctx.author}')
            embed.add_field(name=f'Default volume set to:', value=50)

            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.set_volume(50)
            time.sleep(0.2)
            await player.play()

    '''@commands.command(aliases=['q'])
    async def queue(self, ctx, *, cmd=None):
        """Fetches the queue list. (no work proper)"""
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        queue = player.queue
        if player.is_playing and player.queue is not None:
            hek = int(len(queue))
            for i in range(hek):
                qu = queue[i]['title'] 
                embed = discord.Embed(title=f'Queue:', colour=discord.Colour.red())
                embed.description = f'{i+1}) {qu}'
                await ctx.send(embed=embed)
        elif not queue:
            await ctx.send(f'***Nothing in queue!***')

    @commands.command(aliases=['qt'])
    async def qtest(self, ctx):
        player = self.client.lavalink.player_manager.get(ctx.message.guild.id)
        queues = player.queue
        hek = int(len(queues))
        for i in range(hek):
            x = player.queue
            qu =  (str(queue.title) for queue in x)
            await self.client.wait_until_ready()
        embed = discord.Embed(title=f'Queue:', colour=discord.Colour.red())
        embed.description = f'{i+1}' + ''.join(qu)
        await ctx.send(embed=embed)

        for queue in queues:
            await ctx.send(str(queue.title))'''

    @commands.command(aliases=['qr'])
    async def remove(self, ctx, *, pos: int):
        """ Removes the requested track from queue. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        queue = player.queue
        name = queue[pos-1]['title']
        dd = queue.pop(pos-1)
        await ctx.send(f'**Removed {name} from queue!**')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, vol: int):
        """ Sets the volume to given value. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        if 0 < vol < 101:
            await player.set_volume(vol)
            em = discord.Embed(colour=discord.Colour.red())
            em.add_field(name=f'Volume set to {vol}', value=f'**Requested by {ctx.author}**')
            await ctx.send(embed=em)
        else:
            await ctx.send(f'Volume should be between 0 and 100.')

    @commands.command(aliases=['next'])
    async def skip(self, ctx):
        """ Skips the ongoing track. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        queue = player.queue
        if not queue:
            await ctx.send(f'**No more tracks left in the queue! Disconnecting.**')
            time.sleep(0.5)
            player.queue.clear()
            await player.stop()
            await self.connect_to(ctx.guild.id, None)
        else:
            await ctx.send(f'***Skipping current track!***')
            time.sleep(0.5)
            await player.skip()

    @commands.command()
    async def pause(self, ctx):
        """ Pauses the ongoing track. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        state = player.paused
        if state:
            await ctx.send("***Player already paused!***")
        elif not player.is_connected:
            await ctx.send("***Nothing to pause!***")
        elif not state:
            await player.set_pause(True)
            await ctx.send(f'***Player paused!***')

    @commands.command()
    async def resume(self, ctx):
        """ Resumes the track if paused. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)
        state = player.paused
        if state:
            await player.set_pause(False)
            await ctx.send("***Resumed player!***")
        elif not player.is_connected:
            await ctx.send("***Nothing to resume...***")
        elif not state:
            await ctx.send(f'***Player is not paused...***')
            
    @commands.command(aliases=['dc', 'stop'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voice channel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('*⃣ | Disconnected.')

    @commands.command(name='q')
    async def queue(self, ctx, page: int = 1):
        """Fetches queue list."""
        player = self.client.lavalink.player_manager.get(ctx.guild.id)

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(tite=f'Queue:', colour=discord.Color.red(), description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Music(client))