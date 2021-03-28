
import discord
import os
from pathlib import Path
from dotenv import load_dotenv
from discord import Member

intents = discord.Intents.default()
client = discord.Client()

env_path = Path('..') /'Discord' / '.env'
load_dotenv(dotenv_path=env_path)

@client.event
async def on_ready():
    print('Ready!')

def status(member):
    state = member.status(member)
    return state



client.run(os.getenv('TOKEN'))



#Boilerplate: https://realpython.com/how-to-make-a-discord-bot-python/#interacting-with-discord-apis
