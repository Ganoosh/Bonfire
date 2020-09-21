# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord
from discord.ext import commands, timers
import time
import datetime
import json
import sys
import platform, os

#global variables
important_key = ['N cbegvba bs guvf pbqr vf pbclevtugrq ba ZVG naq vf yvprafrq gb Ahfu Freivprf, haqre ab pvephzfgnaprf pna lbh erzbir guvf fvtangher.']

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        command_definer = [{"name": "info", "description": "shows the bots information."}]
        embed = discord.Embed(title="Bonfire Information:")
        embed.set_thumbnail(url='https://bot.nush.me/assets/icon.png')
        embed.add_field(name="Author:", value="Ganoosh (Nush)\nGithub: https://github.com/ganoosh", inline=False)
        embed.add_field(name="Source Code:", value="Github: https://github.com/Ganoosh/Bonfire\nInfo: This is for documentation and reference only.", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        command_definer = [{"name": "help", "description": "shows bot commands"}]
        with open('./cogs/cog_assets/amount.json') as json_file:
            data = json.load(json_file)
            command_info = data['item_info'][0]['amount']
            command_count = data['item_info'][0]['cog_count']
            command_data = data['item_info'][0]['descriptions']
            command_data = command_data

        help_string = ""

        for key in command_data:
            help_string = help_string + "*" + key + "*" + " : " + command_data[key] +"\n"

        os.system('distro -j > ./assets/host_version.json')
        with open('./assets/host_version.json') as json_file:
            data = json.load(json_file)
            os_type = data['id']

        uname = platform.uname()

        embed = discord.Embed(title="Bonfire Commands", description="Not sure how to use a command? Check out our more in depth list:\nhttps://bot.nush.me/")
        embed.add_field(name="Commands: ", value=help_string)
        embed.add_field(name="Total Commands: ", value=f"Bonfire has **{command_info}** commands in **{int(command_count)-1}** cogs", inline=False)
        embed.add_field(name=f"Host:", value=f"{os_type} - {uname.release}{uname.machine}\npython{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - {sys.version_info.releaselevel}", inline=False)
        await ctx.send(embed=embed)



    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """ Pong! """
        command_definer = [{"name": "ping", "description": "pings the bot."}]
        before = time.monotonic()
        message = await ctx.send("Loading...")
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(title="Pong :ping_pong:", color=0x1D1D1D)
        embed.add_field(name="Bot:", value=f"{round(ctx.bot.latency *1000, 2)}ms", inline=False)
        embed.add_field(name="Gateway:", value=f"{int(ping)}ms", inline=False)
        await message.delete()
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(info(client))


# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
