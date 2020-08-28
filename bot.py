"""Discord AutoReact Bot

Reacts to users' messages with their favorite emoji.

Activates and connects to Discord. Allows users to set their favorite emoji,
after which the bot will react to the user's messages with their favorite emoji
for every channel in which the bot and the user are both members.

This script depends on the discord and dotenv modules. See README.md for more.
"""

import datetime as dt
import os
import json
import logging

import discord
from dotenv import load_dotenv
import emoji as em

# Discord logging set-up (basic logging code from the discord.py documentation)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='a')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Bot logging set-up
bot_logger = logging.getLogger('AutoReact')
bot_logger.setLevel(logging.INFO)
bot_logger.addHandler(handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s: %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S'))
console_handler.setLevel(logging.INFO)
bot_logger.addHandler(console_handler)

client = discord.Client()

# Discord calls


@client.event
async def on_disconnect():
    """Handles logging when the client disconnects.

    Args:
        None

    Returns:
        None
    """

    bot_logger.error('Client disconnected!')


@client.event
async def on_message(message):
    """Handles functionality whenever a message visible to AutoReact is seen.

    If the message is a command in a DM, then the command is appropriately 
    handled. Otherwise, the bot attempts to react to the message.

    Args:
        message: The discord.Message object representing the message triggering
            the event.

    Returns:
        None
    """

    bot_logger.debug(f"Message received with contents '{message.content}'.")
    if message.content[:10] == "!AutoReact" and \
        type(message.channel) == discord.DMChannel:
        bot_logger.debug(
            (f'Command recieved from {message.author} on channel '
             f"{message.channel} with contents '{message.content}'."))
        if message.content[11:15] == "set ":
            await _set_pref(message)
        elif message.content[11:16] == "help":
            await _help(message)
        elif message.content[11:19] == "disable":
            await _disable(message)
        else:
            bot_logger.debug(f"{message.author} sent an invalid command.")
    else:
        await _react(message)


@client.event
async def on_ready():
    """Handles the startup once the bot connects to Discord.

    Sets the bot's status and prints a success message to console.

    Args:
        None

    Returns:
        None
    """

    #Adds a help instruction by the bot's name in the users sidebar
    help_instruction = discord.Game("PM '!AutoReact.help'")
    await client.change_presence(activity=help_instruction)
    bot_logger.info(f'{client.user} has connected to Discord!\n')


@client.event
async def on_resumed():
    """Handles the logging when connection is resumed after a disconnect.

    Args:
        None

    Returns:
        None
    """
    bot_logger.ERROR('Client reconnected!')


# Commands


async def _disable(message):
    """Disables the bot for a user by removing their emoji preference.

    Args:
        message: A Discord.message object representing a message written by the 
        user for which the bot will be disabled.

    Returns:
        None
    """

    try:
        del user_emojis[message.author.id]
        bot_logger.debug((f"{message.author}'s ({message.author.id}) emoji "
                          "deleted from dictionary."))
        await _save_emojis()
    except KeyError:
        ""


async def _help(message):
    """Provides a help dialogue for the user.

    Direct messages a user sending a message requesting help with the help 
    dialogue for the bot.

    Args:
        message: A discord.Message object to reply to.

    Returns:
        None
    """

    bot_author = "Vawqer#6022"
    help_dialogue = (
        f"Hello! This is Discord bot made by {bot_author}. "
        "This bot will automatically react to any messages with a user's "
        "favorite emoji for those users who opt in. This will only work"
        " in servers where the bot is installed.\n\n"
        "The commands are as follows:\n"
        "'!AutoReact.disable' - removes the emoji preference, disabling the bot"
        " for the user\n"
        "'!AutoReact.help' - prints a help message\n"
        r"'!AutoReact.set {emoji}' - set the preferred reaction emoji"
        "\n"
        "\nHave a nice day!")
    if not (await _needs_cooldown(message.author.id, 120)):
        await message.author.send(help_dialogue)
        last_message[message.author.id] = dt.datetime.now()
        bot_logger.debug((f'Sent help dialogue to {message.author} in '
                          f'{message.channel}.'))


async def _set_pref(message):
    """Sets a user's preference for their reaction emoji.

    Takes the emoji within a message and sets that to be the user's preferred 
    emoji for reactions.

    Args:
        message: A discord.Message object with contents of 
            format "!Autoreact.set {emoji}".

    Returns:
        None
    """

    emoji = message.content[15:16]
    if em.emoji_count(emoji) == 1:
        user_emojis[message.author.id] = emoji
        await _save_emojis()
        bot_logger.debug((f"Set {message.author}'s ({message.author.id}) emoji "
                          f'preference as {emoji}.'))
    elif not (await _needs_cooldown(message.author.id, 30)):
        await message.author.send(f'"{emoji}" is not an emoji!')
        last_message[message.author.id] = dt.datetime.now()
        bot_logger.debug((f"{message.author} sent invalid emoji '{emoji}' "
                          "in attempting to set their emoji. No emoji set."))


# Core functions


async def _react(message):
    """Reacts to the given message with the user's preferred emoji.

    The message's author's preference of emoji is checked. If a preference has
    been set, then the message is reacted to with the preferred emoji. 
    Otherwise, no reaction is used.

    Args:
        message: A discord.Message object representing the message that will
            recieve a reaction.

    Returns:
        None

    Raises:
        Exception: An error occured in reacting (possibly from an invalid 
            emoji in use).
    """

    try:
        if not (await _needs_cooldown(message.author.id, 300)):
            emoji = user_emojis.get(message.author.id, None)
            if emoji is not None:
                await message.add_reaction(emoji)
                last_message[message.author.id] = dt.datetime.now()
                bot_logger.info((f"Reacted to {message.author}'s message "
                                 f'with {emoji}.'))
    # Exception reached if invalid emoji is used (should not happen anymore)
    except Exception as e:
        bot_logger.warning('Error adding reaction to message')
        bot_logger.debug(
            (f'Error "{repr(e)}" reached in attempting to react to '
             f"{message.author}'s ({message.author.id}) message in "
             f'{message.channel} with emoji '
             f'"{user_emojis.get(message.author.id, None)}".'))


# Database functions


def _load_emojis():
    """Loads the emoji preferences from the database.

    Args:
        None

    Returns:
        A dictionary with keys being (integer) uuid's of Discord users and 
        values being the (string) emoji preference of the user.
    """

    try:
        with open('user_emojis.json', 'r') as f:
            temp_dict = json.load(f)
            # Changes the loaded string keys to integers.
            # Note that json.load does have a parse_int parameter, however it
            # did not appear to be working for this.
            temp_dict_keys = list(temp_dict.keys())
            for key in temp_dict_keys:
                temp_dict[int(key)] = temp_dict[key]
                del temp_dict[key]
                bot_logger.debug((f"Loaded {key}'s preferences into memory."))
            bot_logger.info('Loaded preferences into memory from database.')
            return temp_dict
    # Handles case where database has not been created yet
    except FileNotFoundError:
        bot_logger.debug('Database not found.')
        user_emojis = dict()
        with open('user_emojis.json', 'w') as f:
            json.dump(user_emojis, f)
        bot_logger.debug('Database created.')
        return _load_emojis()


async def _save_emojis():
    """Saves the emoji preferences from memory into the database.

    Args:
        None

    Returns:
        None
    """

    with open('user_emojis.json', 'w') as f:
        json.dump(user_emojis, f)
    bot_logger.debug('Emoji preferences saved to database.')


# Helper functions


async def _needs_cooldown(user, cooldown):
    """Checks if a user needs a cooldown

    Args:
        user: The UUID of the user to check.
        cooldown: An integer representing time in seconds of the cooldown.

    Returns:
        A boolean of value True if the user needs a cooldown. False otherwise.
    """

    return (dt.datetime.now() - last_message[user]).total_seconds() < cooldown \
        if user in last_message else False


# Start-up functionality

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

user_emojis = _load_emojis()

# Used for cooldown
last_message = dict()

client.run(TOKEN)
