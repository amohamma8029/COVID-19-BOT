import asyncio
from api import APIHandler

class YoutubeAPI(APIHandler.APIHandler):
    def __init__(self):
        super().__init__()