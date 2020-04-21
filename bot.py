"""
The main file for a bot to auto-react to user's messages on Discord.
"""

import os
import datetime

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

user_emojis = dict()

@client.event
async def on_ready():
    """The main event once the bot connects to Discord."""
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    """Either sets the user's emoji's preferences, or reacts to a message"""
    #Message must have contents "!Autoreact.set {Preferred-Emoji}"
    if message.content[:15] == "!AutoReact.set ":
        user_emojis[message.author] = message.content[15:16]
    else:
        try:
            emoji = user_emojis.get(message.author, None)
            if emoji is not None:
                await message.add_reaction(emoji)
        except Exception as e:
            print(f"{datetime.datetime.now()}: error reacting")
            raise
        else:
            print(
                f"{datetime.datetime.now()}: Reacted to {message.author}'s message",
                f"in guild {message.guild} in channel {message.channel} with",
                f"{emoji}")


client.run(TOKEN)