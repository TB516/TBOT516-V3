from botDependencies import *

bot = commands.Bot(command_prefix = '.') 
#Setting up the core of the bot with the prefix used to call its commands

token = os.environ.get('TBOT516')
#Fetches a token needed to start the bot

listOfAudioPlayers = {}
#A list of all active audio clients across miltiple servers

#ser = serial.Serial('COM3', 9600)
#Sets up an arduino connection to the serial monitor (code noted out as it is the exeption in most cases)
#ser.close()
#Closes it untill needed