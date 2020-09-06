# Copyright MIT 2020 Nuch Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord
from discord.ext import commands, timers
import time
import datetime
import json


class info(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("Loading...")
        ping = (time.monotonic() - before) * 1000
        embed = discord.Embed(title="Pong :ping_pong:", color=0x1D1D1D)
        embed.add_field(name="Bot:", value=f"{round(ctx.bot.latency *1000, 2)}ms", inline=False)
        embed.add_field(name="Gateway:", value=f"{int(ping)}ms", inline=False)
        await message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="MAB Commands")
        embed.add_field(name="Polls:", value="_m!create_ : Interactive poll setup\n_m!create_ {channel} {time (f = forever)} {type s(sec)/m(min)/f(inf)} {poll title} | {option1, option2, etc}\nCommas in your title arent allowed.")
        embed.add_field(name="Info:", value="_m!ping_ : Gets bot ping", inline=False)
        embed.add_field(name="Util:", value="_m!remindme {time} {m(minutes) or s(seconds)} {reminder text}_ : reminds you.", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(info(client))


# Copyright MIT 2020 Nuch Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
