from flask import Flask, render_template, request, jsonify
import lyricsgenius as lg
import csv
import base64

access_token = "LC2defTjjGgEM09GFXIhStvjR9d_YnZ3WArkc_yoW3aA1ewUgCbJGVk8k2BYuveo"
app = Flask(__name__, template_folder='templates')

# Define routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lyrics", methods=["POST"])
def process_form():
    songInput = request.form.get("searchInput")
    
    if "-" in songInput:
        songartistSeparated = songInput.split(" - ")
        songName = songartistSeparated[0].title()
        artistName = songartistSeparated[1].title()

    else:
        songName = songInput
    
    with open('Artists.csv') as csvfile:
        genius = lg.Genius(access_token)
        
        # Artist Database
        artistsCSV = csv.reader(csvfile, delimiter='\n')
        artistsDatabase = []
        
        for row in artistsCSV:
            artistsDatabase.append(row)
        
        flattenedArtistsDatabase = []

        for sublist in artistsDatabase:
            for artist in sublist:
                flattenedArtistsDatabase.append(artist)
        
        # Initializing song name and artist as key value pairs
        data = []
        artistNames = []
        songTitles = []
        
        song = genius.search_song(songInput)
        songDict = genius.search_songs(songName)
        songResults = songDict["hits"]
        
        for hit in songResults:
            song_info = hit["result"]
            artistName = song_info.get("primary_artist").get("name")
            songTitle = song_info.get("title")
            data.append({artistName + " , " + songTitle})   
            artistNames.append(artistName)
            songTitles.append(songTitle)
        
        
        # New Search Method (Song Name)
        secularArtistNames = []
        christianArtistNames = []
        artistSongforHTML = []


        
        for artist in artistNames:
            if artist in flattenedArtistsDatabase:
                christianArtistNames.append(artist)
            elif artist not in flattenedArtistsDatabase:
                secularArtistNames.append(artist)
                #return render_template("404.html")
       
                
        for name in christianArtistNames:
            artistSongforHTML.append(songInput + " - " + name)
            print(songInput + " - " + name)


        # Output Test Code
        print("Secular: " + str(secularArtistNames))
        print("Christian: " + str(christianArtistNames))

        # Initial Search Method (Song - Artist Name)
        """if any(artistName in sublist for sublist in artistsDatabase):
            artist = genius.search_artist(artistName, max_songs=1, sort="title")
            song = artist.song(songName)
            
        else:
            return render_template("404.html")"""
    
    encoded_lyrics = base64.b64encode(song.lyrics.encode()).decode()
    return render_template("lyrics.html", content=encoded_lyrics, song=songName+ " - " + artistName)











# Search Function using Artist and Song Name
@app.route("/lyrics", methods=["POST"])
def process_form():
    songInput = request.form.get("searchInput")
    
    if "-" in songInput:
        songartistSeparated = songInput.split(" - ")
        songName = songartistSeparated[0].title()
        artistName = songartistSeparated[1].title()

    else:
        songName = songInput
    
    with open('Artists.csv') as csvfile:
        genius = lg.Genius(access_token)
        
        # Artist Database
        artistsCSV = csv.reader(csvfile, delimiter='\n')
        artistsDatabase = []
        
        for row in artistsCSV:
            artistsDatabase.append(row)
        
        flattenedArtistsDatabase = []

        for sublist in artistsDatabase:
            for artist in sublist:
                flattenedArtistsDatabase.append(artist)
        
        # Initializing song name and artist as key value pairs
        data = []
        artistNames = []
        songTitles = []
        
        
        songDict = genius.search_songs(songName)
        songResults = songDict["hits"]
        
        for hit in songResults:
            song_info = hit["result"]
            artistName = song_info.get("primary_artist").get("name")
            songTitle = song_info.get("title")
            data.append({artistName + " , " + songTitle})   
            artistNames.append(artistName)
            songTitles.append(songTitle)
        
        
        # New Search Method (Song Name)
        secularArtistNames = []
        christianArtistNames = []
        artistSongforHTML = []


        
        for artist in artistNames:
            if artist in flattenedArtistsDatabase:
                christianArtistNames.append(artist)
            elif artist not in flattenedArtistsDatabase:
                secularArtistNames.append(artist)
       
                
        for name in christianArtistNames:
            artistSongforHTML.append(songInput + " - " + name)
            print(songInput + " - " + name)


        # Output Test Code
        print("Secular: " + str(secularArtistNames))
        print("Christian: " + str(christianArtistNames))

        # Initial Search Method (Song - Artist Name)
        if any(artistName in sublist for sublist in artistsDatabase):
            song = genius.search_song(songInput)
        
        
    encoded_lyrics = base64.b64encode(song.lyrics.encode()).decode()
    return render_template("lyrics.html", content=encoded_lyrics, song=songName+ " - " + artistName)