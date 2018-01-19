#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json, requests, logging
from apikey import tgbottoken
import telegram, sendgrid_bn
from telegram.ext import Updater, CommandHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

# Bot define using class telegram.Bot
# Test Environment

reqarg = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:9099')
bot = telegram.Bot(token=tgbottoken, request=reqarg)
updater = Updater(token=tgbottoken, request_kwargs={
    'proxy_url': 'socks5://127.0.0.1:9099/'
})

# Production Environment
# bot = telegram.Bot(token=tgbottoken)
# updater = Updater(token=tgbottoken)

dispatcher = updater.dispatcher

# Error Handler and Log

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG, filename='tgpkgbot.log')


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        print('unauthorized')
        return json.dumps({'code': 401, 'bmsg': 'unauthorized'})
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print('BadRequest')
        return json.dumps({'code': 400, 'bmsg': 'bad request'})
        # handle malformed requests - read more below!
    except TimedOut:
        print('timed out')
        return json.dumps({'code': 408, 'bmsg': 'request timed out'})
        # handle slow connection problems
    except NetworkError:
        print('network error')
        return json.dumps({'code': 502, 'bmsg': 'network error'})
        # handle other connection problems
    except ChatMigrated as e:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        return json.dumps({'code': 500, 'bmsg': 'server error'})
        # handle all other telegram related errors

dispatcher.add_error_handler(error_callback)

# Send message with commands
# works with requests on flask.

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Use this bot, use commands listed below.")


def recvedu(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="This bot cannot be used to receive mails. Contact @uuidgen if you need assistance.")

def pkg(bot, update, args):
    pass  # TODO


def sendedu(bot, update, args):
    pass  # TODO


starthandler = CommandHandler('start', start)
pkghandler = CommandHandler('exp', pkg, pass_args=True)
recvhandler = CommandHandler('recvedu', recvedu)
sendeduhandler = CommandHandler('sendedu', sendedu, pass_args=True)  # Inline Mode predicted.
dispatcher.add_handler(recvhandler)
dispatcher.add_handler(starthandler)
dispatcher.add_handler(pkghandler)
dispatcher.add_handler(sendeduhandler)

# Start the process

updater.start_polling()
updater.idle(stop_signals=7)
