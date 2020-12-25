import discord
from discord.ext import commands
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

client = commands.Bot(command_prefix='?')

@client.event
async def on_ready():
    print('Bot is online!')

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