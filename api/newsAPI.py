import asyncio
import os
from api import APIHandler
from database.DBHandler import DatabaseHandler
from utils.asyncOperations import *
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# NOTE: APIKEY HAS BEEN ADDED TO HEADER PARAMETER TO AVOID THINGS SUCH AS REQUEST SNIFFING

class NewsAPI(APIHandler.APIHandler):
    """
    A class to format and handle requests from the news API. Inherits from the base APIhandler class.

    ...

    Attributes
    ----------
    baseURL : str
        the base link in the form of a string that will be used to access the data

    payload : dict
        a dictionary of strings that lets you pass on specific arguments into the link (empty by default)

    apiKey : str
        a string that contains the key to access the news API

    database : DatabaseHandler
        an instance of the DatabaseHandler class

    Methods
    -------
    updateSources()
        Updates the list of sources within the database.

    getCategories()
        Gets a list of all valid categories and returns it.

    getLanguages()
        Gets a list of all valid languages and returns it.

    getCountries()
        Gets a list of all valid countries and returns it.

    getCountryNames()
        Gets a list of all country names and returns it.

    getSortBy()
        Gets a list of all article sort methods and returns it.

    queryCategory(categoryName)
        Checks if a category is valid.

    queryCountry(countryName)
        Checks if a country is valid.

    getLanguageCode(languageName)
        Returns the ISO-639-1 code associated with a language.

    getCountryCode(countryName)
        Returns the ISO-639-1 code associated with a country.

    getSources(category='', language='', country='', name='')
        Returns a list of all valid sources.

    querySource(sourceName)
        Checks if a source is valid.

    getTopHeadlines(country='', category='', sources='', query='')
        Gets the recent and latest headlines related to a query.

    getEverything(query='', titleSearch='', sources='', domains='', exludeDomains='', fromDate='', toDate='', language='', sortBy='')
        Gets ALL articles related to a query.
    """

    def __init__(self):
        """
        Parameters
        ----------
        ...
        """

        self.apiKey = os.getenv('NEWS_API_KEY') # environment variable is used for security purposes
        self.database = DatabaseHandler() # initialize an instance of the DatabaseHandler class
        super().__init__() # inherit from parent class

    async def updateSources(self):
        '''Updates the list of sources within the database.

        Parameters
        ----------
        ...

        Returns
        -------
        str
            a string that says that the update is complete

        Raises
        ------
        ...
        '''

        sources = await self.getAPI('https://newsapi.org/v2/sources?', headers={'X-Api-Key':self.apiKey}) # grabs api
        sourcesList = sources['sources'] # gets all the sources

        # iterates through each source and grabs the id, name, description, url, category, language, and country
        async for source in aiter(sourcesList):
            id = source['id']
            name = source['name']
            description = source['description']
            url = source['url']
            category = source['category']
            language = source['language']
            country = source['country']

            post = {'_id':id, 'name':name, 'description':description, 'url':url, 'category':category, 'language':language, 'country':country} # maps each variable to a dictionary
            await self.database.update_one('NEWSAPI', 'sources', {'_id':id}, {'$set':post}, upsert=True) # updates each source (NOTE: with upsert = True, if it doesn't already exist it will just insert it)

        return 'Update Complete.'

    async def getCategories(self):
        '''Gets a list of all valid categories and returns it.

        Parameters
        ----------
        ...

        Returns
        -------
        list
            a list containing all the valid categories

        Raises
        ------
        ...
        '''

        categories = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Categories'}) # finds the list of categories from database
        return categories[0]['CategoryList'] # returns list

    async def getLanguages(self):
        '''Gets a list of all valid languages and returns it.

        Parameters
        ----------
        ...

        Returns
        -------
        list
            a list of dictionaries containing the name of the language and the language code in ISO-639-1 format

        Raises
        ------
        ...
        '''

        languages = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Languages'}) # finds list of languages from database
        return languages[0]['LanguageList'] #returns list

    async def getCountries(self):
        '''Gets a list of all valid countries and returns it.

        Parameters
        ----------
        ...

        Returns
        -------
        list
            a list of dictionaries containing the name of the country and the country code in ISO-639-1 format

        Raises
        ------
        ...
        '''

        countries = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'Countries'}) # finds list of countries from database
        return countries[0]['CountryList'] # returns list

    async def getCountryNames(self):
        '''Gets a list of all country names and returns it.

        Parameters
        ----------
        ...

        Returns
        -------
        list
            a list containing JUST the names of all supported countries

        Raises
        ------
        ...
        '''

        countryList = await self.getCountries() # gets list of countries
        countries = [key async for dict in aiter(countryList) async for key in aiter(dict.keys())]  # retrieve all keys within the list of dictionaries and puts them in a list

        return countries

    async def getSortBy(self):
        '''Gets a list of all article sort methods and returns it.

        Parameters
        ----------
        ...

        Returns
        -------
        list
            a list containing all methods of sorting articles

        Raises
        ------
        ...
        '''

        sortBy = await self.database.find('NEWSAPI', 'miscellaneous', {'_id':'SortBy'}) # gets sort methods from database
        return sortBy[0]['SortByList'] # returns list

    async def queryCategory(self, categoryName):
        '''Checks if a category is valid.

        Parameters
        ----------
        categoryName : str
            the name of the category (ex. general, health, entertainment)

        Returns
        -------
        bool
            returns True if the category specified is within the list of valid categories

        Raises
        ------
        ...
        '''

        categoryList = await self.getCategories() # gets list of categories

        # checks if the category specified is in the list of valid categories, returns True if yes, returns False if no
        if categoryName in categoryList:
            return True
        else:
            return False

    async def queryCountry(self, countryName):
        '''Checks if a country is valid.

        Parameters
        ----------
        countryName : str
            the name of the country (ex. Canada, United States, Japan)

        Returns
        -------
        bool
            returns True if the category specified is within the list of valid categories

        Raises
        ------
        ...
        '''

        countries = await self.getCountryNames() # gets list of all country names

        # checks if the specified country is in the list of all valid country names, returns True if yes, False if no
        if countryName in countries:
            return True
        else:
            return False

    async def getLanguageCode(self, languageName):
        '''Returns the ISO-639-1 code associated with a language.

        Parameters
        ----------
        languageName : str
            the name of the language (ex. English, French, German)

        Returns
        -------
        str
            the ISO-639-1 code associated with the language

        Raises
        ------
        ...
        '''

        languageList = await self.getLanguages() # gets list of languages
        languages = [key async for dict in aiter(languageList) async for key in aiter(dict.keys())] # retrieve all keys within the list of dictionaries and puts them in a a list

        # checks if the language specifed is valid, returns the language code if yes, returns False if no
        if languageName in languages:
            async for language in aiter(languageList): #every dict
                async for key in aiter(language): #every key
                    if key == languageName:
                        return language[languageName]
        else:
            return False

    async def getCountryCode(self, countryName):
        '''Returns the ISO-639-1 code associated with a country.

        Parameters
        ----------
        countryName : str
            the name of the country (ex. Canada, United States, Japan)

        Returns
        -------
        str
            the ISO-639-1 code associated with the country

        Raises
        ------
        ...
        '''

        # checks if the country specifed is valid, returns the country code if yes, returns False if no
        countryList = await self.getCountries()
        countries = [key async for dict in aiter(countryList) async for key in aiter(dict.keys())] # retrieve all keys within the list of dictionaries and puts them in a list

        if countryName in countries:
            async for country in aiter(countryList): #every dict
                async for key in aiter(country): #every key
                    if key == countryName:
                        return country[countryName]
        else:
            return False

    async def getSources(self, category='', language='', country='', name=''):
        '''Returns a list of all valid sources.

        Parameters
        ----------
        category : str
            the name of a category (ex. general, health, entertainment)

        language : str
            the name of a language (ex. English, French, German)

        country : str
            name of a country (ex. Canada, United States, Japan)

        Returns
        -------
        str
            a list of dictionaries containing information for all sources.

        Raises
        ------
        ...
        '''

        search = {'category':category, 'language':language, 'country':country, 'name':name} # takes parameters and maps the values to a dict
        filter = {key: value async for (key, value) in aiter(search.items()) if value}  # removes keys that contain empty string as value

        # checkes if language provided is valid, if so, it gets the language code
        if language:
            languageCode = await self.getLanguageCode(language)
            filter['language'] = languageCode

        # checks if country provided is valid, if so, it gets the country code
        if country:
            countryCode = await self.getCountryCode(country)
            filter['country'] = countryCode

        sources = await self.database.find('NEWSAPI', 'sources', filter) # finds sources with the given filter (NOTE: if blank, it will simply return ALL sources)
        return sources

    async def querySource(self, sourceName):
        '''Checks if a source is valid.

        Parameters
        ----------
        sourceName : str
             the name of a source (ex. ABC News, CBC News, Wired)

        Returns
        -------
        str/bool
            returns either the source ID or returns None

        Raises
        ------
        ...
        '''

        sourcesList = await self.getSources() # gets all sources

        # checks if the name of the source is in the database, returns source ID if yes, returns False if no
        async for source in aiter(sourcesList):
            if source['name'] == sourceName:
                return source['_id']
        else:
            return None

    async def getTopHeadlines(self, country='', category='', sources='', query=''):
        '''Gets the recent and latest headlines related to a query.

        Parameters
        ----------
        country : str
             the name of a country (ex. Canada, United States, Japan)

        category : str
            the name of a category (ex. general, health entertainment)

        sources : str
            A comma-seperated string of identifiers (maximum 20) for the news sources or blogs you want headlines from (ex. ABC News,CBC News,Google News)

        query : str
            a key-word or phrase to look for in articles

        Returns
        -------
        dict
            a dict containing all the data related to that specific query

        Raises
        ------
        ValueError
            if the category, sources are invalid OR if you have a source with either a country or category OR if you all paramters are blank.
        '''
        search = {'country':country, 'category':category, 'sources':sources, 'q':query} # puts all parameters in dictionary
        filter = {key: value async for (key, value) in aiter(search.items()) if value} # removes keys that contain empty string as value

        # if country is provided, gets the country code
        if country:
            countryCode = await self.getCountryCode(country)
            filter['country'] = countryCode

        # checks if category provided is valid, if no, raises a ValueError
        if category:
            checkCategories = await self.queryCategory(category)
            if not checkCategories:
                raise ValueError('This is not a valid category')

        # checks if all sources provided are valid, if no, raises a value error, if yes, gets the source ID for each source
        if sources:
            async for source in aiter(sources.split(',')):
                sourceID = await self.querySource(source)
                if not sourceID:
                    raise ValueError(f'Invalid source(s) provided: {source}')
                else:
                    sourcesID = []
                    sourcesID.append(sourceID)
            filter['sources'] = ','.join(sourcesID)

            # if the source parameter exists, then there cannot be a country or category parameter, if there is it will raise a ValueError
            if country or category:
                raise ValueError('You cannot specify a country or category if you specify a source')

        # if the paramters are empty
        if not country and not category and not sources and not query:
            raise ValueError('You need at least one of the required parameters! [country, category, sources, query]')

        articles = await self.getAPI('https://newsapi.org/v2/top-headlines?', {**filter, 'pageSize':100}, {'X-Api-Key':self.apiKey}) # grabs all articles
        return articles

    async def getEverything(self, query='', titleSearch='', sources='', domains='', exludeDomains='', fromDate='', toDate='', language='', sortBy=''):
        '''Gets ALL articles related to a query.

        Parameters
        ----------
        query : str
            a key-word or phrase to look for in articles

        titleSearch : str
            a key-word or phrase to look for in the title articles only

        sources : str
            a comma-seperated string of identifiers (maximum 20) for the news sources or blogs you want headlines from (ex. ABC News,CBC News,Google News)

        domains : str
            a comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search to

        exludeDomains : str
            a comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to remove from the results

        fromDate : str
            a date and optional time for the oldest article allowed (ex. January 1 2020)

        toDate : str
            a date and optional time for the newest article allowed (ex. March 3 2020)

        language : str
            the name of a language (ex. English, French, German)

        sortBy : str
            a specifier how the articles will be sorted (relevancy, popularity, publishedAt)

        Returns
        -------
        dict
            a dict containing all the data related to that specific query

        Raises
        ------
        ValueError
            if the language, sources are invalid OR if the toDate is greater than the fromDate OR if you all paramters are blank.
        '''
        search = {'q':query, 'qInTitle':titleSearch, 'sources':sources, 'domains':domains, 'excludeDomains':exludeDomains, 'from':fromDate, 'to':toDate, 'language':language, 'sortBy':sortBy} # maps the values of the parameters to a dictionary
        filter = {key: value async for (key, value) in aiter(search.items()) if value} # for every key value pair in the filter, add it to the dictionary if the value is not an empty string

        # checks if language is valid, if not, raises ValueError
        if language:
            languageCode = await self.getLanguageCode(language)
            if languageCode:
                filter['language'] = languageCode
            else:
                raise ValueError(f'Invalid Language Provided: {language}')

        # checks if sources are valid, if not, raises ValueError
        if sources:
            async for source in aiter(sources.split(',')):
                sourceID = await self.querySource(source)
                if not sourceID:
                    raise ValueError(f'Invalid source(s) provided: {source}')
                else:
                    sourcesID = []
                    sourcesID.append(sourceID)
            filter['sources'] = ','.join(sourcesID)

        # formats date and turns it into a string
        if fromDate:
            initialDate = datetime.strptime(f'{fromDate}', '%B %d %Y').date()
            fromDate = str(initialDate)

        # formats date and turns it into a string, if the date goes past today's date then it will raise a ValueError
        if toDate:
            finalDate = datetime.strptime(f'{toDate}', '%B %d %Y').date()
            if finalDate > datetime.today().date():
                raise ValueError("The final date cannot go past today's date!")
            else:
                toDate = str(finalDate)

        # if the initial date is newer than the final date then it will raise a ValueError
        if fromDate and toDate:
            if finalDate < initialDate:
                raise ValueError('The initial date cannot not be earlier than the final date!')

        # checks if sort method is valid, if not, raises ValueError
        if sortBy:
            sortByList = await self.getSortBy()
            if sortBy not in sortByList:
                raise ValueError(f'Invalid category provided ({sortBy}), can only sort articles by [relevancy, popularity, publishedAt]')

        # if parameters are blank
        if not query and not titleSearch and not sources and not domains:
            raise ValueError('You need at least one of the required parameters! [query, titleSearch, sources, domains]')

        articles = await self.getAPI('https://newsapi.org/v2/everything?', {**filter, 'pageSize':100}, {'X-Api-Key':self.apiKey}) # grabs all articles related to the query
        return articles

'''
#TESTING ASYNC FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(NewsAPI().getLanguages())
print(test)
'''