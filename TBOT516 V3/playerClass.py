from botDependencies import *
from botCore import *

async def getArduinoOutput():
    #Opens the serial port from earlier
    #ser.open()
    #Gets the newest line
    #serialOut = ser.readline()
    #Closes the port
    #ser.close()

    #Turn it from a byte to string, then removes "Whitespace"
    #volumeNum = serialOut.decode().strip()
    #Turns the string to a float to be set as the volume
    #volumeNum = float(volumeNum)
    
    return volumeNum

class AudioPlayer():
    def __init__(self, guild):
        #Constructs object and sets vars
        self.voice = None
        self.playlist = []
        self.queue = []
        self.guildId = guild
        self.ytdl_opts = {
            'outtmpl' : f'{self.guildId} song.mp3',
            'format': 'bestaudio/best',
            }

    async def updateVoice(self, ctx):
        #Updates voice
        return get(bot.voice_clients, guild = ctx.guild)

    async def joinCall(self, ctx):
        #Joins call
        voiceChannel = ctx.author.voice
        await voiceChannel.channel.connect()
        self.voice = await self.updateVoice(ctx)

    async def leaveCall(self, ctx):
        #Leaves call
        await ctx.voice_client.disconnect()

    async def setupListOfUrls(self, listOfSongs):
        listOfUrls = []
        #Loops around the list of songs added
        for i in range(len(listOfSongs)):
            #Checks to see if list item is a url or if it needs to be converted to one
            if(await self.isUrl(listOfSongs[i])):
                listOfUrls.append(listOfSongs[i])
                continue
            else:
                #This converts it to a url
                listOfUrls.append(await self.convertToUrl(listOfSongs[i]))
        return listOfUrls

    async def isUrl(self, itemToCheck):
        #Slices the first 5 letters of the string to check
        itemToCheck = itemToCheck[0:5]

        #Checks to see if the HTTPS is in the string
        if(itemToCheck == "https"):
            return True
        else:
            return False

    async def   convertToUrl(self, nameToConvert):
        #Takes the name of the song and searches it on youtube
        results = YoutubeSearch(nameToConvert, max_results=1).to_dict()
        #Gets the video id
        urlSuffix = results[0]["url_suffix"]
        #Uses the video id to create a link
        songUrl = f'https://www.youtube.com{urlSuffix}'

        return songUrl

    async def makePlaylist(self, voice, listOfUrls, ctx):
        #Checks to see if it needs to make a new playlist or add to an existing one
        if(self.playlist == []):
            #If creating, then loop around the list and add each link
            for i in range(len(listOfUrls)):
                self.playlist.append(listOfUrls[i])

            #Randomizes the playlist to spice things up
            random.shuffle(self.playlist)

            #Updates the queue that is shown to users
            await self.updateNameQueue([])

            await ctx.send("Set up playlist")

            return False

        else:
            tempPlaylist = []
            #Loops through songs being added and adds them to a seperate playlist 
            for i in range(len(listOfUrls)):
                tempPlaylist.append(listOfUrls[i])

            #Shuffles the seperate playlist
            random.shuffle(tempPlaylist)

            #Adds the songs of the seperate playlist to the main playlist
            for j in range(len(tempPlaylist)):
                self.playlist.append(tempPlaylist[j])

            #Updates the queue being shown to the user
            await self.updateNameQueue(tempPlaylist)

            await ctx.send("Added Song(s)")

            return True

    async def updateNameQueue(self, tempPlaylist):
        #Checks to see if adding songs to the visual queue or making a new one
        if(tempPlaylist == []):
            #Loops around the main playlist
            for i in range(len(self.playlist)):
                #Allows us to download the information needed to make the queue
                #Gets name of song
                songName = yt_dlp.YoutubeDL(self.ytdl_opts).extract_info(self.playlist[i], download=False)['title']
                    #Retreaves the name of the song
                    #songName = ydl.extract_info(self.playlist[i], download=False)['title']
                #Adds it to queue
                self.queue.append(songName)
        else:
            #Loops around list of songs being added
            for i in range(len(tempPlaylist)):
                #Allows us to download the information needed to make the queue
                songName = yt_dlp.YoutubeDL(self.ytdl_opts).extract_info(tempPlaylist[i], download=False)['title']
                    #Retreaves the name of the song
                    #songName = ydl.extract_info(tempPlaylist[i], download=False)['title']
                #Adds sond to queue 
                self.queue.append(songName)

    async def playPlaylist(self, ctx, listOfSongs):
        #Updates the voice connection
        self.voice = await self.updateVoice(ctx)

        #Sets up list of URLS
        listOfUrls = await self.setupListOfUrls(listOfSongs)

        #Uses the list of URLS to make a playlist and then determine if songs are being added or not
        addingSongs = await self.makePlaylist(self.voice, listOfUrls, ctx)
    
        if(addingSongs == True):
            #Ends this function if songs are being added
            return
        
        k = 0

        #Sets up loop to loop through the playlist
        while(k <= len(self.playlist)):
            #If the bot is playing audio or if its paused, wait for it to end/resume
            await self.waitForAudioEnd(self.voice)

            try:
                #Removes the song file if it exists
                os.remove(f"{self.guildId} song.mp3")
                print("Deleted song.")
            except WindowsError:   
                print("The file doesnt exist.")
        
            if(not self.voice.is_connected()):
                #If the voice isnt connected, stop looping
                await ctx.send("Ended audio stream because bot was disconnected")
                print("Stoped player")
                break

            if(k > 0):
                #If the song isnt the first one in the playlist, remove the first song from the queue
                del self.queue[0]

            if(k == len(self.playlist)):
                #If final song has finished playing and is removed, then cut the loop
                break

            #Plays the song
            await self.playSong(self.voice, self.playlist[k], ctx)

            k += 1
    
        self.playlist.clear()
        self.queue.clear()

    async def waitForAudioEnd(self, voice):
        #Waits for the audio to be done or for the player to be unpaused
        while(voice.is_playing() or voice.is_paused()):
            #Uses arduino to get the volume
            #volumeNum = await getArduinoOutput()
            
            #Sets the volume to the arduino output
            #voice.source.volume = volumeNum

            #Wait IN THIS FUNCTION ONLY, value can be ajusted depending on audio quality
            await asyncio.sleep(10)
        
    async def playSong(self, voice, url, ctx):
        #Uses the settings for the player to download the audio
        yt_dlp.YoutubeDL(self.ytdl_opts).download([url])
        #youtube_dl.YoutubeDL(self.ytdl_opts) as ydl:
            #ydl.download([url])

        #Plays the downloaded audio through the bot
        voice.play(discord.FFmpegPCMAudio(f'{self.guildId} song.mp3'))

        #self.voice.source = discord.PCMVolumeTransformer(self.voice.source)

        await ctx.send(f"Now playing {self.queue[0]}")

    async def sayNameQueue(self, ctx):
        #If the queue is empty, states it
        if(self.queue == []):
            await ctx.send("The queue is empty!")
            return

        #Creates an embed object to add the song names to
        queueEmbed = discord.Embed()

        #loops through the queue
        for j in range(len(self.queue)):
            if(j == 0):
                #Adds a field for the current song with its information
                queueEmbed.add_field(name = "Playing now", value = self.queue[j], inline = False)
            elif (j > 0):
                #Adds upcoming songs to embed
                queueEmbed.add_field(name = f"{j}.", value = self.queue[j], inline = False)
    
        #Sends the embed of the queue
        await ctx.send(embed = queueEmbed)

    async def skipSong(self, ctx):
        self.voice = await self.updateVoice(ctx)

        #Stops the song from playing, causing the bot to move on to the next song
        self.voice.stop()

    async def pause(self, ctx):
        self.voice = await self.updateVoice(ctx)

        #Pauses audio feed
        self.voice.pause()

    async def resume(self, ctx):
        self.voice = await self.updateVoice(ctx)

        if(self.voice.is_Paused()):
            #If the player is paused, resume it
            self.voice.resume()
        else:
            ctx.send("Bot is not paused")

    async def removeSongNum(self, ctx, num):
        try:
            #Takes in number and turns to int
            num = int(num)
        except ValueError:
            #If it cant, then send the error saying it isnt an int to the user
            await ctx.send(f"{num} is not an int.")
            return

        if(num <= 0):
            #If the number is negative, then say its invalad
            await ctx.send(f"{num} is not a valad queue position.")
        else:
            #Removes the song from both playlists
            del self.playlist[num]
            del self.queue[num]

            await ctx.send(f"Removed song in spot {num}.")