# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord
from discord.ext import commands
import json

#global variables
important_key = ['N cbegvba bs guvf pbqr vf pbclevtugrq ba ZVG naq vf yvprafrq gb Ahfu Freivprf, haqre ab pvephzfgnaprf pna lbh erzbir guvf fvtangher.']

class events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready.')

        listOfCommands = {}

        filepath = './cogs/poll.py'
        with open(filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                if(line.strip().startswith('command_definer')):
                    lineToStrip = line.strip().partition("[")[2].partition("]")[0]
                    lineToStrip = json.loads(lineToStrip)

                    listOfCommands[lineToStrip["name"]] = lineToStrip["description"]

                line = fp.readline()
                cnt += 1

        print(f"Commands Amount: {len(listOfCommands) }\nCommands Json: {listOfCommands}")

    @commands.Cog.listener()
    async def on_command_error(self, msg, error):
        await msg.send("An error occured, please check to make sure your syntax is correct.")

def setup(client):
    client.add_cog(events(client))

# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
