from botCore import *
from botCommands import *
import subprocess
import sys

#if PyNaCl not present, install it
if(not importlib.util.find_spec("PyNaCl")):
    subprocess.run([sys.executable, "-m", "pip", "install", "PyNaCl"])

#Runs the bot using the token
bot.run(token)