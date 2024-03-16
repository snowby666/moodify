import json, locale
from urllib.request import urlopen
from urllib.parse import quote, quote_plus

import requests_html
from bs4 import BeautifulSoup
from ytmusicapi import YTMusic


class MusicArtist:


    __all__ = ['albums', 'singles', 'genres', 'tophits', 'similar']


    def __init__(self, name: str):
        ytm = YTMusic()
        result = ytm.search(name, "artists")[0]
        artist = result['artist']
        if name != artist:
            msg = f"Unable to find {name}.\n"
            msg += f"Using closest match instead: {artist}"
            print(msg)
        self.name, self.ytm = artist, ytm

    def _url(self):
        searchapi = 'https://itunes.apple.com/search?'
        albums = self.albums()
        lang, loc = locale.getdefaultlocale()[0].split("_")
        term = f"{albums[0]} by {self.name}"
        params = f'term={quote_plus(term)}&entity=album'
        params += f'&country={loc}&lang={lang}&media=music'
        url = searchapi + params
        return url

    def _album_url(self):
        url = self._url()
        if not url:
            print("Error building itunes request")
            return
        res = urlopen(url)
        try:
            assert res.status == 200
            content = res.read()
            resjson = json.loads(content.decode("utf-8"))
            result = resjson['results'][0]
            collection_url = result['collectionViewUrl']
            track_count = int(result['trackCount'])
            catalogue_start_id = \
                int(collection_url.split('/')[-1].split('?')[0])
            catalogue_end_id = \
                catalogue_start_id + (track_count - 1)
            i = f'{catalogue_start_id}-{catalogue_end_id}'
            album_url = f'{collection_url}?i={i}'
            return album_url
        except:
            print(f"Access Denied: Status Code {res.status}")
    
    def _schema(self):
        album_url = self._album_url()
        if album_url:
            res = urlopen(album_url)
            try:
                assert res.status == 200
                content =  res.read()
                assert type(content) == bytes
                html = content.decode("utf-8")
                html = BeautifulSoup(html, 'lxml')
                html_tag = {
                    'element': 'script',
                    'class': {"name": "schema:music-album"}}
                schema = html.find(html_tag['element'], html_tag['class'])
                schema = json.loads(schema.contents[0])
                return schema
            except:
                msg = f"Access Denied: Status Code {res.status}\n"
                msg += "Unable to fetch schema."
                print(msg)

    def albums(self):
        try:
            results = self.ytm.search(self.name, "albums")
            albums = []
            for result in results:
                if result['type'] == 'Album':
                    album = result['title']
                    albums.append(album)
            return albums
        except:
            print("Unable to fetch artist's albums.")

    def singles(self):
        try:
            results = self.ytm.search(self.name, "albums")
            singles = []
            for result in results:
                if result['type'] == 'Single':
                    single = result['title']
                    singles.append(single)
            return singles
        except:
            print("Unable to fetch artist's albums.")

    def tophits(self):
        schema = self._schema()
        if not schema:
            return
        examples = \
            [f"{track['name']} | {self.name}" \
            for track in schema['workExample']]
        return examples
        
    def genres(self):
        schema = self._schema()
        if not schema:
            return 
        genres = schema['genre']
        return genres

    def similar(self):
        session = None
        try:
            artists = []
            base = "https://www.allmusic.com/"
            session = requests_html.HTMLSession()
            res = session.get(base+"search/artists/"+quote(self.name))
            params = res.text.split(self.name)[13]
            params = params.split('href="/')[1]
            params = params.split('" title="')[0]  
            artist_page = "https://www.allmusic.com/" + params
            res = session.get(f'{artist_page}/related')
            session.close()
            results = res.text.split('Similar To')[1].split('<li>\n')
            for result in results:
                if '/artist/' in result:
                    href_name = result.split('}">')
                    name = href_name[1].split('</a>')[0]
                    origin_tag = f" ~ {self.name}"
                    artists.append(name+origin_tag)
            return artists
        except Exception as e:
            if session:
                try:
                    session.close()
                except:
                    pass
            msg = "Unable to fetch similar artists.\n"
            msg += f"Execption: {str(e)}"
            print(msg)