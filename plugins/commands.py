import os
from config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import asyncio
import sys

START_MSG="Hi {},\nThis is a simple bot to forward all messages from one channel to other\n\n⚠️Warning\nYour account may get banned if you forward more files(from private channels). Use at Own Risk!!"

HELP_MSG="Available commands:-\n\n/index - To index a channel\n/forward - To start forwarding\n/total - Count total messages in DB\n/status - Check Current status\n/help - Help data\n/stop - To stop all running processes. \n/cleardb - clear all files in database.\n\nUse /index to index messages from a channel to database.\n\nAfter indexing you can start forwarding by using /forward.\n\n<b>Note:</b>\nYou will require the following data to index a channel:-\n\n<b>Channel Invite Link</b>:- If channel is a Private channel User needs to join channel to acces the messages. Please note that do not leave channel until forwarding completes.\n\n<b>Channel ID</b>:- If channel is a private channel you may need to enter Channel ID. Get it from @ChannelidHEXbot.\n\n<b>SKIP_NO</b>:-From where you want to start Forwarding files.Give 0 if from starting\n\n<b>Caption</b>:- Custom Caption for forwarded files. Use 0 to use default captions."

ABOUT_TXT="""

@Client.on_message(filters.private & filters.command('start'))
async def start(client, message):
    await message.reply_text(
        text=START_MSG.format(message.from_user.first_name),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("ℹ️ HELP", callback_data="help"),
            InlineKeyboardButton("💫 ABOUT", callback_data="abt")
            ],[
            InlineKeyboardButton("🍂 SUPPORT 🍂", url="https://t.me/PYRO_BOTZ_CHAT")
            ]]
            )
        )

@Client.on_message(filters.command("stop"))
async def stop_button(bot, message):

    if str(message.from_user.id) not in Config.OWNER_ID:
        return
    msg = await message.reply_text(
        text="Stoping all processes...",
        #chat_id=message.chat.id
    )
    await asyncio.sleep(1)
    await msg.edit("All Processes Stopped and Restarted")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.private & filters.command('help'))
async def help(client, message):
    await message.reply_text(
        #chat_id=message.chat.id,
        text=HELP_MSG,
        parse_mode="html")


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=START_MSG.format(query.from_user.first_name),
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("ℹ️ HELP", callback_data="help"),
                InlineKeyboardButton("💫 ABOUT", callback_data="abt")
                ],[
                InlineKeyboardButton("🍂 SUPPORT 🍂", url="https://t.me/PYRO_BOTZ_CHAT")
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=HELP_MSG,
            reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔐 CLOSE", callback_data="close"),
                 InlineKeyboardButton("↩️ BACK", callback_data="start")
                 ]]
                 )
            )

    elif data == "abt":
        await query.message.edit_text(
            text=ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔐 CLOSE", callback_data="close"),
                 InlineKeyboardButton("↩️ BACK", callback_data="start")
                 ]]
                 )
            )
    elif data == "settings":
        await query.message.edit_text(
            text="checkout and edit your settings...",
            reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("ADD CHANNEL TO FORWARD", callback_data="adcnl")
                 ],[
                 InlineKeyboardButton("SET CUSTOM CAPTION", callback_data="setcap")
                 ]]
                 )
            )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

