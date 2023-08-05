from .utils.http_request import http
from .utils.parser import parser
#from .utils.errors import error
from .utils.checker import check
from .song import Song
#initializing other things here
class client:
    def __init__(self):
        self.gameVersion = '21'
        self.binaryVersion = '35'
        self.secret = "Wmfd2893gb7"

    def get_song(self, songid: int = 0):
        if (songid == 0):
            raise error.IDNotSpecified()
        else:
            parameters = {
                "gameVersion": self.gameVersion,
                "binaryVersion": self.binaryVersion,
                "songID": str(songid),
                "secret": self.secret
            }
            print(parameters)
            resp = http.SendHTTPRequest("getGJSongInfo", parameters)
            if resp == '-1':
                raise error.SongNotFound()
            else:
                resp = resp.split("~|~")
                SongInfo = parser.SongParse(resp)

        return Song(
            name=SongInfo['name'], author=SongInfo['author'],
            _id=SongInfo['id'], size=SongInfo['size'],
            size_mb=SongInfo['size_mb'], links=SongInfo['links']
        )

    def get_user(self, userid: int = 0):
        if userid == 0:
            raise error.IDNotSpecified()
        else:
            parameters = {
                "gameVersion": self.gameVersion,
                "binaryVersion": self.binaryVersion,
                "gdw": "0",
                "targetAccountID": userid,
                "secret": self.secret
            }
            resp = http.SendHTTPRequest("getGJUserInfo20", parameters)
    
            if resp == "-1":          
                raise error.UserNotFound()
    
            u = resp.split(":")
            m = u[21]
            fr = u[23]
            com = u[25]
            if m == '0':
                messages = 'Opened to all'
            if m == '1':
                messages = 'Opened to friends only'
            if m == '2':
                messages = 'Closed'
            if fr == '0':
                fr_req = 'Enabled'
            if fr == '1':
                fr_req = 'Disabled'
            if com == '0':
                comm_history = 'Opened to all'
            if com == '1':
                comm_history = 'Opened to friends only'
            if com == '2':
                comm_history = 'Closed'
            if u[27] == '':
                yt_link = None
            if u[27] != '':
                yt_link = f'https://www.youtube.com/{u[27]}'
            if u[53] == '':
                twt = None
                twt_link = None
            if u[53] != '':
                twt = f'@{u[53]}'
                twt_link = f'https://twitter.com/@{twt}'
            if u[55] == '':
                twch = None
                twch_link = None
            if u[55] != '':
                twch = u[55]
                twch_link = f'https://twitch.tv/{twch}'
            return User(
                username=u[1], userid=int(u[3]), accountid=int(u[49]), coins=int(u[5]), usercoins=int(u[7]),
                stars=int(u[13]), diamonds=int(u[15]), demons=int(u[17]), cp=int(u[19]), rank=int(u[47]),
                dms=messages, friend_requests=fr_req, comment_history=comm_history,
                youtube_link=yt_link, twitter=twt, twitter_link=twt_link,
                twitch=twch, twitch_link=twch_link, status=int(u[57])  #ok, needa finish w/ icons (main and all) and colors
            ) #add this to parser, and initialize it from there
#actually, convert this to map (or something what's it called in python) xd
                        
    def search_for(self, item: str = None, **kwargs):
        #allows to search with format:
        #gd.search_for('levels', query='VorteX', id_mode=True, limit=10)
        if (item is None) or (item not in ['levels', 'users']):
            raise error.MissingArguments()
        else:
            prepare = check.run_search_check(kwargs)
            if prepare[0]:
                pass #we do our search stuff here
                #prepare[1]-id_mode, prepare[2]-limit
