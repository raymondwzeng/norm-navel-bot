# NormNavel.py
import os

import interactions
from dotenv import load_dotenv
from discord.ext import commands
from NormNavelJSON import *

load_dotenv()
TOKEN = os.getenv('TOKEN')
guild_ids=[959869467926622248, 958840606090735636]   #<- enter server IDs (switch to developer mode on discord and RCLick your serve -> copy ID)

client = interactions.Client(token = TOKEN)
httpClient = interactions.HTTPClient(token = TOKEN)
guild = None

@client.event
async def on_ready():
    #Load the JSON file into NormNavelJSONTest's globals. Please do not remove this.
    load_initial()
    global guild
    data = await httpClient.get_guild(959869467926622248)
    guild = interactions.Guild(**data)
    guild._client = httpClient
    print(f'{client.me.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    channel = client.get_channel(960021234052132905)
    await channel.send(
        f'Welcome {member.mention}, please go to the <#960021166213460048> channel to assign yourself roles that correspond to your classes'
    )

# @client.command(
#     name="test",
#     description="This is just a test command, nothing more.",
#     scope=guild_ids,
#     options=[
#         interactions.Option(
#             name="option1",
#             description="choose your word!",
#             required=True,
#             type=interactions.OptionType.STRING
#         )
#     ]
# )
# async def test(ctx: interactions.CommandContext, option1:str):
#     await ctx.send(f'Hello {option1}! channel ID test: <#958840606090735639>')
    

@commands.has_permissions(administrator=True)
@client.command(
    name="createrole",
    description="Create a new role for the server.",
    scope=guild_ids,
    options=[
        interactions.Option(
            name="role_name",
            description="string name of role to add.",
            required=True,
            type=interactions.OptionType.STRING # option_type 3 = string
        ),
        interactions.Option(
            name="category",
            description="category of the role in the bot JSON file.",
            required=True,
            type=interactions.OptionType.STRING # option_type 3 = string
        )
        # interactions.Option(
        #     name="channel",
        #     description="string name of the channel for the new role.",
        #     required=False,
        #     type=interactions.OptionType.STRING # option_type 3 = string
        # )
    ]
)
async def create_role(ctx: interactions.CommandContext, role_name:str, category:str):
    print(guild)
    print(guild._client)
    new_role = await guild.create_role(role_name)
    snowflake = new_role.id
    print(f'{snowflake.epoch * 1000:042b}')
    print(f'{snowflake.worker_id:05b}')
    print(f'{snowflake.process_id:05b}')
    print(f'{snowflake.increment:012b}')
    snowflake_code = f'{snowflake.epoch * 1000:042b}' + f'{snowflake.worker_id:05b}' + f'{snowflake.process_id:05b}' + f'{snowflake.increment:012b}'
    print(snowflake_code)
    snowflake_code = str(int(snowflake_code, 2))
    print(snowflake_code)
    add_role_to_category(role_name, category, snowflake_code)
    await ctx.send(f'/createrole {role_name}, {category}')

@commands.has_permissions(administrator=True)
@client.command(
    name="deleterole", 
    description="Delete an existing role from the server.", 
    scope=guild_ids,
    options= [
        interactions.Option(
            name="role_name",
            description="Name of the role.",
            type=interactions.OptionType.STRING,
            required=True
        ),
        interactions.Option(
            name="category_name",
            description="Name of the category.",
            type=interactions.OptionType.STRING,
            required=True
        )
    ])
async def delete_role(ctx: interactions.CommandContext, role_name: str, category_name: str):
    role_id = get_role_id_for_role_and_category(role_name, category_name)
    await guild.remove_role(role_id)
    await ctx.send(content="Deleted role " + role_id)

@client.command(
    name="get_roles",
    description="Gets a list of roles for a given category.",
    scope=guild_ids,
    options = [
        interactions.Option(
            name="category_name",
            description="Name of the category.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def get_category_roles(ctx: interactions.CommandContext, category_name: str):
    await ctx.send('Roles: 'f'{get_roles_in_category(category_name)}')     

# -----------------------------------------------------------------------------------------------------
# @commands.has_permissions(administrator=True)
# @client.command(
#     name="editrole", 
#     description="Change the name of an existing role.", 
#     scope=guild_ids,
#     options=[
#         interactions.Option(
#             name="role_to_be_edited",
#             description="Choose the Role you want to edit",
#             required=True,
#             type=interactions.OptionType.STRING, 
#         )    
#     ]
# )
# async def edit_role(ctx: interactions.CommandContext):
#     await ctx.send(content="/editrole str:oldRoleName str:newRoleName")


@client.command(
    name="assignrole", 
    description="Assign yourself a role.", 
    scope=guild_ids,
    options=[
        interactions.Option(
            name="role_to_be_assigned",
            description="Choose a role to assign yourself!",
            required=True,
            type=interactions.OptionType.STRING, 
        )
    ]
)
async def assign_role(ctx: interactions.CommandContext, role_to_be_assigned: str):
    print(ctx.data)
    print(ctx.target)
    await ctx.send(content="/assignrole str:role")


@client.command(
    name="unassignrole", 
    description="Unassign yourself a role.", 
    scope=guild_ids,
    options=[
        interactions.Option(
            name="role_name",
            description="Choose one of your roles that you want to unnassign",
            required=True,
            type=interactions.OptionType.STRING, 
        )
    ]
)
async def unassign_role(ctx: interactions.CommandContext, role_name: str):
    await ctx.send(content="/unassignrole str:role")


@client.command(
    name="linkserver", 
    description="link a server to a class role", 
    scope=guild_ids,
    options=[
        interactions.Option(
            name="role_name",
            description="Choose a role for the class server",
            required=True,
            type=interactions.OptionType.STRING, 
        ),
        interactions.Option(
            name="category_name",
            description="Choose a category to which the role belongs",
            required=True,
            type=interactions.OptionType.STRING, 
        ),
        interactions.Option(
            name="server_url",
            description="Choose a server to link to your class role",
            required=True,
            type=interactions.OptionType.STRING, 
        )
    ]
)
async def link_server(ctx: interactions.CommandContext, role_name: str, category_name: str, server_url: str):
    add_link_to_role(server_url, role_name, category_name)
    await ctx.send(content="Successfully set the server url for role " + role_name + " to " + server_url)


@client.command(
    name="unlinkserver", 
    description="unlink all servers from a single class role", 
    scope=guild_ids,
    options=[
        interactions.Option(
            name="role_name",
            description="Choose a role for which you want to unlink all servers",
            required=True,
            type=interactions.OptionType.STRING, 
        ),
        interactions.Option(
            name="category_name",
            description="Choose a category for the role",
            required=True,
            type=interactions.OptionType.STRING, 
        )
    ]
)
async def unlink_server(ctx: interactions.CommandContext, role_name: str, category_name: str):
    remove_all_links_from_role(role_name, category_name)
    await ctx.send(content="Successfully unlinked servers from " + role_name)


@commands.has_permissions(administrator=True)
@client.command(
    name="nukeservers", 
    description="unlink all servers from all class role", 
    scope=guild_ids,
    options=[
        interactions.Option(
            name="nuclear_launch_code",
            description="Enter Nuclear Launch code to nuke server",
            required=True,
            type=interactions.OptionType.STRING, 
        )
    ]
)
async def nuke_server(ctx: interactions.CommandContext, nuclear_launch_code: str):
    if nuclear_launch_code == "wololo":
        nuke_servers()
        await ctx.send(content="Servers nuked.")
    else:
        await ctx.send(content="Launch aborted")
    

client.start()