import asyncio
from api import APIHandler
from database.DBHandler import DatabaseHandler
from utils.asyncOperations import *

# TODO: add sortBy to database
# TODO: add documentation
# TODO: add error handling

# https://docs.mongodb.com/manual/reference/operator/query/and/#op._S_and
# https://docs.mongodb.com/manual/reference/operator/query/all/
# https://stackoverflow.com/questions/8930915/append-a-dictionary-to-a-dictionary

class NewsAPI(APIHandler.APIHandler):
    def __init__(self):
        self.__apiKey = 'e389c21d0c544790b26d548fd5e620d1' # make this into .env variable, double underscore added to avoid accidental re-write (constant)
        self.database = DatabaseHandler()
        super().__init__()

    async def updateSources(self):
        sources = await self.getAPI('https://newsapi.org/v2/sources?',{'apiKey':self.__apiKey})
        sourcesList = sources['sources']

        async for source in aiter(sourcesList):
            id = source['id']
            name = source['name']
            description = source['description']
            url = source['url']
            category = source['category']
            language = source['language']
            country = source['country']

            post = {'_id':id, 'name':name, 'description':description, 'url':url, 'category':category, 'language':language, 'country':country}
            await self.database.update_one('NEWSAPI', 'sources', {'_id':id}, {'$set':post}, upsert=True)

    async def getCategories(self):
        categories = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Categories'})
        return categories[0]['CategoryList']

    async def getLanguages(self):
        languages = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Languages'})
        return languages[0]['LanguageList']

    async def getCountries(self):
        countries = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Countries'})
        return countries[0]['CountryList']

    async def getSources(self, category='', language='', country=''):
        filter = {'category':category, 'language':language, 'country':country}

        if not category:
            del filter['category']

        if not language:
            del filter['language']

        if not country:
            del filter['country']

        sources = await self.database.find('NEWSAPI', 'sources', filter)
        return sources

    async def getTopHeadlines(self, country, category, sources, query):
        pass

    async def getEverything(self, query, titleSearch, sources, domains, exludeDomains, fromDate, toDate, language, sortBy):
        pass

#TESTING ASYNC FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(NewsAPI().getSources())
print(test)