from utils import main, telegram_bot_sendtext
from importlib import reload
from asyncio import sleep
from json import dumps
import Constants
import discord

client = discord.Client(intents=discord.Intents.all(), activity=discord.Game(name=f"Minecraft"))

@client.event
async def on_ready():
    print(f"Logged as {client.user}")
    while True:
        await main()
        await sleep(900) #15 min

@client.event
async def on_message(message):
    user_message = str(message.content)
    channel = str(message.channel.name)
    if message.author != client.user:
        print(f"Message from '{message.author}' on '{channel}' ")

    if message.author == client.user:
        return
    if user_message.lower() == "!commands":
        await message.channel.send("Command list:\n!commands\n!code\n!test\n!url\n!explode_server\n!status")
        return
    elif user_message.lower() == "!code":
        await message.channel.send("Source code:\nhttps://github.com/euMts")
        return
    elif user_message.lower() == "!test":
        await message.channel.send("return")
        return
    elif user_message.lower() == "!url":
        await message.channel.send("Twitter page:\nhttps://twitter.com/Mtss_e")
        return
    elif user_message.lower() == "!explode_server":
        await message.channel.send(f"Your username has been sent to the administrators.")
        telegram_bot_sendtext(f"Troll: {message.author}")
        return
    elif user_message.lower() == "!status":
        reload(Constants)
        status = {"status":200, "sent_midia":Constants.number}
        await message.channel.send(f"```{dumps(status, indent=4)}```")
        return

async def send_message(msg):
    channel = client.get_channel( ) # text channel id
    await channel.send(msg)

if __name__ == "__main__":
    try:
        client.run(Constants.TOKEN)
    except Exception as e:
        telegram_bot_sendtext(f"Error on bot_disco\n{e}")