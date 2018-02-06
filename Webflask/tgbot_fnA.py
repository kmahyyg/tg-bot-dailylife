#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import telebot
from telebot import types
from apikey import tgbottoken, authedchat
from ymodules.m_aliexp import packagereq
from ymodules.m_ipip import ipsbgeo
from ymodules.m_kd100 import *

# define bot instance

bot = telebot.TeleBot(tgbottoken)

# Test Environment with GFW Involved, fuck CCP
# telebot.apihelper.proxy = {'https': 'http://127.0.0.1:9099'}

# separate arguments into list to handle with msg text
def extract_arg(arg):
    return arg.split()[1:]

# show chat id and welcome msg
@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    msgid = str(msg.chat.id)
    reply_msg = "Welcome to use the bot of @uuidgen. We love @chinanet . \n Your Private Chat ID: " + msgid
    bot.reply_to(msg, reply_msg)

# if auto detect failed, ask user to check company code here.
@bot.message_handler(commands=['expcmpy'])
def cmd_expcmpy(msg):
    msgrpy = "This command is used to check the proper company code of express. \n https://github.com/kmahyyg/life-tg-bot/blob/dev/Webflask/expno.md "
    bot.reply_to(msg, msgrpy)

# check express package status
@bot.message_handler(commands=['express'])
def cmd_express(msg):
    msgid = msg.chat.id
    if (msgid in authedchat):
        exparg = extract_arg(msg.text)
        # indexerror, import types from telebot
        # except Exception as e: bot.reply_to(message,e)
        if (len(exparg) == 1):
            cmpy = checkcmpy(exparg[0])
            if (isinstance(cmpy, int) == True):
                bot.reply_to(msg, "Cannot auto detect company. \n Use /expcmpy to check proper company code.")
            elif (cmpy == 'shunfeng'):
                checked_pkg = packagereq(exparg[0], 'SFEXPRESS')
                final = checked_pkg['result']['list'][0]
                bot.reply_to(msg, str(final))
            else:
                checked_pkg = ckkd100pkg(exparg[0], cmpy)
                bot.reply_to(msg, checked_pkg)
        elif (len(exparg) == 2):
            result1 = packagereq(exparg[0], exparg[1])
            checked_pkg = result1['result']['list'][0]
            bot.reply_to(msg, str(checked_pkg))
        else:
            bot.reply_to(msg, "Illegal Input")
    else:
        pass

# handle new mail request with my sendgrid api, xxx.edu.pl
#TODO: inline keyboard Hidden and inlineQueryCallback
@bot.message_handler(commands=['newmail'])
def mailwithsg(msg):
    cid = msg.chat.id
    mkup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(cid, "Send me some text", reply_markup=mkup)

# thanks to ip.sb, use this api to get ip's geoip info and AS num
@bot.message_handler(commands=['ipip'])
def geoipinfo(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        ipaddr = extract_arg(msg.text)
        if (ipaddr == []):
            bot.reply_to(msg, "Illegal Input.")
        else:
            repy = ipsbgeo(ipaddr)
            bot.send_message(cid, repy)
    else:
        pass


# receive mail attachments
filelist = " "
hasattachment = False
@bot.message_handler(content_types=['document'])
def handle_file(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        file_info = bot.get_file(msg.document.file_id)
        file_name = "/tmp" + str(msg.document.file_name)
        filelist = file_name
        DFILE = open(file_name, 'wb')
        downloaded_file = bot.download_file(file_info.file_path)
        DFILE.write(downloaded_file)
        DFILE.close()
        hasattachment = True
        bot.send_message(cid, "File Successfully Received.")
    else:
        pass

# polling updates, ignore errors to be focused on running
bot.polling(none_stop=True)
