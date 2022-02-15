from twitter_image_dl import twitter_image_dl
from twitter_video_dl import download_video
from importlib import reload
import Constants
import requests
import json
import os

def enviar_mensagem_discord(msg, file, token, channel_id):
    header = {'authorization': f"Bot {token}"} # se não for bot troca "Bot " por "Bearer "
    files = {"file" : (file, open(file, 'rb'))}
    payload = {"content":msg}
    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header, files=files)
    return r

def telegram_bot_sendtext(bot_message):
    send_text = f"https://api.telegram.org/bot{Constants.API_KEY}/sendMessage?chat_id={Constants.BOT_CHAT_ID}&parse_mode=Markdown&text={bot_message}"
    response = requests.get(send_text)
    return response.json()

def atualizar_numero():
    reload(Constants)
    num_antigo = Constants.number
    arquivo = open("Constants.py", "r")
    conteudo_antigo = arquivo.read()
    arquivo.close
    arquivo = open("Constants.py", "w")
    arquivo.write(conteudo_antigo.replace(f"number = {num_antigo}", f"number = {num_antigo + 1}"))
    arquivo.close()
    reload(Constants)
    return {"valor_antigo":num_antigo, "valor_novo":Constants.number}

def atualizar_log(txt):
    reload(Constants)
    valor_antigo = Constants.tweets
    arquivo = open("Constants.py", "r")
    conteudo_antigo = arquivo.read()
    arquivo.close
    valor_novo = []
    for item in Constants.tweets:
        valor_novo.append(item)
    valor_novo.append(txt)
    arquivo = open("Constants.py", "w")
    arquivo.write(conteudo_antigo.replace(f"tweets = {valor_antigo}", f"tweets = {valor_novo}"))
    arquivo.close()
    reload(Constants)
    valor_novo = Constants.tweets
    return {"valor_antigo":valor_antigo, "valor_novo":valor_novo}

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {Constants.BEARER_TOKEN}"
    r.headers["User-Agent"] = "get_tweets"
    return r

def get_recent_tweets(page_name):
    try:
        url = f"https://api.twitter.com/2/tweets/search/recent?query=from%3A{page_name}%20-is%3Areply%20has%3Amedia&max_results=10"
        response = requests.get(url, auth=bearer_oauth)
        status = response.status_code
        ids = []
        if status == 200:
            for x in range(len(json.loads(response.text)["data"])):
                ids.append(str(json.loads(response.text)["data"][x]["id"]))
            return {
                "status":status,
                "ids":ids
                }
        else:
            telegram_bot_sendtext("Erro em get_recent_tweets")
            return {
                "status":status,
                "ids":ids
                }
    except Exception as e:
        telegram_bot_sendtext(f"Erro em get_recent_tweets\n{e}")
        return {
            "status":status,
            "ids":ids
            }

def get_media_type(tweet_id):
    try:
        url = f"https://api.twitter.com/2/tweets?ids={tweet_id}&expansions=attachments.media_keys&media.fields=url"
        response = requests.get(url, auth=bearer_oauth)
        status = response.status_code
        if status == 200:
            media_type = str(json.loads(response.text)["includes"]["media"][0]["type"])
            return {
                "status":status,
                "media_type":media_type
                }
        else:
            telegram_bot_sendtext("Erro em get_media_type")
            return {
                "status":status,
                "media_type":""
                }
    except Exception as e:
        telegram_bot_sendtext(f"Erro em get_media_type\n{e}")
        return {
            "status":status,
            "media_type":""
            }

async def main():
    reload(Constants)
    last_tweets = get_recent_tweets("Mtss_e")["ids"]
    saved_tweets = Constants.tweets
    added_tweets = 0
    for x in range(len(last_tweets)):
        if last_tweets[x] not in saved_tweets:
            added_tweets += 1
            print("Adicionando novo tweet.")
            atualizar_log(last_tweets[x])
            if get_media_type(last_tweets[x])["media_type"] == "video":
                video_url = f"https://twitter.com/i/status/{last_tweets[x]}"
                print("Baixando video...")
                download_video(video_url, f"./media/{Constants.number}.mp4")
                print("Video baixado!")
                print("Enviando para o discord...")
                enviar_mensagem_discord("", f"./media/{Constants.number}.mp4", Constants.TOKEN, "1234567890")
                print("Video enviado!")
                print("Deletando arquivo...")
                try:
                    try:
                        os.remove(f"./media/{Constants.number}.mp4")
                    except:
                        os.remove(f"./media/{Constants.number}")
                except:
                    print("Erro ao excluir arquivo")
                print("Arquivo deletado.")
                atualizar_numero()
            elif get_media_type(last_tweets[x])["media_type"] == "photo":
                print("Baixando foto...")
                extension = twitter_image_dl(last_tweets[x], f"./media/{Constants.number}")["extension"]
                print("Foto baixada!")
                print("Enviando para o discord...")
                enviar_mensagem_discord("", f"./media/{Constants.number}{extension}", Constants.TOKEN, "1234567890")
                print("Foto enviada!")
                print("Deletando arquivo...")
                try:
                    try:
                        os.remove(f"./media/{Constants.number}{extension}")
                    except:
                        os.remove(f"./media/{Constants.number}")
                except:
                    print("Erro ao excluir arquivo")
                print("Arquivo deletado.")
                atualizar_numero()
            else:
                print("Erro em main")
                telegram_bot_sendtext(f"Erro em main\n{last_tweets[x]}\npulando...")
                pass
        else:
            print("Tweet antigo.")
    return {"added_tweets":added_tweets}

if __name__ == "__main__":
    print(main())