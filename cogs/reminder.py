# Copyright MIT 2020 Nuch Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord, pytz, json, time, asyncio
import datetime as dt
from discord import *
from discord.ext import *
from discord.ext import commands, timers
from datetime import datetime as datetime_dt
from itertools import cycle
from discord.ext import tasks
from json import loads

with open('./conf.json') as config_file:
    config = json.load(config_file)

#global vars
dt_now = datetime_dt.today()

class reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.timer_manager = timers.TimerManager(client)
        self.my_loop.start()

    # this checks the json file for entries that match the current time, if they do it sends a dm and then removes the entry.
    @tasks.loop(seconds=1)
    async def my_loop(self):
        with open('./cogs/cog_assets/remindme.json') as json_file:
            data = json.load(json_file)
        dt_now = datetime_dt.today()
        timeString = f"{dt_now.year}.{dt_now.month}.{dt_now.day} - {dt_now.hour}.{dt_now.minute}.{dt_now.second}"
        time = timeString
        def search():
          for n, dic in enumerate(data["main"]):
            if dic["time"] == time:
              return n
          return None
        index = search()
        if(index != None):
            channel = self.client.get_channel(data['main'][index]['channel_id'])
            await channel.send(f"<@{data['main'][index]['user_id']}> Reminder:\n```{data['main'][index]['content']}```")
            del data['main'][index]
            with open('./cogs/cog_assets/remindme.json', 'w') as f:
                json.dump(data, f)

    @commands.command()
    async def remindme(self, ctx, time, amount, *, text):
        tz = pytz.timezone("US/Pacific")
        dt_now = datetime_dt.today()

        if(amount == "s" or amount == "second" or amount == "seconds"):
            future_add_time = dt.timedelta(seconds = int(time))
        elif(amount == "m" or amount == "minute" or amount == "minutes"):
            future_add_time = dt.timedelta(minutes = int(time))
        elif(amount == "h" or amount == "hour" or amount == "hours"):
            future_add_time = dt.timedelta(hours = int(time))
        elif(amount == "d" or amount == "day" or amount == "days"):
            future_add_time = dt.timedelta(days = int(time))
        elif(amount == "month" or amount == "months"):
            future_add_time = dt.timedelta(months = int(time))
        elif(amount == "y" or amount == "year" or amount == "years"):
            future_add_time = dt.timedelta(years = int(time))
        dt_future = tz.localize(dt_now) + future_add_time
        #opens main remindme.json
        with open('./cogs/cog_assets/remindme.json') as json_file:
            data = json.load(json_file)
        data['main'].append({'time': f"{dt_future.year}.{dt_future.month}.{dt_future.day} - {dt_future.hour}.{dt_future.minute}.{dt_future.second}", "user_id": ctx.author.id, "content": text, "channel_id" : ctx.channel.id})
        with open('./cogs/cog_assets/remindme.json', 'w') as f:
            json.dump(data, f)


def setup(client):
    client.add_cog(reminder(client))

# Copyright MIT 2020 Nuch Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
