@client.command()
async def welp(ctx, *, name=None, link=None):
    if not link:
        searching = await ctx.send("**Searching...**")
        time.sleep(0.5)
        search = searchYoutube(f"{name}", offset=1, mode="dict", max_results=1)
        result = search.result()["search_result"]
        for video in result:
            link = video["link"]
        await searching.edit(content='***Found!***')
        await ctx.send(f'{link}')
    elif not name:
        link1 = f'{link}'
        await ctx.send(f'{link1}')
    else:
        await ctx.send("Error")
        
    #search = searchYoutube(f"{name}", offset=1, mode="dict", max_results=1)
    #result = search.result()["search_result"]
    #for video in result:
    #    link = video["link"]
    #await ctx.send(f'{link}')
    

@client.command()
async def stop(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()
    channel = ctx.message.author.voice.channel.id

    def on_voice_leave():
        with open('volume.json', 'r') as f:
            volume = json.load(f)

        volume.pop(str(channel))

        with open('volume.json', 'w') as f:
            json.dump(volume, f, indent=4)

    on_voice_leave()



@client.command(pass_context=True, aliases=['p'])
async def play(ctx, *, name=None, link=None):
    if not link:

        channel = ctx.message.author.voice.channel

        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        ch1 = ctx.message.author.voice.channel.id

        def on_voice_join(channel):
            with open('volume.json', 'r') as f:
                volume = json.load(f)

            volume[str(ch1)] = 100
            print("working")

            with open('volume.json', 'w') as f:
                json.dump(volume, f, indent=4)
            
        on_voice_join(channel)

        searching = await ctx.send("*Searching...*")
        time.sleep(0.5)
        search = searchYoutube(f"{name}", offset=1, mode="dict", max_results=1)
        result = search.result()["search_result"]
        for video in result:
            link = video["link"]
        await searching.edit(content='**Found!**')
        #await ctx.send(f'{link}')
        
        yt = YouTube(f'{link}')
        ys = yt.streams.filter(only_audio=True).first()
        path1 = os.path.expanduser("~")
        path = r"" + path1 +"/Music/discord"
        ys.download(path)
        vid1 = ys.title
        remove_characters = [":", ",", ".", "?", "'", "|"]

        for c in remove_characters:
            vid1 = vid1.replace(c, "")
        vid = vid1+".mp4"

        source = FFmpegPCMAudio(f'{path}/{vid}')
        player = voice.play(source)
        await searching.edit(content='***Playing...***')

        vid_title = yt.title
        dura = f'{round(yt.length / 60)} minute(s)'
        thumb = yt.thumbnail_url
        author = yt.author
        em = discord.Embed(title='Player', colour=discord.Colour.magenta())
        em.add_field(name='Title:', value=f'{vid_title}', inline=True)
        em.add_field(name='Duration:', value=f'{dura}', inline=True)
        em.add_field(name='Author:', value=f'{author}', inline=True)
        em.set_thumbnail(url=f'{thumb}')
        await ctx.send(embed=em)

        time.sleep(1)

        #os.remove(f'{path}/{vid}')

    else:
        await ctx.send("Error")

@client.command()
async def l(ctx):

     
    links = ["https://media.tenor.com/images/80064a5cb9cbf9a0e270a0ca48e62b0a/tenor.gif",
             "https://media.tenor.com/images/c869fbe58e8448115b1ccef3b93cf347/tenor.gif",
             "https://media1.tenor.com/images/ce88e2dc9538a5520ce2cb0c306324e7/tenor.gif?itemid=17400460",
             "https://media1.tenor.com/images/05a1180e8dc21845cb4a14266b14691c/tenor.gif?itemid=17327799",
             "https://media1.tenor.com/images/1b0cd28998ffbca90b6c452cd4d822b2/tenor.gif?itemid=17312947",
             "https://media.tenor.com/images/1d8ec01e6c4dc48a74224e9f5f789e6e/tenor.gif",
             "https://media.tenor.com/images/05e87b50725c72901a2f225c13453983/tenor.gif",
             "https://media.tenor.com/images/877a506ab2e28369a4835b06e3fd756c/tenor.gif"]
                          
    em = discord.Embed(colour=discord.Colour.gold())
    url = random.choice(links)
    em.set_image(url=url)
    await ctx.send(embed=em)


@client.command(aliases=['ts'])
async def tomjerry(ctx):     
    links = ["https://media.tenor.com/images/41e91aa3fd3bfbf227fe8e97945f0995/tenor.gif",
            "https://media.tenor.com/images/d178cfc2b04a596efb979b2b239facf3/tenor.gif",
            "https://media1.tenor.com/images/cdee9f6abcccb4807635621c1e16a509/tenor.gif?itemid=13983499",
            "https://media1.tenor.com/images/e1364319b3fad9f6d83abb7821cb0da6/tenor.gif?itemid=13329408",
            "https://media.tenor.com/images/5c1eaa78ebca82bca08a9a70b901d38e/tenor.gif",
            "https://media.tenor.com/images/806edb06141f596bb6f5caccb61d7b6e/tenor.gif"]

    em = discord.Embed(colour=discord.Colour.blue())
    url = random.choice(links)
    em.set_image(url=url)
    await ctx.send(embed=em)

@client.command()
async def react(ctx): 
    links = ["https://media.tenor.com/images/2f80207842c20c5281ce27cbbceeb90b/tenor.gif"]


    emb = discord.Embed(title="reaction", colour=discord.Colour.greyple())
    url = random.choice(links)
    emb.set_image(url=url)
    await ctx.send(embed=emb)

@client.command()
async def lol(ctx, *, gaali):
    if gaali == 'aji':
        gaali = discord.Embed(title='Aji lund mera', colour=discord.Colour.magenta())
        gaali.set_image(url="https://media1.tenor.com/images/a2ef63da5721cbf22b060a1b436933ba/tenor.gif?itemid=17145260")
        await ctx.send(embed=gaali)

@client.command()
async def users(ctx):
    users = ctx.message.author.voice.channel.members
    time.sleep(0.5)
    await ctx.send(f'{dict(users[4:10])} are the users in channel!')


@client.command(aliases=['woah'])
async def _volume(ctx, *, volume: int):

    voice = get(client.voice_clients, guild=ctx.message.guild)

    if not voice.is_playing:
        return await ctx.send('Nothing being played at the moment.')

    try:
        if volume > 100:
            return await ctx.send("Volume must be between 0 and 100")
    except:
        vol = volume / 100
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = vol
        await ctx.send('Volume of the player set to {}%'.format(volume))

'''      vid1 = emote
        remove_characters = [":"]

        for c in remove_characters:
            vid1 = vid1.replace(c, "")

        kay = vid1
        emojay = ctx.message.guild.emojis
        for kay in emojay:
            emole = emote.id

        emotes = self.client.get_emoji(emole) '''