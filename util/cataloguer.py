import requests, subprocess
from multiprocessing.pool import ThreadPool

class InfoRequester():
    """
    InfoRequesters should return queries in a json-object-like format.
    """
    def item_queries(self) -> dict:
        """
        Returns single item related queries.
        """
        raise NotImplementedError('Method not implemented. Return single item related queries.')

class JikanRequest(InfoRequester):
    def __init__(self, base_url : str) -> None:
        """
        base_url: Should include version too. Example: http://127.0.0.1:8000/v3
        """
        self.url = base_url

    def query_item(self, item_id):
        r = requests.get(self.url+'/anime/'+item_id)
        print(self.url+'/anime/'+item_id)
        return r.json()
    
    def query_img(self, item_id):
        r = requests.get(self.url+'/anime/'+item_id+'/pictures')
        return r.json()

    def item_queries(self) -> dict:
        """
        Returns callable queries for a single item query.
        """
        queries = {
            ('title'  , 'episodes',
             'aired'  , 'duration', 
             'rating' , 'score'   , 
             'title_japanese',
             'synopsis')        : lambda item : self.query_item(str(item['item'])) ,

            ('pictures',)       : lambda item : self.query_img(str(item['item']))
        }

        return queries

    def query_popular(self):
        r = requests.get(self.url+'/search/anime?q=&order_by=members&sort=desc&page=1')
        return r.json()

        
class YTRequest(InfoRequester):
    def __init__(self, ytdl_path='yt-dlp') -> None:
        """
        ytdl_path: Path to ytdl interface for video source url query.
        """
        self.ytdl_path = ytdl_path

    def get_video_source(self, title : str, genre : str, type : str) -> dict:
        vid_src = subprocess.run([
                                self.ytdl_path,
                                '--get-url', 
                                f'ytsearch1:"{title} {genre} {type}"'
                            ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout \
                            .decode('utf-8').split('\n',1)[0]

        return { 'video_source' : vid_src }

    def get_video_id(self, title : str, genre : str, type : str) -> dict:
        vid_id  = subprocess.run([
                                self.ytdl_path,
                                '--get-id', 
                                f'ytsearch1:"{title} {genre} {type}"'
                            ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout \
                            .decode('utf-8')

        return { 'video_id' : vid_id }


    def get_embed_video(self, title : str, genre : str, type : str) -> str:
        return { 'embeded' : "https://www.youtube.com/embed/" + self.get_video_id(title, genre, type)['video_id'] }


    def item_queries(self) -> dict:
        """
        Returns callable queries for a single item query.
        """
        queries = {
            ('video_source',)    : lambda item : self.get_video_source(item['title'], "anime", item['Type']+" trailer") ,
            ('embeded',)         : lambda item : self.get_embed_video(item['title'], "anime", item['Type']+" trailer")
        }

        return queries


class Cataloguer():
    def __init__(self, requesters : list[InfoRequester]):
        self.requesters = requesters                # Each requester has it's own queries.
        
    def query_from_requesters(self, prediction : dict) -> dict: # Takes a prediction spark Row asDict().
        for requester in self.requesters:
            queries = requester.item_queries()      # Get all queries for the item from the requester.
            for query in queries:                   # Get queries keys. AKA, what-the-query-does labels.
                json = queries[query](prediction)   # Make query to the API and store json. Passing object to lambdas.
                for tag in query:                   # For each tag indicated on the item_queries return object.
                    prediction[tag] = json[tag]     # Some queries may be used to obtain more than one result. We support this. Line 32.

        return prediction

    def catalogue_predictions(self, predictions : list[dict], n_cores = 4) -> list[dict]:
        with ThreadPool(n_cores) as p:
            return p.map(self.query_from_requesters, predictions)
