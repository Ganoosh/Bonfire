import discord, pause, pytz, json, time, asyncio
from discord import *
from discord.ext import *
import datetime as dt
from datetime import datetime as datetime_dt
from itertools import cycle
from discord.ext import tasks
from json import loads

with open('./config.json') as config_file:
    config = json.load(config_file)

#global vars
dt_now = datetime_dt.today()

class poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.timer_manager = timers.TimerManager(client)
        self.check_loop.start()

    # this checks the json file for entries that match the current time, if they do it sends a dm and then removes the entry.
    @tasks.loop(seconds=1)
    async def check_loop(self):
        with open('./cogs/cog_assets/polls.json') as json_file:
            data = json.load(json_file)
        dt_now = datetime_dt.today()
        timeString = dt_now.strftime("%-d.%-m %-y-%-I.%M.%-S")
        time = timeString
        def search():
          for n, dic in enumerate(data["main"]):
            if dic["time"] == time:
              return n
          return None
        index = search()
        if(index != None):

            channel_fetch = self.client.get_channel(data['main'][index]['channel_id'])
            message_fetch = await channel_fetch.fetch_message(data['main'][index]['message_id'])


            emoji_string = '';
            for item in message_fetch.reactions:
                emoji_string = emoji_string + str(item) + str(item.count) + '\n'


            await channel_fetch.send(f"Emojis:\n{emoji_string}")
            del data['main'][index]
            with open('./cogs/cog_assets/remindme.json', 'w') as f:
                json.dump(data, f)


    @commands.command()
    async def create(self, ctx):
        await ctx.message.delete()

        tz = pytz.timezone("US/Pacific")
        dt_now = datetime_dt.today()

        del_msg = await ctx.send("Alright, lets setup a new poll! So, what channel do you want the poll to be posted in?\n``Please write the channel name via hyperlink below. Example: #polls``")
        channelMsg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        channelId = str(channelMsg.content)[2:][:-1]
        await del_msg.delete()
        await channelMsg.delete()

        del_msg = await ctx.send(f"Indubitably epic, The message will be sent in <#{channelId}>, Now that we have that out of the way, how long do you want the poll to last? **Type forever or f to disable a countdown.**\n``The amount will be counted in seconds, if you want to use minutes please include your amount with a m at the end, Example: 30 m``")
        timeMsg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await timeMsg.delete()
        timeMsg = str(timeMsg.content).upper().split()
        await del_msg.delete()
        try:
            minute_value = timeMsg[1]
            del_msg = await ctx.send(f"Sounds like a plan! Your poll will last for a whole {timeMsg[0]} minutes! Last but not least, what do you want the poll to be about?\n``Example: What is your favorite minecraft server?``")
        except:
            del_msg = await ctx.send(f"Sounds like a plan! Your poll will last for a whole {timeMsg[0]} seconds! Along with that, what do you want the poll to be about(poll question)?\n``Example: What is your favorite minecraft server?``")


        pollMsgContent = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await del_msg.delete()
        await pollMsgContent.delete()

        del_msg = await ctx.send(f"Awesome! Along with that, what options do you want?\n``Please split each option with a comma and a space. Max is 9, Example: Hypixel, The Hive, Lifeboat``")
        pollMsgOptions = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await del_msg.delete()
        await pollMsgOptions.delete()

        pollMsgOptions = str(pollMsgOptions.content).split(", ")
        pollOptionsAmount = len(pollMsgOptions)

        reactionDict = {
            1: "1\N{variation selector-16}\N{combining enclosing keycap}",
            2: "2\N{variation selector-16}\N{combining enclosing keycap}",
            3: "3\N{variation selector-16}\N{combining enclosing keycap}",
            4: "4\N{variation selector-16}\N{combining enclosing keycap}",
            5: "5\N{variation selector-16}\N{combining enclosing keycap}",
            6: "6\N{variation selector-16}\N{combining enclosing keycap}",
            7: "7\N{variation selector-16}\N{combining enclosing keycap}",
            8: "8\N{variation selector-16}\N{combining enclosing keycap}",
            9: "9\N{variation selector-16}\N{combining enclosing keycap}"
        }


        if not(timeMsg[0] == "F" or timeMsg[0] == "FOREVER"):
            try:
                if(timeMsg[1] == "M" or timeMsg[1] == "MINUTES" or timeMsg[1] == "MINUTE"):
                    future_add_time = dt.timedelta(minutes = int(timeMsg[0]))
                elif(timeMsg[1] == "S" or timeMsg[1] == "SECONDS" or timeMsg[1] == "SECOND"):
                    future_add_time = dt.timedelta(seconds = int(timeMsg[0]))
            except:
                future_add_time = dt.timedelta(seconds = int(timeMsg[0]))


            dt_future = tz.localize(dt_now) + future_add_time

            logTimestamp = datetime_dt.timestamp(dt_future)

            descriptionMsg = '';
            for i, val in enumerate(pollMsgOptions):
                descriptionMsg = descriptionMsg + f"{reactionDict[i + 1]} : {pollMsgOptions[i]}\n"

            customEmbed = discord.Embed(title="Poll: " + pollMsgContent.content, description=descriptionMsg)

            timeStringFooter = dt_future.strftime("%-d %b %Y at %-I:%M %p - %Z")
            logTimeString = dt_future.strftime("%-d.%-m %-y-%-I.%M.%-S")

            customEmbed.set_footer(text=f'Ends on {timeStringFooter}')

            channel = self.client.get_channel(int(channelId))
            messageToReact = await channel.send(embed=customEmbed)

            xKey = 1
            for key in reactionDict:
                if not(xKey > pollOptionsAmount):
                    await messageToReact.add_reaction(reactionDict[key])
                    xKey += 1
                else:
                    break

            #opens main remindme.json
            with open('./cogs/cog_assets/polls.json') as json_file:
                data = json.load(json_file)
            data['main'].append({ 'time': logTimeString, 'message_id': messageToReact.id, 'channel_id':  int(channelId)})
            with open('./cogs/cog_assets/polls.json', 'w') as f:
                json.dump(data, f)



        else:
            descriptionMsg = '';
            for i, val in enumerate(pollMsgOptions):
                descriptionMsg = descriptionMsg + f"{reactionDict[i + 1]} : {pollMsgOptions[i]}\n"

            customEmbed = discord.Embed(title="Poll: " + pollMsgContent.content, description=descriptionMsg)

            channel = self.client.get_channel(int(channelId))
            messageToReact = await channel.send(embed=customEmbed)

            xKey = 1
            for key in reactionDict:
                if not(xKey > pollOptionsAmount):
                    await messageToReact.add_reaction(reactionDict[key])
                    xKey += 1
                else:
                    break




    @commands.command()
    async def pollCreate(self, ctx, time, amount, *, text):
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
    client.add_cog(poll(client))
