import asyncio
import os
from api import APIHandler
from database.DBHandler import DatabaseHandler
from utils.asyncOperations import *
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# TODO: add documentation

# NOTE: APIKEY HAS BEEN ADDED TO HEADER PARAMETER TO AVOID THINGS SUCH AS REQUEST SNIFFING

class NewsAPI(APIHandler.APIHandler):
    def __init__(self):
        self.apiKey = os.getenv('NEWS_API_KEY') # environment variable is used for security purposes.
        self.database = DatabaseHandler()
        super().__init__()

    async def updateSources(self):
        sources = await self.getAPI('https://newsapi.org/v2/sources?', headers={'X-Api-Key':self.apiKey})
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

        return 'Update Complete.'

    async def getCategories(self):
        categories = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Categories'})
        return categories[0]['CategoryList']

    async def getLanguages(self):
        languages = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Languages'})
        return languages[0]['LanguageList']

    async def getCountries(self):
        countries = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Countries'})
        return countries[0]['CountryList']

    async def getCountryNames(self):
        countryList = await self.getCountries()
        countries = [key async for dict in aiter(countryList) async for key in aiter(dict.keys())]  # retrieve all keys within the list of dictionaries

        return countries

    async def getSortBy(self):
        sortBy = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'SortBy'})
        return sortBy[0]['SortByList']

    async def queryCategory(self, categoryName):
        categoryList = await self.getCategories()

        if categoryName in categoryList:
            return True
        else:
            return False

    async def queryCountry(self, countryName):
        countries = await self.getCountryNames()

        if countryName in countries:
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
                return source['_id']
        else:
            return None

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
                sourceID = await self.querySource(source)
                if not sourceID:
                    raise ValueError(f'Invalid source(s) provided: {source}')
                else:
                    sourcesID = []
                    sourcesID.append(sourceID)
            filter['sources'] = ','.join(sourcesID)

            if country or category:
                raise ValueError('You cannot specify a country or category if you specify a source')

        if not country and not category and not sources and not query:
            raise ValueError('You need at least one of the required parameters! [country, category, sources, query]')

        articles = await self.getAPI('https://newsapi.org/v2/top-headlines?', {**filter, 'pageSize':100}, {'X-Api-Key':self.apiKey})
        return articles

    async def getEverything(self, query='', titleSearch='', sources='', domains='', exludeDomains='', fromDate='', toDate='', language='', sortBy=''):
        search = {'q':query, 'qInTitle':titleSearch, 'sources':sources, 'domains':domains, 'excludeDomains':exludeDomains, 'from':fromDate, 'to':toDate, 'language':language, 'sortBy':sortBy}
        filter = {key: value async for (key, value) in aiter(search.items()) if value} # for every key value pair in the filter, add it to the dictionary if the value is not an empty string

        if language:
            languageCode = await self.getLanguageCode(language)
            if languageCode:
                filter['language'] = languageCode
            else:
                raise ValueError(f'Invalid Language Provided: {language}')

        if sources:
            async for source in aiter(sources.split(',')):
                sourceID = await self.querySource(source)
                if not sourceID:
                    raise ValueError(f'Invalid source(s) provided: {source}')
                else:
                    sourcesID = []
                    sourcesID.append(sourceID)
            filter['sources'] = ','.join(sourcesID)

        if fromDate:
            initialDate = datetime.strptime(f'{fromDate}', '%B %d %Y').date()
            fromDate = str(initialDate)

        if toDate:
            finalDate = datetime.strptime(f'{toDate}', '%B %d %Y').date()
            if finalDate > datetime.today().date():
                raise ValueError("The final date cannot go past today's date!")
            else:
                toDate = str(finalDate)

        if fromDate and toDate:
            if finalDate < initialDate:
                raise ValueError('The initial date cannot not be earlier than the final date!')

        if sortBy:
            sortByList = await self.getSortBy()
            if sortBy not in sortByList:
                raise ValueError(f'Invalid category provided ({sortBy}), can only sort articles by [relevancy, popularity, publishedAt]')

        if not query and not titleSearch and not sources and not domains:
            raise ValueError('You need at least one of the required parameters! [query, titleSearch, sources, domains]')

        articles = await self.getAPI('https://newsapi.org/v2/everything?', {**filter, 'pageSize':100}, {'X-Api-Key':self.apiKey})
        return articles

'''
#TESTING ASYNC FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(NewsAPI().getLanguages())
print(test)
'''