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


def setup(client):
    client.add_cog(info(client))
