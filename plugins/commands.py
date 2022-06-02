import os
from config import Config
from pyrogram import Client, filters
from Help.txt import pyro
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import asyncio
import sys

@Client.on_message(filters.private & filters.command('start'))
async def start(client, message):
    await message.reply_text(
        text=pyro.START_MSG.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("ℹ️ HELP", callback_data="sahayam"),
            InlineKeyboardButton("💫 ABOUT", callback_data="about")
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


@Client.on_callback_query(filters.regex(r'^start$'))
async def cb_start(bot, q):
    await q.message.edit_text(
        text=pyro.START_MSG.format(q.message.from_user.first_name),
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("ℹ️ HELP", callback_data="sahayam"),
            InlineKeyboardButton("💫 ABOUT", callback_data="about")
            ],[
            InlineKeyboardButton("🍂 SUPPORT 🍂", url="https://t.me/PYRO_BOTZ_CHAT")
            ]]
            )
        )
@Client.on_callback_query(filters.regex(r'^sahayam$'))
async def cb_help(bot, q):
    await q.message.edit_text(
        text=pyro.HELP_MSG,
        reply_markup=InlineKeyboardMarkup( [[
             InlineKeyboardButton("🔐 CLOSE", callback_data="close"),
             InlineKeyboardButton("↩️ BACK", callback_data="start")
             ]]
             )
        )

@Client.on_callback_query(filters.regex(r'^about$'))
async def cb_abt(bot, q):
    await q.message.edit_text(
        text=pyro.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup( [[
             InlineKeyboardButton("🔐 CLOSE", callback_data="close"),
             InlineKeyboardButton("↩️ BACK", callback_data="start")
             ]]
             )
        )
@Client.on_callback_query(filters.regex(r'^close$'))
async def cb_close(bot, q):
    await q.message.delete()
    try:
        await q.message.reply_to_message.delete()
    except:
        pass
