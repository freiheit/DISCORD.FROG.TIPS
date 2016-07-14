#!/usr/bin/python3
# https://discordapp.com/oauth2/authorize?&client_id=203243007317639168&scope=bot&permissions=3072

import configparser
import asyncio
import discord
from discord.ext import commands
import random

import re
import sys
import six
import os
import click
from frogsay.version import __version__
from frogsay.client import open_client
from frogsay.speech import make_frog_fresco

# Parse the config and stick in global "config" var.
config = configparser.ConfigParser()
for inifile in [os.path.expanduser('~')+'/.frog.tips.ini','frog.tips.local.ini','frog.tips.ini']:
  if os.path.isfile(inifile):
    config.read(inifile)
    break # First config file wins
MAIN = config['MAIN']

def get_cache_dir(app_name='frogsay'):
    return os.path.join(click.get_app_dir(app_name), 'croak_cache')


description = '''frog tips'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.group(pass_context=True)
@asyncio.coroutine
def tip(ctx):
    with open_client(cache_dir=get_cache_dir()) as client:
        tip = client.frog_tip()
    yield from bot.say(tip)

@bot.group(pass_context=True)
@asyncio.coroutine
def fresco(ctx):
    with open_client(cache_dir=get_cache_dir()) as client:
        tip = client.frog_tip()
    terminal_width = 60
    wisdom = make_frog_fresco(tip, width=terminal_width)
    fresco = "```\n" + wisdom + "\n```"
    yield from bot.say(fresco)

# @bot.group(pass_context=True)
# @asyncio.coroutine
# def help(ctx):
#    yield from bot.say('FROG.TIPS BOT ONLY KNOWS HOW TO !TIP AND HOW TO !FRESCO')

bot.run(MAIN.get('login_token'))
