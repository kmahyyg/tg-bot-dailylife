#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from socket import gethostbyname

import telebot
import logging

from telebot import types

from apikey import tgbottoken, authedchat
from ymodules.m_aliexp import packagereq
from ymodules.m_bdcall import *
from ymodules.m_douyu import *
from ymodules.m_archwiki import *
from ymodules.m_ipip import ipsbgeo
from ymodules.m_kd100 import *
from ymodules.m_sentry import *
from ymodules.m_sogouhmt import *
from ymodules.m_tuling123 import *
from ymodules.m_lwstress import *

# define bot instance
bot = telebot.TeleBot(tgbottoken)

telebot.logger.setLevel(logging.INFO)


# Test Environment with GFW Involved, fuck CCP
# telebot.apihelper.proxy = {'https': 'http://127.0.0.1:3084'}

# separate arguments into list to handle with msg text
def extract_arg(arg):
    return arg.split()[1:]


# show chat id and welcome msg
@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    msgid = str(msg.chat.id)
    reply_msg = "Welcome to use the bot of @welovezoe. We love @chinanet . \n Your Private Chat ID: " + msgid
    bot.reply_to(msg, reply_msg)


# douyu live notification status check
@bot.message_handler(commands=['douyu'])
def cmd_douyu(msg):
    msgid = str(msg.chat.id)
    try:
        roomid = extract_arg(msg.text)[0]
    except:
        roomid = 71017
    live_status = douyunty(roomid)
    bot.send_message(msgid, live_status, parse_mode='Markdown')


# if auto detect failed, ask user to check company code here.
@bot.message_handler(commands=['expcmpy'])
def cmd_expcmpy(msg):
    msgrpy = "This command is used to check the proper company code of express. \n https://www.kmahyyg.xyz/express/index.html "
    bot.reply_to(msg, msgrpy)


# check express package status
@bot.message_handler(commands=['express'])
def cmd_express(msg):
    msgid = msg.chat.id
    if (msgid in authedchat):
        exparg = extract_arg(msg.text)
        bot.send_chat_action(msgid, 'typing')
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
                autodetect_cmpy_answer = 'The company auto-detected is: **' + str(
                    cmpy) + '** . If anything went wrong, append company code after you check it via /expcmpy.'
                bot.send_message(msgid, autodetect_cmpy_answer, parse_mode='Markdown')
                checked_pkg = ckkd100pkg(exparg[0], cmpy)
                bot.reply_to(msg, checked_pkg)
        elif (len(exparg) == 2):
            result1 = packagereq(exparg[0], exparg[1])
            checked_pkg = result1['result']['list'][0]
            pkg_poster = '\nPostman: ' + result1['result']['courier'] + result1['result']['courierPhone']
            if pkg_poster == '':
                bot.reply_to(msg, str(checked_pkg))
            else:
                bot.reply_to(msg, str(checked_pkg) + pkg_poster)
        else:
            bot.reply_to(msg, "Illegal Input[ERR-EXP-ELSE]")
    else:
        pass


# thanks to ip.sb, use this api to get ip's geoip info and AS num
@bot.message_handler(commands=['ipip'])
def geoipinfo(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        ipaddrlst = extract_arg(msg.text)
        try:
            ipaddr = ipaddrlst[0]
            ipaddr = gethostbyname(ipaddr)
            bot.send_chat_action(cid, 'typing')
            repy = ipsbgeo(ipaddr)
            bot.send_message(cid, repy)
        except IndexError as ierr:
            bot.reply_to(msg, 'Illgeal Input![IERR]')
            sendlog_sent()
        except UnboundLocalError as ubderr:
            bot.reply_to(msg, 'Illegal Input![UBDERR]')
            sendlog_sent()
    else:
        pass


@bot.message_handler(commands=['disstel'])
def disssb(msg):
    cid = msg.chat.id
    tel4u = extract_arg(msg.text)
    tel4u = tel4u[0]
    telsta = check_phone(tel4u)
    bot.send_message(cid, 'This command is UNRELIABLE.')
    if telsta == False:
        bot.reply_to(msg, 'Illegal Tel Number!')
    elif isinstance(telsta, str):
        resp = start_call(telsta)
    else:
        bot.reply_to(msg, 'Sent to queue.')

    if resp == False:
        bot.reply_to(msg, 'Unknown Error!')
    elif isinstance(resp, str):
        bot.reply_to(msg, str(resp))
    elif resp == True:
        bot.reply_to(msg, 'Sent to queue!')


@bot.message_handler(commands=['wtftel'])
def checkspam(msg):
    cid = msg.chat.id
    tel4u = extract_arg(msg.text)
    try:
        tel4u = tel4u[0]
    except:
        bot.send_message(cid, "Input Error.")
        return None
    result1 = usr_subdata(tel4u)
    if result1 == '':
        result1 = '暂无Spam记录'
    result2 = ofc_belonging(tel4u)
    if result2 == 'null':
        result2 = '您可能输入错误'
    if result2 == '':
        result2 = '您输入的电话号码可能是座机'
    result = "您查询的号码来自  " + result2 + "  可能是  " + result1
    bot.reply_to(msg, str(result))


# Deprecated Google Search Feature, use @letmebot instead,  due to search result rank unreliable.
# Add get arch wiki link.
@bot.message_handler(commands=['archwiki'])
def getarchwiki(msg):
    keyw = extract_arg(msg.text)
    try:
        keyw = keyw[0:]
        keyn = ''
        keyn += ' '.join(keyw)
        retmsg = archwikilink(keyn)
    except IndexError as e:
        retmsg = e
    bot.reply_to(msg, str(retmsg))


@bot.message_handler(commands=['ddoch'])
def ddochelp(msg):
    bot.reply_to(msg, lwhelp())


@bot.message_handler(commands=['ddoc'])
def lwstddoc(msg):
    msgid = msg.chat.id
    destination = extract_arg(msg.text)[0]
    before_check = ipipcheck(destination)
    if before_check < 0:
        bot.reply_to(msg, "Server Internal Error or Invalid Request.")
        return
    elif before_check == 0:
        bot.reply_to(msg, "Sending the request to an Outside China IP.")
        result = lwattack(destination)
        bot.reply_to(msg, result)
        return
    elif before_check == 1:
        bot.reply_to(msg, "Sending the request. Be careful, to an HK/TW/MACAU IP.")
        result = lwattack(destination)
        bot.reply_to(msg, result)
        return
    elif before_check == 2:
        bot.reply_to(msg, "CHINA MAINLAND IP IS BANNED!")
        return


# Channel manager to post and forward new msg from the channel you defined.
@bot.message_handler(commands=['chanman'])
def chanmgr_permcheck(msg):
    cid = msg.chat.id
    chan_usrname = extract_arg(msg.text)
    try:
        chan_usrname = chan_usrname[0]
    except IndexError as e:
        bot.reply_to(msg, e)
        return None
    if (cid in authedchat):
        if chan_usrname[0] != '@':
            bot.send_message(cid, "Please input your channel username, start with @")
            return None
        botid = bot.get_me().id
        global postchanid
        postchanid = bot.get_chat(str(chan_usrname)).id
        try:
            botstatus = bot.get_chat_member(postchanid, botid).status
            botidentity = bot.get_chat_member(postchanid, botid).can_post_messages
            if botstatus == 'administrator' and botidentity == True:
                bot.send_message(cid, "Channel administration permission check completed and passed.")
                global requestmsg
                mkup = types.ForceReply(selective=True)
                requestmsg = bot.send_message(cid, "Please reply. Your reply msg will be send to channel.",
                                              reply_markup=mkup)
                bot.register_next_step_handler(msg, chanmgr_resendmsg)
                # https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
            else:
                bot.reply_to(msg, 'No permission to do this operation. @Line181')
        except:
            bot.reply_to(msg, 'No permission to do this operation. @Line183')
    else:
        bot.reply_to(msg, 'No permission to do this operation. @Line184')


def chanmgr_resendmsg(msg):
    if msg.reply_to_message.message_id == requestmsg.message_id:
        if msg.content_type == 'text':
            bot.send_message(postchanid, msg.text, parse_mode='Markdown')
        elif msg.content_type == 'photo':
            photolstlen = len(msg.photo)
            photoid = msg.photo[photolstlen - 1]['file_id']
            desc1 = msg.caption
            if desc1 == None:
                desc1 = ''
            bot.send_photo(postchanid, photoid, caption=desc1)
        elif msg.content_type == 'sticker':
            stker_id = msg.sticker.file_id
            bot.send_sticker(postchanid, stker_id, disable_notification=True)
        elif msg.content_type == 'document':
            doc_id = msg.document.file_id
            desc1 = msg.caption
            if desc1 == None:
                desc1 = ''
            bot.send_document(postchanid, doc_id, caption=desc1)
        elif msg.content_type == 'video':
            vid_id = msg.video.file_id
            desc1 = msg.caption
            if desc1 == None:
                desc1 = ''
            bot.send_document(postchanid, vid_id, caption=desc1)
        elif msg.content_type == 'audio':
            audi_id = msg.audio.file_id
            desc1 = msg.caption
            if desc1 == None:
                desc1 = ''
            bot.send_audio(postchanid, audi_id, caption=desc1)
        elif msg.content_type == 'voice':
            voc_id = msg.voice.file_id
            desc1 = msg.caption
            if desc1 == None:
                desc1 = ''
            bot.send_voice(postchanid, voc_id, caption=desc1)
        else:
            bot.send_message(msg.chat.id, '''
             This type of message is not supported currently for channel manager.
             If you still want to send this message, send it as a file please.
             The location & video note & media group & contact is not supported, due to privacy protection.
            ''')


# tuling123 chat API introduced, proceed all text message
@bot.message_handler(content_types=['text'])
def chattuling(msg):
    cid = msg.chat.id
    if (cid in authedchat):
        text = msg.text
        bot.send_chat_action(cid, 'typing')
        rpy = send_turing(text, cid)
        bot.reply_to(msg, rpy)
    else:
        pass


# polling updates, ignore errors to be focused on running
try:
    from os import getpid

    pid = str(getpid())
    pidfile = open('/var/run/tgbot.pid', 'w')
    pidfile.write(pid)
    pidfile.close()
    bot.polling(none_stop=True, timeout=30, interval=5)
except:
    sendlog_sent()
