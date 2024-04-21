import lyricsgenius as lg

songName = input("Song Name: ")
   
genius = lg.Genius("LC2defTjjGgEM09GFXIhStvjR9d_YnZ3WArkc_yoW3aA1ewUgCbJGVk8k2BYuveo")

song = genius.search_song(songName)
songDict = genius.search_songs(songName)
songResults = songDict["hits"]

data = []
for hit in songResults:
    song_info = hit["result"]
    name = song_info.get("primary_artist").get("name")
    title = song_info.get("title")
    data.append({'name': name, 'title': title})

print (data)

