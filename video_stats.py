import requests
import json 
import os 

from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")

CHANNEL_HANDLE = "@MrBeast"
maxResults = 50

def get_playlist_id():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        #print(json.dumps(data, indent=4)) 
      
        channel_items = data["items"][0]
        channel_playlisId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlisId)

        return channel_playlisId
    
    except requests.exceptions.RequestException as e:
        raise e

def get_video_id(playlist_Id):
    videos_id = []
    pageToken = None
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_Id}&key={API_KEY}'

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            for item in data["items"]:
                video_id = item["contentDetails"]["videoId"]
                videos_id.append(video_id)
            pageToken = data.get("nextPageToken")

            if not pageToken:
                break
            return videos_id
        

    except requests.exceptions.RequestException as e:
        raise e 
if __name__ == "__main__":
    playlist_Id = get_playlist_id()
