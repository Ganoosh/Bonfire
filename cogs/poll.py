# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord, pytz, json, time, asyncio
from discord import *
from discord.ext import *
from discord.ext import commands
from discord.ext import timers as timers
import datetime as dt
from datetime import datetime as datetime_dt
from itertools import cycle
from discord.ext import tasks
from json import loads

with open('./conf.json') as config_file:
    config = json.load(config_file)

#global vars
dt_now = datetime_dt.today()
important_key = ['N cbegvba bs guvf pbqr vf pbclevtugrq ba ZVG naq vf yvprafrq gb Ahfu Freivprf, haqre ab pvephzfgnaprf pna lbh erzbir guvf fvtangher.']

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
        timeString = dt_now.strftime("%-d.%-m %-y:%-I.%M.%-S")
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

            emoji_count_list = [];
            emoji_string = '';
            number_thing = 0;
            for item in message_fetch.reactions:
                if(item.count == 1):
                    votess = "vote"
                else:
                    votess = "votes"
                emoji_string = emoji_string + "``" + str(data['main'][index]['content'][number_thing]) +"``" + " Got " "``" + str(item.count) + "``" + f" {votess}\n"
                emoji_count_list.append(int(item.count))
                number_thing += 1;

            decription_msg = data['main'][index]['timestamp']
            decription_msg = datetime_dt.fromtimestamp(int(decription_msg))
            decription_msg = decription_msg.strftime('Ended At: %-d %b %Y at %-I:%M %p - PDT')

            count_list_index = emoji_count_list.index(max(emoji_count_list))
            embed = discord.Embed(title=f"🎉 Results for: {data['main'][index]['title']}! 🎉", description=f"**{data['main'][index]['content'][count_list_index]}** is the winner with **{emoji_count_list[count_list_index]}** votes!\n\n{emoji_string}")
            embed.set_footer(text=decription_msg)

            await message_fetch.delete()

            await channel_fetch.send(embed=embed)
            del data['main'][index]
            with open('./cogs/cog_assets/remindme.json', 'w') as f:
                json.dump(data, f)


    @commands.command()
    async def create(self, ctx):

        command_definer = [{"name": "create", "description": "interactive poll setup"}]

        await ctx.message.delete()

        tz = pytz.timezone("US/Pacific")
        dt_now = datetime_dt.today()

        del_msg = await ctx.send("Alright, lets setup a new poll! So, what channel do you want the poll to be posted in?\n``Please write the channel name via hyperlink below. Example: #polls``")
        channelMsg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        channelId = str(channelMsg.content)[2:][:-1]
        await del_msg.delete()
        await channelMsg.delete()

        if(channelId.isdigit() == False):
            await ctx.send("Please make sure you selected a channel, example: #polls, after typing this discord should automatically correct it to a blue highlighted text, then send it to the bot.")
            return

        del_msg = await ctx.send(f"Indubitably epic, The message will be sent in <#{channelId}>, Now that we have that out of the way, how long do you want the poll to last? **Type forever or f to disable a countdown.**\n``The amount will be counted in seconds, if you want to use minutes please include your amount with a m at the end, Example: 30 m``")
        timeMsg = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await timeMsg.delete()
        timeMsg = str(timeMsg.content).upper().split()
        await del_msg.delete()


        if not(timeMsg[0] == "F" or timeMsg[0] == "FOREVER"):
            try:
                if not(timeMsg[1] == "S" or timeMsg[1] == "SECOND" or timeMsg[1] == "SECONDS" or timeMsg[1] == "M" or timeMsg[1] == "MINUTES" or timeMsg[1] == "MINUTE"):
                    await ctx.send("Please make sure you selected a channel, example: #polls, after typing this discord should automatically correct it to a blue highlighted text, then send it to the bot.")
                    return
            except:
                await ctx.send("You entered a invalid time and value, here is a dictionary for reference:\n```Forever   : F or Forever\nSeconds   : {Your Amount} S or Second(s)\nMinutes   : {Your amount} M or Minute(s)\n\nExamples:\nForever    : f\nSeconds    : 30 s\nMinutes    : 120 m```")
                return

        try:
            minute_value = timeMsg[1]
            del_msg = await ctx.send(f"Sounds like a plan! Your poll will last for a whole {timeMsg[0]} minutes! Last but not least, what do you want the poll to be about?\n``Example: What is your favorite minecraft server?``")
        except:
            del_msg = await ctx.send(f"Sounds like a plan! Your poll will last for a whole {timeMsg[0]} seconds! Along with that, what do you want the poll to be about(poll question)?\n``Example: What is your favorite minecraft server?``")


        pollMsgContent = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await del_msg.delete()
        await pollMsgContent.delete()

        del_msg = await ctx.send(f"Awesome! Along with that, what options do you want?\n``Please split each option with a comma. Max is 9, Example: Hypixel, The Hive, Lifeboat``")
        pollMsgOptions = await self.client.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        await del_msg.delete()
        await pollMsgOptions.delete()

        await ctx.send(f"Poll has been successfully posting in: <#{channelId}>!")

        pollMsgOptions = str(pollMsgOptions.content).split(",")
        pollOptionsAmount = len(pollMsgOptions)

        for key in range(len(pollMsgOptions)):
            pollMsgOptions[key] = pollMsgOptions[key].strip()

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

            descriptionMsg = '';
            for i, val in enumerate(pollMsgOptions):
                descriptionMsg = descriptionMsg + f"{reactionDict[i + 1]} : {pollMsgOptions[i]}\n"

            customEmbed = discord.Embed(title="Poll: " + pollMsgContent.content, description=descriptionMsg)

            timeStringFooter = dt_future.strftime("%-d %b %Y at %-I:%M %p - %Z")
            logTimeString = dt_future.strftime("%-d.%-m %-y:%-I.%M.%-S")

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
            logTimestamp = datetime_dt.timestamp(dt_future)
            logTimestamp = str(logTimestamp).split('.')
            logTimestamp = str(logTimestamp[0])
            #opens main remindme.json
            with open('./cogs/cog_assets/polls.json') as json_file:
                data = json.load(json_file)
            data['main'].append({ 'title' : pollMsgContent.content , 'content': pollMsgOptions, 'timestamp' : logTimestamp, 'time': logTimeString, 'message_id': messageToReact.id, 'channel_id':  int(channelId)})
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
    async def start(self, ctx, channel, time, amount, *, text):

        command_definer = [{"name": "start", "description": "quick poll setup"}]

        split_text = text.split('| ')
        options_text = str(split_text[1]).split(', ')
        title_text = str(split_text[0])
        channelId = str(channel)[2:][:-1]
        pollOptionsAmount = len(options_text)
        amount = amount.upper()

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

        tz = pytz.timezone("US/Pacific")
        dt_now = datetime_dt.today()
        future_add_time = '';

        if not(amount == "F" or amount == "FOREVER"):
            try:
                if(amount == "M" or amount == "MINUTES" or amount == "MINUTE"):
                    future_add_time = dt.timedelta(minutes = int(time))
                elif(amount == "S" or amount == "SECONDS" or amount == "SECOND"):
                    future_add_time = dt.timedelta(seconds = int(time))
            except:
                future_add_time = dt.timedelta(seconds = int(time))

            dt_future = tz.localize(dt_now) + future_add_time

            descriptionMsg = '';
            for i, val in enumerate(options_text):
                descriptionMsg = descriptionMsg + f"{reactionDict[i + 1]} : {options_text[i]}\n"

            customEmbed = discord.Embed(title="Poll: " + title_text, description=descriptionMsg)

            timeStringFooter = dt_future.strftime("%-d %b %Y at %-I:%M %p - %Z")
            logTimeString = dt_future.strftime("%-d.%-m %-y:%-I.%M.%-S")

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

            logTimestamp = datetime_dt.timestamp(dt_future)
            logTimestamp = str(logTimestamp).split('.')
            logTimestamp = str(logTimestamp[0])

            #opens main remindme.json
            with open('./cogs/cog_assets/polls.json') as json_file:
                data = json.load(json_file)
            data['main'].append({ 'title' : title_text , 'content': options_text, 'timestamp' : logTimestamp, 'time': logTimeString, 'message_id': messageToReact.id, 'channel_id':  int(channelId)})
            with open('./cogs/cog_assets/polls.json', 'w') as f:
                json.dump(data, f)

        else:
            descriptionMsg = '';
            for i, val in enumerate(options_text):
                descriptionMsg = descriptionMsg + f"{reactionDict[i + 1]} : {options_text[i]}\n"

            customEmbed = discord.Embed(title="Poll: " + title_text, description=descriptionMsg)

            channel = self.client.get_channel(int(channelId))
            messageToReact = await channel.send(embed=customEmbed)

            xKey = 1
            for key in reactionDict:
                if not(xKey > pollOptionsAmount):
                    await messageToReact.add_reaction(reactionDict[key])
                    xKey += 1
                else:
                    break

def setup(client):
    client.add_cog(poll(client))

# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
