from botDependencies import *

bot = commands.Bot(command_prefix = '.', intents = discord.Intents.all())
#Setting up the core of the bot with the prefix used to call its commands

token = os.environ.get('BotKey')
#Fetches a token needed to start the bot

listOfAudioPlayers = {}
#A list of all active audio clients across miltiple servers