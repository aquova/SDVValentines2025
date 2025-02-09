import discord
import requests

from utils import award_roles

_FORWARD_URL = "https://0x0.st"
_EXPIRE_TIME = 24 * 7 # Images will expire in one week

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
            print(attachment.url)
            new_url = requests.post(_FORWARD_URL, data={"url": attachment.url, "expires": _EXPIRE_TIME})
            if new_url.ok:
                embed.set_image(url=new_url.text)
                embed.add_field(name="URL:", value=new_url.text)
            else:
                print(f"Something went wrong: {new_url.text}")
            await channel.send(embed=embed, view=EntryView(message.author))
    await message.delete()
