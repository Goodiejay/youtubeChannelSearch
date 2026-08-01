import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
Api_key = os.getenv('Api_key')

class UnexpectedError(Exception):
    pass

def info(api_key:str) -> dict:
    return {
                "q": "", 
                "part": "snippet",
                "type": "",
                "maxResults": 1,
                "key": f"{api_key}"
            }

def search_yt_video(search_keyword: str,params: dict) -> dict:
    url ="https://www.googleapis.com/youtube/v3/search?"
    params["q"] = f"{search_keyword}"
    params["type"] = "video"
    params["maxResults"] = 5
    try:
        response=requests.get(url=url, params = params)
        if response.status_code != 200:
            raise ValueError(f"No results for  {search_keyword}: {response.text}:  make sure you enter the right channel name")
        return response.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internat connection, check your internet and try again")
    except Exception as e:
        raise UnexpectedError(f"An unexpected error occured {e}") 
        
def display_Video_details(video_info: dict) -> dict:
    pass

def get_channel_id(channel_name: str, params: dict) -> str:
    url ="https://www.googleapis.com/youtube/v3/search?"
    params["q"] = f"{channel_name}"
    params["type"] = "channel"
    try:
        response=requests.get(url=url, params = params)
        response.raise_for_status
        response=response.json()
        return response["items"][0]["snippet"]["channelId"]
    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet connection, check your internet and try again")
    except Exception as e:
        raise UnexpectedError(f"An error occured: {e}")
    

def get_channel_playlist_id(channel: str, params: dict) ->  str: 
    url = "https://www.googleapis.com/youtube/v3/channels"
    del params["q"]
    del params["type"]
    del params["maxResults"]
    params["part"] = "snippet, statistics, contentDetails"
    params["id"]= f"{channel}"
    try:
        response = requests.get(url=url,params=params)
        response.raise_for_status()
        response= response.json()
        print("-"*40)
        print(f"Channel Name:\t{response["items"][0]["snippet"]["title"]}")
        print(f"Total Video Posted:\t{response["items"][0]["statistics"]["videoCount"]}")
        print(f"Total Subscribers:\t{response["items"][0]["statistics"]["subscriberCount"]}")
        return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except requests.exceptions.ConnectionError:
        raise ConnectionError
    except Exception as e:
        raise UnexpectedError


    
def get_video_ids(playlistId: str) -> str:
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params ={
        "part": "snippet,contentDetails",
        "playlistId": playlistId,
        "maxResults": 50,
        "key": Api_key
    }
    video_ids=[]
    try:
        response=requests.get(url=url,params=params)
        response.raise_for_status()
        response = response.json()
     
        for video in response["items"]:
            video_ids.append(video["contentDetails"]["videoId"])
        return ",".join(video_ids)
       
    
    except requests.exceptions.ConnectionError:
        raise ConnectionError("No internet connection, check your intenet and try again")
    except Exception as e:
        raise UnexpectedError(f"An error occured: {e}")

    
def display_Channel_videos_detail(videos: dict) :
   
    url = "https://www.googleapis.com/youtube/v3/videos"
    params={
        "part": "snippet,statistics,contentDetails",
        "id": videos,
        "key": Api_key
    }
    print(40)

    try:
        response= requests.get(url=url,params=params)
        print(response)
        if response.status_code != 200:
            raise ValueError(response.reason)
        response=response.json()
        print(23)

        print(json.dumps(response,indent=4))

    except requests.exceptions.ConnectionError:
        raise ConnectionError
    except Exception as e:
        raise UnexpectedError




def menu():
    print("="*40)
    print("YouTube".center(40))
    print("="*40)
    return input("1. Search for channel...\n2. Search video...\n3. exit\n?: ")


def main():
    while True:
        user_choice=menu()
        if user_choice == "1":
            channelName= input("Enter channel name: ")
            if not channelName:
                continue
            parameter=info(api_key=Api_key)
            try:
                channel=get_channel_id(channel_name=channelName, params=parameter)
                channel_playlist_id=get_channel_playlist_id(channel=channel, params=parameter)
                videos=get_video_ids(channel_playlist_id)
                print(11)
                display_Channel_videos_detail(videos)
            except ConnectionError as c:
                print(c)
                continue
            except UnexpectedError as u:
                print(u)
                continue
            except requests.exceptions.HTTPError as e:
                print(e)
                continue
            except ValueError as v:
                print(f"{v}")
                continue


        elif user_choice == "2":
                while True:
                    video = input("Search... : ")
                    if not video:
                        continue
                    params=info(api_key=Api_key)
                    try:
                        Video_info=search_yt_video(search_keyword=video,params=params)
                        display_Video_details(Video_info)
                    except ValueError as v:
                        print(f"{v}: Be more specific with your search")
                        continue
                    except ConnectionError as c:
                        print(c)
                        continue
                    except UnexpectedError as u:
                        print(u)
                    
        elif user_choice == "3":
            print("Goodbye...")
            exit()
        else:
            print("Must be 1 or 2")
            continue

if __name__ == "__main__":
    main()



# channel = input("ENTER NAME OF CHANNEL: ")
# g=info(api_key=Api_key)
# f=get_channel_id(channel_name=channel, params=g)
# print(f)
