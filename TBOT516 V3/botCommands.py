#All the possible commands the bot can execute
from botDependencies import *
from botCore import *
from playerClass import *

@bot.command()
async def ping(ctx): 
    #Gets client latency and returns it in the chat that the command was entered in
    await ctx.send(f'Your ping is {round(bot.latency * 1000)} ms!')

@bot.command()
async def join(ctx):
    #Only describing once as it is semi-repatative (neet to make function for it)
    #Gets the voice channel the user is in
    userVoiceState = ctx.author.voice

    #If they arent in one then we dont run anything further
    if(userVoiceState == None):
        await ctx.send('You need to be in a vc to have the bot join.')
        return 
    #Gets the discord server's id 
    guild = ctx.guild.id

    #Checks to see if there is an audio player for the server, bot joins call if there is none
    if(not guild in listOfAudioPlayers):
        listOfAudioPlayers[guild] = AudioPlayer(guild)
        await listOfAudioPlayers[guild].joinCall(ctx)
    else:
        await ctx.send("Bot is already in call")

@bot.command()
async def disconnect(ctx):
    guild = ctx.guild.id
    userVoiceState = ctx.author.voice

    if(userVoiceState == None):
        await ctx.send('You need to be in a vc to have the bot disconnect.')
        return 
    #If the server has an audio player, delete it and have the bot leave call
    if(guild in listOfAudioPlayers):
        await listOfAudioPlayers[guild].leaveCall(ctx)
        del listOfAudioPlayers[guild]
    else:
        await ctx.send("Bot is not in a voice channel")

@bot.command(aliases = ["p"])
async def play(ctx, url: str):
    userVoiceState = ctx.author.voice

    if(userVoiceState == None):
        await ctx.send('You need to be in a vc to have the bot play a song.')
        return 

    guild = ctx.guild.id

    #Take in the user input and turn it to a list
    if(guild in listOfAudioPlayers):
        listOfSongs = url.split(', ')
        #Send the song(s) off to be played by the bot
        await listOfAudioPlayers[guild].playPlaylist(ctx, listOfSongs)
    else:
        await ctx.send("Bot is not in a voice channel")

@bot.command(aliases = ["s"])
async def skip(ctx):
    userVoiceState = ctx.author.voice

    if(userVoiceState == None):
        await ctx.send('You need to be in a vc to have the bot skip a song.')
        return 

    guild = ctx.guild.id

    if(guild in listOfAudioPlayers):
        #Skips song that is playing
        await listOfAudioPlayers[guild].skipSong(ctx)
        await ctx.send("Skiped Song")
    else:
        await ctx.send("Bot is not in a voice channel")

@bot.command()
async def queue(ctx):
    guild = ctx.guild.id

    if(guild in listOfAudioPlayers):
        #Prints the list of upcomming songs
        await listOfAudioPlayers[guild].sayNameQueue(ctx)
    else:
        await ctx.send("Bot is not in a voice channel")

@bot.command()
async def pause(ctx):
    userVoiceState = ctx.author.voice

    if(userVoiceState == None):
        await ctx.send('You need to be in a vc to pause the player.')
        return 

    guild = ctx.guild.id

    if(guild in listOfAudioPlayers):
        #Pauses audio player
        await listOfAudioPlayers[guild].pause(ctx)
    else:
        await ctx.send("Bot is not in a voice channel")

@bot.command()
async def resume(ctx):
    userVoiceState = ctx.author.voice

    if(userVoiceState == None):
        await ctx.send('You need to be in a vc to resume the player.')
        return 

    guild = ctx.guild.id

    if(guild in listOfAudioPlayers):
        #Resumes player
        await listOfAudioPlayers[guild].resume(ctx)
    else:
        await ctx.send("Bot is not in a voice channel")

@bot.command(aliases = ["rs"])
async def removeSong(ctx, songNum):
    userVoiceState = ctx.author.voice

    if(userVoiceState == None):
        await ctx.send('You need to be in a vc remove a song from the queue.')
        return 

    guild = ctx.guild.id

    if(guild in listOfAudioPlayers):
        #Removes the song in the queue position
        await listOfAudioPlayers[guild].removeSongNum(ctx, songNum)
    else:
        await ctx.send("Bot is not in a voice channel and doesn't have a que.")