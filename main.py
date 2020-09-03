import discord
from discord.ext import commands
import json
import os

#declares the config file
with open('config.json') as config_file:
    config = json.load(config_file)

#client variables
client = commands.Bot(command_prefix = config['prefix'])
token = config['token']

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


client.run(token)
