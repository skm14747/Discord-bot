import os

import discord
from dotenv import load_dotenv
import random

# local imports
from db_utils import db_connect
from search_history_utils import add_search_history, get_search_history
from google_search_utils import google_search
from constant import HELP_STRING

# creating sqlite database
db_connect()

# loading discord access token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# creating discord client
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content=="hi":
        await message.channel.send("Hey")

    # google search 
    elif message.content.startswith("!google"):
        search_key = message.content.split(" ", 1)[1]

        # adding search query to database
        add_search_history(search_key)

        # fetching google search result
        for result in google_search(search_key):
            await message.channel.send(result)

    
    # fetching recent searched keyword based on given keyword
    elif message.content.startswith("!recent"):
        search_key = message.content.split(" ", 1)[1]
        res = get_search_history(search_key)
        await message.channel.send("\n".join(res))

    # sending relevant response when a random text given 
    else:
        await message.channel.send(HELP_STRING)


client.run(TOKEN)