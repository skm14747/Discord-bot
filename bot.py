import os

import discord
from dotenv import load_dotenv
import random

# local imports
from db_utils import db_connect
from search_history_utils import add_search_history, get_search_history
from google_search_utils import google_search
from constant import HELP_STRING

db_connect()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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

    elif message.content.startswith("!google"):
        search_key = message.content.split(" ", 1)[1]
        add_search_history(search_key)
        for result in google_search(search_key):
            await message.channel.send(result)

    elif message.content.startswith("!recent"):
        search_key = message.content.split(" ", 1)[1]
        res = get_search_history(search_key)
        await message.channel.send("\n".join(res))
    
    else:
        await message.channel.send(HELP_STRING)


client.run(TOKEN)