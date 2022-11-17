import os
import json
import time
import math
import discord
import aiohttp
import asyncio
import jinja2

ELASTIC_USERNAME   = os.getenv('ELASTIC_USERNAME')
ELASTIC_PASSWORD   = os.getenv('ELASTIC_PASSWORD')
ELASTIC_ENDPOINT   = os.getenv('ELASTIC_ENDPOINT')
DISCORD_BOT_TOKEN  = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
DISCORD_MESSAGE_ID = int(os.getenv('DISCORD_MESSAGE_ID'))
QUERY              = os.getenv('QUERY')
TEMPLATE           = os.getenv('TEMPLATE')
EVAL_INTERVAL      = int(os.getenv('EVAL_INTERVAL'))

template = jinja2.Template(TEMPLATE)
client = discord.Client(intents=discord.Intents.default())

async def update():
    async with aiohttp.ClientSession() as session:
        result_r = await session.post(ELASTIC_ENDPOINT,
                                      auth=aiohttp.BasicAuth(ELASTIC_USERNAME, ELASTIC_PASSWORD),
                                      headers={'Content-Type': 'application/json'},
                                      data=QUERY)
        result_j = await result_r.json()
        newmsg = template.render(r=result_j)
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        message = await channel.fetch_message(DISCORD_MESSAGE_ID)
        await message.edit(content=newmsg)
        with open('/tmp/healthy', 'a') as fp:
            pass

@client.event
async def on_ready():
    while True:
        await update()
        await asyncio.sleep(EVAL_INTERVAL)

client.run(DISCORD_BOT_TOKEN)
