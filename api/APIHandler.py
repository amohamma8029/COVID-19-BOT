import aiohttp
import asyncio
from aiocache import cached

'''   
API LINKS:
https://corona-api.com/countries
https://newsapi.org/
'''

class APIHandler:
    '''
    The base class that handles basic requests to all the APIs.

    ...

    Attributes
    ----------
    baseURL : str
        the base link in the form of a string that will be used to access the data

    payload : dict
        a dictionary of strings that lets you pass on specific arguments into the link (empty by default)

    headers: dict
        a dictionary of strings that lets you pass on specific arguments into the HTTP header (empty by default)

    Methods
    -------
    getAPI()
        returns a json response from a get request and caches it to avoid hitting rate-limit and overusing the API.
    '''

    def __init__(self):
        pass

    @cached(ttl=3600) # cached all responses to avoid over-calling whatever API is used
    async def getAPI(self, baseURL, payload = {}, headers = {}):
        '''Returns a cached json response of the link (cached for 1hr)

        Parameters
        ----------
        ...

        Returns
        -------
        dict
            a json response in the form of a dictionary/list of dictionaries

        Raises
        ------
        ...
        '''

        async with aiohttp.ClientSession() as session:
            async with session.get(baseURL, params = payload, headers = headers) as r:
                if r.status == 200:
                    data = await r.json()
                    return data
                else:
                    return r.status






