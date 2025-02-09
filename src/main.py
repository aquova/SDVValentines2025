# SDV Valentine's 2025 Event Bot
# https://github.com/aquova/SDVValentines2025
# aquova, 2025

import discord

from client import client
from approval import post_entry
from config import DISCORD_KEY, ADMIN_ROLES, REDIRECT_CHANNELS
from utils import award_roles, check_roles

_APPROVE_REACTION = "💘"

@client.event
async def on_ready():
    print("Logged in as:")
    if client.user:
        print(client.user.name)
        print(client.user.id)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    if reaction.emoji == _APPROVE_REACTION and check_roles(user, ADMIN_ROLES):
        await award_roles(reaction.message.author, reaction.message.guild.roles)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.channel.id in REDIRECT_CHANNELS:
        dest = REDIRECT_CHANNELS[message.channel.id]
        channel = client.get_channel(dest)
        if channel is not None:
            await post_entry(message, channel)

client.run(DISCORD_KEY)
