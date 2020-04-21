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
    print(f'{client.user} has connected to Discord!\n')


@client.event
async def on_message(message):
    """Either sets the user's emoji's preferences, or reacts to a message"""
    if message.content[:15] == "!AutoReact.set ":
        await _set_pref(message)
    else:
        await _react(message)


async def _set_pref(message):
    """Sets a user's preference for their reaction emoji.

    Accepts an argument of a Discord message of format "!Autoreact.set {emoji}"
    Takes the emoji and sets that to be the user's preferred emoji.
    """
    user_emojis[message.author] = message.content[15:16]


async def _react(message):
    """Reacts to the given emoji with the user's preferred emoji.

    Accepts an argument of a Discord message to be reacted to.
    Checks the author's preference of emoji and reacts.
    """
    try:
        emoji = user_emojis.get(message.author, None)
        if emoji is not None:
            await message.add_reaction(emoji)
            print(
                f"{datetime.datetime.now()}: Reacted to {message.author}'s",
                f"message with {emoji}.")
    except Exception as e:
        print(f"{datetime.datetime.now()}: error reacting")
        raise

client.run(TOKEN)
