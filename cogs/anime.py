# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord
from discord.ext import commands, timers
import time
import datetime
import json
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


#global variables
important_key = ['N cbegvba bs guvf pbqr vf pbclevtugrq ba ZVG naq vf yvprafrq gb Ahfu Freivprf, haqre ab pvephzfgnaprf pna lbh erzbir guvf fvtangher.']

with open('./conf.json') as config_file:
    config = json.load(config_file)

class anime(commands.Cog):
    def __init__(self, client):
        self.client = client

""" 
    @commands.command()
    async def w2anime(self, ctx, url):
        


    @commands.command(aliases=['w2g', 'animew2g', 'w2ga', 'a2g'])
    async def w2a(self, ctx, aType, episode, *, query):



        payload = {}
        headers= {}
        
        jurl = f"https://api.jikan.moe/v3/search/anime?q={query}&page=1"

        jresponse = requests.request("GET", jurl, headers=payload, data = payload)
        jresponse = jresponse.text.encode('utf8')
        jresponse = json.loads(jresponse)


        name_list = []
        number_results_list = []


        for i, val in enumerate(jresponse['results']):
            name_list.append(jresponse['results'][i]['title'])

        for i, val in enumerate(name_list):
            number_results_list.append(fuzz.ratio(jresponse['results'][i]['title'], query))

        
        max_number = max(number_results_list)
    
        best_r = jresponse['results'][number_results_list.index(max_number)]




        membed = discord.Embed(title="Loading...")
        msg = await ctx.send(embed=membed)

        private_api_url = config['aniscrap']

        url = f"{private_api_url}/search?query={best_r['title']}&type={aType}&episode={episode}"



        response = requests.request("GET", url, headers=headers, data = payload)
        response = response.text.encode('utf8')
        response = json.loads(response)

        purl = f"{private_api_url}/create?url={response['url']}"


        presponse = requests.request("GET", purl, headers=headers, data = payload)
        presponse = presponse.text.encode('utf8')
        presponse = json.loads(presponse)

        w2gR = f"https://w2g.tv/rooms/{presponse['streamkey']}"

        

        embed = discord.Embed(title="Success!", description=f"Now playing: {best_r['title']}\nType: {aType.capitalize()}\nEpisode: {episode}")
        embed.add_field(name="Your w2g room: ", value=w2gR)
        embed.set_image(url=best_r['image_url'])

        await msg.edit(embed=embed)
 """


def setup(client):
    client.add_cog(anime(client))


# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
