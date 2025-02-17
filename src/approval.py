import os, shutil

import discord
import requests

from config import TMP_PATH
from utils import award_roles, to_thread

_FORWARD_URL = "https://catbox.moe/user/api.php"

class ApproveButton(discord.ui.Button):
    def __init__(self, entry_user: discord.Member):
        self.entry_user = entry_user
        super().__init__(label="Approve", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        if interaction.message is None or interaction.message.guild is None:
            return
        await award_roles(self.entry_user, interaction.message.guild.roles)
        embed = interaction.message.embeds[0]
        self.view.clear_items()
        self.view.add_item(discord.ui.Button(label="Approved!", style=discord.ButtonStyle.green, disabled=True))
        await interaction.message.edit(embed=embed, view=self.view)
        try:
            await self.entry_user.send("Your submission has been approved, well done!")
        except discord.errors.Forbidden:
            pass
        await interaction.response.defer()

class DenyButton(discord.ui.Button):
    def __init__(self, entry_user: discord.Member):
        self.entry_user = entry_user
        super().__init__(label="Deny", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        if interaction.message is None:
            return
        embed = interaction.message.embeds[0]
        self.view.clear_items()
        self.view.add_item(discord.ui.Button(label="Denied!", style=discord.ButtonStyle.red, disabled=True))
        await interaction.message.edit(embed=embed, view=self.view)
        try:
            await self.entry_user.send("We're sorry, but your submission been denied by the SDV staff. For additional info, please DM the Modmail bot.")
        except discord.errors.Forbidden:
            pass
        await interaction.response.defer()

class EntryView(discord.ui.View):
    def __init__(self, entry_user: discord.Member):
        super().__init__(timeout=None)
        self.add_item(ApproveButton(entry_user))
        self.add_item(DenyButton(entry_user))

async def post_entry(message: discord.Message, channel: discord.TextChannel):
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)

    # Want submitted text to always appear in the first embedded entry, even if there are one or more image embeds too
    if len(message.attachments) == 0:
        message_embed = discord.Embed(description=message.content, color=message.author.color)
        message_embed.add_field(name="Submitter:", value=message.author.mention)
        await channel.send(embed=message_embed, view=EntryView(message.author))
    else:
        for i, attachment in enumerate(message.attachments):
            if i == 0 and message.content != "":
                embed = discord.Embed(description=message.content, color=message.author.color)
            else:
                embed = discord.Embed(description=f"Image submission {i + 1}", color=message.author.color)
            embed.add_field(name="Submitter:", value=message.author.mention)
            filename = str(hash(attachment))
            filepath = os.path.join(TMP_PATH, filename)
            success = await download_image(attachment.url, filepath)
            if success:
                file = discord.File(filepath, filename="image.png")
                embed.set_image(url="attachment://image.png")
                await channel.send(file=file, embed=embed, view=EntryView(message.author))
    await message.delete()

@to_thread
def download_image(url: str, filename: str) -> bool:
    try:
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as outfile:
            shutil.copyfileobj(response.raw, outfile)
        del response
        return True
    except requests.exceptions.ConnectionError as err:
        print(f"Issue downloading image {url}. Aborting.")
        print(str(err))
        return False
