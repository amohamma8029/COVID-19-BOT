import aiohttp
import asyncio
from aiocache import cached

'''   
API LINKS:
https://corona-api.com/countries (about-corona) note: some endpoints are cached for up to an hour
https://newsapi.org/
'''

class APIHandler:
    """
    The base class that handles basic requests to all the APIs.

    ...

    Attributes
    ----------
    baseURL : str
        the base link in the form of a string that will be used to access the data

    payload : dict
        a dictionary of strings that lets you pass on specific arguments into the link (empty by default)

    Methods
    -------
    getAPI():
        returns a json response from a get request and caches it to avoid hitting rate-limit and overusing the API.
    """

    def __init__(self):
        pass

    # TODO: implement error handling.
    @cached(ttl=3600)
    async def getAPI(self, baseURL, payload = {}):
        """Returns a cached json response of the link (cached for 1hr)

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
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(baseURL, params = payload) as r:
                if r.status == 200:
                    data = await r.json()
                    return data

'''
#TESTING ASYNC FUNCTIONS EXAMPLE:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(APIhandler().getAPI('https://corona-api.com/countries'))
print(test)
'''





