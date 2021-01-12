import discord
from discord import Embed, Emoji
from discord.ext import commands
from typing import Union
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from api import covidAPI, newsAPI
from utils.asyncOperations import *

client = commands.Bot(command_prefix='?')
covidClient = covidAPI.CovidAPI()
newsAPI = newsAPI.NewsAPI()

@client.event
async def on_ready():
    print('Bot is online!')

@client.command()
async def CovidCountries(ctx):
   countryList = await covidClient.getCountries()
   countryNames = [f"{country['name']} - :flag_{country['code'].lower()}:" async for country in aiter(countryList)]
   countries = [countryNames[x:x + 20] for x in range(0, len(countryNames), 20)]
   pages = len(countries)
   curPage = 1

   countryFormat = '\n'.join(countries[curPage-1])
   message = await ctx.send(f"Page {curPage}/{pages}:\n{countryFormat}")

   await message.add_reaction("⬅")
   await message.add_reaction("➡")
   await message.add_reaction("❌")

   def check(reaction, user):
       return user == ctx.author and str(reaction.emoji) in ["⬅", "➡", "❌"]
       # This makes sure nobody except the command sender can interact with the "menu"

   while True:
        reaction, user = await client.wait_for("reaction_add", check = check)
        # waiting for a reaction to be added

        if str(reaction.emoji) == "➡" and curPage != pages:
            curPage += 1
            countryFormat = '\n'.join(countries[curPage - 1])
            await message.edit(content=f"Page {curPage}/{pages}:\n{countryFormat}")
            await message.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "⬅" and curPage > 1:
            curPage -= 1
            countryFormat = '\n'.join(countries[curPage - 1])
            await message.edit(content=f"Page {curPage}/{pages}:\n{countryFormat}")
            await message.remove_reaction(reaction, user)

        elif str(reaction.emoji) == "❌":
            await message.remove_reaction(reaction, user)
            await message.remove_reaction("⬅", client.user)
            await message.remove_reaction("➡", client.user)
            await message.remove_reaction("❌", client.user)
            # await message.delete()
            break

        else:
            await message.remove_reaction(reaction, user)
            # removes reactions if the user tries to go forward on the last page or
            # backwards on the first page

@client.command()
async def geturl(ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]):
    await ctx.send(emoji.url)

@client.command()
async def CountryStats(ctx, *args):
    country = ' '.join(args)
    code = await covidClient.getCountryCode(country)
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

# https://stackoverflow.com/questions/61787520/i-want-to-make-a-multi-page-help-command-using-discord-py
# https://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists

'''
@client.command()
async def plot_test(ctx, *args):
    x = args
    image = discord.File("test.png")
    plt.bar(np.arange(len(x)), x)
    plt.savefig("test.png")
    plt.close()
    await ctx.send(file=image)
    //os.remove("test.png")
'''

client.run('NzgzNzcwNDIxMjQwOTIyMTUz.X8flFg.Gp2Wo7BMw7mB5EtfiUI0OFbPAgI')