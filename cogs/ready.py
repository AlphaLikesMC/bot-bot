import discord
from discord.ext import commands
from pytube import YouTube

class on_ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        #channel = self.client.get_channel(int(705791844356718594))
        #user = self.client.get_user(437044361528737812)
        #link = "https://www.youtube.com/watch?v=eEa3vDXatXg"
        #yt = YouTube(f'{link}')
        #title = yt.title
        #thumb = yt.thumbnail_url
        #embed = discord.Embed(title=f'{title}', colour=discord.Colour.red(), description=f'{link}')
        #embed.set_image(url=f'{thumb}')
        #await channel.send("**__Bot update:__** *I am stopping bot development again due to not having enough time. I might work on it later if I get time or if the other dev decides to come online. Feel free to remove the bot if your server still has it! :)*")
        #await user.send('I is on!')
        await self.client.change_presence(activity=discord.Streaming(name="Boredom", url='https://www.youtube.com/watch?v=eLo33ZsZHbY'))
        print('Bot: {0.user} is ready!'.format(self.client))

def setup(client):
    client.add_cog(on_ready(client))