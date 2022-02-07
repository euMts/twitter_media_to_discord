import Constants
import requests
import json
import wget

# github.com/euMts

bearer_token = Constants.BEARER_TOKEN

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "get_image_py"
    return r

def get_image_url(image_id):
    try:
        request_url = f"https://api.twitter.com/2/tweets?ids={image_id}&expansions=attachments.media_keys&media.fields=url"
        response = requests.get(request_url, auth=bearer_oauth)

        if response.status_code != 200:
            return {
            "status":response.status_code,
            "url":"",
            "extension":""
            }
        else:
            url = json.loads(response.text)["includes"]["media"][0]["url"]
            extension = f'.{url.split(".")[len(url.split(".")) - 1]}'
            return {
                "status":response.status_code,
                "url":url,
                "extension":extension
                }
    except:
        return {
        "status":"",
        "url":"",
        "extension":""
        }

def twitter_image_dl(image_id, file_name):
    try:
        status, url, extension = get_image_url(image_id).values()
        print("Verifying the image...")
        if status == 200:
            print("Image found, downloading...")
            wget.download(url, out=f"{file_name}{extension}")
            print("\nImage downloaded.")
            return {"status":"Complete", "extension":extension}
        else:
            print("Error:\nPlease check the image_id")
            return{"Status":"Error", "extension":""}
    except Exception as e:
        return {"Status":str(e), "extension":""}

def main():
    twitter_image_dl("your_tweet_id", "your_file_name")

if __name__ == "__main__":
    main()