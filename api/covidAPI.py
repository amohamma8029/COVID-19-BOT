import asyncio
import matplotlib
import string
import matplotlib.dates as mdates
from api import APIHandler
from datetime import datetime
from matplotlib import pyplot as plt

#TODO: Add examples in parameters for methods
#TODO: Add database functions to this
#TODO: Add more explnatation to the code as single comments (ex. #this line does this)

class CovidAPI(APIHandler.APIHandler):
    """
    A class to format and handle specific requests to the COVID-19 API. Inherits from APIhandler class.

    ...

    Attributes
    ----------
    baseURL : str
        the base link in the form of a string that will be used to access the data

    payload : dict
        a dictionary of strings that lets you pass on specific arguments into the link (empty by default)

    Methods
    -------
    getCountries():
        returns a list of available countries in a dictionary format with the country code.
    """
    def __init__(self):
        """
        Parameters
        ----------
        baseURL : str
            the base link in the form of a string that will be used to access the data

        payload : dict
            a dictionary of strings that lets you pass on specific arguments into the link (empty by default)

        """
        super().__init__()

    async def getCountries(self):
        """Returns a list of available countries in a dictionary format with the country code

        Parameters
        ----------
        ...

        Returns
        -------
        list
            list of all available countries as dictionaries with the name and country code
        """
        api = await self.getAPI('https://corona-api.com/countries')
        data = api['data']
        countries = [{'name':data[i]['name'],'code':data[i]['code']} async for i in self.aiter(range(len(data)))]
        return countries

    async def getCountryCode(self, country):
        """Returns the country code of a specific country as a string

        Parameters
        ----------
        country : str
            the name of the country

        Returns
        -------
        str
            the country code of the given country a two character string
        """

        countryList = await self.getCountries()
        async for c in self.aiter(countryList):
            if c['name'] == country:
                return c['code']

    async def getCountryStats(self, country):
        """Returns the specific statistics of a country

        Parameters
        ----------
        country : str
            the name of the country

        Returns
        -------
        dict
            dictionaries containing all the data including coordinates, name, country code, latest statistics, and timeline
        """
        code = await self.getCountryCode(country)
        data = await self.getAPI(f'http://corona-api.com/countries/{code}')
        return  data['data']

    async def getCountryTimeline(self, country):
        """Returns the timeline of cases within a given country

        Parameters
        ----------
        country : str
            the name of the country, if 'global' is inputted instead of a country name it will grab the global timeline instead

        Returns
        -------
        list
            a list of dictionaries containing data for cases in previous dates
        """
        if country.lower() != 'global':
            stats = await self.getCountryStats(country)
            return stats['timeline']
        else:
            stats = await self.getAPI('https://corona-api.com/timeline')
            return stats['data']


    #TODO: add error handling for if the output is a NoneType
    async def queryDate(self, country, date):
        """Returns the statistics given a certain date

        Paramters
        ---------
        country : str
            the name of the country

        date : str
            the date to be queried (ex. August 29th 2020)

        Returns
        -------
        dict
            a dictionary containing all the statistics for that given date
        """
        targetDate = datetime.strptime(f'{date}', '%B %d %Y').date()
        timeline = await self.getCountryTimeline(country)

        async for day in self.aiter(timeline):
            if str(targetDate) in day['date']:
                return day

    async def getTimelineGraph(self, country, statistic, graphType = 'line'):
        """Generates a graph, displaying the timeline of a certain statistic overtime given a country and graph type

        Parameters
        ----------
        country : str
            name of the country, if 'global' is inputted instead of a country name it will grab the global timeline instead

        statistic : str
            the name of the statistic, can choose from deaths, confirmed, recovered, active, new_confirmed, new_recovered, new_deaths

        graphType : str
            type of graph, can choose from a line (default value), bar, and scatter plot
        """
        countryTimeline = await self.getCountryTimeline(country) # grabs timeline
        dates = [countryTimeline[i]['date'] async for i in self.aiter(range(len(countryTimeline)))] # grabs dates and puts it in an array
        stat = [countryTimeline[i][f'{statistic}'] async for i in self.aiter(range(len(countryTimeline)))] # grabs the statistics and puts it in an array

        dateTimes = mdates.num2date(mdates.datestr2num(dates)) # convert date strings to datetime objects
        fig, ax = plt.subplots() # create two subplots
        plt.ticklabel_format(style='plain') # too avoid weird values like 1e7

        # to handle the graph type
        if graphType.lower() == 'line':
            ax.plot(dateTimes, stat)
        elif graphType.lower() == 'bar':
            ax.bar(dateTimes, stat)
        elif graphType.lower() == 'scatter':
            ax.scatter(dateTimes, stat)

        # properly formats the title based on the statistic
        if statistic in ['new_confirmed', 'new_recovered', 'new_deaths']:
            formatStatistic = string.capwords(statistic.replace('_', ' '))
            if 'Deaths' in formatStatistic:
                plt.title(f'# of {formatStatistic} Over Time ({country.capitalize()})')
            else:
                plt.title(f'# of {formatStatistic} Cases Over Time ({country.capitalize()})')
        else:
            formatStatistic = statistic.capitalize()
            if 'Deaths' in formatStatistic:
                plt.title(f'# of {formatStatistic} Over Time ({country.capitalize()})')
            else:
                plt.title(f'# of {formatStatistic} Cases Over Time ({country.capitalize()})')

        plt.xlabel('Dates') # set label for x-axis
        plt.ylabel('Cases') # set label for y-axis
        fig.autofmt_xdate() # interprets the x-axis as dates and neatly formats it to avoid any messy overlapping

        plt.savefig('graph.png') #use os.remove('graph.png') in bot function
        plt.close() #closes the graph

#TESTING ASYNC FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(CovidAPI().getTimelineGraph('Canada', 'deaths'))
print(test)




