from PyQt4 import QtCore
import urllib
from settings import *
import json
from threading import Thread

class Model(QtCore.QObject):
    searchCompleted = QtCore.pyqtSignal(object)

    def search(self, tag, tagArtists, tagThreshold):
        self.tag = tag
        self.tagArtists = tagArtists
        self.tagThreshold = tagThreshold
        thread = Thread(target = self.searchThreaded)
        thread.setDaemon(True)
        thread.start()

    def searchThreaded(self):
        #try:
        self.searchCompleted.emit("Getting artists by tag...")
        artists = self.getArtistsByTag(self.tag)
        if artists == None:
            self.searchCompleted.emit("No such tag")
            return
        artistListeners = []
        nArtists = len(artists)
        for i, artist in enumerate(artists):
            if not self.checkTagRelevance(artist):
                continue
            self.searchCompleted.emit("Getting artist info: {num}/{total}".format(num = i, total = nArtists))
            listeners = self.getArtistListeners(artist)
            artistListeners.append((listeners, artist))

        artistListeners.sort(key = lambda info: info[0], reverse = True)
        result = u"\n".join([u"{listeners}{artist}".format(listeners = str(info[0]).ljust(16), artist = info[1])
                            for info in artistListeners])
        #except Exception as e:
        #    self.searchCompleted.emit("Error:\n{error}".format(error = str(e)))
        #    return

        self.searchCompleted.emit(result)

    def getArtistsByTag(self, tag):
            url = "http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={tag}&api_key={apiKey}&format=json&limit={tagArtists}".format(
                  tag = urllib.quote_plus(tag), apiKey = lastfmKey, tagArtists = self.tagArtists)
            tagArtistsRes = json.loads(urllib.urlopen(url).read())
            if not "topartists" in tagArtistsRes:
                return None
            return [artist["name"] for artist in tagArtistsRes["topartists"]["artist"]]

    def getArtistListeners(self, artist):
            url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={apiKey}&format=json".format(
                  artist = urllib.quote_plus(artist.encode("utf-8")), apiKey = lastfmKey)
            artistInfoRes = json.loads(urllib.urlopen(url).read())
            return int(artistInfoRes["artist"]["stats"]["listeners"])

    
    def checkTagRelevance(self, artist):
            url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={artist}&api_key={apiKey}&format=json".format(
                  artist = urllib.quote_plus(artist.encode("utf-8")), apiKey = lastfmKey)
            artistTagsRes = json.loads(urllib.urlopen(url).read())
            for tag in artistTagsRes["toptags"]["tag"]:
                if int(tag["count"]) < self.tagThreshold:
                    return False
                if tag["name"] == self.tag:
                    return True
            return False
