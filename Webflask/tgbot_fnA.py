#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import telebot
from apikey import tgbottoken

bot = telebot.TeleBot(tgbottoken)

# Test Environment with GFW Involved
telebot.apihelper.proxy = {'https': 'http://127.0.0.1:9099'}

def extract_arg(arg):
    return arg.split()[1]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to use the bot of @uuidgen. We love @chinanet . ")

@bot.message_handler(commands=['express'])
def cmd_express(message):
    exparg = extract_arg(message.text)

