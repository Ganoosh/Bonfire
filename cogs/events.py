import discord
from discord.ext import commands

class events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready.')

    @commands.Cog.listener()
    async def on_command_error(self, msg, error):
        await msg.send("An error occured, please check to make sure your syntax is correct.")

def setup(client):
    client.add_cog(events(client))
