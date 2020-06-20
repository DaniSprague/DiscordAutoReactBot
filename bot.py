"""
The main file for a bot to auto-react to user's messages on Discord.
"""

import datetime
import os
import json

import discord
from dotenv import load_dotenv

client = discord.Client()

@client.event
async def on_ready():
    """The main event once the bot connects to Discord."""
    #Adds a help instruction by the bot's name in the users sidebar
    help_instruction = discord.Game("PM '!AutoReact.help'")
    await client.change_presence(activity = help_instruction)
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
        elif message.content[11:19] == "disable":
            await _disable(message)
    else:
        await _react(message)


async def _set_pref(message):
    """Sets a user's preference for their reaction emoji.

    Accepts an argument of a Discord message of format "!Autoreact.set {emoji}"
    Takes the emoji and sets that to be the user's preferred emoji.
    """
    user_emojis[message.author.id] = message.content[15:16]
    await _save_emojis()

async def _disable(message):
    """
    Removes a user's preference for their reactions emoji.

    Accepts an argument of a Discord message of format "!AutoReact.disable".
    Reads who the user is and removes their entry from the preferences
    """
    try:
        del user_emojis[message.author.id]
        await _save_emojis()
    except KeyError:
        ""

async def _react(message):
    """Reacts to the given emoji with the user's preferred emoji.

    Accepts an argument of a Discord message to be reacted to.
    Checks the author's preference of emoji and reacts.
    """
    try:
        emoji = user_emojis.get(message.author.id, None)
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
        "'!AutoReact.disable' - removes the emoji preference, disabling the bot for the user\n" +\
        "'!AutoReact.help' - prints a help message\n" +\
        r"'!AutoReact.set {emoji}' - set the preferred reaction emoji"+"\n" +\
        "\nHave a nice day!"
    await message.author.send(help_dialogue)

async def _save_emojis():
    """
    Saves the emoji preferences from a dictionary format into the database.

    Returns nothing.
    """
    with open('user_emojis.json', 'w') as f:
        json.dump(user_emojis, f)

def _load_emojis():
    """
    Loads the emoji preferences into a dictionary format from the database.

    Returns the dictionary containing all the emoji preferences.
    """
    try:
        with open('user_emojis.json', 'r') as f:
            temp_dict = json.load(f)
            # Changes the loaded string keys to integers.
            # Note that json.load does have a parse_int parameter, but I failed to get it working
            temp_dict_keys = list(temp_dict.keys())
            for key in temp_dict_keys:
                temp_dict[int(key)] = temp_dict[key]
                del temp_dict[key]
            return temp_dict
    #Handles case where database has not been created yet
    except FileNotFoundError:
        user_emojis = dict()
        with open('user_emojis.json', 'w') as f:
            json.dump(user_emojis, f)
        return _load_emojis()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

user_emojis = _load_emojis()

client.run(TOKEN)
