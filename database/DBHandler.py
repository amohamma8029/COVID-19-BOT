import pymongo
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from utils.asyncOperations import *
from dotenv import load_dotenv
load_dotenv()

class DatabaseHandler:
    def __init__(self, defaultDB=''):
        self.password = os.getenv('DB_PASS') # environment variable is used for security purposes.
        self.cluster = AsyncIOMotorClient(f'mongodb+srv://admin:{self.password}@cluster0.6cb7x.mongodb.net/{defaultDB}?retryWrites=true&w=majority')

    async def find(self, database, collection, search = {}):
        db = self.cluster[database]
        results = [document async for document in db[collection].find(search)]
        return results

    async def find_one(self, database, collection, search = {}):
        db = self.cluster[database]
        results = [document async for document in db[collection].find_one(search)]
        return results

    async def delete_one(self, database, collection, criteria):
        db = self.cluster[database]
        await db[collection].delete_one(criteria)

    async def delete_many(self, database, collection, criteria):
        db = self.cluster[database]
        await db[collection].delete_many(criteria)

    async def insert_one(self, database, collection, post):
        db = self.cluster[database]
        await db[collection].insert_one(post)

    async def insert_many(self, database, collection, post):
        db = self.cluster[database]
        await db[collection].insert_many(post)

    async def update_one(self, database, collection, document, post, upsert = False):
        db = self.cluster[database]
        await db[collection].update_one(document, post, upsert)

    async def update_many(self, database, collection, document, post, upsert = False):
        db = self.cluster[database]
        await db[collection].update_many(document, post, upsert)

'''
#TESTING ASYNC FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(DatabaseHandler().find('NEWSAPI', 'sources'))
print(test)
'''