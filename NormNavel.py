# NormNavel.py
import os

import discord
from discord import Client, Intents, Embed
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

load_dotenv()
TOKEN = os.getenv('TOKEN')
guild_ids=[959869467926622248]

#bot = commands.Bot(command_prefix='!', intents=intents)
intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(959869741122584626)
    await channel.send(
        f'Hi {member.mention}, welcome to The Shop!'
    )

@slash.slash(name="test", description="This is just a test command, nothing more.", guild_ids=guild_ids)
async def test(ctx):
    await ctx.send(content="Hello World!")

client.run(TOKEN)