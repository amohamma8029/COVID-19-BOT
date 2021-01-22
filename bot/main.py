import discord
import os
from discord import Embed
from discord.ext import commands
from typing import Union
from api import covidAPI, newsAPI
from utils.asyncOperations import *
from dotenv import load_dotenv
load_dotenv()

# TODO: add documentation

client = commands.Bot(command_prefix='?')
client.remove_command('help') # default built-in discord help command is removed to make way for the custom help command
covidClient = covidAPI.CovidAPI()
newsAPIClient = newsAPI.NewsAPI()

# custom help menu
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title='Commands',
        description='Type ?help `<command>` for more info on a command (ex. ?help newsCountries).',
        color=discord.Colour.blue()
    )

    embed.add_field(
        name='__NEWS API__  :newspaper:',
        value='?newsSources\n?newsCountries\n?newsLanguages\n?newsCategories\n?newsSortList\n?newsSearch\n?newsHeadlines'
    )

    embed.add_field(
        name='__COVID-19 API__  :microbe:',
        value='?covidCountries\n?countryStats\n?getDateStats\n?getTimeline\n?dateGraph\n?timelineGraph'
    )

    embed.add_field(
        name='__OTHER__ :question:',
        value='?help *(shows this menu)*',
        inline=False
    )

    await ctx.send(embed=embed)

# not actual commands, these are called when help command is used (ex. ?help newsSources)
# NEWS API commands
@help.command()
async def newsSources(ctx):
    embed = discord.Embed(
        title='?newsSources',
        description='Lists all valid sources supported by the NEWS API.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?newsSources')

    await ctx.send(embed=embed)

@help.command()
async def newsCountries(ctx):
    embed = discord.Embed(
        title='?newsCountries',
        description='Lists all valid countries supported by the NEWS API.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?newsCountries')

    await ctx.send(embed=embed)

@help.command()
async def newsLanguages(ctx):
    embed = discord.Embed(
        title='?newsLanguages',
        description='Lists all valid languages supported by the NEWS API.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?newsLanguages')

    await ctx.send(embed=embed)

@help.command()
async def newsCategories(ctx):
    embed = discord.Embed(
        title='?newsCategories',
        description='Lists all valid categories supported by the NEWS API.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?newsCategories')

    await ctx.send(embed=embed)

@help.command()
async def newsSortList(ctx):
    embed = discord.Embed(
        title='?newsSortList',
        description='Lists all the possible ways articles can be sorted by the NEWS API.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?newsSortList')

    await ctx.send(embed=embed)

@help.command()
async def newsSearch(ctx):
    embed = discord.Embed(
        title='?newsSearch',
        description='Gets ALL articles related to a query.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?newsSearch')

    await ctx.send(embed=embed)

@help.command()
async def newsHeadlines(ctx):
    embed = discord.Embed(
        title='?newsHeadlines',
        description='Gets the recent and latest headlines related to a query.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?newsHeadlines')

    await ctx.send(embed=embed)

# COVID-19 API commands

@help.command()
async def covidCountries(ctx):
    embed = discord.Embed(
        title='?covidCountries',
        description='Lists all valid countries supported by the COVID-19 API.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?covidCountries')

    await ctx.send(embed=embed)

@help.command()
async def countryStats(ctx):
    embed = discord.Embed(
        title='?countryStats',
        description='Generates an embedded table containing all the data for a country.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?countryStats `<country>`')
    embed.add_field(name='Example', value='?countryStats `Canada`')

    await ctx.send(embed=embed)

@help.command()
async def getDateStats(ctx):
    embed = discord.Embed(
        title='?getDateStats',
        description='Generates an embedded table containing all the data for a country on a specific date.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?getDateStats `<country>` `<date>`')
    embed.add_field(name='Example', value='?getDateStats `United Kingdom` `August 29 2020`')

    await ctx.send(embed=embed)

@help.command()
async def getTimeline(ctx):
    embed = discord.Embed(
        title='?getTimeline',
        description='Generates an embedded table containing all the data for a country over time.',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?getTimeline `<country>`')
    embed.add_field(name='Example', value='?getTimeline `Japan`')

    await ctx.send(embed=embed)

@help.command()
async def dateGraph(ctx):
    embed = discord.Embed(
        title='?dateGraph',
        description='Generates a graph containing all the data for a country on a specific date (can choose from bar graph and pie chart).',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?dateGraph `<country>` `<date>` `<graphType (optional)>`')
    embed.add_field(name='Example 1', value='?dateGraph `Bangladesh` `February 3 2020`')
    embed.add_field(name='Example 2', value='?dateGraph `Bangladesh` `February 3 2020` `pie`')

    await ctx.send(embed=embed)

@help.command()
async def timelineGraph(ctx):
    embed = discord.Embed(
        title='?timelineGraph',
        description='Generates an graph (line [default], bar, and scatter) containing data for a statistic in a country over time (can choose from: deaths, confirmed, recovered, active, new_confirmed, new_recovered, new_deaths).',
        color=discord.Colour.blue()
    )

    embed.add_field(name='Syntax', value='?timelineGraph `<country>` `<statistic>` `<graphType (optional)>`')
    embed.add_field(name='Example 1', value='?dateGraph `Greece` `deaths`')
    embed.add_field(name='Example 2', value='?dateGraph `Greece` `deaths` `bar`')

    await ctx.send(embed=embed)

@client.event
async def on_ready():
    print('Bot is online!')

# general error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That seems to be an invalid command... *(use the ?help command to find a list of valid commands!)*")

# lists all available countries for COVID-19 API
@client.command()
async def covidCountries(ctx):
   countryList = await covidClient.getCountries()
   countryNames = [f"{country['name']} - :flag_{country['code'].lower()}:" async for country in aiter(countryList)] #takes country name and uses the contry code to format the country flag as an emoji
   countries = [countryNames[x:x + 20] async for x in aiter(range(0, len(countryNames), 20))] # creates 20 sublists of the countries to create 'pages'
   pages = len(countries)
   curPage = 1

   countryFormat = '\n'.join(countries[curPage-1])
   message = await ctx.send(f"**__LIST OF COUNTRIES__ (COVID-19 API) | Page [`{curPage}/{pages}`]**\n{countryFormat}")

   # adds reactions for the user to interact with
   await message.add_reaction("⬅")
   await message.add_reaction("➡")
   await message.add_reaction("❌")

   while True:
        # handles the interaction, makes sure the user who reacts is the correct one and reacts to the correct message as well
        reaction, user = await client.wait_for("reaction_add", check = lambda reaction, user : user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"] and reaction.message.id == message.id)
        # waiting for a reaction to be added

        if str(reaction.emoji) == "➡" and curPage != pages:
            curPage += 1
            countryFormat = '\n'.join(countries[curPage - 1])
            await message.edit(content=f"**__LIST OF COUNTRIES__ (COVID-19 API) | Page [`{curPage}/{pages}`]**\n{countryFormat}")
            await message.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "⬅" and curPage > 1:
            curPage -= 1
            countryFormat = '\n'.join(countries[curPage - 1])
            await message.edit(content=f"**__LIST OF COUNTRIES__ (COVID-19 API) | Page [`{curPage}/{pages}`]**\n{countryFormat}")
            await message.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "❌":
            await message.remove_reaction(reaction, user)
            await message.remove_reaction("⬅", client.user)
            await message.remove_reaction("➡", client.user)
            await message.remove_reaction("❌", client.user)
            break

        else:
            await message.remove_reaction(reaction, user)
            # removes reactions if the user tries to go forward on the last page or
            # backwards on the first page

@client.command()
async def countryStats(ctx, *args):
    if args:
        country = ' '.join(args)
        code = await covidClient.getCountryCode(country)
        if code:
            stats = await covidClient.getCountryStats(country)

            embed = discord.Embed(
                title=f'Country Statistics ({country})',
                description=f'Displaying all COVID-19 related statistics for {country}.',
                color=discord.Colour.blue()
            )

            population = stats['population']
            deaths_td = stats['today']['deaths']
            confirmed_td = stats['today']['confirmed']
            deathsTotal = stats['latest_data']['deaths']
            confirmedTotal = stats['latest_data']['confirmed']
            recoveredTotal = stats['latest_data']['recovered']
            critical = stats['latest_data']['critical']
            deathRate = stats['latest_data']['calculated']['death_rate']
            recoveryRate = stats['latest_data']['calculated']['recovery_rate']
            recover_vs_dead = stats['latest_data']['calculated']['recovered_vs_death_ratio']
            casesPerMillion = stats['latest_data']['calculated']['cases_per_million_population']

            formatStats = [population, deaths_td, confirmed_td, deathsTotal, confirmedTotal, recoveredTotal, critical, deathRate, recoveryRate, recover_vs_dead, casesPerMillion]

            async for i in aiter(range(len(formatStats))):
                if formatStats[i] is None:
                    formatStats[i] = 'N/A'

            async for i in aiter(range(7, 10)):
                if formatStats[i] != 'N/A':
                    formatStats[i] = '{:.2f}'.format(formatStats[i])

            embed.set_footer(text='data retrieved from: https://about-corona.net/')
            embed.set_thumbnail(url=f'https://www.countryflags.io/{code.lower()}/flat/64.png')
            embed.add_field(name='Country Name', value=country, inline=False)
            embed.add_field(name='Population', value=formatStats[0], inline=False)
            embed.add_field(name='Deaths (Today)', value=formatStats[1])
            embed.add_field(name='Confirmed Cases (Today)', value=formatStats[2])
            embed.add_field(name='Deaths (Total)', value=formatStats[3])
            embed.add_field(name='Confirmed Cases (Total)', value=formatStats[4])
            embed.add_field(name='Recovered (Total)', value=formatStats[5])
            embed.add_field(name='Critical Condition (Total)', value=formatStats[6])
            embed.add_field(name='Death Rate (%)', value=formatStats[7], inline=False)
            embed.add_field(name='Recovery Rate (%)', value=formatStats[8], inline=False)
            embed.add_field(name='Recovered/Death Ratio (%)', value=formatStats[9], inline=False)
            embed.add_field(name='Cases (Per Million)', value=formatStats[10], inline=False)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f'Statistics on {country}',
                description='No data could be provided...',
                color=discord.Colour.blue()
            )

            embed.add_field(name='No Data', value='No data could be provided with this query, sorry!', inline=False)

            await ctx.send(embed=embed)
    else:
        await ctx.send("Please pass in the required arguments.")

@client.command()
async def getTimeline(ctx, *args):
    if args:
        country = ' '.join(args)
        timeline = await covidClient.getCountryTimeline(country)
        pages = len(timeline)
        curPage = 1

        timelineDay = timeline[curPage-1]
        date = timelineDay['date']
        deaths = timelineDay['deaths']
        confirmed = timelineDay['confirmed']
        active = timelineDay['active']
        recovered = timelineDay['recovered']
        newConfirmed = timelineDay['new_confirmed']
        newRecovered = timelineDay['new_recovered']
        newDeaths = timelineDay['new_deaths']

        embed = discord.Embed(
            title='Statistics Timeline',
            description=f'Displaying all COVID-19 related statistics for {country} during {date}',
            color=discord.Colour.blue()
        )

        embed.set_footer(text='data retrieved from: https://about-corona.net/')

        if country.lower() != 'global':
            code = await covidClient.getCountryCode(country)
            embed.set_thumbnail(url=f'https://www.countryflags.io/{code.lower()}/flat/64.png')

        embed.add_field(name='Country Name', value=country, inline=False)
        embed.add_field(name='Deaths (Total)', value=deaths, inline=False)
        embed.add_field(name='Confirmed (Total)', value=confirmed)
        embed.add_field(name='Active', value=active)
        embed.add_field(name='Recovered (Total)', value=recovered)
        embed.add_field(name='Confirmed (New)', value=newConfirmed)
        embed.add_field(name='Recovered (New)', value=newRecovered)
        embed.add_field(name='Deaths (New)', value=newDeaths)

        message = await ctx.send(embed=embed)

        await message.add_reaction("⬅")
        await message.add_reaction("➡")
        await message.add_reaction("❌")

        while True:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user : user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"] and reaction.message.id == message.id)
            # waiting for a reaction to be added

            if str(reaction.emoji) == "➡" and curPage != pages:
                curPage += 1

                timelineDay = timeline[curPage - 1]
                date = timelineDay['date']
                deaths = timelineDay['deaths']
                confirmed = timelineDay['confirmed']
                active = timelineDay['active']
                recovered = timelineDay['recovered']
                newConfirmed = timelineDay['new_confirmed']
                newRecovered = timelineDay['new_recovered']
                newDeaths = timelineDay['new_deaths']

                embed = discord.Embed(
                    title='Statistics Timeline',
                    description=f'Displaying all COVID-19 related statistics for {country} during {date}',
                    color=discord.Colour.blue()
                )

                embed.set_footer(text='data retrieved from: https://about-corona.net/')

                if country.lower() != 'global':
                    code = await covidClient.getCountryCode(country)
                    embed.set_thumbnail(url=f'https://www.countryflags.io/{code.lower()}/flat/64.png')

                embed.add_field(name='Country Name', value=country, inline=False)
                embed.add_field(name='Deaths (Total)', value=deaths, inline=False)
                embed.add_field(name='Confirmed (Total)', value=confirmed)
                embed.add_field(name='Active', value=active)
                embed.add_field(name='Recovered (Total)', value=recovered)
                embed.add_field(name='Confirmed (New)', value=newConfirmed)
                embed.add_field(name='Recovered (New)', value=newRecovered)
                embed.add_field(name='Deaths (New)', value=newDeaths)

                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "⬅" and curPage > 1:
                curPage -= 1

                timelineDay = timeline[curPage - 1]
                date = timelineDay['date']
                deaths = timelineDay['deaths']
                confirmed = timelineDay['confirmed']
                active = timelineDay['active']
                recovered = timelineDay['recovered']
                newConfirmed = timelineDay['new_confirmed']
                newRecovered = timelineDay['new_recovered']
                newDeaths = timelineDay['new_deaths']

                embed = discord.Embed(
                    title='Statistics Timeline',
                    description=f'Displaying all COVID-19 related statistics for {country} during {date}',
                    color=discord.Colour.blue()
                )

                embed.set_footer(text='data retrieved from: https://about-corona.net/')

                if country.lower() != 'global':
                    code = await covidClient.getCountryCode(country)
                    embed.set_thumbnail(url=f'https://www.countryflags.io/{code.lower()}/flat/64.png')

                embed.add_field(name='Country Name', value=country, inline=False)
                embed.add_field(name='Deaths (Total)', value=deaths, inline=False)
                embed.add_field(name='Confirmed (Total)', value=confirmed)
                embed.add_field(name='Active', value=active)
                embed.add_field(name='Recovered (Total)', value=recovered)
                embed.add_field(name='Confirmed (New)', value=newConfirmed)
                embed.add_field(name='Recovered (New)', value=newRecovered)
                embed.add_field(name='Deaths (New)', value=newDeaths)

                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "❌":
                await message.remove_reaction(reaction, user)
                await message.remove_reaction("⬅", client.user)
                await message.remove_reaction("➡", client.user)
                await message.remove_reaction("❌", client.user)
                break

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
    else:
        await ctx.send("Please pass in the required arguments.")

@client.command()
async def getDateStats(ctx, *args):
    if args:
        countryList = await covidClient.getCountries()
        countries = [country['name'] async for country in aiter(countryList)]

        data = ' '.join(args)

        async for country in aiter(countries):
            if country in data:
                queryCountry = country
                break

        queryDate = data.replace(f'{queryCountry} ', '')

        dateStats = await covidClient.queryDate(queryCountry, queryDate)

        if dateStats:
            date = dateStats['date']
            deaths = dateStats['deaths']
            confirmed = dateStats['confirmed']
            active = dateStats['active']
            recovered = dateStats['recovered']
            newConfirmed = dateStats['new_confirmed']
            newRecovered = dateStats['new_recovered']
            newDeaths = dateStats['new_deaths']

            embed = discord.Embed(
                title=f'Statistics on {queryDate}',
                description=f'Displaying all COVID-19 related statistics for {country} on {queryDate}',
                color=discord.Colour.blue()
            )

            embed.set_footer(text='data retrieved from: https://about-corona.net/')

            if country.lower() != 'global':
                code = await covidClient.getCountryCode(country)
                embed.set_thumbnail(url=f'https://www.countryflags.io/{code.lower()}/flat/64.png')

            embed.add_field(name='Country Name', value=country, inline=False)
            embed.add_field(name='Deaths (Total)', value=deaths, inline=False)
            embed.add_field(name='Confirmed (Total)', value=confirmed)
            embed.add_field(name='Active', value=active)
            embed.add_field(name='Recovered (Total)', value=recovered)
            embed.add_field(name='Confirmed (New)', value=newConfirmed)
            embed.add_field(name='Recovered (New)', value=newRecovered)
            embed.add_field(name='Deaths (New)', value=newDeaths)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f'Statistics on {queryDate}',
                description='No data could be provided...',
                color=discord.Colour.blue()
            )

            embed.add_field(name='No Data', value='No data could be provided with this query, sorry!', inline=False)

            await ctx.send(embed=embed)
    else:
        await ctx.send("Please pass in the required arguments.")

@client.command()
async def dateGraph(ctx, *args):
    if args:
        countryList = await covidClient.getCountries()
        countries = [country['name'] async for country in aiter(countryList)]
        graphTypes = ['bar', 'pie']
        data = ' '.join(args)

        async for country in aiter(countries):
            if country in data:
                queryCountry = country
                break
        else:
            raise ValueError('Invalid Country Name')

        newData = data.replace(f'{queryCountry} ', '')

        async for graphType in aiter(graphTypes):
            if graphType in newData:
                queryGraph = graphType
                queryDate = newData.replace(f' {queryGraph}', '')
                graph = await covidClient.getDateGraph(queryCountry, queryDate, queryGraph)
                break
        else:
            if len(newData.split(' ')) > 3:
                raise ValueError('Invalid graph type')
            else:
                queryDate = newData
                graph = await covidClient.getDateGraph(queryCountry, queryDate)

        if graph:
            image = discord.File("dateGraph.png")
            await ctx.send(file=image)
            os.remove("dateGraph.png")
        else:
            embed = discord.Embed(
                title=f'Graph for {queryCountry} on {queryDate}',
                description='No data could be provided...',
                color=discord.Colour.blue()
            )

            embed.add_field(name='No Data', value='No data could be provided with this query, sorry!', inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Please pass in the required arguments.")

@client.command()
async def timelineGraph(ctx, *args):
    if args:
        countryList = await covidClient.getCountries()
        countries = [country['name'] async for country in aiter(countryList)]
        graphTypes = ['line', 'bar', 'scatter']

        data = ' '.join(args)

        async for country in aiter(countries):
            if country in data:
                queryCountry = country
                break
        else:
            raise ValueError('Invalid Country Name')

        newData = data.replace(f'{queryCountry} ', '')

        async for graphType in aiter(graphTypes):
            if graphType in newData:
                queryGraph = graphType
                queryStat = newData.replace(f' {queryGraph}', '')
                graph = await covidClient.getTimelineGraph(queryCountry, queryStat, queryGraph)
                break
        else:
            if len(newData.split(' ')) > 2:
                raise ValueError('Invalid graph type')
            else:
                queryStats = newData
                graph = await covidClient.getTimelineGraph(queryCountry, queryStats)

        if graph:
            image = discord.File("timelineGraph.png")
            await ctx.send(file=image)
            os.remove("timelineGraph.png")
        else:
            embed = discord.Embed(
                title=f'Graph For Data Over Time in {queryCountry}',
                description='No data could be provided...',
                color=discord.Colour.blue()
            )

            embed.add_field(name='No Data', value='No data could be provided with this query, sorry!', inline=False)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Please pass in the required arguments.")

@client.command()
async def newsSources(ctx):
    categoryResponse = 'None'
    languageResponse = 'None'
    countryResponse = 'None'
    nameResponse = 'None'

    menu = discord.Embed(
        title='**__Sources Search__**',
        description='Press the emojis to specify the parameters of your search, then press :mag_right: to search *(NOTE: if you wanna ALL sources, just press :mag_right: without setting any parameters)*',
        color=discord.Colour.blue()
    )

    menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
    menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
    menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
    menu.add_field(name='**:writing_hand: Name**', value=nameResponse, inline=False)

    message = await ctx.send(embed=menu)

    await message.add_reaction("📁")
    await message.add_reaction("🗣️")
    await message.add_reaction("🌎")
    await message.add_reaction("✍️")
    await message.add_reaction("🔎")

    while True:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user : user == ctx.author and str(reaction.emoji) in ["📁","🗣️","🌎","✍️","🔎"] and reaction.message.id == message.id)

        if str(reaction.emoji) == "📁":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **category** you'd like to sort sources by.")
            userInput = await client.wait_for("message", check=lambda message : message.author == ctx.author)
            categoryCheck = await newsAPIClient.queryCategory(userInput.content)

            if categoryCheck:
                categoryResponse = userInput.content

                menu = discord.Embed(
                    title='**__Sources Search__**',
                    description='Press the emojis to specify the parameters of your search, then press :mag_right: to search *(NOTE: if you wanna ALL sources, just press :mag_right: without setting any parameters)*',
                    color=discord.Colour.blue()
                )

                menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
                menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
                menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
                menu.add_field(name='**:writing_hand: Name**', value=nameResponse, inline=False)

                await message.edit(embed=menu)

                response = await ctx.send("Alrighty, I've set the specified **category** to the search parameters!")
                await asyncio.sleep(2)
                await response.delete()
            else:
                response = await ctx.send("Invalid category, try again. *(use ?newsCategories to see a list of supported categories)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "🗣️":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **language** you'd like me to search articles in")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            languageCheck = await newsAPIClient.getLanguageCode(userInput.content)

            if languageCheck:
                languageResponse = userInput.content
                menu = discord.Embed(
                    title='**__Sources Search__**',
                    description='Press the emojis to specify the parameters of your search, then press :mag_right: to search *(NOTE: if you wanna ALL sources, just press :mag_right: without setting any parameters)*',
                    color=discord.Colour.blue()
                )

                menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
                menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
                menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
                menu.add_field(name='**:writing_hand: Name**', value=nameResponse, inline=False)

                await message.edit(embed=menu)

                response = await ctx.send("Alrighty, I've set the specified **language** to the search parameters!")
                await asyncio.sleep(2)
                await response.delete()

            else:
                response = await ctx.send("Invalid language, please try again. *(use ?newsLanguages to see a list of supported languages)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "🌎":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **country** you'd like to search sources in.")
            userInput = await client.wait_for("message", check=lambda message : message.author == ctx.author)
            countryCheck = await newsAPIClient.queryCountry(userInput.content)

            if countryCheck:
                countryResponse = userInput.content

                menu = discord.Embed(
                    title='**__Sources Search__**',
                    description='Press the emojis to specify the parameters of your search, then press :mag_right: to search *(NOTE: if you wanna ALL sources, just press :mag_right: without setting any parameters)*',
                    color=discord.Colour.blue()
                )

                menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
                menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
                menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
                menu.add_field(name='**:writing_hand: Name**', value=nameResponse, inline=False)

                await message.edit(embed=menu)

                response = await ctx.send("Alrighty, I've set the specified **country** to the search parameters!")
                await asyncio.sleep(2)
                await response.delete()
            else:
                response = await ctx.send("Invalid country, try again. *(use ?newsCountries to see a list of supported countries)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "✍️":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me a specific **name** you'd like to search for in the list of sources.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            queryResponse = userInput.content
            menu = discord.Embed(
                title='**__Sources Search__**',
                description='Press the emojis to specify the parameters of your search, then press :mag_right: to search *(NOTE: if you wanna ALL sources, just press :mag_right: without setting any parameters)*',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
            menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
            menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
            menu.add_field(name='**:writing_hand: Name**', value=nameResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I've set the specified **query** to the search parameters!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "🔎":
            await message.remove_reaction(reaction, user)
            await message.delete()
            message = await ctx.send("Searching...")
            await asyncio.sleep(2)
            await message.delete()

            if categoryResponse == 'None':
                categoryResponse = ''
            if languageResponse == 'None':
                languageResponse = ''
            if countryResponse == 'None':
                countryResponse = ''
            if nameResponse == 'None':
                nameResponse = ''

            sourcesList = await newsAPIClient.getSources(categoryResponse, languageResponse, countryResponse, nameResponse)

            if sourcesList:
                sourceData = [f"```name: {source['name']}\ncountry: {source['country']}\ncategory: {source['category']}\nlanguage: {source['language']}\nurl: {source['url']}\ndescription: {source['description']}```" async for source in aiter(sourcesList)]
            else:
                embed = discord.Embed(
                    title=f'News Sources',
                    description='No sources could be provided...',
                    color=discord.Colour.blue()
                )

                embed.add_field(name='No Data', value='No available news sources could be provided with this query, sorry!', inline=False)
                await ctx.send(embed=embed)

            sources = [sourceData[x:x + 5] async for x in aiter(range(0, len(sourceData), 5))]
            result = [''.join(page) async for page in aiter(sources)]

            pages = len(sources)
            curPage = 1

            message = await ctx.send(f"**__LIST OF KNOWN NEWS SOURCES__ [Page `{curPage}/{pages}`]**\n{result[curPage-1]}")

            await message.add_reaction("⬅")
            await message.add_reaction("➡")
            await message.add_reaction("❌")

            while True:
                reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user : user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"] and reaction.message.id == message.id)
                # waiting for a reaction to be added

                if str(reaction.emoji) == "➡" and curPage != pages:
                    curPage += 1
                    await message.edit(content=f"**__LIST OF KNOWN NEWS SOURCES__ [Page `{curPage}/{pages}`]**\n{result[curPage-1]}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⬅" and curPage > 1:
                    curPage -= 1
                    await message.edit(content=f"**__LIST OF KNOWN NEWS SOURCES__ [Page `{curPage}/{pages}`]**\n{result[curPage-1]}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "❌":
                    await message.remove_reaction(reaction, user)
                    await message.remove_reaction("⬅", client.user)
                    await message.remove_reaction("➡", client.user)
                    await message.remove_reaction("❌", client.user)
                    break

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page

@client.command()
async def newsHeadlines(ctx):
    countryResponse = 'None'
    categoryResponse = 'None'
    sourcesResponse = ['None']
    queryResponse = 'None'

    menu = discord.Embed(
        title='**__News Headlines Search__**',
        description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
        color=discord.Colour.blue()
    )

    menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
    menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
    menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
    menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)

    message = await ctx.send(embed=menu)

    await message.add_reaction("🌎")
    await message.add_reaction("📁")
    await message.add_reaction("📰")
    await message.add_reaction("❓")
    await message.add_reaction("🔎")

    while True:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user : user == ctx.author and str(reaction.emoji) in ["🌎","📁","📰","❓","🔎"] and reaction.message.id == message.id)

        if str(reaction.emoji) == "🌎":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **country** you'd like to search articles in.")
            userInput = await client.wait_for("message", check=lambda message : message.author == ctx.author)
            countryCheck = await newsAPIClient.queryCountry(userInput.content)

            if countryCheck:
                countryResponse = userInput.content
                menu = discord.Embed(
                    title='**__News Headlines Search__**',
                    description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                    color=discord.Colour.blue()
                )

                menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
                menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
                menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
                menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)

                await message.edit(embed=menu)

                response = await ctx.send("Alrighty, I've set the specified **country** to the search parameters!")
                await asyncio.sleep(2)
                await response.delete()
            else:
                response = await ctx.send("Invalid country, try again. *(use ?newsCountries to see a list of supported countries)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "📁":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **category** you'd like to sort articles by.")
            userInput = await client.wait_for("message", check=lambda message : message.author == ctx.author)
            categoryCheck = await newsAPIClient.queryCategory(userInput.content)

            if categoryCheck:
                categoryResponse = userInput.content
                menu = discord.Embed(
                    title='**__News Headlines Search__**',
                    description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                    color=discord.Colour.blue()
                )

                menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
                menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
                menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
                menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)

                await message.edit(embed=menu)

                response = await ctx.send("Alrighty, I've set the specified **category** to the search parameters!")
                await asyncio.sleep(2)
                await response.delete()
            else:
                response = await ctx.send("Invalid category, try again. *(use ?newsCategories to see a list of supported categories)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "📰":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **source** you'd like to find articles by.")
            userInput = await client.wait_for("message", check=lambda message : message.author == ctx.author)
            sourceCheck = await newsAPIClient.querySource(userInput.content)

            if sourceCheck:
                if "None" in sourcesResponse:
                    sourcesResponse.remove("None")
                elif len(sourcesResponse) > 20:
                    await ctx.send("You have exceeded the maximum number of sources for a single query! You cannot add anymore.")
                else:
                    sourcesResponse.append(userInput.content)
                    menu = discord.Embed(
                        title='**__News Headlines Search__**',
                        description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                        color=discord.Colour.blue()
                    )

                    menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
                    menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
                    menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
                    menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)

                    await message.edit(embed=menu)

                    response = await ctx.send("Alrighty, I've set the specified **source** to the search parameters!")
                    await asyncio.sleep(2)
                    await response.delete()
            else:
                response = await ctx.send("Invalid source, try again. *(use ?newsSources to see a list of supported sources)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "❓":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me a specific **phrase or any key-words** you'd like to search for in articles.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            queryResponse = userInput.content
            menu = discord.Embed(
                title='**__News Headlines Search__**',
                description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:earth_americas: Country**', value=countryResponse, inline=False)
            menu.add_field(name='**:file_folder: Category**', value=categoryResponse, inline=False)
            menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
            menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I've set the specified **query** to the search parameters!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "🔎":
            await message.remove_reaction(reaction, user)
            await message.delete()
            message = await ctx.send("Searching...")
            await asyncio.sleep(2)

            if countryResponse == 'None':
                countryResponse = ''
            if categoryResponse == 'None':
                categoryResponse = ''
            if sourcesResponse == ['None']:
                sourcesResponse = ''
            if queryResponse == 'None':
                queryResponse = ''

            headlines = await newsAPIClient.getTopHeadlines(countryResponse, categoryResponse, ','.join(sourcesResponse), queryResponse)

            if headlines in [400, 401, 429, 500]:
                await ctx.send("Whoops, looks like something went wrong. Please try again at a later time!")
            else:
                articles = headlines['articles']
                pages = len(articles)
                curPage = 1

                if articles:
                    article = articles[curPage - 1]
                    title = article['title']
                    source = article['source']['name']
                    publishedAt = article['publishedAt']
                    description = article['description']
                    url = article['url']
                    image = article['urlToImage']

                    embed = discord.Embed(
                        title=f'{title}',
                        description=f'{description}".',
                        color=discord.Colour.blue()
                    )

                    embed.set_footer(text='data retrieved from: https://newsapi.org/')

                    if image:
                        embed.set_image(url=image)

                    embed.add_field(name='Source', value=source, inline=False)
                    embed.add_field(name='Publish Date', value=publishedAt, inline=False)
                    embed.add_field(name='URL', value=url, inline=False)

                    await message.edit(embed=embed, content=f'**Page [``{curPage}/{pages}``]**')

                    await message.add_reaction("⬅")
                    await message.add_reaction("➡")
                    await message.add_reaction("❌")

                    while True:
                        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"] and reaction.message.id == message.id) # waiting for a reaction to be added

                        if str(reaction.emoji) == "➡" and curPage != pages:
                            curPage += 1

                            article = articles[curPage - 1]
                            title = article['title']
                            source = article['source']['name']
                            publishedAt = article['publishedAt']
                            description = article['description']
                            url = article['url']
                            image = article['urlToImage']

                            embed = discord.Embed(
                                title=f'{title}',
                                description=f'{description}".',
                                color=discord.Colour.blue()
                            )

                            embed.set_footer(text='data retrieved from: https://newsapi.org/')

                            if image:
                                embed.set_image(url=image)

                            embed.add_field(name='Source', value=source, inline=False)
                            embed.add_field(name='Publish Date', value=publishedAt, inline=False)
                            embed.add_field(name='URL', value=url, inline=False)

                            await message.edit(embed=embed, content=f'**Page [``{curPage}/{pages}``]**')
                            await message.remove_reaction(reaction, user)

                        elif str(reaction.emoji) == "⬅" and curPage > 1:
                            curPage -= 1

                            article = articles[curPage - 1]
                            title = article['title']
                            source = article['source']['name']
                            publishedAt = article['publishedAt']
                            description = article['description']
                            url = article['url']
                            image = article['urlToImage']

                            embed = discord.Embed(
                                title=f'{title}',
                                description=f'{description}".',
                                color=discord.Colour.blue()
                            )

                            embed.set_footer(text='data retrieved from: https://newsapi.org/')
                            embed.set_image(url=image)

                            embed.add_field(name='Source', value=source, inline=False)
                            embed.add_field(name='Publish Date', value=publishedAt, inline=False)
                            embed.add_field(name='URL', value=url, inline=False)

                            await message.edit(embed=embed, content=f'**Page [``{curPage}/{pages}``]**')
                            await message.remove_reaction(reaction, user)

                        elif str(reaction.emoji) == "❌":
                            await message.remove_reaction(reaction, user)
                            await message.remove_reaction("⬅", client.user)
                            await message.remove_reaction("➡", client.user)
                            await message.remove_reaction("❌", client.user)
                            break

                        else:
                            await message.remove_reaction(reaction, user)
                            # removes reactions if the user tries to go forward on the last page or
                            # backwards on the first page
                else:
                    embed = discord.Embed(
                        title=f'News Sources',
                        description='No sources could be provided...',
                        color=discord.Colour.blue()
                    )

                    embed.add_field(name='No Data', value='No articles could be provided with this query, sorry!', inline=False)

                    await ctx.send(embed=embed)

@client.command()
async def newsSearch(ctx):
    queryResponse = 'None'
    titleResponse = 'None'
    sourcesResponse = ['None']
    domainsResponse = ['None']
    exDomainsResponse = ['None']
    fromDateResponse = 'None'
    toDateResponse = 'None'
    languageResponse = 'None'
    sortByResponse = 'None'

    menu = discord.Embed(
        title='**__News Search (Everything)__**',
        description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
        color=discord.Colour.blue()
    )

    menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
    menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
    menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
    menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
    menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
    menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
    menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
    menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
    menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

    message = await ctx.send(embed=menu)

    await message.add_reaction("❓")
    await message.add_reaction("📌")
    await message.add_reaction("📰")
    await message.add_reaction("🌐")
    await message.add_reaction("🚫")
    await message.add_reaction("⏪")
    await message.add_reaction("⏩")
    await message.add_reaction("🗣️")
    await message.add_reaction("🗂️")
    await message.add_reaction("🔎")

    while True:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user : user == ctx.author and str(reaction.emoji) in ["❓","📌","📰","🌐","🚫","⏪","⏩","🗣️","🗂️","🔎"] and reaction.message.id == message.id)

        if str(reaction.emoji) == "❓":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me a specific **phrase or any key-words** you'd like to search for in articles.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            queryResponse = userInput.content
            menu = discord.Embed(
                title='**__News Search (Everything)__**',
                description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
            menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
            menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
            menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
            menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
            menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
            menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
            menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
            menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I've set the specified **query** to the search parameters!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "📌":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me a specific **phrase or any key-words** you'd like to search for within article **titles**.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            titleResponse = userInput.content
            menu = discord.Embed(
                title='**__News Search (Everything)__**',
                description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
            menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
            menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
            menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
            menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
            menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
            menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
            menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
            menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I've set the specified **query** to the search parameters!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "📰":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **source** you'd like to find articles by.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            sourceCheck = await newsAPIClient.querySource(userInput.content)

            if sourceCheck:
                if "None" in sourcesResponse:
                    sourcesResponse.remove("None")
                elif len(sourcesResponse) > 20:
                    await ctx.send("You have exceeded the maximum number of sources for a single query! You cannot add anymore.")
                else:
                    sourcesResponse.append(userInput.content)
                    menu = discord.Embed(
                        title='**__News Search (Everything)__**',
                        description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                        color=discord.Colour.blue()
                    )

                    menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
                    menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
                    menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
                    menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
                    menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
                    menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
                    menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
                    menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
                    menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

                    await message.edit(embed=menu)

                    response = await ctx.send("Alrighty, I've set the specified **source** to the search parameters!")
                    await asyncio.sleep(2)
                    await response.delete()
            else:
                response = await ctx.send("Invalid source, try again. *(use ?newsSources to see a list of supported sources)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "🌐":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **domains** you'd like me to include articles from.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            if "None" in domainsResponse:
                domainsResponse.remove("None")

            domainsResponse.append(userInput.content)

            menu = discord.Embed(
                title='**__News Search (Everything)__**',
                description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
            menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
            menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
            menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
            menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
            menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
            menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
            menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
            menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I've set the specified **domain** to the search parameters!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "🚫":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **domains** you'd like me to **NOT** include articles from.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            if "None" in exDomainsResponse:
                exDomainsResponse.remove("None")

            exDomainsResponse.append(userInput.content)

            menu = discord.Embed(
                title='**__News Search (Everything)__**',
                description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
            menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
            menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
            menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
            menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
            menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
            menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
            menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
            menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I will **not** include the specified **domain** when searching for articles!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "⏪":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me the **oldest** date you want me to search articles from.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            fromDateResponse = userInput.content

            menu = discord.Embed(
                title='**__News Search (Everything)__**',
                description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
            menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
            menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
            menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
            menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
            menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
            menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
            menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
            menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I've set the specified **date** to the search parameters!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "⏩":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me the **newest** date you want me to search articles from.")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)

            toDateResponse = userInput.content

            menu = discord.Embed(
                title='**__News Search (Everything)__**',
                description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                color=discord.Colour.blue()
            )

            menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
            menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
            menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
            menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
            menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
            menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
            menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
            menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
            menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

            await message.edit(embed=menu)

            response = await ctx.send("Alrighty, I've set the specified **date** to the search parameters!")
            await asyncio.sleep(2)
            await response.delete()

        elif str(reaction.emoji) == "🗣️":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me what **language** you'd like me to search articles in")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            languageCheck = await newsAPIClient.getLanguageCode(userInput.content)

            if languageCheck:
                languageResponse = userInput.content

                menu = discord.Embed(
                    title='**__News Search (Everything)__**',
                    description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                    color=discord.Colour.blue()
                )

                menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
                menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
                menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
                menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
                menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
                menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
                menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
                menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
                menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

                await message.edit(embed=menu)

                response = await ctx.send("Alrighty, I've set the specified **language** to the search parameters!")
                await asyncio.sleep(2)
                await response.delete()
            else:
                response = await ctx.send("Invalid language, please try again. *(use ?newsLanguages to see a list of supported languages)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "🗂️":
            await message.remove_reaction(reaction, user)
            await ctx.send("Please tell me you'd like me to **sort** any found articles")
            userInput = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            sortByList = await newsAPIClient.getSortBy()

            if userInput.content in sortByList:
                sortByResponse = userInput.content

                menu = discord.Embed(
                    title='**__News Search (Everything)__**',
                    description='Press the emojis to specify the parameters of your search (press :mag_right: to search)',
                    color=discord.Colour.blue()
                )

                menu.add_field(name='**:question: Query**', value=queryResponse, inline=False)
                menu.add_field(name='**:pushpin: Title Search**', value=titleResponse, inline=False)
                menu.add_field(name='**:newspaper: Sources**', value='\n'.join(sourcesResponse), inline=False)
                menu.add_field(name='**:globe_with_meridians: Domains**', value='\n'.join(domainsResponse), inline=False)
                menu.add_field(name='**:no_entry_sign: Exclude Domains**', value='\n'.join(exDomainsResponse), inline=False)
                menu.add_field(name='**:rewind: From (date)**', value=fromDateResponse, inline=False)
                menu.add_field(name='**:fast_forward: To (date)**', value=toDateResponse, inline=False)
                menu.add_field(name='**:speaking_head: Language**', value=languageResponse, inline=False)
                menu.add_field(name='**:dividers: Sort By**', value=sortByResponse, inline=False)

                await message.edit(embed=menu)

                response = await ctx.send(f"Alrighty, I will **sort** articles by {sortByResponse}!")
                await asyncio.sleep(2)
                await response.delete()
            else:
                response = await ctx.send("Invalid method of **sorting**, please try again. *(use ?newsSortList to see how I can sort articles)*")
                await asyncio.sleep(2)
                await response.delete()

        elif str(reaction.emoji) == "🔎":
            await message.remove_reaction(reaction, user)
            await message.delete()
            message = await ctx.send("Searching...")
            await asyncio.sleep(2)

            if queryResponse == 'None':
                queryResponse = ''
            if titleResponse == 'None':
                titleResponse = ''
            if sourcesResponse == ['None']:
                sourcesResponse = ''
            if domainsResponse == ['None']:
                domainsResponse = ''
            if exDomainsResponse == ['None']:
                exDomainsResponse = ''
            if fromDateResponse == 'None':
                fromDateResponse = ''
            if toDateResponse == 'None':
                toDateResponse = ''
            if languageResponse == 'None':
                languageResponse = ''
            if sortByResponse == 'None':
                sortByResponse = ''

            newsArticles = await newsAPIClient.getEverything(queryResponse, titleResponse, ','.join(sourcesResponse), ','.join(domainsResponse), ','.join(exDomainsResponse), fromDateResponse, toDateResponse, languageResponse, sortByResponse)

            if newsArticles in [400, 401, 429, 500]:
                await ctx.send("Whoops, looks like something went wrong. Please try again at a later time!")
            else:
                articles = newsArticles['articles']
                pages = len(articles)
                curPage = 1

                if articles:
                    article = articles[curPage - 1]
                    title = article['title']
                    source = article['source']['name']
                    publishedAt = article['publishedAt']
                    description = article['description']
                    url = article['url']
                    image = article['urlToImage']

                    embed = discord.Embed(
                        title=f'{title}',
                        description=f'{description}".',
                        color=discord.Colour.blue()
                    )

                    embed.set_footer(text='data retrieved from: https://newsapi.org/')

                    if image:
                        embed.set_image(url=image)

                    embed.add_field(name='Source', value=source, inline=False)
                    embed.add_field(name='Publish Date', value=publishedAt, inline=False)
                    embed.add_field(name='URL', value=url, inline=False)

                    await message.edit(embed=embed, content=f'**Page [``{curPage}/{pages}``]**')

                    await message.add_reaction("⬅")
                    await message.add_reaction("➡")
                    await message.add_reaction("❌")

                    while True:
                        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"] and reaction.message.id == message.id) # waiting for a reaction to be added

                        if str(reaction.emoji) == "➡" and curPage != pages:
                            curPage += 1

                            article = articles[curPage - 1]
                            title = article['title']
                            source = article['source']['name']
                            publishedAt = article['publishedAt']
                            description = article['description']
                            url = article['url']
                            image = article['urlToImage']

                            embed = discord.Embed(
                                title=f'{title}',
                                description=f'{description}".',
                                color=discord.Colour.blue()
                            )

                            embed.set_footer(text='data retrieved from: https://newsapi.org/')

                            if image:
                                embed.set_image(url=image)

                            embed.add_field(name='Source', value=source, inline=False)
                            embed.add_field(name='Publish Date', value=publishedAt, inline=False)
                            embed.add_field(name='URL', value=url, inline=False)

                            await message.edit(embed=embed, content=f'**Page [``{curPage}/{pages}``]**')
                            await message.remove_reaction(reaction, user)

                        elif str(reaction.emoji) == "⬅" and curPage > 1:
                            curPage -= 1

                            article = articles[curPage - 1]
                            title = article['title']
                            source = article['source']['name']
                            publishedAt = article['publishedAt']
                            description = article['description']
                            url = article['url']
                            image = article['urlToImage']

                            embed = discord.Embed(
                                title=f'{title}',
                                description=f'{description}".',
                                color=discord.Colour.blue()
                            )

                            embed.set_footer(text='data retrieved from: https://newsapi.org/')
                            embed.set_image(url=image)

                            embed.add_field(name='Source', value=source, inline=False)
                            embed.add_field(name='Publish Date', value=publishedAt, inline=False)
                            embed.add_field(name='URL', value=url, inline=False)

                            await message.edit(embed=embed, content=f'**Page [``{curPage}/{pages}``]**')
                            await message.remove_reaction(reaction, user)

                        elif str(reaction.emoji) == "❌":
                            await message.remove_reaction(reaction, user)
                            await message.remove_reaction("⬅", client.user)
                            await message.remove_reaction("➡", client.user)
                            await message.remove_reaction("❌", client.user)
                            break

                        else:
                            await message.remove_reaction(reaction, user)
                            # removes reactions if the user tries to go forward on the last page or
                            # backwards on the first page
                else:
                    embed = discord.Embed(
                        title=f'News Sources',
                        description='No sources could be provided...',
                        color=discord.Colour.blue()
                    )

                    embed.add_field(name='No Data', value='No articles could be provided with this query, sorry!', inline=False)

                    await ctx.send(embed=embed)


@client.command()
async def newsCountries(ctx):
    countryList = await newsAPIClient.getCountries()
    countryNames = [f'{key} - :flag_{dict[key]}:' async for dict in aiter(countryList) async for key in aiter(dict.keys())] # retrieve all keys within the list of dictionaries
    countries = [countryNames[x:x + 20] async for x in aiter(range(0, len(countryNames), 20))]
    pages = len(countries)
    curPage = 1

    countryFormat = '\n'.join(countries[curPage - 1])
    message = await ctx.send(f"**__LIST OF COUNTRIES__ (NEWS API) | Page [`{curPage}/{pages}`]**\n{countryFormat}")

    await message.add_reaction("⬅")
    await message.add_reaction("➡")
    await message.add_reaction("❌")

    while True:
        reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user : user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"] and reaction.message.id == message.id)
        # waiting for a reaction to be added

        if str(reaction.emoji) == "➡" and curPage != pages:
            curPage += 1
            countryFormat = '\n'.join(countries[curPage - 1])
            await message.edit(content=f"**__LIST OF COUNTRIES__ (NEWS API) | Page [`{curPage}/{pages}`]**\n{countryFormat}")
            await message.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "⬅" and curPage > 1:
            curPage -= 1
            countryFormat = '\n'.join(countries[curPage - 1])
            await message.edit(content=f"**__LIST OF COUNTRIES__ (NEWS API) | Page [`{curPage}/{pages}`]**\n{countryFormat}")
            await message.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "❌":
            await message.remove_reaction(reaction, user)
            await message.remove_reaction("⬅", client.user)
            await message.remove_reaction("➡", client.user)
            await message.remove_reaction("❌", client.user)
            break

        else:
            await message.remove_reaction(reaction, user)
            # removes reactions if the user tries to go forward on the last page or
            # backwards on the first page

@client.command()
async def newsLanguages(ctx):
    languageList = await newsAPIClient.getLanguages()
    languageNames = [key async for dict in aiter(languageList) async for key in aiter(dict.keys())] # retrieve all keys within the list of dictionaries

    languageFormat = '\n'.join(languageNames)

    await ctx.send(f"**__LIST OF SUPPORTED LANGUAGES__ (NEWS API)**\n{languageFormat}")

@client.command()
async def newsCategories(ctx):
    categoryList = await newsAPIClient.getCategories()
    categoryFormat = '\n'.join(categoryList)

    await ctx.send(f"**__LIST OF NEWS CATEGORIES__ (NEWS API)**\n{categoryFormat}")

@client.command()
async def newsSortList(ctx):
    sortByList = await newsAPIClient.getSortBy()
    sortByFormat = '\n'.join(sortByList)

    await ctx.send(f"**__NEWS ARTICLES SORT__ (NEWS API)**\n{sortByFormat}")

@newsSearch.error
async def newsSearch_error(ctx, error):
    await ctx.send(error)

@newsHeadlines.error
async def newsHeadlines_error(ctx, error):
    await ctx.send(error)

@timelineGraph.error
async def timelineGraph_error(ctx, error):
    await ctx.send(error)

@dateGraph.error
async def dateGraph_error(ctx, error):
    await ctx.send(error)

client.run((os.getenv('BOT_TOKEN'))) # environment variable used for security purposes