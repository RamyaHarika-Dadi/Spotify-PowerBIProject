import pandas as pd
import requests

# Load your dataset
spotify_data = pd.read_csv("spotify-2023.csv", encoding="ISO-8859-1")


# Spotify API credentials
client_id = "enter client_id######"
client_secret = "enter client_secret######"

# Step 1: Obtain an OAuth token
auth_url = "https://accounts.spotify.com/api/token"
auth_response = requests.post(
    auth_url,
    {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    },
)
auth_data = auth_response.json()
access_token = auth_data["access_token"]

# Step 2: Function to fetch cover URL
def fetch_cover_url(track_name, artist_name):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"track:{track_name} artist:{artist_name}", "type": "track", "limit": 1}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["album"]["images"][0]["url"]
    return None

# Step 3: Apply the function to your dataset
spotify_data["cover_url"] = spotify_data.apply(
    lambda row: fetch_cover_url(row["track_name"], row["artist(s)_name"]), axis=1
)

# Save the updated dataset
spotify_data.to_csv("spotify_with_covers.csv", index=False)
print("Cover URLs added and saved to 'spotify_with_covers.csv'.")
