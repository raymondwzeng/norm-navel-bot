# NormNavel.py
import os

import discord
from discord import Client, Intents, Embed
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

load_dotenv()
TOKEN = os.getenv('TOKEN')
guild_ids=[959869467926622248, 958840606090735636]   #<- enter server IDs (switch to developer mode on discord and RCLick your serve -> copy ID)

#bot = commands.Bot(command_prefix='!', intents=intents)
intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(960021234052132905)
    await channel.send(
        f'Welcome {member.mention}, please go to the <#960021166213460048> channel to assign yourself roles that correspond to your classes'
    )

@slash.slash(name="test", description="This is just a test command, nothing more.", guild_ids=guild_ids)
async def test(ctx):
    await ctx.send(content="Hello World! channel ID test: <#958840606090735639>")
    


client.run(TOKEN)