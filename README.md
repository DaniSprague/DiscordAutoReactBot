# [DiscordAutoReactBot](https://github.com/DaniSprague/DiscordAutoReactBot)

This bot automatically reacts to user's messages with their favorite emoji on Discord.

__WARNING:__ AutoReact is in early development, and is only updated when @DaniSprague has time. Some functionality is still missing, although AutoReact is now considered to be at v0.3. Use this at your own risk!

## Usage

AutoReact supports several commands. To use any of these commands, users should direct message the bot on Discord with any of the following:

| __Prefix__ | __Command__ | __Arguments__ | __Functionality__ | __Example__ |
| --- | --- | --- | --- | --- |
| !AutoReact | .disable | *none* | Removes the user's settings | `!AutoReact.disable` |
| !AutoReact | .help | *none* | Messages the user with help info | `!AutoReact.help` |
| !AutoReact | .set | emoji | Sets the user's reaction emoji | `!AutoReact.set 🤔` |

## Functionality

Once the user sets their preferred emoji using `!AutoReact set`, then AutoReact will react to that user's messages with the set emoji in servers where AutoReact is enabled.

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
4. Run `bot.py` from a command line.

[This article](https://realpython.com/how-to-make-a-discord-bot-python/) provides additional details on handling the Discord Developer Portal to get the bot running on a local installation. It also covers how to add the bot to a Discord server.

There are plans to provide both a Docker Image and the ability to load the bot on one's own server from a hosted installation, but those are not yet ready.

## Roadmap

This project is still quite lacking. One goal is to get the Wiki up and running for a more formal roadmap. Until then, [the Milestones portion of the Issues tab](https://github.com/DaniSprague/DiscordAutoReactBot/milestones) should give a good idea of what is needed for each version.

Currently, the project is considered to be in v0.3.

## Code Styling

This project uses [YAPF](https://github.com/google/yapf) to format the code, using the config in the included `.style.yapf` file. For comments and docstrings, the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#s3.8-comments-and-docstrings) is followed.

## Why?

This project sprung out of the COVID-19 pandemic when @DaniSprague desired something to work on. Checking their list of ideas, they saw an auto-reacting Discord bot listed. They thought it would be a most excellent idea as it would improve their Python skills and help them learn how to work with APIs (even if it was entirely wrapped in a Python package).

As to why the project idea came into existence in the first place, there was a joke about emojis and wholesomeness in a Discord chat. It is not a very deep story.

## Thanks

This project would have been infinitely more difficult without [realpython.com's wonderful tutorial on making a Discord bot in Python](https://realpython.com/how-to-make-a-discord-bot-python/). The basic template code came from there.

Additionally, shout-out to the maintainers and authors of all of the Python packages used in this project.
