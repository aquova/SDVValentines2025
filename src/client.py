import discord
from discord.ext import commands

class DiscordClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='$', intents=intents)

client = DiscordClient()
