from . import marklinkous

__all__ = ['albums','songs','I']

class I:
    class will:
        class always:
            class remember:
                class you:
                    pass

_albums_name = [i for i in dir(marklinkous) if not i.startswith('_')]
_albums = {}

for alb in _albums_name:
    if alb not in _albums: _albums[alb] = []
    album_obj = getattr(marklinkous,alb)
    for song in dir(album_obj):
        if not song.startswith('__'):
            _albums[alb].append({
                'album':alb,
                'name':song,
                'lyric':getattr(album_obj,song),
            })

class Song:
    def __init__(self,song):
        '''
        { 'album':album,
          'name':name,
          'lyric':lyric }
        '''
        self._song = song

    def __str__(self):
        song = []
        song.append('<<{}>>'.format(self._song['album']))
        song.append('    <{}>'.format(self._song['name']))
        lyric = list(map(lambda i:'        {}'.format(i),self._song['lyric'].splitlines()))
        lyric = lyric if lyric else ['        [ None lyric ]']
        song.extend(lyric)
        return '\n'.join(song)

    def __repr__(self):
        return self.__str__()

class Songs:
    def __init__(self,albums):
        self._albums = albums
        for _,album in self._albums.items():
            for song in album:
                setattr(self,song['name'],Song(song))

    def __str__(self):
        songs =[]
        for albname,album in self._albums.items():
            songs.append('<<{}>>'.format(albname))
            for song in album:
                songs.append('    <{}>'.format(song['name']))
            songs.append('')
        return '\n'.join(songs)

    def __repr__(self):
        return self.__str__()

class Album:
    def __init__(self,album):
        self._album = album

    def __str__(self):
        album = []
        if self._album:
            album.append('<<{}>>'.format(self._album[0]['album']))
        for song in self._album:
            '''
            { 'album':album,
              'name':name,
              'lyric':lyric }
            '''
            album.append('    <{}>'.format(song['name']))
            lyric = list(map(lambda i:'        {}'.format(i),song['lyric'].splitlines()))
            lyric = lyric if lyric else ['        [ None lyric ]']
            album.extend(lyric)
            album.append('')
        return '\n'.join(album)

    def __repr__(self):
        return self.__str__()

class Albums:
    def __init__(self,albums):
        self._albums = albums
        for album in self._albums:
            setattr(self,album,Album(self._albums[album]))

    def __str__(self):
        albums = list(map(lambda i:'<<{}>>'.format(i),self._albums))
        return '\n'.join(albums)

    def __repr__(self):
        return self.__str__()

albums = Albums(_albums)
songs  = Songs(_albums)