import pymongo
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from utils.asyncOperations import *
from dotenv import load_dotenv
load_dotenv()

class DatabaseHandler:
    '''
    A class to handle operations for the database.

    ...

    Attributes
    ----------
    passsword : str
        the password that allows you to connect to the database

    cluster : AsyncIOMotorClient
        an instance of the AsyncIOMotorClient class which connects to the database using the password

    Methods
    -------
    find(self, database, collection, search = {})
        Updates the list of sources within the database.

    find_one(self, database, collection, search = {})
        Gets a list of all valid categories and returns it.

    delete_one(self, database, collection, criteria)
        Gets a list of all valid languages and returns it.

    delete_many(self, database, collection, criteria)
        Gets a list of all valid countries and returns it.

    async def insert_one(self, database, collection, post)
        Gets a list of all country names and returns it.

    insert_many(self, database, collection, post)
        Gets a list of all article sort methods and returns it.

    update_one(self, database, collection, document, post, upsert = False)
        Checks if a category is valid.

    update_many(self, database, collection, document, post, upsert = False)
        Checks if a country is valid.
    '''

    def __init__(self, defaultDB=''):
        '''
        Parameters
        ----------
        defaultDB : str
            the name of the database the AsyncIOMotorClient will connect to by default (empty by default)
        '''

        self.password = os.getenv('DB_PASS') # environment variable is used for security purposes.
        self.cluster = AsyncIOMotorClient(f'mongodb+srv://admin:{self.password}@cluster0.6cb7x.mongodb.net/{defaultDB}?retryWrites=true&w=majority')

    async def find(self, database, collection, search = {}):
        '''Gets all the items within a cursor from the database that matches a certain query.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        search : dict
            a dictionary containing what the database will search for {'language':'en'}

        Returns
        -------
        results : list
            a list containing all the items within the cursor
        '''

        db = self.cluster[database]
        results = [document async for document in db[collection].find(search)] # iterates through the cursor which contains all matched items
        return results

    async def find_one(self, database, collection, search = {}):
        '''Gets the first occurrence of an item from the database that matches a certain query.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        search : dict
            a dictionary containing what the database will search for {'language':'en'}

        Returns
        -------
        results : list
            a list containing the item
        '''

        db = self.cluster[database]
        results = [document async for document in db[collection].find_one(search)]
        return results

    async def delete_one(self, database, collection, criteria):
        '''Removes a single item from the database that matches a certain criteria.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        criteria: dict
            a dictionary containing what the database will look to delete {'_id':'CategoryList'}

        Returns
        -------
        ...
        '''

        db = self.cluster[database]
        await db[collection].delete_one(criteria)

    async def delete_many(self, database, collection, criteria):
        '''Removes all items from the database that matches a certain criteria.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        criteria: dict
            a dictionary containing what the database will look to delete {'language':'en'}

        Returns
        -------
        ...
        '''

        db = self.cluster[database]
        await db[collection].delete_many(criteria)

    async def insert_one(self, database, collection, post):
        '''Inserts an item into the database.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        post: dict
            a dictionary containing what the database will insert {'_id':'cbc-news', 'name':'CBC News'}

        Returns
        -------
        ...
        '''
        db = self.cluster[database]
        await db[collection].insert_one(post)

    async def insert_many(self, database, collection, post):
        '''Inserts multiple items into the database.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        post: list
            a list of dictionaries containing what the database will insert [{'_id':'cbc-news', 'name':'CBC News'}, {'_id':'abc-news', 'name':'ABC News'}]

        Returns
        -------
        ...
        '''
        db = self.cluster[database]
        await db[collection].insert_many(post)

    async def update_one(self, database, collection, document, post, upsert = False):
        '''Updates an item in the database.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        document : str
            a dictionary that identifies what document to update (ex. {'name':'Billy Bob Joe'} or {'_id':'cbc-news})

        post: dict
            a dictionary containing what the database will update {'$set':{'name':'Tony Pizzaro Bologna'}} (NOTE: Update operators like '$set' can be found on mongoDB's website)

        Returns
        -------
        ...
        '''
        db = self.cluster[database]
        await db[collection].update_one(document, post, upsert)

    async def update_many(self, database, collection, document, post, upsert = False):
        '''Updates multiple items in the database that match a criteria.

        Parameters
        ----------
        database : str
            name of the database (ex. NEWSAPI, YOUTUBE)

        collection : str
            name of the collection or 'sub-category' that will be accessed from the specified database (ex. miscellaneous, sources)

        document : str
            a dictionary that identifies what document to update (ex. {'_id':'5'})

        post: dict
            a dictionary containing what the database will update {'$inc':{'_id':7}} (NOTE: Update operators like '$inc' can be found on mongoDB's website)

        Returns
        -------
        ...
        '''
        db = self.cluster[database]
        await db[collection].update_many(document, post, upsert)

'''
#TESTING ASYNC FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(DatabaseHandler().find('NEWSAPI', 'sources'))
print(test)
'''