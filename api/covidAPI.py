import asyncio
import matplotlib
import string
import matplotlib.dates as mdates
from api import APIHandler
from utils.asyncOperations import *
from datetime import datetime
from matplotlib import pyplot as plt

class CovidAPI(APIHandler.APIHandler):
    '''
    A class to format and handle specific requests to the COVID-19 API. Inherits from the base APIhandler class.

    ...

    Attributes
    ----------
    baseURL : str
        the base link in the form of a string that will be used to access the data

    payload : dict
        a dictionary of strings that lets you pass on specific arguments into the link (empty by default)

    Methods
    -------
    getCountries()
        Returns a list of available countries in a dictionary format with the country code

    getCountryCode(country)
        Returns the country code of a specific country as a string

    getCountryStats(country)
        Returns the specific statistics of a country

    getCountryTimeline(country)
        Returns the timeline of cases within a given country

    queryDate(country, date)
        Returns the statistics given a certain date

    getDateGraph(country, date, graphType = 'bar')
        Generates a graph that displays the statistics of a certain date, given a country

    getTimelineGraph(country, statistic, graphType = 'line')
        Generates a graph that displays the timeline of a certain statistic overtime given a country and graph type
    '''

    def __init__(self):
        '''
        Parameters
        ----------
        ...
        '''

        super().__init__() # inherit from parent class

    async def getCountries(self):
        '''Returns a list of available countries in a dictionary format with the country code.

        Parameters
        ----------
        ...

        Returns
        -------
        list
            list of all available countries as dictionaries with the name and country code

        Raises
        ------
        ...
        '''

        api = await self.getAPI('https://corona-api.com/countries') # grabs api
        data = api['data'] # gets the data
        countries = [{'name':data[i]['name'],'code':data[i]['code']} async for i in aiter(range(len(data)))] # takes the name and country code of each country and puts it in a list
        return countries

    async def getCountryCode(self, country):
        '''Returns the country code of a specific country as a string.

        Parameters
        ----------
        country : str
            the name of the country (ex. Canada, USA, Japan)

        Returns
        -------
        str
            the country code of the given country a two character string

        Raises
        ------
        ...
        '''

        countryList = await self.getCountries() # gets the list of countries

        # checks if the country paramter matches with a valid country, if it does it returns the code. If not, it returns false
        async for c in aiter(countryList):
            if c['name'] == country:
                return c['code']
        else:
            return False

    async def getCountryStats(self, country):
        '''Returns the specific statistics of a country.

        Parameters
        ----------
        country : str
            the name of the country (ex. Canada, USA, Japan)

        Returns
        -------
        dict
            dictionaries containing all the data including coordinates, name, country code, latest statistics, and timeline

        Raises
        ------
        ...
        '''
        code = await self.getCountryCode(country) # gets the code of the country
        data = await self.getAPI(f'http://corona-api.com/countries/{code}') # gets the country's stats with the code
        return  data['data'] # data returned

    async def getCountryTimeline(self, country):
        '''Returns the timeline of cases within a given country.

        Parameters
        ----------
        country : str
            the name of the country, if 'global' is inputted instead of a country name it will grab the global timeline instead (ex. Canada, USA, Japan)

        Returns
        -------
        list
            a list of dictionaries containing data for cases in previous dates

        Raises
        ------
        ...
        '''

        # grabs the stats of the country, but if 'global' is input as the country name, it will grab the global timeline instead
        if country.lower() != 'global':
            stats = await self.getCountryStats(country)
            return stats['timeline']
        else:
            stats = await self.getAPI('https://corona-api.com/timeline')
            return stats['data']

    async def queryDate(self, country, date):
        '''Returns the statistics given a certain date.

        Paramters
        ---------
        country : str
            the name of the country (ex. Canada, USA, Japan)

        date : str
            the date to be queried (ex. August 29th 2020)

        Returns
        -------
        dict
            a dictionary containing all the statistics for that given date

        Raises
        ------
        ...
        '''

        targetDate = datetime.strptime(f'{date}', '%B %d %Y').date() # formats the date
        timeline = await self.getCountryTimeline(country) # grabs country timeline

        # checks if the date provided matches a date on the timeline, if not, it will return false
        async for day in aiter(timeline):
            if str(targetDate) in day['date']:
                return day
        else:
            return False

    async def getDateGraph(self, country, date, graphType = 'bar'):
        '''Generates a graph that displays the statistics of a certain date, given a country.

        Parameters
        ----------
        country : str
            name of the country, if 'global' is inputted instead of a country name it will grab the global timeline instead (ex. Canada, USA, Japan)

        date : str
            the date to be queried (ex. August 29th 2020)

        graphType : str
            type of graph, can choose from a bar graph (default) and pie chart

        Returns
        -------
        str/bool
            a string saying that a graph has been created, or returns false

        Raises
        ------
        ValueError
            if the graphType provided is incorrect.
        '''

        data = await self.queryDate(country, date) #grabs data for that date

        # if that date exists it will graph the data, if not, it will return false
        if data:
            stats = [data['deaths'], data['confirmed'], data['recovered'], data['new_confirmed'], data['new_recovered'], data['new_deaths'], data['active']] #puts the statistics in an array

            # handles graphType
            if graphType.lower() == 'bar':
                labels = ['deaths', 'confirmed', 'recovered', '(new) confirmed', '(new) recovered', '(new) deaths', 'active'] # sets the labels
                plt.bar(labels, stats) # creates bar graph
                plt.xticks(rotation=15) # gives the labels in the x-axis a 15 degree rotation to avoid overlapping
                plt.tick_params(axis='x', which='major', labelsize=7) # adjusts label size
                plt.ticklabel_format(style='plain', axis='y')
                plt.title(f'Statistics for {country} on {date}')
                plt.xlabel('Statistics')  # set label for x-axis
                plt.ylabel('Cases')  # set label for y-axis
            elif graphType.lower() == 'pie':
                labels = [f'deaths - {stats[0]}', f'confirmed - {stats[1]}', f'recovered - {stats[2]}',
                      f'(new) confirmed - {stats[3]}', f'(new) recovered - {stats[4]}', f'(new) deaths - {stats[5]}',
                      f'active - {stats[6]}'] # formats the labels for the legend
                pie = plt.pie(stats, startangle=90) # creates a pie chart
                plt.legend(pie[0], labels, bbox_to_anchor=(-0.5,0.5), title=f"Statistics for {country} on {date}", loc='center left') # formats the legend
                plt.axis('equal') # equal aspect ratio ensures that pie is drawn as a circle.
                plt.title(f'Statistics for {country} on {date}')
            else:
                raise ValueError('Invalid graph type. Can only make a bar graph or pie chart.') # raises an error if incorrect graphType is provided

            plt.savefig('dateGraph.png', bbox_inches='tight') # saves graph as a file
            plt.close() # closes the graph

            return f'new {graphType} graph created (as dateGraph.png)'
        else:
            return False

    async def getTimelineGraph(self, country, statistic, graphType = 'line'):
        '''Generates a graph that displays the timeline of a certain statistic overtime given a country and graph type.

        Parameters
        ----------
        country : str
            name of the country, if 'global' is inputted instead of a country name it will grab the global timeline instead (ex. Canada, USA, Japan)

        statistic : str
            the name of the statistic, can choose from deaths, confirmed, recovered, active, new_confirmed, new_recovered, new_deaths

        graphType : str
            type of graph, can choose from a line (default value), bar, and scatter plot

        Returns
        -------
        string/bool
            a string saying that a graph has been created, or returns false

        Raises
        ------
        ValueError
            if the graphType provided is incorrect.
        '''

        countryTimeline = await self.getCountryTimeline(country) # grabs timeline

        # if there is a response it will graph the timeline, if not, it will return false
        if countryTimeline:
            dates = [countryTimeline[i]['date'] async for i in aiter(range(len(countryTimeline)))] # grabs dates and puts it in an array
            stat = [countryTimeline[i][f'{statistic}'] async for i in aiter(range(len(countryTimeline)))] # grabs the statistics and puts it in an array

            dateTimes = mdates.num2date(mdates.datestr2num(dates)) # convert date strings to datetime objects
            fig, ax = plt.subplots() # create two subplots
            plt.ticklabel_format(style='plain') # to avoid weird values like 1e7

            # to handle the graph type
            if graphType.lower() == 'line':
                ax.plot(dateTimes, stat)
            elif graphType.lower() == 'bar':
                ax.bar(dateTimes, stat)
            elif graphType.lower() == 'scatter':
                ax.scatter(dateTimes, stat)
            else:
                raise ValueError('Invalid graph type.')

            # properly formats the title based on the statistic
            if statistic in ['new_confirmed', 'new_recovered', 'new_deaths']:
                formatStatistic = string.capwords(statistic.replace('_', ' '))
                if 'Deaths' in formatStatistic:
                    plt.title(f'# of {formatStatistic} Over Time ({country.capitalize()})')
                else:
                    plt.title(f'# of {formatStatistic} Cases Over Time ({country.capitalize()})')
            elif statistic in ['deaths', 'confirmed', 'recovered', 'active']:
                formatStatistic = statistic.capitalize()
                if 'Deaths' in formatStatistic:
                    plt.title(f'# of {formatStatistic} Over Time ({country.capitalize()})')
                else:
                    plt.title(f'# of {formatStatistic} Cases Over Time ({country.capitalize()})')
            else:
                raise ValueError('Invalid statistic.')

            plt.xlabel('Dates') # set label for x-axis
            plt.ylabel('Cases') # set label for y-axis
            fig.autofmt_xdate() # interprets the x-axis as dates and neatly formats it to avoid any messy overlapping

            plt.savefig('timelineGraph.png') # saves graph as file NOTE: use os.remove('timelineGraph.png') in bot function
            plt.close() # closes the graph

            return f'new {graphType} graph created (as timelineGraph.png)'
        else:
            return False

'''
#TESTING FUNCTIONS:

loop = asyncio.get_event_loop()
test = loop.run_until_complete(CovidAPI().getDateGraph('Japan', 'January 1 2021'))
print(test)
'''





