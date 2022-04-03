# NormNavel.py
import os
import discord
from discord import Client, Intents, Embed
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

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

@slash.slash(
    name="test",
    description="This is just a test command, nothing more.",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="option1",
            description="choose your word!",
            required=True,
            option_type=3 # option_type 3 = string
            # choices=[
            #     create_choice(
            #         name="World!",
            #         value="world"
            #     ),
            #     create_choice(
            #         name="You!",
            #         value="you"
            #     )
            # ]
        )
    ]
)
async def test(ctx:SlashContext, option1:str):
    await ctx.send(f'Hello {option1}! channel ID test: <#958840606090735639>')
    

@commands.has_permissions(administrator=True)
@slash.slash(
    name="createrole",
    description="Create a new role for the server.",
    guild_ids=guild_ids,
    options=[
        create_option(
            name="role_name",
            description="string name of role to add.",
            required=True,
            option_type=3 # option_type 3 = string
        ),
        create_option(
            name="category",
            description="category of the role in the bot JSON file.",
            required=True,
            option_type=3 # option_type 3 = string
        )
        # create_option(
        #     name="channel",
        #     description="string name of the channel for the new role.",
        #     required=False,
        #     option_type=3 # option_type 3 = string
        # )
    ]
)
async def create_role(ctx:SlashContext, role_name:str, category:str):
    user = ctx.message.author
    await client.create_role(author.server, name=role_name)
    #await ctx.send(f'/createrole {role_name}, {category}')

@commands.has_permissions(administrator=True)
@slash.slash(name="deleterole", description="Delete an existing role from the server.", guild_ids=guild_ids)
async def test(ctx):
    await ctx.send(content="/deleterole str:roleName")



@slash.slash(name="roles", description="View the list of roles.", guild_ids=guild_ids,)
async def roles(ctx):
    await ctx.send(content="/roles optional: str:category")

# -----------------------------------------------------------------------------------------------------
@commands.has_permissions(administrator=True)
@slash.slash(
    name="editrole", 
    description="Change the name of an existing role.", 
    guild_ids=guild_ids,
    options=[
        create_option(
            name="role_to_be_edited",
            description="Choose the Role you want to edit",
            required=True,
            option_type=3, 
        )    
    ]
)
async def edit_role(ctx):
    await ctx.send(content="/editrole str:oldRoleName str:newRoleName")




@slash.slash(name="assignrole", description="Assign yourself a role.", guild_ids=guild_ids,
    options=[
        create_option(
            name="role_to_be_assigned",
            description="Choose a role to assign yourself!",
            required=True,
            option_type=3, 
        )
    ]
)
async def assign_role(ctx):
    await ctx.send(content="/assignrole str:role")




@slash.slash(name="unassignrole", description="Unassign yourself a role.", guild_ids=guild_ids,
    options=[
        create_option(
            name="role_to_be_unassigned ",
            description="Choose one of your roles that you want to unnassign",
            required=True,
            option_type=3, 
        )
    ]
)
async def unassign_role(ctx):
    await ctx.send(content="/unassignrole str:role")




@slash.slash(name="linkserver", description="link a server to a class role", guild_ids=guild_ids,
    options=[
        create_option(
            name="url_to_be_linked",
            description="Choose a server to link to your class role",
            required=True,
            option_type=3, 
        )
    ]
)
async def link_server(ctx):
    await ctx.send(content="/linkserver str:role")




@slash.slash(name="unlinkserver", description="unlink all servers from a single class role", guild_ids=guild_ids,
    options=[
        create_option(
            name="role_to_unlink",
            description="Choose a role for which you want to unlink all servers",
            required=True,
            option_type=3, 
        )
    ]
)
async def unlink_server(ctx):
    await ctx.send(content="/unlinkserver str:role")




@commands.has_permissions(administrator=True)
@slash.slash(name="nukeservers", description="unlink all servers from all class role", guild_ids=guild_ids,
    options=[
        create_option(
            name="nuclear_launch_code",
            description="Enter Nuclear Launch code to nuke server",
            required=True,
            option_type=3, 
        )
    ]
)
async def nuke_server(ctx):
    await ctx.send(content="/nukeservers")






client.run(TOKEN)