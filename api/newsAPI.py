import asyncio
from api import APIHandler
from utils.asyncOperations import *

class NewsAPI(APIHandler.APIHandler):
    def __init__(self):
        super().__init__()

#TODO: put all the country codes for the newsapi in the database
#TODO: put all the languages for the newsapi in the database
#TODO: put all the topics for the newsapi in the database