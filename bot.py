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
    if message.content[:10] == "!AutoReact" and \
        type(message.channel) == discord.DMChannel:
        if message.content[11:15] == "set ":
            await _set_pref(message)
        elif message.content[11:16] == "help":
            await _help(message)
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

async def _help(message):
    """Provides a help dialogue for the user

    Accepts the input of a message to reply to.
    Prints out a help dialogue.
    """
    bot_author = "Vawqer#6022"
    help_dialogue = f"Hello! This is Discord bot made by {bot_author}. " +\
        "This bot will automatically react to any messages with a user's " +\
        "favorite emoji for those users who opt in. This will only work" +\
        " in servers where the bot is installed.\n\n" +\
        "The commands are as follows:\n" +\
        "'!AutoReact.help' - prints a help message\n"+\
        r"'!AutoReact.set {emoji}' - set the preferred reaction emoji"+"\n" +\
        "\nHave a nice day!"
    await message.author.send(help_dialogue)

client.run(TOKEN)
