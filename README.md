# COVID-19 BOT

**COVID-19 BOT** is a bot application that tracks global statistics for COVID-19 and acts as a news search engine made entirely for Discord. The bot is coded entirely using python and mainly the [discord.py (rewrite)](https://discordpy.readthedocs.io/en/latest/) module.

**FEATURES:**
- Track global COVID-19 statistics
- Search COVID-19 related (or general) news
- Visualize data using graphs and charts

# SETTING UP THE PROJECT

In order to properly use and test the **COVID-19 BOT**, the following must be done.

## REQUIREMENTS.TXT

Firstly, ensure that you have all the packages listed within the requirements.txt file installed on your machine so that the code can smoothly run. 

To install the packages, you should be able to do the following within the command line:
>pip install `package name`==`version number`

## PYTHON

Secondly, ensure that you're running the right version of python. For example, **COVID-19 BOT** was coded on python 3.8.2---which is what you will need to run the code properly. 

## .ENV

The source code contains environment variables *(for security purposes)*, so in order for the code to work, you must have those in place so that it recognizes them. You can take a look at the `.env.example` file to see how the variables are structured. To get the password to the database, API key *(for the news API)*, and bot token you must either generate them,yourself or I will e-mail them to you. Use those values to create a `.env` file of your own.

# GENERATING OWN VARIABLES

**If I have sent you the source code including the .env file then you can skip this section.** If I have not emailed any variables or anything here's how you can set up everything.

## MONGODB

Let's start with the database. First, create an account on https://www.mongodb.com/ *(unless you already have one)*. Once you created an account *(or already have one)*, simply create a new cluster. Then you need to create a database called `NEWS API` and create collections within that database called `sources` and `miscellaneous`. Once you've completed that step you can copy and paste the following sets of data to each collection. 

### SOURCES

Due to the large number of sources in this collection, I would recommend simply just running the `NewsAPI.updateSources()` method in the `newsAPI.py` file at the bottom of the testing portion of the code to automatically insert them.

### MISCELLANEOUS

```
{"_id":"Countries","CountryList":[{"UAE":"ae"},{"Argentina":"ar"},{"Austria":"at"},{"Australia":"au"},{"Belgium":"be"},{"Bulgaria":"bg"},{"Brazil":"br"},{"Canada":"ca"},{"Switzerland":"ch"},{"China":"cn"},{"Colombia":"co"},{"Cuba":"cu"},{"Czech Republic":"cz"},{"Germany":"de"},{"Egypt":"eg"},{"France":"fr"},{"United Kingdom":"gb"},{"Greece":"gr"},{"Hong Kong":"hk"},{"Hungary":"hu"},{"Indonesia":"id"},{"Ireland":"ie"},{"Israel":"il"},{"India":"in"},{"Italy":"it"},{"Japan":"jp"},{"South Korea":"kr"},{"Lithuania":"lt"},{"Latvia":"lv"},{"Morocco":"ma"},{"Mexico":"mx"},{"Malaysia":"my"},{"Nigeria":"ng"},{"Netherlands":"nl"},{"Norway":"no"},{"New Zealand":"nz"},{"Philippines":"ph"},{"Poland":"pl"},{"Portugal":"pt"},{"Romania":"ro"},{"Serbia":"rs"},{"Russia":"ru"},{"Saudi Arabia":"sa"},{"Sweden":"se"},{"Singapore":"sg"},{"Slovenia":"si"},{"Slovakia":"sk"},{"Thailand":"th"},{"Turkey":"tr"},{"Taiwan":"tw"},{"Ukraine":"ua"},{"United States":"us"},{"Venuzuela":"ve"},{"South Africa":"za"}]}
```
```
{"_id":"Categories","CategoryList":["business","entertainment","general","health","science","sports","technology"]}
```
```
{"_id":"Languages","LanguageList":[{"Arabic":"ar"},{"German":"de"},{"English":"en"},{"Spanish":"es"},{"French":"fr"},{"Hebrew":"he"},{"Italian":"it"},{"Dutch":"nl"},{"Norwegian":"no"},{"Portuguese":"pt"},{"Russian":"ru"},{"Sami":"se"},{"Urdu":"ud"},{"Chinese":"zh"}]}
```
```
{"_id":"SortBy","SortByList":["relevancy","popularity","publishedAt"]}
```
## NEWS API KEY

Now let's get an API key for the news. Head to https://newsapi.org/ and sign up for an account if you haven't already. Once you've done that, just copy and paste the given API key to the appropriate variable in your `.env` file, and it should work fine.

## BOT TOKEN

To get a Discord bot token of your own, you need to head to https://discord.com/developers/applications *(make sure you have a discord account already)*. Then you will need to create a new application, and then go into the application settings and click on `Bot` on the left-hand menu and then `add bot`. Once the bot has been created, you can simply copy the newly generated token, put it in your `.env` file and then invite the bot to your own discord server by clicking on `OAuth2` on the left-hand menu and then configuring the parameters/permissions to generate an invitation link for your bot. 

# TESTING THE BOT

Once you're all setup, you can run the code, and the bot should be online on discord. If you're running my bot specifically you'll want to head to the following discord link: https://discord.gg/QjSexc9P45 and run the source code I've sent you and start using the bot. You can start off by doing `?help` in the chat, which will display the entire list of commands that the bot can perform and then just test away. If you're doing this with you're own bot, on your own server, just follow the same steps as well.
