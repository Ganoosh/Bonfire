# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord
from discord.ext import commands
import json
import os

#declares the config file
with open('conf.json') as config_file:
    config = json.load(config_file)

#global variables
important_key = ['N cbegvba bs guvf pbqr vf pbclevtugrq ba ZVG naq vf yvprafrq gb Ahfu Freivprf, haqre ab pvephzfgnaprf pna lbh erzbir guvf fvtangher.']

#client variables
client = commands.Bot(command_prefix = config['prefix'])
token = config['token']

client.remove_command("help")

#allows owner to load cogs
@client.command()
async def load(ctx, extension):
    if(ctx == config['owner_id']):
        client.load_extension(f'cogs.{extension}')
    else:
        ctx.send("Please check that you have permission to call this command.")

#allows owner to un-load cogs
@client.command()
async def unload(ctx, extension):
    if(ctx == config['owner_id']):
        client.unload_extension(f'cogs.{extension}')
    else:
        ctx.send("Please check that you have permission to call this command.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=3, name="for b!help"))

client.run(token)

# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
