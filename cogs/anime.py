# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.

import discord
from discord.ext import commands, timers
import time
import datetime
import json
import requests

#global variables
important_key = ['N cbegvba bs guvf pbqr vf pbclevtugrq ba ZVG naq vf yvprafrq gb Ahfu Freivprf, haqre ab pvephzfgnaprf pna lbh erzbir guvf fvtangher.']

class anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['w2g', 'animew2g', 'w2ga', 'a2g'])
    async def w2a(self, ctx, aType, episode, *, query):

        membed = discord.Embed(title="Loading...")
        msg = await ctx.send(embed=membed)

        url = f"https://AnimeScrap.ganoosh.repl.co/search?query={query}&type={aType}&episode={episode}"

        payload = {}
        headers= {}

        response = requests.request("GET", url, headers=headers, data = payload)
        response = response.text.encode('utf8')
        response = json.loads(response)

        purl = f"https://animescrap-1.ganoosh.repl.co/create?url={response['url']}"

        ppayload = {}
        pheaders= {}

        presponse = requests.request("GET", purl, headers=pheaders, data = ppayload)
        presponse = presponse.text.encode('utf8')
        presponse = json.loads(presponse)

        w2gR = f"https://w2g.tv/rooms/{presponse['streamkey']}"

        jurl = f"https://api.jikan.moe/v3/search/anime?q={query}&page=1"
        jpayload = {}
        jheaders = {}

        jresponse = requests.request("GET", jurl, headers=jpayload, data = jpayload)
        jresponse = jresponse.text.encode('utf8')
        jresponse = json.loads(jresponse)


        embed = discord.Embed(title="Success!", description=f"Now playing: {query}\nType: {aType}\nEpisode: {episode}")
        embed.add_field(name="Your w2g room: ", value=w2gR)
        embed.set_image(url=jresponse['results'][0]['image_url'])

        await msg.edit(embed=embed)



def setup(client):
    client.add_cog(anime(client))


# Copyright MIT 2020 Nush Services
# This code or template is created by Ganoosh, and therefore you may not under any circumstances claim it as your own nor remove this signature.
