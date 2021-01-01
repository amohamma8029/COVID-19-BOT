import pymongo
# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from utils.asyncOperations import *

#TODO: Remind yourself how MongoDB works again
#TODO: Check TNGBOT code to model your methods/functions and the class overall
#TODO: make sure to add environment variables
#TODO: add error handling in case database name is incorrect
#TODO: add .env variables to dbpassword

class DatabaseHandler:
    def __init__(self, password, defaultDB=''):
        self.cluster = AsyncIOMotorClient(f'mongodb+srv://admin:{password}@cluster0.6cb7x.mongodb.net/{defaultDB}?retryWrites=true&w=majority')

    async def find(self, database, collection, search = {}):
        db = self.cluster[database]
        results = [document async for document in db[collection].find(search)]
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

#TESTING ASYNC FUNCTIONS:

post1 = {"_id":"test", "name":"corona", "food":"chicken"}
post2 = {"_id":"rest", "name":"joe mama", "food":"bologna"}

loop = asyncio.get_event_loop()
test = loop.run_until_complete(DatabaseHandler('kemp1935').insert_many('NEWSAPI', 'articles', [post1, post2]))
print(test)
