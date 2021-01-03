import asyncio
from api import APIHandler
from utils.asyncOperations import *

#TODO: add sortBy to database

class NewsAPI(APIHandler.APIHandler):
    def __init__(self):
        self.__apiKey = 'e389c21d0c544790b26d548fd5e620d1' # make this into .env variable, double underscore added to avoid accidental re-write (constant)
        super().__init__()

    async def updateSources(self, sources, language, country):
        pass

    async def getTopHeadlines(self, country, category, sources, query):
        pass

    async def getEverything(self, query, titleSearch, sources, domains, exludeDomains, fromDate, toDate, language, sortBy):
        pass