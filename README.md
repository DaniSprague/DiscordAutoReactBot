# [DiscordAutoReactBot](https://github.com/DaniSprague/DiscordAutoReactBot)

This bot automatically reacts to user's messages with their favorite emoji on Discord.

Please check [the Wiki](https://github.com/DaniSprague/DiscordAutoReactBot/wiki) for more information, including a roadmap.

## Usage

AutoReact supports several commands. To use these commands, users should direct message the bot on Discord with any of the following:

| __Prefix__ | __Command__ | __Arguments__ | __Functionality__ | __Example__ |
| --- | --- | --- | --- | --- |
| !AutoReact | .disable | *none* | Removes the user's settings | `!AutoReact.disable` |
| !AutoReact | .help | *none* | Messages the user with help info | `!AutoReact.help` |
| !AutoReact | .set | emoji | Sets the user's reaction emoji | `!AutoReact.set 🤔` |

## Functionality

Once the user sets their preferred emoji using `!AutoReact.set`, AutoReact will react to that user's messages with the set emoji in servers where AutoReact is enabled.

### Cooldowns

Anytime a message to a user is sent or a reaction is made, the cooldown timer is reset. While a cooldown is active, reactions and messages will not be sent to the user. The following table shows the cooldown times:

| Action | Cooldown (seconds) |
| --- | --- |
| Reaction to emoji | 300 |
| Help message sent | 120 |
| Error setting reaction emoji | 30 |

## Installation

In order to get AutoReact running on a local machine, the following steps should work:

1. Pull this repository onto a local machine.
2. Create the `.env` file with the private key info.
    * The `.env` file should be in the same directory as `bot.py`.
    * The format of `.env` should be two lines as follows:

    ```none
    DISCORD_TOKEN=[PRIVATE_TOKEN]

    ```

    * The private token can be found on the Discord Developer Portal

3. Install [`discord.py`](https://discordpy.readthedocs.io/en/latest/index.html), [`emoji`](https://github.com/carpedm20/emoji/), and [`python-dotenv`](https://saurabh-kumar.com/python-dotenv/) using a Python package manager.
4. Change the save location of the database within _open_db() to 'AutoReact_prod.db'.
5. Run `bot.py` from a command line.

[This article](https://realpython.com/how-to-make-a-discord-bot-python/) provides additional details on handling the Discord Developer Portal to get the bot running on a local installation. It also covers how to add the bot to a Discord server.

The wiki covers [how to create and run the docker file](https://github.com/DaniSprague/DiscordAutoReactBot/wiki/Installation).

There are plans to provide the ability to load the bot on one's own server from a hosted installation, but that are not yet ready.

## Code Styling

This project uses [YAPF](https://github.com/google/yapf) to format the code, using the config in the included `.style.yapf` file. For comments and docstrings, the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#s3.8-comments-and-docstrings) is followed.

## Thanks

This project would have been infinitely more difficult without [realpython.com's wonderful tutorial on making a Discord bot in Python](https://realpython.com/how-to-make-a-discord-bot-python/). The basic template code came from there.

Additional thanks to the maintainers and authors of all of the Python packages used in this project.
