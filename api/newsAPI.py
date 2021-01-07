import asyncio
from api import APIHandler
from database.DBHandler import DatabaseHandler
from utils.asyncOperations import *

# TODO: add sortBy to database
# TODO: add documentation
# TODO: add error handling

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

    async def queryCategory(self, categoryName):
        categoryList = await self.getCategories()

        if categoryName in categoryList:
            return True
        else:
            return False

    async def getLanguageCode(self, languageName):
        languageList = await self.getLanguages()
        languages = [key async for dict in aiter(languageList) async for key in aiter(dict.keys())] # retrieve all keys within the list of dictionaries

        if languageName in languages:
            async for language in aiter(languageList): #every dict
                async for key in aiter(language): #every key
                    if key == languageName:
                        return language[languageName]
        else:
            return False

    async def getCountryCode(self, countryName):
        countryList = await self.getCountries()
        countries = [key async for dict in aiter(countryList) async for key in aiter(dict.keys())] # retrieve all keys within the list of dictionaries

        if countryName in countries:
            async for country in aiter(countryList): #every dict
                async for key in aiter(country): #every key
                    if key == countryName:
                        return country[countryName]
        else:
            return False

    async def getSources(self, category='', language='', country='', name=''):
        search = {'category':category, 'language':language, 'country':country, 'name':name}
        filter = {key: value async for (key, value) in aiter(search.items()) if value}  # removes keys that contain empty string as value

        if language:
            languageCode = await self.getLanguageCode(language)
            filter['language'] = languageCode

        if country:
            countryCode = await self.getCountryCode(country)
            filter['country'] = countryCode

        sources = await self.database.find('NEWSAPI', 'sources', filter)
        return sources

    async def querySource(self, sourceName):
        sourcesList = await self.getSources()

        async for source in aiter(sourcesList):
            if source['name'] == sourceName:
                return True
        else:
            return False

    async def getTopHeadlines(self, country='', category='', sources='', query=''):
        search = {'country':country, 'category':category, 'sources':sources, 'q':query}
        filter = {key: value async for (key, value) in aiter(search.items()) if value} # removes keys that contain empty string as value

        if country:
            countryCode = await self.getCountryCode(country)
            filter['country'] = countryCode

        if category:
            checkCategories = await self.queryCategory(category)
            if not checkCategories:
                raise ValueError('This is not a valid category')

        if sources:
            async for source in aiter(sources.split(',')):
                sourceCheck = await self.querySource(source)
                if not sourceCheck:
                    raise ValueError(f'Invalid source(s) provided: {source}')

            if country or category:
                raise ValueError('You cannot specify a country or category if you specify a source')

        if not filter:
            raise TypeError('you need at least one parameter! (country, category, sources, query)')

        # check if the filter/query is already in the database
        # if so, check if the date is outdated by a day or so
        # if it is update it, if not output it as the headlines for today

        headlines = await self.getAPI('https://newsapi.org/v2/top-headlines?', {**filter, 'pageSize':100, 'apiKey':self.__apiKey})
        return headlines


    async def getEverything(self, query='', titleSearch='', sources='', domains='', exludeDomains='', fromDate='', toDate='', language='', sortBy=''):
        search = {'q':query, 'qInTitle':titleSearch, 'sources':sources, 'domains':domains, 'excludeDomains':exludeDomains, 'from':fromDate, 'to':toDate, 'language':language, 'sortBy':sortBy}
        filter = {key: value async for (key, value) in aiter(search.items()) if value} # for every key value pair in the filter, add it to the dictionary if the value is not an empty string

        if language:
            languageCode = await self.getLanguageCode(language)
            filter['language'] = language

#TESTING ASYNC FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(NewsAPI().getTopHeadlines())
print(test)