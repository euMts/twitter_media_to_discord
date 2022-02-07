from utils import main, telegram_bot_sendtext
from importlib import reload
from asyncio import sleep
from json import dumps
import Constants
import discord

client = discord.Client(intents=discord.Intents.all(), activity=discord.Game(name=f"Minecraft"))

@client.event
async def on_ready():
    print(f"Logado como {client.user}")
    while True:
        await main()
        await sleep(900) #15 min

@client.event
async def on_message(message):
    user_message = str(message.content)
    channel = str(message.channel.name)
    if message.author != client.user:
        print(f"Mensagem de '{message.author}' no canal '{channel}' ")
    if message.author == client.user:
        return
    if user_message.lower() == "!comandos":
        await message.channel.send("Lista de comandos disponíveis:\n!comandos\n!codigo\n!teste\n!url\n!explodir_servidor\n!status")
        return
    elif user_message.lower() == "!codigo":
        await message.channel.send("Código fonte do bot disponível em:\nhttps://github.com/euMts")
        return
    elif user_message.lower() == "!teste":
        await message.channel.send("retorno")
        return
    elif user_message.lower() == "!url":
        await message.channel.send("Página alvo:\nhttps://twitter.com/Mtss_e")
        return
    elif user_message.lower() == "!explodir_servidor":
        await message.channel.send(f"Seu nome foi reportado para um dos administradores.")
        telegram_bot_sendtext(f"Troll: {message.author}")
        return
    elif user_message.lower() == "!status":
        reload(Constants)
        status = {"status":200, "midias_enviadas":Constants.number}
        await message.channel.send(f"```{dumps(status, indent=4)}```")
        return

async def enviar_mensagem(msg):
    channel = client.get_channel(1234567890) # id do canal de texto
    await channel.send(msg)

if __name__ == "__main__":
    try:
        client.run(Constants.TOKEN)
    except Exception as e:
        telegram_bot_sendtext(f"Erro em bot_disco\n{e}")