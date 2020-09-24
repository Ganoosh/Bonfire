# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord
from discord.ext import commands, tasks
import json
import os
import requests

with open('./conf.json') as config_file:
    config = json.load(config_file)

#global variables
important_key = ['N cbegvba bs guvf pbqr vf pbclevtugrq ba ZVG naq vf yvprafrq gb Ahfu Freivprf, haqre ab pvephzfgnaprf pna lbh erzbir guvf fvtangher.']

class events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.write_stats.start()

    @tasks.loop(seconds=60)
    async def write_stats(self):
        await self.client.wait_until_ready()
        server_list = []
        channels_list = []
        totalMembers = 0
        for server in self.client.guilds:
            server_list.append(server.name)
            for channel in server.channels:
                channels_list.append(channel.id)
            totalMembers += len(server.members)
        channel_amount = str(len(channels_list))
        server_amount = str(len(server_list))
        reqUrl = f"https://bonfiredashboard.ganoosh.repl.co/add/info/stats?auth={config['stats_auth_token']}&guilds={server_amount}&channels={channel_amount}&users={totalMembers}"
        requests.get(reqUrl) 
        

    @commands.Cog.listener()
    async def on_ready(self):

        print('Ready.')

        listOfFiles = []

        files = os.listdir('./cogs')

        for i in files:
            if i.endswith(".py"):
                listOfFiles.append(f'./cogs/{i}')

        fileAmount = len(listOfFiles)

        listOfCommands = {}

        for key in range(len(listOfFiles)):
            with open(listOfFiles[key]) as fp:
                line = fp.readline()
                cnt = 1
                while line:
                    if(line.strip().startswith('command_definer')):
                        lineToStrip = line.strip().partition("[")[2].partition("]")[0]
                        lineToStrip = json.loads(lineToStrip)

                        listOfCommands[lineToStrip["name"]] = lineToStrip["description"]

                    line = fp.readline()
                    cnt += 1

        command_info = len(listOfCommands)
        command_json = listOfCommands

        open('./cogs/cog_assets/amount.json', 'w').write('{"item_info": []}')
        #opens main remindme.json
        with open('./cogs/cog_assets/amount.json') as json_file:
                data = json.load(json_file)
                data['item_info'].append({'amount':command_info, 'cog_count': fileAmount, 'descriptions': command_json})
        with open('./cogs/cog_assets/amount.json', 'w') as f:
                json.dump(data, f)

    @commands.Cog.listener()
    async def on_command_error(self, msg, error):
        await msg.send("An error occured, please check to make sure your syntax is correct.")

def setup(client):
    client.add_cog(events(client))

# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
