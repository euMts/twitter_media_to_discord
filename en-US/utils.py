from twitter_image_dl import twitter_image_dl
from twitter_video_dl import download_video
from importlib import reload
import Constants
import requests
import json
import os

def send_discord_message(msg, file, token, channel_id):
    header = {'authorization': f"Bot {token}"} # if is not a bot account, change "Bot " to "Bearer "
    files = {"file" : (file, open(file, 'rb'))}
    payload = {"content":msg}
    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", data=payload, headers=header, files=files)
    return r

def telegram_bot_sendtext(bot_message):
    send_text = f"https://api.telegram.org/bot{Constants.API_KEY}/sendMessage?chat_id={Constants.BOT_CHAT_ID}&parse_mode=Markdown&text={bot_message}"
    response = requests.get(send_text)
    return response.json()

def update_number():
    reload(Constants)
    old_num = Constants.number
    archive = open("Constants.py", "r")
    old_content = archive.read()
    archive.close
    archive = open("Constants.py", "w")
    archive.write(old_content.replace(f"number = {old_num}", f"number = {old_num + 1}"))
    archive.close()
    reload(Constants)
    return {"old_value":old_num, "new_value":Constants.number}

def update_log(txt):
    reload(Constants)
    old_value = Constants.tweets
    archive = open("Constants.py", "r")
    old_content = archive.read()
    archive.close
    new_value = []
    for item in Constants.tweets:
        new_value.append(item)
    new_value.append(txt)
    archive = open("Constants.py", "w")
    archive.write(old_content.replace(f"tweets = {old_value}", f"tweets = {new_value}"))
    archive.close()
    reload(Constants)
    new_value = Constants.tweets
    return {"old_value":old_value, "new_value":new_value}

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
            telegram_bot_sendtext("Error on get_recent_tweets")
            return {
                "status":status,
                "ids":ids
                }
    except Exception as e:
        telegram_bot_sendtext(f"Error on get_recent_tweets\n{e}")
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
            telegram_bot_sendtext("Error on get_media_type")
            return {
                "status":status,
                "media_type":""
                }
    except Exception as e:
        telegram_bot_sendtext(f"Error on get_media_type\n{e}")
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
            print("Adding new tweet.")
            update_log(last_tweets[x])
            if get_media_type(last_tweets[x])["media_type"] == "video":
                video_url = f"https://twitter.com/i/status/{last_tweets[x]}"
                print("Downloading video...")
                download_video(video_url, f"./media/{Constants.number}")
                print("Video downloaded!")
                print("Sending to discord...")
                send_discord_message("", f"./media/{Constants.number}.mp4", Constants.TOKEN, "1234567890")
                print("Video sent!")
                print("Deleting the archive...")
                os.remove(f"./media/{Constants.number}.mp4")
                print("Archive deleted.")
                update_number()
            elif get_media_type(last_tweets[x])["media_type"] == "photo":
                print("Downloading photo...")
                extension = twitter_image_dl(last_tweets[x], f"./media/{Constants.number}")["extension"]
                print("Photo downloaded!")
                print("Sending to discord...")
                send_discord_message("", f"./media/{Constants.number}{extension}", Constants.TOKEN, "1234567890")
                print("Photo sent!")
                print("Deleting the archive...")
                os.remove(f"./media/{Constants.number}{extension}")
                print("Archive deleted.")
                update_number()
            else:
                print("Error on main")
                telegram_bot_sendtext(f"Error on main\n{last_tweets[x]}\nskipping...")
                pass
        else:
            print("Old tweet.")
    return {"added_tweets":added_tweets}

if __name__ == "__main__":
    print(main())