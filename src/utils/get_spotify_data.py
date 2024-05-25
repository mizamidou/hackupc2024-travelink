import requests

def get_top_artists(access_token):
    top_artists_url = 'https://api.spotify.com/v1/me/top/artists'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(top_artists_url, headers=headers)
    return response.json()

def extract_top_genres(top_artists):
    genre_count = {}
    for artist in top_artists['items']:
        for genre in artist['genres']:
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1
    # Sort genres by occurrence
    sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
    return [genre[0] for genre in sorted_genres][:5]  # Top 5 genres

def main():
    with open('src/utils/keys/token.key', 'r') as file:
        access_token = file.read()
    
    top_genres = None
    if access_token:
        top_artists = get_top_artists(access_token)
        top_genres = extract_top_genres(top_artists)
    
    return top_genres
   

if __name__ == "__main__":
    main()